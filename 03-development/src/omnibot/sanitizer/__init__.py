"""[FR-04] Input Sanitizer L2 — NFKC normalization and control character removal.

Citations: SRS.md:59-68
"""

import unicodedata


def sanitize(text: str) -> str:
    """Normalize user input: NFKC compose, strip control chars, trim whitespace.

    Keeps newline (\\n) and tab (\\t) as printable characters.
    Does NOT perform pattern matching — that is L3's responsibility.

    Raises:
        ValueError: if input contains malformed Unicode sequences.
    """
    try:
        # Step 1: NFKC normalization
        text = unicodedata.normalize("NFKC", text)
    except (UnicodeError, TypeError) as e:
        raise ValueError(f"Input text contains malformed Unicode: {e}") from e

    # Step 2: Remove non-printable control characters, keeping \n and \t
    # Unicode categories C (control) except \n (U+000A) and \t (U+0009)
    cleaned = []
    for ch in text:
        cp = ord(ch)
        if unicodedata.category(ch) == "Cc" and cp not in (0x0A, 0x09):
            continue
        cleaned.append(ch)
    text = "".join(cleaned)

    # Step 3: Strip leading/trailing whitespace
    text = text.strip()

    return text
