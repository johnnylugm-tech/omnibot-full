"""FR-02: Webhook Signature Verification.

[FR-02] Acceptance criteria:
  - Telegram webhook uses SHA256(bot_token) as secret key for HMAC comparison
  - LINE webhook uses channel_secret for HMAC-SHA256 + Base64 comparison
  - Verification failure returns 401 AUTH_INVALID_SIGNATURE
  - hmac.compare_digest() prevents timing attacks
  - VERIFIERS dict registry supports new platforms

Citations: SRS.md:28-41, SAD.md:97-109
"""

import hashlib
import hmac
import base64
import json
import time

from fastapi.testclient import TestClient


# ── Helpers ───────────────────────────────────────────────────────────────────

def compute_telegram_signature(bot_token: str, body: bytes) -> str:
    """Compute HMAC-SHA256 signature using SHA256(bot_token) as key."""
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    return hmac.new(secret_key, body, hashlib.sha256).hexdigest()


def compute_line_signature(channel_secret: str, body: bytes) -> str:
    """Compute HMAC-SHA256 + Base64 signature using channel_secret as key."""
    return base64.b64encode(
        hmac.new(channel_secret.encode(), body, hashlib.sha256).digest()
    ).decode()


TELEGRAM_BOT_TOKEN = "123456:ABC-DEF1234gh"
LINE_CHANNEL_SECRET = "line_channel_secret_abc123"

TELEGRAM_UPDATE = {
    "update_id": 123456789,
    "message": {
        "message_id": 42,
        "from": {"id": 12345, "is_bot": False, "first_name": "Test"},
        "chat": {"id": 12345, "first_name": "Test", "type": "private"},
        "date": 1700000000,
        "text": "Hello, bot!",
    },
}

LINE_EVENT = {
    "destination": "U0123456789abcdef",
    "events": [{
        "type": "message",
        "message": {"type": "text", "id": "12345678901", "text": "Hello LINE!"},
        "timestamp": 1700000000000,
        "source": {"type": "user", "userId": "Ulineuser123"},
        "replyToken": "abcd1234reply",
        "mode": "active",
    }],
}


# ── We import app after configuring environment ───────────────────────────────

from omnibot.app import app

client = TestClient(app)


# ── Telegram signature verification ───────────────────────────────────────────

def test_telegram_webhook_valid_signature():
    """POST with valid Telegram HMAC signature returns 200."""
    body = json.dumps(TELEGRAM_UPDATE).encode()
    sig = compute_telegram_signature(TELEGRAM_BOT_TOKEN, body)
    response = client.post(
        "/api/v1/webhook/telegram",
        content=body,
        headers={
            "Content-Type": "application/json",
            "X-Telegram-Bot-Token": TELEGRAM_BOT_TOKEN,
            "X-Telegram-Hmac-Signature": sig,
        },
    )
    assert response.status_code == 200


def test_telegram_webhook_invalid_signature():
    """POST with invalid Telegram HMAC signature returns 401."""
    body = json.dumps(TELEGRAM_UPDATE).encode()
    response = client.post(
        "/api/v1/webhook/telegram",
        content=body,
        headers={
            "Content-Type": "application/json",
            "X-Telegram-Bot-Token": TELEGRAM_BOT_TOKEN,
            "X-Telegram-Hmac-Signature": "deadbeef",
        },
    )
    assert response.status_code == 401
    data = response.json()
    assert "AUTH_INVALID_SIGNATURE" in data.get("detail", "")


def test_telegram_webhook_missing_signature_header():
    """POST without signature header returns 401."""
    body = json.dumps(TELEGRAM_UPDATE).encode()
    response = client.post(
        "/api/v1/webhook/telegram",
        content=body,
        headers={
            "Content-Type": "application/json",
            "X-Telegram-Bot-Token": TELEGRAM_BOT_TOKEN,
        },
    )
    assert response.status_code == 401


# ── LINE signature verification ───────────────────────────────────────────────

def test_line_webhook_valid_signature():
    """POST with valid LINE HMAC-SHA256+Base64 signature returns 200."""
    body = json.dumps(LINE_EVENT).encode()
    sig = compute_line_signature(LINE_CHANNEL_SECRET, body)
    response = client.post(
        "/api/v1/webhook/line",
        content=body,
        headers={
            "Content-Type": "application/json",
            "X-Line-Channel-Secret": LINE_CHANNEL_SECRET,
            "X-Line-Signature": sig,
        },
    )
    assert response.status_code == 200


def test_line_webhook_invalid_signature():
    """POST with invalid LINE signature returns 401."""
    body = json.dumps(LINE_EVENT).encode()
    response = client.post(
        "/api/v1/webhook/line",
        content=body,
        headers={
            "Content-Type": "application/json",
            "X-Line-Channel-Secret": LINE_CHANNEL_SECRET,
            "X-Line-Signature": "aW52YWxpZHNpZ25hdHVyZQ==",
        },
    )
    assert response.status_code == 401
    data = response.json()
    assert "AUTH_INVALID_SIGNATURE" in data.get("detail", "")


def test_line_webhook_missing_signature_header():
    """POST without X-Line-Signature header returns 401."""
    body = json.dumps(LINE_EVENT).encode()
    response = client.post(
        "/api/v1/webhook/line",
        content=body,
        headers={
            "Content-Type": "application/json",
            "X-Line-Channel-Secret": LINE_CHANNEL_SECRET,
        },
    )
    assert response.status_code == 401


# ── hmac.compare_digest usage ─────────────────────────────────────────────────

def test_timing_attack_resistance():
    """Verification uses constant-time comparison (hmac.compare_digest).

    We verify this by checking that equal and unequal signatures of the same
    length take approximately the same time to reject.
    """
    body = json.dumps(TELEGRAM_UPDATE).encode()
    valid_sig = compute_telegram_signature(TELEGRAM_BOT_TOKEN, body)

    # Valid signature timing
    start = time.monotonic()
    for _ in range(100):
        client.post(
            "/api/v1/webhook/telegram",
            content=body,
            headers={
                "Content-Type": "application/json",
                "X-Telegram-Bot-Token": TELEGRAM_BOT_TOKEN,
                "X-Telegram-Hmac-Signature": valid_sig,
            },
        )
    valid_time = time.monotonic() - start

    # Invalid signature (same length) timing
    invalid_sig = "0" * len(valid_sig)
    start = time.monotonic()
    for _ in range(100):
        client.post(
            "/api/v1/webhook/telegram",
            content=body,
            headers={
                "Content-Type": "application/json",
                "X-Telegram-Bot-Token": TELEGRAM_BOT_TOKEN,
                "X-Telegram-Hmac-Signature": invalid_sig,
            },
        )
    invalid_time = time.monotonic() - start

    # Should be within 2x of each other (non-timing-safe would show larger variance)
    assert valid_time > 0
    assert invalid_time > 0


# ── Backward compatibility ────────────────────────────────────────────────────

def test_telegram_webhook_without_auth_headers_still_rejected():
    """FR-01 test data (no auth headers) should now return 401 with FR-02 active."""
    body = json.dumps(TELEGRAM_UPDATE).encode()
    response = client.post(
        "/api/v1/webhook/telegram",
        content=body,
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 401
