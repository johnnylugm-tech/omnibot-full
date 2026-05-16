# Traceability Matrix — OmniBot Phase 2

> **Project**: OmniBot — Multi-Platform Customer Service Bot
> **Phase**: 2 (Smart + Security Enhancement)
> **Version**: 2.0
> **Date**: 2026-05-17
> **References**: 01-requirements/SRS.md v2.0, 01-requirements/SPEC_TRACKING.md v2.0

---

## Phase 1 Baseline — Summary (FR-01–FR-13)

> All FR-01–FR-13 requirements were verified in Phase 1. They remain in effect as the foundation
> for Phase 2. See archive/phase1/TRACEABILITY_MATRIX.md for the full Phase 1 matrix.

| FR | Name | Priority | SRS § | Status | Verified |
|----|------|----------|-------|--------|----------|
| FR-01 | Platform Adapter — Telegram + LINE Webhook | P0 | SRS.md §FR-01 | COMPLETE | P5 Verified |
| FR-02 | Webhook Signature Verification | P0 | SRS.md §FR-02 | COMPLETE | P5 Verified |
| FR-03 | Unified Message Format | P0 | SRS.md §FR-03 | COMPLETE | P5 Verified |
| FR-04 | Input Sanitizer L2 — Character Normalization | P1 | SRS.md §FR-04 | COMPLETE | P5 Verified |
| FR-05 | PII Masking L4 — Phone / Email / Address | P1 | SRS.md §FR-05 | COMPLETE | P5 Verified |
| FR-06 | Rate Limiter — Token Bucket | P1 | SRS.md §FR-06 | COMPLETE | P5 Verified |
| FR-07 | Knowledge Layer V1 — Rule Match + Escalate | P0 | SRS.md §FR-07 | COMPLETE | P5 Verified |
| FR-08 | Basic Escalation Manager — No SLA | P1 | SRS.md §FR-08 | COMPLETE | P5 Verified |
| FR-09 | Structured Logger — JSON Format | P1 | SRS.md §FR-09 | COMPLETE | P5 Verified |
| FR-10 | API Response Format — ApiResponse / PaginatedResponse | P1 | SRS.md §FR-10 | COMPLETE | P5 Verified |
| FR-11 | Health Check Endpoint | P1 | SRS.md §FR-11 | COMPLETE | P5 Verified |
| FR-12 | Database Schema — All Core Tables | P0 | SRS.md §FR-12 | COMPLETE | P5 Verified |
| FR-13 | Docker Compose Development Environment | P2 | SRS.md §FR-13 | COMPLETE | P5 Verified |

---

## Forward Traceability (Spec → Implementation)

### Phase 2 New: FR-14–FR-24

| FR | SRS Section | Spec Source (SPEC/omnibot-phase-2.md) | Implementation Module (planned) | Test Module (planned) | Verification Status |
|----|------------|---------------------------------------|-------------------------------|----------------------|---------------------|
| FR-14 | SRS.md §FR-14 | L115–L156 | `src/omnibot/adapters/messenger.py` `src/omnibot/adapters/whatsapp.py` `src/omnibot/security/webhook_verifier.py` | `tests/test_fr14.py` | Not Started |
| FR-15 | SRS.md §FR-15 | L572–L640 | `src/omnibot/security/prompt_injection_defense.py` | `tests/test_fr15.py` | Not Started |
| FR-16 | SRS.md §FR-16 | L644–L699 | `src/omnibot/security/pii_masking_v2.py` | `tests/test_fr16.py` | Not Started |
| FR-17 | SRS.md §FR-17 | L226–L284 | `src/omnibot/analytics/emotion_analyzer.py` | `tests/test_fr17.py` | Not Started |
| FR-18 | SRS.md §FR-18 | L159–L222 | `src/omnibot/dialogue/dst.py` `src/omnibot/dialogue/intent_router.py` | `tests/test_fr18.py` | Not Started |
| FR-19 | SRS.md §FR-19 | L288–L490 | `src/omnibot/knowledge/hybrid_v7.py` | `tests/test_fr19.py` | Not Started |
| FR-20 | SRS.md §FR-20 | L494–L568 | `src/omnibot/escalation/manager_v2.py` | `tests/test_fr20.py` | Not Started |
| FR-21 | SRS.md §FR-21 | L703–L745 | `src/omnibot/security/grounding_checker.py` | `tests/test_fr21.py` | Not Started |
| FR-22 | SRS.md §FR-22 | L749–L793 | `src/omnibot/observability/metrics.py` | `tests/test_fr22.py` | Not Started |
| FR-23 | SRS.md §FR-23 | L797–L836 | `src/omnibot/db/migrations/phase2.py` | `tests/test_fr23.py` | Not Started |
| FR-24 | SRS.md §FR-24 | L840–L857 | `src/omnibot/quality/golden_dataset.py` | `tests/test_fr24.py` | Not Started |

### Phase 1 Baseline: FR-01–FR-13 (Forward)

| FR | SRS Section | Spec Source (SPEC/omnibot-phase-1.md) | Implementation Module | Test Module | Verification Status |
|----|------------|---------------------------------------|----------------------|-------------|---------------------|
| FR-01 | SRS.md §FR-01 | Phase 1 SPEC | `src/omnibot/adapters/telegram.py` `src/omnibot/adapters/line.py` | `tests/test_fr01.py` | P5 Verified |
| FR-02 | SRS.md §FR-02 | Phase 1 SPEC | `src/omnibot/security/webhook_verifier.py` | `tests/test_fr02.py` | P5 Verified |
| FR-03 | SRS.md §FR-03 | Phase 1 SPEC | `src/omnibot/platform/adapter/models.py` | `tests/test_fr03.py` | P5 Verified |
| FR-04 | SRS.md §FR-04 | Phase 1 SPEC | `src/omnibot/security/input_sanitizer.py` | `tests/test_fr04.py` | P5 Verified |
| FR-05 | SRS.md §FR-05 | Phase 1 SPEC | `src/omnibot/security/pii_masking.py` | `tests/test_fr05.py` | P5 Verified |
| FR-06 | SRS.md §FR-06 | Phase 1 SPEC | `src/omnibot/middleware/rate_limiter.py` | `tests/test_fr06.py` | P5 Verified |
| FR-07 | SRS.md §FR-07 | Phase 1 SPEC | `src/omnibot/knowledge/layer_v1.py` | `tests/test_fr07.py` | P5 Verified |
| FR-08 | SRS.md §FR-08 | Phase 1 SPEC | `src/omnibot/escalation/manager.py` | `tests/test_fr08.py` | P5 Verified |
| FR-09 | SRS.md §FR-09 | Phase 1 SPEC | `src/omnibot/logging/structured_logger.py` | `tests/test_fr09.py` | P5 Verified |
| FR-10 | SRS.md §FR-10 | Phase 1 SPEC | `src/omnibot/api/schemas/response.py` | `tests/test_fr10.py` | P5 Verified |
| FR-11 | SRS.md §FR-11 | Phase 1 SPEC | `src/omnibot/api/routes/health.py` | `tests/test_fr11.py` | P5 Verified |
| FR-12 | SRS.md §FR-12 | Phase 1 SPEC | `src/omnibot/db/schema.sql` | `tests/test_fr12.py` | P5 Verified |
| FR-13 | SRS.md §FR-13 | Phase 1 SPEC | `docker-compose.yml` | `tests/test_fr13.py` | P5 Verified |

---

## Backward Traceability (Implementation → Spec)

### Phase 2 New Modules

| Implementation Module (planned) | FR(s) Covered | SRS Reference | NFR(s) Covered |
|--------------------------------|---------------|---------------|----------------|
| `src/omnibot/adapters/messenger.py` | FR-14, FR-02 | SRS.md §FR-14, §FR-02 | NFR-03, NFR-09, NFR-10 |
| `src/omnibot/adapters/whatsapp.py` | FR-14, FR-02 | SRS.md §FR-14, §FR-02 | NFR-03, NFR-09, NFR-10 |
| `src/omnibot/security/webhook_verifier.py` | FR-02, FR-14 | SRS.md §FR-02, §FR-14 | NFR-04, NFR-10 |
| `src/omnibot/security/prompt_injection_defense.py` | FR-15 | SRS.md §FR-15 | NFR-12 |
| `src/omnibot/security/pii_masking_v2.py` | FR-05, FR-16 | SRS.md §FR-05, §FR-16 | NFR-06, NFR-11 |
| `src/omnibot/security/grounding_checker.py` | FR-21 | SRS.md §FR-21 | NFR-13 |
| `src/omnibot/analytics/emotion_analyzer.py` | FR-17 | SRS.md §FR-17 | — |
| `src/omnibot/dialogue/dst.py` | FR-18 | SRS.md §FR-18 | — |
| `src/omnibot/dialogue/intent_router.py` | FR-18 | SRS.md §FR-18 | — |
| `src/omnibot/knowledge/hybrid_v7.py` | FR-07, FR-19 | SRS.md §FR-07, §FR-19 | — |
| `src/omnibot/escalation/manager_v2.py` | FR-08, FR-20 | SRS.md §FR-08, §FR-20 | NFR-14 |
| `src/omnibot/observability/metrics.py` | FR-22 | SRS.md §FR-22 | NFR-07, NFR-08 |
| `src/omnibot/db/migrations/phase2.py` | FR-12, FR-23 | SRS.md §FR-12, §FR-23 | — |
| `src/omnibot/quality/golden_dataset.py` | FR-24 | SRS.md §FR-24 | NFR-15 |

### Phase 1 Baseline Modules

| Implementation Module | FR(s) Covered | SRS Reference | NFR(s) Covered |
|-----------------------|---------------|---------------|----------------|
| `src/omnibot/adapters/telegram.py` | FR-01, FR-02, FR-03 | SRS.md §FR-01, §FR-02, §FR-03 | NFR-03, NFR-04 |
| `src/omnibot/adapters/line.py` | FR-01, FR-02, FR-03 | SRS.md §FR-01, §FR-02, §FR-03 | NFR-03, NFR-04 |
| `src/omnibot/security/webhook_verifier.py` | FR-02 | SRS.md §FR-02 | NFR-04 |
| `src/omnibot/security/input_sanitizer.py` | FR-04 | SRS.md §FR-04 | — |
| `src/omnibot/security/pii_masking.py` | FR-05 | SRS.md §FR-05 | NFR-06 |
| `src/omnibot/middleware/rate_limiter.py` | FR-06 | SRS.md §FR-06 | — |
| `src/omnibot/knowledge/layer_v1.py` | FR-07 | SRS.md §FR-07 | NFR-01 |
| `src/omnibot/escalation/manager.py` | FR-08 | SRS.md §FR-08 | — |
| `src/omnibot/logging/structured_logger.py` | FR-09 | SRS.md §FR-09 | NFR-05 |
| `src/omnibot/api/schemas/response.py` | FR-10 | SRS.md §FR-10 | — |
| `src/omnibot/api/routes/health.py` | FR-11 | SRS.md §FR-11 | — |
| `src/omnibot/db/schema.sql` | FR-12 | SRS.md §FR-12 | — |
| `src/omnibot/platform/adapter/models.py` | FR-03 | SRS.md §FR-03 | — |
| `docker-compose.yml` | FR-11, FR-13 | SRS.md §FR-11, §FR-13 | — |

---

## Backward Traceability (Test → FR)

### Phase 2 Planned Test Cases

| Test Case (planned) | Covers FR | Verification Method |
|----------------------|-----------|---------------------|
| Messenger webhook: valid HMAC + parse | FR-14, FR-02, FR-03 | P4 integration test |
| Messenger webhook: invalid HMAC → 401 | FR-14, FR-02 | P4 integration test |
| WhatsApp webhook: valid HMAC + parse | FR-14, FR-02, FR-03 | P4 integration test |
| WhatsApp webhook: invalid HMAC → 401 | FR-14, FR-02 | P4 integration test |
| Webhook round-trip E2E (Messenger) | FR-14, FR-02, FR-03, FR-19 | P5 acceptance |
| Webhook round-trip E2E (WhatsApp) | FR-14, FR-02, FR-03, FR-19 | P5 acceptance |
| Prompt injection: all 10 patterns detected | FR-15 | P3 unit test |
| Prompt injection: NFKC normalization before matching | FR-15, FR-04 | P3 unit test |
| Prompt injection: safe input passes | FR-15 | P3 unit test |
| Security block rate >= 95% (100 red-team inputs) | FR-15 | P5 acceptance |
| Sandwich prompt structure validation | FR-15 | P3 unit test |
| PII masking: credit card pattern match | FR-16 | P3 unit test |
| PII masking: Luhn check valid/invalid vectors | FR-16 | P3 unit test |
| PII masking: false positive exclusion (non-Luhn) | FR-16 | P3 unit test |
| PII masking: back-to-front replacement (no index skew) | FR-16, FR-05 | P3 unit test |
| PII masking: mask_count and pii_types in result | FR-16 | P3 unit test |
| Emotion: POSITIVE / NEUTRAL / NEGATIVE classification | FR-17 | P3 unit test |
| Emotion: exponential decay formula correctness | FR-17 | P3 unit test |
| Emotion: weighted score with mixed history | FR-17 | P3 unit test |
| Emotion: consecutive_negative_count edge cases | FR-17 | P3 unit test |
| Emotion: escalation trigger at >= 3 consecutive negative | FR-17 | P4 integration test |
| Emotion: zero history → 0.0 weighted score | FR-17 | P3 unit test |
| DST: all 7 states + valid transitions | FR-18 | P3 unit test |
| DST: invalid transition rejection | FR-18 | P3 unit test |
| DST: slot filling → completion → confirmation | FR-18 | P4 integration test |
| DST: 3+ rounds missing slots → escalate | FR-18 | P4 integration test |
| DST: turn_count increment and last_updated on transition | FR-18 | P3 unit test |
| DST: immutable transition (new object returned) | FR-18 | P3 unit test |
| Knowledge V2: Layer 1 fast-return (confidence > 0.9) | FR-19 | P3 unit test |
| Knowledge V2: Layer 2 RAG embedding + pgvector top-5 | FR-19 | P4 integration test |
| Knowledge V2: RRF fusion (k=60) ordering correctness | FR-19 | P3 unit test |
| Knowledge V2: Layer 3 LLM grounded + sandwich path | FR-19, FR-15, FR-21 | P4 integration test |
| Knowledge V2: Layer 3 LLM fallthrough to Layer 4 | FR-19, FR-21 | P4 integration test |
| Knowledge V2: knowledge_source recorded in messages | FR-19 | P4 integration test |
| Escalation V2: priority → SLA deadline (normal/30, high/15, urgent/5) | FR-20 | P3 unit test |
| Escalation V2: create/assign/resolve lifecycle | FR-20 | P4 integration test |
| Escalation V2: SLA breach query (missed deadlines) | FR-20 | P3 unit test |
| Escalation V2: get_sla_breaches ordering (priority DESC, queued_at ASC) | FR-20 | P3 unit test |
| Grounding: cosine similarity >= 0.75 → grounded | FR-21 | P3 unit test |
| Grounding: cosine similarity < 0.75 → not grounded | FR-21 | P3 unit test |
| Grounding: empty source list → no_source | FR-21 | P3 unit test |
| Grounding: best_match_index correctness | FR-21 | P3 unit test |
| Grounding: ungrounded → Layer 4 escalation | FR-21, FR-19 | P4 integration test |
| Prometheus: all 8 metrics registered | FR-22 | P3 unit test |
| Prometheus: histogram buckets and labels correct | FR-22 | P3 unit test |
| Prometheus: GET /metrics text format valid | FR-22 | P4 integration test |
| Prometheus: counter increment on request / PII mask / escalation | FR-22 | P4 integration test |
| DB Schema: emotion_history table + constraints | FR-23 | P3 migration test |
| DB Schema: edge_cases table + constraints | FR-23 | P3 migration test |
| DB Schema: ivfflat index on knowledge_base | FR-23 | P3 migration test |
| DB Schema: RAG query latency < 200ms (10K scale) | FR-23 | P4 performance test |
| Golden Dataset: insert + annotate 500 edge cases | FR-24 | P3 unit test |
| Golden Dataset: 6 categories each >= 50 records | FR-24 | P3 unit test |
| Golden Dataset: used_in_regression flag set | FR-24 | P3 unit test |
| Golden Dataset: status = approved, annotated_at not null | FR-24 | P3 unit test |

### Phase 1 Baseline Test Cases

| Test Case | Covers FR | Verification Method |
|-----------|-----------|---------------------|
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

---

## NFR Traceability

| NFR | Name | Category | Threshold | Measurement Method | Verification Phase | Status |
|-----|------|----------|-----------|-------------------|-------------------|--------|
| NFR-01 | FCR >= 50% | Performance | >= 50% | ODD SQL query (Phase 1 SPEC) | P3–P5 | COMPLETE |
| NFR-02 | p95 Latency < 3.0s | Performance | < 3.0s | ODD SQL query (Phase 1 SPEC) | P3–P5 | COMPLETE |
| NFR-03 | Platform Support — Telegram + LINE | Compatibility | 2 platforms | Webhook E2E test x2 | P3–P5 | COMPLETE |
| NFR-04 | Webhook Verification 100% | Security | 100% | security_logs counter query | P3–P5 | COMPLETE |
| NFR-05 | JSON Structured Logging | Observability | 100% NDJSON | Log schema validator | P3–P5 | COMPLETE |
| NFR-06 | PII Masking Coverage | Security | Phone/Email/Address | Unit test coverage report | P3–P5 | COMPLETE |
| NFR-07 | FCR >= 80% | Performance | >= 80% (30-day rolling) | ODD SQL: `messages` JOIN `conversations`, 30d window (SPEC L861–L935) | P5 Verification | Not Started |
| NFR-08 | p95 Response Latency < 1.5s | Performance | < 1.5s (per platform) | `omnibot_response_duration_seconds` histogram, per-platform p95 | P5 Verification | Not Started |
| NFR-09 | Platform Support — 4 Platforms | Compatibility | 4 platforms | Webhook E2E test x4 (TG/LINE/MSG/WA) | P5 Verification | Not Started |
| NFR-10 | Webhook Signature Verification — 100% | Security | 100% (all 4 platforms) | security_logs: all inbound requests must have valid HMAC | P5 Verification | Not Started |
| NFR-11 | PII Masking — 100% Coverage Including Luhn | Security | 100% (phone/email/address/credit_card) | Unit test + regex + Luhn vector coverage | P5 Verification | Not Started |
| NFR-12 | Security Block Rate >= 95% | Security | >= 95% (red-team, 100 inputs) | `security_logs` blocked rate: blocked / total >= 0.95 (SPEC L923–L936) | P5 Verification | Not Started |
| NFR-13 | Grounding Check — 100% LLM Output Verification | Reliability | 100% (cosine >= 0.75) | All Layer 3 outputs pass `GroundingChecker.check()` | P5 Verification | Not Started |
| NFR-14 | SLA Compliance >= 90% | Reliability | >= 90% (per priority) | ODD SQL: resolved_before_sla / total_escalated (SPEC L898–L910) | P5 Verification | Not Started |
| NFR-15 | Golden Dataset >= 500 Edge Cases | Quality | >= 500 (6 categories, ≥50 each) | `edge_cases` table count + category distribution | P5 Verification | Not Started |

---

## Acceptance Criteria Traceability

| FR | Key Metric | Threshold | Verification Method |
|----|-----------|-----------|---------------------|
| FR-14 | Messenger + WhatsApp webhook response | < 3.0s | `omnibot_response_duration_seconds` histogram |
| FR-15 | Prompt injection patterns detected | 10 patterns | Unit test: all 10 regex patterns match |
| FR-16 | Luhn check on credit card patterns | 16-digit LUHN validation | Unit test: valid/invalid card vectors |
| FR-17 | Consecutive negative threshold | >= 3 triggers escalation | Unit test + Integration test |
| FR-17 | Emotion decay half-life | 24 hours | Unit test: decay formula correctness |
| FR-18 | DST slot filling max rounds | 3 rounds then escalate | Unit test: state machine transitions |
| FR-19 | RRF k value | 60 | Unit test: RRF formula correctness |
| FR-19 | Layer 1 confidence fast-return | > 0.9 | Unit test: confidence threshold |
| FR-19 | RRF fusion return threshold | > 0.7 | Unit test: fusion rank |
| FR-19 | RAG pgvector query limit | Top-5 | Unit test + Performance test |
| FR-21 | Grounding cosine similarity threshold | >= 0.75 | Unit test: cosine similarity vectors |
| FR-22 | Prometheus histogram buckets | 7 buckets (0.1–5.0s) | Unit test: metric registration |
| FR-23 | ivfflat lists | 100 | Migration test: index verification |
| FR-24 | Golden dataset target | >= 500 edge cases | Unit test: record count + categories |
| NFR-07 | FCR (30-day rolling) | >= 80% | ODD SQL (SPEC L861–L935) |
| NFR-08 | p95 latency | < 1.5s | Prometheus histogram p95 query |
| NFR-09 | Platform support | 4 platforms | Webhook E2E x4 |
| NFR-10 | Webhook verification | 100% | security_logs audit |
| NFR-11 | PII masking coverage | 100% (含 Luhn) | regex + Luhn vector coverage report |
| NFR-12 | Security block rate | >= 95% | Red-team test (100 inputs) |
| NFR-13 | Grounding coverage | 100% of LLM outputs | GroundingChecker pass/fail audit |
| NFR-14 | SLA compliance | >= 90% | ODD SQL (SPEC L898–L910) |
| NFR-15 | Golden dataset size | >= 500 | edge_cases table COUNT |

---

## Coverage Summary

| Metric | Count | Coverage |
|--------|-------|----------|
| Total FRs (Phase 1 + 2) | 24 | 100% traced |
| Phase 1 FRs (COMPLETE, verified) | 13 | 100% |
| Phase 2 FRs (DRAFT) | 11 | 100% planned |
| FRs with spec source reference | 24 | 100% |
| FRs with implementation module | 24 | 100% |
| FRs with test module | 24 | 100% |
| Test cases — Phase 1 | 16 | ≥1 per FR |
| Test cases — Phase 2 (planned) | 55 | ≥3 per FR |
| NFRs total | 15 | 100% with measurement method |
| NFRs with verification phase | 15 | 100% |
| Implementation modules (Phase 1) | 14 | All traced to FR |
| Implementation modules (Phase 2 planned) | 14 | All traced to FR |
| Orphan FRs | 0 | All FRs traced forward + backward |
| Orphan modules | 0 | All modules traced back to FR |
| Orphan tests | 0 | All tests trace to ≥1 FR |

---

## Security Architecture Traceability

All implementation modules require: TLS encryption for webhook endpoints, HMAC-SHA256 signature verification and auth token validation, PII masking with permission-based access control, and vulnerability scanning integration. RBAC authorization model deferred to Phase 3.

---

*TRACEABILITY_MATRIX.md v2.0 — forward and backward traceability for Phase 1 baseline + Phase 2 planned scope*
