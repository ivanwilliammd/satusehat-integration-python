"""RateLimiter — per-process rate limiter using sliding window."""
from __future__ import annotations

import re
import time
from email.utils import parsedate_to_datetime
from typing import Callable, Optional


class RateLimiter:
    """Prevents hammering SATUSEHAT API when processing batches."""

    def __init__(self, rpm: float = 300.0, sleep_fn: Optional[Callable[[float], None]] = None) -> None:
        self.rpm = max(1.0, float(rpm))
        self.interval = 60.0 / self.rpm
        self.last_request_at: Optional[float] = None
        self._sleep_fn = sleep_fn or time.sleep

    def wait(self) -> None:
        """Block until a request slot is available."""
        if self.last_request_at is not None:
            elapsed = time.time() - self.last_request_at
            remaining = self.interval - elapsed
            if remaining > 0:
                self._sleep_fn(remaining)
        self.last_request_at = time.time()

    @staticmethod
    def parse_retry_after(header: Optional[str]) -> Optional[float]:
        """Seconds to wait based on Retry-After header value."""
        if header is None or header.strip() == "":
            return None

        trimmed = header.strip()

        # HTTP-date format: "Wed, 31 Oct 2026 12:00:00 GMT"
        if re.match(r"^[A-Z][a-z]{2},", trimmed):
            try:
                dt = parsedate_to_datetime(trimmed)
                return max(0.0, dt.timestamp() - time.time())
            except Exception:
                return None

        # Integer seconds
        if re.match(r"^-?\d+$", trimmed):
            try:
                return float(int(trimmed))
            except ValueError:
                return None

        return None

    parseRetryAfter = parse_retry_after
