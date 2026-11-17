"""QueueMonitor — queue monitoring: stats, health check, and top error analytics."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from .sqlite_queue import SqliteQueue


class QueueStats:
    """Backwards-compatible queue statistics container."""

    def __init__(self, pending: int = 0, success: int = 0, dlq: int = 0) -> None:
        self.pending = pending
        self.success = success
        self.dlq = dlq


class QueueMonitor:
    """Queue monitoring — stats, health, error analytics."""

    def __init__(self, queue: SqliteQueue) -> None:
        self._queue = queue

    def summary(self) -> dict[str, Any]:
        """High-level summary: counts, rates, queue depth."""
        stats = self._queue.stats()
        total = sum(stats.values())
        success_rate = round(stats["success"] / total * 100.0, 1) if total > 0 else 0.0
        oldest = self._oldest_pending()

        return {
            "total": total,
            "pending": stats["pending"],
            "processing": stats["processing"],
            "success": stats["success"],
            "failed": stats["failed"],
            "dlq": stats["dlq"],
            "success_rate": success_rate,
            "oldest_pending_at": oldest.get("created_at") if oldest else None,
            "dlq_count": stats["dlq"],
        }

    def health_check(self) -> dict[str, Any]:
        """Health check — returns status + recommendations."""
        stats = self._queue.stats()
        status = "healthy"
        issues: list[str] = []

        if stats["dlq"] > 0 and stats["dlq"] >= stats["success"]:
            status = "critical"
            issues.append("DLQ count >= success count — investigate failed jobs")
        elif stats["dlq"] > 20:
            status = "degraded"
            issues.append(f"{stats['dlq']} jobs in DLQ — review and requeue or fix payload")

        if stats["pending"] > 500:
            status = "degraded" if status == "healthy" else status
            issues.append(f"{stats['pending']} pending jobs — worker may be idle or under-provisioned")

        oldest = self._oldest_pending()
        if oldest and oldest.get("created_at"):
            try:
                created_dt = datetime.fromisoformat(str(oldest["created_at"])).replace(tzinfo=timezone.utc)
                now_dt = datetime.now(timezone.utc)
                age_minutes = (now_dt - created_dt).total_seconds() / 60.0
                if age_minutes > 30 and stats["processing"] == 0:
                    status = "degraded" if status == "healthy" else status
                    issues.append(f"Oldest pending job is {int(age_minutes)}min old — worker may be down")
            except ValueError:
                pass

        return {
            "status": status,
            "issues": issues,
            "summary": self.summary(),
        }

    healthCheck = health_check

    def top_errors(self, limit: int = 10) -> list[dict[str, Any]]:
        """Top error categories from failed + DLQ jobs."""
        conn = self._queue.connection()
        cur = conn.execute(
            """
            SELECT last_error, COUNT(*) as cnt
            FROM satusehat_queue
            WHERE status IN ('failed', 'dlq') AND last_error IS NOT NULL
            GROUP BY last_error
            ORDER BY cnt DESC
            LIMIT ?
            """,
            (limit,),
        )
        return [{"last_error": str(r["last_error"]), "cnt": int(r["cnt"])} for r in cur.fetchall()]

    topErrors = top_errors

    def _oldest_pending(self) -> Optional[dict[str, Any]]:
        conn = self._queue.connection()
        cur = conn.execute(
            """
            SELECT id, created_at, method, url, status, attempts
            FROM satusehat_queue
            WHERE status IN ('pending', 'failed')
            ORDER BY created_at ASC
            LIMIT 1
            """
        )
        row = cur.fetchone()
        return dict(row) if row else None
