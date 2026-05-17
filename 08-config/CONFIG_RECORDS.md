# Configuration Records — Phase 3 Exit

> Phase: 3 (Implementation Complete) → 4 | Date: 2026-05-17

## Repository Configuration

| Item | Value |
|------|-------|
| Repository | omnibot-full |
| Branch | main |
| Python version | 3.11+ |
| Database | PostgreSQL 16 + pgvector |
| Framework | harness-methodology v2.4.0 |
| CI | GitHub Actions (harness_quality_gate.yml) |

## Environment Variables Required

| Variable | Purpose |
|----------|---------|
| HERMES_REVIEWER_TARGET | Hermes reviewer channel |
| TELEGRAM_BOT_TOKEN | Telegram webhook auth |
| LINE_CHANNEL_SECRET | LINE webhook auth |
| MESSENGER_APP_SECRET | Messenger webhook auth |
| WHATSAPP_VERIFY_TOKEN | WhatsApp webhook auth |
| DATABASE_URL | PostgreSQL connection |

## Dependency Policy
- stdlib-first: re for regex, hmac for signatures, json for serialization
- asyncpg for database (no synchronous ORM)
- prometheus_client for metrics
- FastAPI + uvicorn for HTTP
- No external vector DB (pgvector via PostgreSQL)

## State
- FSM: Phase 4 active, state=RUNNING
- last_gate: 4 (96.33)
- last_fr: FR-24
