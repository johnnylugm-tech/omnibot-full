"""[FR-01][FR-03] UnifiedMessage, UnifiedResponse, and supporting enums.

Citations: SRS.md:13-25,44-55, SAD.md:140-167
"""

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional


class Platform(str, Enum):
    """Supported messaging platforms.

    Citations: SRS.md:51
    """
    TELEGRAM = "TELEGRAM"
    LINE = "LINE"
    MESSENGER = "MESSENGER"
    WHATSAPP = "WHATSAPP"


class MessageType(str, Enum):
    """Supported message types.

    Citations: SRS.md:52
    """
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    STICKER = "STICKER"
    LOCATION = "LOCATION"
    FILE = "FILE"


@dataclass(frozen=True)
class UnifiedMessage:
    """Platform-agnostic inbound message.

    Citations: SRS.md:50, SAD.md:142-153
    """
    platform: Platform
    platform_user_id: str
    message_type: MessageType
    content: str
    raw_payload: Dict[str, Any] = field(default_factory=dict)
    received_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    unified_user_id: str = ""
    reply_token: Optional[str] = None

    def to_json_dict(self) -> Dict[str, Any]:
        """Serialize to a JSON-safe dict with ISO8601 datetime conversion."""
        data = asdict(self)
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
        return data


@dataclass(frozen=True)
class UnifiedResponse:
    """Platform-agnostic outbound response.

    Citations: SRS.md:53, SAD.md:155-161
    """
    content: str
    source: str
    confidence: float
    knowledge_id: int
