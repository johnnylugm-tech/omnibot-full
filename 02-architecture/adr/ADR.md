# Architecture Decision Records — OmniBot Phase 1

> **Project**: OmniBot — 多平台客服機器人
> **Phase**: 1 (MVP 基礎)
> **Version**: 1.0
> **Date**: 2026-05-13
> **Authored by**: Agent A (ARCHITECT)
> **Input**: SRS.md v1.0, CONSTRAINTS.md v1.0, SAD.md v1.0

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

SQL query pattern: `SELECT ... WHERE question ILIKE '%{term}%' OR '{term}' = ANY(keywords) AND is_active = TRUE ORDER BY version DESC LIMIT 1`

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
- A committed `.env.example` with placeholder values documents the required variable names without exposing values

### Consequences
- **Positive**: Simple; no extra service; compatible with any cloud runtime; secrets rotate without image rebuild
- **Negative**: Secrets visible in process environment (e.g., `ps aux` or `/proc/PID/environ` leakage); Phase 3 should migrate to Vault or cloud-native secrets manager for production hardening

---

*ADR.md v1.0 — OmniBot Phase 1 — Agent A (ARCHITECT) — 2026-05-13*
