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
