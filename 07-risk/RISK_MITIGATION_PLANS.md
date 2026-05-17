# Risk Mitigation Plans — Phase 3 (24 FRs)

> Generated: 2026-05-17

## Implemented Mitigations

### Security (FR-15, FR-02, FR-06)
- **Prompt injection**: 10-pattern regex detection, sandwich defense for LLM, NFKC normalization
- **Webhook spoofing**: HMAC-SHA256 per platform, hmac.compare_digest timing attack protection
- **Rate limit abuse**: Token bucket algorithm, per-user + per-IP isolation

### Privacy (FR-16, FR-05)
- **PII exposure**: Regex patterns + Luhn algorithm for credit cards, masking levels
- **False positives**: Luhn validation eliminates non-valid credit card patterns

### Quality (FR-21, FR-24)
- **LLM hallucination**: Cosine similarity ≥0.75 grounding check, ungrounded outputs escalated
- **Regression**: Golden dataset 510 edge cases auto-verified on pipeline run

### Operations (FR-20, FR-22)
- **SLA breach**: Priority-based deadlines, automated breach query
- **Observability**: 8 Prometheus metrics, health check endpoint
