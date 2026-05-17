# Test Plan — Phase 3 (24 FRs)

> Generated: 2026-05-17 | Phase: 3 (Implementation Complete)

## Scope
All 24 FRs (FR-01–FR-24) covering platform adapters, security layers, knowledge layers, dialogue state, escalation, observability, and golden dataset. 390 tests total.

## Test Strategy
- **Unit tests**: pytest with async support, frozen dataclass invariants, regex pattern validation
- **Security tests**: HMAC-SHA256 signature verification, prompt injection (100 adversarial inputs), Luhn credit card validation, grounding cosine similarity
- **Integration tests**: asyncpg MockPool/MockConnection for DB operations, FastAPI TestClient for HTTP endpoints
- **Regression tests**: Golden dataset (510 edge cases, 6 categories)
- **Performance tests**: Token bucket rate limiter latency, RAG query benchmarks, p95 latency targets

## FR Coverage

| FR | Module | Test File | Tests |
|----|--------|-----------|-------|
| FR-01 | Platform Adapter Telegram LINE | test_fr01.py | 8 |
| FR-02 | Webhook Signature Verification | test_fr02.py | 8 |
| FR-03 | Unified Message Format | test_fr03.py | 10 |
| FR-04 | Input Sanitizer L2 | test_fr04.py | 11 |
| FR-05 | PII Masking L4 | test_fr05.py | 10 |
| FR-06 | Rate Limiter Token Bucket | test_fr06.py | 5 |
| FR-07 | Knowledge Layer V1 | test_fr07.py | 6 |
| FR-08 | Basic Escalation Manager | test_fr08.py | 10 |
| FR-09 | Structured Logger | test_fr09.py | 12 |
| FR-10 | API Response Format | test_fr10.py | 13 |
| FR-11 | Health Check Endpoint | test_fr11.py | 9 |
| FR-12 | Database Schema Phase 1 | test_fr12.py | 13 |
| FR-13 | Docker Compose Environment | test_fr13.py | 12 |
| FR-14 | Messenger WhatsApp Adapters | test_fr14.py | 15 |
| FR-15 | Prompt Injection Defense L3 | test_fr15.py | 25 |
| FR-16 | PII Masking V2 Credit Card Luhn | test_fr16.py | 18 |
| FR-17 | Emotion Analyzer | test_fr17.py | 30 |
| FR-18 | DST 7-State FSM | test_fr18.py | 35 |
| FR-19 | HybridKnowledgeV2 Four-Layer | test_fr19.py | 55 |
| FR-20 | Escalation V2 SLA Priorities | test_fr20.py | 28 |
| FR-21 | Grounding Checks L5 | test_fr21.py | 15 |
| FR-22 | Prometheus Metrics | test_fr22.py | 20 |
| FR-23 | DB Schema Phase 2 | test_fr23.py | 12 |
| FR-24 | Golden Dataset | test_fr24.py | 20 |

## Acceptance Criteria
Each FR has documented AC mapped to test cases in test files.
Security NFRs verified via red-team tests (NFR-12 ≥95% block rate with 100 inputs).

## Architecture Constraints Verified
- No synchronous ORM in request path
- No circular dependencies
- All messages immutable (frozen dataclass)
- Webhook signature verification before business logic
- Single PostgreSQL 16 + pgvector
- Python 3.11+, stdlib-first dependency policy
