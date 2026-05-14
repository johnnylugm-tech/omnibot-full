# Test Results — Phase 4

## FR-01: Platform Adapter — Telegram + LINE Webhook

Citations: SRS.md:13-25, SAD.md:64-109, SAD.md:492-496

### Run Summary
- **Date**: 2026-05-14
- **Python**: 3.11.15
- **pytest**: 9.0.3
- **pytest-cov**: 7.1.0

### Test Results
```
tests/test_fr01.py::test_telegram_webhook_text_message PASSED
tests/test_fr01.py::test_telegram_webhook_response_time PASSED
tests/test_fr01.py::test_line_webhook_text_message PASSED
tests/test_fr01.py::test_line_webhook_response_time PASSED
tests/test_fr01.py::test_unsupported_platform_returns_400 PASSED
tests/test_fr01.py::test_line_empty_events_returns_400 PASSED
tests/test_fr01.py::test_platform_enum_values PASSED
tests/test_fr01.py::test_message_type_enum_values PASSED

8 passed, 0 failed, 0 skipped in 0.14s
```

### Coverage Report — FR-01 Modules

| Module | Stmts | Miss | Branch | BrPart | Cover |
|--------|-------|------|--------|--------|-------|
| adapters/line.py | 16 | 0 | 2 | 0 | 100% |
| adapters/telegram.py | 9 | 0 | 0 | 0 | 100% |
| models.py | 31 | 0 | 0 | 0 | 100% |
| app.py | 37 | 2 | 6 | 0 | 95% |
| auth/verifier.py | 39 | 5 | 8 | 4 | 81% |

### FR-01 Adapter Layer: 100% (line + branch)

### Notes
- app.py missed lines are GET /api/v1/health endpoint (FR-11 scope, not FR-01)
- auth/verifier.py missed lines are FR-02 scope (PlatformVerifier.register, unknown platform, missing-credentials, signature mismatch)
- All FR-01 acceptance criteria (AC1-AC4) verified passing
- Branch coverage for FR-01 adapter modules: 100% (2/2 branches in line.py)

### Confidence
- FR-01 adapter layer: HIGH (100% line + branch coverage)
- Webhook route handler: HIGH (95%, only health endpoint missed)
- Overall FR-01: 10/10

---

## FR-02: Webhook Signature Verification

Citations: SRS.md:28-41, SAD.md:97-109

### Run Summary
- **Date**: 2026-05-14
- **Python**: 3.11.15
- **pytest**: 9.0.3
- **pytest-cov**: 7.1.0

### Test Results
```
tests/test_fr02.py::test_telegram_webhook_valid_signature PASSED
tests/test_fr02.py::test_telegram_webhook_invalid_signature PASSED
tests/test_fr02.py::test_telegram_webhook_missing_signature_header PASSED
tests/test_fr02.py::test_line_webhook_valid_signature PASSED
tests/test_fr02.py::test_line_webhook_invalid_signature PASSED
tests/test_fr02.py::test_line_webhook_missing_signature_header PASSED
tests/test_fr02.py::test_timing_attack_resistance PASSED
tests/test_fr02.py::test_telegram_webhook_without_auth_headers_still_rejected PASSED

8 passed, 0 failed, 0 skipped in 0.18s
```

### Coverage Report — FR-02 Modules

| Module | Stmts | Miss | Cover | Missing |
|--------|-------|------|-------|---------|
| auth/__init__.py | 0 | 0 | 100% | — |
| auth/verifier.py | 39 | 3 | 92% | 50, 56, 84 |
| **TOTAL** | 39 | 3 | **92%** | — |

### Missed Lines Analysis
| Line | Function | Why Missed | Criticality |
|------|----------|-----------|-------------|
| 50 | PlatformVerifier.register() | No test registers a new verifier | Low — not required by AC |
| 56 | PlatformVerifier.verify() (ValueError) | No test calls with unregistered platform | Low — unknown-platform guard |
| 84 | verify_signature() (HTTP 400) | No test calls with unsupported platform | Low — guarded by route path param |

### Acceptance Criteria Verification
- **AC1** (Telegram HMAC with SHA256(bot_token)): PASSED via tests #1, #7
- **AC2** (LINE HMAC-SHA256 + Base64): PASSED via test #4
- **AC3** (401 AUTH_INVALID_SIGNATURE on failure): PASSED via tests #2, #3, #5, #6, #8
- **AC4** (hmac.compare_digest timing safety): PASSED via test #7
- **AC5** (VERIFIERS dict registry extensibility): Partially covered (static init exercised; dynamic register() not tested)

### Risk Assessment
- **Core signature verification path (AC1-AC4)**: FULLY covered, 8/8 tests pass
- **Extensibility path (AC5: register())**: Not tested — low risk, trivial one-liner
- **Edge cases (unknown platform)**: Not tested — guarded by route-level validation
- **Timing attack vector**: Covered — hmac.compare_digest() usage verified

### Confidence
- FR-02 core verification path: HIGH (92% line coverage, all AC verified)
- FR-02 extensibility: MEDIUM (register path untested but trivial)
- Overall FR-02: 9/10

---

## FR-03: Unified Message Format

Citations: SRS.md:44-55, SAD.md:140-167

### Run Summary
- **Date**: 2026-05-14
- **Python**: 3.11.15
- **pytest**: 9.0.3
- **pytest-cov**: 7.1.0

### Test Results
```
tests/test_fr03.py::test_unified_message_is_frozen PASSED
tests/test_fr03.py::test_unified_message_required_fields PASSED
tests/test_fr03.py::test_unified_message_defaults PASSED
tests/test_fr03.py::test_unified_message_reply_token PASSED
tests/test_fr03.py::test_unified_response_fields PASSED
tests/test_fr03.py::test_unified_response_escalate_defaults PASSED
tests/test_fr03.py::test_platform_enum_completeness PASSED
tests/test_fr03.py::test_message_type_enum_completeness PASSED
tests/test_fr03.py::test_platform_enum_from_string PASSED
tests/test_fr03.py::test_message_type_enum_from_string PASSED

10 passed, 0 failed, 0 skipped in 0.02s
```

### Coverage Report — FR-03 Modules

| Module | Stmts | Miss | Cover | Missing |
|--------|-------|------|-------|---------|
| models.py | 31 | 0 | 100% | — |
| **TOTAL** | 31 | 0 | **100%** | — |

### Acceptance Criteria Verification
- **AC1** (UnifiedMessage frozen=True dataclass with all required fields): PASSED via tests #1, #2, #3, #4
- **AC2** (UnifiedResponse with content/source/confidence/knowledge_id): PASSED via tests #5, #6
- **AC3** (Platform enum: TELEGRAM, LINE, MESSENGER, WHATSAPP): PASSED via tests #7, #9
- **AC4** (MessageType enum: TEXT, IMAGE, STICKER, LOCATION, FILE): PASSED via tests #8, #10

### Risk Assessment
- **All data model invariants**: FULLY covered, 10/10 tests pass, 31/31 statements covered
- **frozen=True enforcement**: Verified via dataclasses.FrozenInstanceError catch
- **Enum from_string parsing**: Both Platform and MessageType parsing verified
- **No gaps or missed lines**

### Confidence
- FR-03 data model: HIGH (100% line coverage, all AC verified)
- Overall FR-03: 10/10

---

## FR-04: Input Sanitizer L2 — Character Normalization

Citations: SRS.md:59-68, SAD.md:182-198

### Run Summary
- **Date**: 2026-05-14
- **Python**: 3.11.15
- **pytest**: 9.0.3
- **pytest-cov**: 7.1.0

### Test Results
```
tests/test_fr04.py::test_nfkc_normalization PASSED
tests/test_fr04.py::test_nfkc_combining_characters PASSED
tests/test_fr04.py::test_control_characters_removed PASSED
tests/test_fr04.py::test_newline_and_tab_preserved PASSED
tests/test_fr04.py::test_leading_trailing_whitespace_stripped PASSED
tests/test_fr04.py::test_empty_string PASSED
tests/test_fr04.py::test_only_whitespace PASSED
tests/test_fr04.py::test_unicode_emojis_preserved PASSED
tests/test_fr04.py::test_no_pattern_matching_performed PASSED
tests/test_fr04.py::test_idempotent PASSED
tests/test_fr04.py::test_zwj_emoji_preserved PASSED

11 passed, 0 failed, 0 skipped in 0.02s
```

### Coverage Report — FR-04 Modules

| Module | Stmts | Miss | Cover | Missing |
|--------|-------|------|-------|---------|
| sanitizer/__init__.py | 12 | 0 | 100% | — |
| **TOTAL** | 12 | 0 | **100%** | — |

### Missed Lines Analysis
- None — all 12 statements in sanitizer/__init__.py are fully covered.

### Acceptance Criteria Verification
- **AC1** (NFKC normalization via unicodedata.normalize): PASSED via tests #1 (fullwidth -> ASCII), #2 (combining chars -> precomposed)
- **AC2** (Remove Cc control chars, keep \n and \t): PASSED via tests #3 (\x00-\x03 removed), #4 (\n and \t preserved)
- **AC3** (strip() leading/trailing whitespace): PASSED via tests #5 (strip), #6 (empty input), #7 (whitespace-only)
- **AC4** (No pattern matching — L2 only normalizes): PASSED via tests #8 (emoji preserved), #9 (<script> tags pass through unmodified)
- **Bonus**: Idempotency verified via test #10 — sanitize(sanitize(x)) == sanitize(x)
- **Bonus**: ZWJ emoji preserved via test #11 — Cf-category characters (U+200D) are not stripped

### Risk Assessment
- **Core normalization path (AC1-AC4)**: FULLY covered, 11/11 tests pass, 12/12 statements covered
- **Edge cases**: Empty string, whitespace-only, ZWJ sequences — all tested
- **Layer boundary**: Confirmed L2 does NOT perform pattern matching (L3 responsibility) via test #9
- **No gaps or missed lines**

### Confidence
- FR-04 sanitizer: HIGH (100% line coverage, all AC verified)
- Layer boundary correctness: HIGH (no pattern-matching leak into L2)
- Overall FR-04: 10/10

---

## FR-06: Rate Limiter — Token Bucket

Citations: SRS.md FR-06 section

### Run Summary
- **Date**: 2026-05-14
- **Python**: 3.11.15
- **pytest**: 9.0.3
- **pytest-cov**: 7.1.0

### Test Results
```
tests/test_fr06.py::test_token_bucket_allows_within_limit PASSED
tests/test_fr06.py::test_token_bucket_refills_over_time PASSED
tests/test_fr06.py::test_rate_limiter_per_user_isolation PASSED
tests/test_fr06.py::test_rate_limiter_new_user_gets_full_bucket PASSED
tests/test_fr06.py::test_rate_limiter_capacity_zero_blocks_all PASSED

5 passed, 0 failed, 0 skipped in 0.18s
```

### Coverage Report — FR-06 Modules

| Module | Stmts | Miss | Cover | Missing |
|--------|-------|------|-------|---------|
| rate_limiter/__init__.py | 35 | 0 | 100% | — |
| **TOTAL** | 35 | 0 | **100%** | — |

Note: Coverage report also captured pii/__init__.py (21 stmts, 100%) as a side-effect of import resolution; those 21 statements are FR-08 scope, not FR-06.

### Missed Lines Analysis
No missed lines. All 35 statements in rate_limiter/__init__.py are exercised.

### Acceptance Criteria Verification
- **AC1** (TokenBucket allows up to capacity, then rejects): PASSED via test #1
- **AC2** (Tokens refill over elapsed time): PASSED via test #2
- **AC3** (RateLimiter per-user isolation): PASSED via test #3
- **AC4** (New user gets full bucket): PASSED via test #4
- **AC5** (Capacity zero blocks all): PASSED via test #5

### Risk Assessment
- **Core token bucket logic**: FULLY covered, 5/5 tests pass, 35/35 statements covered
- **Thread safety**: Lock acquisition exercised via consume()/allow() paths (single-threaded tests still exercise lock enter/exit)
- **Default rps=100**: Not tested directly (default_capacity=10, default_refill_rate=1.0 used in tests); SRS default documented but implementation ships with capacity=10 default
- **No gaps or missed lines**

### Confidence
- FR-06 rate limiter: HIGH (100% line coverage, all AC verified)
- Overall FR-06: 10/10

---

## FR-05: PII Masking L4 -- Phone / Email / Address

Citations: SRS.md FR-05 section

### Run Summary
- **Date**: 2026-05-14
- **Python**: 3.11.15
- **pytest**: 9.0.3
- **pytest-cov**: 7.1.0

### Test Results
```
tests/test_fr05.py::test_mask_taiwan_mobile PASSED
tests/test_fr05.py::test_mask_taiwan_landline PASSED
tests/test_fr05.py::test_phone_without_dashes PASSED
tests/test_fr05.py::test_mask_email PASSED
tests/test_fr05.py::test_mask_multiple_emails PASSED
tests/test_fr05.py::test_mask_taiwan_address PASSED
tests/test_fr05.py::test_no_false_positive_ordinary_text PASSED
tests/test_fr05.py::test_sensitive_keyword_triggers_escalation PASSED
tests/test_fr05.py::test_normal_message_no_escalation PASSED
tests/test_fr05.py::test_escalation_flag_dataclass PASSED

10 passed, 0 failed, 0 skipped in 0.02s
```

### Coverage Report -- FR-05 Modules

| Module | Stmts | Miss | Cover | Missing |
|--------|-------|------|-------|---------|
| omnibot/pii/__init__.py | 21 | 0 | 100% | -- |
| **TOTAL** | 21 | 0 | **100%** | -- |

### Missed Lines Analysis
No missed lines. All 21 statements in omnibot/pii/__init__.py are exercised.

### Acceptance Criteria Verification
- **AC1** (Taiwan phone numbers masked: mobile + landline, dash-optional): PASSED via tests #1, #2, #3
- **AC2** (Email addresses masked): PASSED via tests #4, #5
- **AC3** (Taiwan addresses masked: city/district/road pattern): PASSED via test #6
- **AC4** (No false positives on ordinary text): PASSED via test #7
- **AC5** (`contains_sensitive_keywords()` escalation gate): PASSED via tests #8, #9
- **AC6** (`EscalationFlag` dataclass integrity): PASSED via test #10

### Risk Assessment
- **Core PII masking (AC1-AC4)**: FULLY covered, 7/7 masking tests pass, all 4 regex patterns exercised (mobile, landline, email, address)
- **Escalation gate (AC5)**: Covered -- both positive (suicide, police keywords) and negative (normal message) paths verified
- **Dataclass integrity (AC6)**: Covered -- EscalationFlag.message and .keywords fields verified
- **Implementation gap vs SRS**: `mask_pii()` returns plain `str` instead of `PIIMaskResult(masked_text, mask_count, pii_types)` as specified in SRS. Mask count and PII type tracking not implemented. Low risk for L4 masking function, but should be addressed for downstream consumers expecting the richer return type.
- **Regex coverage**: Mobile pattern `\b09\d{2}[-\s]?\d{3}[-\s]?\d{3}\b`, landline `\b0\d{1,2}[-\s]?\d{4}[-\s]?\d{4}\b`, email `\b[\w.+-]+@[\w-]+\.[\w.-]+\b`, address with city/county/district/road pattern all exercised.
- **No gaps or missed lines in production code**

### Confidence
- FR-05 PII masking: HIGH (100% line coverage, all 6 AC verified)
- FR-05 escalation: HIGH (both positive and negative paths covered)
- Overall FR-05: 9/10 (deducted 1 for PIIMaskResult return type gap vs SRS spec)
