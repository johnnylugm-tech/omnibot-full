# Specification Tracking Matrix — OmniBot

> **Project**: OmniBot — 多平台客服機器人
> **Phase**: 1 (Requirements Specification)
> **Version**: 1.0
> **Date**: 2026-05-13
> **Depends on**: SRS.md v1.0

---

## FR Status Tracking

| FR-ID | Name | Priority | Status | Owner | Acceptance Verified | Notes |
|-------|------|----------|--------|-------|--------------------|-------|
| FR-01 | Platform Adapter — Telegram + LINE Webhook | P0 | specified | REQUIREMENTS_ENGINEER | pending (P5) | P3 impl, P5 acceptance |
| FR-02 | Webhook Signature Verification | P0 | specified | REQUIREMENTS_ENGINEER | pending (P5) | P3 impl, P5 acceptance |
| FR-03 | Unified Message Format | P0 | specified | REQUIREMENTS_ENGINEER | pending (P5) | P3 impl, P5 acceptance |
| FR-04 | Input Sanitizer L2 — Character Normalization | P1 | specified | REQUIREMENTS_ENGINEER | pending (P5) | P3 impl, P5 acceptance |
| FR-05 | PII Masking L4 — Phone / Email / Address | P1 | specified | REQUIREMENTS_ENGINEER | pending (P5) | P3 impl, P5 acceptance |
| FR-06 | Rate Limiter — Token Bucket | P1 | specified | REQUIREMENTS_ENGINEER | pending (P5) | P3 impl, P5 acceptance |
| FR-07 | Knowledge Layer V1 — Rule Match + Escalate | P0 | specified | REQUIREMENTS_ENGINEER | pending (P5) | P3 impl, P5 acceptance |
| FR-08 | Basic Escalation Manager — No SLA | P1 | specified | REQUIREMENTS_ENGINEER | pending (P5) | P3 impl, P5 acceptance |
| FR-09 | Structured Logger — JSON Format | P1 | specified | REQUIREMENTS_ENGINEER | pending (P5) | P3 impl, P5 acceptance |
| FR-10 | API Response Format — ApiResponse / PaginatedResponse | P1 | specified | REQUIREMENTS_ENGINEER | pending (P5) | P3 impl, P5 acceptance |
| FR-11 | Health Check Endpoint | P1 | specified | REQUIREMENTS_ENGINEER | pending (P5) | P3 impl, P5 acceptance |
| FR-12 | Database Schema — All Core Tables | P0 | specified | REQUIREMENTS_ENGINEER | pending (P5) | P3 impl, P5 acceptance |
| FR-13 | Docker Compose Development Environment | P2 | specified | REQUIREMENTS_ENGINEER | pending (P5) | P3 impl, P5 acceptance |

## NFR Status Tracking

| NFR-ID | Name | Category | Status | Measurement | Verified |
|--------|------|----------|--------|-------------|----------|
| NFR-01 | First Contact Resolution (FCR) >= 50% | Performance | specified | ODD SQL (30-day rolling) | pending (P3–P5) |
| NFR-02 | p95 Response Latency < 3.0s | Performance | specified | ODD SQL (per-platform) | pending (P3–P5) |
| NFR-03 | Platform Support — Telegram + LINE | Compatibility | specified | Functional test | pending (P3–P5) |
| NFR-04 | Webhook Verification 100% | Security | specified | security_logs audit | pending (P3–P5) |
| NFR-05 | JSON Structured Logging | Observability | specified | Log inspection | pending (P3–P5) |
| NFR-06 | PII Masking Coverage | Security | specified | Unit test | pending (P3–P5) |

## FR → Phase Mapping

| Phase | FRs Covered | Gate |
|-------|-------------|------|
| P1 (Requirements) | FR-01 – FR-13 (specified) | Human peer review |
| P2 (Architecture) | All FRs → SAD.md design | Human peer review |
| P3 (Implementation) | All FRs → code + unit tests | Gate 1 (per-FR) + Gate 2 (exit, ≥75) |
| P4 (Testing) | All FRs → test plan + results | Gate 1 (per-FR) + Gate 3 (exit, ≥80) |
| P5 (Verification) | All FRs → acceptance verification | Gate 1 (per-FR); Phase Truth ≥90% |
| P6 (QA) | Full project audit | Gate 4 (exit, ≥85) |

## Review Gap Register

Carried forward from A/B reviews; all non-blocking.

| Gap ID | Source | Area | Disposition | Target Phase |
|--------|--------|------|-------------|-------------|
| GAP-01 | B-1/4 | NFR-04 measurement | security_logs counters in FR-12 AC | P3 |
| GAP-02 | B-1/4 | FR-07 tie-breaking | Deferred to implementation detail | P3 |
| GAP-03 | B-1/4 | FR-05 PII precedence | email→phone→address adopted | P3 |
| GAP-04 | B-1/4 | Cross-platform identity | Out-of-scope; Phase 2 | P2 |
| GAP-05 | B-1/4 | Security event logging FR | Added to scope | P3 |
| M-GAP-01 | B-2/4 | Cost model API $5 ambiguous | Clarify budget line item | P1 (next revision) |
| M-GAP-02 | B-2/4 | Self-hosting breakdown vague | Detail PG/Redis cost split | P1 (next revision) |
| M-GAP-03 | B-2/4 | NFR-03 traceability in tech stack | Confirm Python/FastAPI platform capability | P1 (next revision) |

---

*SPEC_TRACKING.md v1.0 — derived from SRS.md v1.0 and A/B review outputs*
