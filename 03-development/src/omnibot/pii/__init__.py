"""[FR-05] PII Masking L4 — Phone, Email, Address detection and masking.

Citations: SRS.md FR-05 section
"""

import re
from dataclasses import dataclass, field
from typing import List


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

def mask_pii(text: str) -> str:
    """Mask PII in text: phone numbers, emails, and addresses.

    Each PII type is replaced with a corresponding tag.
    """
    text = _TW_MOBILE.sub("[PHONE]", text)
    text = _TW_LANDLINE.sub("[PHONE]", text)
    text = _EMAIL.sub("[EMAIL]", text)
    text = _TW_ADDRESS.sub("[ADDR]", text)
    return text


def contains_sensitive_keywords(text: str) -> bool:
    """Check if text contains keywords that require escalation."""
    return any(kw in text for kw in _SENSITIVE_KEYWORDS)
