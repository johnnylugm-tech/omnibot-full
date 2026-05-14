"""[FR-04] Input Sanitizer L2 — NFKC normalization and control character removal.

Citations: SRS.md:59-68
"""

import unicodedata
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


def x_sanitize__mutmut_orig(text: str) -> str:
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


def x_sanitize__mutmut_1(text: str) -> str:
    """Normalize user input: NFKC compose, strip control chars, trim whitespace.

    Keeps newline (\\n) and tab (\\t) as printable characters.
    Does NOT perform pattern matching — that is L3's responsibility.

    Raises:
        ValueError: if input contains malformed Unicode sequences.
    """
    try:
        # Step 1: NFKC normalization
        text = None
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


def x_sanitize__mutmut_2(text: str) -> str:
    """Normalize user input: NFKC compose, strip control chars, trim whitespace.

    Keeps newline (\\n) and tab (\\t) as printable characters.
    Does NOT perform pattern matching — that is L3's responsibility.

    Raises:
        ValueError: if input contains malformed Unicode sequences.
    """
    try:
        # Step 1: NFKC normalization
        text = unicodedata.normalize(None, text)
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


def x_sanitize__mutmut_3(text: str) -> str:
    """Normalize user input: NFKC compose, strip control chars, trim whitespace.

    Keeps newline (\\n) and tab (\\t) as printable characters.
    Does NOT perform pattern matching — that is L3's responsibility.

    Raises:
        ValueError: if input contains malformed Unicode sequences.
    """
    try:
        # Step 1: NFKC normalization
        text = unicodedata.normalize("NFKC", None)
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


def x_sanitize__mutmut_4(text: str) -> str:
    """Normalize user input: NFKC compose, strip control chars, trim whitespace.

    Keeps newline (\\n) and tab (\\t) as printable characters.
    Does NOT perform pattern matching — that is L3's responsibility.

    Raises:
        ValueError: if input contains malformed Unicode sequences.
    """
    try:
        # Step 1: NFKC normalization
        text = unicodedata.normalize(text)
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


def x_sanitize__mutmut_5(text: str) -> str:
    """Normalize user input: NFKC compose, strip control chars, trim whitespace.

    Keeps newline (\\n) and tab (\\t) as printable characters.
    Does NOT perform pattern matching — that is L3's responsibility.

    Raises:
        ValueError: if input contains malformed Unicode sequences.
    """
    try:
        # Step 1: NFKC normalization
        text = unicodedata.normalize("NFKC", )
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


def x_sanitize__mutmut_6(text: str) -> str:
    """Normalize user input: NFKC compose, strip control chars, trim whitespace.

    Keeps newline (\\n) and tab (\\t) as printable characters.
    Does NOT perform pattern matching — that is L3's responsibility.

    Raises:
        ValueError: if input contains malformed Unicode sequences.
    """
    try:
        # Step 1: NFKC normalization
        text = unicodedata.normalize("XXNFKCXX", text)
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


def x_sanitize__mutmut_7(text: str) -> str:
    """Normalize user input: NFKC compose, strip control chars, trim whitespace.

    Keeps newline (\\n) and tab (\\t) as printable characters.
    Does NOT perform pattern matching — that is L3's responsibility.

    Raises:
        ValueError: if input contains malformed Unicode sequences.
    """
    try:
        # Step 1: NFKC normalization
        text = unicodedata.normalize("nfkc", text)
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


def x_sanitize__mutmut_8(text: str) -> str:
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
        raise ValueError(None) from e

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


def x_sanitize__mutmut_9(text: str) -> str:
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
    cleaned = None
    for ch in text:
        cp = ord(ch)
        if unicodedata.category(ch) == "Cc" and cp not in (0x0A, 0x09):
            continue
        cleaned.append(ch)
    text = "".join(cleaned)

    # Step 3: Strip leading/trailing whitespace
    text = text.strip()

    return text


def x_sanitize__mutmut_10(text: str) -> str:
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
        cp = None
        if unicodedata.category(ch) == "Cc" and cp not in (0x0A, 0x09):
            continue
        cleaned.append(ch)
    text = "".join(cleaned)

    # Step 3: Strip leading/trailing whitespace
    text = text.strip()

    return text


def x_sanitize__mutmut_11(text: str) -> str:
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
        cp = ord(None)
        if unicodedata.category(ch) == "Cc" and cp not in (0x0A, 0x09):
            continue
        cleaned.append(ch)
    text = "".join(cleaned)

    # Step 3: Strip leading/trailing whitespace
    text = text.strip()

    return text


def x_sanitize__mutmut_12(text: str) -> str:
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
        if unicodedata.category(ch) == "Cc" or cp not in (0x0A, 0x09):
            continue
        cleaned.append(ch)
    text = "".join(cleaned)

    # Step 3: Strip leading/trailing whitespace
    text = text.strip()

    return text


def x_sanitize__mutmut_13(text: str) -> str:
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
        if unicodedata.category(None) == "Cc" and cp not in (0x0A, 0x09):
            continue
        cleaned.append(ch)
    text = "".join(cleaned)

    # Step 3: Strip leading/trailing whitespace
    text = text.strip()

    return text


def x_sanitize__mutmut_14(text: str) -> str:
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
        if unicodedata.category(ch) != "Cc" and cp not in (0x0A, 0x09):
            continue
        cleaned.append(ch)
    text = "".join(cleaned)

    # Step 3: Strip leading/trailing whitespace
    text = text.strip()

    return text


def x_sanitize__mutmut_15(text: str) -> str:
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
        if unicodedata.category(ch) == "XXCcXX" and cp not in (0x0A, 0x09):
            continue
        cleaned.append(ch)
    text = "".join(cleaned)

    # Step 3: Strip leading/trailing whitespace
    text = text.strip()

    return text


def x_sanitize__mutmut_16(text: str) -> str:
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
        if unicodedata.category(ch) == "cc" and cp not in (0x0A, 0x09):
            continue
        cleaned.append(ch)
    text = "".join(cleaned)

    # Step 3: Strip leading/trailing whitespace
    text = text.strip()

    return text


def x_sanitize__mutmut_17(text: str) -> str:
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
        if unicodedata.category(ch) == "CC" and cp not in (0x0A, 0x09):
            continue
        cleaned.append(ch)
    text = "".join(cleaned)

    # Step 3: Strip leading/trailing whitespace
    text = text.strip()

    return text


def x_sanitize__mutmut_18(text: str) -> str:
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
        if unicodedata.category(ch) == "Cc" and cp in (0x0A, 0x09):
            continue
        cleaned.append(ch)
    text = "".join(cleaned)

    # Step 3: Strip leading/trailing whitespace
    text = text.strip()

    return text


def x_sanitize__mutmut_19(text: str) -> str:
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
        if unicodedata.category(ch) == "Cc" and cp not in (11, 0x09):
            continue
        cleaned.append(ch)
    text = "".join(cleaned)

    # Step 3: Strip leading/trailing whitespace
    text = text.strip()

    return text


def x_sanitize__mutmut_20(text: str) -> str:
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
        if unicodedata.category(ch) == "Cc" and cp not in (0x0A, 10):
            continue
        cleaned.append(ch)
    text = "".join(cleaned)

    # Step 3: Strip leading/trailing whitespace
    text = text.strip()

    return text


def x_sanitize__mutmut_21(text: str) -> str:
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
            break
        cleaned.append(ch)
    text = "".join(cleaned)

    # Step 3: Strip leading/trailing whitespace
    text = text.strip()

    return text


def x_sanitize__mutmut_22(text: str) -> str:
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
        cleaned.append(None)
    text = "".join(cleaned)

    # Step 3: Strip leading/trailing whitespace
    text = text.strip()

    return text


def x_sanitize__mutmut_23(text: str) -> str:
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
    text = None

    # Step 3: Strip leading/trailing whitespace
    text = text.strip()

    return text


def x_sanitize__mutmut_24(text: str) -> str:
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
    text = "".join(None)

    # Step 3: Strip leading/trailing whitespace
    text = text.strip()

    return text


def x_sanitize__mutmut_25(text: str) -> str:
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
    text = "XXXX".join(cleaned)

    # Step 3: Strip leading/trailing whitespace
    text = text.strip()

    return text


def x_sanitize__mutmut_26(text: str) -> str:
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
    text = None

    return text

x_sanitize__mutmut_mutants : ClassVar[MutantDict] = {
'x_sanitize__mutmut_1': x_sanitize__mutmut_1, 
    'x_sanitize__mutmut_2': x_sanitize__mutmut_2, 
    'x_sanitize__mutmut_3': x_sanitize__mutmut_3, 
    'x_sanitize__mutmut_4': x_sanitize__mutmut_4, 
    'x_sanitize__mutmut_5': x_sanitize__mutmut_5, 
    'x_sanitize__mutmut_6': x_sanitize__mutmut_6, 
    'x_sanitize__mutmut_7': x_sanitize__mutmut_7, 
    'x_sanitize__mutmut_8': x_sanitize__mutmut_8, 
    'x_sanitize__mutmut_9': x_sanitize__mutmut_9, 
    'x_sanitize__mutmut_10': x_sanitize__mutmut_10, 
    'x_sanitize__mutmut_11': x_sanitize__mutmut_11, 
    'x_sanitize__mutmut_12': x_sanitize__mutmut_12, 
    'x_sanitize__mutmut_13': x_sanitize__mutmut_13, 
    'x_sanitize__mutmut_14': x_sanitize__mutmut_14, 
    'x_sanitize__mutmut_15': x_sanitize__mutmut_15, 
    'x_sanitize__mutmut_16': x_sanitize__mutmut_16, 
    'x_sanitize__mutmut_17': x_sanitize__mutmut_17, 
    'x_sanitize__mutmut_18': x_sanitize__mutmut_18, 
    'x_sanitize__mutmut_19': x_sanitize__mutmut_19, 
    'x_sanitize__mutmut_20': x_sanitize__mutmut_20, 
    'x_sanitize__mutmut_21': x_sanitize__mutmut_21, 
    'x_sanitize__mutmut_22': x_sanitize__mutmut_22, 
    'x_sanitize__mutmut_23': x_sanitize__mutmut_23, 
    'x_sanitize__mutmut_24': x_sanitize__mutmut_24, 
    'x_sanitize__mutmut_25': x_sanitize__mutmut_25, 
    'x_sanitize__mutmut_26': x_sanitize__mutmut_26
}

def sanitize(*args, **kwargs):
    result = _mutmut_trampoline(x_sanitize__mutmut_orig, x_sanitize__mutmut_mutants, args, kwargs)
    return result 

sanitize.__signature__ = _mutmut_signature(x_sanitize__mutmut_orig)
x_sanitize__mutmut_orig.__name__ = 'x_sanitize'
