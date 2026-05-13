"""[FR-01] FastAPI application with platform webhook endpoints.

Citations: SAD.md:287-288 (API routes), SRS.md:13-25
"""

from dataclasses import asdict
from datetime import datetime
from typing import Any, Dict

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from omnibot.adapters.telegram import parse_telegram_update
from omnibot.adapters.line import parse_line_event

app = FastAPI()

SUPPORTED_PLATFORMS = {"telegram": parse_telegram_update, "line": parse_line_event}


def _serialize_message(msg: Any) -> Dict[str, Any]:
    """Serialize a UnifiedMessage to a JSON-safe dict."""
    data = asdict(msg)
    for key, value in data.items():
        if isinstance(value, datetime):
            data[key] = value.isoformat()
    return data


@app.post("/api/v1/webhook/{platform}")
async def webhook(platform: str, request: Request):
    """Receive webhook from a platform, parse into UnifiedMessage."""
    parser = SUPPORTED_PLATFORMS.get(platform.lower())
    if parser is None:
        return JSONResponse(
            status_code=400, content={"detail": f"Unsupported platform: {platform}"}
        )
    try:
        payload = await request.json()
        message = parser(payload)
    except (ValueError, KeyError) as e:
        return JSONResponse(
            status_code=400, content={"detail": str(e)}
        )
    return JSONResponse(content=_serialize_message(message))
