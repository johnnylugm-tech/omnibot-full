# Architecture Decision Records — OmniBot Phase 2

> **Project**: OmniBot — 多平台客服機器人
> **Phase**: 2 (智慧化 + 安全強化)
> **Version**: 2.0
> **Date**: 2026-05-17
> **Authored by**: Agent A (ARCHITECT)
> **Input**: SRS.md v2.0, SAD.md v2.0, ADR.md v1.0
> **Supersedes**: 02-architecture/adr/ADR.md Phase 1 v1.0

---

## Phase 1 ADRs (Preserved)

> ADR-001 through ADR-012 were authored in Phase 1 and remain valid. They are preserved verbatim below.

---

## ADR-001: FastAPI as Web Framework

### Status
Accepted

### Context
OmniBot must handle concurrent webhook requests from Telegram and LINE with a p95 response latency of < 3.0 s (NFR-02). Request handlers must validate JSON bodies and produce typed responses. The team is Python-only (CONSTRAINTS.md §6).

Alternatives evaluated: Flask (synchronous by default), Django REST Framework (heavier ORM coupling), Starlette (bare, no validation layer).

### Decision
Use **FastAPI ≥ 0.110** with Pydantic v2 for validation and response serialization.

### Rationale
- Native `asyncio` support: all handlers are `async def`; no event loop blocking in request path
- Pydantic v2 validates incoming webhook bodies at the boundary (FR-10 acceptance criteria)
- Auto-generated OpenAPI schema aids future integration testing
- FastAPI's dependency injection (`Depends()`) enforces SignatureVerifier before any handler body executes, ensuring 100% webhook verification (NFR-04)

### Consequences
- **Positive**: Uniform async model; Pydantic v2 catches malformed payloads at boundary; OpenAPI docs free
- **Negative**: Heavier dependency tree vs. Flask; Pydantic v2 breaking changes from v1 require careful migration if existing code exists

---

## ADR-002: PostgreSQL 16 + pgvector as Single Database

### Status
Accepted

### Context
Phase 1 requires relational tables (users, conversations, messages, knowledge_base, escalation_queue, security_logs, etc.) per FR-12. Phase 2 requires vector similarity search (RAG Layer 2). Two options: (1) PostgreSQL + separate vector database (Pinecone, Weaviate, Qdrant); (2) PostgreSQL + pgvector extension.

### Decision
Use **PostgreSQL 16** with the **pgvector** extension for both relational storage and future vector search. No external vector database in Phase 1 or Phase 2.

### Rationale
- Single infrastructure dependency: one database covers all persistence needs across phases
- pgvector supports `vector(384)` columns — `knowledge_base.embeddings` pre-provisioned for Phase 2 without `ALTER TABLE` (FR-12 acceptance criteria: "avoid subsequent ALTER TABLE")
- Managed PostgreSQL services (Supabase, Neon, RDS) natively support pgvector
- Phase 1 load is not vector-search-bound; ivfflat index deferred to Phase 2

### Consequences
- **Positive**: No Pinecone/Weaviate subscription; single connection pool; schema migrations stay in one place
- **Negative**: Vector search performance limited to single-node Postgres at scale; ivfflat index must be added before vector queries in Phase 2

---

## ADR-003: Redis 7 for Rate Limiter State

### Status
Accepted

### Context
FR-06 requires per-user per-platform rate limiting (default 100 rps). Options: (1) In-process Python dict; (2) Redis-backed token bucket.

### Decision
Use **Redis 7-alpine** as the persistent store for token bucket state (key: `ratelimit:{platform}:{user_id}`).

### Rationale
- In-process dict does not survive process restart and cannot be shared across multiple worker processes/replicas
- Redis INCR + EXPIRE operations are atomic — no race condition between token check and deduction
- Redis already required by Phase 2 (caching, session state); no new infrastructure in Phase 1
- Failure policy: fail-open (allow-all) is preferred over fail-closed on Redis unavailability because a Redis outage during peak load should not block all legitimate user messages in Phase 1 MVP; the rate-limit bypass risk is accepted until HA Redis is provisioned in Phase 3

### Consequences
- **Positive**: Rate limit state persists across restarts; correct under horizontal scaling; sub-millisecond per check
- **Negative**: Adds Redis as a required infrastructure dependency; Redis outage disables rate limiting (fail-open, not fail-safe)

---

## ADR-004: Frozen Dataclasses for UnifiedMessage / UnifiedResponse

### Status
Accepted

### Context
All downstream modules (InputSanitizerL2, PIIMaskerL4, RateLimiter, KnowledgeRepository) consume the normalized message object. If the object is mutable, any module can accidentally modify fields that another module relies on, causing subtle bugs.

Alternatives evaluated: Pydantic BaseModel (mutable by default, requires explicit `frozen=True` config in v2); NamedTuple (immutable, less expressive for Optional fields); plain dict (no type safety).

### Decision
Use Python `@dataclass(frozen=True)` for `UnifiedMessage` and `UnifiedResponse`. `reply_token: Optional[str] = None` declared last to satisfy Python's default-after-non-default field ordering rule.

### Rationale
- `frozen=True` raises `FrozenInstanceError` on any mutation attempt — catches bugs at development time
- Hashable: can be used as dict key or in sets without custom `__hash__`
- Zero external dependencies (stdlib `dataclasses`)
- Thread-safe by construction: no lock required when passing across async boundaries

### Consequences
- **Positive**: Immutable messages prevent inter-module data corruption; hashable for caching future
- **Negative**: Slight verbosity vs. Pydantic models; updating a field requires `dataclasses.replace()` instead of assignment

---

## ADR-005: VERIFIERS Dict Registry for Webhook Signature Extensibility

### Status
Accepted

### Context
FR-02 requires platform-specific HMAC signature verification. FR-02 acceptance criteria: "支援新增平台驗證器（`VERIFIERS` dict 註冊）". Phase 2 adds Messenger and WhatsApp adapters, each with different signature schemes.

### Decision
Implement `SignatureVerifier` as a single module with a `VERIFIERS: dict[Platform, Callable]` registry. Each platform's verification logic is a callable registered at module load time. `verify(platform, headers, body)` dispatches to the correct callable.

### Rationale
- Open for extension (new platform → add entry to dict), closed for modification (no change to existing verification logic)
- All verifiers in one auditable location — security review only needs to inspect one module
- Each callable can be independently unit-tested

### Consequences
- **Positive**: Adding Messenger/WhatsApp in Phase 2 requires zero changes to SignatureVerifier core
- **Negative**: All verifiers must use `hmac.compare_digest()` by convention — no static enforcement; enforced by code review

---

## ADR-006: SQL Rule Matching (Layer 1) with Fixed Confidence Thresholds

### Status
Accepted

### Context
FR-07 requires a knowledge query engine. Phase 1 budget does not justify LLM per-request cost. Options: (1) SQL ILIKE rule match; (2) TF-IDF vector match; (3) LLM generation immediately.

### Decision
Implement **Layer 1 SQL rule matching** using `ILIKE` on `knowledge_base.question` and `ANY(keywords)` array search. Fixed confidence scores: exact match = 0.95, partial match = 0.70. Threshold: score **>= 0.70** → reply; score **< 0.70** → escalate (boundary score 0.70 treated as partial-match/reply, consistent with FR-07 intent that only scores strictly below the threshold escalate). Tie-breaking by `version DESC`.

SQL query pattern (parameterized; `$1` bound to the search term at runtime — no string interpolation per SAD.md §2.3.1):
`SELECT ... WHERE (question ILIKE '%' || $1 || '%' OR $1 = ANY(keywords)) AND is_active = TRUE ORDER BY version DESC LIMIT 1`

Note: parentheses around the OR clause are required because AND binds tighter than OR; without them, the `is_active = TRUE` filter only applies to the `ANY(keywords)` branch, allowing inactive rows through the ILIKE path.

### Rationale
- Zero LLM cost per query in Phase 1 (LLM cost ~$0.002–$0.01/query)
- SQL ILIKE is deterministic and auditable — knowledge base authors can predict which queries will match
- pgvector column is pre-provisioned for Phase 2 Layer 2 upgrade without schema change
- Fixed confidence scores avoid the complexity of calibrating a scoring model in Phase 1

### Consequences
- **Positive**: Zero per-query LLM cost; deterministic matching; transparent to knowledge base authors
- **Negative**: No semantic understanding — "退款" and "退貨" will not match each other; escalation rate expected to be higher than Phase 2 (RAG) baseline; GAP-02 (tie-breaking for identical confidence) deferred to Phase 3

---

## ADR-007: Stdlib re for PII Masking (No External NLP)

### Status
Accepted

### Context
FR-05 requires masking of Taiwan-format phone numbers, email addresses, and postal addresses. Options: (1) stdlib `re` regex; (2) spaCy NER; (3) Presidio (Microsoft PII detection).

### Decision
Use **Python stdlib `re`** for all PII pattern matching. Three sequential regex passes: email → phone → address (inter-type precedence per GAP-03). Replacement is rightmost-first within each pass.

### Rationale
- Zero additional dependencies — no spaCy model download, no Presidio service
- Patterns are short, auditable, and reviewable by non-ML team members
- Taiwan-specific formats (country code, address structure) are well-defined by regex; NER would introduce false negatives for short messages
- Performance: regex is sub-millisecond per message; NER would add 10–100 ms startup overhead

### Consequences
- **Positive**: No model loading overhead; fully auditable; no internet/model dependency
- **Negative**: No semantic PII detection (e.g., informal address phrasing may escape regex); extends to only pre-defined patterns — novel PII formats not covered until regex is updated

---

## ADR-008: ConversationContext as Explicit Pipeline Stage

### Status
Accepted

### Context
Every request needs a `unified_user_id` (UUID from the `users` table) and a `conversation_id` (from `conversations` table) before downstream modules process the message. These could be embedded inside each adapter (TelegramAdapter, LINEAdapter) or extracted into a shared module.

### Decision
Implement **ConversationContext** as an explicit pipeline stage between PlatformAdapter output and InputSanitizerL2. It performs the `users` upsert and `conversations` create/reuse atomically, injecting both IDs into the pipeline.

### Rationale
- Prevents duplication: without ConversationContext, both TelegramAdapter and LINEAdapter would need identical DB upsert logic
- Clear separation: adapters own parsing (platform → UnifiedMessage); ConversationContext owns identity resolution
- Testable independently: ConversationContext unit tests only need to mock asyncpg; adapter tests mock only the HTTP parsing

### Consequences
- **Positive**: No code duplication across adapters; identity resolution is a single auditable location; adapters remain slim
- **Negative**: Adds one DB round-trip per request (the upsert); mitigated by asyncpg connection pooling and the 3 s latency budget

---

## ADR-009: Docker Compose v2 for Development Environment (Single-Node)

### Status
Accepted

### Context
FR-13 requires a one-command development environment. Phase 3 considers Kubernetes. Options: (1) Docker Compose v2; (2) Kubernetes (minikube/kind); (3) bare-metal scripts.

### Decision
Use **Docker Compose v2** with three services: `omnibot-api`, `postgres` (pgvector/pg16), `redis` (7-alpine). Service dependency order: postgres[healthy] + redis[healthy] → omnibot-api.

### Rationale
- `docker compose up` provides a complete environment in one command — matches the FR-13 acceptance criteria directly
- Healthchecks (`pg_isready`, `redis-cli ping`) ensure API container does not start before dependencies are ready, preventing connection-refused errors on startup
- Docker Compose topology is conceptually similar to Kubernetes deployment manifests — migration to Phase 3 k8s is a re-expression of the same service graph, not a redesign

### Consequences
- **Positive**: One-command environment; healthcheck-gated startup; no Kubernetes cluster required for development
- **Negative**: Single-node only; no horizontal scaling in dev; production deployment must use a different orchestration approach

---

## ADR-010: asyncpg + aioredis for Database Clients (No ORM)

### Status
Accepted

### Context
CONSTRAINTS.md §1 specifies: "no synchronous ORM in request path". Options: (1) asyncpg (raw async PostgreSQL); (2) SQLAlchemy 2.0 async (ORM); (3) Tortoise-ORM.

### Decision
Use **asyncpg** for PostgreSQL access and **aioredis** for Redis access. Both initialized as connection pools in the FastAPI `lifespan` context manager. No ORM.

### Rationale
- asyncpg is the fastest pure-Python async PostgreSQL driver (benchmarks: 3–5× faster than psycopg2 in async mode)
- SQL queries in this system are simple (ILIKE, upsert, insert) — an ORM layer adds complexity without benefit
- No ORM means SQL is explicit, readable, and independently reviewable by database administrators
- Both pool lifetimes are tied to the FastAPI `lifespan` context — no resource leak on shutdown

### Consequences
- **Positive**: Maximum async performance; no ORM migration overhead; SQL is the interface
- **Negative**: No automatic schema migration (requires Alembic or manual scripts); SQL must be written for each query (no `session.query()` convenience)

---

## ADR-011: Alembic for Database Schema Migration

### Status
Accepted

### Context
ADR-010 adopts asyncpg with no ORM, which means there is no auto-migration mechanism. The database schema includes 8 tables in Phase 1, with Phase 2 adding an ivfflat vector index and activating the `sla_deadline` column. A version-controlled migration approach is required to evolve the schema safely across phases. Alternatives: Flyway (JVM), Liquibase (JVM/XML), raw SQL scripts with manual versioning, Yoyo-migrations.

### Decision
Use **Alembic** with autogenerate disabled (manual migration scripts). SQLAlchemy Core metadata is used only for Alembic's connection interface; no ORM models are defined.

### Rationale
- Python-native: no JVM dependency; consistent with the Python-only constraint (CONSTRAINTS.md §6)
- Works with asyncpg via SQLAlchemy's async engine adapter — migration scripts use `AsyncConnection.run_sync()` so Alembic's synchronous script runner can drive asyncpg; `env.py` must configure an async engine and call `context.run_migrations()` via `run_sync()`
- Version-controlled migration history in `alembic/versions/` enables rollback and CI validation
- Autogenerate disabled because pgvector column types (`vector(384)`) are not recognized by SQLAlchemy's reflection layer — manual scripts are explicit and correct

### Consequences
- **Positive**: Explicit migration history; rollback support; CI can run `alembic upgrade head` to validate schema state
- **Negative**: Migration scripts must be written manually per schema change; autogenerate reliability is low for pgvector column types

---

## ADR-012: Secret Management via Environment Variables (Phase 1)

### Status
Accepted

### Context
FR-02 HMAC secrets (Telegram bot token, LINE channel_secret), PostgreSQL password, and Redis password must never be hardcoded in source. Alternatives: HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager, `.env` file committed to repository.

### Decision
Use **environment variables** injected at container start. A `.env` file (gitignored) holds local development values. `docker-compose.yml` references `${VAR}` syntax. Secrets rotate without rebuilding the Docker image.

### Rationale
- Zero additional infrastructure for Phase 1 MVP — no Vault or cloud secrets service required
- Docker Compose natively supports `${VAR}` substitution from `.env` files
- Environment variables are the de-facto standard for 12-factor apps; compatible with any cloud platform's secrets injection (GCP Cloud Run, AWS ECS, Railway)
- A committed `.env.example` with placeholder values documents the required variable names without exposing values (e.g. `TELEGRAM_BOT_TOKEN={your_token}`, `LINE_CHANNEL_SECRET={your_channel_secret}`)

### Consequences
- **Positive**: Simple; no extra service; compatible with any cloud runtime; secrets rotate without image rebuild
- **Negative**: Secrets visible in process environment (e.g., `ps aux` or `/proc/PID/environ` leakage); Phase 3 should migrate to Vault or cloud-native secrets manager for production hardening

---

## Phase 2 ADRs

> ADR-013 through ADR-024 are new for Phase 2 and build on Phase 1 foundations.

---

## ADR-013: Messenger + WhatsApp Adapters — VERIFIERS Dict Extension

### Status
Accepted

### Context
FR-14 requires Messenger and WhatsApp webhook support in addition to Phase 1 Telegram and LINE. Both new platforms use HMAC-SHA256 verification but with different header formats (`X-Hub-Signature-256`). The VERIFIERS dict registry pattern (ADR-005) was designed for this extension. Each platform also requires a dedicated Adapter class to parse platform-specific webhook payloads into `UnifiedMessage`.

Alternatives evaluated: (1) Generic webhook adapter with platform-specific parser plugins; (2) Separate FastAPI route handlers with inline verification; (3) Extend VERIFIERS dict + dedicated Adapter classes.

### Decision
Add `MessengerAdapter` and `WhatsAppAdapter` as dedicated Adapter classes, each with their own `POST` route handler. Extend `VERIFIERS` dict with two new entries: `"messenger"` and `"whatsapp"`. Both use the pattern `sha256=` + `HMAC-SHA256(app_secret, body).hexdigest()` compared against `X-Hub-Signature-256` header via `hmac.compare_digest()`. New `Platform` enum values: `Platform.MESSENGER`, `Platform.WHATSAPP`.

### Rationale
- ADR-005 VERIFIERS dict was explicitly designed for this: each new platform adds one callable entry with zero changes to `SignatureVerifier.verify()`
- Dedicated Adapter classes keep parsing logic isolated — Messenger and WhatsApp share Graph API infrastructure but differ in payload structure (`recipient.id` vs `to`), route paths, and reply endpoints
- Uniform 3 s webhook response deadline applies across all 4 platforms, enforced by async handler pattern from Phase 1
- Messenger and WhatsApp reply via `POST` to `graph.facebook.com/v18.0/`, but to different endpoints (`{PAGE_ID}/messages` vs `{PHONE_NUMBER_ID}/messages`) — separate `send_reply()` implementations per adapter

### Consequences
- **Positive**: 4-platform coverage completed; VERIFIERS dict pattern validated; each Adapter independently testable; `ReplyDispatcher` extends cleanly with per-adapter `send_reply()` methods
- **Negative**: Messenger and WhatsApp share Facebook Graph API infrastructure — token management must handle two separate credentials (`PAGE_ACCESS_TOKEN` and `WHATSAPP_ACCESS_TOKEN`); Graph API version coupling across two adapters

---

## ADR-014: Prompt Injection Defense L3 — Pattern Matching vs ML-Based Detection

### Status
Accepted

### Context
FR-15 requires detection of prompt injection attacks at the input boundary (Layer 3). The system must detect 10 specific injection patterns with >= 95% block rate against a red-team test suite of 100 malicious inputs (NFR-12). Options: (1) Regex pattern matching with stdlib `re`; (2) ML-based classifier (e.g., fine-tuned BERT/deberta-v3-base-prompt-injection); (3) LLM-as-judge (send input to a separate LLM for classification).

### Decision
Use **stdlib `re` with 10 case-insensitive regex patterns**. Input is NFKC-normalized before pattern matching. Any pattern match returns `SecurityCheckResult(is_safe=False, blocked_reason=<matching_pattern>, risk_level="high")` and the request is blocked. Safe input is wrapped in Sandwich Defense format before reaching LLM Layer 3.

### Rationale
- **Deterministic and auditable**: Regex patterns are transparent — security reviewers can understand exactly what is blocked without understanding model behavior
- **Zero dependency**: stdlib `re` adds no pip dependency, no model download, no GPU requirement
- **Extensible**: Adding a new pattern is a one-line regex addition — no retraining, no data collection, no false positive recalibration
- **Performance**: Sub-millisecond per message vs 10–100ms for ML inference
- **ML-based false positive risk**: An ML classifier tuned to detect injection would require a labeled dataset of benign Chinese/English customer service messages to calibrate — this dataset does not exist at Phase 2 scope. Regex patterns are conservative but predictable
- The 10 patterns cover known injection vectors: ignore/override instructions, role impersonation, system prompt extraction, delimiter injection. This is not exhaustive but targets the most common attacks seen in production LLM applications

### Consequences
- **Positive**: Transparent, auditable, no model dependency; pattern additions require only code review; blocked requests logged with specific `blocked_reason` for debugging
- **Negative**: May miss novel injection techniques not matching any pattern (e.g., encoded payloads, multi-turn jailbreaks); false positives possible if a benign user message coincidentally matches a pattern (e.g., "please act as a customer service representative"); pattern maintenance burden grows as attack techniques evolve

---

## ADR-015: Credit Card Detection — Luhn Algorithm Validation

### Status
Accepted

### Context
FR-16 extends Phase 1 PII masking with credit card number detection. A naive `\d{16}` regex would match many false positives: order numbers, tracking IDs, timestamps. The Luhn algorithm (mod 10 checksum) is the industry-standard checksum used by all major credit card issuers — valid card numbers pass Luhn, random 16-digit strings almost never do.

Alternatives: (1) Regex-only detection (no validation); (2) Regex + Luhn check; (3) Regex + BIN lookup against known issuer identification numbers.

### Decision
Use a **two-stage detection**: (1) regex pattern `\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b` to find 16-digit candidates; (2) `_luhn_check(card_number)` validates the checksum. Only numbers passing Luhn are masked (replaced with `[credit_card_masked]`). Numbers failing Luhn are left unmasked. Replacement is rightmost-first (matching ADR-007 Phase 1 approach) to avoid index shift.

`_luhn_check` implementation:
- Strip spaces/hyphens; accept only 16-digit numbers
- From rightmost digit (position 1, the check digit), skip position 1; for even positions (2, 4, 6...) multiply by 2; if result > 9 subtract 9
- Sum all digits; return `sum % 10 == 0`

### Rationale
- **False positive elimination**: A random 16-digit number has a 10% chance of passing Luhn (1 in 10). Without validation, every 16-digit number in a message would be masked, including order IDs, invoice numbers, and tracking codes. Luhn reduces false positives by 90%
- **No false negatives on valid cards**: All valid credit card numbers satisfy Luhn by definition (it's part of the ISO/IEC 7812 standard)
- **stdlib only**: No external dependency — the algorithm is a simple digit summation
- **Rightmost-first replacement**: Consistent with ADR-007 Phase 1 PII masking approach, preventing index shift bugs when multiple matches exist in the same text
- **Scope**: 16-digit cards only (Visa, Mastercard). 15-digit Amex cards are out of scope for Phase 2 — the pattern `\d{15}` is too prone to false positives without the Luhn+Luhn variant used by Amex

### Consequences
- **Positive**: High-precision credit card detection; no external dependency; `pii_types` list includes `"credit_card"` for Prometheus metric tracking via `omnibot_pii_masked_total`; false positive rate near-zero for non-card 16-digit numbers
- **Negative**: Amex (15-digit) cards not detected; Diners Club (14-digit) not detected; cards with non-standard formatting (e.g., mixed separator types) may escape detection; `PIIMaskingV2` must be tested separately from `PIIMasking` to ensure inheritance works correctly

---

## ADR-016: Emotion Analyzer — Rule-Based Keyword + Intensity vs ML Model

### Status
Accepted

### Context
FR-17 requires classifying each user message as POSITIVE, NEUTRAL, or NEGATIVE with an intensity score (0.0–1.0) and tracking emotion history with 24h exponential decay. The classification feeds into the escalation pipeline: >= 3 consecutive NEGATIVE messages trigger human handoff.

Options evaluated: (1) Rule-based keyword matching with intensity scoring; (2) ML sentiment model (e.g., `cardiffnlp/twitter-xlm-roberta-base-sentiment`); (3) LLM-based classification (call Claude to classify tone).

### Decision
Use a **rule-based keyword + intensity scoring** approach. A curated keyword dictionary maps Chinese and English words to `EmotionCategory` and base intensity. Intensity modifiers (degree adverbs like 非常/很/有點, exclamation marks, emoji) adjust intensity up or down. `EmotionTracker` then applies exponential decay (`decay = e^(-0.693 * hours_ago / 24)`) over the history window and computes a weighted score.

### Rationale
- **Deterministic and debuggable**: Every classification can be traced back to specific keywords — support teams can understand why a message triggered escalation
- **No ML model dependency**: The SAD module dependency graph (Section 8) shows `EmotionAnalyzer` depending only on `emotion_history` and `StructuredLogger` — no `sentence-transformers` or external API. Adding an ML model would introduce a dependency not budgeted in the architecture
- **Emotion is a supplementary signal**: The primary routing decisions are made by the knowledge layer (L1–L4). Emotion is a trigger for escalation, not a core decision engine. A lightweight approach is proportional to its role
- **Chinese/English coverage**: ML sentiment models trained primarily on English or product reviews would perform poorly on informal Chinese customer service chat. A keyword dictionary can be tuned specifically for the CS domain
- **LLM-based classification cost**: Using Claude API for every message's sentiment would add $0.001–0.002 per message — unjustified for an auxiliary classification

### Consequences
- **Positive**: Transparent; domain-tunable; no model download or GPU requirement; consistent with SAD dependency constraints; keyword dictionary is a data file, not code — CS team can extend it
- **Negative**: Sarcasm and implicit sentiment are not detected; keyword coverage must be manually curated; intensity scoring is heuristic, not calibrated against human-annotated data; may misclassify culturally specific expressions; emotion tracking data quality depends on keyword dictionary completeness

---

## ADR-017: DST 7-State Finite State Machine Design

### Status
Accepted

### Context
FR-18 requires a Dialogue State Tracker (DST) to manage conversation flow across 7 states with slot filling, confirmation loops, and automatic escalation after 3 rounds of unresolved slot filling. The DST must persist state to `conversations.dst_state` JSONB and support immutable state transitions.

Options evaluated: (1) Finite State Machine (FSM) with explicit transition rules; (2) Rule engine (e.g., `durable_rules` or custom DSL); (3) External workflow engine (Temporal, Airflow); (4) LLM-based dialogue management.

### Decision
Implement a **7-state Finite State Machine** with immutable state transitions. States: `IDLE → INTENT_DETECTED → SLOT_FILLING → AWAITING_CONFIRMATION → PROCESSING → RESOLVED | ESCALATED`. Each `DialogueState.transition(new_state)` returns a new `DialogueState` instance (frozen pattern from ADR-004) with incremented `turn_count` and updated `last_updated`. State is persisted to `conversations.dst_state` JSONB column. Slot filling has a hard limit of 3 rounds before forced escalation (`SLOT_FILLING → ESCALATED`).

### Rationale
- **Deterministic and auditable**: Every state transition is explicit and traceable — debugging a stuck conversation is a matter of reading the JSONB state blob
- **Minimal complexity**: A 7-state FSM does not warrant a workflow engine or rule DSL. The transition table (SAD §2.4.1) is small enough to be implemented as a set of guard conditions on the `transition()` method
- **Immutable transitions**: Consistent with ADR-004 dataclass pattern — `DialogueState` is `frozen=True`, which prevents accidental in-place mutation in async pipelines
- **JSONB persistence**: PostgreSQL JSONB supports indexing and partial queries — future Phase 3 analytics can query `dst_state->>'current_state'` without schema changes
- **LLM-based dialogue management** was rejected: LLM-driven state transitions are unpredictable, cannot guarantee the 3-round hard limit, and add per-turn latency that violates p95 < 1.5 s (NFR-08)
- **Workflow engines** (Temporal, Airflow) introduce heavy operational dependencies disproportionate to a 7-state local FSM

### Consequences
- **Positive**: Explicit transition rules; JSONB enables ad-hoc analytics; immutable states prevent async corruption; 3-round hard limit prevents infinite slot-filling loops; state machine fits in a single module
- **Negative**: Adding new states requires modifying the transition table — not externally configurable; complex multi-intent dialogues where two intents interleave are not supported (FSM is single-intent per conversation); slot extraction relies on intent detection quality which is a separate concern

---

## ADR-018: HybridKnowledgeV2 — RRF Fusion Strategy (k=60) vs Linear Combination

### Status
Accepted

### Context
FR-19 HybridKnowledgeV2 fuses results from Layer 1 (rule match, confidence 0–1) and Layer 2 (RAG vector search, cosine distance 0–2). These scores are on different scales and distributions — rule match confidence is a heuristic (0.95 exact, 0.70 partial), while RAG distance is unbounded. Direct score averaging would require normalization and calibration weights.

Options evaluated: (1) Reciprocal Rank Fusion (RRF); (2) Weighted linear combination with min-max normalization; (3) Simple concatenation (L1 results first, then L2).

### Decision
Use **Reciprocal Rank Fusion with k=60**. Each document's RRF score = `Σ 1 / (rank_in_list_i + k)`, summed across the L1 result list and the L2 result list. Results are sorted by descending RRF score and the Top-3 are returned. Confidence > 0.7 triggers early return (`source="rag"`).

### Rationale
- **Score-scale agnostic**: RRF only uses rank position, not raw scores — eliminates the need to calibrate normalization between L1 heuristic confidences and L2 cosine distances. A score of 0.70 from L1 means something different than a cosine distance of 0.70 from L2; RRF sidesteps this entirely
- **k=60 dampens rank differences**: With k=60, `1/(1+60) ≈ 0.0164` and `1/(5+60) ≈ 0.0154` — top results are close in score but still ordered. Lower k (e.g., 20) would amplify rank-1 over rank-5 by ~25%; higher k (e.g., 100) would flatten the distribution too much. k=60 provides the right balance for the typical 1–5 result range
- **Empirically validated**: RRF is the standard fusion approach used by Elasticsearch, Weaviate, and academic IR benchmarks (TREC). k=60 is the original value proposed in the Cormack et al. 2009 SIGIR paper and is the de-facto default
- **Linear combination rejected**: Requires choosing weights (w1 for L1, w2 for L2), normalizing L1 confidence and L2 cosine distance to a common [0,1] scale, and validating the weights against a relevance benchmark — overhead disproportionate to Phase 2 scope
- **Simple concatenation rejected**: L1 results always appear before L2 results, meaning a mediocre rule match at rank 3 would beat an excellent RAG match at rank 1 — semantically wrong

### Consequences
- **Positive**: No score normalization; no weight calibration; Top-3 fused ranking respects both retrieval methods; k=60 is well-understood and defensible
- **Negative**: Rank-only fusion discards magnitude information — a 0.95-confidence L1 match and a 0.71-confidence L1 match at the same rank contribute equally; L1 results with identical confidence but different ranks are ordered by position, not relevance; if L1 returns 0 results, RRF degenerates to L2-only ranking

---

## ADR-019: RAG Embedding Model — paraphrase-multilingual-MiniLM-L12-v2

### Status
Accepted

### Context
Both Layer 2 RAG (FR-19) and Layer 5 Grounding Checks (FR-21) require sentence embeddings. The model must support Chinese and English (OmniBot's primary languages), produce embeddings suitable for cosine similarity, and operate within the memory/performance constraints of a single Docker Compose development environment.

Options evaluated: (1) `paraphrase-multilingual-MiniLM-L12-v2` (384-dim); (2) `paraphrase-multilingual-mpnet-base-v2` (768-dim); (3) `LaBSE` (768-dim); (4) OpenAI `text-embedding-3-small` (API).

### Decision
Use **`paraphrase-multilingual-MiniLM-L12-v2`** via `sentence-transformers`. Embeddings are 384-dimensional. The same model instance is shared across RAG (L2) and GroundingChecker (L5) components.

### Rationale
- **384-dim is the sweet spot**: Half the storage and compute of 768-dim models (mpnet, LaBSE) while delivering comparable multilingual performance on semantic similarity benchmarks. For a 10K-entry knowledge base, 384-dim saves ~15 MB of vector storage vs 768-dim
- **Multilingual out of the box**: Trained on 50+ languages including Chinese and English — no separate monolingual models needed
- **Shared model = single memory footprint**: Both RAG and GroundingChecker use the same model, halving the memory requirement (~120 MB for one instance vs ~240 MB for two separate models)
- **pgvector compatibility**: `vector(384)` column already pre-provisioned from Phase 1 (ADR-002); ivfflat index with `vector_cosine_ops` operator class is the correct pairing for normalized MiniLM embeddings
- **OpenAI embeddings API rejected**: API latency per embedding (~50–100ms) would dominate RAG query time; per-token cost for every knowledge base entry on every search is unbounded; API dependency creates a hard external failure mode
- **LaBSE rejected**: 768-dim doubles storage; heavier model (~1.8 GB) vs MiniLM (~470 MB); marginal improvement on Chinese semantic similarity not justified by the overhead
- **mpnet-base-v2 rejected**: 768-dim doubles storage; primarily English-optimized with weaker Chinese support; the `multilingual` variant exists but is larger

### Consequences
- **Positive**: Single model loading; 384-dim embeddings fit in pgvector column sized from Phase 1; shared across RAG + grounding; Chinese/English bilingual support; no API cost per embedding
- **Negative**: 384-dim ceiling on embedding expressiveness — complex semantic relationships may be less distinguishable than with 768-dim models; MiniLM's distillation from a larger teacher model means some accuracy loss vs the teacher; future domain-specific fine-tuning would need to work within the 384-dim constraint

---

## ADR-020: Escalation Manager V2 — SLA Priority Tier Design

### Status
Accepted

### Context
FR-20 upgrades Phase 1 BasicEscalationManager with SLA priority levels and deadline enforcement. The escalation queue must differentiate urgency: a customer reporting a billing error (urgent) needs faster response than a general FAQ escalation (normal). The system must detect SLA breaches and support agent assignment/resolution lifecycle.

Options evaluated: (1) Three-tier priority with fixed SLA windows; (2) Single queue with FIFO ordering; (3) Dynamic SLA based on customer tier/history.

### Decision
Implement a **three-tier priority system** with configurable SLA windows: `normal` (priority=0, 30 min), `high` (priority=1, 15 min), `urgent` (priority=2, 5 min). `EscalationRequest` includes a `reason` enum (`out_of_scope`, `low_confidence`, `emotion_trigger`) that maps to priority: `emotion_trigger` → high, all others → normal. SLA deadlines are computed as `NOW() + SLA_BY_PRIORITY[priority]` at creation time and stored in `escalation_queue.sla_deadline`. Breach detection queries for `resolved_at IS NULL AND sla_deadline < NOW()` ordered by `priority DESC, queued_at ASC`.

### Rationale
- **Granularity matched to triggers**: Three tiers map cleanly to the three escalation triggers in the pipeline — knowledge exhaustion (normal), grounding failure (normal), emotion trigger (high). An additional "urgent" tier is reserved for future PII-sensitive escalations or manual agent flags
- **Configurable windows**: `SLA_BY_PRIORITY` is a dict, not hardcoded constants — operations can adjust SLA windows without code changes
- **FIFO within priority**: `queued_at ASC` as secondary sort ensures fairness within the same priority level — no starvation of older tickets
- **Simple SQL-based breach detection**: No need for a scheduler or cron job — a simple query identifies breaches, suitable for dashboard polling or alert integration in Phase 3
- **Customer-tier dynamic SLA rejected for Phase 2**: Requires a customer model and tier assignment system (RBAC, authentication) — both deferred to Phase 3 per SAD §11
- **Single FIFO queue rejected**: Would treat "customer is furious" the same as "FAQ not found" — violates the intent of emotion-triggered escalation

### Consequences
- **Positive**: Clear priority-to-SLA mapping; configurable via dict; SQL-based breach detection with no additional infrastructure; `omnibot_escalation_queue_size` gauge tracks queue depth
- **Negative**: Priority is statically assigned at creation time — cannot be upgraded mid-escalation (e.g., if a normal escalation receives additional angry messages); no auto-reassignment if the assigned agent does not pick up the ticket (requires Phase 3 alerting); SLA windows are global, not per-platform

---

## ADR-021: Grounding Checks L5 — Cosine Similarity vs Alternative Metrics

### Status
Accepted

### Context
FR-21 requires semantic alignment verification between LLM output and knowledge base source texts. The GroundingChecker must determine whether the LLM-generated response is semantically grounded in the retrieved knowledge. If not grounded, the output is discarded and the conversation is escalated.

Options evaluated: (1) Cosine similarity; (2) Euclidean distance; (3) Dot product (unnormalized); (4) Cross-encoder (e.g., `cross-encoder/stsb-roberta-base`).

### Decision
Use **cosine similarity** with a default threshold of 0.75. Both LLM output and source texts are embedded using the shared `paraphrase-multilingual-MiniLM-L12-v2` model (ADR-019). The max cosine similarity across all source texts is compared against the threshold. `max_score >= 0.75` → `grounded=True`; `max_score < 0.75` → `grounded=False, reason="below_threshold"`.

### Rationale
- **Direction-focused, not magnitude-sensitive**: Cosine similarity measures semantic direction, ignoring embedding magnitude — a short LLM answer ("您的訂單編號是 12345") should match a longer knowledge base entry ("訂單查詢結果：您的訂單編號是 12345，狀態為已出貨") even though their vector magnitudes differ
- **Consistent with pgvector operator**: The RAG query (ADR-019) uses `vector_cosine_ops` — grounding and retrieval use the same distance metric, so the grounding score is directly comparable to the RAG relevance score
- **Threshold 0.75 is conservative**: Cosine similarities of 0.75+ correspond to high semantic overlap in MiniLM embedding space. Setting it lower (e.g., 0.5) risks hallucinated content passing grounding; setting it higher (e.g., 0.9) would reject legitimate paraphrases
- **Euclidean distance rejected**: Sensitive to embedding magnitude — longer texts produce higher-magnitude vectors, making Euclidean distances incomparable across different-length source texts
- **Dot product rejected**: MiniLM embeddings are L2-normalized by default from `sentence-transformers.encode()`, so dot product is equivalent to cosine similarity in practice. Using cosine similarity explicitly documents the intent
- **Cross-encoder rejected**: A cross-encoder model would require running the LLM output + each source text as a pair through a transformer — O(n) inference cost where n = number of source texts. For 5 source texts, this is 5× the inference time vs 1× for bi-encoder cosine similarity. Latency impact violates p95 < 1.5 s

### Consequences
- **Positive**: Same model as RAG (shared memory); metric consistent with pgvector index; threshold is configurable via constructor; every LLM output verified before dispatch; ungrounded outputs never reach users
- **Negative**: Cosine similarity may miss hallucinated content that is lexically similar but factually wrong (e.g., wrong order number but right format); threshold is a global value — different knowledge domains may need different thresholds; grounding can only verify against available source texts, not against external truth

---

## ADR-022: Prometheus Metrics Library — prometheus_client vs OpenTelemetry

### Status
Accepted

### Context
FR-22 requires 8 core Prometheus metrics (histogram, counters, gauge) exported at `GET /metrics` in Prometheus text format. Phase 3 scope includes OpenTelemetry tracing. The choice of metrics library affects Phase 3 migration path.

Options evaluated: (1) `prometheus_client` (canonical Python Prometheus library); (2) OpenTelemetry Python SDK with Prometheus exporter; (3) Custom `/metrics` endpoint with manual text formatting.

### Decision
Use **`prometheus_client`** for Phase 2 metrics instrumentation. All 8 metrics (See SAD §2.7.2) are defined as module-level singletons and registered with the default collector registry. The `GET /metrics` endpoint calls `generate_latest()`.

### Rationale
- **Batteries included**: `prometheus_client` provides Histogram, Counter, and Gauge classes with built-in label support and text format export. No additional infrastructure or collector process
- **Phase 2 scope is metrics-only**: Tracing (OpenTelemetry's primary value proposition) is Phase 3 scope (SAD §11). Adopting OpenTelemetry now for metrics alone adds complexity (SpanProcessor, TracerProvider, Exporter configuration) for no Phase 2 benefit
- **Phase 3 migration path clean**: `prometheus_client` metrics can be bridged to OpenTelemetry via `opentelemetry-exporter-prometheus` in Phase 3 without rewriting metric definitions. The metric names, labels, and types stay the same
- **Proven in production**: `prometheus_client` is the most widely used Python Prometheus library (~20M downloads/month), maintained by the Prometheus team
- **Custom text formatting rejected**: Manually generating Prometheus text format is error-prone (escaping rules, type annotations, HELP/TYPE lines) and adds maintenance burden for no benefit

### Consequences
- **Positive**: Simple setup; standard Prometheus format; Phase 3 migration path to OpenTelemetry is additive, not a rewrite; extensive documentation and community support
- **Negative**: Two observability libraries in the codebase after Phase 3 (prometheus_client for metrics + OpenTelemetry for tracing); no built-in exemplar support (linking traces to metrics) without additional configuration; histogram bucket configuration is static

---

## ADR-023: pgvector ivfflat Index — Configuration (lists=100)

### Status
Accepted

### Context
FR-23 requires a pgvector index on `knowledge_base.embeddings` to achieve RAG query latency < 200ms at 10K entries scale. pgvector offers two index types: ivfflat (approximate, inverted file with flat compression) and ivfpq (inverted file with product quantization). The `lists` parameter controls the number of inverted file clusters — too few reduces recall, too many increases build time and memory.

### Decision
Create an **ivfflat index** with `lists = 100` and `vector_cosine_ops` operator class:
```sql
CREATE INDEX idx_kb_embeddings ON knowledge_base
  USING ivfflat (embeddings vector_cosine_ops) WITH (lists = 100);
```
Queries filter by `embedding_model = 'paraphrase-multilingual-MiniLM-L12-v2'` to ensure only compatible embeddings are compared.

### Rationale
- **lists = 100 follows the sqrt(n) heuristic**: For n ≈ 10,000 entries, `sqrt(10000) = 100`. This is the pgvector documentation's recommended starting point — it balances the number of clusters probed against recall
- **ivfflat not ivfpq**: ivfpq uses product quantization which compresses vectors, trading accuracy for speed and storage. At 10K scale with 384-dim vectors, the storage savings (~50%) do not justify the recall degradation (~5-10%). ivfpq is appropriate at 1M+ scale — out of scope for Phase 2
- **vector_cosine_ops**: Matches the cosine similarity metric used throughout the system (ADR-021 grounding, RAG retrieval). Consistent metric across indexing and querying
- **embedding_model filter**: The same column may store embeddings from different models if the model is upgraded in Phase 3. The WHERE clause ensures cross-model comparisons don't occur
- **< 200ms latency target**: With ivfflat and lists=100, querying 10K vectors with probes=1 (default) scans ~100 vectors per query (n/lists). This is well within the 200ms budget for cosine distance over 384-dim vectors

### Consequences
- **Positive**: < 200ms RAG query latency at 10K scale; index created via Alembic migration (ADR-011); consistent cosine operator across retrieval and grounding; embedding_model filter prevents cross-model errors
- **Negative**: ivfflat is approximate — recall is ~95-98% at lists=100, meaning 2-5% of relevant results may be missed compared to brute-force; index must be rebuilt after bulk inserts (requires periodic `REINDEX` if knowledge base grows significantly); lists=100 may need tuning as the knowledge base scales beyond 10K

---

## ADR-024: Golden Dataset — Schema and Collection Strategy

### Status
Accepted

### Context
FR-24 requires a golden dataset of >= 500 annotated edge cases across 6 boundary types for regression testing. The dataset must support automated test execution (batch evaluation of the full pipeline against known inputs and expected outputs) and be gated by an approval workflow to ensure annotation quality.

Options evaluated: (1) `edge_cases` table with status workflow; (2) JSON/YAML file checked into repository; (3) External annotation tool (Label Studio, Argilla).

### Decision
Use an **`edge_cases` database table** with a status-based approval workflow. Six boundary types are predefined: (1) ASR garbled text, (2) spelling errors, (3) dialect/abbreviation, (4) multi-intent, (5) emotional outburst, (6) prompt injection. Each requires >= 50 approved records. Records must be `status='approved'` with a non-null `annotated_at` timestamp before inclusion in regression tests. The `used_in_regression` boolean flag enables selective test set curation.

Table schema:
- `id SERIAL PRIMARY KEY`
- `query TEXT NOT NULL` — the input message
- `expected_intent VARCHAR(50)` — expected intent classification
- `expected_answer TEXT` — expected bot response
- `status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected'))`
- `annotated_at TIMESTAMPTZ` — set on approval
- `used_in_regression BOOLEAN DEFAULT FALSE` — gates test inclusion
- `created_at TIMESTAMPTZ DEFAULT NOW()`

### Rationale
- **Database-backed, not file-backed**: A JSON/YAML file checked into the repo would couple the regression test data to the codebase version. A database table allows continuous ingestion of new edge cases from production without code changes. It also enables SQL-based queries (e.g., "show me all approved prompt injection cases")
- **Approval workflow ensures quality**: Raw edge case collection (e.g., from production logs) enters with `status='pending'`. A human reviewer must approve (`status='approved'`) before the record enters the test set. This prevents mislabeled or ambiguous cases from polluting the regression baseline
- **6-category classification maps to known failure modes**: Each category targets a specific ML/NLP failure mode:
  1. ASR garbled → robustness to speech-to-text errors
  2. Spelling errors → robustness to typos (critical for mobile input)
  3. Dialect/abbreviation → robustness to domain-specific jargon
  4. Multi-intent → correctness under intent ambiguity
  5. Emotional outburst → escalation trigger accuracy
  6. Prompt injection → security block rate validation (NFR-12)
- **`used_in_regression` flag**: Not all approved edge cases need to run in every CI pipeline — a curated subset can be used for fast pre-commit checks, while the full set runs in nightly regression
- **External annotation tool rejected**: Label Studio or Argilla would require hosting an additional service, configuring authentication, and integrating with the OmniBot pipeline. For a 500-record target, the overhead of a dedicated annotation platform is disproportionate
- **File-based approach rejected**: A static file cannot be easily appended to from production (e.g., "log this conversation as a potential edge case"). It also requires a separate process for review and approval

### Consequences
- **Positive**: Database-backed ingestion from production; SQL-queryable test sets; approval workflow prevents mislabeled test data; `used_in_regression` flag enables CI vs nightly test split; 6-category classification aligns with NFR-12 and NFR-15 measurement
- **Negative**: Requires human annotation effort for all 500+ records (cannot be fully automated); `edge_cases` table adds one more table to the migration stack; no built-in inter-annotator agreement metrics (manual review by a single reviewer is assumed); test execution must load records from DB at test suite startup

---

*ADR.md v2.0 — OmniBot Phase 2 — Agent A (ARCHITECT) — 2026-05-17*
