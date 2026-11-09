"""Worker — processes pending SATUSEHAT queue jobs using an HTTP client."""
from __future__ import annotations

import json
import time
from typing import Any, Optional

import requests

from .error_classifier import ErrorClassifier
from .queue_interface import QueueInterface
from .queue_result import QueueResult
from .rate_limiter import RateLimiter
from .sqlite_queue import SqliteQueue


class Worker:
    """Queue worker — handles OAuth2 token lifecycle, retry backoff, DLQ routing, and rate limiting."""

    def __init__(
        self,
        queue: QueueInterface,
        oauth2_config: dict[str, Any],
        rate_limiter: Optional[RateLimiter] = None,
        session: Optional[requests.Session] = None,
    ) -> None:
        self._queue = queue
        self._oauth2_config = oauth2_config
        self._rate_limiter = rate_limiter or RateLimiter(300.0)
        self._session = session or requests.Session()
        self._token_cache: Optional[dict[str, Any]] = None
        self._processed = 0
        self._succeeded = 0
        self._failed = 0
        self._dlq = 0

    def process(self, limit: int = 50) -> dict[str, int]:
        """Process up to `limit` pending jobs."""
        self._processed = 0
        self._succeeded = 0
        self._failed = 0
        self._dlq = 0

        for _ in range(limit):
            job = self._queue.dequeue()
            if job is None:
                break

            result = self.handle_job(job)
            self._processed += 1

            if result.is_success():
                self._succeeded += 1
            elif result.is_dlq():
                self._dlq += 1
            else:
                self._failed += 1

        return {
            "processed": self._processed,
            "succeeded": self._succeeded,
            "failed": self._failed,
            "dlq": self._dlq,
        }

    def handle_job(self, job: dict[str, Any]) -> QueueResult:
        """Handle a single job end-to-end."""
        job_id = int(job["id"])
        attempts = int(job.get("attempts") or 0) + 1

        try:
            self._rate_limiter.wait()
            response = self._send(job)
            http_code = int(response.get("http_code") or 0)
            body = response.get("body") or ""
            location = response.get("location") or ""

            parsed: Any = body
            if isinstance(body, str) and body != "":
                try:
                    parsed = json.loads(body)
                except ValueError:
                    parsed = body

            classified = ErrorClassifier.classify(http_code, parsed)

            # 2xx -> success
            if classified["category"] == ErrorClassifier.CAT_SUCCESS:
                self._queue.mark_success(job_id, response, location)
                return QueueResult.success(job_id, response, attempts)

            # 401 -> token likely expired — invalidate + let mark_failed requeue
            if classified["category"] == ErrorClassifier.CAT_UNAUTHORIZED:
                self._token_cache = None

            # 429 with Retry-After -> honor it before requeue
            if classified["category"] == ErrorClassifier.CAT_RATE_LIMITED:
                retry_after = RateLimiter.parse_retry_after(response.get("retry_after"))
                if retry_after is not None and retry_after > 0:
                    self._queue.mark_failed(job_id, classified["detail"], response)
                    if isinstance(self._queue, SqliteQueue):
                        conn = self._queue.connection()
                        conn.execute(
                            """
                            UPDATE satusehat_queue
                            SET scheduled_at = datetime('now', ? || ' seconds'),
                                updated_at = datetime('now')
                            WHERE id = ? AND status = 'pending'
                            """,
                            (str(int(retry_after)), job_id),
                        )
                        conn.commit()
                    return QueueResult.failed(job_id, classified["detail"], response, attempts)

            # Non-retryable -> DLQ
            if not classified["retryable"]:
                self._queue.mark_dlq(job_id, classified["detail"], response)
                return QueueResult.dlq(job_id, classified["detail"], response, attempts)

            # Retryable -> failed
            self._queue.mark_failed(job_id, classified["detail"], response)
            return QueueResult.failed(job_id, classified["detail"], response, attempts)

        except Exception as exc:
            self._queue.mark_failed(job_id, str(exc), {})
            return QueueResult.failed(job_id, str(exc), {}, attempts)

    handleJob = handle_job

    def _send(self, job: dict[str, Any]) -> dict[str, Any]:
        token = self._get_token()
        method = str(job.get("method") or "POST").upper()
        fhir_url = str(self._oauth2_config.get("fhir_url") or "").rstrip("/")
        rel_url = str(job.get("url") or "").lstrip("/")
        url = f"{fhir_url}/{rel_url}"
        payload = job.get("bundle_payload")

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/fhir+json",
            "Accept": "application/fhir+json",
        }

        if method == "POST" and job.get("idempotency_key"):
            headers["If-None-Exist"] = f"uuid={job['idempotency_key']}"
        if method in ("PUT", "PATCH") and job.get("etag"):
            headers["If-Match"] = str(job["etag"])

        data_str = None
        if payload is not None and method in ("POST", "PUT", "PATCH"):
            data_str = json.dumps(payload) if not isinstance(payload, str) else payload

        resp = self._session.request(
            method=method,
            url=url,
            headers=headers,
            data=data_str,
            timeout=30,
        )

        body = resp.text or ""
        http_code = int(resp.status_code)
        retry_after = None
        if hasattr(resp, "headers") and resp.headers:
            retry_after = resp.headers.get("Retry-After") or resp.headers.get("retry-after")

        location = self._extract_location(body, http_code)
        try:
            decoded = resp.json() if body != "" else None
        except ValueError:
            decoded = None

        return {
            "body": body,
            "http_code": http_code,
            "location": location,
            "retry_after": retry_after,
            "response": decoded,
        }

    def _get_token(self) -> str:
        if (
            self._token_cache is not None
            and "expires_at" in self._token_cache
            and time.time() < float(self._token_cache["expires_at"]) - 60.0
        ):
            return str(self._token_cache["access_token"])

        self._token_cache = self._fetch_token()
        return str(self._token_cache["access_token"])

    def _fetch_token(self) -> dict[str, Any]:
        base_url = str(self._oauth2_config.get("base_url") or "").rstrip("/")
        token_url = f"{base_url}/oauth2/v1/accesstoken"
        resp = self._session.post(
            token_url,
            data={
                "grant_type": "client_credentials",
                "client_id": self._oauth2_config.get("client_id", ""),
                "client_secret": self._oauth2_config.get("client_secret", ""),
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=15,
        )
        if resp.status_code != 200 or not resp.text:
            raise RuntimeError(f"OAuth2 token fetch failed (HTTP {resp.status_code}): {resp.text}")

        try:
            data = resp.json()
        except ValueError as exc:
            raise RuntimeError(f"Invalid OAuth2 token response: {resp.text}") from exc

        if not isinstance(data, dict) or not data.get("access_token"):
            raise RuntimeError(f"Invalid OAuth2 token response: {resp.text}")

        data["expires_at"] = time.time() + int(data.get("expires_in") or 3600)
        return data

    @staticmethod
    def _extract_location(body: str, http_code: int) -> str:
        _ = http_code
        if not body:
            return ""
        try:
            data = json.loads(body)
        except ValueError:
            return ""
        if not isinstance(data, dict):
            return ""
        if data.get("fullUrl"):
            return str(data["fullUrl"])
        res = data.get("resource")
        if isinstance(res, dict) and res.get("id"):
            return f"{res.get('resourceType', '')}/{res['id']}"
        return ""
