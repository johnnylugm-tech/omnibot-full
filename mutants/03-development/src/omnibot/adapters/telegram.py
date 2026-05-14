"""[FR-01] TelegramAdapter — parse Telegram Update → UnifiedMessage.

Citations: SAD.md:68-81
"""

from typing import Any, Dict

from omnibot.models import UnifiedMessage, Platform, MessageType
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


def x_parse_telegram_update__mutmut_orig(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get("chat", {})

    platform_user_id = str(chat.get("id", ""))
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_1(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = None
    chat = message.get("chat", {})

    platform_user_id = str(chat.get("id", ""))
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_2(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get(None, {})
    chat = message.get("chat", {})

    platform_user_id = str(chat.get("id", ""))
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_3(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", None)
    chat = message.get("chat", {})

    platform_user_id = str(chat.get("id", ""))
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_4(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get({})
    chat = message.get("chat", {})

    platform_user_id = str(chat.get("id", ""))
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_5(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", )
    chat = message.get("chat", {})

    platform_user_id = str(chat.get("id", ""))
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_6(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("XXmessageXX", {})
    chat = message.get("chat", {})

    platform_user_id = str(chat.get("id", ""))
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_7(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("MESSAGE", {})
    chat = message.get("chat", {})

    platform_user_id = str(chat.get("id", ""))
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_8(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = None

    platform_user_id = str(chat.get("id", ""))
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_9(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get(None, {})

    platform_user_id = str(chat.get("id", ""))
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_10(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get("chat", None)

    platform_user_id = str(chat.get("id", ""))
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_11(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get({})

    platform_user_id = str(chat.get("id", ""))
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_12(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get("chat", )

    platform_user_id = str(chat.get("id", ""))
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_13(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get("XXchatXX", {})

    platform_user_id = str(chat.get("id", ""))
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_14(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get("CHAT", {})

    platform_user_id = str(chat.get("id", ""))
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_15(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get("chat", {})

    platform_user_id = None
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_16(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get("chat", {})

    platform_user_id = str(None)
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_17(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get("chat", {})

    platform_user_id = str(chat.get(None, ""))
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_18(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get("chat", {})

    platform_user_id = str(chat.get("id", None))
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_19(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get("chat", {})

    platform_user_id = str(chat.get(""))
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_20(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get("chat", {})

    platform_user_id = str(chat.get("id", ))
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_21(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get("chat", {})

    platform_user_id = str(chat.get("XXidXX", ""))
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_22(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get("chat", {})

    platform_user_id = str(chat.get("ID", ""))
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_23(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get("chat", {})

    platform_user_id = str(chat.get("id", "XXXX"))
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_24(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get("chat", {})

    platform_user_id = str(chat.get("id", ""))
    text = None
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_25(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get("chat", {})

    platform_user_id = str(chat.get("id", ""))
    text = message.get(None, "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_26(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get("chat", {})

    platform_user_id = str(chat.get("id", ""))
    text = message.get("text", None)
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_27(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get("chat", {})

    platform_user_id = str(chat.get("id", ""))
    text = message.get("")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_28(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get("chat", {})

    platform_user_id = str(chat.get("id", ""))
    text = message.get("text", )
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_29(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get("chat", {})

    platform_user_id = str(chat.get("id", ""))
    text = message.get("XXtextXX", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_30(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get("chat", {})

    platform_user_id = str(chat.get("id", ""))
    text = message.get("TEXT", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_31(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get("chat", {})

    platform_user_id = str(chat.get("id", ""))
    text = message.get("text", "XXXX")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_32(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get("chat", {})

    platform_user_id = str(chat.get("id", ""))
    text = message.get("text", "")
    message_type = None

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_33(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get("chat", {})

    platform_user_id = str(chat.get("id", ""))
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=None,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_34(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get("chat", {})

    platform_user_id = str(chat.get("id", ""))
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=None,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_35(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get("chat", {})

    platform_user_id = str(chat.get("id", ""))
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=None,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_36(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get("chat", {})

    platform_user_id = str(chat.get("id", ""))
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=None,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_37(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get("chat", {})

    platform_user_id = str(chat.get("id", ""))
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=None,
    )


def x_parse_telegram_update__mutmut_38(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get("chat", {})

    platform_user_id = str(chat.get("id", ""))
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_39(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get("chat", {})

    platform_user_id = str(chat.get("id", ""))
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        message_type=message_type,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_40(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get("chat", {})

    platform_user_id = str(chat.get("id", ""))
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        content=text,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_41(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get("chat", {})

    platform_user_id = str(chat.get("id", ""))
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        raw_payload=payload,
    )


def x_parse_telegram_update__mutmut_42(payload: Dict[str, Any]) -> UnifiedMessage:
    """Parse a Telegram Bot API Update object into a UnifiedMessage."""
    message = payload.get("message", {})
    chat = message.get("chat", {})

    platform_user_id = str(chat.get("id", ""))
    text = message.get("text", "")
    message_type = MessageType.TEXT

    # Future: handle photo, sticker, location, document message types

    return UnifiedMessage(
        platform=Platform.TELEGRAM,
        platform_user_id=platform_user_id,
        message_type=message_type,
        content=text,
        )

x_parse_telegram_update__mutmut_mutants : ClassVar[MutantDict] = {
'x_parse_telegram_update__mutmut_1': x_parse_telegram_update__mutmut_1, 
    'x_parse_telegram_update__mutmut_2': x_parse_telegram_update__mutmut_2, 
    'x_parse_telegram_update__mutmut_3': x_parse_telegram_update__mutmut_3, 
    'x_parse_telegram_update__mutmut_4': x_parse_telegram_update__mutmut_4, 
    'x_parse_telegram_update__mutmut_5': x_parse_telegram_update__mutmut_5, 
    'x_parse_telegram_update__mutmut_6': x_parse_telegram_update__mutmut_6, 
    'x_parse_telegram_update__mutmut_7': x_parse_telegram_update__mutmut_7, 
    'x_parse_telegram_update__mutmut_8': x_parse_telegram_update__mutmut_8, 
    'x_parse_telegram_update__mutmut_9': x_parse_telegram_update__mutmut_9, 
    'x_parse_telegram_update__mutmut_10': x_parse_telegram_update__mutmut_10, 
    'x_parse_telegram_update__mutmut_11': x_parse_telegram_update__mutmut_11, 
    'x_parse_telegram_update__mutmut_12': x_parse_telegram_update__mutmut_12, 
    'x_parse_telegram_update__mutmut_13': x_parse_telegram_update__mutmut_13, 
    'x_parse_telegram_update__mutmut_14': x_parse_telegram_update__mutmut_14, 
    'x_parse_telegram_update__mutmut_15': x_parse_telegram_update__mutmut_15, 
    'x_parse_telegram_update__mutmut_16': x_parse_telegram_update__mutmut_16, 
    'x_parse_telegram_update__mutmut_17': x_parse_telegram_update__mutmut_17, 
    'x_parse_telegram_update__mutmut_18': x_parse_telegram_update__mutmut_18, 
    'x_parse_telegram_update__mutmut_19': x_parse_telegram_update__mutmut_19, 
    'x_parse_telegram_update__mutmut_20': x_parse_telegram_update__mutmut_20, 
    'x_parse_telegram_update__mutmut_21': x_parse_telegram_update__mutmut_21, 
    'x_parse_telegram_update__mutmut_22': x_parse_telegram_update__mutmut_22, 
    'x_parse_telegram_update__mutmut_23': x_parse_telegram_update__mutmut_23, 
    'x_parse_telegram_update__mutmut_24': x_parse_telegram_update__mutmut_24, 
    'x_parse_telegram_update__mutmut_25': x_parse_telegram_update__mutmut_25, 
    'x_parse_telegram_update__mutmut_26': x_parse_telegram_update__mutmut_26, 
    'x_parse_telegram_update__mutmut_27': x_parse_telegram_update__mutmut_27, 
    'x_parse_telegram_update__mutmut_28': x_parse_telegram_update__mutmut_28, 
    'x_parse_telegram_update__mutmut_29': x_parse_telegram_update__mutmut_29, 
    'x_parse_telegram_update__mutmut_30': x_parse_telegram_update__mutmut_30, 
    'x_parse_telegram_update__mutmut_31': x_parse_telegram_update__mutmut_31, 
    'x_parse_telegram_update__mutmut_32': x_parse_telegram_update__mutmut_32, 
    'x_parse_telegram_update__mutmut_33': x_parse_telegram_update__mutmut_33, 
    'x_parse_telegram_update__mutmut_34': x_parse_telegram_update__mutmut_34, 
    'x_parse_telegram_update__mutmut_35': x_parse_telegram_update__mutmut_35, 
    'x_parse_telegram_update__mutmut_36': x_parse_telegram_update__mutmut_36, 
    'x_parse_telegram_update__mutmut_37': x_parse_telegram_update__mutmut_37, 
    'x_parse_telegram_update__mutmut_38': x_parse_telegram_update__mutmut_38, 
    'x_parse_telegram_update__mutmut_39': x_parse_telegram_update__mutmut_39, 
    'x_parse_telegram_update__mutmut_40': x_parse_telegram_update__mutmut_40, 
    'x_parse_telegram_update__mutmut_41': x_parse_telegram_update__mutmut_41, 
    'x_parse_telegram_update__mutmut_42': x_parse_telegram_update__mutmut_42
}

def parse_telegram_update(*args, **kwargs):
    result = _mutmut_trampoline(x_parse_telegram_update__mutmut_orig, x_parse_telegram_update__mutmut_mutants, args, kwargs)
    return result 

parse_telegram_update.__signature__ = _mutmut_signature(x_parse_telegram_update__mutmut_orig)
x_parse_telegram_update__mutmut_orig.__name__ = 'x_parse_telegram_update'
