# Risk Register — OmniBot

> **[FR-01]** Platform Adapter — Telegram + LINE Webhook
> **[FR-02]** Webhook Signature Verification
> **[FR-03]** Unified Message Format
> **Phase**: 7 (Risk Register)
> **Date**: 2026-05-15
> **Status**: DRAFT

Citations:
- SPEC/omnibot-phase-1.md:106-136 (Webhook endpoint API design)
- SPEC/omnibot-phase-1.md:319-360 (UnifiedMessage / Platform enum definitions)
- SRS.md:13-25 (FR-01 functional requirements and acceptance criteria)
- SAD.md:64-95 (TelegramAdapter / LINEAdapter module design)
- build/lib/omnibot/adapters/telegram.py:11-28 (TelegramAdapter implementation)
- build/lib/omnibot/adapters/line.py:20-46 (LINEAdapter implementation)
- build/lib/omnibot/router.py:15-26 (PLATFORM_ROUTES routing table)
- SRS.md:28-41 (FR-02 functional requirements and acceptance criteria)
- SAD.md:97-109 (SignatureVerifier design and VERIFIERS registry)
- SPEC/omnibot-phase-1.md:276-313 (Webhook signature verification reference implementation)
- 03-development/src/omnibot/auth/verifier.py:17-24 (verify_telegram_signature)
- 03-development/src/omnibot/auth/verifier.py:27-31 (verify_line_signature)
- 03-development/src/omnibot/auth/verifier.py:36-60 (PlatformVerifier registry and VERIFIERS singleton)
- 03-development/src/omnibot/auth/verifier.py:77-103 (verify_signature FastAPI dependency)
- SRS.md:44-55 (FR-03 functional requirements and acceptance criteria)
- SAD.md:140-167 (UnifiedMessage / UnifiedResponse data contracts)
- SAD.md:447-452 (pipeline: parse → identity resolution → inject unified_user_id)
- SPEC/omnibot-phase-1.md:327-351 (Platform enum, MessageType enum, UnifiedMessage reference definition)
- 03-development/src/omnibot/models.py:12-20 (Platform enum implementation)
- 03-development/src/omnibot/models.py:35-48 (UnifiedMessage frozen dataclass)
- build/lib/omnibot/router.py:15-18 (PLATFORM_ROUTES — telegram and line only)
- SRS.md:74-87 (FR-05 functional requirements and acceptance criteria)
- SAD.md:190-207 (PIIMaskerL4 design and logical constraints)
- SPEC/omnibot-phase-1.md:383-435 (PIIMasking reference implementation — rightmost-first replacement, should_escalate)
- 03-development/src/omnibot/pii/__init__.py:12-20 (PIIMaskResult dataclass — not frozen)
- 03-development/src/omnibot/pii/__init__.py:25-36 (phone, email, address regex patterns)
- 03-development/src/omnibot/pii/__init__.py:39-47 (_SENSITIVE_KEYWORDS list — substring match tokens)
- 03-development/src/omnibot/pii/__init__.py:65-93 (mask_pii — sequential left-to-right substitution)
- 03-development/src/omnibot/pii/__init__.py:96-98 (contains_sensitive_keywords — wrong API name vs should_escalate)
- SRS.md:91-101 (FR-06 functional requirements and acceptance criteria)
- SRS.md:285 (FR-06 default rate limit 100 rps)
- SPEC/omnibot-phase-1.md:440-484 (FR-06 Token Bucket reference implementation)
- 03-development/src/omnibot/rate_limiter/__init__.py:13-40 (TokenBucket implementation)
- 03-development/src/omnibot/rate_limiter/__init__.py:43-59 (RateLimiter implementation)

---

## Summary Table

| risk_id | description (short) | likelihood | impact | score | status |
|---------|---------------------|:----------:|:------:|:-----:|--------|
| RISK-FR01-01 | External API schema break (Telegram/LINE) | 2 | 4 | 8 | OPEN |
| RISK-FR01-02 | 3-second webhook response SLA breach | 3 | 4 | 12 | OPEN |
| RISK-FR01-03 | Unsupported Telegram message types → silent data loss | 4 | 3 | 12 | OPEN |
| RISK-FR01-04 | LINE batch webhook — only first event processed | 3 | 3 | 9 | OPEN |
| RISK-FR01-05 | Webhook secret rotation causes platform outage | 2 | 5 | 10 | OPEN |
| RISK-FR02-01 | Bot token in request header — credential log exposure | 3 | 4 | 12 | OPEN |
| RISK-FR02-02 | Replay attack — body-only HMAC has no timestamp/nonce | 3 | 3 | 9 | OPEN |
| RISK-FR02-03 | Mutable VERIFIERS registry enables runtime injection | 2 | 4 | 8 | OPEN |
| RISK-FR02-04 | 401 detail string leaks failure subtype (info disclosure) | 4 | 2 | 8 | OPEN |
| RISK-FR03-01 | `unified_user_id=""` default — pre-resolution identity bypass | 4 | 4 | 16 | OPEN |
| RISK-FR03-02 | `received_at` server clock diverges from platform event time | 3 | 3 | 9 | OPEN |
| RISK-FR03-03 | `raw_payload` dict interior-mutable despite `frozen=True` | 2 | 3 | 6 | OPEN |
| RISK-FR03-04 | `Platform.MESSENGER/WHATSAPP` defined without adapter guard | 3 | 3 | 9 | OPEN |
| RISK-FR04-01 | `Cc`-only filter preserves bidi override / `Cf` format chars | 3 | 4 | 12 | OPEN |
| RISK-FR04-02 | `ValueError` on malformed Unicode unhandled → 500 + retry storm | 3 | 3 | 9 | OPEN |
| RISK-FR04-03 | L3 pattern matching absent in Phase 1 — NFKC-normalized injections pass | 4 | 3 | 12 | OPEN |
| RISK-FR04-04 | All-control-char input silently collapses to `""` with no diagnostic log | 3 | 2 | 6 | OPEN |
| RISK-FR05-01 | International `+886` phone format bypasses all phone regex patterns | 3 | 4 | 12 | OPEN |
| RISK-FR05-02 | `contains_sensitive_keywords()` substring match → false positives on "110" in addresses; name deviates from `should_escalate()` spec | 4 | 3 | 12 | OPEN |
| RISK-FR05-03 | Detection on original `text` after substitution on `result` — `pii_types` inflated for overlapping patterns | 3 | 3 | 9 | OPEN |
| RISK-FR05-04 | `PIIMaskResult` not `frozen=True` — mutable `pii_types` corrupts NFR-06 compliance audit trail | 2 | 3 | 6 | OPEN |
| RISK-FR06-01 | Unbounded `_buckets` dict → OOM DoS via unique `platform:user_id` flood | 3 | 4 | 12 | OPEN |
| RISK-FR06-02 | `allow()` return value not wired to HTTP 429 — rate limiting inoperative in pipeline | 4 | 4 | 16 | OPEN |
| RISK-FR06-03 | Global `_lock` on `RateLimiter` serializes all per-user lookups under concurrency | 3 | 3 | 9 | OPEN |
| RISK-FR06-04 | In-memory bucket state resets on process restart — rate limit bypass on redeploy | 3 | 3 | 9 | OPEN |
| RISK-FR07-01 | Partial-match confidence 0.70 always escalates — `<= 0.7` threshold conflicts with SAD `>= 0.7` reply contract | 4 | 4 | 16 | OPEN |
| RISK-FR07-02 | `QueryResult` not `frozen=True`; `id`/`knowledge_id` absent — Phase 2 `AttributeError` at runtime | 4 | 3 | 12 | OPEN |
| RISK-FR07-03 | Case-sensitive `kw in text` vs ILIKE — mixed-case English keywords miss rule matches | 3 | 3 | 9 | OPEN |
| RISK-FR07-04 | No `is_active` guard or `version DESC` order — deprecated rules permanently active | 3 | 3 | 9 | OPEN |
| RISK-FR09-01 | `print()` without `flush=True` — NDJSON entries silently lost on container crash/SIGTERM | 3 | 4 | 12 | OPEN |
| RISK-FR09-02 | No minimum log-level filter — `debug()` emits raw PII payloads to production stdout | 3 | 4 | 12 | OPEN |
| RISK-FR09-03 | `log()` caller-supplied `service` overrides `self._service` — false service attribution | 3 | 2 | 6 | OPEN |
| RISK-FR09-04 | `app.py` uses stdlib `logging` — application-layer errors bypass FR-09 NDJSON format | 4 | 3 | 12 | OPEN |

> **Score** = likelihood × impact. Scores ≥ 10 are HIGH priority.

---

## Detailed Risk Entries

---

### RISK-FR01-01 — External API Schema Break

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR01-01 |
| **fr_tag** | [FR-01] |
| **category** | Technical / External Dependency |
| **description** | Telegram or LINE changes their webhook event payload structure (field renames, removals, type changes) without a deprecation period, causing `parse_telegram_update` or `parse_line_event` to produce empty or incorrect `UnifiedMessage` fields silently. |
| **likelihood** | 2 / 5 — Both APIs are versioned and relatively stable; breaking changes are announced, but unannounced minor schema shifts have occurred historically. |
| **impact** | 4 / 5 — Silently malformed `UnifiedMessage` propagates to the knowledge layer producing spurious escalations or empty responses; affects all users on the changed platform until detected and patched. |
| **mitigation** | (1) Maintain golden-path payload fixtures in `tests/test_fr01.py` tied to specific API versions. (2) Emit structured WARN log (FR-09) on missing required fields during parse. (3) Subscribe to Telegram Bot API changelog and LINE Developer News for schema announcements. (4) CI snapshot tests catch regression on fixture payloads before deploy. |
| **owner** | Platform Team |

**Citations**: SPEC/omnibot-phase-1.md:111-135, SRS.md:19-22, build/lib/omnibot/adapters/telegram.py:11-28, build/lib/omnibot/adapters/line.py:20-46

---

### RISK-FR01-02 — 3-Second Webhook Response SLA Breach

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR01-02 |
| **fr_tag** | [FR-01] |
| **category** | Performance / Operational |
| **description** | Downstream processing (DB query, knowledge-layer rule match, PII masking) pushes total handler time past 3 seconds, violating the NFR-02 p95 latency constraint and the SAD.md adapter constraint that requires `200 OK` within 3 s of receipt regardless of downstream outcome. |
| **likelihood** | 3 / 5 — Cold-start in Docker, PostgreSQL connection acquisition under load, or synchronous knowledge-layer evaluation can each add 1-2 s; combining them exceeds the budget. |
| **impact** | 4 / 5 — LINE retries unacknowledged webhooks causing duplicate message ingestion; Telegram silently drops events for which no `200` was returned; NFR-02 breach triggers SLA alert. |
| **mitigation** | (1) Decouple acknowledgment from downstream processing: return `200 OK` immediately upon successful parse, then process via background task or queue. (2) Add p95 latency metric to MONITORING_PLAN.md. (3) Docker Compose healthcheck (FR-13) ensures PostgreSQL and Redis are `healthy` before API container accepts traffic, eliminating cold-start DB failures. (4) Set hard request timeout at the ASGI layer (e.g., 2.5 s) to fail fast and surface latency issues. |
| **owner** | DevOps |

**Citations**: SRS.md:21 (< 3s acceptance criterion), SAD.md:78 (3 s constraint), SAD.md:94 (LINE retries), SPEC/omnibot-phase-1.md:117-135 (200 OK / 429 responses)

---

### RISK-FR01-03 — Unsupported Telegram Message Types Cause Silent Data Loss

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR01-03 |
| **fr_tag** | [FR-01] |
| **category** | Technical / Functional |
| **description** | `parse_telegram_update` defaults any non-text Telegram message (photo, voice, sticker, document, location) to `MessageType.TEXT` with an empty `content` field (`build/lib/omnibot/adapters/telegram.py:18`). This produces a structurally valid but semantically empty `UnifiedMessage`, which is invisible to callers and to ops. |
| **likelihood** | 4 / 5 — Real Telegram users routinely send photos, stickers, and voice messages; any customer-service bot will receive these immediately in production. |
| **impact** | 3 / 5 — Knowledge layer receives empty content → confidence 0 → triggers unnecessary escalation. No error is raised; the silent default masks the actual message type in logs. Degrades FCR metric (NFR-01) for non-text interactions. |
| **mitigation** | (1) Add explicit type dispatch in `parse_telegram_update`: map known non-text types to `MessageType.IMAGE / STICKER / LOCATION / FILE` with empty `content`; preserve `raw_payload` for Phase 2 media handling. (2) Emit `WARN` log (FR-09) when `message.get("text")` is absent, including the raw Telegram message type. (3) Add acceptance test for photo/sticker payloads in `tests/test_fr01.py`. Phase 2 extends non-text content extraction (SPEC/omnibot-phase-1.md:269). |
| **owner** | Platform Team |

**Citations**: build/lib/omnibot/adapters/telegram.py:17-18, SPEC/omnibot-phase-1.md:333-338 (MessageType enum), SRS.md:19-22 (acceptance criteria), SPEC/omnibot-phase-1.md:269 (Phase 2 scope note)

---

### RISK-FR01-04 — LINE Batch Webhook: Only First Event Processed

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR01-04 |
| **fr_tag** | [FR-01] |
| **category** | Technical / Functional |
| **description** | `parse_line_event` uses `events[0]` exclusively (`build/lib/omnibot/adapters/line.py:29`). LINE Messaging API delivers multiple events in a single webhook call (e.g., a `follow` event bundled with an initial `message` event). All events after index 0 are silently discarded. |
| **likelihood** | 3 / 5 — LINE batch delivery is documented behavior and occurs in practice on group joins, follow events, and high-throughput scenarios. |
| **impact** | 3 / 5 — Subsequent events in the batch are dropped with no log entry; users whose events are at index ≥ 1 receive no response, lowering FCR (NFR-01). |
| **mitigation** | (1) Short-term: emit `WARN` log when `len(events) > 1` so ops is aware of dropped events. (2) Medium-term (Phase 2 prep): refactor `parse_line_event` to return `List[UnifiedMessage]` and update the router to dispatch all events; update `tests/test_fr01.py` with multi-event fixture. |
| **owner** | Platform Team |

**Citations**: build/lib/omnibot/adapters/line.py:25-46, SPEC/omnibot-phase-1.md:319-360 (UnifiedMessage format), SRS.md:19-22 (acceptance criteria)

---

### RISK-FR01-05 — Webhook Secret Rotation Causes Complete Platform Outage

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR01-05 |
| **fr_tag** | [FR-01] |
| **category** | Operational / Security |
| **description** | Rotating the Telegram `bot_token` or LINE `channel_secret` (e.g., due to credential leak or scheduled key rotation) immediately invalidates all in-flight HMAC verification (FR-02), causing 100% of webhook requests for the affected platform to return `401 AUTH_INVALID_SIGNATURE` until the new secret is deployed. |
| **likelihood** | 2 / 5 — Planned rotations are infrequent but required; unplanned emergency rotation (credential exposure) can occur at any time without advance notice. |
| **impact** | 5 / 5 — Complete platform outage for the affected Telegram or LINE channel; all user messages are rejected until deployment completes; no graceful degradation path. |
| **mitigation** | (1) `platform_configs.webhook_secret_key_ref` (SRS.md:193) stores secret references rather than plaintext, enabling secret-manager-side rotation without code deploy. (2) Implement dual-secret grace period: accept either old or new secret for a configurable window (e.g., 60 s) during rotation. (3) Document rotation runbook in MONITORING_PLAN.md: update secret-manager value → verify new signatures in staging → remove old secret after TTL. (4) Alert on consecutive `401` spikes (threshold: > 5% of requests over 30 s) to detect accidental rotation. |
| **owner** | SecOps / Platform Team |

**Citations**: SRS.md:192-193 (platform_configs.webhook_secret_key_ref), SAD.md:97-108 (SignatureVerifier design), SPEC/omnibot-phase-1.md:276-315 (Webhook signature verification section)

---

## [FR-02] Webhook Signature Verification — Detailed Risk Entries

---

### RISK-FR02-01 — Bot Token Transmitted as HTTP Request Header

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR02-01 |
| **fr_tag** | [FR-02] |
| **category** | Security / Credential Exposure |
| **description** | `verify_signature` (verifier.py:86-87) reads the Telegram bot_token from the `X-Telegram-Bot-Token` request header on every webhook call. In the standard Telegram Bot API security model, the bot_token is a shared secret stored server-side and never transmitted over the wire. Passing it as a request header means it appears in reverse proxy access logs, WAF inspection logs, API gateway audit trails, and any middleware that captures HTTP request headers by default — which covers nginx, AWS ALB, and most APM agents out of the box. |
| **likelihood** | 3 / 5 — Cloud load balancers (nginx, AWS ALB, Cloudflare), WAFs, and APM agents (Datadog, New Relic) log HTTP request headers by default; misconfigured log aggregation is common in early-stage deployments, and a single log-forwarding misconfiguration exposes every bot_token ever sent. |
| **impact** | 4 / 5 — A leaked bot_token allows an attacker to: (1) derive the HMAC key via `SHA256(bot_token)` and forge valid signatures for arbitrary webhook payloads, bypassing FR-02 entirely; (2) call the Telegram Bot API directly as the bot to read conversations, send messages, ban users, and delete the webhook registration. |
| **mitigation** | (1) Remove bot_token from request headers; derive and store the HMAC key (`SHA256(bot_token)`) server-side at startup using `platform_configs.webhook_secret_key_ref` (SRS.md:193) — the raw token never travels over the wire. (2) Replace `X-Telegram-Bot-Token` with a signature-only header (`X-Telegram-Hmac-Signature`) pattern, consistent with how LINE's `X-Line-Signature` already works. (3) Before removing the header in production, audit all log pipelines for `X-Telegram-Bot-Token` and apply field redaction. (4) Rotate any bot_tokens that have been transmitted as headers in non-production environments. |
| **owner** | SecOps / Platform Team |

**Citations** (HR-15): verifier.py:65-74 (`_PLATFORM_CONFIG` header names), verifier.py:86-93 (header extraction and missing-credentials check), SAD.md:97-109 (SignatureVerifier design), SRS.md:192-193 (`webhook_secret_key_ref`)

---

### RISK-FR02-02 — Replay Attack: Body-Only HMAC Lacks Timestamp or Nonce

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR02-02 |
| **fr_tag** | [FR-02] |
| **category** | Security / Replay Vulnerability |
| **description** | Both `verify_telegram_signature` (verifier.py:17-24) and `verify_line_signature` (verifier.py:27-31) compute HMAC over the raw request body bytes only. No timestamp, request ID, or nonce is incorporated into the signed payload. A valid webhook request captured once — from server access logs that record bodies, a compromised intermediary, or API gateway request-replay tooling — can be resent indefinitely and will pass signature verification each time, causing duplicate event processing downstream. |
| **likelihood** | 3 / 5 — TLS prevents passive in-transit capture; however, server-side body logging (common for debugging), API gateway replay features, and LINE's documented retry-on-timeout behavior (RISK-FR01-02) each provide realistic replay paths. The SPEC reference implementation (SPEC/omnibot-phase-1.md:276-313) also omits nonce/timestamp, giving no upstream guidance to add one. |
| **impact** | 3 / 5 — Replayed webhooks trigger duplicate message ingestion: double responses to end-users, duplicate escalation tickets, inflated analytics, and LINE `replyToken` exhaustion (tokens are single-use; a replay consumes the token, making the original event un-repliable). |
| **mitigation** | (1) Persist and deduplicate on a per-platform message identifier: Telegram `message.message_id`, LINE event `timestamp` + `source.userId` composite key; reject duplicates seen within a configurable TTL (e.g., 5 min). (2) Validate event recency: reject Telegram updates and LINE events with a timestamp older than ±5 minutes from server clock. (3) Enable idempotency keys in the downstream message store (Phase 2 / FR-04 scope). (4) Emit a structured WARN log (FR-09) on detected replay attempts, keyed by `request_id`, for ops alerting. |
| **owner** | Platform Team |

**Citations** (HR-15): verifier.py:17-24 (`verify_telegram_signature` — body-only HMAC), verifier.py:27-31 (`verify_line_signature` — body-only HMAC), SPEC/omnibot-phase-1.md:276-313 (reference verifier — no nonce/timestamp), SRS.md:28-41 (FR-02 acceptance criteria — replay not addressed)

---

### RISK-FR02-03 — Mutable VERIFIERS Registry Enables Runtime Verifier Injection

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR02-03 |
| **fr_tag** | [FR-02] |
| **category** | Security / Integrity |
| **description** | `VERIFIERS = PlatformVerifier()` (verifier.py:60) is a module-level mutable singleton. Its public `register()` method (verifier.py:48-50) allows any code with module import access to replace the production `verify_telegram_signature` or `verify_line_signature` callable at runtime. A deserialization vulnerability, a future plugin system without access controls, or a test that modifies the registry without restoring it could install a verifier that always returns `True`, bypassing FR-02 for all subsequent requests on the affected platform for the lifetime of the process. |
| **likelihood** | 2 / 5 — Exploitation requires prior code execution in the same process; not directly exploitable from the network in the current architecture. Most likely vector in the short term: test isolation failure where a stub verifier registered in one test leaks into subsequent tests (particularly when running `pytest -x` or in parallel). |
| **impact** | 4 / 5 — A tampered verifier accepts all webhook requests without valid HMAC signatures, rendering FR-02 completely ineffective for that platform. Any actor who can send HTTP requests can inject arbitrary payloads into the message pipeline, bypassing all authentication. Blast radius is scoped to the per-platform registry entry, not cross-platform. |
| **mitigation** | (1) After initial startup population, convert `_verifiers` to a `types.MappingProxyType` or remove/gate the `register()` method behind an initialization-phase flag so it cannot be called at request time. (2) In tests, mock the verifier functions directly via `unittest.mock.patch("omnibot.auth.verifier.verify_telegram_signature", ...)` rather than mutating the global registry. (3) Add a CI-level assertion (in `conftest.py`) that compares the registry contents against a known-good snapshot before and after each test. |
| **owner** | Platform Team |

**Citations** (HR-15): verifier.py:36-60 (`PlatformVerifier` class and `VERIFIERS` singleton), verifier.py:48-50 (public `register()` method), SAD.md:107-108 (`VERIFIERS` dict registry design — extensibility requirement)

---

### RISK-FR02-04 — 401 Response Detail Exposes Failure Subtype to Unauthenticated Callers

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR02-04 |
| **fr_tag** | [FR-02] |
| **category** | Security / Information Disclosure |
| **description** | `verify_signature` returns two distinct `HTTPException` detail strings: `"AUTH_INVALID_SIGNATURE: missing credentials"` (verifier.py:92) when the secret or signature header is absent, and `"AUTH_INVALID_SIGNATURE: signature mismatch"` (verifier.py:100) when the HMAC does not match. Both strings are returned to the unauthenticated caller in the HTTP response body. An attacker can distinguish "no credentials sent" from "credentials received but HMAC incorrect", enabling targeted reconnaissance: probe with no headers → learn what headers are expected; probe with a crafted token → learn whether the token format is recognised. |
| **likelihood** | 4 / 5 — No authentication is required to receive the discriminating detail string; it appears in every 401 response. Any automated scanner or curious caller will observe both variants without effort. |
| **impact** | 2 / 5 — Reveals attack surface granularity (token format recognition), but does not weaken the cryptographic HMAC check itself. Useful for speeding up targeted credential-stuffing or token enumeration, but does not provide a path to bypass verification. |
| **mitigation** | (1) Collapse both failure cases to a single opaque error code: return `{"detail": "AUTH_INVALID_SIGNATURE"}` without a subtype for all 401 responses. (2) Log the full subtype detail internally via the FR-09 structured logger, keyed by `request_id`, so ops retains diagnostic visibility without exposing it externally. (3) Apply rate-limiting (FR-08) on 401 responses per source IP to reduce the value of enumeration attempts. |
| **owner** | Platform Team |

**Citations** (HR-15): verifier.py:89-93 (missing-credentials 401 branch), verifier.py:97-101 (signature-mismatch 401 branch), SAD.md:410 (security event logging at boundary), SRS.md:28-41 (FR-02 acceptance criteria — no info-disclosure requirement stated)

---

## [FR-03] Unified Message Format — Detailed Risk Entries

---

### RISK-FR03-01 — `unified_user_id=""` Default Enables Pre-Resolution Messages to Propagate as Valid

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR03-01 |
| **fr_tag** | [FR-03] |
| **category** | Technical / Functional |
| **description** | `UnifiedMessage.unified_user_id` is defined with a default value of `""` (empty string) (`03-development/src/omnibot/models.py:47`). The SAD spec (`SAD.md:147`) and pipeline design (`SAD.md:447-452`) treat `unified_user_id` as a UUID that must be injected by `ConversationContext` after identity resolution. In Phase 1, `app.py` calls `parser(payload)` and returns the result directly, bypassing identity resolution entirely. Every Phase 1 `UnifiedMessage` therefore carries `unified_user_id == ""`. Phase 2 downstream consumers (knowledge layer, conversation tracker) that branch on or store `unified_user_id` will silently process messages with no resolved identity, either failing on UUID validation or associating responses with the empty-string pseudo-identity. Because `frozen=True` prevents in-place injection, Phase 2 must construct a replacement `UnifiedMessage` with the resolved UUID — a pattern not enforced by the type system and easy to omit. |
| **likelihood** | 4 / 5 — All Phase 1 webhook responses already return `"unified_user_id": ""`; the gap is active in every deployed message, not a hypothetical. Phase 2 code that forgets to replace the pre-resolution instance will introduce the bug silently. |
| **impact** | 4 / 5 — Downstream consumers relying on `unified_user_id` for identity, conversation threading, or audit trail will either crash on UUID validation, silently produce orphaned conversation records keyed on `""`, or bypass per-user rate limiting and FCR tracking (NFR-01). No error is raised at the `UnifiedMessage` construction site. |
| **mitigation** | (1) Change `unified_user_id` from a defaulted field to a required positional field (`unified_user_id: str`) matching `SAD.md:147`; update all adapter call sites to explicitly pass `""` until identity resolution is wired, making the gap visible. (2) Add a `__post_init__` invariant (via `object.__setattr__`) that emits a `WARN` log (FR-09) when `unified_user_id == ""` at request-response boundary. (3) In Phase 2, enforce the injection pattern in a `ConversationContext.resolve()` wrapper that always returns a new `UnifiedMessage` with a validated non-empty UUID — validate with `uuid.UUID(unified_user_id)` before constructing. (4) Add `test_fr03.py` assertion that a freshly parsed `UnifiedMessage` with `unified_user_id=""` cannot reach the knowledge layer without explicit override. |
| **owner** | Platform Team |

**Citations** (HR-15): 03-development/src/omnibot/models.py:47 (`unified_user_id: str = ""`), SAD.md:143-153 (frozen dataclass spec — `unified_user_id` has no default), SAD.md:447-452 (pipeline: parse → identity resolution → inject `unified_user_id`), SPEC/omnibot-phase-1.md:345 (`unified_user_id: Optional[str]` in reference definition), SRS.md:50 (FR-03 acceptance criterion — field must be present), 01-requirements/SRS.md:44-55 (FR-03 scope)

---

### RISK-FR03-02 — `received_at` Uses Server Process Clock Instead of Platform Event Timestamp

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR03-02 |
| **fr_tag** | [FR-03] |
| **category** | Technical / Data Integrity |
| **description** | `UnifiedMessage.received_at` is populated by `datetime.now(timezone.utc)` at parse time on the API server (`03-development/src/omnibot/models.py:46`). Both Telegram and LINE webhook payloads carry authoritative platform-side event timestamps — `message.date` (Unix epoch, Telegram) and `event.timestamp` (milliseconds, LINE). The server-side clock measures when the server parsed the payload, not when the user sent the message. Under three realistic conditions the divergence becomes operationally significant: (1) LINE's documented webhook retry behavior (RISK-FR01-02) re-delivers a timed-out event minutes later; the retried `UnifiedMessage` gets a `received_at` matching the retry, not the original send. (2) Queue or ASGI backlog under load introduces multi-second lag between event arrival and parse. (3) Replay-detection logic proposed in RISK-FR02-02 mitigation uses a ±5-minute recency window — server-clock `received_at` cannot be trusted as the event's true age for this purpose. |
| **likelihood** | 3 / 5 — Clock drift between parse time and event time is negligible in normal operation but systematic on retries and queue backlogs, both of which are expected production conditions (LINE retries every 30 s for up to 3 attempts). |
| **impact** | 3 / 5 — Corrupts SLA latency measurements (NFR-02 p95 metric), inflates `received_at` on retried LINE events causing them to appear as new messages rather than retries, and undermines the timestamp-based replay-detection TTL proposed in RISK-FR02-02 mitigation. Deduplication logic keyed on `received_at` will treat genuine retries as new events. |
| **mitigation** | (1) Populate `received_at` from the platform payload timestamp: `datetime.fromtimestamp(update["message"]["date"], tz=timezone.utc)` (Telegram) and `datetime.fromtimestamp(event["timestamp"] / 1000, tz=timezone.utc)` (LINE). (2) Retain `processed_at = datetime.now(timezone.utc)` as a separate field (or log annotation) for SLA measurement; do not conflate the two. (3) Validate that the platform timestamp falls within a ±24 h window of server clock and emit `WARN` on outliers to detect clock skew. (4) Update `tests/test_fr03.py` to assert that `received_at` matches the fixture payload timestamp, not `unittest.mock.ANY`. |
| **owner** | Platform Team |

**Citations** (HR-15): 03-development/src/omnibot/models.py:46 (`received_at` default factory — server clock), SPEC/omnibot-phase-1.md:340-351 (UnifiedMessage reference definition — `received_at` field), build/lib/omnibot/adapters/telegram.py:11-28 (Telegram parser — `message.date` not extracted), build/lib/omnibot/adapters/line.py:20-46 (LINE parser — `event.timestamp` not extracted), SRS.md:50 (FR-03 acceptance criterion — `received_at` field required), SAD.md:94 (LINE retries on missing 200 OK)

---

### RISK-FR03-03 — `raw_payload` Dict Interior-Mutable Despite `frozen=True` Dataclass

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR03-03 |
| **fr_tag** | [FR-03] |
| **category** | Technical / Correctness |
| **description** | `UnifiedMessage` is declared `frozen=True` (`03-development/src/omnibot/models.py:35`), which prevents reassignment of the `raw_payload` attribute reference. However, `frozen=True` does not deep-freeze the dict value: any code holding a reference to the `UnifiedMessage` can call `msg.raw_payload["key"] = "value"` or `msg.raw_payload.update(...)` without raising `FrozenInstanceError`. The test suite (`tests/test_fr03.py:27-36`) verifies that attribute reassignment raises `FrozenInstanceError` but does not test interior mutability. Two production-relevant consequences: (1) An adapter that parses a LINE batch payload and reuses the same `raw_payload` dict across multiple `UnifiedMessage` instances (e.g., via a shallow copy) will cause one instance's payload to reflect mutations intended for another. (2) Audit/logging code that annotates `raw_payload` post-construction (e.g., adding a `"_processed": True` key for idempotency marking) will silently mutate the "immutable" message, corrupting replay-detection checks that compare `raw_payload` snapshots. |
| **likelihood** | 2 / 5 — Not exploitable from the network; requires code in the same process to call `raw_payload[key] = ...`. The most likely vector is a test fixture that shares a dict literal across multiple `UnifiedMessage` constructions, or a logging middleware that annotates the dict for tracing. |
| **impact** | 3 / 5 — Silent data corruption: mutated `raw_payload` invalidates HMAC re-verification (FR-02) on the stored payload, corrupts audit logs, and breaks any downstream code that treats `raw_payload` as an immutable snapshot of the original webhook body for replay or forensic purposes. |
| **mitigation** | (1) In `UnifiedMessage.__post_init__`, store `raw_payload` as an immutable snapshot: `object.__setattr__(self, "raw_payload", types.MappingProxyType(raw_payload))`. This raises `TypeError` on any interior mutation attempt. (2) Where deep-frozen nested dicts are needed (Phase 2), use `frozendict` or serialize to `bytes` at construction. (3) Update `tests/test_fr03.py` to assert `msg.raw_payload["k"] = "v"` raises `TypeError`. (4) Guard the LINE batch parser against shared dict references by always constructing a fresh `dict(event)` per `UnifiedMessage`. |
| **owner** | Platform Team |

**Citations** (HR-15): 03-development/src/omnibot/models.py:35-48 (`UnifiedMessage` frozen dataclass definition), 03-development/src/omnibot/models.py:45 (`raw_payload: Dict[str, Any] = field(default_factory=dict)` — mutable default), tests/test_fr03.py:27-36 (immutability test — only covers attribute reassignment, not interior mutation), build/lib/omnibot/adapters/line.py:25-46 (LINE parser — single `events[0]` dict passed as `raw_payload`), SPEC/omnibot-phase-1.md:340-351 (frozen=True design intent)

---

### RISK-FR03-04 — `Platform.MESSENGER` and `Platform.WHATSAPP` Defined in Enum Without Adapter or Router Guard

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR03-04 |
| **fr_tag** | [FR-03] |
| **category** | Technical / Functional |
| **description** | The `Platform` enum defines four values: `TELEGRAM`, `LINE`, `MESSENGER`, and `WHATSAPP` (`03-development/src/omnibot/models.py:12-20`), but `PLATFORM_ROUTES` in the router only maps `"telegram"` and `"line"` (`build/lib/omnibot/router.py:15-18`). Phase 2 is the intended enablement date for `MESSENGER` and `WHATSAPP` (SRS.md:51). The gap creates two concrete risks. First, any code that iterates `list(Platform)` — e.g., a monitoring dashboard that checks signature-verifier coverage, or a test parametrization — will silently include `MESSENGER` and `WHATSAPP`, causing `KeyError` in the `VERIFIERS` registry (FR-02) and `AttributeError` in any `platform`-switched adapter call. Second, a utility or migration script that constructs `UnifiedMessage(platform=Platform.MESSENGER, ...)` will produce a structurally valid object that passes `test_platform_enum_completeness` (`tests/test_fr03.py:115-118`) but will be rejected or misrouted by every downstream consumer that only handles `TELEGRAM` or `LINE`. |
| **likelihood** | 3 / 5 — Realistic in test parametrization (`@pytest.mark.parametrize("p", list(Platform))`) and in monitoring code that checks coverage across all enum members. Phase 2 development work (beginning before this register is retired) will create the first concrete adapter code paths that touch `MESSENGER`/`WHATSAPP`, increasing blast radius. |
| **impact** | 3 / 5 — `KeyError` in `VERIFIERS` registry causes unhandled 500 rather than 400; a `UnifiedMessage` with `platform=Platform.MESSENGER` that reaches the knowledge layer will produce an unhandled branch in any platform-conditional logic, potentially returning an incorrect response or failing silently. Phase 2 regression risk if the adapter guard is not added before the enum values are activated. |
| **mitigation** | (1) Add a `SUPPORTED_PLATFORMS: frozenset[Platform] = frozenset({Platform.TELEGRAM, Platform.LINE})` constant in `models.py`; use it in the router and verifier to guard enum dispatch. (2) Annotate `Platform.MESSENGER` and `Platform.WHATSAPP` with a Phase 2 marker (e.g., docstring or `__phase__ = 2` class attribute) so grep and linters can flag premature use. (3) Add a CI assertion that `set(PLATFORM_ROUTES.keys())` maps 1:1 to `SUPPORTED_PLATFORMS` platform slugs, failing fast if a new platform is added to the enum without a corresponding adapter. (4) Update `tests/test_fr03.py` to assert that constructing `UnifiedMessage(platform=Platform.MESSENGER, ...)` succeeds at the model layer but that `resolve_route("messenger")` returns `None`. |
| **owner** | Platform Team |

**Citations** (HR-15): 03-development/src/omnibot/models.py:12-20 (`Platform` enum — all four values defined), build/lib/omnibot/router.py:15-18 (`PLATFORM_ROUTES` — telegram and line only), 01-requirements/SRS.md:51 (MESSENGER/WHATSAPP as Phase 2 scope), tests/test_fr03.py:115-118 (`test_platform_enum_completeness` — asserts all four values present), SPEC/omnibot-phase-1.md:327-332 (Platform enum reference definition)

---

## [FR-04] Input Sanitizer L2 — Detailed Risk Entries

---

### RISK-FR04-01 — `Cc`-Only Filter Preserves Bidirectional Override and Other `Cf` Format Characters

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR04-01 |
| **fr_tag** | [FR-04] |
| **category** | Security / Information Disclosure |
| **description** | The control-character filter in `sanitize()` (`03-development/src/omnibot/sanitizer/__init__.py:29`) removes only Unicode category `Cc` (C0/C1 control codes). Unicode category `Cf` — format characters — is not filtered. `Cf` includes bidi override characters (U+202A LEFT-TO-RIGHT EMBEDDING through U+202E RIGHT-TO-LEFT OVERRIDE, U+2066–U+2069 bidi isolates) and the BOM/ZWNBSP (U+FEFF). A caller can embed bidi overrides inside a message that visually appears benign in a left-to-right log viewer but is stored and processed with reversed character order, enabling log injection, visual spoofing of audit trails, and bypassing human review of escalated content. The SPEC reference implementation (`SPEC/omnibot-phase-1.md:377`) uses `c.isprintable() or c in "\n\t"` — Python's `isprintable()` returns `False` for all `Cf` characters, making the intended behaviour broader than the implemented `category == "Cc"` check. |
| **likelihood** | 3 / 5 — Bidi injection via U+202E (RIGHT-TO-LEFT OVERRIDE) is a documented CVE-class technique (e.g., Trojan Source); crafting such inputs requires no special tooling. The gap is invisible to unit tests because `tests/test_fr04.py:84-88` explicitly preserves ZWJ (U+200D, also `Cf`) as a design decision for emoji — but that decision implicitly passes all `Cf` chars including bidi overrides. |
| **impact** | 4 / 5 — A log line containing bidi overrides renders differently in a terminal or SIEM than it is stored, allowing an attacker to make malicious content appear as a benign audit entry. Escalated tickets processed by human agents (FR-05 escalation path) may show visually different content than what was actually received, undermining the integrity of the support workflow. |
| **mitigation** | (1) Extend the filter to also strip `Cf` characters that are not semantically required for emoji: strip U+202A–U+202E, U+2066–U+2069 (bidi), and U+FEFF (BOM) unconditionally; keep U+200D (ZWJ) only when flanked by emoji codepoints. (2) Alternatively, align with the SPEC `isprintable()` approach and add an explicit carve-out for ZWJ in emoji sequences. (3) Add a test asserting that `sanitize("Hello‮World")` removes U+202E. (4) Log a structured WARN (FR-09) when `Cf` bidi characters are stripped, so ops can detect probing attempts. |
| **owner** | Platform Team / SecOps |

**Citations** (HR-15): 03-development/src/omnibot/sanitizer/__init__.py:29 (`category(ch) == "Cc"` — `Cf` not filtered), SPEC/omnibot-phase-1.md:377 (reference uses `isprintable()` — broader exclusion), tests/test_fr04.py:84-88 (`test_zwj_emoji_preserved` — confirms `Cf` chars pass through), SRS.md:64-67 (FR-04 acceptance criteria — "remove non-printable control chars, keep `\n`, `\t`")

---

### RISK-FR04-02 — `ValueError` on Malformed Unicode Is Unhandled at the Call Site, Producing 500 + Retry Storm

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR04-02 |
| **fr_tag** | [FR-04] |
| **category** | Operational / Reliability |
| **description** | `sanitize()` raises `ValueError("Input text contains malformed Unicode: ...")` (`03-development/src/omnibot/sanitizer/__init__.py:21-22`) when `unicodedata.normalize("NFKC", text)` raises `UnicodeError` or `TypeError`. Neither the Telegram adapter (`build/lib/omnibot/adapters/telegram.py`), the LINE adapter (`build/lib/omnibot/adapters/line.py`), nor any documented call site catches this exception. An unhandled `ValueError` propagates through FastAPI's exception handlers as a 500 Internal Server Error. Telegram and LINE interpret a non-2xx response as a delivery failure and retry the webhook: LINE retries every 30 seconds for up to 3 attempts (SAD.md:94); Telegram queues the update for redelivery. If the malformed payload is persistent (e.g., a platform encoding edge case or a crafted test message), every retry produces another 500, generating a sustained retry storm and polluting structured logs with uncorrelated tracebacks rather than FR-09 structured error events. |
| **likelihood** | 3 / 5 — Python's `json.loads()` decodes valid UTF-8 and will not produce lone surrogates in the standard path; however, LINE and Telegram payloads that include emoji encoded as CESU-8, messages from third-party platform bridges, or deliberate fuzzing of the webhook endpoint can produce `str` values that trigger `UnicodeError` in `unicodedata.normalize`. The gap between decoding and normalization is narrow but non-zero in production. |
| **impact** | 3 / 5 — Each retry produces a 500 with no structured log entry; the FR-09 observability layer (RISK-FR01-02 context) receives no actionable event. Ops sees a spike in 500s without a per-request trace. On LINE, three retries consume the `replyToken`, making the original message un-repliable even after the issue is fixed. A sustained storm from a looped retry can exhaust ASGI worker threads. |
| **mitigation** | (1) Catch `ValueError` raised by `sanitize()` at the adapter parse boundary; log a structured `ERROR` event (FR-09) with `request_id`, platform, and the offending `repr(text[:100])`. (2) Return a 200 OK (with the message dropped) rather than 500 to prevent platform retry storms — document this as the "accept and discard" pattern for unprocessable payloads. (3) Add a FastAPI exception handler for `ValueError` at the app level as a safety net, converting it to a 422 with a sanitized error body. (4) Add `test_fr04.py` assertion covering the `sanitize(None)` and `sanitize("\udcff")` (surrogate) edge cases. |
| **owner** | Platform Team |

**Citations** (HR-15): 03-development/src/omnibot/sanitizer/__init__.py:18-22 (`try/except` block — raises `ValueError` to caller), 03-development/src/omnibot/sanitizer/__init__.py:1-4 (module docstring — no caller error-handling contract specified), SRS.md:64-68 (FR-04 acceptance criteria — no error-handling requirement stated), SAD.md:94 (LINE retry-on-timeout behaviour — applies equally to 500 responses)

---

### RISK-FR04-03 — L3 Pattern Matching Absent in Phase 1: NFKC-Normalized Injection Content Reaches Pipeline Unrestricted

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR04-03 |
| **fr_tag** | [FR-04] |
| **category** | Security / Functional |
| **description** | The sanitizer's docstring explicitly states: "Does NOT perform pattern matching — that is L3's responsibility" (`03-development/src/omnibot/sanitizer/__init__.py:13`). L3 (`PromptInjectionDefense`) is scoped to Phase 2 (`SPEC/omnibot-phase-1.md:372`). In Phase 1, the pipeline has no layer that filters or flags injection payloads — XSS strings, prompt-injection sequences, and SQL fragments all pass through `sanitize()` and are forwarded to the knowledge layer. Critically, NFKC normalization actively expands the attack surface: a sender encodes `<script>` using fullwidth characters (`＜ｓｃｒｉｐｔ＞`) — which would be visually detectable — and `sanitize()` canonicalises them to ASCII `<script>`, producing a clean attack payload from an obfuscated input. `tests/test_fr04.py:67-73` (`test_no_pattern_matching_performed`) confirms this behaviour is intentional at L2, but no compensating control exists at Phase 1. |
| **likelihood** | 4 / 5 — Any user of the bot can send fullwidth or homoglyph-encoded injection content; no authentication barrier exists at the webhook layer beyond signature verification. Phase 1 is the only deployed pipeline layer; L3 has no implementation date within the current sprint scope. The pattern is well-known and actively used in LLM prompt injection attacks. |
| **impact** | 3 / 5 — Injection payloads reaching the Phase 1 knowledge layer can manipulate rule matching, trigger spurious escalations, or — once a generative model is wired in Phase 2 — exfiltrate conversation context or override system instructions. In Phase 1 the knowledge layer is rule-based, limiting immediate damage; the risk escalates sharply when the generative model is added. |
| **mitigation** | (1) Add a minimal Phase 1 blocklist: reject or flag messages that, after sanitization, contain known prompt-injection lead phrases (e.g., "ignore previous instructions", `<script>`, `{{`) — this is a thin heuristic L3 proxy until Phase 2. (2) Log all post-sanitize content at DEBUG level (FR-09) with a `sanitized=True` flag to enable retrospective analysis of injection attempts before L3 ships. (3) Track Phase 2 L3 implementation as a blocking dependency for any generative-model integration. (4) Document in `SPEC/omnibot-phase-1.md` that NFKC normalization is a pre-condition for L3 pattern matching, not a substitute for it. |
| **owner** | Platform Team |

**Citations** (HR-15): 03-development/src/omnibot/sanitizer/__init__.py:13 (docstring — "Does NOT perform pattern matching — that is L3's responsibility"), tests/test_fr04.py:67-73 (`test_no_pattern_matching_performed` — confirms XSS passes through post-normalization), SPEC/omnibot-phase-1.md:372 (L3 = `PromptInjectionDefense`, Phase 2 scope), SRS.md:68 (FR-04 acceptance criterion — "不執行 pattern matching（Phase 2 L3 負責）")

---

### RISK-FR04-04 — All-Control-Char Input Silently Collapses to `""` with No Diagnostic Log

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR04-04 |
| **fr_tag** | [FR-04] |
| **category** | Technical / Observability |
| **description** | When a webhook payload contains a `content` field composed entirely of non-printable control characters (e.g., `"\x01\x02\x03"` or a NUL-padded filler), `sanitize()` strips every character and returns `""` after `strip()` (`03-development/src/omnibot/sanitizer/__init__.py:26-35`). The return value is indistinguishable from a legitimately empty message or a message with only whitespace (`tests/test_fr04.py:55-57` confirms this). No warning is emitted and the original pre-sanitization length is not preserved. Downstream consumers — the knowledge layer, escalation logic, and the `UnifiedMessage.content` field — receive `""` without any indication that content was present and discarded. This creates two problems: (1) the confidence-0 knowledge-layer path is triggered silently, matching RISK-FR01-03's empty-content scenario; (2) forensic log review cannot reconstruct that a non-empty (though control-char-only) payload was received, complicating incident analysis. |
| **likelihood** | 3 / 5 — Deliberate probing (fuzz testing, malformed-packet attacks) reliably produces control-char-only content; accidental occurrence arises from platform encoding bugs or message corruption in transit. LINE's batch webhook retry path (RISK-FR01-02) may re-deliver corrupted events. |
| **impact** | 2 / 5 — Knowledge layer receives `""` and follows the low-confidence path; no escalation is triggered and the user receives a generic response. The primary harm is observability loss: ops cannot distinguish "user sent nothing" from "user sent sanitized-away content". No data corruption or security bypass results directly. |
| **mitigation** | (1) In `sanitize()`, before returning, compare `len(result) == 0` against `len(text.strip()) > 0`; if the pre-strip input was non-empty but the result is empty, emit a structured `WARN` log (FR-09) including `original_length`, `stripped_length`, and platform `request_id`. (2) Return a named result type (`SanitizeResult(text=..., was_content_dropped=bool)`) rather than a bare `str` so call sites can branch explicitly. (3) Add a `test_fr04.py` assertion that `sanitize("\x01\x02\x03")` produces `""` AND (once the WARN log is added) that the log emits a `content_dropped` event. |
| **owner** | Platform Team |

**Citations** (HR-15): 03-development/src/omnibot/sanitizer/__init__.py:26-35 (control-char removal loop and `strip()` — no diagnostic on empty result), tests/test_fr04.py:55-57 (`test_only_whitespace` — `""` return with no warning, same path as all-control-char input), SRS.md:64-68 (FR-04 acceptance criteria — no requirement for empty-result signaling), 03-development/src/omnibot/sanitizer/__init__.py:9-10 (function docstring — no mention of empty-output semantics)

---

## [FR-05] PII Masking L4 — Detailed Risk Entries

---

### RISK-FR05-01 — International Phone Format Bypasses Phone Regex Patterns

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR05-01 |
| **fr_tag** | [FR-05] |
| **category** | Technical / Functional |
| **description** | `_TW_MOBILE` (pii/__init__.py:25) matches only the domestic prefix `09XX[-\s]XXX[-\s]XXX`. It does not match the international format `+886 9XX-XXX-XXX` (where the leading `0` is dropped in favour of `+886`) or parenthesized area codes `(09XX) XXX-XXX`. A user who copies a contact from a business-card app or an international-format address book will paste `+886912345678` or `+886-912-345-678`, which does not start with `09` and therefore passes `_TW_MOBILE.subn()` with zero substitutions. `_TW_LANDLINE` (pii/__init__.py:26) has the symmetric gap for landlines: `+886-2-XXXX-XXXX` bypasses the `\b0\d{1,2}` prefix anchor. The SPEC reference pattern (SPEC/omnibot-phase-1.md:408-411) provides `\d{10,11}` as an alternate branch to catch fully-concatenated digit runs regardless of prefix, but the implementation omits this branch entirely. |
| **likelihood** | 3 / 5 — International-format numbers appear regularly in business-context messages (customer-service, B2B support); LINE and Telegram do not normalize phone formats before delivering webhook payloads. |
| **impact** | 4 / 5 — An unmasked phone number stored in a DB write or emitted to a structured log constitutes a PII breach. PDPA (Taiwan Personal Data Protection Act) and NFR-06 (SAD.md:531-533) require all phone numbers to be masked before any persistence or log output; a single unmasked number is a notifiable data breach event. |
| **mitigation** | (1) Add an alternate branch to `_TW_MOBILE` covering 10–11 consecutive digit runs (`\d{10,11}`) as the SPEC specifies (SPEC/omnibot-phase-1.md:408-411). (2) Add a dedicated pass with `re.compile(r"\+886[-\s]?[0-9]{9,10}")` before the domestic passes to catch explicitly prefixed international format. (3) Add `tests/test_fr05.py` cases for `+886912345678`, `+886-912-345-678`, and `(09XX) XXX-XXX` asserting `[PHONE]` substitution. (4) Align mask token with SRS.md:80 — use `[phone_masked]` rather than `[PHONE]` so downstream log-scrubbing rules match the documented PII token format. |
| **owner** | Platform Team / SecOps |

**Citations** (HR-15): 03-development/src/omnibot/pii/__init__.py:25-26 (`_TW_MOBILE` and `_TW_LANDLINE` — `09` prefix anchor only, no `+886` branch), 03-development/src/omnibot/pii/__init__.py:74-81 (`mask_pii` phone substitution passes), SPEC/omnibot-phase-1.md:408-411 (reference `\d{10,11}` alternate branch — covers all-digit runs), SRS.md:80 (acceptance criterion — 10–11 digit format), tests/test_fr05.py:35-40 (`test_phone_without_dashes` — only tests domestic `0912345678`, not `+886` prefix)

---

### RISK-FR05-02 — `contains_sensitive_keywords()` Substring Match Produces False Positives; API Name Deviates from Spec

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR05-02 |
| **fr_tag** | [FR-05] |
| **category** | Technical / Functional |
| **description** | Two compounding issues in the escalation detection path. **First (false positives)**: `_SENSITIVE_KEYWORDS` (pii/__init__.py:39-47) includes the bare string `"110"`. `contains_sensitive_keywords()` (pii/__init__.py:96-98) uses `any(kw in text ...)` — a plain substring match with no word boundary. Any Taiwan address containing `110` (e.g., `信義路三段110號`) and any digit sequence containing `1100` or `2110` triggers escalation. Similarly, `"緊急"` matches `緊急聯絡人` (emergency contact person field, common in onboarding forms). False-positive escalations bypass the automated resolution path entirely, routing routine messages to human agents and degrading FCR (NFR-01). **Second (API contract mismatch)**: SRS.md:84 requires a `should_escalate()` function; SPEC/omnibot-phase-1.md:434 defines `PIIMasking.should_escalate()`. The implementation exposes `contains_sensitive_keywords()` (pii/__init__.py:96). Any Phase 2 code written against the spec's `should_escalate()` contract will raise `AttributeError` at runtime when importing from `omnibot.pii`. |
| **likelihood** | 4 / 5 — Taiwan addresses routinely contain numeric components such as `信義路三段110號`; the false-positive trigger is deterministic and immediate for any user sending a street address. The API name mismatch surfaces at the first Phase 2 import of `should_escalate`. |
| **impact** | 3 / 5 — False-positive escalations overload human agents and degrade FCR (NFR-01). An `AttributeError` on `should_escalate` import causes an unhandled exception at the Phase 2 module-load boundary, blocking the affected pipeline path entirely until patched. |
| **mitigation** | (1) Replace bare-string `"110"` with a regex pattern `re.compile(r"\b110\b")` and apply `p.search(text)` checks, consistent with the SPEC's approach (SPEC/omnibot-phase-1.md:413-416). (2) Add a context-aware exclusion for `"緊急"` when followed by `聯絡人` (e.g., use a negative lookahead). (3) Add `should_escalate` as a public alias: `should_escalate = contains_sensitive_keywords`, or rename the function to match the SRS contract. (4) Add a regression test asserting `contains_sensitive_keywords("信義路三段110號") is False`. |
| **owner** | Platform Team |

**Citations** (HR-15): 03-development/src/omnibot/pii/__init__.py:39-47 (`_SENSITIVE_KEYWORDS` — includes bare `"110"` and `"緊急"` with no word boundary), 03-development/src/omnibot/pii/__init__.py:96-98 (`contains_sensitive_keywords` — substring match, deviates from spec name), SPEC/omnibot-phase-1.md:413-416 (reference — `re.compile(p)` per keyword, not substring), SPEC/omnibot-phase-1.md:434 (`should_escalate()` — mandated API name), SRS.md:84 (`should_escalate()` acceptance criterion), tests/test_fr05.py:82-90 (`test_sensitive_keyword_triggers_escalation` — does not test address-number false positives)

---

### RISK-FR05-03 — PII-Type Detection on Original `text` After Substitution on `result` Inflates `pii_types` for Overlapping Patterns

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR05-03 |
| **fr_tag** | [FR-05] |
| **category** | Technical / Correctness |
| **description** | `mask_pii()` applies substitutions sequentially on a mutable `result` variable, but the detection guards (`_EMAIL.search(text)` at pii/__init__.py:83 and `_TW_ADDRESS.search(text)` at pii/__init__.py:88) search the original `text` argument — not the already-masked `result`. When a string contains a token matching multiple patterns — for example a phone number embedded in an email-like token (`09XX@example.com`) or an address string whose digit components match the landline pattern — the phone pass masks the overlapping token in `result`, but the email/address detection guard still finds a match in `text`, appending `"email"` or `"address"` to `pii_types` even when the subsequent `_EMAIL.subn()`/`_TW_ADDRESS.subn()` call finds zero occurrences in `result`. The output is a `PIIMaskResult` claiming PII types that were not actually masked, corrupting the NFR-06 audit record. The SPEC (SPEC/omnibot-phase-1.md:418-432) avoids this entirely by running each pattern's `finditer()` on the already-mutated `masked` string — detection and substitution always share the same target. |
| **likelihood** | 3 / 5 — Overlapping patterns are unusual in typical customer messages but reliably triggered by fuzzing or by users who include multiple contact formats. The split detection/substitution target is a latent defect active in every `mask_pii()` call; any overlap will trigger it. |
| **impact** | 3 / 5 — A `PIIMaskResult.pii_types` list claiming a PII type that was not masked misleads audit log aggregation (NFR-06), inflating PII incident counts and producing false compliance reports. Downstream code branching on `"email" in result.pii_types` will invoke the email-PII path unnecessarily, potentially triggering unneeded PDPA notification workflows. |
| **mitigation** | (1) Change `_EMAIL.search(text)` (pii/__init__.py:83) and `_TW_ADDRESS.search(text)` (pii/__init__.py:88) to search `result` — the already-phone-masked string — rather than the original `text`. (2) Alternatively, adopt the SPEC's single-pass dict iteration (`for pii_type, pattern in PATTERNS.items(): matches = list(pattern.finditer(masked))`) which eliminates the split entirely. (3) Add a `tests/test_fr05.py` case asserting that `mask_pii("0912@example.com")` produces `mask_count == 1` and `pii_types == ["phone"]`, not `["phone", "email"]`. |
| **owner** | Platform Team |

**Citations** (HR-15): 03-development/src/omnibot/pii/__init__.py:65-93 (`mask_pii` — substitution on `result`, detection on `text`), 03-development/src/omnibot/pii/__init__.py:83 (`_EMAIL.search(text)` — original text, not masked result), 03-development/src/omnibot/pii/__init__.py:88 (`_TW_ADDRESS.search(text)` — original text, not masked result), SPEC/omnibot-phase-1.md:418-432 (`mask()` — `pattern.finditer(masked)` on evolving masked string, no detection/substitution split), SRS.md:83 (acceptance criterion — rightmost-first replacement to avoid index offset), SAD.md:203-204 (inter-type precedence — sequential passes on already-masked text)

---

### RISK-FR05-04 — `PIIMaskResult` Not `frozen=True` — Mutable Fields Undermine NFR-06 Compliance Audit Trail

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR05-04 |
| **fr_tag** | [FR-05] |
| **category** | Technical / Data Integrity |
| **description** | `PIIMaskResult` is declared `@dataclass` without `frozen=True` (pii/__init__.py:12). The SPEC defines it as `@dataclass(frozen=True)` (SPEC/omnibot-phase-1.md:388-394). Both `masked_text: str` and `pii_types: List[str]` are mutable after construction. `pii_types` is backed by a `field(default_factory=list)` (pii/__init__.py:20), so any caller can invoke `result.pii_types.append("phone")` or `result.pii_types.clear()` without raising `FrozenInstanceError`. SAD.md:531-533 (NFR-06) specifies that PIIMaskerL4's output is the authoritative record of PII categories found in each message, written to the structured audit log (FR-09) without post-construction mutation. A logging middleware that annotates `result.pii_types` for distributed tracing silently corrupts the persisted audit record. Additionally, `result.masked_text = original_text` reassignment is possible without `frozen=True`, allowing unmasked content to be stored under the appearance of a sanitized value, defeating PII masking entirely while bypassing any type-level protection. |
| **likelihood** | 2 / 5 — Not exploitable from the network; requires co-located Python code with module import access. Most likely vector: a Phase 2 logging middleware annotating `pii_types` for tracing, or a test fixture that shares a `PIIMaskResult` instance across multiple assertions and mutates it between checks. |
| **impact** | 3 / 5 — Corrupted `pii_types` in the audit log produces inaccurate PDPA/NFR-06 compliance reports. A mutated `masked_text` storing unmasked PII would violate PDPA data minimisation obligations and constitute a notifiable incident if the record were disclosed. |
| **mitigation** | (1) Add `frozen=True` to the `@dataclass` declaration: `@dataclass(frozen=True)` (pii/__init__.py:12). (2) Change `pii_types: List[str] = field(default_factory=list)` to `pii_types: tuple = field(default_factory=tuple)` — `frozen=True` prevents attribute reassignment but does not deep-freeze a `List`; a `tuple` provides interior immutability. (3) Add a `tests/test_fr05.py` assertion that `result.pii_types.append("x")` raises `AttributeError` (tuple) or that `result.masked_text = ""` raises `FrozenInstanceError`. (4) Document the immutability contract in the `PIIMaskResult` docstring so Phase 2 authors do not attempt mutation. |
| **owner** | Platform Team |

**Citations** (HR-15): 03-development/src/omnibot/pii/__init__.py:12-20 (`PIIMaskResult` — `@dataclass` without `frozen=True`, `pii_types: List[str]` mutable), SPEC/omnibot-phase-1.md:388-394 (`PIIMaskResult` — `@dataclass(frozen=True)` — spec mandates frozen), SAD.md:531-533 (NFR-06 — PIIMaskerL4 output is compliance-audit record, must not be mutated post-construction), tests/test_fr05.py:93-96 (`test_escalation_flag_dataclass` — no immutability assertion on `PIIMaskResult`)

---

## [FR-06] Rate Limiter Token Bucket — Detailed Risk Entries

---

### RISK-FR06-01 — Unbounded `_buckets` Dict Enables OOM Denial-of-Service

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR06-01 |
| **fr_tag** | [FR-06] |
| **category** | Security / Availability |
| **description** | `RateLimiter._buckets` is an unbounded `Dict[str, TokenBucket]` (`03-development/src/omnibot/rate_limiter/__init__.py:49`) with no eviction, TTL, or maximum-size guard. Every distinct `user_id` string passed to `allow()` inserts a new `TokenBucket` that is never removed. An attacker (or a misconfigured upstream component) that sends webhook payloads with unique `platform:user_id` values — trivially achievable by cycling numeric suffixes — causes `_buckets` to grow monotonically. Each `TokenBucket` instance holds a `threading.Lock`, a float, and two float timestamps, adding roughly 200–300 bytes per entry. At 1 million unique keys the process heap expands by ~300 MB; at 10 million the container OOM-killer terminates the process, dropping all in-flight webhook requests for every platform. The SPEC reference implementation (`SPEC/omnibot-phase-1.md:473`) also uses a bare `dict` with no eviction, meaning the gap is inherited from upstream design. |
| **likelihood** | 3 / 5 — Requires adversarial webhook payloads with unique user_ids or a misconfigured platform bridge that mints new identifiers per-request; no authentication barrier prevents arbitrary user_ids from arriving at the webhook layer beyond FR-02 signature verification. |
| **impact** | 4 / 5 — OOM crash terminates the entire FastAPI process, dropping all concurrent requests across all platforms until the container scheduler restarts it. No graceful degradation path; all users lose service during the restart window. PostgreSQL connections are also severed, potentially corrupting any in-flight writes. |
| **mitigation** | (1) Cap `_buckets` with an LRU eviction policy using `functools.lru_cache` or `cachetools.LRUCache(maxsize=50_000)` so stale user buckets are evicted as new ones arrive. (2) Add a periodic background sweep (e.g., every 60 s) that removes buckets whose `_last_refill` is older than a configurable TTL (e.g., 5 × bucket capacity / refill_rate seconds). (3) Expose a `len(self._buckets)` metric via FR-09 structured logging so ops can alert on `bucket_count > threshold`. (4) Add a `tests/test_fr06.py` assertion that `allow()` with 100 000 distinct user_ids does not raise `MemoryError` and that `len(limiter._buckets)` is bounded. |
| **owner** | Platform Team / SecOps |

**Citations** (HR-15): 03-development/src/omnibot/rate_limiter/__init__.py:49 (`_buckets: Dict[str, TokenBucket] = {}` — unbounded, no eviction), 03-development/src/omnibot/rate_limiter/__init__.py:55-58 (new `TokenBucket` inserted on every unseen user_id — no size limit), SPEC/omnibot-phase-1.md:473 (`_buckets: dict[str, TokenBucket]` in reference — eviction equally absent), tests/test_fr06.py:35-42 (`test_rate_limiter_per_user_isolation` — verifies independent buckets but never tests cardinality bound), SRS.md:99 (`platform:user_id` as bucket key — key space is per-platform, unbounded)

---

### RISK-FR06-02 — `allow()` Return Value Not Wired to HTTP 429 — Rate Limiting Is Inoperative

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR06-02 |
| **fr_tag** | [FR-06] |
| **category** | Technical / Functional |
| **description** | SRS.md:101 requires that requests exceeding the token-bucket limit return `429 RATE_LIMIT_EXCEEDED`. The implementation's `RateLimiter.allow(user_id)` returns a `bool` (`03-development/src/omnibot/rate_limiter/__init__.py:52-59`) but is not called from any FastAPI route handler, middleware, or dependency. No `HTTPException(status_code=429)` is raised anywhere in the codebase when `allow()` returns `False`. The `RateLimiter` class is instantiated only in `tests/test_fr06.py` — it has no integration with the webhook request pipeline. The SPEC reference implementation (`SPEC/omnibot-phase-1.md:469-483`) similarly provides only the `check()` method and leaves HTTP wiring to the caller, but the Phase 1 app does not implement that wiring. The result is that every webhook request is processed regardless of per-user request rate, making FR-06 acceptance criterion (SRS.md:96-101) entirely unmet at runtime. |
| **likelihood** | 4 / 5 — The gap is structural and active in every deployed request; no user is rate-limited in Phase 1, making this not a latent risk but an immediate functional deficiency. Any load test or abuse scenario will confirm the bypass. |
| **impact** | 4 / 5 — Without rate limiting, a single user can submit unlimited webhook requests per second, exhausting ASGI worker threads, PostgreSQL connections, and knowledge-layer query budgets, potentially degrading service for all other users. NFR compliance (SRS.md:285) is unmet, and the 100 rps per-user contract advertised to platform operators is not enforced. |
| **mitigation** | (1) Instantiate a module-level `RateLimiter` singleton in `app.py` and add a FastAPI dependency (`Depends`) that calls `limiter.allow(f"{platform}:{user_id}")` and raises `HTTPException(status_code=429, detail="RATE_LIMIT_EXCEEDED")` when it returns `False`. (2) Wire the dependency into the Telegram and LINE webhook route handlers as a parameter. (3) Add an integration test in `tests/test_fr06.py` that posts > 100 requests via the FastAPI `TestClient` and asserts the 101st returns HTTP 429. (4) Emit a structured `WARN` log (FR-09) on each 429 emission including `platform`, `user_id`, and `request_id` for ops alerting. |
| **owner** | Platform Team |

**Citations** (HR-15): 03-development/src/omnibot/rate_limiter/__init__.py:52-59 (`allow()` — returns `bool`, no FastAPI integration at call site), SRS.md:101 (FR-06 acceptance criterion — exceeded requests must return `429 RATE_LIMIT_EXCEEDED`), SRS.md:285 (`FR-06 | Default rate limit | 100 rps` — NFR table entry), SPEC/omnibot-phase-1.md:469-483 (reference `RateLimiter.check()` — HTTP wiring absent in reference too), tests/test_fr06.py:53-56 (`test_rate_limiter_capacity_zero_blocks_all` — unit test only; no HTTP-layer assertion)

---

### RISK-FR06-03 — Global `_lock` on `RateLimiter` Serializes All Per-User Bucket Lookups

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR06-03 |
| **fr_tag** | [FR-06] |
| **category** | Performance / Operational |
| **description** | `RateLimiter.allow()` acquires a single global `threading.Lock` (`self._lock`) at the top of every call (`03-development/src/omnibot/rate_limiter/__init__.py:54`) to protect the `_buckets` dict lookup and potential insertion. Under the default 100 rps per-user limit with, for example, 500 concurrent active users, the FastAPI ASGI worker pool submits 50 000 requests per second all competing for the same `self._lock` even though their `user_id` keys are fully independent. The lock is released before `bucket.consume()` is called (line 59), meaning `TokenBucket._lock` (per-bucket) provides the actual consume-side thread safety; the global lock adds serialization overhead for dict operations that Python's GIL already makes atomic for `dict.get()`. The SPEC reference implementation (`SPEC/omnibot-phase-1.md:469-483`) has no lock at all on the `RateLimiter`, relying implicitly on GIL-protected dict access — a simpler model with less contention. |
| **likelihood** | 3 / 5 — Lock contention is negligible at low request volumes but measurable under the 100 rps × multi-user load that FR-06 is designed to handle; the bottleneck becomes significant once concurrent-user count exceeds ASGI thread-pool size (typically 10–20 threads). |
| **impact** | 3 / 5 — Increased tail latency for rate-limit checks adds to the webhook response time budget (NFR-02, < 3 s p95). Under extreme load, `allow()` becomes the synchronization bottleneck across all user traffic, adding queuing delay that can push p95 latency past the SLA threshold even for users whose buckets are not exhausted. |
| **mitigation** | (1) Remove the global `_lock` and rely on the GIL for `dict.get()` / `dict.__setitem__` atomicity (CPython guarantee): two concurrent inserts for the same new key are idempotent because both would create equivalent `TokenBucket` instances. (2) If non-CPython compatibility is required, replace with a `threading.Lock` per user_id prefix shard (e.g., 256 shards by `hash(user_id) % 256`) to reduce contention. (3) If adopting an async framework (Phase 2), replace `threading.Lock` with `asyncio.Lock` per bucket to avoid blocking the event loop. (4) Add a micro-benchmark in CI (`tests/test_fr06.py`) that asserts `allow()` latency p99 < 1 ms under 100 concurrent callers. |
| **owner** | Platform Team |

**Citations** (HR-15): 03-development/src/omnibot/rate_limiter/__init__.py:50 (`self._lock = threading.Lock()` — single global lock), 03-development/src/omnibot/rate_limiter/__init__.py:54-58 (global lock scope covers dict lookup and insert), 03-development/src/omnibot/rate_limiter/__init__.py:59 (`return bucket.consume()` — outside global lock, inside per-bucket lock), 03-development/src/omnibot/rate_limiter/__init__.py:25 (`TokenBucket._lock` — per-bucket lock for consume), SPEC/omnibot-phase-1.md:469-483 (reference `RateLimiter` — no locking; relies on GIL)

---

### RISK-FR06-04 — In-Memory Bucket State Lost on Process Restart Enables Rate Limit Bypass

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR06-04 |
| **fr_tag** | [FR-06] |
| **category** | Technical / Operational |
| **description** | All `TokenBucket` instances and their `_tokens` float values live exclusively in the `RateLimiter._buckets` dict in the Python process heap (`03-development/src/omnibot/rate_limiter/__init__.py:20-25, 49`). A process restart — triggered by a rolling deployment, container OOM recovery (see RISK-FR06-01), or watchdog restart — resets every user's bucket to full capacity (`_tokens = float(capacity) = 100.0`). A user who has exhausted their bucket and is receiving 429 responses can immediately restore 100 tokens by triggering a container restart (e.g., by exploiting RISK-FR06-01) or by timing their burst to coincide with a known deploy window. In a multi-replica deployment (two Docker Compose service replicas behind a load balancer), each replica maintains independent state; a user rate-limited on replica A can freely use replica B with a full 100-token bucket, effectively multiplying the per-user limit by the number of replicas. The SPEC reference (`SPEC/omnibot-phase-1.md:469-483`) is identically in-memory with no persistence strategy documented. |
| **likelihood** | 3 / 5 — Rolling deployments are routine (every merge to main triggers a container redeploy); multi-replica setups are the recommended production configuration for NFR-02 availability. Both conditions are expected in production, not edge cases. |
| **impact** | 3 / 5 — A determined bad actor can sustain traffic above the nominal 100 rps limit across deploys, degrading knowledge-layer query capacity and ASGI thread availability for legitimate users. The bypass does not grant authentication privileges or data access, but it undermines the abuse-prevention guarantee (SRS.md:94) and inflates infrastructure costs. |
| **mitigation** | (1) Back `_buckets` with a shared Redis store keyed on `platform:user_id` using Redis's atomic `INCRBY` + `EXPIRE` pattern or the token-bucket Lua script, so bucket state survives restarts and is consistent across replicas. (2) As a lower-effort interim: add a startup log (`WARN`) that reports `_buckets` was reset to empty on init, enabling ops to detect post-restart rate-limit amnesia in the structured log stream. (3) Document the ephemeral rate-limit behavior in MONITORING_PLAN.md so on-call staff are aware that 429 suppression resets on restart. (4) In the multi-replica case, use sticky session routing (platform:user_id hash) at the load balancer as a stopgap until Redis-backed state is implemented. |
| **owner** | Platform Team / DevOps |

**Citations** (HR-15): 03-development/src/omnibot/rate_limiter/__init__.py:20-25 (`TokenBucket.__init__` — `_tokens` and `_last_refill` initialized in process memory, no persistence), 03-development/src/omnibot/rate_limiter/__init__.py:46-49 (`RateLimiter.__init__` — `_buckets = {}` constructed fresh on every instantiation), SPEC/omnibot-phase-1.md:469-483 (reference `RateLimiter` — in-memory only, no Redis or persistence layer), SRS.md:91-101 (FR-06 acceptance criteria — per-user isolation required; no persistence requirement stated), tests/test_fr06.py:35-42 (`test_rate_limiter_per_user_isolation` — single-process test; cross-replica isolation not covered)

---

## [FR-07] Knowledge Layer V1 Rule Match — Detailed Risk Entries

---

### RISK-FR07-01 — Partial-Match Confidence 0.70 Always Escalates: `<= 0.7` Threshold Conflicts with SAD `>= 0.7` Reply Contract

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR07-01 |
| **fr_tag** | [FR-07] |
| **category** | Technical / Functional |
| **description** | The SPEC `_rule_match_list()` assigns a confidence of exactly `0.70` to any partial match — a row where the query text is found via `ILIKE` or `ANY(keywords)` but is not a full-string substring of `question` (SPEC/omnibot-phase-1.md:532). The implementation's `query()` method uses `escalate = best_confidence <= 0.7` (03-development/src/omnibot/knowledge/__init__.py:52), which means any result at confidence `0.70` triggers escalation. This directly conflicts with SAD.md:244, which specifies `>= 0.7 → reply; < 0.7 → escalate`. The SPEC's own `query()` also uses `> 0.7` (SPEC/omnibot-phase-1.md:507), creating an inconsistency between SPEC and SAD: partial matches (the one confidence tier between no-match and exact-match) are never returned as automated replies in either the SPEC or the implementation, despite SAD designating them as successful matches. In production this means every partial-knowledge-base hit — ILIKE match without full containment — is silently routed to a human agent rather than returning the matching rule's canned answer. `tests/test_fr07.py:32-37` (`test_partial_match_fuzzy`) only asserts `result.confidence > 0`, not that a 0.7 partial match is replied rather than escalated, leaving the boundary behaviour unverified. |
| **likelihood** | 4 / 5 — Every partial-confidence match (the intended middle tier of FR-07) deterministically escalates; this fires on any user query that triggers an ILIKE hit without full containment, which is the common case for abbreviated or colloquial phrasing in bilingual customer-service interactions. |
| **impact** | 4 / 5 — All partial matches are permanently routed to human agents, collapsing the three-tier confidence model (0.95 exact / 0.70 partial / 0.0 none) into a binary system (0.95 exact / escalate). FCR (NFR-01) degrades because knowledge-base partial hits that should auto-reply inflate the escalation queue instead. |
| **mitigation** | (1) Align the threshold to SAD.md:244: change `escalate = best_confidence <= 0.7` (knowledge/__init__.py:52) and `source="rule_match" if best_confidence > 0.7` (knowledge/__init__.py:59) to use `< 0.7` and `>= 0.7` respectively. (2) Resolve the SPEC/SAD conflict by updating SPEC/omnibot-phase-1.md:507 from `confidence > 0.7` to `confidence >= 0.7` so all three documents are consistent. (3) Add a `tests/test_fr07.py` assertion: a single-keyword rule with one keyword matched returns `escalate=False` when `confidence == 0.7` (achievable with a 7-of-10 keyword rule). (4) Add `test_partial_match_boundary` asserting that `query()` on a partial match does not set `escalate=True`. |
| **owner** | Platform Team |

**Citations** (HR-15): 03-development/src/omnibot/knowledge/__init__.py:52 (`escalate = best_confidence <= 0.7`), 03-development/src/omnibot/knowledge/__init__.py:59 (`source="rule_match" if best_confidence > 0.7` — boundary at > not >=), SPEC/omnibot-phase-1.md:507 (`if result.confidence > 0.7` — same strict inequality), SPEC/omnibot-phase-1.md:532 (`confidence=0.95 if … else 0.7` — partial match returns exactly 0.70), 02-architecture/SAD.md:244 (`>= 0.7 → reply; < 0.7 → escalate` — requires inclusive bound), 01-requirements/SRS.md:115 (部分匹配信心度 0.7), tests/test_fr07.py:32-37 (`test_partial_match_fuzzy` — asserts `confidence > 0` only, no escalation assertion)

---

### RISK-FR07-02 — `QueryResult` Not `frozen=True`; Missing `id` and `knowledge_id` Fields Break Phase 2 Contract

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR07-02 |
| **fr_tag** | [FR-07] |
| **category** | Technical / Data Integrity |
| **description** | The SPEC defines `KnowledgeResult` as `@dataclass(frozen=True)` with five fields: `id: int`, `content: str`, `confidence: float`, `source: str`, and `knowledge_id: Optional[int]` (SPEC/omnibot-phase-1.md:494-500). The implementation exposes `QueryResult` — a plain `@dataclass` without `frozen=True` (03-development/src/omnibot/knowledge/__init__.py:13) — and omits both `id` and `knowledge_id`. SAD.md:158 specifies `knowledge_id: int` as the field logged by the pipeline INFO entry after every successful knowledge match (`log INFO: knowledge_match, confidence, knowledge_id, user_id` — SAD.md:474). Phase 2 pipeline code that accesses `result.knowledge_id` will raise `AttributeError` at the first knowledge-layer call, blocking the entire request path until patched. Without `frozen=True`, any middleware or logging decorator can mutate `result.confidence` or `result.response` post-construction, silently corrupting the audit log (NFR-06) and undermining the reliability of the `confidence_score` written to the `messages` table (SPEC/omnibot-phase-1.md:713-714). The mutable `source` field can also be overwritten from `"rule_match"` to `"escalate"` after the fact, corrupting `knowledge_source` analytics (SPEC/omnibot-phase-1.md:834-843). |
| **likelihood** | 4 / 5 — Phase 2 integration is the next sprint scope; any code importing `KnowledgeResult` per the SPEC/SAD contract will hit `AttributeError` on `knowledge_id` immediately. The mutable fields compound every log-annotation pass with a silent corruption risk. |
| **impact** | 3 / 5 — `AttributeError` on `knowledge_id` blocks the Phase 2 request path entirely until patched; corrupted `confidence` or `source` fields produce incorrect compliance reports and mislead FCR analytics (NFR-01). In Phase 1 the missing fields cause no immediate runtime failure but mask the gap until Phase 2 integration. |
| **mitigation** | (1) Add `frozen=True` to the `@dataclass` declaration: `@dataclass(frozen=True)` (knowledge/__init__.py:13). (2) Add `id: int` and `knowledge_id: Optional[int]` fields to `QueryResult` matching SPEC/omnibot-phase-1.md:494-500; populate them from rule index or DB row `id` when available, `-1` for no-match escalation path. (3) Rename `QueryResult` to `KnowledgeResult` (or provide a public alias) to align with the SPEC/SAD contract and avoid Phase 2 import failures. (4) Add `tests/test_fr07.py` assertions: (a) `result.confidence = 0.5` raises `FrozenInstanceError`; (b) `result.knowledge_id` is accessible without `AttributeError`; (c) escalation path sets `knowledge_id = -1`. |
| **owner** | Platform Team |

**Citations** (HR-15): 03-development/src/omnibot/knowledge/__init__.py:13 (`@dataclass` — no `frozen=True`), 03-development/src/omnibot/knowledge/__init__.py:13-22 (`QueryResult` definition — `id` and `knowledge_id` absent), SPEC/omnibot-phase-1.md:494-500 (`@dataclass(frozen=True)` — `id`, `content`, `confidence`, `source`, `knowledge_id`), SPEC/omnibot-phase-1.md:540-545 (`_escalate()` returns `id=-1` — sentinel absent in implementation), 02-architecture/SAD.md:158-160 (`KnowledgeResult` fields — `knowledge_id: int` required), 02-architecture/SAD.md:474 (pipeline INFO log includes `knowledge_id`), tests/test_fr07.py:49-55 (`test_query_result_dataclass` — no immutability assertion, no `knowledge_id` field check)

---

### RISK-FR07-03 — Case-Sensitive `kw in text` Match vs Case-Insensitive ILIKE — Mixed-Case English Keywords Miss

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR07-03 |
| **fr_tag** | [FR-07] |
| **category** | Technical / Functional |
| **description** | The rule matching loop uses Python's `kw in text` containment test (03-development/src/omnibot/knowledge/__init__.py:45), which is case-sensitive. The SPEC SQL uses `question ILIKE '%{query_text}%'` and `{query_text} = ANY(keywords)` (SPEC/omnibot-phase-1.md:521-522), both of which are case-insensitive in PostgreSQL. English keywords registered in the default rule set — `"return"` and `"order"` (knowledge/__init__.py:66-67) — will fail to match user input typed as `"Return"`, `"ORDER"`, `"RETURN"`, or mixed-case variants. A user typing "I want to RETURN my order" matches neither the `"return"` nor the `"order"` rule under case-sensitive comparison and receives a no-match escalation instead of the configured canned answer. Chinese-language keywords are unaffected (no case dimension), but bilingual customer-service bots serving international users or using product codes, SKU strings, or command words in English are exposed immediately. The confidence inflation from case-normalized matches that would hit partial confidence (0.70) is lost; the path falls to confidence 0.0 and escalates. |
| **likelihood** | 3 / 5 — English keywords appear in the default rule set and are a first-class use case in bilingual customer-service bots; mixed-case input is normal for all-caps emphasis and auto-corrected mobile keyboard input. The gap is deterministic for any English keyword with case variation in user input. |
| **impact** | 3 / 5 — Missed matches inflate the escalation queue with queries that should have been answered automatically, degrading FCR (NFR-01) and adding unnecessary load to human agents. No data is corrupted; the failure mode is silent under-matching rather than incorrect matching. |
| **mitigation** | (1) Normalize both keyword and input text to lowercase before comparison: change `kw in text` (knowledge/__init__.py:45) to `kw.lower() in text.lower()`, mirroring ILIKE case-folding semantics. (2) When PostgreSQL is wired in Phase 2, rely on the SQL `ILIKE` predicate and `= ANY(keywords)` operator rather than Python-level case folding. (3) Add `tests/test_fr07.py` assertion: a rule with keyword `"return"` matches query text `"RETURN"` and `"Return"`. (4) Apply the same normalization to `_default_kb` rules so the Phase 1 in-memory store is consistent with the Phase 2 SQL behaviour. |
| **owner** | Platform Team |

**Citations** (HR-15): 03-development/src/omnibot/knowledge/__init__.py:45 (`kw in text` — case-sensitive Python containment), 03-development/src/omnibot/knowledge/__init__.py:66-67 (default rules with English keywords `"return"`, `"order"`), SPEC/omnibot-phase-1.md:521-522 (`ILIKE %s` + `= ANY(keywords)` — case-insensitive SQL operators), SPEC/omnibot-phase-1.md:532 (`query_text.lower() in row["question"].lower()` — SPEC explicitly lowercases for exact-match check), 01-requirements/SRS.md:113 (`ILIKE` acceptance criterion — implies case-insensitive matching), tests/test_fr07.py:14-19 (`test_exact_match_high_confidence` — uses Chinese only; no English case-variation test)

---

### RISK-FR07-04 — No `is_active` Guard or `version DESC` Ordering — Deprecated Rules Permanently Active

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR07-04 |
| **fr_tag** | [FR-07] |
| **category** | Technical / Operational |
| **description** | SRS.md:114 requires `WHERE is_active = TRUE` and SRS.md:116 requires `ORDER BY version DESC` as acceptance criteria for FR-07. The `KnowledgeBase` in-memory store (knowledge/__init__.py:32-37) has no `is_active` concept and no version tracking: every rule added via `add_rule()` is permanently active and matched in insertion order. When Phase 2 wires the PostgreSQL `knowledge_base` table — which contains an `is_active BOOL` column and a `version INT` column (SPEC/omnibot-phase-1.md:725-731) — the absence of these guards in the query layer means: (1) deactivated rules (is_active=FALSE, e.g., outdated promotional responses or deprecated product lines) continue to match alongside current rules, potentially returning stale or incorrect answers to users; (2) if multiple versions of the same rule exist (v1 and v2), the lowest-version (oldest) entry may shadow the canonical current answer depending on database storage order, since there is no `ORDER BY version DESC` clause to guarantee the latest version is selected first (SPEC/omnibot-phase-1.md:523). SAD.md:239 and SAD.md:242 list both constraints as required logical invariants for `KnowledgeRepository`. |
| **likelihood** | 3 / 5 — The risk is latent in Phase 1 (no PostgreSQL) but materializes at the first Phase 2 database wiring. Content teams regularly deactivate and version-update rules as product information changes; without the guards, every rule update produces a regression path. |
| **impact** | 3 / 5 — Deactivated rules returning stale answers erode user trust and can violate regulatory requirements for current product/pricing information. Stale rule shadowing causes inconsistent responses where different users (hitting different DB replicas or query plans) receive different answers for identical queries. |
| **mitigation** | (1) Add an `is_active: bool = True` field to the `add_rule()` contract (knowledge/__init__.py:35-37) and filter on `is_active=True` in `query()` so Phase 1 in-memory behaviour mirrors the SQL constraint. (2) Add a `version: int = 1` field to the rule dict and sort candidates by `version DESC` before selecting the best match, mirroring `ORDER BY version DESC` (SPEC/omnibot-phase-1.md:523). (3) When Phase 2 wires PostgreSQL, validate that the SQL template includes both `AND is_active = TRUE` (as a top-level predicate, not inside the ILIKE OR group per SAD.md:241) and `ORDER BY version DESC LIMIT 5`. (4) Add a `tests/test_fr07.py` case: register two versions of the same rule (v1 old answer, v2 new answer) and assert the higher-version answer is returned; register a rule with `is_active=False` and assert it is never matched. |
| **owner** | Platform Team |

**Citations** (HR-15): 03-development/src/omnibot/knowledge/__init__.py:32-37 (`KnowledgeBase.__init__` and `add_rule()` — no `is_active` or `version` fields), 03-development/src/omnibot/knowledge/__init__.py:44-50 (match loop — no `is_active` filter, no version-based ordering), SPEC/omnibot-phase-1.md:519-524 (`WHERE is_active = TRUE … ORDER BY version DESC LIMIT 5` — SQL template with both constraints), SPEC/omnibot-phase-1.md:725-731 (`knowledge_base` table schema — `is_active BOOL`, `version INT`), 02-architecture/SAD.md:239 (`is_active = TRUE` logical constraint), 02-architecture/SAD.md:242 (`ORDER by version DESC, take first result`), 01-requirements/SRS.md:114 (`is_active = TRUE` acceptance criterion), 01-requirements/SRS.md:116 (`version DESC` acceptance criterion)

---

## [FR-08] Basic Escalation Manager — Detailed Risk Entries

---

### RISK-FR08-01 — `conversation_id` Type Mismatch: `str` in Implementation vs. `int` in SPEC Contract and DB Schema

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR08-01 |
| **fr_tag** | [FR-08] |
| **category** | Technical / Data Integrity |
| **description** | The SPEC defines `EscalationRequest.conversation_id` as `int` (SPEC/omnibot-phase-1.md:560), and the `escalation_queue` schema declares `conversation_id INTEGER REFERENCES conversations(id) UNIQUE` (SPEC/omnibot-phase-1.md:764). The implementation's `EscalationRecord` declares `conversation_id: str` (03-development/src/omnibot/escalation/__init__.py:22) and `EscalationManager.create()` accepts `conversation_id: str` (03-development/src/omnibot/escalation/__init__.py:41). SAD.md:136 specifies that the `conversations` lookup returns `conversation_id INT`, which is then passed directly to `EscalationService.create()` (SAD.md:482); passing a Python `str` to a PostgreSQL `INTEGER` column will raise `psycopg2.errors.InvalidTextRepresentation` on every Phase 2 `create()` call, blocking the entire human-handoff path. In Phase 1, tests pass string literals such as `"conv_001"` (tests/test_fr08.py:21), which succeed in the in-memory store but will fail at the Phase 2 database boundary without an explicit `int()` coercion. There is no type-annotation enforcement or runtime validation at the call site to catch this discrepancy early. |
| **likelihood** | 4 / 5 — Phase 2 PostgreSQL wiring is the next sprint scope; every `create()` call will raise on the first real database connection unless the type is corrected. The in-memory Phase 1 store masks the error completely, so the bug will not surface until integration. |
| **impact** | 3 / 5 — All escalation insertions fail at the Phase 2 boundary; human handoff for low-confidence and no-match queries is completely broken until patched. No data is silently corrupted in Phase 1, but the gap blocks the critical escalation path at Phase 2 go-live. |
| **mitigation** | (1) Change `EscalationRecord.conversation_id` from `str` to `int` (03-development/src/omnibot/escalation/__init__.py:22). (2) Update `EscalationManager.create()` signature: `conversation_id: int` (03-development/src/omnibot/escalation/__init__.py:41). (3) Update all Phase 1 test calls in `tests/test_fr08.py` to pass integer conversation IDs (e.g., `1`, `2`, `3`) rather than string literals like `"conv_001"`. (4) Add a `tests/test_fr08.py` type assertion: `assert isinstance(record.conversation_id, int)` after `mgr.create(1, "reason")`. |
| **owner** | Platform Team |

**Citations** (HR-15): 03-development/src/omnibot/escalation/__init__.py:22 (`conversation_id: str` — implementation declares str, not int), 03-development/src/omnibot/escalation/__init__.py:41 (`def create(self, conversation_id: str, reason: str)` — str parameter), SPEC/omnibot-phase-1.md:560 (`conversation_id: int` — SPEC EscalationRequest declares int), SPEC/omnibot-phase-1.md:764 (`conversation_id INTEGER REFERENCES conversations(id) UNIQUE` — schema column is INTEGER), 02-architecture/SAD.md:136 (`conversations` lookup returns `conversation_id INT`), 02-architecture/SAD.md:482 (`EscalationService.create(conversation_id, reason="no_rule_match")` — caller passes int from pipeline), tests/test_fr08.py:21 (`mgr.create("conv_001", "low_confidence")` — string literal; would fail Phase 2 type check)

---

### RISK-FR08-02 — `assign()` Missing `resolved_at IS NULL` Guard — Resolved Escalations Can Be Silently Re-Assigned

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR08-02 |
| **fr_tag** | [FR-08] |
| **category** | Technical / Data Integrity |
| **description** | The SPEC's `BasicEscalationManager.assign()` SQL includes `WHERE id = %s AND resolved_at IS NULL` (SPEC/omnibot-phase-1.md:585), ensuring that calling `assign()` on an already-resolved escalation is a no-op rather than overwriting audit-critical fields. The implementation's `EscalationManager.assign()` performs no such state check (03-development/src/omnibot/escalation/__init__.py:54-60): it retrieves the record, raises `KeyError` only if absent, and then unconditionally overwrites `assigned_agent` and `picked_at`. Calling `assign()` on a record that has `resolved_at` set advances `picked_at` past `resolved_at`, creating an impossible audit trail (agent assigned after resolution). Symmetrically, `resolve()` contains no idempotency guard (03-development/src/omnibot/escalation/__init__.py:62-67): calling it twice silently advances `resolved_at` on each invocation, making the timestamp unreliable. SAD.md:516 specifies that `first_contact_resolution BOOL` is set to TRUE when `resolve()` is called without a prior `assign()`; corrupted `picked_at` / `resolved_at` timestamps break this FCR determination. `tests/test_fr08.py` does not test calling `assign()` on a resolved record or calling `resolve()` twice. |
| **likelihood** | 3 / 5 — Agent-facing UIs commonly include retry logic on failure; a double-submit or concurrent webhook delivery triggers re-assignment. The resolve-without-assign path (self-service FCR) also calls `resolve()` directly, creating a scenario where a subsequent `assign()` would corrupt the audit record. |
| **impact** | 3 / 5 — Corrupted `picked_at` and `resolved_at` timestamps invalidate FCR analytics (SAD.md:516) and compliance audit trails (NFR-06). Two agents may independently act on the same escalation record if `assign()` succeeds after resolution, causing duplicate handling of a closed conversation. |
| **mitigation** | (1) Add a resolved guard in `assign()`: `if record.resolved_at is not None: raise ValueError(f"Escalation {escalation_id} already resolved")` (03-development/src/omnibot/escalation/__init__.py:56). (2) Make `resolve()` idempotent: `if record.resolved_at is not None: return` (03-development/src/omnibot/escalation/__init__.py:64). (3) Add `tests/test_fr08.py` cases: (a) `assign()` after `resolve()` raises `ValueError`; (b) calling `resolve()` twice leaves `resolved_at` unchanged at its original value. (4) Carry the `WHERE id = %s AND resolved_at IS NULL` guard (SPEC/omnibot-phase-1.md:585) forward verbatim into the Phase 2 SQL implementation. |
| **owner** | Platform Team |

**Citations** (HR-15): 03-development/src/omnibot/escalation/__init__.py:54-60 (`assign()` — no `resolved_at IS NULL` check; unconditionally overwrites `assigned_agent` and `picked_at`), 03-development/src/omnibot/escalation/__init__.py:62-67 (`resolve()` — no idempotency guard; overwrites `resolved_at` on every invocation), SPEC/omnibot-phase-1.md:585 (`WHERE id = %s AND resolved_at IS NULL` — SPEC SQL guards assign against resolved records), 02-architecture/SAD.md:264-265 (`assign()` sets `picked_at = NOW()`, `resolve()` sets `resolved_at = NOW()` — lifecycle order implied, not enforced), 02-architecture/SAD.md:516 (`first_contact_resolution BOOL` set TRUE when `resolve()` called without prior `assign()` — corrupted timestamps break this FCR logic), tests/test_fr08.py:55-62 (`test_resolve_sets_resolved_at` — single resolve only; no double-resolve or post-resolve assign test)

---

### RISK-FR08-03 — No `conversation_id` Uniqueness Enforcement — Duplicate Escalation Records Allowed Per Conversation

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR08-03 |
| **fr_tag** | [FR-08] |
| **category** | Technical / Functional |
| **description** | The `escalation_queue` schema enforces `conversation_id INTEGER REFERENCES conversations(id) UNIQUE` (SPEC/omnibot-phase-1.md:764), meaning exactly one escalation record may exist per conversation. The in-memory `EscalationManager.create()` performs no such check (03-development/src/omnibot/escalation/__init__.py:41-52): it allocates a new auto-incremented `_next_id` and inserts a new `EscalationRecord` without verifying whether the given `conversation_id` already has a pending or resolved entry. A webhook retry, concurrent request for the same user, or accidental double-trigger of the escalation path creates a second record with a distinct `escalation_id` but the same `conversation_id`, silently doubling that conversation's queue entry. Agent dashboards will show duplicate rows; two agents may independently pick up and attempt to resolve the same underlying conversation. In Phase 2, the first `INSERT INTO escalation_queue` succeeds and the second raises `psycopg2.errors.UniqueViolation` (SPEC/omnibot-phase-1.md:572-578 — the INSERT has no `ON CONFLICT` clause), crashing the escalation path for all retry scenarios. `tests/test_fr08.py:37-43` (`test_create_increments_id`) creates two records with different `conversation_id` strings and verifies only that IDs increment; no duplicate-conversation test exists. |
| **likelihood** | 3 / 5 — LINE and Telegram both retry webhook deliveries on non-2xx HTTP responses; any transient error during the escalation INSERT causes a retry that fires `create()` a second time for the same conversation. Concurrent pipeline executions for the same user compound the risk. |
| **impact** | 3 / 5 — In Phase 1, duplicate records inflate agent queue counts and cause two-agent conflicts on a single conversation. In Phase 2, the `UNIQUE` constraint violation on retry crashes the escalation insert, leaving the conversation in a state where neither escalation record is actionable and human handoff fails silently. |
| **mitigation** | (1) Add a uniqueness check in `create()`: maintain a `Dict[str, int]` (or `Dict[int, int]`) index mapping `conversation_id` to `escalation_id`; raise `ValueError` or return the existing `escalation_id` if a record for that conversation already exists (03-development/src/omnibot/escalation/__init__.py:41). (2) In Phase 2 SQL, add `ON CONFLICT (conversation_id) DO NOTHING RETURNING id` to the INSERT, or add a pre-check `SELECT id FROM escalation_queue WHERE conversation_id = %s AND resolved_at IS NULL`. (3) Add a `tests/test_fr08.py` test: calling `create()` twice with the same `conversation_id` either raises `ValueError` or returns the original `escalation_id`. (4) Leverage the existing `idx_escalation_pending` partial index (SPEC/omnibot-phase-1.md:774-775 — `WHERE resolved_at IS NULL`) for the Phase 2 pre-check query. |
| **owner** | Platform Team |

**Citations** (HR-15): 03-development/src/omnibot/escalation/__init__.py:38-52 (`EscalationManager.__init__` and `create()` — no uniqueness check on `conversation_id`; new record always inserted), SPEC/omnibot-phase-1.md:764 (`conversation_id INTEGER REFERENCES conversations(id) UNIQUE` — schema enforces one escalation per conversation), SPEC/omnibot-phase-1.md:572-578 (`INSERT INTO escalation_queue (conversation_id, reason) VALUES (%s, %s) RETURNING id` — no `ON CONFLICT` clause; bare insert raises on duplicate), SPEC/omnibot-phase-1.md:774-775 (`CREATE INDEX idx_escalation_pending ON escalation_queue (queued_at) WHERE resolved_at IS NULL` — partial index exists but application-layer uniqueness absent), tests/test_fr08.py:37-43 (`test_create_increments_id` — creates two records with different conversation IDs; no same-conversation duplicate test)

---

### RISK-FR08-04 — `EscalationRecord` Is a Plain Mutable Dataclass — Violates SAD Immutability Principle, Exposes Audit Fields to Silent Corruption

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR08-04 |
| **fr_tag** | [FR-08] |
| **category** | Technical / Operational |
| **description** | SAD.md:58 designates `frozen=True` dataclasses as an explicit architectural principle: "Immutable message types: `UnifiedMessage` is a `frozen=True` dataclass — thread-safe and hashable by design." SAD.md:429 lists `frozen=True dataclasses` among the Phase 1 design patterns for thread-safe, hashable domain objects. `EscalationRecord` uses a plain `@dataclass` without `frozen=True` (03-development/src/omnibot/escalation/__init__.py:14), making all fields — including audit-critical `reason`, `assigned_agent`, `picked_at`, and `resolved_at` — mutable after construction. Any middleware, logging decorator, or inadvertent reference alias can silently overwrite these fields with no error. The current `assign()` and `resolve()` methods already rely on direct field mutation (`record.assigned_agent = agent_id` at 03-development/src/omnibot/escalation/__init__.py:59; `record.resolved_at = datetime.now(timezone.utc)` at 03-development/src/omnibot/escalation/__init__.py:67), meaning applying `frozen=True` would require refactoring these methods to use `dataclasses.replace()` rather than in-place mutation. The `reason` field — the audit record of why escalation was triggered — is equally mutable and could be overwritten from `"no_rule_match"` to any arbitrary string after creation. `tests/test_fr08.py:87-99` (`test_escalation_record_fields`) checks initial field values but includes no immutability assertion. |
| **likelihood** | 3 / 5 — The mutable design is load-bearing in the current implementation (assign/resolve mutate in place); the corruption risk materialises whenever new code — a logging pass, a serialization step, or a future middleware layer — touches the live record object without realising it is shared state. |
| **impact** | 2 / 5 — Silent mutation of `reason` or `resolved_at` corrupts the escalation audit log and FCR metrics (NFR-06); the failure mode is invisible at runtime and surfaces only during compliance review or analytics queries. No immediate service outage results, but audit integrity is permanently compromised for affected records. |
| **mitigation** | (1) Apply `@dataclass(frozen=True)` to `EscalationRecord` (03-development/src/omnibot/escalation/__init__.py:14) and refactor `assign()` and `resolve()` to create new immutable snapshots via `dataclasses.replace()` stored back into `_records`. (2) As a pragmatic minimum if full refactor is deferred: annotate the mutable state fields (`assigned_agent`, `picked_at`, `resolved_at`) with `# mutable state — do not access outside EscalationManager` and treat `reason`, `created_at`, `escalation_id` as logically immutable. (3) Add `tests/test_fr08.py` assertion: after `create()`, directly assigning `record.reason = "tampered"` raises `FrozenInstanceError`. (4) Follow SAD.md:429 and apply `@dataclass(frozen=True)` to all new Phase 1 domain types, consistent with `UnifiedMessage` (03-development/src/omnibot/models.py:35). |
| **owner** | Platform Team |

**Citations** (HR-15): 03-development/src/omnibot/escalation/__init__.py:14 (`@dataclass` — no `frozen=True`; violates SAD immutability principle), 03-development/src/omnibot/escalation/__init__.py:59 (`record.assigned_agent = agent_id` — direct in-place field mutation), 03-development/src/omnibot/escalation/__init__.py:67 (`record.resolved_at = datetime.now(timezone.utc)` — direct in-place field mutation), 02-architecture/SAD.md:58 (`frozen=True` dataclass principle — `UnifiedMessage` cited as canonical immutable domain type), 02-architecture/SAD.md:429 (`frozen=True dataclasses | Thread-safe, hashable messages without external library` — Phase 1 design pattern), 03-development/src/omnibot/models.py:35 (`@dataclass(frozen=True)` — `UnifiedMessage` correctly applies the principle), tests/test_fr08.py:87-99 (`test_escalation_record_fields` — checks initial field values; no immutability assertion, no `FrozenInstanceError` test)

---

## [FR-09] Structured Logger — JSON Format — Detailed Risk Entries

---

### RISK-FR09-01 — `print()` to stdout Without `flush=True` — NDJSON Log Entries Silently Lost on Container Crash or SIGTERM

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR09-01 |
| **fr_tag** | [FR-09] |
| **category** | Technical / Operational |
| **description** | `StructuredLogger.log()` emits each NDJSON entry via `print(json.dumps(entry, ensure_ascii=False), file=sys.stdout)` (03-development/src/omnibot/logger/__init__.py:35) without `flush=True`. Python's `print()` writes to the OS file buffer; in containerised environments (Docker, Kubernetes), default block-buffered stdout holds entries in memory until the buffer fills or the process exits cleanly. On OOM kill, SIGKILL, or container preemption, buffered entries are discarded with no error. The SPEC reference implementation routes log entries through `self.logger.log(self.LOG_LEVELS.get(level, logging.INFO), json.dumps(entry))` (SPEC/omnibot-phase-1.md:634), where the stdlib logging handler manages flushing; the implementation's bare `print()` provides no equivalent guarantee. During a production incident — the moment when log entries are most critical — a process crash discards any buffered CRITICAL or ERROR entries, leaving operators blind to the events immediately preceding the failure. `tests/test_fr09.py` verifies single-newline NDJSON output (tests/test_fr09.py:40-44) but never tests that the entry is flushed to the underlying OS stream. |
| **likelihood** | 3 / 5 — Containerised deployment is the standard Phase 2 target; OOM kills and rolling restarts are routine. Python's block-buffering is silent in normal operation and only manifests as data loss on abnormal termination, making the risk invisible until an incident occurs. |
| **impact** | 4 / 5 — Lost log entries during the crash window destroy forensic evidence for post-incident review. CRITICAL and ERROR entries — integrity threats and DB failures — are the highest-value log events and most likely to precede a crash, making loss asymmetrically harmful to on-call response and NFR-06 audit trails. |
| **mitigation** | (1) Add `flush=True` to the `print()` call: `print(json.dumps(entry, ensure_ascii=False), file=sys.stdout, flush=True)` (03-development/src/omnibot/logger/__init__.py:35). (2) Set `PYTHONUNBUFFERED=1` in all container run configurations as a defence-in-depth complement — this disables Python stdout buffering globally but is not a substitute for fix (1). (3) Add a `tests/test_fr09.py` test that patches `sys.stdout.flush` and asserts it is called after each log emission. |
| **owner** | Platform Team |

**Citations** (HR-15): 03-development/src/omnibot/logger/__init__.py:35 (`print(json.dumps(entry, ensure_ascii=False), file=sys.stdout)` — no `flush=True`; OS buffer retained until full or clean exit), SPEC/omnibot-phase-1.md:634 (`self.logger.log(…)` — SPEC routes through stdlib handler with managed flushing), tests/test_fr09.py:40-44 (`test_log_output_is_single_line` — verifies one newline emitted; does not verify OS-level flush), 02-architecture/SAD.md:338 (`Responsibility: Emit JSON NDJSON log entries to stdout` — no flush SLA specified in design)

---

### RISK-FR09-02 — No Minimum Log-Level Filter — `debug()` Emits Raw Payloads to Production stdout, Leaking PII

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR09-02 |
| **fr_tag** | [FR-09] |
| **category** | Security / Compliance |
| **description** | `StructuredLogger.__init__` accepts only `service: str` (03-development/src/omnibot/logger/__init__.py:21-22) and exposes all five log levels unconditionally. The `debug()` method docstring states "Developer diagnostics: raw payload, sanitizer output" (03-development/src/omnibot/logger/__init__.py:37-38), meaning it is designed to emit raw webhook payloads before `PIIMaskerL4` processing. SRS.md:147 classifies PII detection at `WARN` level, but a `logger.debug(raw_payload)` call in the adapter layer (the anticipated next development step) would emit un-masked user message text to stdout in production. The SPEC defines `LOG_LEVELS` with numeric values and routes through `logging.getLogger()` (SPEC/omnibot-phase-1.md:614-624), which inherits Python's default WARNING minimum level from `logging.basicConfig`; the implementation's unconditional `print()` has no equivalent gate. No test in `tests/test_fr09.py` verifies that DEBUG output can be suppressed via configuration. |
| **likelihood** | 3 / 5 — `debug()` calls are routinely added during development and frequently remain in production code; without a level gate there is no infrastructure guard. A single `logger.debug(raw_payload)` call in the adapter parse path exposes every user message to the production log stream. |
| **impact** | 4 / 5 — Raw webhook payloads contain user-identifiable message text and LINE/Telegram user IDs, violating NFR-06 PII controls and GDPR Article 5(1)(f) data minimisation. Log aggregation systems persist these entries indefinitely, creating a persistent PII audit exposure across every collected log. |
| **mitigation** | (1) Add a `min_level` parameter to `StructuredLogger.__init__()` defaulting to `"INFO"` for production; skip emission in `log()` when `level` ranks below `min_level` (03-development/src/omnibot/logger/__init__.py:21-35). (2) Read `LOG_LEVEL` from the environment (`os.environ.get("LOG_LEVEL", "INFO")`) so containerised deployments control verbosity without code changes — consistent with the SPEC `LOG_LEVELS` dict approach (SPEC/omnibot-phase-1.md:614-620). (3) Add a `tests/test_fr09.py` test: `StructuredLogger(service="s", min_level="INFO")` must produce no output when `debug()` is called. |
| **owner** | Platform Team |

**Citations** (HR-15): 03-development/src/omnibot/logger/__init__.py:21-22 (`def __init__(self, service: str)` — no `min_level` parameter; all five levels always active), 03-development/src/omnibot/logger/__init__.py:37-38 (`def debug()` docstring: "Developer diagnostics: raw payload, sanitizer output" — designed to emit raw pre-mask data), 01-requirements/SRS.md:147 (`WARN: 非致命異常（低信心度匹配、PII 偵測）` — PII detection events at WARN; raw payload at DEBUG precedes masking), SPEC/omnibot-phase-1.md:614-620 (`LOG_LEVELS = {…}` — SPEC uses stdlib logging with WARN default; implementation lacks equivalent gate), tests/test_fr09.py:99-102 (`test_level_debug` — verifies DEBUG level emitted; does not test suppression in production configuration)

---

### RISK-FR09-03 — `log()` Caller-Supplied `service` Parameter Overrides `self._service` — False Service Attribution in Log Aggregation

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR09-03 |
| **fr_tag** | [FR-09] |
| **category** | Technical / Operational |
| **description** | `StructuredLogger.log()` accepts `service` as an explicit positional parameter: `def log(self, level: str, service: str, message: str, **kwargs: Any)` (03-development/src/omnibot/logger/__init__.py:24). Any caller invoking `log()` directly can pass an arbitrary `service` value, overriding `self._service` set at construction time. The shorthand methods (`info()`, `warn()`, `error()`, `debug()`, `critical()`) correctly forward `self._service` (03-development/src/omnibot/logger/__init__.py:39: `self.log("DEBUG", self._service, message, **kwargs)`), but the public `log()` API enforces no such constraint. The SPEC's `log()` signature is `def log(self, level: str, message: str, **kwargs)` with `self.service` always used (SPEC/omnibot-phase-1.md:626-634); the implementation's additional `service` positional parameter is a deviation from that contract. The test `tests/test_fr09.py:117-124` (`test_log_method_accepts_level_string`) explicitly passes `service="test2"` and asserts `parsed["service"] == "test2"`, confirming that caller-override is both possible and validated as correct. In multi-service log aggregation, false service attribution prevents correct routing of alerts and breaks `service`-scoped dashboards. |
| **likelihood** | 3 / 5 — `log()` is a public method; future middleware integrations or developers unfamiliar with the shorthand API will invoke `log()` directly and supply an incorrect `service` value. The existing test validates the override as intended behaviour, increasing the risk that it persists. |
| **impact** | 2 / 5 — False service attribution corrupts operational dashboards and alert routing rules that filter by the `service` field, increasing mean-time-to-detect during incidents. No data is lost and no security boundary is crossed; the damage is confined to operational observability. |
| **mitigation** | (1) Remove the explicit `service` positional parameter from `log()` and always use `self._service`: change signature to `def log(self, level: str, message: str, **kwargs: Any)` (03-development/src/omnibot/logger/__init__.py:24), consistent with SPEC/omnibot-phase-1.md:626. (2) Update `tests/test_fr09.py:117-124` to remove the `service="test2"` override and assert `parsed["service"] == "test"` (the constructor-supplied name). (3) If per-call service override is genuinely needed, make it an optional kwarg (`service: str | None = None`) that falls back to `self._service` when absent. |
| **owner** | Platform Team |

**Citations** (HR-15): 03-development/src/omnibot/logger/__init__.py:24 (`def log(self, level: str, service: str, message: str, **kwargs)` — `service` positional param allows caller override of `self._service`), 03-development/src/omnibot/logger/__init__.py:39 (`self.log("DEBUG", self._service, message, **kwargs)` — shorthand correctly uses `self._service`; direct `log()` callers bypass enforcement), SPEC/omnibot-phase-1.md:626 (`def log(self, level: str, message: str, **kwargs)` — no explicit `service` param; SPEC always uses `self.service`), tests/test_fr09.py:117-124 (`test_log_method_accepts_level_string` — passes `service="test2"`, asserts override accepted; documents deviation from SPEC contract as intended)

---

### RISK-FR09-04 — `app.py` Uses Stdlib `logging.getLogger()` — All Application-Layer Errors Bypass FR-09 NDJSON Format

| Field | Value |
|-------|-------|
| **risk_id** | RISK-FR09-04 |
| **fr_tag** | [FR-09] |
| **category** | Technical / Functional |
| **description** | `app.py` imports `logging` from the stdlib (03-development/src/omnibot/app.py:11) and declares `logger = logging.getLogger("omnibot.app")` (03-development/src/omnibot/app.py:21); `omnibot.logger.StructuredLogger` is never imported. The `global_exception_handler` uses this stdlib logger: `logger.error("Unhandled exception", extra={…})` (03-development/src/omnibot/app.py:32-41). Stdlib `logging.error()` emits a text-formatted string to the configured handler — by default a `StreamHandler` producing `ERROR:omnibot.app:Unhandled exception` on stderr — not a JSON object on stdout. Every unhandled exception in the FastAPI application (webhook parse failures, DB connection errors surfacing as 500s, auth bypasses) is therefore logged as an unstructured text line, breaking log aggregation pipelines configured to parse `timestamp`, `level`, `service`, and `message` fields from NDJSON. The `global_exception_handler` is the most security-relevant log point; emitting it in the wrong format means NDJSON-based alerting rules cannot fire on application-layer integrity events. SAD.md:332-360 designates FR-09 as the observability contract for all modules; `app.py` violates this contract on every unhandled exception. |
| **likelihood** | 4 / 5 — The issue is present today and manifests on every unhandled exception. No configuration or deployment change is required to trigger it; it fires on the first 500 error in any environment. |
| **impact** | 3 / 5 — NDJSON-based alerting rules and dashboards cannot extract structured fields from stdlib text output, silently dropping the error from monitoring pipelines. Security-relevant exception events (potential auth bypasses surfacing as 500s) are not parseable by structured monitoring, increasing mean-time-to-detect. No functional outage results, but operational blind spots are created for the highest-severity error class. |
| **mitigation** | (1) Replace `import logging; logger = logging.getLogger("omnibot.app")` with `from omnibot.logger import StructuredLogger; logger = StructuredLogger(service="omnibot.app")` in `app.py` (03-development/src/omnibot/app.py:11, 21). (2) Replace `logger.error("Unhandled exception", extra={…})` (03-development/src/omnibot/app.py:32-41) with `logger.error("Unhandled exception", path=str(request.url.path), method=request.method, error_type=type(exc).__name__, error_message=str(exc))` using `StructuredLogger`'s kwargs API. (3) Add a FastAPI test asserting that a 500 response produces a valid JSON line on stdout. |
| **owner** | Platform Team |

**Citations** (HR-15): 03-development/src/omnibot/app.py:11 (`import logging` — stdlib logging imported; `omnibot.logger.StructuredLogger` absent from imports), 03-development/src/omnibot/app.py:21 (`logger = logging.getLogger("omnibot.app")` — stdlib logger produces text output to stderr, not NDJSON to stdout), 03-development/src/omnibot/app.py:32-41 (`logger.error("Unhandled exception", extra={…})` — stdlib `.error()` emits unstructured text; not parseable as NDJSON), 02-architecture/SAD.md:332-360 (FR-09 coverage section — all modules must emit NDJSON via `StructuredLogger`; `app.py` violates this contract), 01-requirements/SRS.md:138-153 (FR-09 acceptance criteria: every log entry must be one NDJSON line with `timestamp`/`level`/`service`/`message` fields)

---

## Risk Heat Map

```
Impact
  5 |         | R01-05  |         |         |         |
  4 |         |R01-01   |R01-02   | R03-01  |         |
    |         |R02-03   |R02-01   | R06-02  |         |
    |         |         |R04-01   | R07-01  |         |
    |         |         |R05-01   |         |         |
    |         |         |R06-01   |         |         |
    |         |         |R09-01   |         |         |
    |         |         |R09-02   |         |         |
  3 |         |R03-03   |R01-04   | R01-03  |         |
    |         |R05-04   |R02-02   | R04-03  |         |
    |         |         |R03-02   | R05-02  |         |
    |         |         |R03-04   | R07-02  |         |
    |         |         |R04-02   | R08-01  |         |
    |         |         |         | R09-04  |         |
    |         |         |R05-03   |         |         |
    |         |         |R06-03   |         |         |
    |         |         |R06-04   |         |         |
    |         |         |R07-03   |         |         |
    |         |         |R07-04   |         |         |
    |         |         |R08-02   |         |         |
    |         |         |R08-03   |         |         |
  2 |         |         |         | R02-04  |         |
    |         |         |R04-04   |         |         |
    |         |         |R08-04   |         |         |
    |         |         |R09-03   |         |         |
  1 |         |         |         |         |         |
    +---------+---------+---------+---------+---------+
      L=1       L=2       L=3       L=4       L=5
                        Likelihood
```

> **HIGH** (score ≥ 10): RISK-FR01-02, RISK-FR01-03, RISK-FR01-05, RISK-FR02-01, RISK-FR03-01, RISK-FR04-01, RISK-FR04-03, RISK-FR05-01, RISK-FR05-02, RISK-FR06-01, RISK-FR06-02, RISK-FR07-01, RISK-FR07-02, RISK-FR08-01
> **MEDIUM** (score 6–9): RISK-FR01-01, RISK-FR01-04, RISK-FR02-02, RISK-FR02-03, RISK-FR02-04, RISK-FR03-02, RISK-FR03-03, RISK-FR03-04, RISK-FR04-02, RISK-FR04-04, RISK-FR05-03, RISK-FR05-04, RISK-FR06-03, RISK-FR06-04, RISK-FR07-03, RISK-FR07-04, RISK-FR08-02, RISK-FR08-03, RISK-FR08-04

---

*RISK_REGISTER.md v0.7 — FR-01 + FR-02 + FR-03 + FR-04 + FR-05 + FR-06 + FR-07 entries · Phase 7 draft · 2026-05-15*
