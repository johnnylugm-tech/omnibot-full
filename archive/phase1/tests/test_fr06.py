"""FR-06: Rate Limiter — Token Bucket.

[FR-06] Acceptance criteria:
  - Per-user token bucket with configurable rate and capacity
  - Requests within limit are allowed
  - Requests exceeding limit are rejected
  - Tokens refill over time

Citations: SRS.md FR-06 section
"""

import time

from omnibot.rate_limiter import TokenBucket, RateLimiter


def test_token_bucket_allows_within_limit():
    """Bucket with 5 tokens allows 5 requests."""
    bucket = TokenBucket(capacity=5, refill_rate=1.0)
    for _ in range(5):
        assert bucket.consume() is True
    assert bucket.consume() is False


def test_token_bucket_refills_over_time():
    """Tokens refill at the configured rate."""
    bucket = TokenBucket(capacity=2, refill_rate=10.0)  # 10 tokens/sec
    assert bucket.consume() is True
    assert bucket.consume() is True
    assert bucket.consume() is False
    time.sleep(0.15)  # wait for ~1.5 tokens to refill
    assert bucket.consume() is True


def test_rate_limiter_per_user_isolation():
    """Each user has an independent token bucket."""
    limiter = RateLimiter(default_capacity=3, default_refill_rate=1.0)
    assert limiter.allow("user_a") is True
    assert limiter.allow("user_a") is True
    assert limiter.allow("user_a") is True
    assert limiter.allow("user_a") is False  # user_a exhausted
    assert limiter.allow("user_b") is True   # user_b still has tokens


def test_rate_limiter_new_user_gets_full_bucket():
    """New users start with a full bucket."""
    limiter = RateLimiter(default_capacity=5, default_refill_rate=1.0)
    for _ in range(5):
        assert limiter.allow("new_user") is True
    assert limiter.allow("new_user") is False


def test_rate_limiter_capacity_zero_blocks_all():
    """Capacity 0 blocks all requests."""
    limiter = RateLimiter(default_capacity=0, default_refill_rate=1.0)
    assert limiter.allow("anyone") is False
