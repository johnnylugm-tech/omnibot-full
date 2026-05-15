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

## Risk Heat Map

```
Impact
  5 |         | R01-05  |         |         |         |
  4 |         |R01-01   |R01-02   | R03-01  |         |
    |         |R02-03   |R02-01   |         |         |
  3 |         |         |R01-04   | R01-03  |         |
    |         |R03-03   |R02-02   |         |         |
    |         |         |R03-02   |         |         |
    |         |         |R03-04   |         |         |
  2 |         |         |         | R02-04  |         |
  1 |         |         |         |         |         |
    +---------+---------+---------+---------+---------+
      L=1       L=2       L=3       L=4       L=5
                        Likelihood
```

> **HIGH** (score ≥ 10): RISK-FR01-02, RISK-FR01-03, RISK-FR01-05, RISK-FR02-01, RISK-FR03-01
> **MEDIUM** (score 6–9): RISK-FR01-01, RISK-FR01-04, RISK-FR02-02, RISK-FR02-03, RISK-FR02-04, RISK-FR03-02, RISK-FR03-03, RISK-FR03-04

---

*RISK_REGISTER.md v0.3 — FR-01 + FR-02 + FR-03 entries · Phase 7 draft · 2026-05-15*
