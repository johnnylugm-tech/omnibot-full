"""[FR-01] LINEAdapter — parse LINE WebhookEvent → UnifiedMessage.

Citations: SAD.md:83-95
"""

from typing import Any, Dict

from omnibot.models import UnifiedMessage, Platform, MessageType


_LINE_MESSAGE_TYPE_MAP = {
    "text": MessageType.TEXT,
    "image": MessageType.IMAGE,
    "sticker": MessageType.STICKER,
    "location": MessageType.LOCATION,
    "file": MessageType.FILE,
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


def x_parse_line_event__mutmut_orig(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_1(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = None
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_2(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get(None, [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_3(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", None)
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_4(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get([])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_5(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", )
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_6(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("XXeventsXX", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_7(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("EVENTS", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_8(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_9(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError(None)

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_10(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("XXLINE webhook payload contains no eventsXX")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_11(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("line webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_12(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE WEBHOOK PAYLOAD CONTAINS NO EVENTS")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_13(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = None
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_14(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[1]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_15(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = None
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_16(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get(None, {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_17(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", None)
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_18(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get({})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_19(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", )
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_20(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("XXsourceXX", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_21(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("SOURCE", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_22(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = None

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_23(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get(None, {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_24(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", None)

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_25(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get({})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_26(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", )

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_27(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("XXmessageXX", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_28(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("MESSAGE", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_29(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = None
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_30(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(None)
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_31(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get(None, ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_32(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", None))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_33(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get(""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_34(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_35(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("XXuserIdXX", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_36(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userid", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_37(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("USERID", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_38(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", "XXXX"))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_39(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = None
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_40(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get(None, "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_41(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", None)
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_42(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_43(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", )
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_44(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("XXtypeXX", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_45(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("TYPE", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_46(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "XXtextXX")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_47(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "TEXT")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_48(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = None
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_49(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(None, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_50(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, None)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_51(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_52(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, )
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_53(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = None
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_54(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get(None, "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_55(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", None)
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_56(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_57(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", )
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_58(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("XXtextXX", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_59(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("TEXT", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_60(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "XXXX")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_61(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = None

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_62(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get(None)

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_63(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("XXreplyTokenXX")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_64(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replytoken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_65(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("REPLYTOKEN")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_66(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=None,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_67(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=None,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_68(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=None,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_69(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=None,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_70(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=None,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_71(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=None,
    )


def x_parse_line_event__mutmut_72(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_73(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_74(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        content=content,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_75(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        raw_payload=payload,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_76(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        reply_token=reply_token,
    )


def x_parse_line_event__mutmut_77(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a LINE Messaging API WebhookEvent into a UnifiedMessage.

    Raises ValueError if the events array is empty or missing.
    """
    events = payload.get("events", [])
    if not events:
        raise ValueError("LINE webhook payload contains no events")

    event = events[0]
    source = event.get("source", {})
    message = event.get("message", {})

    platform_user_id = str(source.get("userId", ""))
    line_type = message.get("type", "text")
    message_type = _LINE_MESSAGE_TYPE_MAP.get(line_type, MessageType.TEXT)
    content = message.get("text", "")
    reply_token = event.get("replyToken")

    return UnifiedMessage(
        platform=Platform.LINE,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=content,
        raw_payload=payload,
        )

x_parse_line_event__mutmut_mutants : ClassVar[MutantDict] = {
'x_parse_line_event__mutmut_1': x_parse_line_event__mutmut_1, 
    'x_parse_line_event__mutmut_2': x_parse_line_event__mutmut_2, 
    'x_parse_line_event__mutmut_3': x_parse_line_event__mutmut_3, 
    'x_parse_line_event__mutmut_4': x_parse_line_event__mutmut_4, 
    'x_parse_line_event__mutmut_5': x_parse_line_event__mutmut_5, 
    'x_parse_line_event__mutmut_6': x_parse_line_event__mutmut_6, 
    'x_parse_line_event__mutmut_7': x_parse_line_event__mutmut_7, 
    'x_parse_line_event__mutmut_8': x_parse_line_event__mutmut_8, 
    'x_parse_line_event__mutmut_9': x_parse_line_event__mutmut_9, 
    'x_parse_line_event__mutmut_10': x_parse_line_event__mutmut_10, 
    'x_parse_line_event__mutmut_11': x_parse_line_event__mutmut_11, 
    'x_parse_line_event__mutmut_12': x_parse_line_event__mutmut_12, 
    'x_parse_line_event__mutmut_13': x_parse_line_event__mutmut_13, 
    'x_parse_line_event__mutmut_14': x_parse_line_event__mutmut_14, 
    'x_parse_line_event__mutmut_15': x_parse_line_event__mutmut_15, 
    'x_parse_line_event__mutmut_16': x_parse_line_event__mutmut_16, 
    'x_parse_line_event__mutmut_17': x_parse_line_event__mutmut_17, 
    'x_parse_line_event__mutmut_18': x_parse_line_event__mutmut_18, 
    'x_parse_line_event__mutmut_19': x_parse_line_event__mutmut_19, 
    'x_parse_line_event__mutmut_20': x_parse_line_event__mutmut_20, 
    'x_parse_line_event__mutmut_21': x_parse_line_event__mutmut_21, 
    'x_parse_line_event__mutmut_22': x_parse_line_event__mutmut_22, 
    'x_parse_line_event__mutmut_23': x_parse_line_event__mutmut_23, 
    'x_parse_line_event__mutmut_24': x_parse_line_event__mutmut_24, 
    'x_parse_line_event__mutmut_25': x_parse_line_event__mutmut_25, 
    'x_parse_line_event__mutmut_26': x_parse_line_event__mutmut_26, 
    'x_parse_line_event__mutmut_27': x_parse_line_event__mutmut_27, 
    'x_parse_line_event__mutmut_28': x_parse_line_event__mutmut_28, 
    'x_parse_line_event__mutmut_29': x_parse_line_event__mutmut_29, 
    'x_parse_line_event__mutmut_30': x_parse_line_event__mutmut_30, 
    'x_parse_line_event__mutmut_31': x_parse_line_event__mutmut_31, 
    'x_parse_line_event__mutmut_32': x_parse_line_event__mutmut_32, 
    'x_parse_line_event__mutmut_33': x_parse_line_event__mutmut_33, 
    'x_parse_line_event__mutmut_34': x_parse_line_event__mutmut_34, 
    'x_parse_line_event__mutmut_35': x_parse_line_event__mutmut_35, 
    'x_parse_line_event__mutmut_36': x_parse_line_event__mutmut_36, 
    'x_parse_line_event__mutmut_37': x_parse_line_event__mutmut_37, 
    'x_parse_line_event__mutmut_38': x_parse_line_event__mutmut_38, 
    'x_parse_line_event__mutmut_39': x_parse_line_event__mutmut_39, 
    'x_parse_line_event__mutmut_40': x_parse_line_event__mutmut_40, 
    'x_parse_line_event__mutmut_41': x_parse_line_event__mutmut_41, 
    'x_parse_line_event__mutmut_42': x_parse_line_event__mutmut_42, 
    'x_parse_line_event__mutmut_43': x_parse_line_event__mutmut_43, 
    'x_parse_line_event__mutmut_44': x_parse_line_event__mutmut_44, 
    'x_parse_line_event__mutmut_45': x_parse_line_event__mutmut_45, 
    'x_parse_line_event__mutmut_46': x_parse_line_event__mutmut_46, 
    'x_parse_line_event__mutmut_47': x_parse_line_event__mutmut_47, 
    'x_parse_line_event__mutmut_48': x_parse_line_event__mutmut_48, 
    'x_parse_line_event__mutmut_49': x_parse_line_event__mutmut_49, 
    'x_parse_line_event__mutmut_50': x_parse_line_event__mutmut_50, 
    'x_parse_line_event__mutmut_51': x_parse_line_event__mutmut_51, 
    'x_parse_line_event__mutmut_52': x_parse_line_event__mutmut_52, 
    'x_parse_line_event__mutmut_53': x_parse_line_event__mutmut_53, 
    'x_parse_line_event__mutmut_54': x_parse_line_event__mutmut_54, 
    'x_parse_line_event__mutmut_55': x_parse_line_event__mutmut_55, 
    'x_parse_line_event__mutmut_56': x_parse_line_event__mutmut_56, 
    'x_parse_line_event__mutmut_57': x_parse_line_event__mutmut_57, 
    'x_parse_line_event__mutmut_58': x_parse_line_event__mutmut_58, 
    'x_parse_line_event__mutmut_59': x_parse_line_event__mutmut_59, 
    'x_parse_line_event__mutmut_60': x_parse_line_event__mutmut_60, 
    'x_parse_line_event__mutmut_61': x_parse_line_event__mutmut_61, 
    'x_parse_line_event__mutmut_62': x_parse_line_event__mutmut_62, 
    'x_parse_line_event__mutmut_63': x_parse_line_event__mutmut_63, 
    'x_parse_line_event__mutmut_64': x_parse_line_event__mutmut_64, 
    'x_parse_line_event__mutmut_65': x_parse_line_event__mutmut_65, 
    'x_parse_line_event__mutmut_66': x_parse_line_event__mutmut_66, 
    'x_parse_line_event__mutmut_67': x_parse_line_event__mutmut_67, 
    'x_parse_line_event__mutmut_68': x_parse_line_event__mutmut_68, 
    'x_parse_line_event__mutmut_69': x_parse_line_event__mutmut_69, 
    'x_parse_line_event__mutmut_70': x_parse_line_event__mutmut_70, 
    'x_parse_line_event__mutmut_71': x_parse_line_event__mutmut_71, 
    'x_parse_line_event__mutmut_72': x_parse_line_event__mutmut_72, 
    'x_parse_line_event__mutmut_73': x_parse_line_event__mutmut_73, 
    'x_parse_line_event__mutmut_74': x_parse_line_event__mutmut_74, 
    'x_parse_line_event__mutmut_75': x_parse_line_event__mutmut_75, 
    'x_parse_line_event__mutmut_76': x_parse_line_event__mutmut_76, 
    'x_parse_line_event__mutmut_77': x_parse_line_event__mutmut_77
}

def parse_line_event(*args, **kwargs):
    result = _mutmut_trampoline(x_parse_line_event__mutmut_orig, x_parse_line_event__mutmut_mutants, args, kwargs)
    return result 

parse_line_event.__signature__ = _mutmut_signature(x_parse_line_event__mutmut_orig)
x_parse_line_event__mutmut_orig.__name__ = 'x_parse_line_event'
