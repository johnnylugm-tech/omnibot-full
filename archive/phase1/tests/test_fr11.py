"""FR-11: Health Check Endpoint.

[FR-11] Acceptance criteria:
  - GET /api/v1/health returns JSON {status, postgres, redis, uptime_seconds}
  - status enum: healthy / degraded / unhealthy
  - healthy: postgres=True AND redis=True
  - degraded: exactly one is False
  - unhealthy: both False

Citations: SRS.md FR-11 section, SAD.md 2.5.3 HealthCheck
"""

from omnibot.health import HealthCheckService, HealthStatus


def test_health_status_enum():
    """HealthStatus has healthy, degraded, unhealthy."""
    assert HealthStatus.HEALTHY.value == "healthy"
    assert HealthStatus.DEGRADED.value == "degraded"
    assert HealthStatus.UNHEALTHY.value == "unhealthy"


def test_both_up_is_healthy():
    """postgres=True, redis=True → healthy."""
    svc = HealthCheckService(lambda: True, lambda: True)
    result = svc.check()
    assert result["status"] == "healthy"
    assert result["postgres"] is True
    assert result["redis"] is True


def test_both_down_is_unhealthy():
    """postgres=False, redis=False → unhealthy."""
    svc = HealthCheckService(lambda: False, lambda: False)
    result = svc.check()
    assert result["status"] == "unhealthy"
    assert result["postgres"] is False
    assert result["redis"] is False


def test_postgres_down_is_degraded():
    """postgres=False, redis=True → degraded."""
    svc = HealthCheckService(lambda: False, lambda: True)
    result = svc.check()
    assert result["status"] == "degraded"


def test_redis_down_is_degraded():
    """postgres=True, redis=False → degraded."""
    svc = HealthCheckService(lambda: True, lambda: False)
    result = svc.check()
    assert result["status"] == "degraded"


def test_uptime_seconds_present():
    """Response includes uptime_seconds as a non-negative number."""
    svc = HealthCheckService(lambda: True, lambda: True)
    result = svc.check()
    assert "uptime_seconds" in result
    assert isinstance(result["uptime_seconds"], (int, float))
    assert result["uptime_seconds"] >= 0


def test_response_keys():
    """Response has exactly the expected keys."""
    svc = HealthCheckService(lambda: True, lambda: True)
    result = svc.check()
    assert set(result.keys()) == {"status", "postgres", "redis", "uptime_seconds"}


def test_uptime_monotonic():
    """uptime_seconds increases between calls."""
    import time
    svc = HealthCheckService(lambda: True, lambda: True)
    r1 = svc.check()
    time.sleep(0.02)
    r2 = svc.check()
    assert r2["uptime_seconds"] > r1["uptime_seconds"]


def test_health_endpoint_http():
    """GET /api/v1/health returns 200 with expected JSON."""
    from fastapi.testclient import TestClient
    from omnibot.app import app
    client = TestClient(app)
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert set(data.keys()) == {"status", "postgres", "redis", "uptime_seconds"}
    assert isinstance(data["postgres"], bool)
    assert isinstance(data["redis"], bool)
    assert data["status"] in ("healthy", "degraded", "unhealthy")
