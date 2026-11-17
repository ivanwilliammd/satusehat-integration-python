"""SqliteQueue — standalone SQLite queue implementation with no framework dependencies."""
from __future__ import annotations

import json
import sqlite3
import uuid
from typing import Any, Optional, Union

from .queue_exception import QueueException
from .queue_interface import QueueInterface


class SqliteQueue(QueueInterface):
    """Standalone SQLite queue matching the SATUSEHAT queue schema."""

    def __init__(self, db: Union[str, sqlite3.Connection] = ":memory:") -> None:
        try:
            if isinstance(db, sqlite3.Connection):
                self._conn = db
            else:
                self._conn = sqlite3.connect(db, check_same_thread=False)
            self._conn.row_factory = sqlite3.Row
            self._ensure_table()
        except sqlite3.Error as exc:
            raise QueueException.connection(str(exc), exc) from exc

    def connection(self) -> sqlite3.Connection:
        return self._conn

    pdo = connection

    def _ensure_table(self) -> None:
        sql = """
        CREATE TABLE IF NOT EXISTS satusehat_queue (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid                TEXT    UNIQUE NOT NULL,
            bundle_type         TEXT    DEFAULT 'single',
            bundle_payload      TEXT,
            resource_type       TEXT,
            method              TEXT    NOT NULL DEFAULT 'POST',
            url                 TEXT,
            status              TEXT    NOT NULL DEFAULT 'pending',
            attempts            INTEGER NOT NULL DEFAULT 0,
            max_attempts        INTEGER NOT NULL DEFAULT 5,
            last_error          TEXT,
            last_response       TEXT,
            etag                TEXT,
            idempotency_key     TEXT,
            scheduled_at        TEXT,
            completed_at        TEXT,
            dlq_reason          TEXT,
            user_id             TEXT,
            metadata            TEXT,
            created_at          TEXT    NOT NULL DEFAULT (datetime('now')),
            updated_at          TEXT    NOT NULL DEFAULT (datetime('now'))
        );
        CREATE INDEX IF NOT EXISTS idx_queue_status ON satusehat_queue(status);
        CREATE INDEX IF NOT EXISTS idx_queue_scheduled ON satusehat_queue(scheduled_at);
        CREATE INDEX IF NOT EXISTS idx_queue_uuid ON satusehat_queue(uuid);
        """
        self._conn.executescript(sql)
        self._conn.commit()

    # ── Enqueue ────────────────────────────────────────────────────

    def enqueue_bundle(
        self,
        bundle_payload: dict[str, Any],
        bundle_type: str = "transaction",
        user_id: str = "system",
        max_attempts: int = QueueInterface.DEFAULT_MAX_ATTEMPTS,
        metadata: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        job_uuid = str(uuid.uuid4())
        try:
            cur = self._conn.execute(
                """
                INSERT INTO satusehat_queue
                   (uuid, bundle_type, bundle_payload, resource_type, method, url,
                    status, attempts, max_attempts, user_id, metadata, created_at, updated_at)
                VALUES
                   (?, ?, ?, 'Bundle', 'POST', 'Bundle',
                    ?, 0, ?, ?, ?, datetime('now'), datetime('now'))
                """,
                (
                    job_uuid,
                    bundle_type,
                    json.dumps(bundle_payload),
                    self.STATUS_PENDING,
                    max_attempts,
                    user_id,
                    json.dumps(metadata) if metadata else None,
                ),
            )
            self._conn.commit()
            row = self.get(int(cur.lastrowid or 0))
            if row is None:
                raise QueueException.enqueue("Failed to retrieve newly enqueued bundle job")
            return row
        except sqlite3.Error as exc:
            raise QueueException.enqueue(str(exc), exc) from exc

    enqueueBundle = enqueue_bundle

    def enqueue(
        self,
        method: str,
        resource_type: str,
        url: str,
        payload: Optional[dict[str, Any]] = None,
        etag: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        user_id: str = "system",
        max_attempts: int = QueueInterface.DEFAULT_MAX_ATTEMPTS,
        metadata: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        job_uuid = idempotency_key or str(uuid.uuid4())
        try:
            cur = self._conn.execute(
                """
                INSERT INTO satusehat_queue
                   (uuid, bundle_type, bundle_payload, resource_type, method, url,
                    status, attempts, max_attempts, etag, idempotency_key, user_id, metadata,
                    created_at, updated_at)
                VALUES
                   (?, 'single', ?, ?, ?, ?,
                    ?, 0, ?, ?, ?, ?, ?,
                    datetime('now'), datetime('now'))
                """,
                (
                    job_uuid,
                    json.dumps(payload) if payload is not None else None,
                    resource_type,
                    method.upper(),
                    url,
                    self.STATUS_PENDING,
                    max_attempts,
                    etag,
                    idempotency_key,
                    user_id,
                    json.dumps(metadata) if metadata else None,
                ),
            )
            self._conn.commit()
            row = self.get(int(cur.lastrowid or 0))
            if row is None:
                raise QueueException.enqueue("Failed to retrieve newly enqueued job")
            return row
        except sqlite3.Error as exc:
            raise QueueException.enqueue(str(exc), exc) from exc

    # ── Dequeue ───────────────────────────────────────────────────

    def dequeue(self) -> Optional[dict[str, Any]]:
        try:
            cur = self._conn.execute(
                """
                SELECT * FROM satusehat_queue
                WHERE status = ?
                  AND (scheduled_at IS NULL OR scheduled_at <= datetime('now'))
                ORDER BY id ASC
                LIMIT 1
                """,
                (self.STATUS_PENDING,),
            )
            row = cur.fetchone()
            if row is None:
                return None

            row_dict = dict(row)
            upd = self._conn.execute(
                """
                UPDATE satusehat_queue
                SET status = ?, attempts = attempts + 1, updated_at = datetime('now')
                WHERE id = ? AND status = ?
                """,
                (self.STATUS_PROCESSING, row_dict["id"], self.STATUS_PENDING),
            )
            if upd.rowcount == 0:
                self._conn.rollback()
                return None

            self._conn.commit()
            return self._decode(row_dict)
        except sqlite3.Error as exc:
            self._conn.rollback()
            raise QueueException.dequeue(str(exc), exc) from exc

    # ── Update ─────────────────────────────────────────────────────

    def mark_success(
        self,
        job_id: int,
        response: Optional[dict[str, Any]] = None,
        location: Optional[str] = "",
    ) -> bool:
        resp_copy = dict(response or {})
        resp_copy["location"] = location
        try:
            cur = self._conn.execute(
                """
                UPDATE satusehat_queue
                SET status = ?, last_response = ?,
                    completed_at = datetime('now'), last_error = NULL, updated_at = datetime('now')
                WHERE id = ?
                """,
                (self.STATUS_SUCCESS, json.dumps(resp_copy), job_id),
            )
            self._conn.commit()
            return cur.rowcount > 0
        except sqlite3.Error as exc:
            raise QueueException.update(str(exc), exc) from exc

    markSuccess = mark_success

    def mark_failed(
        self,
        job_id: int,
        error: str,
        response: Optional[dict[str, Any]] = None,
    ) -> bool:
        row = self.get(job_id)
        if not row:
            return False

        if int(row["attempts"]) >= int(row["max_attempts"]):
            return self.mark_dlq(job_id, error, response)

        backoff_seconds = min(300, int(row["attempts"]) ** 2 * 30)
        try:
            cur = self._conn.execute(
                """
                UPDATE satusehat_queue
                SET status = ?, last_error = ?,
                    last_response = ?,
                    scheduled_at = datetime('now', ? || ' seconds'),
                    updated_at = datetime('now')
                WHERE id = ?
                """,
                (
                    self.STATUS_PENDING,
                    error,
                    json.dumps(response or {}),
                    str(backoff_seconds),
                    job_id,
                ),
            )
            self._conn.commit()
            return cur.rowcount > 0
        except sqlite3.Error as exc:
            raise QueueException.update(str(exc), exc) from exc

    markFailed = mark_failed

    def mark_dlq(
        self,
        job_id: int,
        reason: str,
        response: Optional[dict[str, Any]] = None,
    ) -> bool:
        try:
            cur = self._conn.execute(
                """
                UPDATE satusehat_queue
                SET status = ?, dlq_reason = ?,
                    last_error = ?, last_response = ?,
                    updated_at = datetime('now')
                WHERE id = ?
                """,
                (
                    self.STATUS_DLQ,
                    reason,
                    reason,
                    json.dumps(response or {}),
                    job_id,
                ),
            )
            self._conn.commit()
            return cur.rowcount > 0
        except sqlite3.Error as exc:
            raise QueueException.update(str(exc), exc) from exc

    markDlq = mark_dlq

    def reset(self, job_id: int) -> bool:
        try:
            cur = self._conn.execute(
                """
                UPDATE satusehat_queue
                SET status = ?, attempts = 0, scheduled_at = NULL,
                    last_error = NULL, dlq_reason = NULL, updated_at = datetime('now')
                WHERE id = ?
                """,
                (self.STATUS_PENDING, job_id),
            )
            self._conn.commit()
            return cur.rowcount > 0
        except sqlite3.Error as exc:
            raise QueueException.update(str(exc), exc) from exc

    # ── Status helpers ──────────────────────────────────────────────

    def get(self, job_id: int) -> Optional[dict[str, Any]]:
        cur = self._conn.execute("SELECT * FROM satusehat_queue WHERE id = ?", (job_id,))
        row = cur.fetchone()
        return self._decode(dict(row)) if row else None

    def pending_count(self) -> int:
        cur = self._conn.execute(
            """
            SELECT COUNT(*) FROM satusehat_queue
            WHERE status = 'pending'
              AND (scheduled_at IS NULL OR scheduled_at <= datetime('now'))
            """
        )
        row = cur.fetchone()
        return int(row[0]) if row else 0

    pendingCount = pending_count

    def dlq_count(self) -> int:
        cur = self._conn.execute("SELECT COUNT(*) FROM satusehat_queue WHERE status = 'dlq'")
        row = cur.fetchone()
        return int(row[0]) if row else 0

    dlqCount = dlq_count

    def stats(self) -> dict[str, int]:
        cur = self._conn.execute(
            "SELECT status, COUNT(*) as cnt FROM satusehat_queue GROUP BY status"
        )
        out = {"pending": 0, "processing": 0, "success": 0, "failed": 0, "dlq": 0}
        for row in cur.fetchall():
            out[str(row["status"])] = int(row["cnt"])
        return out

    def pending_jobs(self, limit: int = 20) -> list[dict[str, Any]]:
        cur = self._conn.execute(
            """
            SELECT * FROM satusehat_queue
            WHERE status = 'pending'
              AND (scheduled_at IS NULL OR scheduled_at <= datetime('now'))
            ORDER BY id ASC LIMIT ?
            """,
            (limit,),
        )
        return [self._decode(dict(r)) for r in cur.fetchall()]

    pendingJobs = pending_jobs

    def dlq_jobs(self, limit: int = 20) -> list[dict[str, Any]]:
        cur = self._conn.execute(
            "SELECT * FROM satusehat_queue WHERE status = 'dlq' ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        return [self._decode(dict(r)) for r in cur.fetchall()]

    dlqJobs = dlq_jobs

    # ── Admin ─────────────────────────────────────────────────────

    def reset_all(self) -> int:
        cur = self._conn.execute(
            """
            UPDATE satusehat_queue
            SET status = 'pending', attempts = 0, scheduled_at = NULL,
                last_error = NULL, dlq_reason = NULL, updated_at = datetime('now')
            WHERE status IN ('failed', 'dlq')
            """
        )
        self._conn.commit()
        return int(cur.rowcount)

    resetAll = reset_all

    def purge_success(self, days: int = 7) -> int:
        cur = self._conn.execute(
            """
            DELETE FROM satusehat_queue
            WHERE status = 'success'
              AND completed_at <= datetime('now', ? || ' days')
            """,
            (str(-days),),
        )
        self._conn.commit()
        return int(cur.rowcount)

    purgeSuccess = purge_success

    @staticmethod
    def _decode(row: dict[str, Any]) -> dict[str, Any]:
        for key in ("bundle_payload", "last_response", "metadata"):
            val = row.get(key)
            if isinstance(val, str) and val != "":
                try:
                    row[key] = json.loads(val)
                except ValueError:
                    pass
        return row
