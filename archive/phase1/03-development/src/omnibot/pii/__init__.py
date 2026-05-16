"""[FR-05] PII Masking L4 — Phone, Email, Address detection and masking.

Citations: SRS.md FR-05 section
"""

import re
from dataclasses import dataclass, field
from typing import List

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

def mask_pii(text: str) -> PIIMaskResult:
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


def contains_sensitive_keywords(text: str) -> bool:
    """Check if text contains keywords that require escalation."""
    return any(kw in text for kw in _SENSITIVE_KEYWORDS)
