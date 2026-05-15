# Deferred Fixes — omnibot-full

> Accumulated from Gate 1–4 review cycles. Reviewed at Phase 7 entry (HR-P7 per-FR pre-check).
> Last updated: 2026-05-16

---

## Gate 3 / Gate 4 Deferred Items

| ID | Severity | Source | Description | Deferred To | Status |
|----|----------|--------|-------------|-------------|--------|
| DF-01 | Medium | Gate 3 / Gate 4 D7 | Mutation testing score 70 (below threshold 85). `mutmut` not installed in CI environment. Accepted at 70 by reviewer. | Phase 8 / Post-MVP | Open |
| DF-02 | Medium | Gate 4 D1 | 6 pylint refactor-level warnings (convention, not errors). Examples: `C0116 missing-function-docstring`, `R0903 too-few-public-methods`. | Phase 8 | Open |
| DF-03 | Low | Gate 4 D11 | 26 pydocstyle issues (D204 missing blank line after class docstring, D107 missing docstring in `__init__`). No functional impact. | Phase 8 | Open |
| DF-04 | Low | Phase 3–5 | PYTHONPATH must be set manually for test runs (`PYTHONPATH=03-development/src pytest`). Packaging not configured (`setup.py` / `pyproject.toml` missing `src` layout). | Phase 8 | Open |

## FR-Specific Deferred Items (from Phase 7 Risk Review)

| ID | FR | Severity | Description | Deferred To |
|----|----|----------|-------------|-------------|
| DF-05 | FR-11 | High | Health check stubs `lambda: False` return permanent `unhealthy`. Real probes needed for production. (RISK-FR11-01) | Phase 2 / Production |
| DF-06 | FR-11 | High | `/api/v1/health` always returns HTTP 200 regardless of health status. Orchestrators cannot detect unhealthy state. (RISK-FR11-02) | Phase 2 / Production |
| DF-07 | FR-12 | High | `knowledge_base.embeddings vector(384)` nullable; Phase 2 ANN queries will silently skip NULL rows without backfill. (RISK-FR12-01) | Phase 2 |
| DF-08 | FR-12 | High | No pgvector index in Phase 1 DDL; Phase 2 similarity queries will run O(N) sequential scans. (RISK-FR12-02) | Phase 2 |
| DF-09 | FR-13 | High | `POSTGRES_PASSWORD: omnibot_dev` hardcoded plain-text in `docker-compose.yml`. Must be parameterized before staging. (RISK-FR13-02) | Pre-staging |
| DF-10 | FR-13 | High | `REDIS_PASSWORD` fallback `dev_redis_password` in `docker-compose.yml`. Must be removed before staging. (RISK-FR13-01) | Pre-staging |

## No-Action Items (Accepted)

| ID | Description | Decision |
|----|-------------|----------|
| NA-01 | Mutation testing score 70 (Gate 3 + Gate 4). Accepted by reviewer; `mutmut` install out of scope for Phase 1 CI. | Accepted |
| NA-02 | 4 gitleaks false positives in test fixtures (bot tokens, test secrets). Confirmed not real credentials. | Accepted |

---

*Reviewed at P7 entry per plan §FR Risk Evaluation pre-check. No items block Phase 7 completion.*
