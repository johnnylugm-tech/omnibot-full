"""FR-01: Platform Adapter — Telegram + LINE Webhook.

[FR-01] Acceptance criteria:
  - POST /api/v1/webhook/telegram correctly parses Telegram Update
  - POST /api/v1/webhook/line correctly parses LINE WebhookEvent
  - Both endpoints return 200 OK within 3s
  - Unsupported platform request returns 400 Bad Request

Citations: SRS.md:13-25, SAD.md:64-167
"""

import hashlib
import hmac
import json
import time
from fastapi.testclient import TestClient

from omnibot.app import app
from omnibot.models import Platform, MessageType

client = TestClient(app)


def _telegram_signature(bot_token: str, body: bytes) -> str:
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    return hmac.new(secret_key, body, hashlib.sha256).hexdigest()


def _telegram_headers(body: bytes, bot_token: str = "test:token123") -> dict:
    return {
        "Content-Type": "application/json",
        "X-Telegram-Bot-Token": bot_token,
        "X-Telegram-Hmac-Signature": _telegram_signature(bot_token, body),
    }


# ── Telegram webhook ──────────────────────────────────────────────────────────

TELEGRAM_TEXT_UPDATE = {
    "update_id": 123456789,
    "message": {
        "message_id": 42,
        "from": {
            "id": 12345,
            "is_bot": False,
            "first_name": "Test",
            "username": "testuser",
        },
        "chat": {"id": 12345, "first_name": "Test", "type": "private"},
        "date": 1700000000,
        "text": "Hello, bot!",
    },
}


def test_telegram_webhook_text_message():
    """POST /api/v1/webhook/telegram parses a text message and returns 200."""
    body = json.dumps(TELEGRAM_TEXT_UPDATE).encode()
    response = client.post(
        "/api/v1/webhook/telegram",
        content=body,
        headers=_telegram_headers(body),
    )
    assert response.status_code == 200
    data = response.json()
    assert data["platform"] == "TELEGRAM"
    assert data["platform_user_id"] == "12345"
    assert data["message_type"] == "TEXT"
    assert data["content"] == "Hello, bot!"
    assert "received_at" in data


def test_telegram_webhook_response_time():
    """Telegram webhook responds within 3 seconds."""
    body = json.dumps(TELEGRAM_TEXT_UPDATE).encode()
    headers = _telegram_headers(body)
    start = time.monotonic()
    client.post("/api/v1/webhook/telegram", content=body, headers=headers)
    elapsed = time.monotonic() - start
    assert elapsed < 3.0


def _line_headers(body: bytes, channel_secret: str = "line_secret_test") -> dict:
    import base64
    sig = base64.b64encode(
        hmac.new(channel_secret.encode(), body, hashlib.sha256).digest()
    ).decode()
    return {
        "Content-Type": "application/json",
        "X-Line-Channel-Secret": channel_secret,
        "X-Line-Signature": sig,
    }


# ── LINE webhook ──────────────────────────────────────────────────────────────

LINE_TEXT_EVENT = {
    "destination": "U0123456789abcdef",
    "events": [
        {
            "type": "message",
            "message": {"type": "text", "id": "12345678901", "text": "Hello LINE!"},
            "timestamp": 1700000000000,
            "source": {
                "type": "user",
                "userId": "Ulineuser123",
            },
            "replyToken": "abcd1234reply",
            "mode": "active",
        }
    ],
}


def test_line_webhook_text_message():
    """POST /api/v1/webhook/line parses a text message and returns 200."""
    body = json.dumps(LINE_TEXT_EVENT).encode()
    response = client.post(
        "/api/v1/webhook/line",
        content=body,
        headers=_line_headers(body),
    )
    assert response.status_code == 200
    data = response.json()
    assert data["platform"] == "LINE"
    assert data["platform_user_id"] == "Ulineuser123"
    assert data["message_type"] == "TEXT"
    assert data["content"] == "Hello LINE!"
    assert "received_at" in data
    assert data.get("reply_token") == "abcd1234reply"


def test_line_webhook_response_time():
    """LINE webhook responds within 3 seconds."""
    body = json.dumps(LINE_TEXT_EVENT).encode()
    headers = _line_headers(body)
    start = time.monotonic()
    client.post("/api/v1/webhook/line", content=body, headers=headers)
    elapsed = time.monotonic() - start
    assert elapsed < 3.0


# ── Unsupported platform ──────────────────────────────────────────────────────

def test_unsupported_platform_returns_400():
    """POST to an unknown platform returns 400 Bad Request."""
    response = client.post("/api/v1/webhook/unknown", json={})
    assert response.status_code == 400


def test_line_empty_events_returns_400():
    """LINE webhook with empty events array returns 400 Bad Request."""
    body = json.dumps({"events": []}).encode()
    response = client.post(
        "/api/v1/webhook/line",
        content=body,
        headers=_line_headers(body),
    )
    assert response.status_code == 400


# ── Platform enum ─────────────────────────────────────────────────────────────

def test_platform_enum_values():
    """Platform enum contains TELEGRAM, LINE, MESSENGER, WHATSAPP."""
    assert Platform.TELEGRAM.value == "TELEGRAM"
    assert Platform.LINE.value == "LINE"
    assert Platform.MESSENGER.value == "MESSENGER"
    assert Platform.WHATSAPP.value == "WHATSAPP"


def test_message_type_enum_values():
    """MessageType enum contains TEXT, IMAGE, STICKER, LOCATION, FILE."""
    assert MessageType.TEXT.value == "TEXT"
    assert MessageType.IMAGE.value == "IMAGE"
    assert MessageType.STICKER.value == "STICKER"
    assert MessageType.LOCATION.value == "LOCATION"
    assert MessageType.FILE.value == "FILE"
