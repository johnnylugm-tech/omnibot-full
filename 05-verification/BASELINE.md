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
- HMAC-SHA256: Telegram, LINE, Messenger, WhatsApp
- PII masking: Phone, email, address, credit card (Luhn)
- Prompt injection defense: 10 patterns, sandwich defense, NFKC normalization
- Grounding checks: cosine similarity ≥0.75 for all LLM outputs

## Quality Baseline
- 390 tests, 98.39% line coverage
- Gate 1 PASS all 24 FRs (93.0–100.0)
- Golden dataset: 510 edge cases, 6 categories
- FCR target ≥80% (NFR-07), SLA compliance ≥90% (NFR-14)
