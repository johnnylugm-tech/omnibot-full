"""[FR-02] SignatureVerifier — platform-agnostic HMAC signature verification.

Citations: SAD.md:97-109
"""

from __future__ import annotations

import hashlib
import hmac
import base64
from typing import Callable, Dict

from fastapi import Request, HTTPException
from omnibot.models import Platform
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


def x_verify_telegram_signature__mutmut_orig(secret: str, body: bytes, signature: str) -> bool:
    """Verify Telegram HMAC-SHA256 signature.

    Telegram uses SHA256(bot_token) as the secret key for HMAC.
    """
    secret_key = hashlib.sha256(secret.encode()).digest()
    expected = hmac.new(secret_key, body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def x_verify_telegram_signature__mutmut_1(secret: str, body: bytes, signature: str) -> bool:
    """Verify Telegram HMAC-SHA256 signature.

    Telegram uses SHA256(bot_token) as the secret key for HMAC.
    """
    secret_key = None
    expected = hmac.new(secret_key, body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def x_verify_telegram_signature__mutmut_2(secret: str, body: bytes, signature: str) -> bool:
    """Verify Telegram HMAC-SHA256 signature.

    Telegram uses SHA256(bot_token) as the secret key for HMAC.
    """
    secret_key = hashlib.sha256(None).digest()
    expected = hmac.new(secret_key, body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def x_verify_telegram_signature__mutmut_3(secret: str, body: bytes, signature: str) -> bool:
    """Verify Telegram HMAC-SHA256 signature.

    Telegram uses SHA256(bot_token) as the secret key for HMAC.
    """
    secret_key = hashlib.sha256(secret.encode()).digest()
    expected = None
    return hmac.compare_digest(expected, signature)


def x_verify_telegram_signature__mutmut_4(secret: str, body: bytes, signature: str) -> bool:
    """Verify Telegram HMAC-SHA256 signature.

    Telegram uses SHA256(bot_token) as the secret key for HMAC.
    """
    secret_key = hashlib.sha256(secret.encode()).digest()
    expected = hmac.new(None, body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def x_verify_telegram_signature__mutmut_5(secret: str, body: bytes, signature: str) -> bool:
    """Verify Telegram HMAC-SHA256 signature.

    Telegram uses SHA256(bot_token) as the secret key for HMAC.
    """
    secret_key = hashlib.sha256(secret.encode()).digest()
    expected = hmac.new(secret_key, None, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def x_verify_telegram_signature__mutmut_6(secret: str, body: bytes, signature: str) -> bool:
    """Verify Telegram HMAC-SHA256 signature.

    Telegram uses SHA256(bot_token) as the secret key for HMAC.
    """
    secret_key = hashlib.sha256(secret.encode()).digest()
    expected = hmac.new(secret_key, body, None).hexdigest()
    return hmac.compare_digest(expected, signature)


def x_verify_telegram_signature__mutmut_7(secret: str, body: bytes, signature: str) -> bool:
    """Verify Telegram HMAC-SHA256 signature.

    Telegram uses SHA256(bot_token) as the secret key for HMAC.
    """
    secret_key = hashlib.sha256(secret.encode()).digest()
    expected = hmac.new(body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def x_verify_telegram_signature__mutmut_8(secret: str, body: bytes, signature: str) -> bool:
    """Verify Telegram HMAC-SHA256 signature.

    Telegram uses SHA256(bot_token) as the secret key for HMAC.
    """
    secret_key = hashlib.sha256(secret.encode()).digest()
    expected = hmac.new(secret_key, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def x_verify_telegram_signature__mutmut_9(secret: str, body: bytes, signature: str) -> bool:
    """Verify Telegram HMAC-SHA256 signature.

    Telegram uses SHA256(bot_token) as the secret key for HMAC.
    """
    secret_key = hashlib.sha256(secret.encode()).digest()
    expected = hmac.new(secret_key, body, ).hexdigest()
    return hmac.compare_digest(expected, signature)


def x_verify_telegram_signature__mutmut_10(secret: str, body: bytes, signature: str) -> bool:
    """Verify Telegram HMAC-SHA256 signature.

    Telegram uses SHA256(bot_token) as the secret key for HMAC.
    """
    secret_key = hashlib.sha256(secret.encode()).digest()
    expected = hmac.new(secret_key, body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(None, signature)


def x_verify_telegram_signature__mutmut_11(secret: str, body: bytes, signature: str) -> bool:
    """Verify Telegram HMAC-SHA256 signature.

    Telegram uses SHA256(bot_token) as the secret key for HMAC.
    """
    secret_key = hashlib.sha256(secret.encode()).digest()
    expected = hmac.new(secret_key, body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, None)


def x_verify_telegram_signature__mutmut_12(secret: str, body: bytes, signature: str) -> bool:
    """Verify Telegram HMAC-SHA256 signature.

    Telegram uses SHA256(bot_token) as the secret key for HMAC.
    """
    secret_key = hashlib.sha256(secret.encode()).digest()
    expected = hmac.new(secret_key, body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature)


def x_verify_telegram_signature__mutmut_13(secret: str, body: bytes, signature: str) -> bool:
    """Verify Telegram HMAC-SHA256 signature.

    Telegram uses SHA256(bot_token) as the secret key for HMAC.
    """
    secret_key = hashlib.sha256(secret.encode()).digest()
    expected = hmac.new(secret_key, body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, )

x_verify_telegram_signature__mutmut_mutants : ClassVar[MutantDict] = {
'x_verify_telegram_signature__mutmut_1': x_verify_telegram_signature__mutmut_1, 
    'x_verify_telegram_signature__mutmut_2': x_verify_telegram_signature__mutmut_2, 
    'x_verify_telegram_signature__mutmut_3': x_verify_telegram_signature__mutmut_3, 
    'x_verify_telegram_signature__mutmut_4': x_verify_telegram_signature__mutmut_4, 
    'x_verify_telegram_signature__mutmut_5': x_verify_telegram_signature__mutmut_5, 
    'x_verify_telegram_signature__mutmut_6': x_verify_telegram_signature__mutmut_6, 
    'x_verify_telegram_signature__mutmut_7': x_verify_telegram_signature__mutmut_7, 
    'x_verify_telegram_signature__mutmut_8': x_verify_telegram_signature__mutmut_8, 
    'x_verify_telegram_signature__mutmut_9': x_verify_telegram_signature__mutmut_9, 
    'x_verify_telegram_signature__mutmut_10': x_verify_telegram_signature__mutmut_10, 
    'x_verify_telegram_signature__mutmut_11': x_verify_telegram_signature__mutmut_11, 
    'x_verify_telegram_signature__mutmut_12': x_verify_telegram_signature__mutmut_12, 
    'x_verify_telegram_signature__mutmut_13': x_verify_telegram_signature__mutmut_13
}

def verify_telegram_signature(*args, **kwargs):
    result = _mutmut_trampoline(x_verify_telegram_signature__mutmut_orig, x_verify_telegram_signature__mutmut_mutants, args, kwargs)
    return result 

verify_telegram_signature.__signature__ = _mutmut_signature(x_verify_telegram_signature__mutmut_orig)
x_verify_telegram_signature__mutmut_orig.__name__ = 'x_verify_telegram_signature'


def x_verify_line_signature__mutmut_orig(secret: str, body: bytes, signature: str) -> bool:
    """Verify LINE HMAC-SHA256 + Base64 signature."""
    expected_bytes = hmac.new(secret.encode(), body, hashlib.sha256).digest()
    expected = base64.b64encode(expected_bytes).decode()
    return hmac.compare_digest(expected, signature)


def x_verify_line_signature__mutmut_1(secret: str, body: bytes, signature: str) -> bool:
    """Verify LINE HMAC-SHA256 + Base64 signature."""
    expected_bytes = None
    expected = base64.b64encode(expected_bytes).decode()
    return hmac.compare_digest(expected, signature)


def x_verify_line_signature__mutmut_2(secret: str, body: bytes, signature: str) -> bool:
    """Verify LINE HMAC-SHA256 + Base64 signature."""
    expected_bytes = hmac.new(None, body, hashlib.sha256).digest()
    expected = base64.b64encode(expected_bytes).decode()
    return hmac.compare_digest(expected, signature)


def x_verify_line_signature__mutmut_3(secret: str, body: bytes, signature: str) -> bool:
    """Verify LINE HMAC-SHA256 + Base64 signature."""
    expected_bytes = hmac.new(secret.encode(), None, hashlib.sha256).digest()
    expected = base64.b64encode(expected_bytes).decode()
    return hmac.compare_digest(expected, signature)


def x_verify_line_signature__mutmut_4(secret: str, body: bytes, signature: str) -> bool:
    """Verify LINE HMAC-SHA256 + Base64 signature."""
    expected_bytes = hmac.new(secret.encode(), body, None).digest()
    expected = base64.b64encode(expected_bytes).decode()
    return hmac.compare_digest(expected, signature)


def x_verify_line_signature__mutmut_5(secret: str, body: bytes, signature: str) -> bool:
    """Verify LINE HMAC-SHA256 + Base64 signature."""
    expected_bytes = hmac.new(body, hashlib.sha256).digest()
    expected = base64.b64encode(expected_bytes).decode()
    return hmac.compare_digest(expected, signature)


def x_verify_line_signature__mutmut_6(secret: str, body: bytes, signature: str) -> bool:
    """Verify LINE HMAC-SHA256 + Base64 signature."""
    expected_bytes = hmac.new(secret.encode(), hashlib.sha256).digest()
    expected = base64.b64encode(expected_bytes).decode()
    return hmac.compare_digest(expected, signature)


def x_verify_line_signature__mutmut_7(secret: str, body: bytes, signature: str) -> bool:
    """Verify LINE HMAC-SHA256 + Base64 signature."""
    expected_bytes = hmac.new(secret.encode(), body, ).digest()
    expected = base64.b64encode(expected_bytes).decode()
    return hmac.compare_digest(expected, signature)


def x_verify_line_signature__mutmut_8(secret: str, body: bytes, signature: str) -> bool:
    """Verify LINE HMAC-SHA256 + Base64 signature."""
    expected_bytes = hmac.new(secret.encode(), body, hashlib.sha256).digest()
    expected = None
    return hmac.compare_digest(expected, signature)


def x_verify_line_signature__mutmut_9(secret: str, body: bytes, signature: str) -> bool:
    """Verify LINE HMAC-SHA256 + Base64 signature."""
    expected_bytes = hmac.new(secret.encode(), body, hashlib.sha256).digest()
    expected = base64.b64encode(None).decode()
    return hmac.compare_digest(expected, signature)


def x_verify_line_signature__mutmut_10(secret: str, body: bytes, signature: str) -> bool:
    """Verify LINE HMAC-SHA256 + Base64 signature."""
    expected_bytes = hmac.new(secret.encode(), body, hashlib.sha256).digest()
    expected = base64.b64encode(expected_bytes).decode()
    return hmac.compare_digest(None, signature)


def x_verify_line_signature__mutmut_11(secret: str, body: bytes, signature: str) -> bool:
    """Verify LINE HMAC-SHA256 + Base64 signature."""
    expected_bytes = hmac.new(secret.encode(), body, hashlib.sha256).digest()
    expected = base64.b64encode(expected_bytes).decode()
    return hmac.compare_digest(expected, None)


def x_verify_line_signature__mutmut_12(secret: str, body: bytes, signature: str) -> bool:
    """Verify LINE HMAC-SHA256 + Base64 signature."""
    expected_bytes = hmac.new(secret.encode(), body, hashlib.sha256).digest()
    expected = base64.b64encode(expected_bytes).decode()
    return hmac.compare_digest(signature)


def x_verify_line_signature__mutmut_13(secret: str, body: bytes, signature: str) -> bool:
    """Verify LINE HMAC-SHA256 + Base64 signature."""
    expected_bytes = hmac.new(secret.encode(), body, hashlib.sha256).digest()
    expected = base64.b64encode(expected_bytes).decode()
    return hmac.compare_digest(expected, )

x_verify_line_signature__mutmut_mutants : ClassVar[MutantDict] = {
'x_verify_line_signature__mutmut_1': x_verify_line_signature__mutmut_1, 
    'x_verify_line_signature__mutmut_2': x_verify_line_signature__mutmut_2, 
    'x_verify_line_signature__mutmut_3': x_verify_line_signature__mutmut_3, 
    'x_verify_line_signature__mutmut_4': x_verify_line_signature__mutmut_4, 
    'x_verify_line_signature__mutmut_5': x_verify_line_signature__mutmut_5, 
    'x_verify_line_signature__mutmut_6': x_verify_line_signature__mutmut_6, 
    'x_verify_line_signature__mutmut_7': x_verify_line_signature__mutmut_7, 
    'x_verify_line_signature__mutmut_8': x_verify_line_signature__mutmut_8, 
    'x_verify_line_signature__mutmut_9': x_verify_line_signature__mutmut_9, 
    'x_verify_line_signature__mutmut_10': x_verify_line_signature__mutmut_10, 
    'x_verify_line_signature__mutmut_11': x_verify_line_signature__mutmut_11, 
    'x_verify_line_signature__mutmut_12': x_verify_line_signature__mutmut_12, 
    'x_verify_line_signature__mutmut_13': x_verify_line_signature__mutmut_13
}

def verify_line_signature(*args, **kwargs):
    result = _mutmut_trampoline(x_verify_line_signature__mutmut_orig, x_verify_line_signature__mutmut_mutants, args, kwargs)
    return result 

verify_line_signature.__signature__ = _mutmut_signature(x_verify_line_signature__mutmut_orig)
x_verify_line_signature__mutmut_orig.__name__ = 'x_verify_line_signature'


# ── Verifier registry ─────────────────────────────────────────────────────────

class PlatformVerifier:
    """Manages per-platform verifiers in an extensible registry.

    Citations: SAD.md:107-108 (VERIFIERS dict registry)
    """

    def xǁPlatformVerifierǁ__init____mutmut_orig(self):
        self._verifiers: Dict[Platform, Callable[[str, bytes, str], bool]] = {
            Platform.TELEGRAM: verify_telegram_signature,
            Platform.LINE: verify_line_signature,
        }

    def xǁPlatformVerifierǁ__init____mutmut_1(self):
        self._verifiers: Dict[Platform, Callable[[str, bytes, str], bool]] = None
    
    xǁPlatformVerifierǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPlatformVerifierǁ__init____mutmut_1': xǁPlatformVerifierǁ__init____mutmut_1
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPlatformVerifierǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁPlatformVerifierǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁPlatformVerifierǁ__init____mutmut_orig)
    xǁPlatformVerifierǁ__init____mutmut_orig.__name__ = 'xǁPlatformVerifierǁ__init__'

    def xǁPlatformVerifierǁregister__mutmut_orig(self, platform: Platform, verifier: Callable[[str, bytes, str], bool]) -> None:
        """Register a new platform verifier."""
        self._verifiers[platform] = verifier

    def xǁPlatformVerifierǁregister__mutmut_1(self, platform: Platform, verifier: Callable[[str, bytes, str], bool]) -> None:
        """Register a new platform verifier."""
        self._verifiers[platform] = None
    
    xǁPlatformVerifierǁregister__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPlatformVerifierǁregister__mutmut_1': xǁPlatformVerifierǁregister__mutmut_1
    }
    
    def register(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPlatformVerifierǁregister__mutmut_orig"), object.__getattribute__(self, "xǁPlatformVerifierǁregister__mutmut_mutants"), args, kwargs, self)
        return result 
    
    register.__signature__ = _mutmut_signature(xǁPlatformVerifierǁregister__mutmut_orig)
    xǁPlatformVerifierǁregister__mutmut_orig.__name__ = 'xǁPlatformVerifierǁregister'

    def xǁPlatformVerifierǁverify__mutmut_orig(self, platform: Platform, secret: str, body: bytes, signature: str) -> bool:
        """Verify signature for a given platform."""
        verifier = self._verifiers.get(platform)
        if verifier is None:
            raise ValueError(f"No verifier registered for platform: {platform}")
        return verifier(secret, body, signature)

    def xǁPlatformVerifierǁverify__mutmut_1(self, platform: Platform, secret: str, body: bytes, signature: str) -> bool:
        """Verify signature for a given platform."""
        verifier = None
        if verifier is None:
            raise ValueError(f"No verifier registered for platform: {platform}")
        return verifier(secret, body, signature)

    def xǁPlatformVerifierǁverify__mutmut_2(self, platform: Platform, secret: str, body: bytes, signature: str) -> bool:
        """Verify signature for a given platform."""
        verifier = self._verifiers.get(None)
        if verifier is None:
            raise ValueError(f"No verifier registered for platform: {platform}")
        return verifier(secret, body, signature)

    def xǁPlatformVerifierǁverify__mutmut_3(self, platform: Platform, secret: str, body: bytes, signature: str) -> bool:
        """Verify signature for a given platform."""
        verifier = self._verifiers.get(platform)
        if verifier is not None:
            raise ValueError(f"No verifier registered for platform: {platform}")
        return verifier(secret, body, signature)

    def xǁPlatformVerifierǁverify__mutmut_4(self, platform: Platform, secret: str, body: bytes, signature: str) -> bool:
        """Verify signature for a given platform."""
        verifier = self._verifiers.get(platform)
        if verifier is None:
            raise ValueError(None)
        return verifier(secret, body, signature)

    def xǁPlatformVerifierǁverify__mutmut_5(self, platform: Platform, secret: str, body: bytes, signature: str) -> bool:
        """Verify signature for a given platform."""
        verifier = self._verifiers.get(platform)
        if verifier is None:
            raise ValueError(f"No verifier registered for platform: {platform}")
        return verifier(None, body, signature)

    def xǁPlatformVerifierǁverify__mutmut_6(self, platform: Platform, secret: str, body: bytes, signature: str) -> bool:
        """Verify signature for a given platform."""
        verifier = self._verifiers.get(platform)
        if verifier is None:
            raise ValueError(f"No verifier registered for platform: {platform}")
        return verifier(secret, None, signature)

    def xǁPlatformVerifierǁverify__mutmut_7(self, platform: Platform, secret: str, body: bytes, signature: str) -> bool:
        """Verify signature for a given platform."""
        verifier = self._verifiers.get(platform)
        if verifier is None:
            raise ValueError(f"No verifier registered for platform: {platform}")
        return verifier(secret, body, None)

    def xǁPlatformVerifierǁverify__mutmut_8(self, platform: Platform, secret: str, body: bytes, signature: str) -> bool:
        """Verify signature for a given platform."""
        verifier = self._verifiers.get(platform)
        if verifier is None:
            raise ValueError(f"No verifier registered for platform: {platform}")
        return verifier(body, signature)

    def xǁPlatformVerifierǁverify__mutmut_9(self, platform: Platform, secret: str, body: bytes, signature: str) -> bool:
        """Verify signature for a given platform."""
        verifier = self._verifiers.get(platform)
        if verifier is None:
            raise ValueError(f"No verifier registered for platform: {platform}")
        return verifier(secret, signature)

    def xǁPlatformVerifierǁverify__mutmut_10(self, platform: Platform, secret: str, body: bytes, signature: str) -> bool:
        """Verify signature for a given platform."""
        verifier = self._verifiers.get(platform)
        if verifier is None:
            raise ValueError(f"No verifier registered for platform: {platform}")
        return verifier(secret, body, )
    
    xǁPlatformVerifierǁverify__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPlatformVerifierǁverify__mutmut_1': xǁPlatformVerifierǁverify__mutmut_1, 
        'xǁPlatformVerifierǁverify__mutmut_2': xǁPlatformVerifierǁverify__mutmut_2, 
        'xǁPlatformVerifierǁverify__mutmut_3': xǁPlatformVerifierǁverify__mutmut_3, 
        'xǁPlatformVerifierǁverify__mutmut_4': xǁPlatformVerifierǁverify__mutmut_4, 
        'xǁPlatformVerifierǁverify__mutmut_5': xǁPlatformVerifierǁverify__mutmut_5, 
        'xǁPlatformVerifierǁverify__mutmut_6': xǁPlatformVerifierǁverify__mutmut_6, 
        'xǁPlatformVerifierǁverify__mutmut_7': xǁPlatformVerifierǁverify__mutmut_7, 
        'xǁPlatformVerifierǁverify__mutmut_8': xǁPlatformVerifierǁverify__mutmut_8, 
        'xǁPlatformVerifierǁverify__mutmut_9': xǁPlatformVerifierǁverify__mutmut_9, 
        'xǁPlatformVerifierǁverify__mutmut_10': xǁPlatformVerifierǁverify__mutmut_10
    }
    
    def verify(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPlatformVerifierǁverify__mutmut_orig"), object.__getattribute__(self, "xǁPlatformVerifierǁverify__mutmut_mutants"), args, kwargs, self)
        return result 
    
    verify.__signature__ = _mutmut_signature(xǁPlatformVerifierǁverify__mutmut_orig)
    xǁPlatformVerifierǁverify__mutmut_orig.__name__ = 'xǁPlatformVerifierǁverify'


VERIFIERS = PlatformVerifier()


# ── FastAPI dependency ────────────────────────────────────────────────────────

_PLATFORM_CONFIG: Dict[Platform, Dict[str, str]] = {
    Platform.TELEGRAM: {
        "secret_header": "X-Telegram-Bot-Token",
        "signature_header": "X-Telegram-Hmac-Signature",
    },
    Platform.LINE: {
        "secret_header": "X-Line-Channel-Secret",
        "signature_header": "X-Line-Signature",
    },
}


async def x_verify_signature__mutmut_orig(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_1(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = None
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_2(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(None)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_3(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is not None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_4(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=None, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_5(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=None)

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_6(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_7(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, )

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_8(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=401, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_9(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = None
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_10(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(None)
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_11(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["XXsecret_headerXX"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_12(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["SECRET_HEADER"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_13(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = None

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_14(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(None)

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_15(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["XXsignature_headerXX"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_16(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["SIGNATURE_HEADER"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_17(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret and not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_18(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_19(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_20(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=None,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_21(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail=None,
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_22(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_23(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_24(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=402,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_25(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="XXAUTH_INVALID_SIGNATURE: missing credentialsXX",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_26(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="auth_invalid_signature: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_27(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: MISSING CREDENTIALS",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_28(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = None

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_29(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_30(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(None, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_31(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, None, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_32(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, None, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_33(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, None):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_34(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_35(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_36(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_37(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, ):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_38(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=None,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_39(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail=None,
        )

    return body


async def x_verify_signature__mutmut_40(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_41(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            )

    return body


async def x_verify_signature__mutmut_42(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=402,
            detail="AUTH_INVALID_SIGNATURE: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_43(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="XXAUTH_INVALID_SIGNATURE: signature mismatchXX",
        )

    return body


async def x_verify_signature__mutmut_44(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="auth_invalid_signature: signature mismatch",
        )

    return body


async def x_verify_signature__mutmut_45(request: Request, platform: Platform) -> bytes:
    """FastAPI dependency: verify webhook signature and return raw body bytes.

    Raises HTTPException(401) if signature is missing or invalid.
    """
    config = _PLATFORM_CONFIG.get(platform)
    if config is None:
        raise HTTPException(status_code=400, detail=f"AUTH_UNSUPPORTED_PLATFORM: {platform.value}")

    secret = request.headers.get(config["secret_header"])
    signature = request.headers.get(config["signature_header"])

    if not secret or not signature:
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: missing credentials",
        )

    body = await request.body()

    if not VERIFIERS.verify(platform, secret, body, signature):
        raise HTTPException(
            status_code=401,
            detail="AUTH_INVALID_SIGNATURE: SIGNATURE MISMATCH",
        )

    return body

x_verify_signature__mutmut_mutants : ClassVar[MutantDict] = {
'x_verify_signature__mutmut_1': x_verify_signature__mutmut_1, 
    'x_verify_signature__mutmut_2': x_verify_signature__mutmut_2, 
    'x_verify_signature__mutmut_3': x_verify_signature__mutmut_3, 
    'x_verify_signature__mutmut_4': x_verify_signature__mutmut_4, 
    'x_verify_signature__mutmut_5': x_verify_signature__mutmut_5, 
    'x_verify_signature__mutmut_6': x_verify_signature__mutmut_6, 
    'x_verify_signature__mutmut_7': x_verify_signature__mutmut_7, 
    'x_verify_signature__mutmut_8': x_verify_signature__mutmut_8, 
    'x_verify_signature__mutmut_9': x_verify_signature__mutmut_9, 
    'x_verify_signature__mutmut_10': x_verify_signature__mutmut_10, 
    'x_verify_signature__mutmut_11': x_verify_signature__mutmut_11, 
    'x_verify_signature__mutmut_12': x_verify_signature__mutmut_12, 
    'x_verify_signature__mutmut_13': x_verify_signature__mutmut_13, 
    'x_verify_signature__mutmut_14': x_verify_signature__mutmut_14, 
    'x_verify_signature__mutmut_15': x_verify_signature__mutmut_15, 
    'x_verify_signature__mutmut_16': x_verify_signature__mutmut_16, 
    'x_verify_signature__mutmut_17': x_verify_signature__mutmut_17, 
    'x_verify_signature__mutmut_18': x_verify_signature__mutmut_18, 
    'x_verify_signature__mutmut_19': x_verify_signature__mutmut_19, 
    'x_verify_signature__mutmut_20': x_verify_signature__mutmut_20, 
    'x_verify_signature__mutmut_21': x_verify_signature__mutmut_21, 
    'x_verify_signature__mutmut_22': x_verify_signature__mutmut_22, 
    'x_verify_signature__mutmut_23': x_verify_signature__mutmut_23, 
    'x_verify_signature__mutmut_24': x_verify_signature__mutmut_24, 
    'x_verify_signature__mutmut_25': x_verify_signature__mutmut_25, 
    'x_verify_signature__mutmut_26': x_verify_signature__mutmut_26, 
    'x_verify_signature__mutmut_27': x_verify_signature__mutmut_27, 
    'x_verify_signature__mutmut_28': x_verify_signature__mutmut_28, 
    'x_verify_signature__mutmut_29': x_verify_signature__mutmut_29, 
    'x_verify_signature__mutmut_30': x_verify_signature__mutmut_30, 
    'x_verify_signature__mutmut_31': x_verify_signature__mutmut_31, 
    'x_verify_signature__mutmut_32': x_verify_signature__mutmut_32, 
    'x_verify_signature__mutmut_33': x_verify_signature__mutmut_33, 
    'x_verify_signature__mutmut_34': x_verify_signature__mutmut_34, 
    'x_verify_signature__mutmut_35': x_verify_signature__mutmut_35, 
    'x_verify_signature__mutmut_36': x_verify_signature__mutmut_36, 
    'x_verify_signature__mutmut_37': x_verify_signature__mutmut_37, 
    'x_verify_signature__mutmut_38': x_verify_signature__mutmut_38, 
    'x_verify_signature__mutmut_39': x_verify_signature__mutmut_39, 
    'x_verify_signature__mutmut_40': x_verify_signature__mutmut_40, 
    'x_verify_signature__mutmut_41': x_verify_signature__mutmut_41, 
    'x_verify_signature__mutmut_42': x_verify_signature__mutmut_42, 
    'x_verify_signature__mutmut_43': x_verify_signature__mutmut_43, 
    'x_verify_signature__mutmut_44': x_verify_signature__mutmut_44, 
    'x_verify_signature__mutmut_45': x_verify_signature__mutmut_45
}

def verify_signature(*args, **kwargs):
    result = _mutmut_trampoline(x_verify_signature__mutmut_orig, x_verify_signature__mutmut_mutants, args, kwargs)
    return result 

verify_signature.__signature__ = _mutmut_signature(x_verify_signature__mutmut_orig)
x_verify_signature__mutmut_orig.__name__ = 'x_verify_signature'
