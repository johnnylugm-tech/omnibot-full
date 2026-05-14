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


def resolve_route(platform: str) -> Optional[Tuple[Platform, Callable[[dict], UnifiedMessage]]]:
    """Resolve a platform URL slug to its enum and payload parser.

    Returns None for unsupported platforms.
    """
    return PLATFORM_ROUTES.get(platform.lower())
