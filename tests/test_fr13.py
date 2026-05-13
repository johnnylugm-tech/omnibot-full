"""FR-13: Docker Compose Development Environment.

[FR-13] Acceptance criteria:
  - docker compose up starts omnibot-api (port 8000), postgres (pgvector/pg16), redis (7-alpine)
  - postgres and redis have healthchecks
  - API container depends on postgres/redis healthy
  - Redis password protected (requirepass)

Citations: SRS.md FR-13 section, SAD.md 2.8.1
"""

import os
import yaml


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _compose():
    with open(os.path.join(PROJECT_ROOT, "docker-compose.yml")) as f:
        return yaml.safe_load(f)


def test_compose_file_exists():
    """docker-compose.yml exists in project root."""
    path = os.path.join(PROJECT_ROOT, "docker-compose.yml")
    assert os.path.isfile(path)


def test_dockerfile_exists():
    """Dockerfile exists in 03-development."""
    path = os.path.join(PROJECT_ROOT, "03-development", "Dockerfile")
    assert os.path.isfile(path)


def test_three_services():
    """docker-compose has exactly 3 services."""
    compose = _compose()
    services = compose.get("services", {})
    assert len(services) == 3


def test_service_names():
    """Services: omnibot-api, postgres, redis."""
    compose = _compose()
    names = set(compose.get("services", {}).keys())
    assert names == {"omnibot-api", "postgres", "redis"}


def test_postgres_image():
    """postgres uses pgvector/pgvector:pg16 image."""
    compose = _compose()
    pg = compose["services"]["postgres"]
    assert "pgvector/pgvector" in pg.get("image", "")


def test_redis_image():
    """redis uses redis:7-alpine image."""
    compose = _compose()
    redis = compose["services"]["redis"]
    assert "redis" in redis.get("image", "")
    assert "alpine" in redis.get("image", "")


def test_api_port_mapping():
    """omnibot-api exposes port 8000."""
    compose = _compose()
    ports = compose["services"]["omnibot-api"].get("ports", [])
    assert any("8000" in str(p) for p in ports)


def test_postgres_healthcheck():
    """postgres service has healthcheck."""
    compose = _compose()
    pg = compose["services"]["postgres"]
    assert "healthcheck" in pg


def test_redis_healthcheck():
    """redis service has healthcheck."""
    compose = _compose()
    redis = compose["services"]["redis"]
    assert "healthcheck" in redis


def test_api_depends_on_both():
    """omnibot-api depends_on postgres and redis."""
    compose = _compose()
    depends = compose["services"]["omnibot-api"].get("depends_on", {})
    assert "postgres" in depends
    assert "redis" in depends


def test_api_depends_condition_healthy():
    """API depends on postgres and redis with service_healthy condition."""
    compose = _compose()
    depends = compose["services"]["omnibot-api"]["depends_on"]
    for svc in ("postgres", "redis"):
        entry = depends[svc]
        assert entry.get("condition") == "service_healthy"


def test_redis_requirepass():
    """Redis has requirepass configuration for password protection."""
    compose = _compose()
    redis = compose["services"]["redis"]
    # requirepass can be in command or environment
    cmd = " ".join(redis.get("command", [])) if isinstance(redis.get("command"), list) else redis.get("command", "")
    env = redis.get("environment", {})
    has_requirepass = "requirepass" in str(cmd).lower() or any("requirepass" in str(v).lower() for v in (env.values() if isinstance(env, dict) else env))
    assert has_requirepass
