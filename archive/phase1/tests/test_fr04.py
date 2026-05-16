"""FR-04: Input Sanitizer L2 — Character Normalization.

[FR-04] Acceptance criteria:
  - Input text passes through unicodedata.normalize("NFKC", text)
  - Remove all non-printable characters (keep \n, \t)
  - Result strip() leading/trailing whitespace
  - No pattern matching performed

Citations: SRS.md:59-68
"""

from omnibot.sanitizer import sanitize


def test_nfkc_normalization():
    """Fullwidth latin characters are normalized to ASCII."""
    fullwidth = "Ｈｅｌｌｏ"  # U+FF28 U+FF45 U+FF4C U+FF4C U+FF4F
    result = sanitize(fullwidth)
    assert result == "Hello"


def test_nfkc_combining_characters():
    """Combining characters are composed to precomposed form."""
    decomposed = "é"  # e + combining acute → é
    result = sanitize(decomposed)
    assert result == "é"


def test_control_characters_removed():
    """Non-printable control characters (except \n, \t) are removed."""
    text = "Hello\x00\x01\x02\x03World"
    result = sanitize(text)
    assert result == "HelloWorld"


def test_newline_and_tab_preserved():
    """\n and \t are kept as printable whitespace."""
    text = "Line1\nLine2\tindented"
    result = sanitize(text)
    assert result == "Line1\nLine2\tindented"


def test_leading_trailing_whitespace_stripped():
    """Leading and trailing whitespace is stripped."""
    text = "  \t  hello world  \n  "
    result = sanitize(text)
    assert result == "hello world"


def test_empty_string():
    """Empty string returns empty string."""
    assert sanitize("") == ""


def test_only_whitespace():
    """String of only whitespace returns empty string after strip."""
    assert sanitize("   \t\n  ") == ""


def test_unicode_emojis_preserved():
    """Emojis and normal unicode text are preserved."""
    text = "Hello 👋 World 🌍"
    result = sanitize(text)
    assert result == "Hello 👋 World 🌍"


def test_no_pattern_matching_performed():
    """Sanitizer does not perform pattern matching — only normalization."""
    text = "<script>alert('xss')</script>"
    result = sanitize(text)
    # The content should be normalized but NOT filtered — L2 only normalizes
    assert "<script>" in result
    assert "</script>" in result


def test_idempotent():
    """Applying sanitize twice gives the same result."""
    text = "  Ｈｅｌｌｏ \x00 World  "
    first = sanitize(text)
    second = sanitize(first)
    assert first == second


def test_zwj_emoji_preserved():
    """ZWJ emoji sequences (family, flags) are preserved — Cf chars not stripped."""
    family = "👨‍👩‍👧‍👦"  # man + ZWJ + woman + ZWJ + girl + ZWJ + boy
    result = sanitize(family)
    assert result == family
