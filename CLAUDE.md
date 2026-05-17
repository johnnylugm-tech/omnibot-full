# Project: OmniBot — 多平台客服機器人

## Methodology Handoff
- Framework: harness-methodology v1.0
- Quality Manifest: .methodology/quality_manifest.json
- Active Phase: P3 (Implementation)
- Last Gate: Gate 4 (Score: 96.33)
- Hermes Reviewer Target: ${HERMES_REVIEWER_TARGET}

## FR Registry
| FR ID | Description | Status | Gate 1 |
|-------|-------------|--------|--------|
| FR-01 | Platform Adapter — Telegram + LINE | COMPLETE | 94.67 |
| FR-02 | Webhook Signature Verification | COMPLETE | 94.67 |
| FR-03 | Unified Message Format | COMPLETE | 94.67 |
| FR-04 | Input Sanitizer L2 | COMPLETE | 94.67 |
| FR-05 | PII Masking L4 | COMPLETE | 94.67 |
| FR-06 | Rate Limiter — Token Bucket | COMPLETE | 94.67 |
| FR-07 | Knowledge Layer V1 — Rule Match | COMPLETE | 94.67 |
| FR-08 | Basic Escalation Manager | COMPLETE | 94.67 |
| FR-09 | Structured Logger | COMPLETE | 94.67 |
| FR-10 | API Response Format | COMPLETE | 94.67 |
| FR-11 | Health Check Endpoint | COMPLETE | 94.67 |
| FR-12 | Database Schema — Phase 1 | COMPLETE | 94.67 |
| FR-13 | Docker Compose Environment | COMPLETE | 94.67 |
| FR-14 | Messenger + WhatsApp Adapters | DESIGNED | — |
| FR-15 | Prompt Injection Defense L3 | DESIGNED | — |
| FR-16 | PII Masking V2 — Credit Card + Luhn | DESIGNED | — |
| FR-17 | Emotion Analyzer | DESIGNED | — |
| FR-18 | DST — 7-State FSM | DESIGNED | — |
| FR-19 | HybridKnowledgeV2 — Four-Layer | DESIGNED | — |
| FR-20 | Escalation V2 — SLA Priorities | DESIGNED | — |
| FR-21 | Grounding Checks L5 | DESIGNED | — |
| FR-22 | Prometheus Metrics | DESIGNED | — |
| FR-23 | DB Schema — Phase 2 Incremental | DESIGNED | — |
| FR-24 | Golden Dataset | DESIGNED | — |

## Architecture Constraints
- No synchronous ORM in request path
- No circular dependencies between modules
- All messages must be immutable (frozen dataclass)
- Webhook signature verification before business logic
- Single PostgreSQL 16 + pgvector database (no external vector DB)
- Python 3.11+, stdlib-first dependency policy

## High-Risk Modules
- PromptInjectionDefense (security boundary, NFR-12 ≥95% block rate)
- PIIMaskingV2 (data privacy, Luhn validation correctness)
- GroundingChecker (LLM output hallucination prevention)
- HybridKnowledgeV2 (core business logic, 4-layer orchestration)
- EscalationManagerV2 (SLA compliance NFR-14 ≥90%)
- DialogueStateTracker (7-state FSM correctness, slot filling limits)

## Open Issues (Top Priority)
- Implementation of Phase 2 FRs (FR-14 to FR-24) — architecture designed, code pending
- Implementation of Phase 3 FRs (RBAC, cost tracking, OpenTelemetry, K8s) — pending Phase 3 plan

## NFR → Dimension Mapping
| NFR | Dimension | Target |
|-----|-----------|--------|
| NFR-01 | effectiveness | FCR ≥ 50% (Phase 1 baseline) |
| NFR-07 | effectiveness | FCR ≥ 80% (Phase 2 target) |
| NFR-08 | performance | p95 latency < 1.5s |
| NFR-09 | compatibility | 4 platforms |
| NFR-10 | security | 100% webhook verification |
| NFR-11 | security | 100% PII masking coverage including Luhn |
| NFR-12 | security | ≥95% injection block rate |
| NFR-13 | correctness | 100% LLM output grounding verification |
| NFR-14 | reliability | SLA compliance ≥90% |
| NFR-15 | testability | ≥500 golden dataset edge cases |

## Agent Interaction Model
```
Johnny: "執行 Phase N"
  → Agent: plan-phase N       (generates Plan_Phase_N.md)
  → Johnny: reviews plan
  → Agent: run-phase N        (executes plan)
  → POST-FLIGHT: gate check + Hermes reviewer
```

## Gate Status
| Gate | Trigger | Score | Status |
|------|---------|-------|--------|
| Gate 1 | P3/P5/P7/P8 per-FR | — | PENDING |
| Gate 2 | P3 exit | — | PENDING |
| Gate 3 | P4 exit | 91.15 | PASSED |
| Gate 4 | P6 full | 96.33 | PASSED |
