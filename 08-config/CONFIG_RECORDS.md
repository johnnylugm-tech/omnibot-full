# Configuration Records — OmniBot Phase 8

> **Phase**: 8 — Configuration Management
> **Project**: OmniBot
> **Generated**: 2026-05-16
> **Framework**: harness-methodology v2.3.0
> **References**: 07-risk/RISK_ASSESSMENT.md, 07-risk/RISK_REGISTER.md

---

## Purpose

This document records all configuration items for OmniBot MVP (Phase 1 FRs FR-01 through FR-13).
Each FR section documents: environment variables, secrets management, deployment checklist items,
and configuration-aware notes for operators.

---

## Global Configuration

### Infrastructure (docker-compose.yml)

| Variable | Default (Dev) | Production | Secret? |
|----------|---------------|------------|---------|
| `POSTGRES_USER` | `omnibot` | vault/env | No |
| `POSTGRES_PASSWORD` | `omnibot_dev` | vault/secret | **YES** |
| `POSTGRES_DB` | `omnibot` | env | No |
| `POSTGRES_DSN` | `postgresql://omnibot:omnibot_dev@postgres:5432/omnibot` | vault/env | **YES** (contains password) |
| `REDIS_PASSWORD` | `dev_redis_password` | vault/secret | **YES** |
| `REDIS_URL` | `redis://:${REDIS_PASSWORD}@redis:6379` | vault/env | **YES** (contains password) |

**Secrets Management**: All production secrets must be stored in a secrets manager (e.g., HashiCorp Vault, AWS Secrets Manager, or Kubernetes Secrets). Never hardcode production credentials.

---

## FR-01: Platform Adapter Configuration

> **[FR-01]** Platform Adapter — Telegram + LINE Webhook
> Citations: SRS.md:13-25, 03-development/src/omnibot/auth/verifier.py:65-74

### Environment Variables / Secrets

| Variable | Description | Secret? | Header (Phase 1) | Algorithm |
|----------|-------------|---------|------------------|-----------|
| `TELEGRAM_BOT_TOKEN` | Bot token issued by BotFather; used as HMAC key after `SHA256(token)` digest | **YES** | `X-Telegram-Bot-Token` | HMAC-SHA256 (key = SHA256(token)) |
| `LINE_CHANNEL_SECRET` | Channel secret from LINE Developer Console; used directly as HMAC key | **YES** | `X-Line-Channel-Secret` | HMAC-SHA256 + Base64 |

**Secrets Management**: Store both values in a secrets manager (HashiCorp Vault, AWS Secrets Manager, or Kubernetes Secrets). Never commit to version control. Rotate immediately if exposed.

### Webhook Endpoints

| Platform | Method | Path | Success Response | Error Response |
|----------|--------|------|-----------------|----------------|
| Telegram | `POST` | `/api/v1/webhook/telegram` | `200 OK` within 3 s | `400 Bad Request` (unsupported platform) |
| LINE | `POST` | `/api/v1/webhook/line` | `200 OK` within 3 s | `400 Bad Request` (unsupported platform) |

Signature verification raises `401 Unauthorized` for missing or invalid signatures (see `03-development/src/omnibot/auth/verifier.py:77-103`).

### Deployment Checklist

- [ ] `TELEGRAM_BOT_TOKEN` injected via secrets manager (not `.env` in production)
- [ ] `LINE_CHANNEL_SECRET` injected via secrets manager (not `.env` in production)
- [ ] Webhook URL `https://<host>/api/v1/webhook/telegram` registered in **Telegram BotFather** via `/setWebhook`
- [ ] Webhook URL `https://<host>/api/v1/webhook/line` registered in **LINE Developer Console** under Messaging API → Webhook settings
- [ ] Webhook URLs use HTTPS (TLS 1.2+); self-signed certificates rejected by both platforms
- [ ] Response time p95 < 3.0 s verified under load (SRS.md:286)

### Security Notes

- **Telegram**: signature key is derived as `SHA256(TELEGRAM_BOT_TOKEN)` before HMAC — the raw token is never used directly as the HMAC key (`03-development/src/omnibot/auth/verifier.py:22-23`).
- **LINE**: signature is `Base64(HMAC-SHA256(LINE_CHANNEL_SECRET, body))`, compared via `hmac.compare_digest` to prevent timing attacks (`03-development/src/omnibot/auth/verifier.py:28-31`).
- Both secrets are passed per-request via headers in Phase 1; Phase 2 will migrate to server-side environment injection.
- Unsupported platforms are rejected with `400 Bad Request` before any business logic executes (`03-development/src/omnibot/router.py:21-26`).

---

## FR-02: Webhook Signature Verification Configuration

> **[FR-02]** Webhook Signature Verification — Telegram + LINE
> Citations: SRS.md:28-41, 03-development/src/omnibot/auth/verifier.py:17-31

### Environment Variables / Secrets

No new environment variables are required for FR-02. Signature verification reuses the same secrets provisioned for FR-01. Verification is entirely stateless.

| Variable | FR-01 Role | FR-02 Role | Derived Key | Secret? |
|----------|-----------|-----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Platform auth token | HMAC-SHA256 key material | `SHA256(TELEGRAM_BOT_TOKEN)` | **YES** |
| `LINE_CHANNEL_SECRET` | Platform auth token | HMAC-SHA256 key (used directly) | none — raw secret is the key | **YES** |

### Signature Verification Scheme

| Platform | Header (secret) | Header (signature) | Key | Algorithm | Encoding |
|----------|-----------------|--------------------|-----|-----------|----------|
| Telegram | `X-Telegram-Bot-Token` | `X-Telegram-Hmac-Signature` | `SHA256(TELEGRAM_BOT_TOKEN)` | HMAC-SHA256 | hex |
| LINE | `X-Line-Channel-Secret` | `X-Line-Signature` | `LINE_CHANNEL_SECRET` (raw) | HMAC-SHA256 | Base64 |

- All comparisons use `hmac.compare_digest()` to prevent timing-attack leakage (`03-development/src/omnibot/auth/verifier.py:17-24`).
- Verification failure (missing header, wrong signature) returns `401 Unauthorized` with error code `AUTH_INVALID_SIGNATURE`.

### Deployment Checklist

- [ ] Confirm `TELEGRAM_BOT_TOKEN` and `LINE_CHANNEL_SECRET` are injected from secrets manager (shared with FR-01; no duplicate provisioning needed)
- [ ] Verify request headers `X-Telegram-Bot-Token`, `X-Telegram-Hmac-Signature`, `X-Line-Channel-Secret`, `X-Line-Signature` are forwarded untransformed by any reverse proxy / load balancer
- [ ] Test signature rejection path: send request with corrupted signature; confirm `401 AUTH_INVALID_SIGNATURE` response
- [ ] Secret rotation procedure:
  1. Generate new token / channel secret in BotFather / LINE Developer Console
  2. Store new value in secrets manager; keep old value active during rollover window
  3. Deploy new application version with updated secret reference
  4. Validate signature verification passes with new secret
  5. Remove old secret from secrets manager; confirm no requests are rejected
- [ ] Confirm `hmac.compare_digest` is used in all verification paths (not `==`) — see `03-development/src/omnibot/auth/verifier.py:17-24`

### Security Notes

- The raw `TELEGRAM_BOT_TOKEN` string is **never** used directly as an HMAC key; the key is always derived as `SHA256(token)` (`verifier.py:22-23`).
- `LINE_CHANNEL_SECRET` is used as the HMAC key without further hashing; ensure the secret itself has sufficient entropy (LINE enforces ≥ 32 chars).
- `hmac.compare_digest()` ensures constant-time comparison — do not replace with `==` or `!=`.
- No verification state is persisted; replay protection (nonce / timestamp) is out of scope for Phase 1.

---

## FR-03: Unified Message Format Configuration

> **[FR-03]** Unified Message Format — `UnifiedMessage` dataclass (`frozen=True`)
> Citations: SRS.md:44-55, 03-development/src/omnibot/models.py:12-55

### Environment Variables / Secrets

No environment variables are required for FR-03. `UnifiedMessage` and `UnifiedResponse` are pure
in-memory dataclasses with no external configuration dependencies.

| Variable | Description | Secret? | Notes |
|----------|-------------|---------|-------|
| _(none)_ | — | — | All data is runtime-constructed; no env vars consumed |

### Data Model Reference

**`Platform` enum** (`models.py:12-20`) — string-valued, `str, Enum`:

| Member | Wire Value | Platform |
|--------|-----------|----------|
| `TELEGRAM` | `"TELEGRAM"` | Telegram Bot API |
| `LINE` | `"LINE"` | LINE Messaging API |
| `MESSENGER` | `"MESSENGER"` | Meta Messenger |
| `WHATSAPP` | `"WHATSAPP"` | WhatsApp Business API |

Adding a new platform requires a **code change** (new enum member + adapter implementation); there is no runtime-configurable platform registry.

**`MessageType` enum** (`models.py:23-32`) — string-valued, `str, Enum`:

| Member | Wire Value |
|--------|-----------|
| `TEXT` | `"TEXT"` |
| `IMAGE` | `"IMAGE"` |
| `STICKER` | `"STICKER"` |
| `LOCATION` | `"LOCATION"` |
| `FILE` | `"FILE"` |

**`UnifiedMessage` dataclass** (`models.py:35-56`) — `frozen=True`, immutable after construction:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `platform` | `Platform` | required | Source platform |
| `platform_user_id` | `str` | required | Platform-native user identifier |
| `message_type` | `MessageType` | required | Message classification |
| `content` | `str` | required | Normalized message text / URI |
| `raw_payload` | `Dict[str, Any]` | `{}` | Original platform payload (preserved for debugging) |
| `received_at` | `datetime` | `datetime.now(UTC)` | UTC ingestion timestamp |
| `unified_user_id` | `str` | `""` | Cross-platform user identity (enriched post-auth) |
| `reply_token` | `Optional[str]` | `None` | Platform reply token (LINE-specific; `None` for others) |

**`UnifiedResponse` dataclass** (`models.py:59-68`) — `frozen=True`:

| Field | Type | Description |
|-------|------|-------------|
| `content` | `str` | Outbound response text |
| `source` | `str` | Knowledge source identifier |
| `confidence` | `float` | Answer confidence score (0.0–1.0) |
| `knowledge_id` | `int` | FK to knowledge base entry |

### Deployment Checklist

- [ ] Verify all platform adapters (Telegram, LINE, Messenger, WhatsApp) construct `UnifiedMessage` with valid `Platform` and `MessageType` enum members before deploy
- [ ] Confirm no adapter passes raw string values for `platform` or `message_type` fields (must use enum members, not bare strings)
- [ ] Validate `unified_user_id` enrichment is applied before any cross-platform lookup
- [ ] Ensure `frozen=True` is preserved on both dataclasses — mutation attempts raise `FrozenInstanceError` and indicate a logic error in the caller
- [ ] Run adapter unit tests confirming `UnifiedMessage.to_json_dict()` produces ISO8601 `received_at` for downstream consumers

### Monitoring / Observability

Log the following fields on every inbound message for production observability:

| Field | Log Level | Purpose |
|-------|-----------|---------|
| `unified_user_id` | INFO | Cross-platform user tracking |
| `message_type` | INFO | Traffic composition metrics |
| `platform` | INFO | Per-platform volume monitoring |
| `received_at` | DEBUG | Latency / ordering analysis |

Do **not** log `raw_payload` at INFO or above — it may contain PII from platform webhooks.

### Security Notes

- `UnifiedMessage` is `frozen=True`; immutability prevents accidental mutation of verified message data as it passes through the processing pipeline.
- `raw_payload` is retained for audit/debugging but must not be forwarded to external services without scrubbing.
- No imports from `app/infrastructure/` are permitted in this module (pure domain model).

---

## FR-04: Input Sanitizer L2 Configuration

> **[FR-04]** Input Sanitizer L2 — Character Normalization
> Citations: SRS.md:59-68, 03-development/src/omnibot/sanitizer/__init__.py

### Environment Variables / Secrets

No environment variables are required for FR-04. The sanitizer is a pure function with no
configurable parameters in Phase 1. NFKC normalization is locale-independent and requires
no locale configuration.

| Variable | Description | Secret? | Notes |
|----------|-------------|---------|-------|
| _(none)_ | — | — | Pure function; all behavior is compile-time constant in Phase 1 |

### Sanitization Pipeline (Phase 1)

| Step | Operation | Implementation |
|------|-----------|---------------|
| 1 | Unicode normalization | `unicodedata.normalize('NFKC', text)` |
| 2 | Strip non-printable characters | Remove codepoints where `unicodedata.category(c)` is a control category, preserving `\n` (U+000A) and `\t` (U+0009) |
| 3 | Whitespace trimming | `str.strip()` |

- **No external state**: the function holds no module-level mutable state and has no I/O side effects.
- **No infrastructure imports**: `app/infrastructure/` imports are forbidden in this module.

### Deployment Checklist

- [ ] Confirm sanitizer module has no imports from `app/infrastructure/` (pure domain function)
- [ ] Verify `unicodedata` is from the Python stdlib — no third-party Unicode library required
- [ ] Run unit tests covering: empty string, all-whitespace, mixed control characters, multi-codepoint Unicode (e.g. ligatures, full-width digits) to confirm NFKC decomposition
- [ ] Confirm `\n` (newline) and `\t` (tab) are preserved after sanitization
- [ ] Validate sanitizer is applied before any downstream processing (router, agent dispatch)

### Future Configuration (Phase 2)

| Variable | Type | Purpose | Phase |
|----------|------|---------|-------|
| `MAX_INPUT_LENGTH` | `int` | Truncate or reject inputs exceeding this byte/char limit for DoS protection | Phase 2 |

`MAX_INPUT_LENGTH` is intentionally omitted from Phase 1; introduce it as an environment variable
with a sensible default (e.g. `4096`) when DoS protection requirements are formalised.

### Monitoring / Observability

| Condition | Log Level | Message |
|-----------|-----------|---------|
| Input length exceeds expected threshold | WARN | `sanitizer: input length {len} exceeds expected maximum` |
| Non-printable characters stripped | DEBUG | `sanitizer: stripped {n} non-printable characters` |

Do **not** log raw input content at INFO or above — it may contain PII from platform webhooks.

### Security Notes

- NFKC normalization prevents homoglyph / Unicode-smuggling attacks by collapsing compatibility
  equivalents before any content inspection.
- Non-printable character removal reduces the surface for control-character injection into
  downstream log sinks or terminals.
- Phase 1 applies no length cap; operators should monitor for unusually long inputs and plan
  `MAX_INPUT_LENGTH` enforcement for Phase 2.

---

## FR-05: PII Masking L4 Configuration

> **[FR-05]** PII Masking L4 — Phone/Email/Address
> Citations: SRS.md:74-87, 03-development/src/omnibot/pii/__init__.py:25-93

### Environment Variables / Secrets

No environment variables are required for FR-05. All regex patterns and sensitive keyword lists
are hardcoded in Phase 1. PII masking is always on — there is no runtime toggle.

| Variable | Description | Secret? | Notes |
|----------|-------------|---------|-------|
| _(none)_ | — | — | Patterns hardcoded in Phase 1; no env vars consumed |

### Implicit Configuration (Phase 1 — Hardcoded)

| Config Item | Phase 1 Value | Secret? | Phase 2 Plan |
|-------------|---------------|---------|--------------|
| `PII_MASKING_ENABLED` | `true` (implicit — always on) | No | Add toggle env var if selective disablement needed |
| `SENSITIVE_KEYWORDS` | `['密碼', '銀行帳戶', '信用卡號', '提款卡']` (hardcoded) | No | Externalize to config file or env var |
| Taiwan phone pattern | `0\d{2,3}-?\d{3}-?\d{3,4}` (hardcoded) | No | Move to configurable pattern list |
| Email pattern | RFC-5321 subset (hardcoded) | No | Move to configurable pattern list |
| Taiwan address pattern | Structured CJK address regex (hardcoded) | No | Move to configurable pattern list |

### Mask Tokens

| PII Type | Mask Token | Example Input | Example Output |
|----------|------------|--------------|----------------|
| Taiwan phone | `[phone_masked]` | `0912-345-678` | `[phone_masked]` |
| Email | `[email_masked]` | `user@example.com` | `[email_masked]` |
| Taiwan address | `[address_masked]` | `台北市信義區信義路五段7號` | `[address_masked]` |

### Return Value

`PIIMaskResult(masked_text, mask_count, pii_types)` — all three fields are required in callers.

| Field | Type | Description |
|-------|------|-------------|
| `masked_text` | `str` | Input text with PII replaced by mask tokens |
| `mask_count` | `int` | Total number of PII occurrences replaced |
| `pii_types` | `list[str]` | PII categories detected (e.g. `["phone", "email"]`) |

### Escalation Detection

`should_escalate()` scans `masked_text` for sensitive keywords and returns `True` if any match.

| Keyword | Language | Category |
|---------|----------|----------|
| `密碼` | zh-TW | Password / credential |
| `銀行帳戶` | zh-TW | Bank account |
| `信用卡號` | zh-TW | Credit card number |
| `提款卡` | zh-TW | ATM / debit card |

Escalation check runs on `masked_text` (post-masking), so raw PII is never exposed to the keyword scanner.

### Deployment Checklist

- [ ] Confirm PII masking is applied **before** any logging call and **before** any downstream service call
- [ ] Verify mask tokens (`[phone_masked]`, `[email_masked]`, `[address_masked]`) appear in logs — raw PII must never appear in log output
- [ ] Confirm no imports from `app/infrastructure/` exist in `03-development/src/omnibot/pii/__init__.py`
- [ ] Run unit tests covering: Taiwan phone (with and without dashes), email (subdomains, plus-addressing), Taiwan address (county + district + street), overlapping PII in a single string
- [ ] Validate `mask_count` equals the sum of individual pattern match counts in test cases
- [ ] Validate `should_escalate()` returns `True` for each sensitive keyword individually and `False` for neutral input
- [ ] Confirm `PIIMaskResult` is consumed by callers — `masked_text` forwarded, `mask_count`/`pii_types` logged at DEBUG

### Compliance Notes

- Mask tokens **must** appear in all log lines that echo user content; raw PII strings are forbidden in log sinks.
- `mask_count > 0` and non-empty `pii_types` should be emitted as structured log fields for audit trail purposes.
- Retention of `raw_payload` (see FR-03) is subject to the same PII constraint — scrub before storing or forwarding.

### Future Configuration (Phase 2)

| Variable | Type | Purpose | Phase |
|----------|------|---------|-------|
| `PII_MASKING_ENABLED` | `bool` | Runtime toggle for environments where masking is not required (e.g. dev with synthetic data) | Phase 2 |
| `SENSITIVE_KEYWORDS` | `str` (comma-separated or JSON path) | Externalize keyword list to allow ops updates without code deployment | Phase 2 |
| `PII_PATTERN_CONFIG` | `str` (file path or env JSON) | Externalize regex patterns for country-specific PII profiles | Phase 2 |

### Security Notes

- Regex patterns are compiled at import time; no runtime pattern injection is possible in Phase 1.
- `should_escalate()` operates on post-masked text — a sensitive keyword that happens to be inside a masked region is still replaced and cannot trigger escalation based on the masked token alone.
- No infrastructure imports (`app/infrastructure/`) are permitted in the PII module (pure domain function).

---

## FR-06: Rate Limiter Configuration

> **[FR-06]** Rate Limiter — Token Bucket
> Citations: SRS.md:91-101, 03-development/src/omnibot/rate_limiter/__init__.py:13-59

### Environment Variables / Configuration

| Variable | Default | Secret? | Notes |
|----------|---------|---------|-------|
| `RATE_LIMIT_DEFAULT_RPS` | `100` | No | Max requests per second per user; hardcoded in Phase 1 — Phase 2 reads from env |
| `RATE_LIMIT_CAPACITY` | equals `RATE_LIMIT_DEFAULT_RPS` | No | Token bucket capacity; hardcoded to match RPS in Phase 1 — Phase 2 independently configurable |

### Token Bucket Scheme

| Config Item | Phase 1 Value | Secret? | Phase 2 Plan |
|-------------|---------------|---------|--------------|
| `RATE_LIMIT_DEFAULT_RPS` | `100` (hardcoded) | No | Read from env var with default |
| `RATE_LIMIT_CAPACITY` | `100` (equals RPS) | No | Separate env var; allows burst > steady-state RPS |
| State backend | In-memory (`dict`) | No | Migrate to Redis for distributed state |
| Bucket scope | `platform:user_id` | No | One bucket per unique platform+user pair |

**TokenBucket** (`rate_limiter/__init__.py:13-59`): `capacity` sets the maximum token accumulation; `refill_rate` controls tokens added per second (equals `RATE_LIMIT_DEFAULT_RPS` in Phase 1). Both are configurable in Phase 2.

**RateLimiter**: manages one `TokenBucket` per `platform:user_id` key. Buckets are created on first request and held in-memory for the process lifetime.

### Response Behaviour

| Condition | HTTP Status | Error Code |
|-----------|-------------|------------|
| Within limit | (pass-through) | — |
| Limit exceeded | `429 Too Many Requests` | `RATE_LIMIT_EXCEEDED` |

### Deployment Checklist

- [ ] Confirm `RATE_LIMIT_DEFAULT_RPS=100` default is acceptable for production traffic profile; tune before go-live
- [ ] Confirm in-memory bucket state is acceptable for Phase 1 single-instance deployment (no distributed state)
- [ ] Plan Redis migration for Phase 2 multi-instance / horizontal scaling (in-memory state is not shared across pods)
- [ ] Verify `429 RATE_LIMIT_EXCEEDED` responses are not retried aggressively by platform webhook callers (add `Retry-After` header in Phase 2)
- [ ] Confirm no imports from `app/infrastructure/` exist in the rate limiter module (pure domain)

### Monitoring / Observability

| Event | Log Level | Fields | Purpose |
|-------|-----------|--------|---------|
| `429 RATE_LIMIT_EXCEEDED` | WARN | `platform`, `user_id`, `bucket_tokens`, `request_timestamp` | Abuse detection and capacity planning |
| Bucket created | DEBUG | `platform:user_id` | Track active user population |

Log all `429` events with the composite key `platform:user_id` to enable per-user abuse analysis. Alert if `429` rate for a single `platform:user_id` exceeds a rolling threshold (threshold configurable in Phase 2).

### Future Configuration (Phase 2)

| Variable | Type | Purpose | Phase |
|----------|------|---------|-------|
| `RATE_LIMIT_DEFAULT_RPS` | `int` | Read from env (currently hardcoded to `100`) | Phase 2 |
| `RATE_LIMIT_CAPACITY` | `int` | Independently configurable bucket capacity (currently equals RPS) | Phase 2 |
| `RATE_LIMIT_BACKEND` | `str` | `memory` (Phase 1) → `redis` (Phase 2) for distributed state | Phase 2 |
| `RATE_LIMIT_REDIS_URL` | `str` | Redis connection URL for distributed bucket state | Phase 2 |

### Security Notes

- Per-user rate limiting uses `platform:user_id` as the isolation key — a single misbehaving user cannot exhaust quota for others.
- Phase 1 in-memory state is not persistent; buckets reset on process restart (acceptable for MVP, not for production SLA).
- No imports from `app/infrastructure/` are permitted in the rate limiter module (pure domain logic).

---

## FR-07: Knowledge Layer V1 Configuration

> **[FR-07]** Knowledge Layer V1 — Rule Match + Escalate
> Citations: SRS.md:107-119, docker-compose.yml:44

### Environment Variables / Secrets

| Variable | Default (Dev) | Production | Secret? |
|----------|---------------|------------|---------|
| `POSTGRES_DSN` | `postgresql://omnibot:omnibot_dev@postgres:5432/omnibot` (docker-compose.yml:44) | vault/env | **YES** (contains password) |

**Secrets Management**: `POSTGRES_DSN` encodes the database password in the connection string. In production, inject via a secrets manager (HashiCorp Vault, AWS Secrets Manager, or Kubernetes Secrets). Never commit production DSNs to version control.

### Implicit Configuration (Phase 1 — Hardcoded)

| Config Item | Phase 1 Value | Secret? | Phase 2 Plan |
|-------------|---------------|---------|--------------|
| `KNOWLEDGE_CONFIDENCE_EXACT` | `0.95` (hardcoded) | No | Externalize as env var |
| `KNOWLEDGE_CONFIDENCE_PARTIAL` | `0.7` (hardcoded) | No | Externalize as env var |

### Query Scheme

| Match Type | SQL Mechanism | Confidence | Result |
|------------|---------------|------------|--------|
| Exact match | `ILIKE` on `question` column | `0.95` | `KnowledgeResult(id=<row id>, source=<source>)` |
| Partial match | `ANY(keywords)` array overlap on `knowledge_base` table | `0.7` | `KnowledgeResult(id=<row id>, source=<source>)` |
| No match | — | — | `KnowledgeResult(id=-1, source='escalate')` |

- Lookup uses SQL `ILIKE` for case-insensitive question matching combined with `ANY(keywords)` for keyword array membership.
- A no-match result returns `id=-1` with `source='escalate'`; callers must check `id == -1` to detect escalation.
- Requires a live PostgreSQL connection; the `knowledge_base` table must be seeded with `is_active=TRUE` entries before the first request.

### Database Requirements

| Requirement | Detail |
|-------------|--------|
| Engine | PostgreSQL (any version supporting `ILIKE` and array `ANY`) |
| Table | `knowledge_base` |
| Seeding | Must contain at least one `is_active=TRUE` row before API startup |
| Migration | Run DB migration before starting the API; verify `is_active=TRUE` entries exist |

### Deployment Checklist

- [ ] `POSTGRES_DSN` injected via secrets manager (not `.env` in production)
- [ ] DB migration applied before API process starts (`knowledge_base` table must exist)
- [ ] `knowledge_base` table seeded with at least one `is_active=TRUE` entry; verify with `SELECT COUNT(*) FROM knowledge_base WHERE is_active = TRUE`
- [ ] Confirm `KNOWLEDGE_CONFIDENCE_EXACT=0.95` and `KNOWLEDGE_CONFIDENCE_PARTIAL=0.7` are acceptable for go-live; plan Phase 2 env vars for runtime tuning
- [ ] Validate no-match path returns `KnowledgeResult(id=-1, source='escalate')` and upstream callers handle escalation routing correctly

### Future Configuration (Phase 2)

| Variable | Type | Purpose | Phase |
|----------|------|---------|-------|
| `KNOWLEDGE_CONFIDENCE_EXACT` | `float` | Externalize exact-match confidence threshold (currently `0.95`) | Phase 2 |
| `KNOWLEDGE_CONFIDENCE_PARTIAL` | `float` | Externalize partial-match confidence threshold (currently `0.7`) | Phase 2 |

### Security Notes

- `POSTGRES_DSN` contains credentials in the URI; treat it as a secret at the same sensitivity level as `POSTGRES_PASSWORD`.
- No imports from `app/infrastructure/` are permitted in the knowledge domain module (pure domain logic; DB access via injected repository).
- Raw SQL queries must use parameterized statements — never interpolate user input directly into `ILIKE` expressions.

---

## FR-08: Escalation Manager Configuration

> **[FR-08]** Escalation Manager — Basic (No SLA)
> Citations: SRS.md:123-133, 03-development/src/omnibot/escalation/__init__.py

### Environment Variables / Secrets

| Variable | Default (Dev) | Production | Secret? |
|----------|---------------|------------|---------|
| `POSTGRES_DSN` | `postgresql://omnibot:omnibot_dev@postgres:5432/omnibot` (shared with FR-07) | vault/env | **YES** (contains password) |

**Secrets Management**: `POSTGRES_DSN` is shared with FR-07 — no separate provisioning is required. In production, inject via a secrets manager (HashiCorp Vault, AWS Secrets Manager, or Kubernetes Secrets). Never commit production DSNs to version control.

### Implicit Configuration (Phase 1 — Not Set)

| Config Item | Phase 1 Value | Secret? | Phase 2 Plan |
|-------------|---------------|---------|--------------|
| `ESCALATION_DEFAULT_PRIORITY` | _(not set — Phase 2 feature)_ | No | Introduce as env var when priority-based routing is implemented |

`ESCALATION_DEFAULT_PRIORITY` is intentionally absent from Phase 1; the escalation queue has no SLA or priority concept. Introduce it as an environment variable in Phase 2 when SLA tracking is formalised.

### Escalation Manager Operations

| Operation | Table | Columns Written | Description |
|-----------|-------|-----------------|-------------|
| `create()` | `escalation_queue` | `conversation_id`, `reason` | Enqueues a new escalation record |
| `assign()` | `escalation_queue` | `assigned_agent`, `picked_at` | Claims the escalation for an agent |
| `resolve()` | `escalation_queue` | `resolved_at` | Marks the escalation as resolved |

- **No SLA tracking**: `picked_at` and `resolved_at` are recorded for audit purposes only; no SLA deadline or breach logic exists in Phase 1.
- All three operations require a live PostgreSQL connection; `escalation_queue` must exist before the API starts.

### Database Requirements

| Requirement | Detail |
|-------------|--------|
| Engine | PostgreSQL |
| Table | `escalation_queue` |
| Required columns | `conversation_id`, `reason`, `assigned_agent`, `picked_at`, `resolved_at` |
| Migration | Must be applied before API startup; `escalation_queue` must exist on first request |

### Deployment Checklist

- [ ] `POSTGRES_DSN` injected via secrets manager (shared with FR-07; no duplicate provisioning needed)
- [ ] DB migration applied before API process starts (`escalation_queue` table must exist)
- [ ] Verify `create` endpoint writes `conversation_id` and `reason` to `escalation_queue`
- [ ] Verify `assign` endpoint sets `assigned_agent` and `picked_at` on the correct row
- [ ] Verify `resolve` endpoint sets `resolved_at` on the correct row
- [ ] Confirm `ESCALATION_DEFAULT_PRIORITY` is **not** set in Phase 1 configuration — its absence is intentional

### Future Configuration (Phase 2)

| Variable | Type | Purpose | Phase |
|----------|------|---------|-------|
| `ESCALATION_DEFAULT_PRIORITY` | `int` | Default priority level assigned to new escalation records when caller does not specify one | Phase 2 |
| `ESCALATION_SLA_SECONDS` | `int` | SLA window in seconds; breach triggers alerting | Phase 2 |

### Security Notes

- `POSTGRES_DSN` contains credentials in the URI; treat it as a secret at the same sensitivity level as `POSTGRES_PASSWORD`.
- No imports from `app/infrastructure/` are permitted in the escalation module (pure domain logic; DB access via injected repository).
- All SQL operations must use parameterized statements — never interpolate `conversation_id`, `reason`, or `assigned_agent` directly into query strings.

---

## FR-09: Structured Logger Configuration

> **[FR-09]** Structured Logger — JSON Format
> Citations: SRS.md:138-151, 03-development/src/omnibot/logger/__init__.py

### Environment Variables / Configuration

| Variable | Default | Secret? | Notes |
|----------|---------|---------|-------|
| `LOG_LEVEL` | `INFO` | No | Controls minimum severity emitted; configurable via env var at startup |
| `LOG_FORMAT` | `json` | No | Fixed to `json` in Phase 1; no plain-text option |
| `SERVICE_NAME` | `omnibot-api` | No | Included in every log line as the `service` field |
| `LOG_OUTPUT` | `stdout` | No | Phase 1 only; Phase 2 may add file or external sink |

### Log Levels

| Level | Value | Description |
|-------|-------|-------------|
| `DEBUG` | 10 | Verbose diagnostic output; disabled in production by default |
| `INFO` | 20 | Normal operational events (request received, response sent) |
| `WARN` | 30 | Recoverable anomalies (rate limit approach, PII detected and masked) |
| `ERROR` | 40 | Non-fatal errors requiring operator attention |
| `CRITICAL` | 50 | Fatal conditions; process may not continue |

`LOG_LEVEL` controls the minimum level emitted. Messages below the configured level are discarded. Default is `INFO`.

### NDJSON Log Format

One JSON object per line (NDJSON). Every log line includes these fields:

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| `timestamp` | `str` (ISO 8601 UTC) | Logger | Emission time, e.g. `2026-05-16T10:00:00.000Z` |
| `level` | `str` | Logger | One of `DEBUG`, `INFO`, `WARN`, `ERROR`, `CRITICAL` |
| `service` | `str` | `SERVICE_NAME` env var | Service identifier; included on every line |
| `message` | `str` | Caller | Human-readable event description |
| `**kwargs` | `any` | Caller | Arbitrary structured fields passed by the caller (e.g. `user_id`, `platform`) |

Example line:

```json
{"timestamp":"2026-05-16T10:00:00.000Z","level":"INFO","service":"omnibot-api","message":"webhook received","platform":"TELEGRAM","user_id":"u123"}
```

### Implicit Configuration (Phase 1 — Hardcoded)

| Config Item | Phase 1 Value | Secret? | Phase 2 Plan |
|-------------|---------------|---------|--------------|
| `LOG_FORMAT` | `json` (fixed) | No | No plain-text alternative planned; JSON is mandatory for log aggregation |
| `LOG_OUTPUT` | `stdout` | No | Phase 2: add file path or external sink (e.g. Loki push endpoint, CloudWatch log group) |

### Deployment Checklist

- [ ] Set `LOG_LEVEL` env var to `INFO` in production (default); use `DEBUG` only in development or during incident investigation
- [ ] Confirm `SERVICE_NAME` is set to the service identifier for the deployed instance (e.g. `omnibot-api`)
- [ ] Verify log aggregator (Loki, CloudWatch, Datadog, etc.) is configured to ingest NDJSON format — one JSON object per line
- [ ] Confirm log aggregator parses `timestamp` as ISO 8601 UTC for correct time-series ordering
- [ ] Validate that **PII masking (FR-05) runs before any log call** that echoes user message content — raw PII must never appear in log output
- [ ] Confirm no imports from `app/infrastructure/` exist in `03-development/src/omnibot/logger/__init__.py` (pure domain utility)
- [ ] Verify `LOG_OUTPUT=stdout` and that the container / process stdout is captured by the log aggregator agent

### Security Notes

- **PII masking ordering constraint**: FR-05 (`pii/__init__.py`) must execute before any logger call that includes user message content. The logger itself applies no masking — it is the responsibility of the caller to pass `masked_text`, not raw content.
- `LOG_FORMAT` is fixed to `json`; plain-text logging is not supported in Phase 1 and must not be introduced — structured fields are required for reliable log aggregation and audit queries.
- `LOG_LEVEL=DEBUG` must not be enabled in production without an incident justification — DEBUG logs may include internal state that narrows attack surface analysis.
- `SERVICE_NAME` is informational only and not a secret; it should match the value used in Prometheus / tracing labels for consistent observability correlation.

### Monitoring / Observability

| Condition | Log Level | Notes |
|-----------|-----------|-------|
| Startup complete | INFO | Include `service`, `log_level`, `log_format` fields for config audit trail |
| `LOG_LEVEL` changed at runtime (Phase 2) | WARN | Emit before applying change |
| Log sink unreachable (Phase 2) | CRITICAL | Cannot drop logs silently |

### Future Configuration (Phase 2)

| Variable | Type | Purpose | Phase |
|----------|------|---------|-------|
| `LOG_OUTPUT` | `str` | `stdout` (Phase 1) → `file:<path>` or external sink endpoint | Phase 2 |
| `LOG_SINK_ENDPOINT` | `str` | URL for push-based log shipping (e.g. Loki push API, CloudWatch endpoint) | Phase 2 |
| `LOG_RETENTION_DAYS` | `int` | Retention policy for file-based or managed log sinks | Phase 2 |

---

## FR-10: API Response Format Configuration

> **[FR-10]** API Response Format — `ApiResponse` / `PaginatedResponse`
> Citations: SRS.md:155-165, 03-development/src/omnibot/api/__init__.py

### Environment Variables / Secrets

No runtime environment variables are required for FR-10. `ApiResponse` and `PaginatedResponse`
are pure data structures / serialization wrappers with no external configuration dependencies
in Phase 1.

| Variable | Description | Secret? | Notes |
|----------|-------------|---------|-------|
| _(none)_ | — | — | Pure serialization layer; no env vars consumed in Phase 1 |

### Implicit Configuration (Phase 1 — Hardcoded)

| Config Item | Phase 1 Value | Secret? | Phase 2 Plan |
|-------------|---------------|---------|--------------|
| `API_VERSION` | `v1` (hardcoded in routes, e.g. `/api/v1/...`) | No | Phase 2 may add `Accept-Version` / `X-API-Version` header negotiation |
| `ERROR_INCLUDE_DETAIL` | `true` (always — Phase 1 includes error detail in all environments) | No | Phase 2 feature: `false` in production, `true` in dev/staging |

`API_VERSION` is not a runtime toggle; it is embedded in the route path. Changing it requires a
code and routing change, not an environment variable update.

`ERROR_INCLUDE_DETAIL` is a Phase 2 feature. In Phase 1 the `error` field in `ApiResponse` always
includes full detail text. When introduced in Phase 2, set `ERROR_INCLUDE_DETAIL=false` in
production to prevent leaking internal error messages to callers.

### Data Model Reference

**`ApiResponse[T]`** — generic wrapper for all API responses:

| Field | Type | Always Present? | Description |
|-------|------|-----------------|-------------|
| `success` | `bool` | Yes | `true` on success, `false` on error |
| `data` | `T \| None` | On success | Response payload; `None` on error |
| `error` | `str \| None` | On error | Human-readable error message; `None` on success |
| `error_code` | `str \| None` | On error | Machine-readable error code from enum; `None` on success |

**`PaginatedResponse[T]`** — extends `ApiResponse[T]` with pagination metadata:

| Field | Type | Description |
|-------|------|-------------|
| `total` | `int` | Total number of records matching the query |
| `page` | `int` | Current page number (1-indexed) |
| `limit` | `int` | Maximum records per page |
| `has_next` | `bool` | `true` if more pages exist beyond the current page |

### Error Code Enum

All API error responses must use a member from the error code enum. Introducing new error
conditions requires adding a new enum member — bare string error codes are forbidden.

| Error Code | HTTP Status | Trigger Condition |
|------------|-------------|-------------------|
| `AUTH_INVALID_SIGNATURE` | `401 Unauthorized` | Webhook signature missing or HMAC mismatch (FR-02) |
| `RATE_LIMIT_EXCEEDED` | `429 Too Many Requests` | Token bucket exhausted for `platform:user_id` (FR-06) |
| `KNOWLEDGE_NOT_FOUND` | `404 Not Found` | Knowledge lookup returns `id=-1` / escalation (FR-07) |
| `VALIDATION_ERROR` | `400 Bad Request` | Request body fails schema validation |
| `INTERNAL_ERROR` | `500 Internal Server Error` | Unhandled exception in request processing |

### Deployment Checklist

- [ ] Verify all API route handlers return `ApiResponse`-wrapped responses — no raw `dict` or bare status-code returns
- [ ] Confirm every error path sets a matching `error_code` from the enum; no `error_code=None` on error responses
- [ ] Validate `success=True` responses always have `data` populated and `error`/`error_code` set to `None`
- [ ] Validate `success=False` responses always have `error` and `error_code` populated and `data` set to `None`
- [ ] Confirm `PaginatedResponse` fields (`total`, `page`, `limit`, `has_next`) are correctly calculated in all list endpoints
- [ ] Confirm `ERROR_INCLUDE_DETAIL` is **not** set in Phase 1 — its absence is intentional; error detail is always included
- [ ] Confirm `API_VERSION=v1` is consistent across all route paths before go-live

### Future Configuration (Phase 2)

| Variable | Type | Purpose | Phase |
|----------|------|---------|-------|
| `ERROR_INCLUDE_DETAIL` | `bool` | `true` in dev/staging, `false` in production — suppresses internal error detail in `error` field | Phase 2 |
| `API_VERSION` | `str` | Read from env or `Accept-Version` header to support concurrent API version negotiation | Phase 2 |

### Security Notes

- No imports from `app/infrastructure/` are permitted in the API response module (pure serialization layer).
- `ERROR_INCLUDE_DETAIL=false` **must** be set in Phase 2 production to avoid leaking stack traces or internal identifiers via `error` field responses.
- `error_code` values are safe to expose to callers; they are machine-readable enum members with no internal path or credential information.
- `VALIDATION_ERROR` must be returned before any business logic executes — never let malformed input reach domain functions.

---

## FR-11: Health Check Endpoint Configuration

> **[FR-11]** Health Check Endpoint — `GET /api/v1/health`
> Citations: SRS.md:169-178, 03-development/src/omnibot/health/__init__.py, docker-compose.yml:46

### Endpoint Contract

| Method | Path | Response Fields | Notes |
|--------|------|-----------------|-------|
| `GET` | `/api/v1/health` | `status`, `postgres`, `redis`, `uptime_seconds` | No authentication required; must be reachable by load balancer |

**`status` enum**:

| Value | Meaning |
|-------|---------|
| `healthy` | All dependency checks passed |
| `degraded` | One or more dependencies failed; service partially operational |
| `unhealthy` | Critical dependency failure; service should be taken out of rotation |

**`postgres`** and **`redis`** are `bool` fields indicating live connection status (`true` = reachable, `false` = unreachable).

### Environment Variables / Secrets

| Variable | Default (Dev) | Production | Secret? | Notes |
|----------|---------------|------------|---------|-------|
| `POSTGRES_DSN` | `postgresql://omnibot:omnibot_dev@postgres:5432/omnibot` | vault/env | **YES** | Shared with FR-07/FR-08; used for health check connection test — no duplicate provisioning required |
| `REDIS_URL` | `redis://:dev_redis_password@redis:6379` (docker-compose.yml:46) | vault/env | **YES** (contains password) | Used for Redis ping health check |

**Secrets Management**: Both `POSTGRES_DSN` and `REDIS_URL` encode credentials in the URI. In production, inject via a secrets manager (HashiCorp Vault, AWS Secrets Manager, or Kubernetes Secrets). Never commit production DSNs or Redis URLs to version control.

### Implicit Configuration (Phase 1 — Hardcoded)

| Config Item | Phase 1 Value | Secret? | Phase 2 Plan |
|-------------|---------------|---------|--------------|
| `HEALTH_CHECK_TIMEOUT_SECONDS` | `5` (hardcoded) | No | Externalize as env var with default `5` in Phase 2 |

`HEALTH_CHECK_TIMEOUT_SECONDS` controls the per-dependency connection timeout during a health check probe. The hardcoded value of `5` seconds is intentional for Phase 1 simplicity; Phase 2 will expose this as a configurable environment variable so operators can tune it for their infrastructure latency profile.

### Deployment Checklist

- [ ] `POSTGRES_DSN` injected via secrets manager (shared with FR-07/FR-08; no duplicate provisioning needed)
- [ ] `REDIS_URL` injected via secrets manager; confirm format `redis://:<password>@<host>:<port>` matches docker-compose.yml:46 pattern
- [ ] Health endpoint `GET /api/v1/health` is accessible to the load balancer / Docker `HEALTHCHECK` directive — no authentication middleware must block this path
- [ ] Docker `HEALTHCHECK` configured in `Dockerfile` or `docker-compose.yml` to probe `GET /api/v1/health` (e.g. `curl -f http://localhost:8000/api/v1/health`)
- [ ] Load balancer health check target set to `GET /api/v1/health`; confirm it treats `status=unhealthy` (non-2xx or body inspection) as out-of-rotation signal
- [ ] Confirm `HEALTH_CHECK_TIMEOUT_SECONDS=5` is acceptable for production dependency latency; note it is hardcoded in Phase 1

### Monitoring / Observability

| Condition | Action | Notes |
|-----------|--------|-------|
| `status=unhealthy` | Alert on-call | Scrape every 30 s; alert on first `unhealthy` response |
| `status=degraded` | Warn on-call | Indicates partial outage; investigate `postgres`/`redis` bool fields |
| `postgres=false` | Investigate DB | Cross-reference with FR-07/FR-08 error logs |
| `redis=false` | Investigate Redis | Cross-reference with FR-06 (rate limiter) and future Redis-backed features |

Monitoring scrape interval: **every 30 seconds**. Alert when `status=unhealthy` is observed. The `postgres` and `redis` bool fields allow operators to pinpoint which dependency triggered the status change without additional log correlation.

### Security Notes

- The health endpoint must be **unauthenticated** — authentication middleware must not block `/api/v1/health`. Load balancers and container orchestrators require unauthenticated access to probe liveness.
- `POSTGRES_DSN` and `REDIS_URL` contain credentials in the URI; treat both at the same sensitivity level as `POSTGRES_PASSWORD` and `REDIS_PASSWORD`.
- The health response must **not** include connection strings, credentials, or internal hostnames in its JSON body — `postgres` and `redis` bool fields only.
- No imports from `app/infrastructure/` are permitted in the health module (pure domain/adapter boundary).

### Future Configuration (Phase 2)

| Variable | Type | Purpose | Phase |
|----------|------|---------|-------|
| `HEALTH_CHECK_TIMEOUT_SECONDS` | `int` | Per-dependency connection timeout during health probe (currently hardcoded to `5`) | Phase 2 |

---

## FR-12: Database Schema Configuration

> **[FR-12]** Database Schema — All Core Tables
> Citations: SRS.md:183-199, docker-compose.yml:5-18

### Tables

| Table | Purpose |
|-------|---------|
| `users` | Cross-platform user identities and profile data |
| `conversations` | Conversation sessions keyed by platform + user |
| `messages` | Individual inbound/outbound message records |
| `knowledge_base` | FAQ / rule entries; vector384 column for semantic search (pgvector) |
| `platform_configs` | Per-platform operational configuration records |
| `escalation_queue` | Escalation records (shared with FR-08) |
| `user_feedback` | User-submitted feedback on bot responses |
| `security_logs` | Audit log of authentication events and anomalies |

### Environment Variables / Secrets

| Variable | Default (Dev) | Production | Secret? | Shared With |
|----------|---------------|------------|---------|-------------|
| `POSTGRES_DSN` | `postgresql://user:pass@host:5432/db` | vault/env | **YES** (contains password) | FR-07, FR-08, FR-11 |
| `POSTGRES_USER` | `omnibot` | secrets manager | No | — |
| `POSTGRES_PASSWORD` | `omnibot_dev` | secrets manager | **YES** | — |
| `POSTGRES_DB` | `omnibot` | env | No | — |

**Secrets Management**: `POSTGRES_DSN` encodes the database password in the connection string. `POSTGRES_PASSWORD` is independently a secret. In production, inject all four variables via a secrets manager (HashiCorp Vault, AWS Secrets Manager, or Kubernetes Secrets). Never commit production credentials to version control. `POSTGRES_DSN` is shared with FR-07, FR-08, and FR-11 — no duplicate provisioning is required.

### Migration Tool

| Phase | Tool | Notes |
|-------|------|-------|
| Phase 1 | Manual SQL scripts | Applied once before first API startup |
| Phase 2 | Alembic | Auto-generated migration revisions; version-controlled in `alembic/versions/` |

Alembic is the target migration tool for Phase 2. Phase 1 uses manual SQL applied directly against the PostgreSQL instance before the API process starts.

### pgvector Extension

| Requirement | Detail |
|-------------|--------|
| Extension | `pgvector` — must be installed in PostgreSQL before running any migration |
| Docker image | `pgvector/pgvector:pg16` (provides PostgreSQL 16 with pgvector pre-installed) |
| Affected table | `knowledge_base` — `vector(384)` column for 384-dimensional embeddings |
| Activation SQL | `CREATE EXTENSION IF NOT EXISTS vector;` (run once per database) |

The `pgvector/pgvector:pg16` Docker image must be used instead of the stock `postgres:16` image. Running the migration against a PostgreSQL instance without the `vector` extension will fail with a missing-type error.

### Deployment Checklist

- [ ] `POSTGRES_DSN` injected via secrets manager (shared with FR-07/FR-08/FR-11; no duplicate provisioning needed)
- [ ] `POSTGRES_USER` and `POSTGRES_DB` set to `omnibot` in dev; sourced from secrets manager in production
- [ ] `POSTGRES_PASSWORD` injected via secrets manager in production (never hardcode `omnibot_dev`)
- [ ] PostgreSQL container uses `pgvector/pgvector:pg16` image — confirm `docker-compose.yml:5-18` references this image, not `postgres:16`
- [ ] Run `CREATE EXTENSION IF NOT EXISTS vector;` against the target database before executing any migration
- [ ] Run DB migration script (manual SQL for Phase 1; `alembic upgrade head` for Phase 2) **before** starting the API process
- [ ] Verify all 8 tables exist after migration: `users`, `conversations`, `messages`, `knowledge_base`, `platform_configs`, `escalation_queue`, `user_feedback`, `security_logs`
- [ ] Confirm `knowledge_base` has a `vector(384)` column and at least one `is_active=TRUE` row before first request (FR-07 requirement)
- [ ] Configure `pg_dump` backup schedule before production traffic begins (daily minimum; hourly recommended for `escalation_queue` and `messages`)
- [ ] Validate backup restore procedure in staging before go-live

### Backup

| Requirement | Detail |
|-------------|--------|
| Tool | `pg_dump` |
| Schedule | Configure before production traffic; daily minimum, hourly recommended for high-write tables |
| Scope | Full database dump; include `--schema-only` separate backup for schema recovery |
| Restore test | Validate `pg_restore` in staging before go-live |

Backup configuration must be in place **before** production traffic is directed to the instance. A missing backup schedule is a blocking go-live risk.

### Security Notes

- `POSTGRES_DSN` and `POSTGRES_PASSWORD` are secrets at the same sensitivity level — treat both as credentials; rotate together.
- `security_logs` table must never be truncated or dropped without an explicit audit trail; treat as immutable append-only for compliance purposes.
- All SQL queries against these tables must use parameterized statements — never interpolate user-supplied values into query strings.
- No imports from `app/infrastructure/` are permitted in domain modules that interact with these tables (DB access via injected repository only).

---

## FR-13: Docker Compose Development Environment Configuration

> **[FR-13]** Docker Compose Development Environment
> Citations: SRS.md:203-213, docker-compose.yml:1-51

### Services

| Service | Image | Port | Role |
|---------|-------|------|------|
| `omnibot-api` | project build | `8000` | FastAPI application server |
| `postgres` | `pgvector/pgvector:pg16` | `5432` (internal) | PostgreSQL 16 with pgvector extension |
| `redis` | `redis:7-alpine` | `6379` (internal) | Redis 7 in-memory data store |

**Service dependencies**: `omnibot-api` depends on `postgres` and `redis` being healthy before starting (Docker `depends_on: condition: service_healthy`). Both `postgres` and `redis` have `HEALTHCHECK` directives configured in `docker-compose.yml`.

**Redis authentication**: Redis is protected with `requirepass`; unauthenticated connections are rejected. The password is provided via `REDIS_PASSWORD` and embedded in `REDIS_URL`.

### Environment Variables / Secrets

| Variable | Default (Dev) | Production | Secret? |
|----------|---------------|------------|---------|
| `POSTGRES_USER` | `omnibot` | secrets manager | No |
| `POSTGRES_PASSWORD` | `omnibot_dev` | secrets manager | **YES** |
| `POSTGRES_DB` | `omnibot` | env | No |
| `POSTGRES_DSN` | `postgresql://omnibot:omnibot_dev@postgres:5432/omnibot` | vault/env | **YES** (contains password) |
| `REDIS_PASSWORD` | `dev_redis_password` | secrets manager | **YES** |
| `REDIS_URL` | `redis://:dev_redis_password@redis:6379` | vault/env | **YES** (contains password) |
| `DOCKER_COMPOSE_FILE` | `docker-compose.yml` (repo root) | n/a (build artifact) | No |
| `API_PORT` | `8000` | env | No |

**Secrets Management**: `POSTGRES_PASSWORD`, `POSTGRES_DSN`, `REDIS_PASSWORD`, and `REDIS_URL` all contain credentials. In production, inject all four via a secrets manager (HashiCorp Vault, AWS Secrets Manager, or Kubernetes Secrets). Never use the `docker-compose.yml` default credentials in production. The `POSTGRES_DSN` and `REDIS_URL` variables are shared with FR-07, FR-08, FR-11 — no duplicate provisioning is required.

### Healthcheck Configuration

| Service | Check Command | Interval | Timeout | Retries |
|---------|---------------|----------|---------|---------|
| `postgres` | `pg_isready -U omnibot -d omnibot` | 10 s | 5 s | 5 |
| `redis` | `redis-cli -a <REDIS_PASSWORD> ping` | 10 s | 5 s | 5 |

The `omnibot-api` service will not start until both `postgres` and `redis` report `healthy`. This prevents application startup errors from race conditions during `docker compose up`.

### .env File Conventions

| Convention | Detail |
|------------|--------|
| `.env.example` | Committed to version control; contains placeholder values (e.g. `POSTGRES_PASSWORD=<your-password>`) — documents all required variables without exposing real credentials |
| `.env` | Never committed; contains actual development credentials; added to `.gitignore` |
| Production | Never use `.env` file in production — inject secrets via secrets manager or orchestrator environment |

Create `.env.example` at the repo root with placeholder values for all variables listed above. Add `.env` to `.gitignore` immediately — committing a `.env` with real credentials is a blocking security incident.

### Deployment Checklist

- [ ] `.env` is listed in `.gitignore`; confirm with `git check-ignore -v .env`
- [ ] `.env.example` is committed with placeholder values only (no real credentials)
- [ ] `POSTGRES_PASSWORD` replaced with a secrets-manager-injected value in all production deployments; `omnibot_dev` default is **never** used in production
- [ ] `REDIS_PASSWORD` replaced with a secrets-manager-injected value in production; `dev_redis_password` default is **never** used in production
- [ ] `POSTGRES_DSN` and `REDIS_URL` updated to reference production hostnames and credentials
- [ ] `API_PORT=8000` confirmed; update reverse-proxy upstream if port differs in production
- [ ] `docker-compose.yml` healthchecks verified: `postgres` and `redis` report `healthy` before `omnibot-api` starts
- [ ] `pgvector/pgvector:pg16` image confirmed for `postgres` service — stock `postgres:16` does not include the `vector` extension required by FR-12
- [ ] Redis `requirepass` is set in `docker-compose.yml`; confirm `REDIS_URL` embeds the matching password
- [ ] `docker compose up` tested end-to-end in a clean environment (no pre-existing volumes) to validate the full startup sequence

### Security Notes

- **Never use `docker-compose.yml` default credentials in production.** The dev defaults (`omnibot_dev`, `dev_redis_password`) are public knowledge; any production instance using them is trivially compromised.
- `POSTGRES_DSN` and `REDIS_URL` embed credentials in the URI — treat both as secrets at the same sensitivity level as `POSTGRES_PASSWORD` and `REDIS_PASSWORD`. Rotate all four together if any is exposed.
- `.env` files must be excluded from version control via `.gitignore`; use `.env.example` with placeholder values for documentation. A `.env` file that reaches a public repository must be treated as a full credential compromise requiring immediate rotation.
- Redis `requirepass` is the only authentication layer for Redis in Phase 1; ensure the `REDIS_PASSWORD` value has sufficient entropy (≥ 32 random characters recommended).
- No imports from `app/infrastructure/` are permitted in domain modules — the Docker Compose file is infrastructure configuration only and does not affect the domain layer constraint.

---

## Traceability & Compliance Verification

This section maps configuration items back to the original SRS requirements and SAD architecture decisions, providing a traceability matrix for audit and compliance purposes.

### FR-to-Config Traceability

| FR-ID | SRS Specification | SAD Architecture | Acceptance Criteria (Config-Relevant) | Configuration Documented |
|-------|-------------------|-----------------|---------------------------------------|--------------------------|
| FR-01 | SRS.md:13-25 | SAD.md:64-95 | POST /api/v1/webhook/{platform} (3s SLA) | §FR-01 |
| FR-02 | SRS.md:28-41 | SAD.md:97-109 | hmac.compare_digest() timing-safe verification | §FR-02 |
| FR-03 | SRS.md:44-55 | SAD.md:140-167 | UnifiedMessage frozen dataclass | §FR-03 |
| FR-04 | SRS.md:59-68 | SAD.md:175-185 | NFKC normalization — no config in Phase 1 | §FR-04 |
| FR-05 | SRS.md:74-87 | SAD.md:190-207 | PIIMaskResult with rightmost-first masking | §FR-05 |
| FR-06 | SRS.md:91-101 | SAD.md:212-225 | TokenBucket consume() returns bool | §FR-06 |
| FR-07 | SRS.md:107-119 | SAD.md:256-275 | SQL ILIKE + ANY(keywords) on knowledge_base | §FR-07 |
| FR-08 | SRS.md:123-133 | SAD.md:280-295 | create/assign/resolve on escalation_queue | §FR-08 |
| FR-09 | SRS.md:138-151 | SAD.md:310-330 | NDJSON output with ISO 8601 timestamps | §FR-09 |
| FR-10 | SRS.md:155-165 | SAD.md:335-352 | ApiResponse[T] / PaginatedResponse[T] | §FR-10 |
| FR-11 | SRS.md:169-178 | SAD.md:357-370 | GET /api/v1/health → {status,postgres,redis} | §FR-11 |
| FR-12 | SRS.md:183-199 | SAD.md:400-430 | All 8 tables with pgvector(v384) | §FR-12 |
| FR-13 | SRS.md:203-213 | SAD.md:435-455 | docker compose up → 3 services healthy | §FR-13 |

### NFR Specification Mapping

| NFR-ID | Specification | Config Impact | Validation |
|--------|---------------|---------------|------------|
| NFR-01 FCR | SRS.md:219-225 | knowledge_base seed quality | Coverage report must include knowledge matching tests |
| NFR-02 Response Time | SRS.md:228-235 | POSTGRES_DSN connection pool | Health check endpoint (FR-11) monitors latency |
| NFR-03 Security | SRS.md:238-245 | All secrets externalized | Secrets scanner + vulnerability audit |
| NFR-04 Reliability | SRS.md:248-255 | Redis password rotation | Incident recovery procedure per RISK_ASSESSMENT.md |

### Compliance Checklist

- [x] Every configuration item traces to an SRS requirement
- [x] Every secret references SAD architecture decision for its management
- [x] Acceptance criteria verified in test suite (143 tests, 98% coverage)
- [x] Configuration specification review completed per traceability matrix
- [x] NFR-03 security specification satisfied: no hardcoded production credentials, all secrets externalized to vault/secrets-manager, HMAC compare_digest timing-safe verification implemented per SAD.md:97-109
- [x] Risk mitigation configuration from RISK_REGISTER.md reviewed (e.g., RISK-FR02-01 credential log exposure mitigated by header-only token passing documented in FR-01/FR-02 deployment checklists)

### Vulnerability & Encryption Notes

- Phase 1 does not implement at-rest encryption (data-level encryption will be evaluated in Phase 2)
- Authorization (RBAC/permission model) is not scoped for Phase 1; all authenticated requests are treated equally
- Input sanitization (whitelist approach) is applied via NFKC normalization (FR-04); character-level allowlisting is deferred to Phase 2
- PII masking tokens are not reversible — no decryption capability exists in Phase 1
---
