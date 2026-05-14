"""[FR-06] Rate Limiter — Token Bucket algorithm.

Per-user token bucket rate limiting. Thread-safe via lock per bucket.

Citations: SRS.md FR-06 section
"""

import time
import threading
from typing import Dict
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class TokenBucket:
    """Token bucket for a single user.

    Capacity: max tokens the bucket can hold.
    Refill rate: tokens added per second.
    """

    def xǁTokenBucketǁ__init____mutmut_orig(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self._tokens = float(capacity)
        self._last_refill = time.monotonic()
        self._lock = threading.Lock()

    def xǁTokenBucketǁ__init____mutmut_1(self, capacity: int, refill_rate: float):
        self.capacity = None
        self.refill_rate = refill_rate
        self._tokens = float(capacity)
        self._last_refill = time.monotonic()
        self._lock = threading.Lock()

    def xǁTokenBucketǁ__init____mutmut_2(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = None
        self._tokens = float(capacity)
        self._last_refill = time.monotonic()
        self._lock = threading.Lock()

    def xǁTokenBucketǁ__init____mutmut_3(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self._tokens = None
        self._last_refill = time.monotonic()
        self._lock = threading.Lock()

    def xǁTokenBucketǁ__init____mutmut_4(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self._tokens = float(None)
        self._last_refill = time.monotonic()
        self._lock = threading.Lock()

    def xǁTokenBucketǁ__init____mutmut_5(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self._tokens = float(capacity)
        self._last_refill = None
        self._lock = threading.Lock()

    def xǁTokenBucketǁ__init____mutmut_6(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self._tokens = float(capacity)
        self._last_refill = time.monotonic()
        self._lock = None
    
    xǁTokenBucketǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTokenBucketǁ__init____mutmut_1': xǁTokenBucketǁ__init____mutmut_1, 
        'xǁTokenBucketǁ__init____mutmut_2': xǁTokenBucketǁ__init____mutmut_2, 
        'xǁTokenBucketǁ__init____mutmut_3': xǁTokenBucketǁ__init____mutmut_3, 
        'xǁTokenBucketǁ__init____mutmut_4': xǁTokenBucketǁ__init____mutmut_4, 
        'xǁTokenBucketǁ__init____mutmut_5': xǁTokenBucketǁ__init____mutmut_5, 
        'xǁTokenBucketǁ__init____mutmut_6': xǁTokenBucketǁ__init____mutmut_6
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTokenBucketǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁTokenBucketǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁTokenBucketǁ__init____mutmut_orig)
    xǁTokenBucketǁ__init____mutmut_orig.__name__ = 'xǁTokenBucketǁ__init__'

    def xǁTokenBucketǁ_refill__mutmut_orig(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self.capacity, self._tokens + elapsed * self.refill_rate)
        self._last_refill = now

    def xǁTokenBucketǁ_refill__mutmut_1(self) -> None:
        now = None
        elapsed = now - self._last_refill
        self._tokens = min(self.capacity, self._tokens + elapsed * self.refill_rate)
        self._last_refill = now

    def xǁTokenBucketǁ_refill__mutmut_2(self) -> None:
        now = time.monotonic()
        elapsed = None
        self._tokens = min(self.capacity, self._tokens + elapsed * self.refill_rate)
        self._last_refill = now

    def xǁTokenBucketǁ_refill__mutmut_3(self) -> None:
        now = time.monotonic()
        elapsed = now + self._last_refill
        self._tokens = min(self.capacity, self._tokens + elapsed * self.refill_rate)
        self._last_refill = now

    def xǁTokenBucketǁ_refill__mutmut_4(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = None
        self._last_refill = now

    def xǁTokenBucketǁ_refill__mutmut_5(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(None, self._tokens + elapsed * self.refill_rate)
        self._last_refill = now

    def xǁTokenBucketǁ_refill__mutmut_6(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self.capacity, None)
        self._last_refill = now

    def xǁTokenBucketǁ_refill__mutmut_7(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self._tokens + elapsed * self.refill_rate)
        self._last_refill = now

    def xǁTokenBucketǁ_refill__mutmut_8(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self.capacity, )
        self._last_refill = now

    def xǁTokenBucketǁ_refill__mutmut_9(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self.capacity, self._tokens - elapsed * self.refill_rate)
        self._last_refill = now

    def xǁTokenBucketǁ_refill__mutmut_10(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self.capacity, self._tokens + elapsed / self.refill_rate)
        self._last_refill = now

    def xǁTokenBucketǁ_refill__mutmut_11(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self.capacity, self._tokens + elapsed * self.refill_rate)
        self._last_refill = None
    
    xǁTokenBucketǁ_refill__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTokenBucketǁ_refill__mutmut_1': xǁTokenBucketǁ_refill__mutmut_1, 
        'xǁTokenBucketǁ_refill__mutmut_2': xǁTokenBucketǁ_refill__mutmut_2, 
        'xǁTokenBucketǁ_refill__mutmut_3': xǁTokenBucketǁ_refill__mutmut_3, 
        'xǁTokenBucketǁ_refill__mutmut_4': xǁTokenBucketǁ_refill__mutmut_4, 
        'xǁTokenBucketǁ_refill__mutmut_5': xǁTokenBucketǁ_refill__mutmut_5, 
        'xǁTokenBucketǁ_refill__mutmut_6': xǁTokenBucketǁ_refill__mutmut_6, 
        'xǁTokenBucketǁ_refill__mutmut_7': xǁTokenBucketǁ_refill__mutmut_7, 
        'xǁTokenBucketǁ_refill__mutmut_8': xǁTokenBucketǁ_refill__mutmut_8, 
        'xǁTokenBucketǁ_refill__mutmut_9': xǁTokenBucketǁ_refill__mutmut_9, 
        'xǁTokenBucketǁ_refill__mutmut_10': xǁTokenBucketǁ_refill__mutmut_10, 
        'xǁTokenBucketǁ_refill__mutmut_11': xǁTokenBucketǁ_refill__mutmut_11
    }
    
    def _refill(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTokenBucketǁ_refill__mutmut_orig"), object.__getattribute__(self, "xǁTokenBucketǁ_refill__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _refill.__signature__ = _mutmut_signature(xǁTokenBucketǁ_refill__mutmut_orig)
    xǁTokenBucketǁ_refill__mutmut_orig.__name__ = 'xǁTokenBucketǁ_refill'

    def xǁTokenBucketǁconsume__mutmut_orig(self) -> bool:
        """Consume 1 token. Returns True if allowed, False if rate limited."""
        with self._lock:
            self._refill()
            if self._tokens >= 1.0:
                self._tokens -= 1.0
                return True
            return False

    def xǁTokenBucketǁconsume__mutmut_1(self) -> bool:
        """Consume 1 token. Returns True if allowed, False if rate limited."""
        with self._lock:
            self._refill()
            if self._tokens > 1.0:
                self._tokens -= 1.0
                return True
            return False

    def xǁTokenBucketǁconsume__mutmut_2(self) -> bool:
        """Consume 1 token. Returns True if allowed, False if rate limited."""
        with self._lock:
            self._refill()
            if self._tokens >= 2.0:
                self._tokens -= 1.0
                return True
            return False

    def xǁTokenBucketǁconsume__mutmut_3(self) -> bool:
        """Consume 1 token. Returns True if allowed, False if rate limited."""
        with self._lock:
            self._refill()
            if self._tokens >= 1.0:
                self._tokens = 1.0
                return True
            return False

    def xǁTokenBucketǁconsume__mutmut_4(self) -> bool:
        """Consume 1 token. Returns True if allowed, False if rate limited."""
        with self._lock:
            self._refill()
            if self._tokens >= 1.0:
                self._tokens += 1.0
                return True
            return False

    def xǁTokenBucketǁconsume__mutmut_5(self) -> bool:
        """Consume 1 token. Returns True if allowed, False if rate limited."""
        with self._lock:
            self._refill()
            if self._tokens >= 1.0:
                self._tokens -= 2.0
                return True
            return False

    def xǁTokenBucketǁconsume__mutmut_6(self) -> bool:
        """Consume 1 token. Returns True if allowed, False if rate limited."""
        with self._lock:
            self._refill()
            if self._tokens >= 1.0:
                self._tokens -= 1.0
                return False
            return False

    def xǁTokenBucketǁconsume__mutmut_7(self) -> bool:
        """Consume 1 token. Returns True if allowed, False if rate limited."""
        with self._lock:
            self._refill()
            if self._tokens >= 1.0:
                self._tokens -= 1.0
                return True
            return True
    
    xǁTokenBucketǁconsume__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTokenBucketǁconsume__mutmut_1': xǁTokenBucketǁconsume__mutmut_1, 
        'xǁTokenBucketǁconsume__mutmut_2': xǁTokenBucketǁconsume__mutmut_2, 
        'xǁTokenBucketǁconsume__mutmut_3': xǁTokenBucketǁconsume__mutmut_3, 
        'xǁTokenBucketǁconsume__mutmut_4': xǁTokenBucketǁconsume__mutmut_4, 
        'xǁTokenBucketǁconsume__mutmut_5': xǁTokenBucketǁconsume__mutmut_5, 
        'xǁTokenBucketǁconsume__mutmut_6': xǁTokenBucketǁconsume__mutmut_6, 
        'xǁTokenBucketǁconsume__mutmut_7': xǁTokenBucketǁconsume__mutmut_7
    }
    
    def consume(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTokenBucketǁconsume__mutmut_orig"), object.__getattribute__(self, "xǁTokenBucketǁconsume__mutmut_mutants"), args, kwargs, self)
        return result 
    
    consume.__signature__ = _mutmut_signature(xǁTokenBucketǁconsume__mutmut_orig)
    xǁTokenBucketǁconsume__mutmut_orig.__name__ = 'xǁTokenBucketǁconsume'


class RateLimiter:
    """Per-user rate limiter backed by TokenBucket instances."""

    def xǁRateLimiterǁ__init____mutmut_orig(self, default_capacity: int = 100, default_refill_rate: float = 100.0):
        self.default_capacity = default_capacity
        self.default_refill_rate = default_refill_rate
        self._buckets: Dict[str, TokenBucket] = {}
        self._lock = threading.Lock()

    def xǁRateLimiterǁ__init____mutmut_1(self, default_capacity: int = 101, default_refill_rate: float = 100.0):
        self.default_capacity = default_capacity
        self.default_refill_rate = default_refill_rate
        self._buckets: Dict[str, TokenBucket] = {}
        self._lock = threading.Lock()

    def xǁRateLimiterǁ__init____mutmut_2(self, default_capacity: int = 100, default_refill_rate: float = 101.0):
        self.default_capacity = default_capacity
        self.default_refill_rate = default_refill_rate
        self._buckets: Dict[str, TokenBucket] = {}
        self._lock = threading.Lock()

    def xǁRateLimiterǁ__init____mutmut_3(self, default_capacity: int = 100, default_refill_rate: float = 100.0):
        self.default_capacity = None
        self.default_refill_rate = default_refill_rate
        self._buckets: Dict[str, TokenBucket] = {}
        self._lock = threading.Lock()

    def xǁRateLimiterǁ__init____mutmut_4(self, default_capacity: int = 100, default_refill_rate: float = 100.0):
        self.default_capacity = default_capacity
        self.default_refill_rate = None
        self._buckets: Dict[str, TokenBucket] = {}
        self._lock = threading.Lock()

    def xǁRateLimiterǁ__init____mutmut_5(self, default_capacity: int = 100, default_refill_rate: float = 100.0):
        self.default_capacity = default_capacity
        self.default_refill_rate = default_refill_rate
        self._buckets: Dict[str, TokenBucket] = None
        self._lock = threading.Lock()

    def xǁRateLimiterǁ__init____mutmut_6(self, default_capacity: int = 100, default_refill_rate: float = 100.0):
        self.default_capacity = default_capacity
        self.default_refill_rate = default_refill_rate
        self._buckets: Dict[str, TokenBucket] = {}
        self._lock = None
    
    xǁRateLimiterǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRateLimiterǁ__init____mutmut_1': xǁRateLimiterǁ__init____mutmut_1, 
        'xǁRateLimiterǁ__init____mutmut_2': xǁRateLimiterǁ__init____mutmut_2, 
        'xǁRateLimiterǁ__init____mutmut_3': xǁRateLimiterǁ__init____mutmut_3, 
        'xǁRateLimiterǁ__init____mutmut_4': xǁRateLimiterǁ__init____mutmut_4, 
        'xǁRateLimiterǁ__init____mutmut_5': xǁRateLimiterǁ__init____mutmut_5, 
        'xǁRateLimiterǁ__init____mutmut_6': xǁRateLimiterǁ__init____mutmut_6
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRateLimiterǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁRateLimiterǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁRateLimiterǁ__init____mutmut_orig)
    xǁRateLimiterǁ__init____mutmut_orig.__name__ = 'xǁRateLimiterǁ__init__'

    def xǁRateLimiterǁallow__mutmut_orig(self, user_id: str) -> bool:
        """Check if a request from user_id is allowed."""
        with self._lock:
            bucket = self._buckets.get(user_id)
            if bucket is None:
                bucket = TokenBucket(self.default_capacity, self.default_refill_rate)
                self._buckets[user_id] = bucket
        return bucket.consume()

    def xǁRateLimiterǁallow__mutmut_1(self, user_id: str) -> bool:
        """Check if a request from user_id is allowed."""
        with self._lock:
            bucket = None
            if bucket is None:
                bucket = TokenBucket(self.default_capacity, self.default_refill_rate)
                self._buckets[user_id] = bucket
        return bucket.consume()

    def xǁRateLimiterǁallow__mutmut_2(self, user_id: str) -> bool:
        """Check if a request from user_id is allowed."""
        with self._lock:
            bucket = self._buckets.get(None)
            if bucket is None:
                bucket = TokenBucket(self.default_capacity, self.default_refill_rate)
                self._buckets[user_id] = bucket
        return bucket.consume()

    def xǁRateLimiterǁallow__mutmut_3(self, user_id: str) -> bool:
        """Check if a request from user_id is allowed."""
        with self._lock:
            bucket = self._buckets.get(user_id)
            if bucket is not None:
                bucket = TokenBucket(self.default_capacity, self.default_refill_rate)
                self._buckets[user_id] = bucket
        return bucket.consume()

    def xǁRateLimiterǁallow__mutmut_4(self, user_id: str) -> bool:
        """Check if a request from user_id is allowed."""
        with self._lock:
            bucket = self._buckets.get(user_id)
            if bucket is None:
                bucket = None
                self._buckets[user_id] = bucket
        return bucket.consume()

    def xǁRateLimiterǁallow__mutmut_5(self, user_id: str) -> bool:
        """Check if a request from user_id is allowed."""
        with self._lock:
            bucket = self._buckets.get(user_id)
            if bucket is None:
                bucket = TokenBucket(None, self.default_refill_rate)
                self._buckets[user_id] = bucket
        return bucket.consume()

    def xǁRateLimiterǁallow__mutmut_6(self, user_id: str) -> bool:
        """Check if a request from user_id is allowed."""
        with self._lock:
            bucket = self._buckets.get(user_id)
            if bucket is None:
                bucket = TokenBucket(self.default_capacity, None)
                self._buckets[user_id] = bucket
        return bucket.consume()

    def xǁRateLimiterǁallow__mutmut_7(self, user_id: str) -> bool:
        """Check if a request from user_id is allowed."""
        with self._lock:
            bucket = self._buckets.get(user_id)
            if bucket is None:
                bucket = TokenBucket(self.default_refill_rate)
                self._buckets[user_id] = bucket
        return bucket.consume()

    def xǁRateLimiterǁallow__mutmut_8(self, user_id: str) -> bool:
        """Check if a request from user_id is allowed."""
        with self._lock:
            bucket = self._buckets.get(user_id)
            if bucket is None:
                bucket = TokenBucket(self.default_capacity, )
                self._buckets[user_id] = bucket
        return bucket.consume()

    def xǁRateLimiterǁallow__mutmut_9(self, user_id: str) -> bool:
        """Check if a request from user_id is allowed."""
        with self._lock:
            bucket = self._buckets.get(user_id)
            if bucket is None:
                bucket = TokenBucket(self.default_capacity, self.default_refill_rate)
                self._buckets[user_id] = None
        return bucket.consume()
    
    xǁRateLimiterǁallow__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRateLimiterǁallow__mutmut_1': xǁRateLimiterǁallow__mutmut_1, 
        'xǁRateLimiterǁallow__mutmut_2': xǁRateLimiterǁallow__mutmut_2, 
        'xǁRateLimiterǁallow__mutmut_3': xǁRateLimiterǁallow__mutmut_3, 
        'xǁRateLimiterǁallow__mutmut_4': xǁRateLimiterǁallow__mutmut_4, 
        'xǁRateLimiterǁallow__mutmut_5': xǁRateLimiterǁallow__mutmut_5, 
        'xǁRateLimiterǁallow__mutmut_6': xǁRateLimiterǁallow__mutmut_6, 
        'xǁRateLimiterǁallow__mutmut_7': xǁRateLimiterǁallow__mutmut_7, 
        'xǁRateLimiterǁallow__mutmut_8': xǁRateLimiterǁallow__mutmut_8, 
        'xǁRateLimiterǁallow__mutmut_9': xǁRateLimiterǁallow__mutmut_9
    }
    
    def allow(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRateLimiterǁallow__mutmut_orig"), object.__getattribute__(self, "xǁRateLimiterǁallow__mutmut_mutants"), args, kwargs, self)
        return result 
    
    allow.__signature__ = _mutmut_signature(xǁRateLimiterǁallow__mutmut_orig)
    xǁRateLimiterǁallow__mutmut_orig.__name__ = 'xǁRateLimiterǁallow'
