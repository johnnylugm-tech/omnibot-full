# Architecture Diagrams — OmniBot Phase 1

> **Project**: OmniBot — 多平台客服機器人
> **Phase**: 1 (MVP 基礎)
> **Version**: 1.0
> **Date**: 2026-05-13
> **Authored by**: Agent A (ARCHITECT)
> **Input**: SAD.md v1.0, ADR.md v1.0

---

## 1. System Context Diagram (C4 Level 1)

```
╔══════════════════════════════════════════════════════════════════════╗
║                        EXTERNAL SYSTEMS                             ║
║                                                                      ║
║   ┌─────────────────┐        ┌─────────────────┐                    ║
║   │  Telegram       │        │  LINE Messaging │                    ║
║   │  Bot API        │        │  API            │                    ║
║   │  (HTTPS/Push)   │        │  (HTTPS/Push)   │                    ║
║   └────────┬────────┘        └────────┬────────┘                    ║
║            │ webhook                  │ webhook                      ║
║            │ POST /telegram           │ POST /line                   ║
╚════════════╪══════════════════════════╪═════════════════════════════╝
             │                          │
             ▼                          ▼
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║               OmniBot API Service [System Boundary]                  ║
║               Port 8000 · FastAPI · Python 3.11 · asyncio            ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
             │                          │
             │ asyncpg                  │ aioredis
             ▼                          ▼
   ┌──────────────────┐      ┌────────────────────┐
   │   PostgreSQL 16  │      │    Redis 7-alpine  │
   │   + pgvector     │      │    (rate-limit)    │
   │   Port 5432      │      │    Port 6379       │
   └──────────────────┘      └────────────────────┘
```

**Actors**:
- **Telegram Bot API**: pushes Update objects to webhook endpoint on every user message
- **LINE Messaging API**: pushes WebhookEvent arrays to webhook endpoint on every user interaction
- **OmniBot API Service**: the system boundary — the only component we build and own
- **PostgreSQL 16 + pgvector**: persistent data (users, conversations, messages, knowledge_base, escalation_queue, security_logs, user_feedback, platform_configs)
- **Redis 7**: ephemeral rate-limit token bucket state

---

## 2. Container Diagram (C4 Level 2 — Docker Compose)

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Docker Compose Network                          │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │               omnibot-api (python:3.11-slim)                 │  │
│  │               Port 8000 exposed · depends_on: pg, redis      │  │
│  │                                                              │  │
│  │    ┌────────────────────────────────────────────────────┐   │  │
│  │    │              FastAPI Application                   │   │  │
│  │    │  POST /api/v1/webhook/telegram                     │   │  │
│  │    │  POST /api/v1/webhook/line                         │   │  │
│  │    │  GET  /api/v1/health                               │   │  │
│  │    └────────────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────────┘  │
│             │ asyncpg pool                   │ aioredis pool        │
│             ▼                               ▼                       │
│  ┌─────────────────────┐     ┌──────────────────────────┐          │
│  │  postgres           │     │  redis                   │          │
│  │  pgvector/pg16      │     │  redis:7-alpine          │          │
│  │  Port 5432          │     │  Port 6379               │          │
│  │  healthcheck:       │     │  healthcheck:            │          │
│  │  pg_isready         │     │  redis-cli ping          │          │
│  └─────────────────────┘     └──────────────────────────┘          │
└─────────────────────────────────────────────────────────────────────┘
```

**Service Startup Order**: `postgres [healthy]` + `redis [healthy]` → `omnibot-api` starts

---

## 3. Component Diagram (C4 Level 3 — Inside omnibot-api)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         omnibot-api (FastAPI)                               │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                    Platform Adapter Layer                             │  │
│  │                                                                      │  │
│  │  ┌──────────────────────┐    ┌──────────────────────────────────┐    │  │
│  │  │   TelegramAdapter    │    │    LINEAdapter                   │    │  │
│  │  │  + ReplyDispatcher   │    │  + ReplyDispatcher               │    │  │
│  │  │  send_reply uses     │    │  send_reply uses reply_token     │    │  │
│  │  │  platform_user_id    │    │  (single-use, ~30s TTL)         │    │  │
│  │  │  as chat_id          │    │  None → no-op (non-reply events) │    │  │
│  │  └──────────┬───────────┘    └──────────┬───────────────────────┘    │  │
│  │             │                            │                           │  │
│  │             ▼                            ▼                           │  │
│  │         ┌─────────────────────────────────────┐                     │  │
│  │         │         SignatureVerifier            │                     │  │
│  │         │   VERIFIERS dict: Platform → fn()   │                     │  │
│  │         │   hmac.compare_digest()             │                     │  │
│  │         └──────────────────┬──────────────────┘                     │  │
│  └──────────────────────────── │ ──────────────────────────────────────┘  │
│                                │ UnifiedMessage (frozen dataclass)          │
│  ┌─────────────────────────── ─│─ ──────────────────────────────────────┐  │
│  │              Identity & Conversation Layer                            │  │
│  │             ┌───────────────▼───────────────┐                        │  │
│  │             │       ConversationContext      │──► PostgreSQL          │  │
│  │             │   upsert users                │    (users +            │  │
│  │             │   create/reuse conversations  │     conversations)     │  │
│  │             └───────────────┬───────────────┘                        │  │
│  └─────────────────────────── ─│─ ──────────────────────────────────────┘  │
│                                │ UnifiedMessage + unified_user_id + conv_id  │
│  ┌─────────────────────────── ─│─ ──────────────────────────────────────┐  │
│  │              Message Processing Pipeline                              │  │
│  │             ┌───────────────▼───────────────┐                        │  │
│  │             │      InputSanitizerL2          │                        │  │
│  │             │  NFKC + control char removal   │                        │  │
│  │             └───────────────┬───────────────┘                        │  │
│  │             ┌───────────────▼───────────────┐                        │  │
│  │             │       PIIMaskerL4              │                        │  │
│  │             │  email→phone→address passes    │                        │  │
│  │             │  should_escalate() → trigger   │──► EscalationService   │  │
│  │             └───────────────┬───────────────┘                        │  │
│  │             ┌───────────────▼───────────────┐                        │  │
│  │             │        RateLimiter             │──► Redis               │  │
│  │             │  TokenBucket per platform:user │    ratelimit:{p}:{u}   │  │
│  │             └───────────────┬───────────────┘                        │  │
│  └─────────────────────────── ─│─ ──────────────────────────────────────┘  │
│                                │ sanitized text                              │
│  ┌─────────────────────────── ─│─ ──────────────────────────────────────┐  │
│  │              Knowledge & Escalation Layer                             │  │
│  │             ┌───────────────▼───────────────┐                        │  │
│  │             │    KnowledgeRepository         │──► PostgreSQL          │  │
│  │             │  ILIKE + ANY(keywords)         │    (knowledge_base)    │  │
│  │             │  confidence >= 0.70 → reply    │                        │  │
│  │             │  confidence < 0.70 → escalate  │──► EscalationService   │  │
│  │             └───────────────┬───────────────┘                        │  │
│  │             ┌───────────────▼───────────────┐                        │  │
│  │             │     EscalationService          │──► PostgreSQL          │  │
│  │             │  create / assign / resolve     │    (escalation_queue)  │  │
│  │             └───────────────┬───────────────┘                        │  │
│  └─────────────────────────── ─│─ ──────────────────────────────────────┘  │
│                                │ UnifiedResponse                             │
│  ┌─────────────────────────────│────────────────────────────────────────┐  │
│  │              Observability                                            │  │
│  │             ┌───────────────▼───────────────┐                        │  │
│  │             │      StructuredLogger          │──► stdout (NDJSON)     │  │
│  │             │  JSON per line; 5 levels       │                        │  │
│  │             └───────────────────────────────┘                        │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                   Health Check                                       │  │
│  │   GET /api/v1/health → postgres ping + redis ping → JSON status     │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Sequence Diagram — Happy Path (Rule Match)

```
User        Telegram/LINE     OmniBot API       ConvCtx    Sanitizer   PII     RateLimiter  KnowledgeRepo  Reply
 │               │                │                 │          │         │           │             │            │
 │  sends msg    │                │                 │          │         │           │             │            │
 │──────────────►│                │                 │          │         │           │             │            │
 │               │  POST /webhook │                 │          │         │           │             │            │
 │               │───────────────►│                 │          │         │           │             │            │
 │               │                │ verify HMAC     │          │         │           │             │            │
 │               │                │─────────────┐  │          │         │           │             │            │
 │               │                │  FAIL → 401 │  │          │         │           │             │            │
 │               │                │◄────────────┘  │          │         │           │             │            │
 │               │                │ parse → UnifiedMsg        │         │           │             │            │
 │               │                │────────────────►│          │         │           │             │            │
 │               │                │                 │ upsert   │         │           │             │            │
 │               │                │                 │ users    │         │           │             │            │
 │               │                │                 │ create   │         │           │             │            │
 │               │                │                 │ conv     │         │           │             │            │
 │               │                │◄────────────────│ (uid,cid)│         │           │             │            │
 │               │                │────────────────────────────►         │           │             │            │
 │               │                │                 │ sanitize │         │           │             │            │
 │               │                │◄────────────────────────── sanitized │           │             │            │
 │               │                │─────────────────────────────────────►│           │             │            │
 │               │                │                 │          │  mask   │           │             │            │
 │               │                │                 │          │  PII    │           │             │            │
 │               │                │◄─────────────────────────────────────│           │             │            │
 │               │                │──────────────────────────────────────────────────►             │            │
 │               │                │                 │          │         │  check()  │             │            │
 │               │                │                 │          │         │  True     │             │            │
 │               │                │◄──────────────────────────────────────────────── │             │            │
 │               │                │─────────────────────────────────────────────────────────────── ►            │
 │               │                │                 │          │         │           │   query()   │            │
 │               │                │                 │          │         │           │   conf=0.95 │            │
 │               │                │◄────────────────────────────────────────────────────────────── │            │
 │               │                │ 200 OK + send_reply()                │           │             │────────────►
 │               │◄───────────────│                 │          │         │           │             │            │
 │◄──────────────│  reply msg     │                 │          │         │           │             │            │
```

---

## 5. Sequence Diagram — Escalation Path

```
User        Platform     OmniBot API     ConvCtx   Sanitizer  PII    RateLimiter  KnowledgeRepo  EscalSvc   Reply
 │              │              │             │          │        │          │             │             │         │
 │  sends msg   │              │             │          │        │          │             │             │         │
 │─────────────►│              │             │          │        │          │             │             │         │
 │              │  POST /wbhk  │             │          │        │          │             │             │         │
 │              │─────────────►│             │          │        │          │             │             │         │
 │              │              │ verify → OK │          │        │          │             │             │         │
 │              │              │────────────►│          │        │          │             │             │         │
 │              │              │◄────────────│ uid,cid  │        │          │             │             │         │
 │              │              │────────────────────────►        │          │             │             │         │
 │              │              │◄─────────────────────── sanitized│          │             │             │         │
 │              │              │─────────────────────────────────►│          │             │             │         │
 │              │              │◄──────────────────────────────── │ masked   │             │             │         │
 │              │              │──────────────────────────────────────────── ►             │             │         │
 │              │              │◄────────────────────────────────────────── True           │             │         │
 │              │              │─────────────────────────────────────────────────────────── ►             │         │
 │              │              │                                             │  no match   │             │         │
 │              │              │◄─────────────────────────────────────────────────────────── conf=0.0    │         │
 │              │              │──────────────────────────────────────────────────────────────────────── ►         │
 │              │              │                                                                │  create()│         │
 │              │              │◄──────────────────────────────────────────────────────────────────────── │         │
 │              │              │──────────────────────────────────────────────────────────────────────────────────► │
 │              │              │                                                                │          │ handoff │
 │              │◄─────────────│ 200 OK + send_reply(handoff msg)                               │          │         │
 │◄─────────────│  handoff msg │                                                                │          │         │
```

---

## 6. Data Flow Diagram — PII Masking

```
Raw user input text
        │
        ▼
┌─────────────────────┐
│  InputSanitizerL2   │
│                     │
│  1. NFKC normalize  │
│  2. Remove ctrl     │
│     chars except    │
│     \n \t           │
│  3. strip()         │
└──────────┬──────────┘
           │ sanitized text
           ▼
┌─────────────────────────────────────────────┐
│                PIIMaskerL4                  │
│                                             │
│  Pass 1: email regex                        │
│    find all matches → sort rightmost-first  │
│    replace each → [email_masked]            │
│           │                                 │
│           ▼  (text after pass 1)            │
│  Pass 2: phone regex                        │
│    find all matches → sort rightmost-first  │
│    replace each → [phone_masked]            │
│           │                                 │
│           ▼  (text after pass 2)            │
│  Pass 3: address regex                      │
│    find all matches → sort rightmost-first  │
│    replace each → [address_masked]          │
│           │                                 │
│           ▼                                 │
│  should_escalate() check on ORIGINAL text   │
│    密碼 | 銀行帳戶 | 信用卡號 | 提款卡      │
│    found → trigger EscalationService        │
└──────────────────────────────────────────────┘
           │
           ▼
   PIIMaskResult(masked_text, mask_count, pii_types)
```

---

## 7. Database Entity Relationship Diagram

```
┌──────────────────┐         ┌──────────────────────┐
│      users       │         │    platform_configs   │
│─────────────────-│         │──────────────────────-│
│ id SERIAL PK     │         │ id SERIAL PK          │
│ unified_user_id  │         │ platform VARCHAR       │
│   UUID UNIQUE    │         │ rate_limit_rps INT     │
│ platform VARCHAR │         │ webhook_secret_key_ref │
│ platform_user_id │         └───────────────────────┘
│ UNIQUE(plt,p_uid)│
│ last_seen TSTZ   │
└───────┬──────────┘
        │ 1:N
        ▼
┌──────────────────┐         ┌──────────────────────┐
│  conversations   │         │    knowledge_base     │
│─────────────────-│         │──────────────────────-│
│ id SERIAL PK     │         │ id SERIAL PK          │
│ unified_user_id  │         │ question TEXT          │
│   FK → users     │         │ answer TEXT            │
│ created_at TSTZ  │         │ keywords TEXT[]        │
│ resolved_at TSTZ │         │ embeddings vector(384) │
│ first_contact_   │         │ version INT            │
│   resolution BOOL│         │ is_active BOOL         │
│ satisfaction_scr │         │ created_at TSTZ        │
│ scope_type       │         └──────────┬─────────────┘
│ dst_state JSONB  │                    │
└───────┬──────────┘                    │ 1:N (knowledge_id)
        │ 1:N                           │
        ▼                               ▼
┌──────────────────┐         ┌──────────────────────┐
│    messages      │         │   escalation_queue   │
│─────────────────-│         │──────────────────────-│
│ id SERIAL PK     │         │ id SERIAL PK          │
│ conversation_id  │         │ conversation_id       │
│   FK → convs     │         │   FK → conversations  │
│ content TEXT     │         │ reason TEXT            │
│ direction        │         │ assigned_agent TEXT    │
│ intent_detected  │         │ picked_at TSTZ         │
│ sentiment_categ  │         │ resolved_at TSTZ       │
│ sentiment_intens │         │ created_at TSTZ        │
│ knowledge_source │         │ priority INT           │
│ received_at TSTZ │         │ sla_deadline TSTZ NULL │
└──────────────────┘         └───────────────────────┘

┌──────────────────┐         ┌──────────────────────┐
│  user_feedback   │         │    security_logs     │
│─────────────────-│         │──────────────────────-│
│ id SERIAL PK     │         │ id SERIAL PK          │
│ conversation_id  │         │ layer INT              │
│   FK → convs     │         │ blocked BOOL           │
│ feedback         │         │ source_ip TEXT         │
│  CHECK('thumbs_  │         │ platform VARCHAR       │
│  up','thumbs_down│         │ created_at TSTZ        │
│ created_at TSTZ  │         └───────────────────────┘
└──────────────────┘
```

---

## 8. Deployment Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        Development Environment                           │
│                         (Docker Compose v2)                              │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                   Host Machine (macOS / Linux)                     │ │
│  │                                                                    │ │
│  │  ┌─────────────────────────────────────────────────────────────┐  │ │
│  │  │                  Docker Compose Network                     │  │ │
│  │  │                                                             │  │ │
│  │  │  ┌────────────────────┐   ┌──────────────┐  ┌──────────┐  │  │ │
│  │  │  │   omnibot-api      │   │  postgres    │  │  redis   │  │  │ │
│  │  │  │   :8000            │   │  :5432       │  │  :6379   │  │  │ │
│  │  │  │   python:3.11-slim │   │  pgvector/   │  │  7-alpine│  │  │ │
│  │  │  │                    │   │  pg16        │  │          │  │  │ │
│  │  │  │   DEPENDS ON:      │   │  healthcheck │  │healthchk │  │  │ │
│  │  │  │   postgres[healthy]│   │  pg_isready  │  │ redis-cli│  │  │ │
│  │  │  │   redis[healthy]   │   │              │  │ ping     │  │  │ │
│  │  │  └────────────────────┘   └──────────────┘  └──────────┘  │  │ │
│  │  └─────────────────────────────────────────────────────────────┘  │ │
│  │                                                                    │ │
│  │  Host ports exposed: 8000 (API), 5432 (PG dev access), 6379 (Redis)│ │
│  └────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────┘

Env vars injected at container start (via .env file — gitignored):
  TELEGRAM_BOT_TOKEN, LINE_CHANNEL_SECRET, POSTGRES_PASSWORD, REDIS_PASSWORD
  (See ADR-012: Secret Management)
```

---

## 9. Module Dependency Graph (Layered)

```
Layer 0 — Entry Points (FastAPI Routes)
╔══════════════════════════════════════════════════════════╗
║  POST /webhook/telegram  POST /webhook/line  GET /health ║
╚═══════════════════╤═══════════════════╤══════════════════╝
                    │                   │
Layer 1 — Platform Adapter
╔═══════════════════▼═══════════════════▼══════════════════╗
║  TelegramAdapter (+ReplyDispatcher)  LINEAdapter (+Reply) ║
║            ├── SignatureVerifier                          ║
║            └── UnifiedMessage (frozen dataclass)         ║
╚═══════════════════════════════╤══════════════════════════╝
                                │
Layer 2 — Identity Resolution
╔═══════════════════════════════▼══════════════════════════╗
║                  ConversationContext                     ║
║           upsert users · create/reuse conversations      ║
╚═══════════════════════════════╤══════════════════════════╝
                                │
Layer 3 — Message Processing Pipeline
╔═══════════════════════════════▼══════════════════════════╗
║  InputSanitizerL2 → PIIMaskerL4 → RateLimiter           ║
║       (stdlib)         (stdlib)    (Redis)               ║
╚═══════════════════════════════╤══════════════════════════╝
                                │
Layer 4 — Business Logic
╔═══════════════════════════════▼══════════════════════════╗
║  KnowledgeRepository ──────────────────► EscalationService║
║       (PostgreSQL)          escalate         (PostgreSQL) ║
╚══════════════════════════════════════════════════════════╝

Cross-cutting — Observability (all layers call this)
╔══════════════════════════════════════════════════════════╗
║                   StructuredLogger                       ║
║                   (stdlib — no external deps)            ║
╚══════════════════════════════════════════════════════════╝

Infrastructure (all services depend on)
╔══════════════════════════════════════════════════════════╗
║  PostgreSQL 16 + pgvector  ·  Redis 7-alpine             ║
╚══════════════════════════════════════════════════════════╝

No upward dependencies (no circular dependencies).
```

---

## 10. FR Coverage Heatmap

```
FR     │ PlatAdapt │ Pipeline │ Knowledge │ Escalation │ API │ Observ │ DataLayer │ Infra │
───────┼───────────┼──────────┼───────────┼────────────┼─────┼────────┼───────────┼───────┤
FR-01  │     ██    │          │           │            │     │        │           │       │
FR-02  │     ██    │          │           │            │     │        │           │       │
FR-03  │     ██    │          │           │            │     │        │     ██    │       │
FR-04  │           │    ██    │           │            │     │        │           │       │
FR-05  │           │    ██    │           │            │     │        │           │       │
FR-06  │           │    ██    │           │            │     │        │           │       │
FR-07  │           │          │    ██     │            │     │        │     ██    │       │
FR-08  │           │          │           │     ██     │     │        │     ██    │       │
FR-09  │           │          │           │            │     │  ██    │           │       │
FR-10  │           │          │           │            │ ██  │        │           │       │
FR-11  │           │          │           │            │ ██  │        │           │       │
FR-12  │           │          │           │            │     │        │     ██    │       │
FR-13  │           │          │           │            │     │        │           │  ██   │
───────┴───────────┴──────────┴───────────┴────────────┴─────┴────────┴───────────┴───────┘
Legend: ██ = primary owner  (all 13 FRs covered, 0 unmapped)
```

---

## 11. Key Technical Notation Reference

| Pattern | Example | Component |
|---------|---------|-----------|
| Redis rate-limit key | `ratelimit:{platform}:{user_id}` | RateLimiter (FR-06) |
| Webhook endpoint template | `POST /api/v1/webhook/{platform}` | TelegramAdapter, LINEAdapter (FR-01) |
| Health response schema | `{status, postgres, redis, uptime_seconds}` | HealthCheck (FR-11) |
| SQL pattern | `(question ILIKE '%' \|\| $1 \|\| '%' OR $1 = ANY(keywords)) AND is_active = TRUE` | KnowledgeRepository (FR-07) |
| API response envelope | `{success, data, error, error_code}` | ApiResponse (FR-10) |

---

*ARCHITECTURE_DIAGRAM.md v1.0 — OmniBot Phase 1 — Agent A (ARCHITECT) — 2026-05-13*
