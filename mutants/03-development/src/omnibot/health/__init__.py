"""[FR-11] Health Check Endpoint.

GET /api/v1/health → {status, postgres, redis, uptime_seconds}.
Status is derived from postgres + redis connectivity bools.

Citations: SRS.md FR-11 section, SAD.md 2.5.3 HealthCheck
"""

import time
from enum import Enum
from typing import Callable, Dict, Union
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


class HealthStatus(str, Enum):
    """Health status values.

    Citations: SRS.md FR-11
    """
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class HealthCheckService:
    """Service health check with postgres/redis probes.

    Accepts callables for postgres and redis checks so they can be
    stubbed in tests and swapped for real pings in production.

    Citations: SAD.md 2.5.3 HealthCheck
    """

    def xǁHealthCheckServiceǁ__init____mutmut_orig(
        self,
        postgres_check: Callable[[], bool],
        redis_check: Callable[[], bool],
    ) -> None:
        self._start_time = time.monotonic()
        self._pg = postgres_check
        self._redis = redis_check

    def xǁHealthCheckServiceǁ__init____mutmut_1(
        self,
        postgres_check: Callable[[], bool],
        redis_check: Callable[[], bool],
    ) -> None:
        self._start_time = None
        self._pg = postgres_check
        self._redis = redis_check

    def xǁHealthCheckServiceǁ__init____mutmut_2(
        self,
        postgres_check: Callable[[], bool],
        redis_check: Callable[[], bool],
    ) -> None:
        self._start_time = time.monotonic()
        self._pg = None
        self._redis = redis_check

    def xǁHealthCheckServiceǁ__init____mutmut_3(
        self,
        postgres_check: Callable[[], bool],
        redis_check: Callable[[], bool],
    ) -> None:
        self._start_time = time.monotonic()
        self._pg = postgres_check
        self._redis = None
    
    xǁHealthCheckServiceǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁHealthCheckServiceǁ__init____mutmut_1': xǁHealthCheckServiceǁ__init____mutmut_1, 
        'xǁHealthCheckServiceǁ__init____mutmut_2': xǁHealthCheckServiceǁ__init____mutmut_2, 
        'xǁHealthCheckServiceǁ__init____mutmut_3': xǁHealthCheckServiceǁ__init____mutmut_3
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁHealthCheckServiceǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁHealthCheckServiceǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁHealthCheckServiceǁ__init____mutmut_orig)
    xǁHealthCheckServiceǁ__init____mutmut_orig.__name__ = 'xǁHealthCheckServiceǁ__init__'

    def xǁHealthCheckServiceǁcheck__mutmut_orig(self) -> Dict[str, Union[str, bool, float]]:
        """Run health checks and return the status dict."""
        pg_ok = self._pg()
        redis_ok = self._redis()

        if pg_ok and redis_ok:
            status = HealthStatus.HEALTHY
        elif pg_ok or redis_ok:
            status = HealthStatus.DEGRADED
        else:
            status = HealthStatus.UNHEALTHY

        return {
            "status": status.value,
            "postgres": pg_ok,
            "redis": redis_ok,
            "uptime_seconds": time.monotonic() - self._start_time,
        }

    def xǁHealthCheckServiceǁcheck__mutmut_1(self) -> Dict[str, Union[str, bool, float]]:
        """Run health checks and return the status dict."""
        pg_ok = None
        redis_ok = self._redis()

        if pg_ok and redis_ok:
            status = HealthStatus.HEALTHY
        elif pg_ok or redis_ok:
            status = HealthStatus.DEGRADED
        else:
            status = HealthStatus.UNHEALTHY

        return {
            "status": status.value,
            "postgres": pg_ok,
            "redis": redis_ok,
            "uptime_seconds": time.monotonic() - self._start_time,
        }

    def xǁHealthCheckServiceǁcheck__mutmut_2(self) -> Dict[str, Union[str, bool, float]]:
        """Run health checks and return the status dict."""
        pg_ok = self._pg()
        redis_ok = None

        if pg_ok and redis_ok:
            status = HealthStatus.HEALTHY
        elif pg_ok or redis_ok:
            status = HealthStatus.DEGRADED
        else:
            status = HealthStatus.UNHEALTHY

        return {
            "status": status.value,
            "postgres": pg_ok,
            "redis": redis_ok,
            "uptime_seconds": time.monotonic() - self._start_time,
        }

    def xǁHealthCheckServiceǁcheck__mutmut_3(self) -> Dict[str, Union[str, bool, float]]:
        """Run health checks and return the status dict."""
        pg_ok = self._pg()
        redis_ok = self._redis()

        if pg_ok or redis_ok:
            status = HealthStatus.HEALTHY
        elif pg_ok or redis_ok:
            status = HealthStatus.DEGRADED
        else:
            status = HealthStatus.UNHEALTHY

        return {
            "status": status.value,
            "postgres": pg_ok,
            "redis": redis_ok,
            "uptime_seconds": time.monotonic() - self._start_time,
        }

    def xǁHealthCheckServiceǁcheck__mutmut_4(self) -> Dict[str, Union[str, bool, float]]:
        """Run health checks and return the status dict."""
        pg_ok = self._pg()
        redis_ok = self._redis()

        if pg_ok and redis_ok:
            status = None
        elif pg_ok or redis_ok:
            status = HealthStatus.DEGRADED
        else:
            status = HealthStatus.UNHEALTHY

        return {
            "status": status.value,
            "postgres": pg_ok,
            "redis": redis_ok,
            "uptime_seconds": time.monotonic() - self._start_time,
        }

    def xǁHealthCheckServiceǁcheck__mutmut_5(self) -> Dict[str, Union[str, bool, float]]:
        """Run health checks and return the status dict."""
        pg_ok = self._pg()
        redis_ok = self._redis()

        if pg_ok and redis_ok:
            status = HealthStatus.HEALTHY
        elif pg_ok and redis_ok:
            status = HealthStatus.DEGRADED
        else:
            status = HealthStatus.UNHEALTHY

        return {
            "status": status.value,
            "postgres": pg_ok,
            "redis": redis_ok,
            "uptime_seconds": time.monotonic() - self._start_time,
        }

    def xǁHealthCheckServiceǁcheck__mutmut_6(self) -> Dict[str, Union[str, bool, float]]:
        """Run health checks and return the status dict."""
        pg_ok = self._pg()
        redis_ok = self._redis()

        if pg_ok and redis_ok:
            status = HealthStatus.HEALTHY
        elif pg_ok or redis_ok:
            status = None
        else:
            status = HealthStatus.UNHEALTHY

        return {
            "status": status.value,
            "postgres": pg_ok,
            "redis": redis_ok,
            "uptime_seconds": time.monotonic() - self._start_time,
        }

    def xǁHealthCheckServiceǁcheck__mutmut_7(self) -> Dict[str, Union[str, bool, float]]:
        """Run health checks and return the status dict."""
        pg_ok = self._pg()
        redis_ok = self._redis()

        if pg_ok and redis_ok:
            status = HealthStatus.HEALTHY
        elif pg_ok or redis_ok:
            status = HealthStatus.DEGRADED
        else:
            status = None

        return {
            "status": status.value,
            "postgres": pg_ok,
            "redis": redis_ok,
            "uptime_seconds": time.monotonic() - self._start_time,
        }

    def xǁHealthCheckServiceǁcheck__mutmut_8(self) -> Dict[str, Union[str, bool, float]]:
        """Run health checks and return the status dict."""
        pg_ok = self._pg()
        redis_ok = self._redis()

        if pg_ok and redis_ok:
            status = HealthStatus.HEALTHY
        elif pg_ok or redis_ok:
            status = HealthStatus.DEGRADED
        else:
            status = HealthStatus.UNHEALTHY

        return {
            "XXstatusXX": status.value,
            "postgres": pg_ok,
            "redis": redis_ok,
            "uptime_seconds": time.monotonic() - self._start_time,
        }

    def xǁHealthCheckServiceǁcheck__mutmut_9(self) -> Dict[str, Union[str, bool, float]]:
        """Run health checks and return the status dict."""
        pg_ok = self._pg()
        redis_ok = self._redis()

        if pg_ok and redis_ok:
            status = HealthStatus.HEALTHY
        elif pg_ok or redis_ok:
            status = HealthStatus.DEGRADED
        else:
            status = HealthStatus.UNHEALTHY

        return {
            "STATUS": status.value,
            "postgres": pg_ok,
            "redis": redis_ok,
            "uptime_seconds": time.monotonic() - self._start_time,
        }

    def xǁHealthCheckServiceǁcheck__mutmut_10(self) -> Dict[str, Union[str, bool, float]]:
        """Run health checks and return the status dict."""
        pg_ok = self._pg()
        redis_ok = self._redis()

        if pg_ok and redis_ok:
            status = HealthStatus.HEALTHY
        elif pg_ok or redis_ok:
            status = HealthStatus.DEGRADED
        else:
            status = HealthStatus.UNHEALTHY

        return {
            "status": status.value,
            "XXpostgresXX": pg_ok,
            "redis": redis_ok,
            "uptime_seconds": time.monotonic() - self._start_time,
        }

    def xǁHealthCheckServiceǁcheck__mutmut_11(self) -> Dict[str, Union[str, bool, float]]:
        """Run health checks and return the status dict."""
        pg_ok = self._pg()
        redis_ok = self._redis()

        if pg_ok and redis_ok:
            status = HealthStatus.HEALTHY
        elif pg_ok or redis_ok:
            status = HealthStatus.DEGRADED
        else:
            status = HealthStatus.UNHEALTHY

        return {
            "status": status.value,
            "POSTGRES": pg_ok,
            "redis": redis_ok,
            "uptime_seconds": time.monotonic() - self._start_time,
        }

    def xǁHealthCheckServiceǁcheck__mutmut_12(self) -> Dict[str, Union[str, bool, float]]:
        """Run health checks and return the status dict."""
        pg_ok = self._pg()
        redis_ok = self._redis()

        if pg_ok and redis_ok:
            status = HealthStatus.HEALTHY
        elif pg_ok or redis_ok:
            status = HealthStatus.DEGRADED
        else:
            status = HealthStatus.UNHEALTHY

        return {
            "status": status.value,
            "postgres": pg_ok,
            "XXredisXX": redis_ok,
            "uptime_seconds": time.monotonic() - self._start_time,
        }

    def xǁHealthCheckServiceǁcheck__mutmut_13(self) -> Dict[str, Union[str, bool, float]]:
        """Run health checks and return the status dict."""
        pg_ok = self._pg()
        redis_ok = self._redis()

        if pg_ok and redis_ok:
            status = HealthStatus.HEALTHY
        elif pg_ok or redis_ok:
            status = HealthStatus.DEGRADED
        else:
            status = HealthStatus.UNHEALTHY

        return {
            "status": status.value,
            "postgres": pg_ok,
            "REDIS": redis_ok,
            "uptime_seconds": time.monotonic() - self._start_time,
        }

    def xǁHealthCheckServiceǁcheck__mutmut_14(self) -> Dict[str, Union[str, bool, float]]:
        """Run health checks and return the status dict."""
        pg_ok = self._pg()
        redis_ok = self._redis()

        if pg_ok and redis_ok:
            status = HealthStatus.HEALTHY
        elif pg_ok or redis_ok:
            status = HealthStatus.DEGRADED
        else:
            status = HealthStatus.UNHEALTHY

        return {
            "status": status.value,
            "postgres": pg_ok,
            "redis": redis_ok,
            "XXuptime_secondsXX": time.monotonic() - self._start_time,
        }

    def xǁHealthCheckServiceǁcheck__mutmut_15(self) -> Dict[str, Union[str, bool, float]]:
        """Run health checks and return the status dict."""
        pg_ok = self._pg()
        redis_ok = self._redis()

        if pg_ok and redis_ok:
            status = HealthStatus.HEALTHY
        elif pg_ok or redis_ok:
            status = HealthStatus.DEGRADED
        else:
            status = HealthStatus.UNHEALTHY

        return {
            "status": status.value,
            "postgres": pg_ok,
            "redis": redis_ok,
            "UPTIME_SECONDS": time.monotonic() - self._start_time,
        }

    def xǁHealthCheckServiceǁcheck__mutmut_16(self) -> Dict[str, Union[str, bool, float]]:
        """Run health checks and return the status dict."""
        pg_ok = self._pg()
        redis_ok = self._redis()

        if pg_ok and redis_ok:
            status = HealthStatus.HEALTHY
        elif pg_ok or redis_ok:
            status = HealthStatus.DEGRADED
        else:
            status = HealthStatus.UNHEALTHY

        return {
            "status": status.value,
            "postgres": pg_ok,
            "redis": redis_ok,
            "uptime_seconds": time.monotonic() + self._start_time,
        }
    
    xǁHealthCheckServiceǁcheck__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁHealthCheckServiceǁcheck__mutmut_1': xǁHealthCheckServiceǁcheck__mutmut_1, 
        'xǁHealthCheckServiceǁcheck__mutmut_2': xǁHealthCheckServiceǁcheck__mutmut_2, 
        'xǁHealthCheckServiceǁcheck__mutmut_3': xǁHealthCheckServiceǁcheck__mutmut_3, 
        'xǁHealthCheckServiceǁcheck__mutmut_4': xǁHealthCheckServiceǁcheck__mutmut_4, 
        'xǁHealthCheckServiceǁcheck__mutmut_5': xǁHealthCheckServiceǁcheck__mutmut_5, 
        'xǁHealthCheckServiceǁcheck__mutmut_6': xǁHealthCheckServiceǁcheck__mutmut_6, 
        'xǁHealthCheckServiceǁcheck__mutmut_7': xǁHealthCheckServiceǁcheck__mutmut_7, 
        'xǁHealthCheckServiceǁcheck__mutmut_8': xǁHealthCheckServiceǁcheck__mutmut_8, 
        'xǁHealthCheckServiceǁcheck__mutmut_9': xǁHealthCheckServiceǁcheck__mutmut_9, 
        'xǁHealthCheckServiceǁcheck__mutmut_10': xǁHealthCheckServiceǁcheck__mutmut_10, 
        'xǁHealthCheckServiceǁcheck__mutmut_11': xǁHealthCheckServiceǁcheck__mutmut_11, 
        'xǁHealthCheckServiceǁcheck__mutmut_12': xǁHealthCheckServiceǁcheck__mutmut_12, 
        'xǁHealthCheckServiceǁcheck__mutmut_13': xǁHealthCheckServiceǁcheck__mutmut_13, 
        'xǁHealthCheckServiceǁcheck__mutmut_14': xǁHealthCheckServiceǁcheck__mutmut_14, 
        'xǁHealthCheckServiceǁcheck__mutmut_15': xǁHealthCheckServiceǁcheck__mutmut_15, 
        'xǁHealthCheckServiceǁcheck__mutmut_16': xǁHealthCheckServiceǁcheck__mutmut_16
    }
    
    def check(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁHealthCheckServiceǁcheck__mutmut_orig"), object.__getattribute__(self, "xǁHealthCheckServiceǁcheck__mutmut_mutants"), args, kwargs, self)
        return result 
    
    check.__signature__ = _mutmut_signature(xǁHealthCheckServiceǁcheck__mutmut_orig)
    xǁHealthCheckServiceǁcheck__mutmut_orig.__name__ = 'xǁHealthCheckServiceǁcheck'
