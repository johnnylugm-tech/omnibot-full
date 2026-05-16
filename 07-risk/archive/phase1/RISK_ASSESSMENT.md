# RISK_ASSESSMENT.md — omnibot-full

> **Phase**: 7 — Risk Management
> **Framework**: harness-methodology v2.3.0
> **Date**: 2026-05-16
> **Scope**: FR-01 through FR-13 (Phase 1 MVP)

---

## Executive Summary

| Metric | Value |
|--------|-------|
| FRs assessed | 13 / 13 |
| Total risks identified | 52 |
| HIGH risks (score ≥ 10) | 21 |
| MEDIUM risks (score 6–9) | 28 |
| LOW risks (score ≤ 5) | 3 |
| Critical risks | 0 |
| Risks with mitigation | 52 / 52 (100%) |
| A/B review APPROVE | 13 / 13 |

All HIGH risks have documented mitigations with file-level citations (HR-15).

---

## Risk Distribution by FR

| FR | Description | Risks | HIGH | MEDIUM | LOW |
|----|-------------|-------|------|--------|-----|
| FR-01 | Platform Adapter (Telegram + LINE) | 5 | 3 | 1 | 1 |
| FR-02 | Webhook Signature Verification | 4 | 1 | 3 | 0 |
| FR-03 | Unified Message Format | 4 | 1 | 3 | 0 |
| FR-04 | Input Sanitizer L2 | 4 | 2 | 2 | 0 |
| FR-05 | PII Masking L4 | 4 | 2 | 2 | 0 |
| FR-06 | Rate Limiter Token Bucket | 4 | 2 | 2 | 0 |
| FR-07 | Knowledge Layer V1 Rule Match | 4 | 2 | 2 | 0 |
| FR-08 | Basic Escalation Manager | 4 | 1 | 3 | 0 |
| FR-09 | Structured Logger JSON | 4 | 0 | 3 | 1 |
| FR-10 | API Response Format | 4 | 1 | 3 | 0 |
| FR-11 | Health Check Endpoint | 4 | 2 | 2 | 0 |
| FR-12 | Database Schema | 4 | 2 | 2 | 0 |
| FR-13 | Infrastructure / Docker Compose | 4 | 2 | 2 | 0 |

---

## Top HIGH Risks

| Risk ID | FR | Score | Category | Summary |
|---------|----|-------|----------|---------|
| RISK-FR13-02 | FR-13 | 16 | Security | `POSTGRES_PASSWORD` hardcoded; credential in version control |
| RISK-FR01-03 | FR-01 | 15 | Operational | LINE webhook 20-second response SLA; downstream processing exceeds limit |
| RISK-FR01-05 | FR-01 | 15 | Security | Telegram/LINE bot token rotation with zero downtime |
| RISK-FR01-02 | FR-01 | 12 | Reliability | Webhook duplicate delivery under retry; no idempotency guard |
| RISK-FR02-01 | FR-02 | 12 | Security | HMAC timing leak if `==` used instead of `hmac.compare_digest()` |
| RISK-FR03-01 | FR-03 | 12 | Technical | `UnifiedMessage` schema drift across platform adapter versions |
| RISK-FR04-01 | FR-04 | 12 | Security | Unicode NFKC normalization bypass via composed/decomposed sequences |
| RISK-FR04-03 | FR-04 | 12 | Security | Control-char filter bypass via zero-width characters not in block list |
| RISK-FR05-01 | FR-05 | 12 | Compliance | PII regex false-negative — non-standard phone/address formats unmasked |
| RISK-FR05-02 | FR-05 | 12 | Security | `should_escalate()` keyword list leaks sensitive topic signal via timing |
| RISK-FR06-01 | FR-06 | 12 | Reliability | Token bucket in-process state lost on restart; per-user limits reset |
| RISK-FR06-02 | FR-06 | 12 | Security | Bucket key collision: `platform:user_id` truncation enables cross-user bypass |
| RISK-FR07-01 | FR-07 | 12 | Technical | SQL ILIKE full-table scan on `knowledge_base` at scale; no index |
| RISK-FR07-02 | FR-07 | 12 | Technical | Confidence 0.95/0.7 thresholds hardcoded; no calibration mechanism |
| RISK-FR08-01 | FR-08 | 12 | Operational | `escalation_queue` unbounded; no SLA/expiry in Phase 1 |
| RISK-FR10-02 | FR-10 | 12 | Technical | `ApiResponse[T]` generic type erased at runtime; validators bypass |
| RISK-FR11-01 | FR-11 | 15 | Technical | Health check stubs `lambda: False` → permanent `unhealthy` status |
| RISK-FR11-02 | FR-11 | 20 | Operational | HTTP 200 always returned; orchestrators cannot detect unhealthy state |
| RISK-FR12-02 | FR-12 | 12 | Performance | No pgvector index; Phase 2 ANN queries run O(N) sequential scans |
| RISK-FR12-03 | FR-12 | 12 | Security | `webhook_secret_key_ref` stores raw secret without vault enforcement |
| RISK-FR13-01 | FR-13 | 12 | Security | `REDIS_PASSWORD` defaults to hardcoded `dev_redis_password` |

---

## Risk Categories Summary

| Category | Count | HIGH | Notes |
|----------|-------|------|-------|
| Security / Credential | 5 | 5 | FR-02, FR-12, FR-13 — hardcoded secrets, timing attacks |
| Technical / Reliability | 14 | 8 | FR-01, FR-06, FR-07, FR-11, FR-12 |
| Compliance / PII | 3 | 2 | FR-04, FR-05 — NFKC bypass, regex gaps |
| Operational | 6 | 4 | FR-01, FR-08, FR-11 — SLA, stubs, escalation |
| Performance | 4 | 2 | FR-07, FR-12 — missing indexes |
| Observability | 3 | 0 | FR-09, FR-11 — logger gaps, uptime metric |

---

## Assessment Methodology

- **Agent A** (DEVOPS developer): Identified risks per FR, documented in `07-risk/RISK_REGISTER.md`
- **Agent B** (ARCHITECT reviewer): Independent stateless review per FR; all 13 returned APPROVE
- **Scoring**: Likelihood (1–5) × Impact (1–5); HIGH ≥ 10, MEDIUM 6–9, LOW ≤ 5
- **Citations**: All risks include file:line citations per HR-15
- **Gate 1**: All 13 FRs PASS (score 96.0); committed in git

---

## Linked Documents

| Document | Path |
|----------|------|
| Detailed risk entries | `07-risk/RISK_REGISTER.md` |
| Mitigation tracking | `07-risk/RISK_MITIGATION_PLANS.md` |
| Current status | `07-risk/RISK_STATUS_REPORT.md` |
| Deferred items | `deferred_fixes.md` |
| Quality baseline | `06-quality/QUALITY_REPORT.md` |

---

*Generated: Phase 7 exit · harness-methodology v2.3.0 · 2026-05-16*
