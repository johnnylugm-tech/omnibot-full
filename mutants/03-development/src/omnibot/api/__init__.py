"""[FR-10] API Response Format — ApiResponse / PaginatedResponse.

Unified response wrappers with Generic[T] support via Pydantic BaseModel.
ErrorCode enum for standard API error classification.

Citations: SRS.md FR-10 section, SAD.md 2.5.2
"""

from enum import Enum
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, computed_field

T = TypeVar("T")
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


class ErrorCode(str, Enum):
    """Standard API error codes.

    Citations: SRS.md FR-10
    """
    AUTH_INVALID_SIGNATURE = "AUTH_INVALID_SIGNATURE"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    KNOWLEDGE_NOT_FOUND = "KNOWLEDGE_NOT_FOUND"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class ApiResponse(BaseModel, Generic[T]):
    """Unified API success/error response.

    Citations: SAD.md 2.5.2 ApiResponse
    """
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
    error_code: Optional[ErrorCode] = None


class PaginatedResponse(ApiResponse[T]):
    """Paginated API response extending ApiResponse.

    has_next is computed from page * limit < total.

    Citations: SAD.md 2.5.2 PaginatedResponse
    """
    total: int = 0
    page: int = 1
    limit: int = 20

    @computed_field
    @property
    def has_next(self) -> bool:
        """True when there are more pages after this one."""
        return self.page * self.limit < self.total
