# Monitoring Plan — Phase 3 (24 FRs)

> Generated: 2026-05-17

## Prometheus Metrics (FR-22)
- `http_request_duration_seconds` — latency, 7 buckets (0.1-5.0s), platform label
- `http_requests_total` — status label, platform label
- `knowledge_hit_total` — source label (rule/rag/llm/escalate)
- `fcr_total` — resolved label
- `pii_masked_total` — type label
- `escalation_queue_depth` — priority label
- `emotion_trigger_total` — category label
- `llm_token_usage_total` — model label

## Health Check (FR-11)
- GET /api/v1/health: status, postgres, redis, uptime_seconds
- States: healthy, degraded, unhealthy

## SLA Monitoring (FR-20)
- Priority tiers: normal (30min SLA), high (15min), urgent (5min)
- SLA breach query: unresolved tickets past deadline
- Target: ≥90% compliance per priority (NFR-14)

## Grounding Assurance (FR-21)
- Cosine similarity ≥0.75 threshold
- Ungrounded outputs rejected and escalated

## Golden Dataset Regression (FR-24)
- 510 edge cases, 6 categories
- Auto-verified on each pipeline run

## NFR Targets
| NFR | Target | Monitoring Method |
|-----|--------|-------------------|
| NFR-07 | FCR ≥80% | Prometheus fcr_total |
| NFR-08 | p95 < 1.5s | Prometheus histogram |
| NFR-12 | Block rate ≥95% | Security log audit |
| NFR-14 | SLA ≥90% | SQL breach query |
