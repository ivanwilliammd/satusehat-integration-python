"""QueueException — thrown by queue operations on unrecoverable errors."""
from __future__ import annotations

from typing import Optional


class QueueException(Exception):
    """Exception raised by SATUSEHAT queue operations."""

    E_CONNECTION = 1
    E_ENQUEUE = 2
    E_DEQUEUE = 3
    E_UPDATE = 4

    def __init__(self, message: str, code: int = 0, cause: Optional[BaseException] = None) -> None:
        super().__init__(message)
        self.code = code
        self.__cause__ = cause

    @classmethod
    def connection(cls, msg: str, prev: Optional[BaseException] = None) -> QueueException:
        return cls(f"Queue connection error: {msg}", cls.E_CONNECTION, prev)

    @classmethod
    def enqueue(cls, msg: str, prev: Optional[BaseException] = None) -> QueueException:
        return cls(f"Failed to enqueue: {msg}", cls.E_ENQUEUE, prev)

    @classmethod
    def dequeue(cls, msg: str, prev: Optional[BaseException] = None) -> QueueException:
        return cls(f"Failed to dequeue: {msg}", cls.E_DEQUEUE, prev)

    @classmethod
    def update(cls, msg: str, prev: Optional[BaseException] = None) -> QueueException:
        return cls(f"Failed to update job: {msg}", cls.E_UPDATE, prev)
