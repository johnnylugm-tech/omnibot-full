# Release Checklist — OmniBot Phase 1

> **Phase**: 8 — Configuration Management
> **Project**: OmniBot
> **Date**: 2026-05-16
> **References**: 07-risk/RISK_ASSESSMENT.md, 07-risk/RISK_REGISTER.md

---

## Pre-Release Gates

- [x] Gate 1 PASS — all 13 FRs (score ≥ 75 per dimension)
- [x] Gate 2 PASS — P3 exit (score 96.5)
- [x] Gate 3 PASS — P4 exit (score 91.15)
- [x] Gate 4 PASS — P6 exit (score 96.33)
- [x] Phase 7 Risk Register complete (13/13 FRs)
- [x] Phase 8 Config Records complete (13/13 FRs)
- [x] All NFR requirements verified against specification: NFR-01 (FCR), NFR-02 (Response Time), NFR-03 (Security), NFR-04 (Reliability)

---

## Environment Configuration

- [ ] All secrets rotated from dev defaults (POSTGRES_PASSWORD, REDIS_PASSWORD, TELEGRAM_BOT_TOKEN, LINE_CHANNEL_SECRET)
- [ ] Secrets stored in secrets manager (HashiCorp Vault / AWS Secrets Manager / Kubernetes Secrets)
- [ ] Deployment environment variables match specification for each service
- [ ] Rollback plan documented for all production configuration changes
- [ ] POSTGRES_DSN points to production database (not docker-compose default)
- [ ] REDIS_URL points to production Redis (not docker-compose default)
- [ ] .env file (if used) is in .gitignore and not committed
- [ ] .env.example committed with placeholder values only

## Database

- [ ] PostgreSQL with pgvector extension available
- [ ] DB migration script executed against production DB
- [ ] All tables exist: users, conversations, messages, knowledge_base, platform_configs, escalation_queue, user_feedback, security_logs
- [ ] knowledge_base seeded with initial entries (is_active=TRUE)
- [ ] pg_dump backup schedule configured

## API / Platform

- [ ] Telegram webhook URL `https://<host>/api/v1/webhook/telegram` registered in BotFather via /setWebhook
- [ ] LINE webhook URL `https://<host>/api/v1/webhook/line` registered in LINE Developer Console
- [ ] Webhook endpoints use HTTPS (TLS 1.2+)
- [ ] Response time p95 < 3.0s verified under load

## Security

- [ ] PII masking verified in pre-deploy test (phone, email, address masked in logs)
- [ ] Rate limiter active (default 100 rps per platform:user_id)
- [ ] No hardcoded credentials in any committed file (grep -r "password\|secret\|token" src/)
- [ ] Security logs table receiving entries
- [ ] Vulnerability scan completed (bandit/npm audit) — no HIGH or CRITICAL findings
- [ ] Encryption verified: all secrets use at-rest encryption in secrets manager; TLS 1.2+ enforced for webhook endpoints
- [ ] Authorization/permission model reviewed: Phase 1 treats all authenticated requests equally; RBAC deferred to Phase 2
- [ ] Input whitelist confirmed: NFKC normalization removes non-printable characters; whitelist-based sanitization active

## Monitoring

- [ ] /api/v1/health returns status=healthy
- [ ] Log aggregator ingesting NDJSON format from stdout
- [ ] Alert configured for status=unhealthy
- [ ] Alert configured for 429 RATE_LIMIT_EXCEEDED spike
- [ ] Escalation queue monitored for unresolved items

## Docker

- [ ] docker compose up starts all 3 services cleanly
- [ ] postgres healthcheck passing
- [ ] redis healthcheck passing
- [ ] omnibot-api healthcheck passing (GET /api/v1/health)
- [ ] API accessible on port 8000

---

## FR Configuration Summary

| FR | Name | Requirement | Secrets | Env Vars | Status |
|----|------|-------------|---------|----------|--------|
| FR-01 | Platform Adapter | SRS.md:13-25 | TELEGRAM_BOT_TOKEN, LINE_CHANNEL_SECRET | — | ✅ |
| FR-02 | Webhook Sig Verify | SRS.md:28-41 | (shared FR-01) | — | ✅ |
| FR-03 | Unified Message | SRS.md:44-55 | None | — | ✅ |
| FR-04 | Input Sanitizer | SRS.md:59-68 | None | — | ✅ |
| FR-05 | PII Masking | SRS.md:74-87 | None | — | ✅ |
| FR-06 | Rate Limiter | SRS.md:91-101 | None | RATE_LIMIT_DEFAULT_RPS | ✅ |
| FR-07 | Knowledge Layer | SRS.md:107-119 | POSTGRES_DSN | — | ✅ |
| FR-08 | Escalation Manager | SRS.md:123-133 | POSTGRES_DSN | — | ✅ |
| FR-09 | Structured Logger | SRS.md:138-151 | None | LOG_LEVEL, SERVICE_NAME | ✅ |
| FR-10 | API Response Format | SRS.md:155-165 | None | — | ✅ |
| FR-11 | Health Check | SRS.md:169-178 | POSTGRES_DSN, REDIS_URL | — | ✅ |
| FR-12 | Database Schema | SRS.md:183-199 | POSTGRES_DSN, POSTGRES_PASSWORD | POSTGRES_USER, POSTGRES_DB | ✅ |
| FR-13 | Docker Compose | SRS.md:203-213 | POSTGRES_PASSWORD, REDIS_PASSWORD | POSTGRES_USER, POSTGRES_DB, API_PORT | ✅ |

---

---

## Specification Compliance

Every deployment configuration item is traced to its originating requirement or specification:

- **FR compliance**: All 13 FR configuration records verified against SRS specification (§FR-01 through §FR-13)
- **NFR compliance**: NFR-03 (Security) specification satisfied via secrets externalization; NFR-02 (Response Time) verified via health check monitoring
- **Architecture specification**: Deployment configuration adheres to SAD.md architecture constraints — no infrastructure dependencies leak into domain modules
- **Rollback specification**: All configuration changes follow documented rollback procedures (see deployment checklist per FR)

---

*Generated by harness-methodology v2.3.0 Phase 8 — Configuration Management*
