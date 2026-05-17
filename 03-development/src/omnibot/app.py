"""[FR-01][FR-02] FastAPI application with platform webhook endpoints.

Architecture: app.py delegates platform routing to omnibot.router and
message serialization to UnifiedMessage.to_json_dict() to minimise
cross-community coupling.

Citations: SAD.md:287-288 (API routes), SRS.md:13-41
"""

import json
import logging
from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response

from omnibot.health import HealthCheckService
from omnibot.metrics import PrometheusMetrics
from omnibot.models import UnifiedMessage
from omnibot.router import resolve_route

logger = logging.getLogger("omnibot.app")

app = FastAPI()


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global error handler — log structured error and return consistent 500 response.

    Citations: SRS.md NFR-SEC-03 (secure error handling)
    """
    logger.error(
        "Unhandled exception",
        extra={
            "path": request.url.path,
            "method": request.method,
            "error_type": type(exc).__name__,
            "error_message": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_error",
            "error_type": type(exc).__name__,
            "detail": "An unexpected error occurred. The incident has been logged.",
        },
    )


metrics_service = PrometheusMetrics()

health_service = HealthCheckService(
    postgres_check=lambda: False,  # stub — Phase 1 no DB
    redis_check=lambda: False,     # stub — Phase 1 no Redis
)


@app.post("/api/v1/webhook/{platform}")
async def webhook(platform: str, request: Request):
    """Receive webhook from a platform, verify signature, parse into UnifiedMessage."""
    route = resolve_route(platform)
    if route is None:
        return JSONResponse(
            status_code=400, content={"detail": f"Unsupported platform: {platform}"}
        )
    platform_enum, parser = route

    from omnibot.auth.verifier import verify_signature
    body = await verify_signature(request, platform_enum)

    try:
        payload = json.loads(body)
        message: UnifiedMessage = parser(payload)
    except (ValueError, KeyError, json.JSONDecodeError) as e:
        return JSONResponse(
            status_code=400, content={"detail": str(e)}
        )
    return JSONResponse(content=message.to_json_dict())


@app.get("/api/v1/health")
async def health():
    """Health check endpoint — returns postgres/redis status and uptime."""
    result = health_service.check()
    return JSONResponse(content=result)


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint — returns text format for scraping.

    Citations: SRS.md FR-22, SAD.md 2.5.9 PrometheusMetrics
    """
    return Response(content=metrics_service.get_metrics(), media_type="text/plain")
