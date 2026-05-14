"""[FR-05] PII Masking L4 — Phone, Email, Address detection and masking.

Citations: SRS.md FR-05 section
"""

import re
from dataclasses import dataclass, field
from typing import List
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

# ── PII Mask Result ─────────────────────────────────────────────────────────────

@dataclass
class PIIMaskResult:
    """Result of PII masking operation.

    Citations: SRS.md FR-05 AC: PIIMaskResult(masked_text, mask_count, pii_types)
    """
    masked_text: str
    mask_count: int = 0
    pii_types: List[str] = field(default_factory=list)


# ── Patterns ──────────────────────────────────────────────────────────────────

_TW_MOBILE = re.compile(r"\b09\d{2}[-\s]?\d{3}[-\s]?\d{3}\b")
_TW_LANDLINE = re.compile(r"\b0\d{1,2}[-\s]?\d{4}[-\s]?\d{4}\b")
_EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
_TW_ADDRESS = re.compile(
    r"(?:台北|新北|桃園|台中|臺中|台南|臺南|高雄"
    r"|基隆|新竹|嘉義|苗栗|彰化|南投|雲林"
    r"|屏東|宜蘭|花蓮|臺東|台東|澎湖|金門|連江)"
    r"(?:市|縣)"
    r"(?:.{0,5}?(?:區|鄉|鎮|市))?"
    r".{1,20}?(?:路|街|巷|弄|號|樓|段|里|村)"
    r".{0,10}"
)

# Keywords that trigger escalation
_SENSITIVE_KEYWORDS = [
    "自殺", "自殘", "自傷",
    "報警", "報案", "110",
    "緊急", "求救", "救命",
    "生命危險", "危及生命",
    "password", "密碼", "銀行帳戶", "bank account",
    "信用卡", "credit card", "提款卡", "debit card",
    "銀行卡號", "card number", "身分證", "身份證",
]


# ── Escalation flag ───────────────────────────────────────────────────────────

@dataclass
class EscalationFlag:
    """Raised when user message contains sensitive keywords.

    Citations: SRS.md FR-05 escalation requirement
    """
    message: str
    keywords: List[str] = field(default_factory=list)
    escalate: bool = True


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_orig(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_1(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = None
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_2(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = None
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_3(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = None

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_4(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 1

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_5(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(None):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_6(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append(None)
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_7(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("XXphoneXX")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_8(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("PHONE")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_9(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = None
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_10(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn(None, result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_11(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", None)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_12(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn(result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_13(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", )
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_14(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("XX[PHONE]XX", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_15(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[phone]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_16(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count = n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_17(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count -= n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_18(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = None
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_19(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn(None, result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_20(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", None)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_21(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn(result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_22(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", )
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_23(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("XX[PHONE]XX", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_24(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[phone]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_25(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count = n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_26(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count -= n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_27(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 or "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_28(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n >= 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_29(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 1 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_30(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "XXphoneXX" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_31(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "PHONE" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_32(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_33(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append(None)

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_34(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("XXphoneXX")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_35(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("PHONE")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_36(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(None):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_37(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append(None)
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_38(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("XXemailXX")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_39(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("EMAIL")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_40(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = None
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_41(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn(None, result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_42(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", None)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_43(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn(result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_44(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", )
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_45(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("XX[EMAIL]XX", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_46(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[email]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_47(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count = n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_48(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count -= n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_49(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(None):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_50(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append(None)
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_51(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("XXaddressXX")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_52(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("ADDRESS")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_53(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = None
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_54(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn(None, result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_55(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", None)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_56(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn(result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_57(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", )
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_58(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("XX[ADDR]XX", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_59(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[addr]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_60(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count = n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_61(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count -= n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_62(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=None, mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_63(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=None, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_64(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, pii_types=None)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_65(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(mask_count=mask_count, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_66(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, pii_types=pii_types)


# ── Public API ────────────────────────────────────────────────────────────────

def x_mask_pii__mutmut_67(text: str) -> PIIMaskResult:
    """Mask PII in text: phone numbers, emails, and addresses.

    Returns PIIMaskResult with masked_text, count of masks applied, and PII types found.
    """
    result = text
    pii_types: List[str] = []
    mask_count = 0

    if _TW_MOBILE.search(result):
        pii_types.append("phone")
    result, n = _TW_MOBILE.subn("[PHONE]", result)
    mask_count += n
    result, n = _TW_LANDLINE.subn("[PHONE]", result)
    mask_count += n
    if n > 0 and "phone" not in pii_types:
        pii_types.append("phone")

    if _EMAIL.search(text):
        pii_types.append("email")
    result, n = _EMAIL.subn("[EMAIL]", result)
    mask_count += n

    if _TW_ADDRESS.search(text):
        pii_types.append("address")
    result, n = _TW_ADDRESS.subn("[ADDR]", result)
    mask_count += n

    return PIIMaskResult(masked_text=result, mask_count=mask_count, )

x_mask_pii__mutmut_mutants : ClassVar[MutantDict] = {
'x_mask_pii__mutmut_1': x_mask_pii__mutmut_1, 
    'x_mask_pii__mutmut_2': x_mask_pii__mutmut_2, 
    'x_mask_pii__mutmut_3': x_mask_pii__mutmut_3, 
    'x_mask_pii__mutmut_4': x_mask_pii__mutmut_4, 
    'x_mask_pii__mutmut_5': x_mask_pii__mutmut_5, 
    'x_mask_pii__mutmut_6': x_mask_pii__mutmut_6, 
    'x_mask_pii__mutmut_7': x_mask_pii__mutmut_7, 
    'x_mask_pii__mutmut_8': x_mask_pii__mutmut_8, 
    'x_mask_pii__mutmut_9': x_mask_pii__mutmut_9, 
    'x_mask_pii__mutmut_10': x_mask_pii__mutmut_10, 
    'x_mask_pii__mutmut_11': x_mask_pii__mutmut_11, 
    'x_mask_pii__mutmut_12': x_mask_pii__mutmut_12, 
    'x_mask_pii__mutmut_13': x_mask_pii__mutmut_13, 
    'x_mask_pii__mutmut_14': x_mask_pii__mutmut_14, 
    'x_mask_pii__mutmut_15': x_mask_pii__mutmut_15, 
    'x_mask_pii__mutmut_16': x_mask_pii__mutmut_16, 
    'x_mask_pii__mutmut_17': x_mask_pii__mutmut_17, 
    'x_mask_pii__mutmut_18': x_mask_pii__mutmut_18, 
    'x_mask_pii__mutmut_19': x_mask_pii__mutmut_19, 
    'x_mask_pii__mutmut_20': x_mask_pii__mutmut_20, 
    'x_mask_pii__mutmut_21': x_mask_pii__mutmut_21, 
    'x_mask_pii__mutmut_22': x_mask_pii__mutmut_22, 
    'x_mask_pii__mutmut_23': x_mask_pii__mutmut_23, 
    'x_mask_pii__mutmut_24': x_mask_pii__mutmut_24, 
    'x_mask_pii__mutmut_25': x_mask_pii__mutmut_25, 
    'x_mask_pii__mutmut_26': x_mask_pii__mutmut_26, 
    'x_mask_pii__mutmut_27': x_mask_pii__mutmut_27, 
    'x_mask_pii__mutmut_28': x_mask_pii__mutmut_28, 
    'x_mask_pii__mutmut_29': x_mask_pii__mutmut_29, 
    'x_mask_pii__mutmut_30': x_mask_pii__mutmut_30, 
    'x_mask_pii__mutmut_31': x_mask_pii__mutmut_31, 
    'x_mask_pii__mutmut_32': x_mask_pii__mutmut_32, 
    'x_mask_pii__mutmut_33': x_mask_pii__mutmut_33, 
    'x_mask_pii__mutmut_34': x_mask_pii__mutmut_34, 
    'x_mask_pii__mutmut_35': x_mask_pii__mutmut_35, 
    'x_mask_pii__mutmut_36': x_mask_pii__mutmut_36, 
    'x_mask_pii__mutmut_37': x_mask_pii__mutmut_37, 
    'x_mask_pii__mutmut_38': x_mask_pii__mutmut_38, 
    'x_mask_pii__mutmut_39': x_mask_pii__mutmut_39, 
    'x_mask_pii__mutmut_40': x_mask_pii__mutmut_40, 
    'x_mask_pii__mutmut_41': x_mask_pii__mutmut_41, 
    'x_mask_pii__mutmut_42': x_mask_pii__mutmut_42, 
    'x_mask_pii__mutmut_43': x_mask_pii__mutmut_43, 
    'x_mask_pii__mutmut_44': x_mask_pii__mutmut_44, 
    'x_mask_pii__mutmut_45': x_mask_pii__mutmut_45, 
    'x_mask_pii__mutmut_46': x_mask_pii__mutmut_46, 
    'x_mask_pii__mutmut_47': x_mask_pii__mutmut_47, 
    'x_mask_pii__mutmut_48': x_mask_pii__mutmut_48, 
    'x_mask_pii__mutmut_49': x_mask_pii__mutmut_49, 
    'x_mask_pii__mutmut_50': x_mask_pii__mutmut_50, 
    'x_mask_pii__mutmut_51': x_mask_pii__mutmut_51, 
    'x_mask_pii__mutmut_52': x_mask_pii__mutmut_52, 
    'x_mask_pii__mutmut_53': x_mask_pii__mutmut_53, 
    'x_mask_pii__mutmut_54': x_mask_pii__mutmut_54, 
    'x_mask_pii__mutmut_55': x_mask_pii__mutmut_55, 
    'x_mask_pii__mutmut_56': x_mask_pii__mutmut_56, 
    'x_mask_pii__mutmut_57': x_mask_pii__mutmut_57, 
    'x_mask_pii__mutmut_58': x_mask_pii__mutmut_58, 
    'x_mask_pii__mutmut_59': x_mask_pii__mutmut_59, 
    'x_mask_pii__mutmut_60': x_mask_pii__mutmut_60, 
    'x_mask_pii__mutmut_61': x_mask_pii__mutmut_61, 
    'x_mask_pii__mutmut_62': x_mask_pii__mutmut_62, 
    'x_mask_pii__mutmut_63': x_mask_pii__mutmut_63, 
    'x_mask_pii__mutmut_64': x_mask_pii__mutmut_64, 
    'x_mask_pii__mutmut_65': x_mask_pii__mutmut_65, 
    'x_mask_pii__mutmut_66': x_mask_pii__mutmut_66, 
    'x_mask_pii__mutmut_67': x_mask_pii__mutmut_67
}

def mask_pii(*args, **kwargs):
    result = _mutmut_trampoline(x_mask_pii__mutmut_orig, x_mask_pii__mutmut_mutants, args, kwargs)
    return result 

mask_pii.__signature__ = _mutmut_signature(x_mask_pii__mutmut_orig)
x_mask_pii__mutmut_orig.__name__ = 'x_mask_pii'


def x_contains_sensitive_keywords__mutmut_orig(text: str) -> bool:
    """Check if text contains keywords that require escalation."""
    return any(kw in text for kw in _SENSITIVE_KEYWORDS)


def x_contains_sensitive_keywords__mutmut_1(text: str) -> bool:
    """Check if text contains keywords that require escalation."""
    return any(None)


def x_contains_sensitive_keywords__mutmut_2(text: str) -> bool:
    """Check if text contains keywords that require escalation."""
    return any(kw not in text for kw in _SENSITIVE_KEYWORDS)

x_contains_sensitive_keywords__mutmut_mutants : ClassVar[MutantDict] = {
'x_contains_sensitive_keywords__mutmut_1': x_contains_sensitive_keywords__mutmut_1, 
    'x_contains_sensitive_keywords__mutmut_2': x_contains_sensitive_keywords__mutmut_2
}

def contains_sensitive_keywords(*args, **kwargs):
    result = _mutmut_trampoline(x_contains_sensitive_keywords__mutmut_orig, x_contains_sensitive_keywords__mutmut_mutants, args, kwargs)
    return result 

contains_sensitive_keywords.__signature__ = _mutmut_signature(x_contains_sensitive_keywords__mutmut_orig)
x_contains_sensitive_keywords__mutmut_orig.__name__ = 'x_contains_sensitive_keywords'
