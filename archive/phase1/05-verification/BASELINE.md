# System Baseline — OmniBot Phase 1 MVP

> **Version**: 1.0
> **Date**: 2026-05-14
> **Phase**: 5 (Verification & Delivery)
> **Gate 3 Score**: 91.15

---

## 1. Functional Requirements Status

| FR | Title | Status | Gate 1 (P5) | Tests |
|----|-------|--------|-------------|-------|
| FR-01 | Platform Adapter (Telegram+LINE) | PASS | 95.3 | 8/8 |
| FR-02 | Webhook Signature Verification | PASS | 95.3 | 8/8 |
| FR-03 | Unified Message Format | PASS | 96.3 | 10/10 |
| FR-04 | Input Sanitizer L2 | PASS | 96.3 | 11/11 |
| FR-05 | PII Masking L4 | PASS | 95.3 | 10/10 |
| FR-06 | Rate Limiter (Token Bucket) | PASS | 93.7 | 5/5 |
| FR-07 | Knowledge Layer V1 | PASS | 93.0 | 6/6 |
| FR-08 | Escalation Manager | PASS | 96.0 | 10/10 |
| FR-09 | Structured Logger | PASS | 96.3 | 12/12 |
| FR-10 | API Response Format | PASS | 97.0 | 13/13 |
| FR-11 | Health Check Endpoint | PASS | 96.0 | 9/9 |
| FR-12 | Database Schema | PASS | 95.3 | 13/13 |
| FR-13 | Docker Compose Dev Env | PASS | 94.7 | 12/12 |

**Total**: 13/13 FRs PASS, 126/126 tests PASS

## 2. Architecture Summary

- **Framework**: FastAPI + Python 3.11
- **Database**: PostgreSQL 16 (pgvector) + Redis 7
- **Deployment**: Docker Compose (3 services)
- **Security**: HMAC-SHA256 signature verification (Telegram + LINE)
- **PII**: Regex-based phone/email/address masking with escalation keywords
- **Rate Limiting**: Per-user token bucket (default 100 rps)
- **Logging**: NDJSON structured stdout logger

## 3. NFR Compliance

| NFR | Target | Status |
|-----|--------|--------|
| NFR-01 | FCR >= 50% | Deferred (Phase 2 measurement) |
| NFR-02 | p95 latency < 3.0s | PASS (webhook < 3s verified) |
| NFR-03 | Telegram + LINE support | PASS |
| NFR-04 | 100% webhook verification | PASS |
| NFR-05 | JSON structured logging | PASS |
| NFR-06 | PII masking coverage | PASS |

## 4. Known Gaps (Phase 2 Deferred)

- FR-07: In-memory prototype → SQL ILIKE/ANY migration
- FR-07: is_active filter, version ordering
- FR-08: SLA tracking (sla_deadline)
- RAG vector search, LLM generation, DST state machine
- Messenger/WhatsApp adapters

## 5. Artifact Inventory

| Artifact | Path |
|----------|------|
| SRS | 01-requirements/SRS.md |
| SAD | 02-design/SAD.md |
| Source | 03-development/src/omnibot/ |
| Tests | tests/test_fr01.py - test_fr13.py |
| Test Plan | 04-testing/TEST_PLAN.md |
| Test Results | 04-testing/TEST_RESULTS.md |
| Compliance Matrix | 03-development/COMPLIANCE_MATRIX.md |
| Docker Compose | docker-compose.yml |
| Schema DDL | 03-development/src/omnibot/schema/__init__.py |

---

*BASELINE.md v1.0 — generated Phase 5 verification*
