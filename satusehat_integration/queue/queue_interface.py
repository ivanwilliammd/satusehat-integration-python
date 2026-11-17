"""QueueInterface — framework-agnostic contract for the SATUSEHAT queue."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional


class QueueInterface(ABC):
    """Contract for SATUSEHAT queue implementations.

    Status flow: pending -> processing -> success | failed (retry) | dlq
    """

    STATUS_PENDING = "pending"
    STATUS_PROCESSING = "processing"
    STATUS_SUCCESS = "success"
    STATUS_FAILED = "failed"
    STATUS_DLQ = "dlq"

    DEFAULT_MAX_ATTEMPTS = 5

    @abstractmethod
    def enqueue_bundle(
        self,
        bundle_payload: dict[str, Any],
        bundle_type: str = "transaction",
        user_id: str = "system",
        max_attempts: int = DEFAULT_MAX_ATTEMPTS,
        metadata: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        raise NotImplementedError

    enqueueBundle = enqueue_bundle

    @abstractmethod
    def enqueue(
        self,
        method: str,
        resource_type: str,
        url: str,
        payload: Optional[dict[str, Any]] = None,
        etag: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        user_id: str = "system",
        max_attempts: int = DEFAULT_MAX_ATTEMPTS,
        metadata: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def dequeue(self) -> Optional[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def mark_success(
        self,
        job_id: int,
        response: Optional[dict[str, Any]] = None,
        location: Optional[str] = "",
    ) -> bool:
        raise NotImplementedError

    markSuccess = mark_success

    @abstractmethod
    def mark_failed(
        self,
        job_id: int,
        error: str,
        response: Optional[dict[str, Any]] = None,
    ) -> bool:
        raise NotImplementedError

    markFailed = mark_failed

    @abstractmethod
    def mark_dlq(
        self,
        job_id: int,
        reason: str,
        response: Optional[dict[str, Any]] = None,
    ) -> bool:
        raise NotImplementedError

    markDlq = mark_dlq

    @abstractmethod
    def reset(self, job_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get(self, job_id: int) -> Optional[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def pending_count(self) -> int:
        raise NotImplementedError

    pendingCount = pending_count

    @abstractmethod
    def dlq_count(self) -> int:
        raise NotImplementedError

    dlqCount = dlq_count

    @abstractmethod
    def stats(self) -> dict[str, int]:
        raise NotImplementedError

    @abstractmethod
    def pending_jobs(self, limit: int = 20) -> list[dict[str, Any]]:
        raise NotImplementedError

    pendingJobs = pending_jobs

    @abstractmethod
    def dlq_jobs(self, limit: int = 20) -> list[dict[str, Any]]:
        raise NotImplementedError

    dlqJobs = dlq_jobs

    @abstractmethod
    def reset_all(self) -> int:
        raise NotImplementedError

    resetAll = reset_all

    @abstractmethod
    def purge_success(self, days: int = 7) -> int:
        raise NotImplementedError

    purgeSuccess = purge_success
