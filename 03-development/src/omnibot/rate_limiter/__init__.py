"""[FR-06] Rate Limiter — Token Bucket algorithm.

Per-user token bucket rate limiting. Thread-safe via lock per bucket.

Citations: SRS.md FR-06 section
"""

import time
import threading
from typing import Dict


class TokenBucket:
    """Token bucket for a single user.

    Capacity: max tokens the bucket can hold.
    Refill rate: tokens added per second.
    """

    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self._tokens = float(capacity)
        self._last_refill = time.monotonic()
        self._lock = threading.Lock()

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self.capacity, self._tokens + elapsed * self.refill_rate)
        self._last_refill = now

    def consume(self) -> bool:
        """Consume 1 token. Returns True if allowed, False if rate limited."""
        with self._lock:
            self._refill()
            if self._tokens >= 1.0:
                self._tokens -= 1.0
                return True
            return False


class RateLimiter:
    """Per-user rate limiter backed by TokenBucket instances."""

    def __init__(self, default_capacity: int = 10, default_refill_rate: float = 1.0):
        self.default_capacity = default_capacity
        self.default_refill_rate = default_refill_rate
        self._buckets: Dict[str, TokenBucket] = {}
        self._lock = threading.Lock()

    def allow(self, user_id: str) -> bool:
        """Check if a request from user_id is allowed."""
        with self._lock:
            bucket = self._buckets.get(user_id)
            if bucket is None:
                bucket = TokenBucket(self.default_capacity, self.default_refill_rate)
                self._buckets[user_id] = bucket
        return bucket.consume()
