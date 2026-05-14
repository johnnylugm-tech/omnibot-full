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
