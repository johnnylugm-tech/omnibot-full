# Monitoring Plan — OmniBot Phase 1

> **Version**: 1.0
> **Date**: 2026-05-14

---

## 1. Health Check Monitoring

| Endpoint | Method | Interval | Alert Threshold |
|----------|--------|----------|-----------------|
| /api/v1/health | GET | 30s | status != "healthy" for 3 consecutive checks |

**Checks**:
- `postgres`: PostgreSQL connectivity (bool)
- `redis`: Redis connectivity (bool)
- `uptime_seconds`: Process uptime

## 2. Performance Monitoring

| Metric | Source | Target | Alert |
|--------|--------|--------|-------|
| p95 response latency | Webhook endpoints | < 3.0s | > 3.0s for 5 min |
| Rate limit rejections | RateLimiter | < 1% of requests | > 5% for 10 min |

## 3. Security Monitoring

| Event | Log Level | Action |
|-------|-----------|--------|
| Signature verification failure | CRITICAL | Alert + log source_ip to security_logs |
| PII detected in message | WARN | Log mask_count + pii_types |
| Sensitive keyword escalation | WARN | Create escalation record + alert |

## 4. Business Metrics

| Metric | Measurement | Target |
|--------|-------------|--------|
| FCR (30-day rolling) | SQL: conversations WHERE first_contact_resolution=TRUE | >= 50% |
| Knowledge match rate | QueryResult.confidence > 0.7 ratio | Baseline TBD |
| Escalation rate | Escalation records / total queries | < 30% |

## 5. Log Aggregation

- **Format**: NDJSON (StructuredLogger)
- **Fields**: timestamp, level, service, message + custom kwargs
- **Retention**: 30 days (hot) + 90 days (cold)
- **Levels**: DEBUG (dev only), INFO (business events), WARN (anomalies), ERROR (failures), CRITICAL (integrity threats)

## 6. Docker Health Checks

| Service | Check | Interval | Retries |
|---------|-------|----------|---------|
| postgres | pg_isready | 10s | 5 |
| redis | redis-cli ping | 10s | 5 |
| omnibot-api | curl /api/v1/health | 30s | 3 |

---

*MONITORING_PLAN.md v1.0 — Phase 5 deliverable*
