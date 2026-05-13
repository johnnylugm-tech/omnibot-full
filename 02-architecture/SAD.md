# Software Architecture Document — OmniBot

> **Project**: OmniBot — 多平台客服機器人
> **Phase**: 1 (MVP 基礎)
> **Version**: 1.0
> **Date**: 2026-05-13
> **Authored by**: Agent A (ARCHITECT)
> **Input**: SRS.md v1.0, CONSTRAINTS.md v1.0

---

## 1. Architecture Overview

### 1.1 System Context

OmniBot is a multi-platform customer service chatbot that receives webhook events from external messaging platforms (Telegram, LINE), processes user messages through a layered pipeline, queries a knowledge base, and replies via platform APIs.

```
┌──────────────────────────────────────────────────────────────────┐
│                        EXTERNAL ACTORS                           │
│  [Telegram Bot API]  [LINE Messaging API]  [Operations Team]     │
└────────┬──────────────────┬────────────────────────┬─────────────┘
         │ HTTPS webhook     │ HTTPS webhook           │ HTTPS API
         ▼                  ▼                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                     OmniBot API Service                          │
│   FastAPI  ·  Python 3.11  ·  asyncio  ·  Port 8000            │
│                                                                  │
│  ┌──────────────┐  ┌──────────────────────────────────────────┐ │
│  │ Platform     │  │        Message Processing Pipeline       │ │
│  │ Adapters     │→ │  Sanitizer → PII Masker → Rate Limiter  │ │
│  └──────────────┘  └───────────────────┬──────────────────────┘ │
│                                        │                         │
│  ┌─────────────────────────────────────▼──────────────────────┐ │
│  │           Knowledge Layer (Layer 1 — SQL Rule Match)       │ │
│  └─────────────────────────────────────┬──────────────────────┘ │
│                                        │                         │
│  ┌─────────────────────────────────────▼──────────────────────┐ │
│  │                   Escalation Manager                       │ │
│  └────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────┬────────────────────────┘
                                         │
               ┌─────────────────────────┤
               ▼                         ▼
    ┌──────────────────┐      ┌────────────────────┐
    │   PostgreSQL 16  │      │    Redis 7-alpine  │
    │   + pgvector     │      │    (rate-limit)    │
    └──────────────────┘      └────────────────────┘
```

### 1.2 Key Design Principles

1. **Pipeline isolation**: Each processing stage (adapter → sanitizer → PII masker → rate limiter → knowledge) is an independent module with no circular dependencies.
2. **Platform abstraction**: `UnifiedMessage` and `UnifiedResponse` decouple all downstream logic from platform specifics.
3. **Single database**: PostgreSQL serves both relational data and future vector embeddings (pgvector), eliminating a second infrastructure dependency in Phase 1.
4. **Async throughout**: All I/O-bound operations use Python `asyncio`; no synchronous ORM in the request path.
5. **Security at boundary**: Webhook signature verification executes before any business logic; unverified requests never reach the pipeline.
6. **Immutable message types**: `UnifiedMessage` is a `frozen=True` dataclass — thread-safe and hashable by design.

---

## 2. Module Design

### 2.1 Platform Adapter Layer

**FR Coverage**: FR-01, FR-02, FR-03

#### 2.1.1 TelegramAdapter

| Attribute | Value |
|-----------|-------|
| Responsibility | Receive `POST /api/v1/webhook/telegram`, verify HMAC-SHA256 signature, parse Telegram Update → `UnifiedMessage` |
| External Interface | `POST /api/v1/webhook/telegram` → `200 OK` / `401 AUTH_INVALID_SIGNATURE` / `400 Bad Request` |
| Dependencies | SignatureVerifier, UnifiedMessage, StructuredLogger |
| Persistence | None |

**Logical Constraints**:
- Must respond `200 OK` within 3 s of receipt regardless of downstream processing time
- HMAC key = SHA256(bot_token); uses `hmac.compare_digest()` for constant-time comparison
- Unsupported update types → `400 Bad Request`
- Platform enum value: `Platform.TELEGRAM`

#### 2.1.2 LINEAdapter

| Attribute | Value |
|-----------|-------|
| Responsibility | Receive `POST /api/v1/webhook/line`, verify HMAC-SHA256 + Base64 signature, parse LINE WebhookEvent → `UnifiedMessage` |
| External Interface | `POST /api/v1/webhook/line` → `200 OK` / `401 AUTH_INVALID_SIGNATURE` / `400 Bad Request` |
| Dependencies | SignatureVerifier, UnifiedMessage, StructuredLogger |
| Persistence | None |

**Logical Constraints**:
- HMAC key = channel_secret; signature header: `X-Line-Signature`
- Must reply `200 OK` to LINE within 3 s or LINE retries
- Platform enum value: `Platform.LINE`

#### 2.1.3 SignatureVerifier

| Attribute | Value |
|-----------|-------|
| Responsibility | Platform-agnostic HMAC signature verification using `VERIFIERS` dict registry |
| External Interface | `verify(platform, headers, body) → bool` |
| Dependencies | None (stdlib only: `hmac`, `hashlib`, `base64`) |
| Persistence | None |

**Logical Constraints**:
- `VERIFIERS` dict maps `Platform` enum → verifier callable; extensible for future platforms without code modification
- Always uses `hmac.compare_digest()` to prevent timing attacks

#### 2.1.4 ReplyDispatcher

| Attribute | Value |
|-----------|-------|
| Responsibility | Outbound message dispatch to platform APIs (Telegram sendMessage / LINE reply) |
| External Interface | `TelegramAdapter.send_reply(platform_user_id: str, content: str) → None`; `LINEAdapter.send_reply(reply_token: str, content: str) → None` |
| Dependencies | Telegram Bot API (HTTPS), LINE Messaging API (HTTPS), StructuredLogger |
| Persistence | None |

**Logical Constraints**:
- Implemented as methods on the respective Adapter classes, not a separate service
- Telegram: calls `POST https://api.telegram.org/bot{TOKEN}/sendMessage` with `chat_id` = platform_user_id
- LINE: calls `POST https://api.line.me/v2/bot/message/reply` with `replyToken` from original webhook payload
- Both mapped to FR-01 in FR-to-Component Mapping (Section 6)

#### 2.1.5 ConversationContext

| Attribute | Value |
|-----------|-------|
| Responsibility | Upsert user identity and create/reuse conversation records; inject `unified_user_id` and `conversation_id` into the pipeline before sanitization |
| External Interface | `resolve(platform: Platform, platform_user_id: str) → (unified_user_id: str, conversation_id: int)` |
| Dependencies | PostgreSQL (asyncpg), StructuredLogger |
| Persistence | `users` table (upsert); `conversations` table (insert or reuse open conversation) |

**Logical Constraints**:
- `users` upsert: `INSERT ... ON CONFLICT (platform, platform_user_id) DO UPDATE SET last_seen = NOW()` → returns `unified_user_id UUID`
- `conversations` lookup: find open conversation for `unified_user_id` with no `resolved_at`; if none, insert new row → returns `conversation_id INT`
- Executes immediately after PlatformAdapter parses the raw webhook and before InputSanitizerL2
- Mapped to FR-12 (database schema) and FR-03 (unified_user_id in UnifiedMessage)

#### 2.1.6 UnifiedMessage / UnifiedResponse (Data Contracts)

```python
@dataclass(frozen=True)
class UnifiedMessage:
    platform: Platform                # TELEGRAM | LINE | MESSENGER | WHATSAPP
    platform_user_id: str
    unified_user_id: str              # UUID assigned per platform+user pair
    message_type: MessageType         # TEXT | IMAGE | STICKER | LOCATION | FILE
    content: str
    raw_payload: dict
    received_at: datetime
    reply_token: Optional[str] = None # LINE only: events[0].replyToken (single-use, 30s TTL)
                                      # Telegram: None (uses chat_id from platform_user_id)

@dataclass(frozen=True)
class UnifiedResponse:
    content: str
    source: str                       # "rule_match" | "escalate"
    confidence: float                 # 0.0-1.0
    knowledge_id: int                 # -1 if escalated
```

**reply_token lifecycle**:
- `LINEAdapter.parse()` extracts `events[0].replyToken` and assigns to `UnifiedMessage.reply_token`
- `LINEAdapter.send_reply()` reads `unified_message.reply_token`; if None (non-reply events like follow/unfollow), send_reply() is a no-op
- LINE reply tokens are single-use and expire in 30 seconds — send_reply() must be called before the request handler returns
- Telegram `send_reply()` uses `platform_user_id` as `chat_id`; `reply_token` is always None for Telegram messages

---

### 2.2 Message Processing Pipeline

**FR Coverage**: FR-04, FR-05, FR-06

#### 2.2.1 InputSanitizerL2

| Attribute | Value |
|-----------|-------|
| Responsibility | NFKC Unicode normalization + non-printable character removal |
| External Interface | `sanitize(text: str) → str` |
| Dependencies | stdlib `unicodedata` |
| Persistence | None |

**Logical Constraints**:
- `unicodedata.normalize("NFKC", text)` applied first
- Remove all characters where `unicodedata.category(c)` is a control character, except `\n` (U+000A) and `\t` (U+0009)
- Result `strip()` to remove leading/trailing whitespace
- Does NOT perform pattern matching (deferred to Phase 2 L3)

#### 2.2.2 PIIMaskerL4

| Attribute | Value |
|-----------|-------|
| Responsibility | Detect and mask Taiwan phone numbers, email addresses, postal addresses; detect sensitive keyword escalation triggers |
| External Interface | `mask(text: str) → PIIMaskResult`; `should_escalate(text: str) → bool` |
| Dependencies | stdlib `re` |
| Persistence | None |

**Logical Constraints**:
- Phone pattern: `0[0-9]{2,3}-[0-9]{3,4}-[0-9]{3,4}` or 10-11 consecutive digits → `[phone_masked]`
- Email pattern: RFC 5321 simplified → `[email_masked]`
- Address pattern: Taiwan city/district + (路|街|巷|弄|號|樓) substring → `[address_masked]`
- Inter-type precedence (GAP-03): three pattern groups applied sequentially — email regex pass first, then phone regex pass on the output, then address regex pass on that output; each pass works on already-masked text from the prior pass
- Within each pass, matches are replaced rightmost-first to avoid index shift from shorter/longer substitution strings
- `should_escalate()` checks for sensitive keywords: 密碼, 銀行帳戶, 信用卡號, 提款卡
- Returns `PIIMaskResult(masked_text: str, mask_count: int, pii_types: list[str])`

#### 2.2.3 RateLimiter

| Attribute | Value |
|-----------|-------|
| Responsibility | Per-user per-platform token bucket rate limiting |
| External Interface | `check(platform: Platform, user_id: str) → bool` |
| Dependencies | Redis (asyncio client), StructuredLogger |
| Persistence | Redis: key `ratelimit:{platform}:{user_id}` → token count + last_refill_ts |

**Logical Constraints**:
- `TokenBucket(capacity=N, refill_rate=R)`: on `consume()` — refill tokens based on elapsed time, then deduct 1 if available
- Default `default_rps=100` (configurable via `platform_configs` table)
- Redis key TTL = `capacity / refill_rate + 60` seconds (auto-expire idle users)
- `False` → `429 RATE_LIMIT_EXCEEDED` returned before knowledge layer is invoked

---

### 2.3 Knowledge Layer

**FR Coverage**: FR-07

#### 2.3.1 KnowledgeRepository

| Attribute | Value |
|-----------|-------|
| Responsibility | SQL-based rule matching against `knowledge_base` table (Layer 1) |
| External Interface | `query(text: str) → KnowledgeResult` |
| Dependencies | PostgreSQL (asyncpg), StructuredLogger |
| Persistence | `knowledge_base` table (read-only in request path) |

**Logical Constraints**:
- Query only `is_active = TRUE` entries
- Exact match: `query_text` substring of `question` → confidence 0.95
- Partial match: `question ILIKE '%{term}%'` OR `'{term}' = ANY(keywords)` → confidence 0.70
- Order by `version DESC`, take first result
- No match → `KnowledgeResult(id=-1, source="escalate", confidence=0.0)`
- Confidence threshold: `>= 0.7` → reply; `< 0.7` → escalate
- SQL uses parameterized queries only; no string interpolation

---

### 2.4 Escalation Manager

**FR Coverage**: FR-08

#### 2.4.1 EscalationService

| Attribute | Value |
|-----------|-------|
| Responsibility | Create, assign, and resolve escalation records in `escalation_queue` |
| External Interface | `create(conversation_id, reason) → int`; `assign(escalation_id, agent_id) → None`; `resolve(escalation_id) → None` |
| Dependencies | PostgreSQL (asyncpg), StructuredLogger |
| Persistence | `escalation_queue` table |

**Logical Constraints**:
- `create()` writes `conversation_id`, `reason`, `created_at = NOW()`; returns new `escalation_id`
- `assign()` sets `assigned_agent`, `picked_at = NOW()`
- `resolve()` sets `resolved_at = NOW()`
- Phase 1: `sla_deadline` column exists but is NULL (activated Phase 2)

---

### 2.5 API & Response Layer

**FR Coverage**: FR-10, FR-11

#### 2.5.1 FastAPI Application

| Attribute | Value |
|-----------|-------|
| Responsibility | HTTP routing, request validation (Pydantic v2), response serialization |
| External Interface | All `/api/v1/*` endpoints |
| Dependencies | All modules above; PostgreSQL connection pool; Redis connection pool |
| Persistence | None (routes delegate to services) |

**Route Table**:

| Method | Path | Handler | FR |
|--------|------|---------|-----|
| POST | `/api/v1/webhook/telegram` | TelegramAdapter | FR-01, FR-02 |
| POST | `/api/v1/webhook/line` | LINEAdapter | FR-01, FR-02 |
| GET | `/api/v1/health` | HealthCheck | FR-11 |

#### 2.5.2 ApiResponse / PaginatedResponse

```python
class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T]
    error: Optional[str]
    error_code: Optional[ErrorCode]

class PaginatedResponse(ApiResponse[T]):
    total: int
    page: int
    limit: int
    has_next: bool

class ErrorCode(str, Enum):
    AUTH_INVALID_SIGNATURE = "AUTH_INVALID_SIGNATURE"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    KNOWLEDGE_NOT_FOUND = "KNOWLEDGE_NOT_FOUND"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"
```

#### 2.5.3 HealthCheck

| Attribute | Value |
|-----------|-------|
| Responsibility | Report service health including PostgreSQL and Redis connectivity |
| External Interface | `GET /api/v1/health` → `{status, postgres, redis, uptime_seconds}` |
| Dependencies | PostgreSQL (ping), Redis (ping) |
| Persistence | None |

**Status Logic**:
- `healthy`: postgres=True AND redis=True
- `degraded`: exactly one is False
- `unhealthy`: both False

---

### 2.6 Observability

**FR Coverage**: FR-09

#### 2.6.1 StructuredLogger

| Attribute | Value |
|-----------|-------|
| Responsibility | Emit JSON NDJSON log entries to stdout with consistent schema |
| External Interface | `log(level, service, message, **kwargs)`; shorthand: `info()`, `warn()`, `error()`, `debug()`, `critical()` |
| Dependencies | stdlib `logging`, `json`, `datetime` |
| Persistence | stdout (external log aggregator Phase 2+) |

**Output Schema** (one JSON object per line):
```json
{
  "timestamp": "2026-05-13T12:00:00.000Z",
  "level": "INFO",
  "service": "omnibot",
  "message": "knowledge match",
  "...kwargs": "..."
}
```

**Log Level Semantics**:
- `INFO`: business events (new conversation, rule match, escalation created)
- `WARN`: non-fatal anomalies (low-confidence match, PII detected, rate limit approaching)
- `ERROR`: fatal errors (DB connection failure, unhandled exception)
- `DEBUG`: developer diagnostics (raw webhook payload, sanitizer output)
- `CRITICAL`: integrity threats (signature bypass attempt, repeated auth failure)

---

### 2.7 Data Layer

**FR Coverage**: FR-12

#### 2.7.1 Schema Summary

| Table | Purpose | Phase 1 Key Columns |
|-------|---------|---------------------|
| `users` | Cross-platform identity | `unified_user_id UUID`, `platform`, `platform_user_id`; UNIQUE(platform, platform_user_id) |
| `conversations` | Conversation lifecycle | `satisfaction_score`, `first_contact_resolution BOOL`, `scope_type`, `dst_state JSONB` |
| `messages` | Message log | `intent_detected`, `sentiment_category`, `sentiment_intensity`, `knowledge_source` |
| `knowledge_base` | Rule entries | `question TEXT`, `answer TEXT`, `keywords TEXT[]`, `embeddings vector(384)`, `version INT`, `is_active BOOL` |
| `platform_configs` | Per-platform settings | `rate_limit_rps INT`, `webhook_secret_key_ref TEXT` |
| `escalation_queue` | Human handoff | `conversation_id`, `reason`, `assigned_agent`, `picked_at`, `resolved_at`, `sla_deadline` (NULL Phase 1) |
| `user_feedback` | Satisfaction signal | `feedback CHECK ('thumbs_up', 'thumbs_down')` |
| `security_logs` | Audit trail | `layer`, `blocked BOOL`, `source_ip TEXT` |

#### 2.7.2 Connection Management

- PostgreSQL: `asyncpg.create_pool(min_size=2, max_size=10)` initialized in FastAPI `lifespan` context
- Redis: `aioredis.from_url()` single connection pool, password-protected
- Both pools closed on shutdown via `lifespan` teardown

---

### 2.8 Infrastructure

**FR Coverage**: FR-13

#### 2.8.1 Docker Compose Services

| Service | Image | Port | Healthcheck |
|---------|-------|------|-------------|
| `omnibot-api` | Local Dockerfile (python:3.11-slim) | 8000 | `GET /api/v1/health` |
| `postgres` | `pgvector/pgvector:pg16` | 5432 | `pg_isready -U postgres` |
| `redis` | `redis:7-alpine` | 6379 | `redis-cli ping` |

**Dependency Order**: `postgres [healthy]` + `redis [healthy]` → `omnibot-api` starts

**Redis security**: `requirepass ${REDIS_PASSWORD}` via environment variable

---

## 3. Error Handling

| Level | Scenario | Handling Strategy |
|-------|----------|------------------|
| L1 — Boundary | Invalid webhook signature | Immediate `401` return; log `security_logs` |
| L1 — Boundary | Malformed request body | Pydantic validation → `422 VALIDATION_ERROR` |
| L2 — Rate Limit | Token bucket exhausted | Immediate `429 RATE_LIMIT_EXCEEDED`; no retry |
| L3 — Business | No knowledge match | Escalate to `escalation_queue`; reply with handoff message |
| L3 — Business | PII sensitive keyword | Escalate immediately; mask before any storage |
| L4 — Infrastructure | PostgreSQL unavailable | `500 INTERNAL_ERROR`; log ERROR; health = degraded/unhealthy |
| L4 — Infrastructure | Redis unavailable | Rate limiter fails open (allow-all); log WARN — acceptable for Phase 1 MVP traffic; Phase 2 adds in-process fallback bucket |

---

## 4. Technology Choices

| Technology | Rationale |
|------------|----------|
| FastAPI | Native async, Pydantic v2 validation, auto OpenAPI docs |
| PostgreSQL 16 + pgvector | Single DB for relational + future vector search; no external vector service in Phase 1 |
| Redis 7 | Persistent rate-limit state across restarts; sub-ms atomic operations |
| asyncpg | Pure-Python async PostgreSQL driver; no ORM overhead in request path |
| stdlib `re` for PII | Zero dependency; regex patterns are auditable and deterministic |
| `frozen=True` dataclasses | Thread-safe, hashable messages without external library |
| Docker Compose v2 | One-command dev environment; matches Phase 3 k8s topology conceptually |

---

## 5. Request Processing Data Flow

### 5.1 Happy Path (Rule Match)

```
[Platform]
    │ POST /api/v1/webhook/{platform}
    ▼
[SignatureVerifier]
    │ valid → continue
    │ invalid → 401 AUTH_INVALID_SIGNATURE  ──────────────────────► STOP
    ▼
[PlatformAdapter] (Telegram or LINE)
    │ parse → raw UnifiedMessage (no unified_user_id yet)
    ▼
[ConversationContext]
    │ upsert users → unified_user_id UUID
    │ create/reuse conversation → conversation_id INT
    │ inject both into UnifiedMessage
    ▼
[InputSanitizerL2]
    │ NFKC normalize + strip control chars → sanitized_text
    ▼
[PIIMaskerL4]
    │ mask PII → PIIMaskResult
    │ should_escalate? → yes ──────────────────────────────────────► [EscalationService.create()]
    ▼
[RateLimiter]
    │ check(platform, user_id) → True
    │ False → 429 RATE_LIMIT_EXCEEDED  ───────────────────────────► STOP
    ▼
[KnowledgeRepository]
    │ query(sanitized_text)
    │ confidence >= 0.7 → KnowledgeResult(id, answer, confidence=0.95|0.70)
    │ confidence < 0.7 → KnowledgeResult(id=-1, source="escalate")  ► [EscalationService.create()]
    ▼
[ReplyDispatcher] (method on TelegramAdapter / LINEAdapter)
    │ send answer to user via platform API
    ▼
[StructuredLogger]
    └── log INFO: knowledge_match, confidence, knowledge_id, user_id
```

### 5.2 Escalation Path

```
[KnowledgeRepository] → no match
    ▼
[EscalationService.create(conversation_id, reason="no_rule_match")]
    ▼
[ReplyDispatcher] → handoff message to user
    ▼
[StructuredLogger]
    └── log WARN: escalation_created, reason, user_id
```

---

## 6. FR-to-Component Mapping

| FR | Requirement | Component(s) |
|----|-------------|-------------|
| FR-01 | Platform Adapter — Telegram + LINE Webhook | TelegramAdapter, LINEAdapter, ReplyDispatcher |
| FR-02 | Webhook Signature Verification | SignatureVerifier |
| FR-03 | Unified Message Format | UnifiedMessage, UnifiedResponse, ConversationContext |
| FR-04 | Input Sanitizer L2 | InputSanitizerL2 |
| FR-05 | PII Masking L4 | PIIMaskerL4 |
| FR-06 | Rate Limiter — Token Bucket | RateLimiter + Redis |
| FR-07 | Knowledge Layer V1 — Rule Match | KnowledgeRepository + PostgreSQL |
| FR-08 | Basic Escalation Manager | EscalationService + PostgreSQL |
| FR-09 | Structured Logger — JSON Format | StructuredLogger |
| FR-10 | API Response Format | ApiResponse, PaginatedResponse, ErrorCode |
| FR-11 | Health Check Endpoint | HealthCheck (`GET /api/v1/health`) |
| FR-12 | Database Schema | PostgreSQL schema (8 tables), ConversationContext (upsert users + conversations) |
| FR-13 | Docker Compose Dev Environment | Docker Compose (3 services) |

---

## 7. Quality Attribute Scenarios

### 7.1 FCR Measurement (NFR-01 >= 50%)

FCR is recorded via `conversations.first_contact_resolution BOOL` (set to TRUE when EscalationService.resolve() is called without prior assign, indicating self-service resolution) and `user_feedback.feedback`. Aggregation query for the 30-day rolling metric is a Phase 2 dashboard deliverable — Phase 1 only provisions the columns and sets values; no runtime computation component is required.

### 7.2 Performance — p95 Latency < 3.0 s (NFR-02)

- Webhook handlers respond `200 OK` immediately; downstream processing can be fire-and-forget
- All DB operations use asyncpg connection pooling (no blocking I/O in request path)
- Rate limiter uses Redis atomic INCR + EXPIRE — sub-ms per check
- SQL knowledge query uses `ILIKE` on indexed `question` + GIN index on `keywords[]`

### 7.3 Security — 100% Webhook Verification (NFR-04)

- SignatureVerifier is the first call in every webhook handler (FastAPI dependency injection)
- No request can reach downstream if `verify()` returns False
- All signature failures logged to `security_logs` with `blocked=True`

### 7.4 PII Masking Coverage (NFR-06)

- PIIMaskerL4 executes after sanitization and before any DB write or log output
- `mask_count` tracked per request; logged at WARN if `mask_count > 0`

### 7.5 Extensibility — New Platform

- Adding a new platform: (1) new Adapter class, (2) entry in `VERIFIERS` dict, (3) new `Platform` enum value
- Zero changes to InputSanitizerL2, PIIMaskerL4, RateLimiter, KnowledgeRepository, EscalationService

---

## 8. Out-of-Scope Architecture (Phase 2+)

| Component | Phase |
|-----------|-------|
| RAG vector search (Layer 2, pgvector ivfflat index) | Phase 2 |
| LLM generation (Layer 3, Anthropic Claude) | Phase 2 |
| DST state machine (conversation state) | Phase 2 |
| Prompt injection defense (L3) | Phase 2 |
| SLA deadline enforcement | Phase 2 |
| Messenger / WhatsApp adapters | Phase 2 |
| RBAC / JWT authentication | Phase 3 |
| Kubernetes deployment | Phase 3 |
| Cost tracking (resolution_cost) | Phase 3 |

---

## 9. Module Dependency Graph

```
FastAPI App
├── TelegramAdapter ──► SignatureVerifier
│   (+ ReplyDispatcher method)
│                  ──► UnifiedMessage
├── LINEAdapter    ──► SignatureVerifier
│   (+ ReplyDispatcher method)
│                  ──► UnifiedMessage
├── ConversationContext ──► PostgreSQL
│                       ──► StructuredLogger
├── InputSanitizerL2   (stdlib only)
├── PIIMaskerL4        (stdlib only)
├── RateLimiter    ──► Redis
├── KnowledgeRepository ──► PostgreSQL
├── EscalationService   ──► PostgreSQL
├── HealthCheck    ──► PostgreSQL + Redis
└── StructuredLogger    (stdlib only)
```

No circular dependencies. Leaf nodes (SignatureVerifier, InputSanitizerL2, PIIMaskerL4, StructuredLogger) are pure-function modules with stdlib-only dependencies.

---

## 10. SAB Block (machine-readable)

<!-- SAB:START -->
```json
{
  "version": "1.0",
  "created_at": "2026-05-13",
  "phase": 2,
  "project": "omnibot",
  "layers": [
    {
      "name": "platform_adapter",
      "modules": ["FR-01", "FR-02", "FR-03"],
      "allowed_dependencies": ["pipeline", "observability"]
    },
    {
      "name": "pipeline",
      "modules": ["FR-04", "FR-05", "FR-06"],
      "allowed_dependencies": ["knowledge", "escalation", "observability", "infrastructure"]
    },
    {
      "name": "knowledge",
      "modules": ["FR-07"],
      "allowed_dependencies": ["data_layer", "observability"]
    },
    {
      "name": "escalation",
      "modules": ["FR-08"],
      "allowed_dependencies": ["data_layer", "observability"]
    },
    {
      "name": "api",
      "modules": ["FR-10", "FR-11"],
      "allowed_dependencies": ["platform_adapter", "pipeline", "knowledge", "escalation", "observability", "infrastructure"]
    },
    {
      "name": "observability",
      "modules": ["FR-09"],
      "allowed_dependencies": []
    },
    {
      "name": "data_layer",
      "modules": ["FR-12"],
      "allowed_dependencies": []
    },
    {
      "name": "infrastructure",
      "modules": ["FR-13"],
      "allowed_dependencies": ["data_layer"]
    }
  ],
  "dependencies": {
    "platform_adapter": ["pipeline", "observability"],
    "pipeline": ["knowledge", "escalation", "observability", "infrastructure"],
    "knowledge": ["data_layer", "observability"],
    "escalation": ["data_layer", "observability"],
    "api": ["platform_adapter", "pipeline", "knowledge", "escalation", "observability", "infrastructure"],
    "observability": [],
    "data_layer": [],
    "infrastructure": ["data_layer"]
  },
  "quality_targets": {
    "max_complexity": 15,
    "min_coverage": 80,
    "max_coupling": 0.3
  }
}
```
<!-- SAB:END -->

---

*SAD.md v1.0 — OmniBot Phase 1 — Agent A (ARCHITECT) — 2026-05-13*
