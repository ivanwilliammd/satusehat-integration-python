import time

class RateLimiter:
    def __init__(self, rpm: float = 300):
        self.rpm = max(1.0, rpm)
        self.interval = 60.0 / self.rpm
        self.last_request_at = None

    def wait(self):
        if self.last_request_at is not None:
            elapsed = time.time() - self.last_request_at
            remaining = self.interval - elapsed
            if remaining > 0:
                time.sleep(remaining)
        self.last_request_at = time.time()
