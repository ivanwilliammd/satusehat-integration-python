"""QueueResult — immutable result of a queue job processed by Worker."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass(frozen=True)
class QueueResult:
    """Immutable result of a queue job processed by Worker."""

    id: int
    status: str
    error: Optional[str]
    response: Optional[dict[str, Any]]
    attempts: int

    STATUS_SUCCESS = "success"
    STATUS_FAILED = "failed"
    STATUS_DLQ = "dlq"

    @classmethod
    def success(
        cls,
        job_id: int,
        response: Optional[dict[str, Any]] = None,
        attempts: int = 1,
    ) -> QueueResult:
        return cls(job_id, cls.STATUS_SUCCESS, None, response or {}, attempts)

    @classmethod
    def failed(
        cls,
        job_id: int,
        error: str,
        response: Optional[dict[str, Any]] = None,
        attempts: int = 1,
    ) -> QueueResult:
        return cls(job_id, cls.STATUS_FAILED, error, response or {}, attempts)

    @classmethod
    def dlq(
        cls,
        job_id: int,
        reason: str,
        response: Optional[dict[str, Any]] = None,
        attempts: int = 0,
    ) -> QueueResult:
        return cls(job_id, cls.STATUS_DLQ, reason, response or {}, attempts)

    def is_success(self) -> bool:
        return self.status == self.STATUS_SUCCESS

    isSuccess = is_success

    def is_failed(self) -> bool:
        return self.status == self.STATUS_FAILED

    isFailed = is_failed

    def is_dlq(self) -> bool:
        return self.status == self.STATUS_DLQ

    isDlq = is_dlq

    def is_retriable(self) -> bool:
        return self.is_failed() and self.attempts < 5

    isRetriable = is_retriable
