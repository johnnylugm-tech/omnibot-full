# Requirements Traceability Matrix — OmniBot Phase 1

> **Project**: OmniBot — 多平台客服機器人
> **Phase**: 1 (Requirements Specification)
> **Version**: 1.0
> **Date**: 2026-05-13
> **Depends on**: SRS.md v1.0, SPEC_TRACKING.md v1.0

---

## Forward Traceability: FR → Design → Test

| FR-ID | Requirement | Design Element (P2) | Implementation (P3) | Test Type (P4) | Acceptance (P5) |
|-------|------------|--------------------|--------------------|----------------|-----------------|
| FR-01 | Platform Adapter — Telegram + LINE Webhook | PlatformAdapter interface, TelegramAdapter, LineAdapter | `POST /api/v1/webhook/{telegram,line}` | Integration test (webhook sim) | Webhook round-trip E2E |
| FR-02 | Webhook Signature Verification | WebhookVerifier ABC, LineWebhookVerifier, TelegramWebhookVerifier | Auth middleware per-endpoint | Unit test (HMAC vectors) + Penetration test | 401 on invalid signature |
| FR-03 | Unified Message Format | UnifiedMessage dataclass, UnifiedResponse dataclass, Platform enum, MessageType enum | `platform/adapter/models.py` | Unit test (serialization) | Cross-platform message parity |
| FR-04 | Input Sanitizer L2 | InputSanitizer class | `security/input_sanitizer.py` | Unit test (NFKC vectors) | Malformed input rejection |
| FR-05 | PII Masking L4 | PIIMaskResult dataclass, PIIMasking class | `security/pii_masking.py` | Unit test (regex patterns) + Privacy audit | PII-free log output |
| FR-06 | Rate Limiter — Token Bucket | TokenBucket dataclass, RateLimiter class | `middleware/rate_limiter.py` | Unit test (bucket math) + Load test | 429 on exhaustion |
| FR-07 | Knowledge Layer V1 — Rule Match + Escalate | KnowledgeLayerV1 class, KnowledgeResult dataclass | `knowledge/layer_v1.py` | Unit test (SQL match vectors) + Integration test | FCR >= 50% |
| FR-08 | Basic Escalation Manager | BasicEscalationManager class, EscalationRequest dataclass | `escalation/manager.py` | Integration test (queue flow) | Escalation created/assigned/resolved |
| FR-09 | Structured Logger | StructuredLogger class | `logging/structured_logger.py` | Unit test (JSON schema) | NDJSON valid per-line |
| FR-10 | API Response Format | ApiResponse[T], PaginatedResponse[T] | `api/schemas/response.py` | Unit test (serialization) | Consistent API contract |
| FR-11 | Health Check Endpoint | Health check route handler | `GET /api/v1/health` | Integration test (DB+Redis status) | Docker healthcheck pass |
| FR-12 | Database Schema — All Core Tables | 8 CREATE TABLE statements, indexes | `db/schema.sql` | Migration test + Schema validation | All tables + indexes exist |
| FR-13 | Docker Compose Development Environment | docker-compose.yml, Dockerfile | `docker-compose.yml` | Smoke test (compose up) | All services healthy |

## Backward Traceability: Test → FR

| Test Case (expected) | Covers FR | Verification Method |
|----------------------|-----------|---------------------|
| Webhook round-trip E2E (Telegram) | FR-01, FR-02, FR-03 | P5 acceptance |
| Webhook round-trip E2E (LINE) | FR-01, FR-02, FR-03 | P5 acceptance |
| HMAC signature valid/invalid vectors | FR-02 | P3 unit test |
| UnifiedMessage serialization round-trip | FR-03 | P3 unit test |
| NFKC normalization edge cases | FR-04 | P3 unit test |
| PII regex pattern coverage (phone/email/address) | FR-05 | P3 unit test |
| Token bucket consume/refill math | FR-06 | P3 unit test |
| Rate limit exhaustion → 429 response | FR-06, FR-10 | P4 integration test |
| Rule match confidence thresholds (0.95/0.7) | FR-07 | P3 unit test |
| Rule match → escalate fallback | FR-07, FR-08 | P4 integration test |
| Escalation lifecycle (create/assign/resolve) | FR-08 | P4 integration test |
| JSON log schema validation | FR-09 | P3 unit test |
| ApiResponse/PaginatedResponse serialization | FR-10 | P3 unit test |
| Health check: healthy/degraded/unhealthy states | FR-11 | P4 integration test |
| Schema migration up/down | FR-12 | P3 migration test |
| Docker compose all services healthy | FR-11, FR-13 | P3 smoke test |

## NFR Traceability

| NFR-ID | Requirement | Measurement Artifact | Verification Phase |
|--------|------------|---------------------|--------------------|
| NFR-01 | FCR >= 50% | ODD SQL query (SPEC/omnibot-phase-1.md L811-L822) | P3–P5 |
| NFR-02 | p95 Latency < 3.0s | ODD SQL query (SPEC/omnibot-phase-1.md L824-L832) | P3–P5 |
| NFR-03 | Telegram + LINE support | Webhook E2E test x2 | P3–P5 |
| NFR-04 | Webhook verification 100% | security_logs counter query | P3–P5 |
| NFR-05 | JSON structured logging | Log schema validator | P3–P5 |
| NFR-06 | PII masking coverage | Unit test coverage report | P3–P5 |

## Coverage Summary

| Metric | Count | Coverage |
|--------|-------|----------|
| Total FRs | 13 | 100% traced |
| FRs with design element | 13 | 100% |
| FRs with test type | 13 | 100% |
| FRs with acceptance criteria | 13 | 100% |
| Test cases (forward) | 16 | ≥1 per FR |
| FRs per test case | 1–3 | Bidirectional |
| NFRs with measurement artifact | 6 | 100% |
| Orphan FRs | 0 | — |
| Orphan tests | 0 | — |

---

*TRACEABILITY_MATRIX.md v1.0 — forward and backward traceability for Phase 1 scope*
