# Specification Tracking Matrix — OmniBot Phase 2

> **Project**: OmniBot — Multi-Platform Customer Service Bot
> **Phase**: 2 (Smart + Security Enhancement)
> **Version**: 2.0
> **Date**: 2026-05-16
> **References**: 01-requirements/SRS.md v2.0, SPEC/omnibot-phase-2.md v7.0

---

## FR Status Summary

| FR | Name | Priority | Status | Owner | Acceptance State | Notes |
|----|------|----------|--------|-------|-----------------|-------|
| FR-01 | Platform Adapter — Telegram + LINE Webhook | P0 | COMPLETE | REQUIREMENTS_ENGINEER | Verified | Phase 1 baseline |
| FR-02 | Webhook Signature Verification | P0 | COMPLETE | REQUIREMENTS_ENGINEER | Verified | Phase 1 baseline |
| FR-03 | Unified Message Format | P0 | COMPLETE | REQUIREMENTS_ENGINEER | Verified | Phase 1 baseline |
| FR-04 | Input Sanitizer L2 — Character Normalization | P1 | COMPLETE | REQUIREMENTS_ENGINEER | Verified | Phase 1 baseline |
| FR-05 | PII Masking L4 — Phone / Email / Address | P1 | COMPLETE | REQUIREMENTS_ENGINEER | Verified | Phase 1 baseline |
| FR-06 | Rate Limiter — Token Bucket | P1 | COMPLETE | REQUIREMENTS_ENGINEER | Verified | Phase 1 baseline |
| FR-07 | Knowledge Layer V1 — Rule Match + Escalate | P0 | COMPLETE | REQUIREMENTS_ENGINEER | Verified | Phase 1 baseline |
| FR-08 | Basic Escalation Manager — No SLA | P1 | COMPLETE | REQUIREMENTS_ENGINEER | Verified | Phase 1 baseline |
| FR-09 | Structured Logger — JSON Format | P1 | COMPLETE | REQUIREMENTS_ENGINEER | Verified | Phase 1 baseline |
| FR-10 | API Response Format — ApiResponse / PaginatedResponse | P1 | COMPLETE | REQUIREMENTS_ENGINEER | Verified | Phase 1 baseline |
| FR-11 | Health Check Endpoint | P1 | COMPLETE | REQUIREMENTS_ENGINEER | Verified | Phase 1 baseline |
| FR-12 | Database Schema — All Core Tables | P0 | COMPLETE | REQUIREMENTS_ENGINEER | Verified | Phase 1 baseline |
| FR-13 | Docker Compose Development Environment | P2 | COMPLETE | REQUIREMENTS_ENGINEER | Verified | Phase 1 baseline |
| FR-14 | Platform Adapter — Messenger + WhatsApp Webhook | P0 | DRAFT | — | Not Started | Phase 2 new |
| FR-15 | Prompt Injection Defense L3 — Sandwich Defense | P0 | DRAFT | — | Not Started | Phase 2 new |
| FR-16 | PII Masking V2 — Credit Card + Luhn Check | P1 | DRAFT | — | Not Started | Phase 2 new |
| FR-17 | Emotion Analyzer — Sentiment Classification + Decay | P1 | DRAFT | — | Not Started | Phase 2 new |
| FR-18 | Intent Router + Dialogue State Tracker (DST) | P0 | DRAFT | — | Not Started | Phase 2 new |
| FR-19 | Hybrid Knowledge Layer V2 — Four-Layer Architecture | P0 | DRAFT | — | Not Started | Phase 2 new |
| FR-20 | Escalation Manager V2 — SLA Priority Levels | P1 | DRAFT | — | Not Started | Phase 2 new |
| FR-21 | Grounding Checks L5 — Semantic Alignment Verification | P1 | DRAFT | — | Not Started | Phase 2 new |
| FR-22 | Prometheus Metrics — Core Instrumentation | P1 | DRAFT | — | Not Started | Phase 2 new |
| FR-23 | Database Schema — Phase 2 Incremental Tables + Index | P1 | DRAFT | — | Not Started | Phase 2 new |
| FR-24 | Golden Dataset — Edge Case Collection + Regression Baseline | P2 | DRAFT | — | Not Started | Phase 2 new |

## NFR Status Summary

| NFR | Name | Category | Threshold | Status | Verified |
|-----|------|----------|-----------|--------|----------|
| NFR-01 | First Contact Resolution (FCR) | Performance | >= 50% | COMPLETE | Verified |
| NFR-02 | p95 Response Latency | Performance | < 3.0s | COMPLETE | Verified |
| NFR-03 | Platform Support — Telegram + LINE | Compatibility | 2 platforms | COMPLETE | Verified |
| NFR-04 | Webhook Verification 100% | Security | 100% | COMPLETE | Verified |
| NFR-05 | JSON Structured Logging | Observability | 100% NDJSON | COMPLETE | Verified |
| NFR-06 | PII Masking Coverage | Security | Phone/Email/Address | COMPLETE | Verified |
| NFR-07 | First Contact Resolution (FCR) >= 80% | Performance | >= 80% (30-day rolling) | DRAFT | Not Started |
| NFR-08 | p95 Response Latency < 1.5s | Performance | < 1.5s (per platform) | DRAFT | Not Started |
| NFR-09 | Platform Support — 4 Platforms | Compatibility | 4 platforms | DRAFT | Not Started |
| NFR-10 | Webhook Signature Verification — 100% Coverage | Security | 100% (all 4 platforms) | DRAFT | Not Started |
| NFR-11 | PII Masking 100% Coverage Including Luhn | Security | 100% (含 credit card) | DRAFT | Not Started |
| NFR-12 | Security Block Rate >= 95% | Security | >= 95% (red-team) | DRAFT | Not Started |
| NFR-13 | Grounding Check — 100% LLM Output Verification | Reliability | 100% (cosine >= 0.75) | DRAFT | Not Started |
| NFR-14 | SLA Compliance >= 90% | Reliability | >= 90% (per priority) | DRAFT | Not Started |
| NFR-15 | Golden Dataset >= 500 Edge Cases | Quality | >= 500 (6 categories) | DRAFT | Not Started |

## Acceptance Criteria Summary

| FR | Key Metric | Threshold |
|----|-----------|-----------|
| FR-14 | Messenger + WhatsApp webhook response | < 3.0s |
| FR-15 | Prompt injection patterns detected | 10 patterns |
| FR-17 | Consecutive negative threshold | >= 3 triggers escalation |
| FR-17 | Emotion decay half-life | 24 hours |
| FR-18 | DST slot filling max rounds | 3 rounds then escalate |
| FR-19 | RRF k value | 60 |
| FR-19 | Layer 1 confidence fast-return | > 0.9 |
| FR-19 | RRF fusion return threshold | > 0.7 |
| FR-19 | RAG pgvector query limit | Top-5 |
| FR-21 | Grounding cosine similarity threshold | >= 0.75 |
| FR-22 | Prometheus histogram buckets | 7 buckets (0.1–5.0s) |
| FR-23 | ivfflat lists | 100 |
| FR-24 | Golden dataset target | >= 500 edge cases |
| NFR-07 | FCR (30-day rolling) | >= 80% |
| NFR-08 | p95 latency | < 1.5s |
| NFR-09 | Platform support | 4 platforms |
| NFR-10 | Webhook verification | 100% |
| NFR-11 | PII masking coverage | 100% (含 Luhn) |
| NFR-12 | Security block rate | >= 95% |
| NFR-13 | Grounding coverage | 100% of LLM outputs |
| NFR-14 | SLA compliance | >= 90% |
| NFR-15 | Golden dataset size | >= 500 |

---

## Security Compliance Reference

All FRs require TLS encryption for endpoints, HMAC-SHA256 signature verification and validation, auth token-based platform verification, PII masking with permission-aware access, and vulnerability scanning. RBAC deferred to Phase 3.

---

*SPEC_TRACKING.md v2.0 — derived from SRS.md v2.0 and SPEC/omnibot-phase-2.md v7.0*
