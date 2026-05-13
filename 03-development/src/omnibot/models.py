"""[FR-01] UnifiedMessage and supporting enums.

Citations: SRS.md:13-25, SAD.md:142-167
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional


class Platform(str, Enum):
    TELEGRAM = "TELEGRAM"
    LINE = "LINE"
    MESSENGER = "MESSENGER"
    WHATSAPP = "WHATSAPP"


class MessageType(str, Enum):
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    STICKER = "STICKER"
    LOCATION = "LOCATION"
    FILE = "FILE"


@dataclass(frozen=True)
class UnifiedMessage:
    platform: Platform
    platform_user_id: str
    message_type: MessageType
    content: str
    raw_payload: Dict[str, Any] = field(default_factory=dict)
    received_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    unified_user_id: str = ""
    reply_token: Optional[str] = None
