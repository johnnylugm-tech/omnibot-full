"""[FR-14] MessengerAdapter — parse Messenger WebhookEvent → UnifiedMessage.

Citations: SAD.md:113-127
"""

from typing import Any, Dict

from omnibot.models import UnifiedMessage, Platform, MessageType


def parse_messenger_webhook(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Messenger WebhookEvent into a UnifiedMessage.

    Raises ValueError if the messaging array is empty or missing.
    """
    entry = payload.get("entry", [])
    if not entry:
        raise ValueError("Messenger webhook payload contains no entries")

    messaging = entry[0].get("messaging", [])
    if not messaging:
        raise ValueError("Messenger webhook payload contains no messaging events")

    event = messaging[0]
    sender = event.get("sender", {})
    message = event.get("message", {})

    platform_user_id = str(sender.get("id", ""))
    text = message.get("text", "")
    message_type = MessageType.TEXT

    return UnifiedMessage(
        platform=Platform.MESSENGER,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )
