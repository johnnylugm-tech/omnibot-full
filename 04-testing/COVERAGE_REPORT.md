# Coverage Report — Phase 4 (24 FRs)

> Generated: 2026-05-18 | pytest-cov | Python 3.11
> Total tests: 396 (all passing)

## Aggregate Coverage (Source Modules)

| Metric | Value |
|--------|-------|
| Total statements | 854 |
| Covered | 838 |
| Missed | 16 |
| Line coverage | 98% |
| FRs with 100% coverage | 18/24 |
| Modules below 80% threshold | 0 |

## Per-Module Coverage

| Module | Stmts | Miss | Cover |
|--------|-------|------|-------|
| adapters/telegram.py | 9 | 0 | 100% |
| adapters/line.py | 16 | 0 | 100% |
| adapters/messenger.py | 16 | 0 | 100% |
| adapters/whatsapp.py | 18 | 0 | 100% |
| api/__init__.py | 23 | 0 | 100% |
| app.py | 38 | 3 | 92% |
| auth/verifier.py | 43 | 3 | 93% |
| dataset.py | 55 | 0 | 100% |
| defense.py | 24 | 0 | 100% |
| dst.py | 35 | 0 | 100% |
| emotion.py | 46 | 1 | 98% |
| escalation/__init__.py | 36 | 0 | 100% |
| escalation/v2.py | 46 | 0 | 100% |
| grounding.py | 42 | 4 | 90% |
| health/__init__.py | 21 | 0 | 100% |
| knowledge/__init__.py | 34 | 0 | 100% |
| knowledge/v2.py | 127 | 3 | 98% |
| logger/__init__.py | 23 | 0 | 100% |
| metrics.py | 13 | 0 | 100% |
| models.py | 37 | 0 | 100% |
| pii/__init__.py | 85 | 0 | 100% |
| rate_limiter/__init__.py | 35 | 0 | 100% |
| router.py | 9 | 0 | 100% |
| sanitizer/__init__.py | 15 | 2 | 87% |
| schema/__init__.py | 8 | 0 | 100% |
| **Total (source only)** | **854** | **16** | **98%** |

## NFR Coverage

| NFR | Verified By | Result |
|-----|-------------|--------|
| NFR-10 | 100% webhook verification (4 platforms) | ✅ |
| NFR-11 | PII masking + Luhn credit card | ✅ |
| NFR-12 | Injection block rate ≥95% (100 inputs) | ✅ |
| NFR-13 | Grounding cosine ≥0.75 | ✅ |
| NFR-14 | SLA compliance ≥90% | ✅ |
| NFR-15 | Golden dataset ≥500 edge cases | ✅ (510) |

## Notes

- Coverage measured on `03-development/src/omnibot/` source modules only
- 25 test files (24 per-FR + 1 performance), 396 tests, all passing
- All 24 FRs have dedicated test files with real assertions
- Modules below 80% threshold: none
