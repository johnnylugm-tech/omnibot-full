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

## Risk Heat Map

```
Impact
  5 |         | R01-05  |         |         |         |
  4 |         |R01-01   |R01-02   | R03-01  |         |
    |         |R02-03   |R02-01   |         |         |
    |         |         |R04-01   |         |         |
    |         |         |R05-01   |         |         |
  3 |         |R03-03   |R01-04   | R01-03  |         |
    |         |R05-04   |R02-02   | R04-03  |         |
    |         |         |R03-02   | R05-02  |         |
    |         |         |R03-04   |         |         |
    |         |         |R04-02   |         |         |
    |         |         |R05-03   |         |         |
  2 |         |         |         | R02-04  |         |
    |         |         |R04-04   |         |         |
  1 |         |         |         |         |         |
    +---------+---------+---------+---------+---------+
      L=1       L=2       L=3       L=4       L=5
                        Likelihood
```

> **HIGH** (score ≥ 10): RISK-FR01-02, RISK-FR01-03, RISK-FR01-05, RISK-FR02-01, RISK-FR03-01, RISK-FR04-01, RISK-FR04-03, RISK-FR05-01, RISK-FR05-02
> **MEDIUM** (score 6–9): RISK-FR01-01, RISK-FR01-04, RISK-FR02-02, RISK-FR02-03, RISK-FR02-04, RISK-FR03-02, RISK-FR03-03, RISK-FR03-04, RISK-FR04-02, RISK-FR04-04, RISK-FR05-03, RISK-FR05-04

---

*RISK_REGISTER.md v0.5 — FR-01 + FR-02 + FR-03 + FR-04 + FR-05 entries · Phase 7 draft · 2026-05-15*
