"""[FR-01][FR-02] FastAPI application with platform webhook endpoints.

Citations: SAD.md:287-288 (API routes), SRS.md:13-41
"""

import json
from dataclasses import asdict
from datetime import datetime
from typing import Any, Callable, Dict

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from omnibot.adapters.telegram import parse_telegram_update
from omnibot.adapters.line import parse_line_event
from omnibot.auth.verifier import verify_signature
from omnibot.health import HealthCheckService
from omnibot.models import Platform

app = FastAPI()
health_service = HealthCheckService(
    postgres_check=lambda: False,  # stub — Phase 1 no DB
    redis_check=lambda: False,     # stub — Phase 1 no Redis
)

PLATFORM_ROUTES: Dict[str, tuple[Platform, Callable]] = {
    "telegram": (Platform.TELEGRAM, parse_telegram_update),
    "line": (Platform.LINE, parse_line_event),
}


def _serialize_message(msg: Any) -> Dict[str, Any]:
    """Serialize a UnifiedMessage to a JSON-safe dict."""
    data = asdict(msg)
    for key, value in data.items():
        if isinstance(value, datetime):
            data[key] = value.isoformat()
    return data


@app.post("/api/v1/webhook/{platform}")
async def webhook(platform: str, request: Request):
    """Receive webhook from a platform, verify signature, parse into UnifiedMessage."""
    route = PLATFORM_ROUTES.get(platform.lower())
    if route is None:
        return JSONResponse(
            status_code=400, content={"detail": f"Unsupported platform: {platform}"}
        )
    platform_enum, parser = route

    body = await verify_signature(request, platform_enum)

    try:
        payload = json.loads(body)
        message = parser(payload)
    except (ValueError, KeyError, json.JSONDecodeError) as e:
        return JSONResponse(
            status_code=400, content={"detail": str(e)}
        )
    return JSONResponse(content=_serialize_message(message))


@app.get("/api/v1/health")
async def health():
    """Health check endpoint — returns postgres/redis status and uptime."""
    result = health_service.check()
    return JSONResponse(content=result)
