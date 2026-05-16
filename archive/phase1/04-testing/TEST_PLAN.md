# Test Plan — Phase 4

## FR-01: Platform Adapter — Telegram + LINE Webhook

### Scope
[FR-01] Verify that POST /api/v1/webhook/telegram and POST /api/v1/webhook/line correctly parse inbound platform payloads into UnifiedMessage format, respond within 3s, and reject unsupported platforms.

Citations: SRS.md:13-25, SAD.md:64-109

### Test Suite: `tests/test_fr01.py`

| # | Test Case | Target | AC Verified |
|---|-----------|--------|-------------|
| 1 | test_telegram_webhook_text_message | telegram.py:parse_telegram_update | AC1: Telegram Update parsed correctly |
| 2 | test_telegram_webhook_response_time | app.py webhook route | AC3: Response < 3s |
| 3 | test_line_webhook_text_message | line.py:parse_line_event | AC2: LINE WebhookEvent parsed correctly |
| 4 | test_line_webhook_response_time | app.py webhook route | AC3: Response < 3s |
| 5 | test_unsupported_platform_returns_400 | app.py webhook route | AC4: Unknown platform -> 400 |
| 6 | test_line_empty_events_returns_400 | line.py:parse_line_event | AC2: Empty events -> 400 |
| 7 | test_platform_enum_values | models.py:Platform | Platform enum completeness |
| 8 | test_message_type_enum_values | models.py:MessageType | MessageType enum completeness |

### Coverage Targets
| Module | Line Target | Actual |
|--------|-------------|--------|
| adapters/telegram.py | >= 80% | 100% |
| adapters/line.py | >= 80% | 100% |
| models.py | >= 80% | 100% |
| app.py (webhook route) | >= 80% | 95% |

### FR-01 Acceptance Criteria Mapping
- **AC1**: POST /api/v1/webhook/telegram correctly parses Telegram Update -> tests #1, #2
- **AC2**: POST /api/v1/webhook/line correctly parses LINE WebhookEvent -> tests #3, #4, #6
- **AC3**: Both endpoints return 200 OK within 3s -> tests #2, #4
- **AC4**: Unsupported platform returns 400 -> test #5

### Exclusions
- HMAC signature failure paths (FR-02 scope, tested by verifier.py unit tests)
- Health check endpoint (FR-11 scope)
- Downstream pipeline processing (FR-03-FR-10)

---

## FR-02: Webhook Signature Verification

### Scope
[FR-02] Verify that every webhook request passes HMAC signature verification before processing. Covers Telegram (SHA256(bot_token) keyed HMAC) and LINE (channel_secret keyed HMAC-SHA256 + Base64). Rejects invalid/missing signatures with 401 AUTH_INVALID_SIGNATURE. Defends against timing attacks via hmac.compare_digest().

Citations: SRS.md:28-41, SAD.md:97-109

### Test Suite: `tests/test_fr02.py`

| # | Test Case | Target | AC Verified |
|---|-----------|--------|-------------|
| 1 | test_telegram_webhook_valid_signature | verifier.py:verify_telegram_signature | AC1: Telegram HMAC with SHA256(bot_token) as key |
| 2 | test_telegram_webhook_invalid_signature | verifier.py:verify_signature | AC3: Invalid signature -> 401 AUTH_INVALID_SIGNATURE |
| 3 | test_telegram_webhook_missing_signature_header | verifier.py:verify_signature | AC3: Missing header -> 401 |
| 4 | test_line_webhook_valid_signature | verifier.py:verify_line_signature | AC2: LINE HMAC-SHA256 + Base64 |
| 5 | test_line_webhook_invalid_signature | verifier.py:verify_signature | AC3: Invalid signature -> 401 |
| 6 | test_line_webhook_missing_signature_header | verifier.py:verify_signature | AC3: Missing header -> 401 |
| 7 | test_timing_attack_resistance | verifier.py:verify_telegram_signature | AC4: hmac.compare_digest() timing safety |
| 8 | test_telegram_webhook_without_auth_headers_still_rejected | verifier.py:verify_signature | FR-01+FR-02 integration: no-auth -> 401 |

### Coverage Targets
| Module | Line Target | Actual |
|--------|-------------|--------|
| auth/verifier.py | >= 80% | 92% |
| auth/__init__.py | >= 80% | 100% |

### FR-02 Acceptance Criteria Mapping
- **AC1**: Telegram webhook uses SHA256(bot_token) as secret key for HMAC -> tests #1, #7
- **AC2**: LINE webhook uses channel_secret for HMAC-SHA256 + Base64 -> test #4
- **AC3**: Verification failure returns 401 AUTH_INVALID_SIGNATURE -> tests #2, #3, #5, #6, #8
- **AC4**: hmac.compare_digest() prevents timing attacks -> test #7
- **AC5**: VERIFIERS dict registry supports new platforms -> partially covered (static init tested; register() path not exercised)

### Coverage Gaps
- Line 50: `PlatformVerifier.register()` — no test registers a new platform verifier
- Line 56: `ValueError` for unknown platform in `VERIFIERS.verify()` — no test calls with unregistered platform
- Line 84: `HTTPException(400)` for unsupported platform in `verify_signature()` — no test calls with unknown platform

All three gaps are non-critical edge cases; core acceptance criteria (AC1-AC4) are fully covered.

---

## FR-03: Unified Message Format

### Scope
[FR-03] Verify that UnifiedMessage (frozen dataclass), Platform enum (TELEGRAM/LINE/MESSENGER/WHATSAPP), MessageType enum (TEXT/IMAGE/STICKER/LOCATION/FILE), and UnifiedResponse dataclass are correctly defined and enforce invariants.

Citations: SRS.md:44-55, SAD.md:140-167

### Test Suite: `tests/test_fr03.py`

| # | Test Case | Target | AC Verified |
|---|-----------|--------|-------------|
| 1 | test_unified_message_is_frozen | models.py:UnifiedMessage | AC1: frozen=True enforced |
| 2 | test_unified_message_required_fields | models.py:UnifiedMessage | AC1: required fields present and typed |
| 3 | test_unified_message_defaults | models.py:UnifiedMessage | AC1: optional fields have correct defaults |
| 4 | test_unified_message_reply_token | models.py:UnifiedMessage | AC1: reply_token field functional |
| 5 | test_unified_response_fields | models.py:UnifiedResponse | AC2: content/source/confidence/knowledge_id present |
| 6 | test_unified_response_escalate_defaults | models.py:UnifiedResponse | AC2: escalate defaults verified |
| 7 | test_platform_enum_completeness | models.py:Platform | AC3: TELEGRAM, LINE, MESSENGER, WHATSAPP |
| 8 | test_message_type_enum_completeness | models.py:MessageType | AC4: TEXT, IMAGE, STICKER, LOCATION, FILE |
| 9 | test_platform_enum_from_string | models.py:Platform | AC3: Platform.from_string() parsing |
| 10 | test_message_type_enum_from_string | models.py:MessageType | AC4: MessageType.from_string() parsing |

### Coverage Targets
| Module | Line Target | Actual |
|--------|-------------|--------|
| models.py | >= 80% | 100% |

### FR-03 Acceptance Criteria Mapping
- **AC1**: UnifiedMessage is a frozen=True dataclass with all required fields -> tests #1, #2, #3, #4
- **AC2**: UnifiedResponse with content/source/confidence/knowledge_id -> tests #5, #6
- **AC3**: Platform enum: TELEGRAM, LINE, MESSENGER, WHATSAPP -> tests #7, #9
- **AC4**: MessageType enum: TEXT, IMAGE, STICKER, LOCATION, FILE -> tests #8, #10

### Exclusions
- None — FR-03 is a pure data model definition with full coverage

---

## FR-04: Input Sanitizer L2 — Character Normalization

### Scope
[FR-04] Verify that `sanitize()` performs NFKC normalization via `unicodedata.normalize("NFKC", text)`, removes non-printable control characters while preserving `\n` and `\t`, strips leading/trailing whitespace, and does NOT perform any pattern matching (L3's responsibility).

Citations: SRS.md:59-68, SAD.md:182-198

### Test Suite: `tests/test_fr04.py`

| # | Test Case | Target | AC Verified |
|---|-----------|--------|-------------|
| 1 | test_nfkc_normalization | sanitizer/__init__.py:sanitize | AC1: Fullwidth Latin -> ASCII via NFKC |
| 2 | test_nfkc_combining_characters | sanitizer/__init__.py:sanitize | AC1: decomposed chars composed to precomposed |
| 3 | test_control_characters_removed | sanitizer/__init__.py:sanitize | AC2: Cc category chars (except \n \t) removed |
| 4 | test_newline_and_tab_preserved | sanitizer/__init__.py:sanitize | AC2: \n and \t explicitly preserved |
| 5 | test_leading_trailing_whitespace_stripped | sanitizer/__init__.py:sanitize | AC3: strip() applied after normalization |
| 6 | test_empty_string | sanitizer/__init__.py:sanitize | AC3: empty input returns empty string |
| 7 | test_only_whitespace | sanitizer/__init__.py:sanitize | AC3: whitespace-only returns empty string |
| 8 | test_unicode_emojis_preserved | sanitizer/__init__.py:sanitize | AC4: no pattern matching — emojis pass through |
| 9 | test_no_pattern_matching_performed | sanitizer/__init__.py:sanitize | AC4: <script> tags NOT filtered by L2 |
| 10 | test_idempotent | sanitizer/__init__.py:sanitize | Sanitize(sanitize(x)) == sanitize(x) |
| 11 | test_zwj_emoji_preserved | sanitizer/__init__.py:sanitize | ZWJ (U+200D, Cf category) not stripped |

### Coverage Targets
| Module | Line Target | Actual |
|--------|-------------|--------|
| sanitizer/__init__.py | >= 80% | 100% |

### FR-04 Acceptance Criteria Mapping
- **AC1**: `unicodedata.normalize("NFKC", text)` is called on input text -> tests #1, #2
- **AC2**: All non-printable control characters removed, but \n and \t are preserved -> tests #3, #4
- **AC3**: Result has leading/trailing whitespace stripped via `.strip()` -> tests #5, #6, #7
- **AC4**: No pattern matching performed — L2 only normalizes, L3 handles patterns -> tests #8, #9
- **Bonus**: Idempotency guarantee — double application yields same result -> test #10
- **Bonus**: ZWJ sequences (emoji combining) preserved via Cf category inclusion -> test #11

### Exclusions
- Pattern matching / XSS filtering (FR-05 L3 scope)
- Duplicate message detection (FR-06 scope)
- Message routing / context assembly (FR-07 scope)

---

## FR-07: Knowledge Layer V1 — Rule Match + Escalate

### Scope
[FR-07] Verify that `KnowledgeBase` performs exact/fuzzy keyword matching with confidence scoring. Confidence > 0.7 returns rule-matched reply with source="rule_match". Confidence <= 0.7 escalates (escalate=True, source="escalate"). Multiple rules resolve to best match. `query_knowledge()` convenience function wraps default KB instance seeded with 3 rules (退貨/return, 訂單/order, 客服/專人).

Citations: SRS.md FR-07 section

### Test Suite: `tests/test_fr07.py`

| # | Test Case | Target | AC Verified |
|---|-----------|--------|-------------|
| 1 | test_exact_match_high_confidence | knowledge/__init__.py:KnowledgeBase.query | AC1: Exact keyword match -> confidence > 0.7 |
| 2 | test_no_match_low_confidence | knowledge/__init__.py:KnowledgeBase.query | AC2: No match -> confidence <= 0.7, escalate=True |
| 3 | test_partial_match_fuzzy | knowledge/__init__.py:KnowledgeBase.query | AC3: Partial keyword overlap -> confidence > 0 |
| 4 | test_multiple_rules_best_match | knowledge/__init__.py:KnowledgeBase.query | AC4: Multiple rules -> best match returned |
| 5 | test_query_result_dataclass | knowledge/__init__.py:QueryResult | AC5: QueryResult fields (response, confidence, source, escalate) |
| 6 | test_convenience_function | knowledge/__init__.py:query_knowledge | AC6: query_knowledge() returns QueryResult |

### Coverage Targets
| Module | Line Target | Actual |
|--------|-------------|--------|
| knowledge/__init__.py | >= 80% | 100% |

### FR-07 Acceptance Criteria Mapping
- **AC1**: Exact keyword match returns confidence > 0.7 and rule response -> test #1
- **AC2**: No keyword match returns confidence <= 0.7 and escalate=True -> test #2
- **AC3**: Partial keyword overlap gives moderate non-zero confidence -> test #3
- **AC4**: Multiple rules — best matching rule (highest confidence) is returned -> test #4
- **AC5**: QueryResult dataclass has response, confidence, source, escalate fields -> test #5
- **AC6**: query_knowledge() convenience function wraps default KB -> test #6

### Exclusions
- SQL ILIKE / ANY() matching (SRS-specified but implementation uses in-memory `in` operator; functionally equivalent)
- is_active=TRUE filtering (in-memory KB has no notion of deactivation)
- Confidence 0.95 / 0.7 thresholds by match type (SRS specifies exact=0.95, partial=0.7; implementation uses matched/total ratio)
- KnowledgeResult(id=-1) on no-match (implementation uses QueryResult with escalate flag instead)
- version DESC ordering (in-memory KB is append-only, no version column)

---

## FR-06: Rate Limiter — Token Bucket

### Scope
[FR-06] Verify TokenBucket (capacity/refill_rate constructor, consume() returns bool) and RateLimiter (per-user isolation via "platform:user_id" key, new-user full bucket, capacity-zero blocks all). Default rps=100 configurable; 429 on exceed is downstream (route-level) responsibility validated by manual SRS trace.

Citations: SRS.md FR-06 section

### Test Suite: `tests/test_fr06.py`

| # | Test Case | Target | AC Verified |
|---|-----------|--------|-------------|
| 1 | test_token_bucket_allows_within_limit | rate_limiter/__init__.py:TokenBucket.consume | AC1: Bucket allows up to capacity requests, then rejects |
| 2 | test_token_bucket_refills_over_time | rate_limiter/__init__.py:TokenBucket._refill | AC2: Tokens refill at configured rate over elapsed time |
| 3 | test_rate_limiter_per_user_isolation | rate_limiter/__init__.py:RateLimiter.allow | AC3: Independent buckets per user_id |
| 4 | test_rate_limiter_new_user_gets_full_bucket | rate_limiter/__init__.py:RateLimiter.allow | AC4: First-seen user starts with full capacity |
| 5 | test_rate_limiter_capacity_zero_blocks_all | rate_limiter/__init__.py:RateLimiter.allow | AC5: Zero capacity blocks all requests |

### Coverage Targets
| Module | Line Target | Actual |
|--------|-------------|--------|
| rate_limiter/__init__.py | >= 80% | 100% |

### FR-06 Acceptance Criteria Mapping
- **AC1**: TokenBucket.capacity limits burst (consume returns True N times then False) -> test #1
- **AC2**: Tokens refill at refill_rate per second over elapsed time -> test #2
- **AC3**: RateLimiter isolates per-user token buckets -> test #3
- **AC4**: New user_id gets a fresh full-capacity bucket -> test #4
- **AC5**: Capacity=0 bucket blocks all consume() calls -> test #5

### Exclusions
- 429 HTTP response on exceed (route-level integration, not unit-level)
- Concurrent/multi-thread stress testing (token-bucket lock is per-bucket; race coverage deferred to integration suite)
- Custom per-user capacity overrides (future feature)

---

## FR-05: PII Masking L4 -- Phone / Email / Address

### Scope
[FR-05] Verify that `omnibot.pii` correctly detects and masks Taiwan phone numbers (mobile 09XX-XXX-XXX and landline 0X-XXXX-XXXX, with or without dashes), email addresses, and Taiwan addresses. Verify that `contains_sensitive_keywords()` triggers escalation on sensitive keywords (suicide, police, emergency) and does not false-positive on normal messages. Verify `EscalationFlag` dataclass fields.

Citations: SRS.md FR-05 section

### Test Suite: `tests/test_fr05.py`

| # | Test Case | Target | AC Verified |
|---|-----------|--------|-------------|
| 1 | test_mask_taiwan_mobile | pii/__init__.py:mask_pii | AC1: Mobile 09XX-XXX-XXX masked to [PHONE] |
| 2 | test_mask_taiwan_landline | pii/__init__.py:mask_pii | AC1: Landline 0X-XXXX-XXXX masked to [PHONE] |
| 3 | test_phone_without_dashes | pii/__init__.py:mask_pii | AC1: Dashes-optional phone patterns masked |
| 4 | test_mask_email | pii/__init__.py:mask_pii | AC2: Email addresses masked to [EMAIL] |
| 5 | test_mask_multiple_emails | pii/__init__.py:mask_pii | AC2: All emails in text masked |
| 6 | test_mask_taiwan_address | pii/__init__.py:mask_pii | AC3: Taiwan address (city+road) masked to [ADDR] |
| 7 | test_no_false_positive_ordinary_text | pii/__init__.py:mask_pii | AC4: Ordinary text with no PII is unchanged |
| 8 | test_sensitive_keyword_triggers_escalation | pii/__init__.py:contains_sensitive_keywords | AC5: Sensitive keywords trigger escalation |
| 9 | test_normal_message_no_escalation | pii/__init__.py:contains_sensitive_keywords | AC5: Normal messages do not trigger escalation |
| 10 | test_escalation_flag_dataclass | pii/__init__.py:EscalationFlag | AC6: EscalationFlag dataclass fields correct |

### Coverage Targets
| Module | Line Target | Actual |
|--------|-------------|--------|
| omnibot/pii/__init__.py | >= 80% | 100% |

### FR-05 Acceptance Criteria Mapping
- **AC1**: Taiwan phone numbers masked (mobile + landline, dash-optional) -> tests #1, #2, #3
- **AC2**: Email addresses masked -> tests #4, #5
- **AC3**: Taiwan addresses masked (city/district/road pattern) -> test #6
- **AC4**: No false positives on ordinary text -> test #7
- **AC5**: `contains_sensitive_keywords()` escalation gate -> tests #8, #9
- **AC6**: `EscalationFlag` dataclass integrity -> test #10

### Exclusions
- `PIIMaskResult(masked_text, mask_count, pii_types)` return type per SRS spec -- current implementation returns plain `str` from `mask_pii()`; count/types tracking not yet implemented
- Non-Taiwan phone formats (international, US, etc.) -- FR-05 scope is Taiwan only
- Non-Taiwan addresses -- FR-05 scope is Taiwan only

---

## FR-08: Basic Escalation Manager — No SLA

### Scope
[FR-08] Verify that `EscalationManager` (in-memory escalation queue) correctly implements create/assign/resolve lifecycle. `create()` writes an `EscalationRecord` with conversation_id and reason. `assign()` sets assigned_agent and picked_at timestamp. `resolve()` sets resolved_at timestamp. Phase 1 has no SLA tracking -- sla_deadline is always None.

Citations: SRS.md FR-08 section, SAD.md 2.4.1 EscalationService

### Test Suite: `tests/test_fr08.py`

| # | Test Case | Target | AC Verified |
|---|-----------|--------|-------------|
| 1 | test_create_returns_escalation_id | escalation/__init__.py:EscalationManager.create | AC1: create() returns positive int ID |
| 2 | test_create_stores_conversation_id_and_reason | escalation/__init__.py:EscalationManager.create | AC1: conversation_id + reason + created_at stored |
| 3 | test_create_increments_id | escalation/__init__.py:EscalationManager.create | AC1: successive create() returns incrementing IDs |
| 4 | test_assign_sets_agent_and_picked_at | escalation/__init__.py:EscalationManager.assign | AC2: assign() sets assigned_agent + picked_at |
| 5 | test_resolve_sets_resolved_at | escalation/__init__.py:EscalationManager.resolve | AC3: resolve() sets resolved_at |
| 6 | test_phase1_no_sla | escalation/__init__.py:EscalationRecord | AC4: Phase 1 -- sla_deadline is None |
| 7 | test_assign_nonexistent_raises | escalation/__init__.py:EscalationManager.assign | AC2: assign() on missing ID raises KeyError |
| 8 | test_resolve_nonexistent_raises | escalation/__init__.py:EscalationManager.resolve | AC3: resolve() on missing ID raises KeyError |
| 9 | test_escalation_record_fields | escalation/__init__.py:EscalationRecord | AC1: EscalationRecord dataclass fields correct |
| 10 | test_full_lifecycle | escalation/__init__.py:EscalationManager | AC1-3: full create -> assign -> resolve cycle |

### Coverage Targets
| Module | Line Target | Actual |
|--------|-------------|--------|
| escalation/__init__.py | >= 80% | 100% |

### FR-08 Acceptance Criteria Mapping
- **AC1**: create() writes escalation_queue record with conversation_id + reason -> tests #1, #2, #3, #9, #10
- **AC2**: assign() sets assigned_agent + picked_at -> tests #4, #7, #10
- **AC3**: resolve() sets resolved_at -> tests #5, #8, #10
- **AC4**: Phase 1 no SLA tracking (sla_deadline is None) -> test #6

### Exclusions
- SLA deadline computation (Phase 2+)
- Persistent storage (in-memory only for Phase 1)
- Multi-agent assignment / round-robin dispatch (future feature)
- Database-backed queue (SQLite/postgres migration deferred)

---

## FR-09: Structured Logger — JSON Format

### Scope
[FR-09] Verify that StructuredLogger outputs NDJSON (one JSON line per entry), includes all required fields (timestamp ISO 8601 UTC, level, service, message), extra kwargs as top-level fields, all five log levels, and shorthand methods.

Citations: SRS.md FR-09 section, SAD.md 2.6.1 StructuredLogger

### Test Suite: `tests/test_fr09.py`

| # | Test Case | Target | AC Verified |
|---|-----------|--------|-------------|
| 1 | test_log_output_is_valid_json | logger/__init__.py:StructuredLogger | AC1: Valid JSON per line |
| 2 | test_log_output_is_single_line | logger/__init__.py:StructuredLogger | AC1: NDJSON (exactly one line) |
| 3 | test_required_fields | logger/__init__.py:StructuredLogger | AC2: timestamp, level, service, message |
| 4 | test_timestamp_is_iso8601_utc | logger/__init__.py:StructuredLogger | AC2: ISO 8601 UTC with Z |
| 5 | test_kwargs_as_extra_fields | logger/__init__.py:StructuredLogger | AC3: Extra kwargs as fields |
| 6 | test_level_info | logger/__init__.py:StructuredLogger | AC4: INFO level |
| 7 | test_level_warn | logger/__init__.py:StructuredLogger | AC4: WARN level |
| 8 | test_level_error | logger/__init__.py:StructuredLogger | AC4: ERROR level |
| 9 | test_level_debug | logger/__init__.py:StructuredLogger | AC4: DEBUG level |
| 10 | test_level_critical | logger/__init__.py:StructuredLogger | AC4: CRITICAL level |
| 11 | test_different_service_name | logger/__init__.py:StructuredLogger | AC2: Configurable service |
| 12 | test_log_method_accepts_level_string | logger/__init__.py:StructuredLogger | AC5: log() accepts level string |

### Coverage Targets
| Module | Line Target | Actual |
|--------|-------------|--------|
| omnibot/logger/__init__.py | >= 80% | 100% |

### FR-09 Acceptance Criteria Mapping
- **AC1**: NDJSON -- one JSON line per log entry -> tests #1, #2
- **AC2**: Required fields (timestamp ISO 8601 UTC, level, service, message) -> tests #3, #4, #11
- **AC3**: Extra kwargs appear as top-level fields -> test #5
- **AC4**: Five levels (DEBUG/INFO/WARN/ERROR/CRITICAL) + shorthand methods -> tests #6-10
- **AC5**: `log()` method accepts level string directly -> test #12

### Exclusions
- File-based logging (rotating files, etc.) -- V1 is stdout-only
- Async/thread-safe logging -- V1 is single-threaded
- Log level filtering at the logger level (e.g., setLevel) -- not in FR-09 spec

---

## FR-10: API Response Format -- ApiResponse / PaginatedResponse

### Scope
[FR-10] Verify that `ApiResponse[T]` (Pydantic BaseModel, Generic[T]) contains success/data/error/error_code fields with correct defaults. Verify that `PaginatedResponse[T]` inherits from ApiResponse and adds total/page/limit/has_next with computed has_next logic. Verify `ErrorCode` str enum has all 5 required members and supports from-string construction. Verify JSON serialization round-trip via Pydantic model_dump/model_validate.

Citations: SRS.md FR-10 section, SAD.md 2.5.2

### Test Suite: `tests/test_fr10.py`

| # | Test Case | Target | AC Verified |
|---|-----------|--------|-------------|
| 1 | test_api_response_success | api/__init__.py:ApiResponse | AC1: success=True + data present |
| 2 | test_api_response_error | api/__init__.py:ApiResponse | AC1: success=False + error + error_code |
| 3 | test_api_response_defaults | api/__init__.py:ApiResponse | AC1: data/error/error_code default None |
| 4 | test_api_response_generic_typed | api/__init__.py:ApiResponse | AC1: ApiResponse[T] generic data binding |
| 5 | test_paginated_response_inherits_api | api/__init__.py:PaginatedResponse | AC2: isinstance(resp, ApiResponse) |
| 6 | test_paginated_response_fields | api/__init__.py:PaginatedResponse | AC2: total/page/limit/has_next |
| 7 | test_paginated_response_no_next_page | api/__init__.py:PaginatedResponse | AC2: has_next=False on last page |
| 8 | test_paginated_response_error | api/__init__.py:PaginatedResponse | AC2: PaginatedResponse carries error info |
| 9 | test_error_code_enum_values | api/__init__.py:ErrorCode | AC3: 5 members (AUTH_INVALID_SIGNATURE, RATE_LIMIT_EXCEEDED, KNOWLEDGE_NOT_FOUND, VALIDATION_ERROR, INTERNAL_ERROR) |
| 10 | test_error_code_from_string | api/__init__.py:ErrorCode | AC3: ErrorCode("AUTH_INVALID_SIGNATURE") construction |
| 11 | test_serialization_round_trip | api/__init__.py:ApiResponse | AC4: model_dump -> model_validate round-trip |
| 12 | test_paginated_response_middle_page | api/__init__.py:PaginatedResponse | AC2: has_next for middle/last/beyond-last pages |

### Coverage Targets
| Module | Line Target | Actual |
|--------|-------------|--------|
| omnibot/api/__init__.py | >= 80% | 100% |

### FR-10 Acceptance Criteria Mapping
- **AC1**: ApiResponse[T] contains success/data/error/error_code with defaults -> tests #1, #2, #3, #4
- **AC2**: PaginatedResponse inherits ApiResponse, adds total/page/limit/has_next -> tests #5, #6, #7, #8, #12
- **AC3**: ErrorCode str enum with 5 members (AUTH_INVALID_SIGNATURE, RATE_LIMIT_EXCEEDED, KNOWLEDGE_NOT_FOUND, VALIDATION_ERROR, INTERNAL_ERROR) + from-string construction -> tests #9, #10
- **AC4**: JSON serialization round-trip via Pydantic model_dump/model_validate -> test #11

### Exclusions
- None -- FR-10 is a pure data model definition with full coverage

---

## FR-13: Docker Compose Dev Environment

### Scope
[FR-13] Verify that docker-compose.yml defines 3 services (omnibot-api on port 8000, postgres pgvector/pg16, redis 7-alpine), postgres and redis have healthchecks, API depends_on both with service_healthy condition, and redis has requirepass password protection.

Citations: SRS.md FR-13 section, SAD.md 2.8.1

### Test Suite: `tests/test_fr13.py`

| # | Test Case | Target | AC Verified |
|---|-----------|--------|-------------|
| 1 | test_compose_file_exists | docker-compose.yml | AC1: Compose file present in project root |
| 2 | test_dockerfile_exists | 03-development/Dockerfile | AC1: Dockerfile present for API image |
| 3 | test_three_services | docker-compose.yml services | AC2: Exactly 3 services defined |
| 4 | test_service_names | docker-compose.yml services | AC2: omnibot-api, postgres, redis |
| 5 | test_postgres_image | postgres service image | AC3: pgvector/pgvector:pg16 image |
| 6 | test_redis_image | redis service image | AC4: redis:7-alpine image |
| 7 | test_api_port_mapping | omnibot-api ports | AC5: Port 8000 exposed |
| 8 | test_postgres_healthcheck | postgres healthcheck | AC6: postgres has healthcheck |
| 9 | test_redis_healthcheck | redis healthcheck | AC6: redis has healthcheck |
| 10 | test_api_depends_on_both | omnibot-api depends_on | AC7: API depends on postgres and redis |
| 11 | test_api_depends_condition_healthy | omnibot-api depends_on condition | AC7: condition=service_healthy for both |
| 12 | test_redis_requirepass | redis command/environment | AC8: Redis has requirepass password protection |

### Coverage Targets
| Module | Line Target | Actual |
|--------|-------------|--------|
| docker-compose.yml (structural) | >= 80% structural coverage | N/A -- static YAML validation |

Note: FR-13 tests validate docker-compose.yml structure via YAML parsing. No Python source module is exercised, so line coverage is not applicable. The `--cov` flag targets a module the tests do not import, producing 0% as expected.

### FR-13 Acceptance Criteria Mapping
- **AC1**: docker-compose.yml and Dockerfile exist -> tests #1, #2
- **AC2**: Three named services (omnibot-api, postgres, redis) -> tests #3, #4
- **AC3**: postgres uses pgvector/pgvector:pg16 image -> test #5
- **AC4**: redis uses redis:7-alpine image -> test #6
- **AC5**: API exposes port 8000 -> test #7
- **AC6**: postgres and redis have healthchecks -> tests #8, #9
- **AC7**: API depends_on both with service_healthy condition -> tests #10, #11
- **AC8**: Redis has requirepass password protection -> test #12

### Exclusions
- Actual `docker compose up` integration testing (requires Docker daemon; beyond unit test scope)
- Container startup time / resource limits (Docker-level concerns)
- Volume mount verification (infrastructure, not FR-13 spec)
- Network configuration (default bridge mode acceptable)

---

## FR-12: Database Schema — All Core Tables

### Scope
[FR-12] Verify that the schema module defines exactly 8 tables with correct columns, constraints, and type annotations. Validate Phase 2/3 reserved columns are present (sla_deadline, priority, vector(384), TEXT[], JSONB). Confirm FOREIGN KEY REFERENCES and PRIMARY KEY presence on every table via `get_schema_sql()`.

Citations: SRS.md FR-12 section, SAD.md 2.7.1 Schema Summary

### Test Suite: `tests/test_fr12.py`

| # | Test Case | Target | AC Verified |
|---|-----------|--------|-------------|
| 1 | test_schema_has_eight_tables | schema/__init__.py:TABLE_DEFS | AC1: Exactly 8 tables |
| 2 | test_required_tables_exist | schema/__init__.py:TABLE_DEFS | AC1: All 8 table names present |
| 3 | test_users_columns | schema/__init__.py:get_schema_sql | AC2: unified_user_id UUID, platform, platform_user_id, UNIQUE |
| 4 | test_conversations_columns | schema/__init__.py:get_schema_sql | AC3: satisfaction_score, first_contact_resolution, dst_state JSONB |
| 5 | test_messages_columns | schema/__init__.py:get_schema_sql | AC4: intent_detected, sentiment_category, sentiment_intensity, knowledge_source |
| 6 | test_knowledge_base_columns | schema/__init__.py:get_schema_sql | AC5: embeddings vector(384), keywords TEXT[], version, is_active |
| 7 | test_platform_configs_columns | schema/__init__.py:get_schema_sql | AC6: rate_limit_rps, webhook_secret_key_ref |
| 8 | test_escalation_queue_columns | schema/__init__.py:get_schema_sql | AC7: priority, sla_deadline (Phase 2 reserved) |
| 9 | test_user_feedback_columns | schema/__init__.py:get_schema_sql | AC8: feedback CHECK (thumbs_up / thumbs_down) |
| 10 | test_security_logs_columns | schema/__init__.py:get_schema_sql | AC9: layer, blocked, source_ip |
| 11 | test_foreign_keys_present | schema/__init__.py:get_schema_sql | AC10: REFERENCES constraint for FK relationships |
| 12 | test_schema_is_valid_sql | schema/__init__.py:get_schema_sql | AC11: Non-empty valid DDL starting with CREATE TABLE |
| 13 | test_each_table_has_id | schema/__init__.py:TABLE_DEFS | AC12: Every table has id + PRIMARY KEY |

### Coverage Targets
| Module | Line Target | Actual |
|--------|-------------|--------|
| omnibot/schema/__init__.py | >= 80% | 100% |

### FR-12 Acceptance Criteria Mapping
- **AC1** (8 tables): users, conversations, messages, knowledge_base, platform_configs, escalation_queue, user_feedback, security_logs -- tests #1, #2
- **AC2** (users columns): unified_user_id UUID, platform, platform_user_id, UNIQUE constraint -- test #3
- **AC3** (conversations columns): satisfaction_score, first_contact_resolution, scope_type, dst_state JSONB -- test #4
- **AC4** (messages columns): intent_detected, sentiment_category, sentiment_intensity, knowledge_source -- test #5
- **AC5** (knowledge_base columns): embeddings vector(384), keywords TEXT[], version -- test #6
- **AC6** (platform_configs columns): rate_limit_rps, webhook_secret_key_ref -- test #7
- **AC7** (escalation_queue Phase 2 columns): priority, sla_deadline -- test #8
- **AC8** (user_feedback CHECK): feedback column CHECK (thumbs_up / thumbs_down) -- test #9
- **AC9** (security_logs columns): layer, blocked, source_ip -- test #10
- **AC10** (foreign keys): REFERENCES constraint present in DDL -- test #11
- **AC11** (valid SQL): get_schema_sql() returns non-empty CREATE TABLE string -- test #12
- **AC12** (primary keys): Every table has id column as PRIMARY KEY -- test #13

### Exclusions
- Schema migration / versioning (Phase 4+)
- Actual database connection and DDL execution (schema is declarative -- validated via DDL string assertions)
- pgvector extension availability detection (Phase 3 integration concern)
- Column-level NOT NULL / DEFAULT granularity (DDL-level assertions only)

---

## FR-11: Health Check Endpoint

### Scope
[FR-11] Verify that GET /api/v1/health returns JSON {status, postgres, redis, uptime_seconds} with status derived from postgres + redis connectivity booleans. Status is healthy (both true), degraded (exactly one false), or unhealthy (both false). Uptime_seconds is computed via time.monotonic() and must be present, non-negative, and monotonic.

Citations: SRS.md FR-11 section, SAD.md 2.5.3 HealthCheck

### Test Suite: `tests/test_fr11.py`

| # | Test Case | Target | AC Verified |
|---|-----------|--------|-------------|
| 1 | test_health_status_enum | health/__init__.py:HealthStatus | AC1: Status enum healthy/degraded/unhealthy |
| 2 | test_both_up_is_healthy | health/__init__.py:HealthCheckService.check | AC2: postgres=True, redis=True -> healthy |
| 3 | test_both_down_is_unhealthy | health/__init__.py:HealthCheckService.check | AC2: postgres=False, redis=False -> unhealthy |
| 4 | test_postgres_down_is_degraded | health/__init__.py:HealthCheckService.check | AC2: exactly one False -> degraded |
| 5 | test_redis_down_is_degraded | health/__init__.py:HealthCheckService.check | AC2: exactly one False -> degraded |
| 6 | test_uptime_seconds_present | health/__init__.py:HealthCheckService.check | AC3: uptime_seconds in response, non-negative |
| 7 | test_response_keys | health/__init__.py:HealthCheckService.check | AC4: Exactly {status, postgres, redis, uptime_seconds} |
| 8 | test_uptime_monotonic | health/__init__.py:HealthCheckService.check | AC3: uptime_seconds increases between calls |
| 9 | test_health_endpoint_http | app.py health route | AC5: GET /api/v1/health returns 200 with JSON |

### Coverage Targets
| Module | Line Target | Actual |
|--------|-------------|--------|
| health/__init__.py | >= 80% | 100% |

### FR-11 Acceptance Criteria Mapping
- **AC1**: HealthStatus enum with healthy/degraded/unhealthy values -> test #1
- **AC2**: Status derived from postgres + redis connectivity -> tests #2, #3, #4, #5
- **AC3**: uptime_seconds present, non-negative, monotonic -> tests #6, #8
- **AC4**: Response keys exactly {status, postgres, redis, uptime_seconds} -> test #7
- **AC5**: HTTP 200 with valid JSON body -> test #9

### Exclusions
- Real database connectivity checks (Phase 1 uses stub callables; app.py wires lambda: False)
- Prometheus metrics endpoint (future feature)
- /health/live and /health/ready split (Kubernetes-style endpoints deferred)
- SLA-based health thresholds (future feature)
