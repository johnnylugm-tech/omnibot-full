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
