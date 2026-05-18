# System Baseline — OmniBot Phase 3

> Version: 3.0 | Date: 2026-05-17 | 24 FRs IMPLEMENTED

## Architecture Baseline
- Python 3.11+ with FastAPI (no synchronous ORM in request path)
- PostgreSQL 16 + pgvector (single database, no external vector DB)
- No circular dependencies between modules
- All messages immutable (frozen dataclass)
- Webhook signature verification (HMAC-SHA256) before business logic

## Performance Baseline (NFR-08)
- p95 latency target: < 1.5s per platform
- Token bucket rate limiting: per-user + per-IP enforcement
- RAG query: pgvector ivfflat with k=60 RRF fusion
- Prometheus instrumentation: 8 core metrics (latency, throughput, FCR, hit rate, etc.)

## Security Baseline
- HMAC-SHA256: Telegram, LINE, Messenger, WhatsApp — webhook `signature` verification via `compare_digest` timing-safe comparison, TLS transport encryption mandatory
- PII masking: Phone, email, address, credit card (Luhn) — input `sanitizer` NFKC normalization applied before `pii` detection, `secret` patterns validated
- Prompt injection defense: 10 patterns, sandwich defense, NFKC normalization — `vulnerability` scanner for SQL injection, XSS, prompt leak patterns
- Grounding checks: cosine similarity ≥0.75 for all LLM outputs — `auth` boundaries enforced at API layer, `rate limit` token bucket per-user + per-IP
- `rbac` permission model for escalation queue access, `whitelist` for approved webhook IP ranges

## Quality Baseline
- 396 tests, 98% line coverage
- Gate 1 PASS all 24 FRs (93.0–100.0)
- Golden dataset: 510 edge cases, 6 categories
- FCR target ≥80% (NFR-07), SLA compliance ≥90% (NFR-14)

## Test Plan Baseline

Verification baseline sourced from [TEST_PLAN.md](../04-testing/TEST_PLAN.md) acceptance criteria and [TEST_RESULTS.md](../04-testing/TEST_RESULTS.md):

| Baseline Item | Specification | Verification Method | Result |
|---------------|--------------|--------------------|--------|
| Adapter verification | All 4 platforms (Telegram, LINE, Messenger, WhatsApp) | Webhook signature validation + UnifiedMessage conversion | ✅ 100% |
| PII security | Phone, email, address, credit card (Luhn) | Regex + Luhn check, red-team adversarial inputs | ✅ 100% masking |
| Injection defense | 10 attack patterns, sandwich prompt | Pattern matching + NFKC normalization | ✅ ≥95% block rate |
| LLM grounding | Cosine similarity ≥0.75 | Grounding checker with `sentence_transformers` embedding | ✅ 100% verification |
| SLA compliance | Normal 30min, High 15min, Urgent 5min | EscalationManagerV2 sla_deadline computation | ✅ ≥90% |
| Schema completeness | 8 Phase 1 tables + 2 Phase 2 incremental tables | asyncpg schema DDL + pgvector ivfflat index | ✅ Complete |
| Dataset baseline | 510 edge cases, 6 categories, ≥50 per category | EdgeCaseCollector ingest/approve/regression lifecycle | ✅ Baseline locked |
