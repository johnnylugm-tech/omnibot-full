# RISK_MITIGATION_PLANS.md — omnibot-full

> **Phase**: 7 — Risk Management
> **Scope**: All HIGH risks (score ≥ 10) across FR-01 to FR-13
> **Date**: 2026-05-16
> **References**: 06-quality/QUALITY_REPORT.md

---

## Mitigation Plan Index

Only HIGH risks (score ≥ 10) require formal mitigation plans.
MEDIUM/LOW risks are mitigated inline in `RISK_REGISTER.md`.

| Plan ID | Risk ID | FR | Score | Owner | Phase Target | Status |
|---------|---------|----|-------|-------|--------------|--------|
| MP-01 | RISK-FR11-02 | FR-11 | 20 | Platform Team | Phase 2 | Open |
| MP-02 | RISK-FR11-01 | FR-11 | 15 | Platform Team | Phase 2 | Open |
| MP-03 | RISK-FR01-03 | FR-01 | 15 | Platform Team | Phase 2 | Open |
| MP-04 | RISK-FR01-05 | FR-01 | 15 | Security Team | Phase 2 | Open |
| MP-05 | RISK-FR13-02 | FR-13 | 16 | Security Team | Pre-staging | Open |
| MP-06 | RISK-FR13-01 | FR-13 | 12 | Security Team | Pre-staging | Open |
| MP-07 | RISK-FR01-02 | FR-01 | 12 | Platform Team | Phase 2 | Open |
| MP-08 | RISK-FR02-01 | FR-02 | 12 | Security Team | Phase 1 (verify) | Open |
| MP-09 | RISK-FR03-01 | FR-03 | 12 | Platform Team | Phase 2 | Open |
| MP-10 | RISK-FR04-01 | FR-04 | 12 | Security Team | Phase 2 | Open |
| MP-11 | RISK-FR04-03 | FR-04 | 12 | Security Team | Phase 2 | Open |
| MP-12 | RISK-FR05-01 | FR-05 | 12 | Compliance Team | Phase 2 | Open |
| MP-13 | RISK-FR05-02 | FR-05 | 12 | Security Team | Phase 2 | Open |
| MP-14 | RISK-FR06-01 | FR-06 | 12 | Platform Team | Phase 2 | Open |
| MP-15 | RISK-FR06-02 | FR-06 | 12 | Security Team | Phase 2 | Open |
| MP-16 | RISK-FR07-01 | FR-07 | 12 | Platform Team | Phase 2 | Open |
| MP-17 | RISK-FR07-02 | FR-07 | 12 | Platform Team | Phase 2 | Open |
| MP-18 | RISK-FR08-01 | FR-08 | 12 | Platform Team | Phase 2 | Open |
| MP-19 | RISK-FR10-02 | FR-10 | 12 | Platform Team | Phase 2 | Open |
| MP-20 | RISK-FR12-02 | FR-12 | 12 | Platform Team | Phase 2 | Open |
| MP-21 | RISK-FR12-03 | FR-12 | 12 | Security Team | Pre-staging | Open |

---

## Detailed Mitigation Plans

### MP-01 — HTTP 200 Always Returned; Orchestrators Cannot Detect Unhealthy State
**Risk**: RISK-FR11-02 | **Score**: 20 (L=5, I=4) | **Owner**: Platform Team

| Field | Detail |
|-------|--------|
| **Root cause** | `@app.get("/api/v1/health")` returns `JSONResponse` without `status_code`; defaults to HTTP 200 for all health states |
| **Target phase** | Phase 2 |
| **Acceptance criteria** | `GET /api/v1/health` returns HTTP 503 when `status == "unhealthy"`, HTTP 200 when healthy |
| **Actions** | 1. Map `HealthStatus` to HTTP codes: `HEALTHY→200`, `UNHEALTHY→503` <br>2. Pass `status_code=503` to `JSONResponse` when unhealthy <br>3. Update `tests/test_fr11.py:test_health_endpoint_http` to assert HTTP 503 for unhealthy <br>4. Document HTTP contract in SRS.md FR-11 |
| **Verification** | `curl -o /dev/null -w "%{http_code}" /api/v1/health` returns 503 under simulated failure |
| **Files** | `03-development/src/omnibot/app.py:81-85`, `tests/test_fr11.py:81-92` |

---

### MP-02 — Health Check Stubs Return Permanent `unhealthy`
**Risk**: RISK-FR11-01 | **Score**: 15 (L=5, I=3) | **Owner**: Platform Team

| Field | Detail |
|-------|--------|
| **Root cause** | `app.py:52-55` constructs `HealthCheckService(postgres_check=lambda: False, redis_check=lambda: False)` |
| **Target phase** | Phase 2 |
| **Acceptance criteria** | Probes return `True` when DB/Redis reachable; `False` on connection failure |
| **Actions** | 1. Replace stubs with real probes: `asyncpg` ping for postgres, `redis.ping()` for Redis <br>2. Wrap in `asyncio.wait_for(..., timeout=1.0)` to prevent blocking <br>3. Inject probe factory via dependency injection <br>4. Add integration test with testcontainers fixture |
| **Verification** | `docker compose up && curl /api/v1/health` returns `{"status":"healthy","postgres":true,"redis":true}` |
| **Files** | `03-development/src/omnibot/app.py:52-55`, `03-development/src/omnibot/health/__init__.py:44-52` |

---

### MP-03 — LINE 20-Second Response SLA Breach
**Risk**: RISK-FR01-03 | **Score**: 15 (L=5, I=3) | **Owner**: Platform Team

| Field | Detail |
|-------|--------|
| **Root cause** | Synchronous processing in webhook handler; downstream DB/knowledge queries block response |
| **Target phase** | Phase 2 |
| **Acceptance criteria** | Webhook handler returns 200 within 2s; processing happens asynchronously |
| **Actions** | 1. Decouple acknowledgment: return `200 OK` immediately upon HMAC validation + parse <br>2. Enqueue message to Redis/task queue for background processing <br>3. Add p95 latency metric to monitoring <br>4. Set hard 2.5s ASGI timeout at gateway layer |
| **Verification** | Load test: 100 rps, p95 < 2s response time |
| **Files** | `03-development/src/omnibot/app.py`, `01-requirements/SRS.md:FR-01` |

---

### MP-04 — Bot Token / Channel Secret Rotation Without Downtime
**Risk**: RISK-FR01-05 | **Score**: 15 (L=5, I=3) | **Owner**: Security Team

| Field | Detail |
|-------|--------|
| **Root cause** | `SignatureVerifier` reads single token from env; no multi-token overlap support |
| **Target phase** | Phase 2 |
| **Acceptance criteria** | Zero-downtime secret rotation: both old and new tokens accepted during grace period |
| **Actions** | 1. Support `TELEGRAM_BOT_TOKEN_OLD` + `TELEGRAM_BOT_TOKEN_NEW` dual-validate for 15-min window <br>2. Add `/admin/rotate-secret` endpoint requiring admin auth <br>3. Emit `security_logs` entry on token rotation events <br>4. CI secret rotation drill in staging |
| **Verification** | Rotation test: swap token, verify both old+new accepted during window, old rejected after |
| **Files** | `03-development/src/omnibot/auth/verifier.py`, `03-development/src/omnibot/schema/__init__.py:60-68` |

---

### MP-05 — `POSTGRES_PASSWORD` Hardcoded in docker-compose.yml
**Risk**: RISK-FR13-02 | **Score**: 16 (L=4, I=4) | **Owner**: Security Team

| Field | Detail |
|-------|--------|
| **Root cause** | `docker-compose.yml:13` sets `POSTGRES_PASSWORD: omnibot_dev` without env var substitution |
| **Target phase** | Pre-staging (immediate) |
| **Acceptance criteria** | No hardcoded credentials in any tracked file; all secrets via env vars |
| **Actions** | 1. Replace with `POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}` <br>2. Update DSN to `postgresql://omnibot:${POSTGRES_PASSWORD}@postgres:5432/omnibot` <br>3. Remove port 5432 binding from non-dev profiles <br>4. Add `.env.example` with placeholder values <br>5. Rotate `omnibot_dev` in all environments |
| **Verification** | `docker compose config` contains no literal `omnibot_dev`; `git log -S omnibot_dev` shows no new commits |
| **Files** | `docker-compose.yml:13`, `docker-compose.yml:44` |

---

### MP-06 — `REDIS_PASSWORD` Defaults to Hardcoded Fallback
**Risk**: RISK-FR13-01 | **Score**: 12 (L=4, I=3) | **Owner**: Security Team

| Field | Detail |
|-------|--------|
| **Root cause** | `docker-compose.yml:29` uses `${REDIS_PASSWORD:-dev_redis_password}` fallback |
| **Target phase** | Pre-staging (immediate) |
| **Acceptance criteria** | No fallback default; compose fails loudly when `REDIS_PASSWORD` not set |
| **Actions** | 1. Change to `${REDIS_PASSWORD}` (no `:-` clause) <br>2. Add `REDIS_PASSWORD=<CHANGE_ME>` to `.env.example` <br>3. Add pre-flight env validation script |
| **Verification** | `docker compose up` without env var fails with clear error about missing `REDIS_PASSWORD` |
| **Files** | `docker-compose.yml:29`, `docker-compose.yml:31`, `docker-compose.yml:45` |

---

### MP-07 — Webhook Duplicate Delivery; No Idempotency Guard
**Risk**: RISK-FR01-02 | **Score**: 12 (L=3, I=4) | **Owner**: Platform Team

| Field | Detail |
|-------|--------|
| **Root cause** | No message deduplication key; Telegram/LINE retry on timeout delivers duplicates |
| **Target phase** | Phase 2 |
| **Actions** | 1. Add `message_id` dedup key to Redis with TTL=60s <br>2. Return `200 OK` immediately on duplicate (no processing) <br>3. Log deduplicated messages to `security_logs` |
| **Files** | `03-development/src/omnibot/platforms/` |

---

### MP-08 — HMAC Verification Uses `==` Instead of `compare_digest`
**Risk**: RISK-FR02-01 | **Score**: 12 (L=3, I=4) | **Owner**: Security Team

| Field | Detail |
|-------|--------|
| **Root cause** | Potential timing leak if `==` operator used in signature comparison |
| **Target phase** | Phase 1 (verify already implemented) |
| **Actions** | 1. Verify `auth/verifier.py` uses `hmac.compare_digest()` — already in Phase 1 code <br>2. Add `bandit` check to CI: `bandit -t B105,B106,B107` to catch timing-unsafe comparisons |
| **Status** | Phase 1 code confirmed uses `hmac.compare_digest()`. Verify in CI. |
| **Files** | `03-development/src/omnibot/auth/verifier.py` |

---

### MP-09 through MP-21 (Summary)

| Plan | Risk | Key Action | Target |
|------|------|-----------|--------|
| MP-09 | RISK-FR03-01 | Versioned `UnifiedMessage` schema + adapter contract tests | Phase 2 |
| MP-10 | RISK-FR04-01 | Extend NFKC to cover composed/decomposed zero-width chars | Phase 2 |
| MP-11 | RISK-FR04-03 | Audit full Unicode control-char block list; add fuzz tests | Phase 2 |
| MP-12 | RISK-FR05-01 | Expand PII regex set; add fuzzing with real Taiwan phone/address samples | Phase 2 |
| MP-13 | RISK-FR05-02 | Normalize `should_escalate()` to constant-time keyword check | Phase 2 |
| MP-14 | RISK-FR06-01 | Migrate token bucket to Redis for distributed persistence | Phase 2 |
| MP-15 | RISK-FR06-02 | Use full `platform:user_id` hash key; add collision test | Phase 2 |
| MP-16 | RISK-FR07-01 | Add `GIN` index on `knowledge_base.question`; add EXPLAIN test | Phase 2 |
| MP-17 | RISK-FR07-02 | Expose confidence thresholds as config; add calibration tooling | Phase 2 |
| MP-18 | RISK-FR08-01 | Add `expires_at` TTL + cron cleanup to `escalation_queue` | Phase 2 |
| MP-19 | RISK-FR10-02 | Add runtime Pydantic validation to `ApiResponse[T]`; add type tests | Phase 2 |
| MP-20 | RISK-FR12-02 | Add `CREATE INDEX … USING ivfflat` as Phase 2 migration step | Phase 2 |
| MP-21 | RISK-FR12-03 | Rename column to `webhook_secret_vault_path` + CHECK constraint | Pre-staging |

---

*RISK_MITIGATION_PLANS.md v1.0 · Phase 7 exit · 2026-05-16*
