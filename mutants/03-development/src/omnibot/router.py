"""[FR-01] Platform webhook router — route dispatching and payload parsing.

Extracted from app.py to reduce hub-module coupling.
Citations: SAD.md 2.4.2 (Routing), SRS.md:13-25
"""

from typing import Callable, Dict, Optional, Tuple

from omnibot.adapters.telegram import parse_telegram_update
from omnibot.adapters.line import parse_line_event
from omnibot.models import Platform, UnifiedMessage


#: Platform route table: URL slug → (Platform enum, parser function)
PLATFORM_ROUTES: Dict[str, Tuple[Platform, Callable]] = {
    "telegram": (Platform.TELEGRAM, parse_telegram_update),
    "line": (Platform.LINE, parse_line_event),
}
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


def x_resolve_route__mutmut_orig(platform: str) -> Optional[Tuple[Platform, Callable[[dict], UnifiedMessage]]]:
    """Resolve a platform URL slug to its enum and payload parser.

    Returns None for unsupported platforms.
    """
    return PLATFORM_ROUTES.get(platform.lower())


def x_resolve_route__mutmut_1(platform: str) -> Optional[Tuple[Platform, Callable[[dict], UnifiedMessage]]]:
    """Resolve a platform URL slug to its enum and payload parser.

    Returns None for unsupported platforms.
    """
    return PLATFORM_ROUTES.get(None)


def x_resolve_route__mutmut_2(platform: str) -> Optional[Tuple[Platform, Callable[[dict], UnifiedMessage]]]:
    """Resolve a platform URL slug to its enum and payload parser.

    Returns None for unsupported platforms.
    """
    return PLATFORM_ROUTES.get(platform.upper())

x_resolve_route__mutmut_mutants : ClassVar[MutantDict] = {
'x_resolve_route__mutmut_1': x_resolve_route__mutmut_1, 
    'x_resolve_route__mutmut_2': x_resolve_route__mutmut_2
}

def resolve_route(*args, **kwargs):
    result = _mutmut_trampoline(x_resolve_route__mutmut_orig, x_resolve_route__mutmut_mutants, args, kwargs)
    return result 

resolve_route.__signature__ = _mutmut_signature(x_resolve_route__mutmut_orig)
x_resolve_route__mutmut_orig.__name__ = 'x_resolve_route'
