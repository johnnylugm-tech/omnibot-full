# Technical Constraints — OmniBot Phase 1

> **Project**: OmniBot — 多平台客服機器人
> **Phase**: 1 (MVP 基礎)
> **Version**: 1.0
> **Date**: 2026-05-13
> **Depends on**: SRS.md v1.0

---

## 1. Technology Stack

| Layer | Technology | Version | Constraint |
|-------|-----------|---------|------------|
| Language | Python | 3.11+ | asyncio-based; no synchronous ORM in request path |
| Web framework | FastAPI | >=0.110 | async handlers; Pydantic v2 for validation |
| Database | PostgreSQL + pgvector | 16 (pgvector/pg16) | pgvector extension required for Phase 2 embeddings |
| Cache / rate-limit | Redis | 7-alpine | password-protected; used for token bucket state |
| Container runtime | Docker Compose | v2 | single-node dev; Phase 3 considers k8s |
| LLM gateway | Anthropic SDK | — | Phase 2 onward; Phase 1 gate eval uses Claude via SSI |
| Logging | stdlib `logging` | — | JSON NDJSON to stdout; no external log aggregator in Phase 1 |
| CI | GitHub Actions | — | `harness_quality_gate.yml` via `harness-init.sh` |

### Technology Decisions (ADR)

| Decision | Rationale | Trade-off |
|----------|-----------|-----------|
| FastAPI over Flask | Native async, Pydantic validation, OpenAPI auto-gen | Heavier dependency tree |
| pgvector over Pinecone/Weaviate | Single DB for rules + vectors; no external vector service in Phase 1 | Vector perf limited to single node |
| Redis for rate-limiting over in-memory dict | Survives restarts; shared across workers | Adds infrastructure dependency |
| Frozen dataclasses for messages | Thread-safe, hashable, no accidental mutation | Slight verbosity |

---

## 2. SLA Targets

| Metric | Target | Measurement Window | Enforcement |
|--------|--------|--------------------|-------------|
| FCR (First Contact Resolution) | >= 50% | 30-day rolling | ODD SQL query; non-blocking in Phase 1 |
| p95 Response Latency | < 3.0s | Per-deploy | ODD SQL query; alert if degraded |
| Uptime | Best-effort (no SLA) | — | Health check endpoint only; no HA in Phase 1 |
| Escalation response | No SLA | — | Phase 2 adds `sla_deadline` to `escalation_queue` |
| Webhook verification rate | 100% | Per-request | Every unverified request = 401 response; audit via `security_logs` |

> **Phase 2**: SLA targets become contractually binding with alerting. Phase 3 adds cost-per-resolution tracking.

---

## 3. Cost Model

### Phase 1 (MVP)

| Resource | Estimated Monthly Cost | Notes |
|----------|------------------------|-------|
| Compute (single VPS, 2 vCPU / 4 GB) | ~$40 | Covers API + background workers |
| PostgreSQL (managed, 10 GB) | ~$20 | Or self-hosted on same VPS |
| Redis (managed, 1 GB) | ~$10 | Or self-hosted on same VPS |
| Anthropic API (gate eval only) | ~$5 | SSI gate scoring; not per-user-request |
| **Total** | **~$75/mo** | Self-hosting PG + Redis on VPS drops to ~$40 |

### Phase 2+ Projections

- LLM per-request cost: $0.002–0.01/query (Claude Haiku)
- Vector DB scaling: pgvector stays within single-node limits for < 1M vectors
- Multi-AZ: +$40/mo for managed PG HA

---

## 4. Security Constraints

| Constraint | Scope | Implementation |
|------------|-------|----------------|
| Webhook signatures | All incoming webhooks | HMAC-SHA256 per platform; `hmac.compare_digest()` |
| PII masking | Phone / Email / Address (Taiwan) | Regex-based; mask before storage or log output |
| Input sanitization | All user text | NFKC normalization + control character removal |
| Secret storage | Bot tokens, channel secrets, DB passwords | Environment variables; never in source |
| Rate limiting | Per-platform per-user | Token bucket; default 100 rps |
| No RBAC in Phase 1 | Admin API endpoints | Phase 3 adds JWT + role-based access |

---

## 5. Regulatory & Compliance

| Requirement | Applicability | Phase 1 Stance |
|-------------|---------------|----------------|
| Taiwan Personal Data Protection Act (PDPA) | User PII (phone, email, address) | PII masking L4 in place; no persistent PII storage in logs |
| Data localization | All user data | PostgreSQL in chosen region; no cross-border transfer in MVP |
| Audit trail | Security events | `security_logs` table captures layer, blocked status, source IP |
| GDPR | Not in scope (Taiwan-only Phase 1) | Phase 3 if EU users are onboarded |

---

## 6. Development Constraints

| Constraint | Value |
|------------|-------|
| Timeline | 3–4 weeks (Phase 1) |
| Team | AI-assisted solo developer (Claude orchestrator + A/B agents) |
| Methodology | harness-methodology v2.3.0; SKILL.md governs; HR-01–HR-15 enforced |
| External frameworks | Forbidden per HR-06 unless specified in SAD.md |
| Code quality | Constitution v2.3; 12-dimension quality charter (full enforcement P3+) |
| Language | Python only for backend; SQL for schema; bash for scripts |

---

## 7. Constraints Inherited from SRS Gaps

The following non-blocking gaps from Sub-Task 1/4 Agent B review are acknowledged and deferred:

| Gap ID | Area | Disposition |
|--------|------|-------------|
| GAP-01 | NFR-04 measurement | `security_logs` counters added to FR-12 acceptance criteria |
| GAP-02 | FR-07 tie-breaking | Tie-breaker rule deferred to Phase 3 implementation detail |
| GAP-03 | FR-05 PII precedence | Email → phone → address precedence adopted |
| GAP-04 | Cross-platform identity | Explicitly out-of-scope for Phase 1; Phase 2 consideration |
| GAP-05 | Security events logging | Security event logging FR added to Phase 1 scope |

---

*CONSTRAINTS.md v1.0 — derived from SRS.md v1.0 and SPEC/omnibot-phase-1.md v7.0*
