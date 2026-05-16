# Phase 8 Full Execution Plan -- omnibot-full

> **Version**: v2.3.0 (project plan)
> **Project**: omnibot-full
> **Date**: 2026-05-16
> **Framework**: harness-methodology v2.3.0
> **Phase**: 8 - Configuration Management
> **Status**: Full version (including Phase 8 detailed tasks)

---

## Phase 8 Tasks: Configuration Management

### Phase 8 Overview
Phase 8 establishes a complete configuration management system ensuring traceability.
Each FR gets a Gate 1 config-aware re-evaluation (CHECKPOINT). No phase-exit gate — P8 cleared by Gate 4.

> **Crash Recovery**: at each **milestone push**, `HANDOVER.md` is written to project root.
> If context is lost, read `HANDOVER.md` first — it contains phase, status, and next steps.
> Per-FR Gate 1 = **local commit only** (no push, no HANDOVER). Push happens at milestones.

> **Checkpoint Index**:
> - CHECKPOINT-1: Gate 1 / FR-01 *(local commit)*
> - CHECKPOINT-2: Gate 1 / FR-02 *(local commit)*
> - CHECKPOINT-3: Gate 1 / FR-03 *(local commit)*
> - CHECKPOINT-4: Gate 1 / FR-04 *(local commit)*
> - CHECKPOINT-5: Gate 1 / FR-05 *(local commit)*
> - CHECKPOINT-6: Gate 1 / FR-06 *(local commit)*
> - CHECKPOINT-7: Gate 1 / FR-07 *(local commit)*
> - CHECKPOINT-8: Gate 1 / FR-08 *(local commit)*
> - CHECKPOINT-9: Gate 1 / FR-09 *(local commit)*
> - CHECKPOINT-10: Gate 1 / FR-10 *(local commit)*
> - CHECKPOINT-11: Gate 1 / FR-11 *(local commit)*
> - CHECKPOINT-12: Gate 1 / FR-12 *(local commit)*
> - CHECKPOINT-13: Gate 1 / FR-13 *(local commit)*
> - MILESTONE: P8 exit push (config records complete) → **HANDOVER.md**

### Entry Gate Verification

- [ ] **[ENTRY-CHECK]** Confirm Phase 6 exit (Gate 4 PASS) before proceeding (HR-03 — no phase skips):
  Proof: .methodology/quality_manifest.json records Gate 4 PASS from P6.
  If NOT confirmed: return to Phase 6 and complete exit gate first.

### Pre-Phase Preflight

- [ ] **[PREFLIGHT]** Run phase hooks (FSM, Constitution, Kill-Switch, Drift, CI Readiness):
  ```bash
  python3 harness_cli.py run-phase --phase 8 --project $REPO
  ```
  If FAILED: fix FSM/Constitution issues. There is no gate bypass flag.

- [ ] **[PREFLIGHT-CI]** Confirm CI wiring unchanged (should be set since P1):
  1. `.github/workflows/harness_quality_gate.yml` exists
  2. Git hooks installed (`ls .git/hooks/prepare-commit-msg`)
  3. harness importable (submodule, PYTHONPATH, or vendored `quality_gate/`)
  4. GitHub repo variable `CURRENT_PHASE` = 8 (updated by `advance-phase`)
  > If stale: run `python3 harness_cli.py init-project --phase 8 --project $REPO --overwrite`

### Configuration Items (20 total)

- **Variable**: configuration record required
- ****Secrets Management**: All production secrets must be stored in a secrets manager (e.g., HashiCorp Vault, AWS Secrets Manager, or Kubernetes Secrets). Never hardcode production credentials.

---

## FR-01: Platform Adapter Configuration

> **[FR-01]** Platform Adapter — Telegram + LINE Webhook
> Citations: SRS.md:13-25, 03-development/src/omnibot/auth/verifier.py:65-74

### Environment Variables / Secrets**: configuration record required
- ****Secrets Management**: Store both values in a secrets manager (HashiCorp Vault, AWS Secrets Manager, or Kubernetes Secrets). Never commit to version control. Rotate immediately if exposed.

### Webhook Endpoints**: configuration record required
- **Signature verification raises `401 Unauthorized` for missing or invalid signatures (see `03-development/src/omnibot/auth/verifier.py:77-103`).

### Deployment Checklist

- [ ] `TELEGRAM_BOT_TOKEN` injected via secrets manager (not `.env` in production)
- [ ] `LINE_CHANNEL_SECRET` injected via secrets manager (not `.env` in production)
- [ ] Webhook URL `https://<host>/api/v1/webhook/telegram` registered in **Telegram BotFather** via `/setWebhook`
- [ ] Webhook URL `https://<host>/api/v1/webhook/line` registered in **LINE Developer Console** under Messaging API → Webhook settings
- [ ] Webhook URLs use HTTPS (TLS 1.2+); self-signed certificates rejected by both platforms
- [ ] Response time p95 < 3.0 s verified under load (SRS.md:286)

### Security Notes

- **Telegram**: signature key is derived as `SHA256(TELEGRAM_BOT_TOKEN)` before HMAC — the raw token is never used directly as the HMAC key (`03-development/src/omnibot/auth/verifier.py:22-23`).
- **LINE**: signature is `Base64(HMAC-SHA256(LINE_CHANNEL_SECRET, body))`, compared via `hmac.compare_digest` to prevent timing attacks (`03-development/src/omnibot/auth/verifier.py:28-31`).
- Both secrets are passed per-request via headers in Phase 1; Phase 2 will migrate to server-side environment injection.
- Unsupported platforms are rejected with `400 Bad Request` before any business logic executes (`03-development/src/omnibot/router.py:21-26`).

---

## FR-02: Webhook Signature Verification Configuration

> **[FR-02]** Webhook Signature Verification — Telegram + LINE
> Citations: SRS.md:28-41, 03-development/src/omnibot/auth/verifier.py:17-31

### Environment Variables / Secrets

No new environment variables are required for FR-02. Signature verification reuses the same secrets provisioned for FR-01. Verification is entirely stateless.**: configuration record required
- **### Signature Verification Scheme**: configuration record required
- **----------**: configuration record required
- **`SHA256(TELEGRAM_BOT_TOKEN)`**: configuration record required
- **LINE**: configuration record required
- **- All comparisons use `hmac.compare_digest()` to prevent timing-attack leakage (`03-development/src/omnibot/auth/verifier.py:17-24`).
- Verification failure (missing header, wrong signature) returns `401 Unauthorized` with error code `AUTH_INVALID_SIGNATURE`.

### Deployment Checklist

- [ ] Confirm `TELEGRAM_BOT_TOKEN` and `LINE_CHANNEL_SECRET` are injected from secrets manager (shared with FR-01; no duplicate provisioning needed)
- [ ] Verify request headers `X-Telegram-Bot-Token`, `X-Telegram-Hmac-Signature`, `X-Line-Channel-Secret`, `X-Line-Signature` are forwarded untransformed by any reverse proxy / load balancer
- [ ] Test signature rejection path: send request with corrupted signature; confirm `401 AUTH_INVALID_SIGNATURE` response
- [ ] Secret rotation procedure:
  1. Generate new token / channel secret in BotFather / LINE Developer Console
  2. Store new value in secrets manager; keep old value active during rollover window
  3. Deploy new application version with updated secret reference
  4. Validate signature verification passes with new secret
  5. Remove old secret from secrets manager; confirm no requests are rejected
- [ ] Confirm `hmac.compare_digest` is used in all verification paths (not `==`) — see `03-development/src/omnibot/auth/verifier.py:17-24`

### Security Notes

- The raw `TELEGRAM_BOT_TOKEN` string is **never** used directly as an HMAC key; the key is always derived as `SHA256(token)` (`verifier.py:22-23`).
- `LINE_CHANNEL_SECRET` is used as the HMAC key without further hashing; ensure the secret itself has sufficient entropy (LINE enforces ≥ 32 chars).
- `hmac.compare_digest()` ensures constant-time comparison — do not replace with `==` or `!=`.
- No verification state is persisted; replay protection (nonce / timestamp) is out of scope for Phase 1.

---

## FR-03: Unified Message Format Configuration

> **[FR-03]** Unified Message Format — `UnifiedMessage` dataclass (`frozen=True`)
> Citations: SRS.md:44-55, 03-development/src/omnibot/models.py:12-55

### Environment Variables / Secrets

No environment variables are required for FR-03. `UnifiedMessage` and `UnifiedResponse` are pure
in-memory dataclasses with no external configuration dependencies.**: configuration record required
- **### Data Model Reference

**`Platform` enum** (`models.py:12-20`) — string-valued, `str, Enum`:**: configuration record required
- **Adding a new platform requires a **code change** (new enum member + adapter implementation); there is no runtime-configurable platform registry.

**`MessageType` enum** (`models.py:23-32`) — string-valued, `str, Enum`:**: configuration record required
- **Field**: configuration record required
- ****`UnifiedResponse` dataclass** (`models.py:59-68`) — `frozen=True`:**: configuration record required
- **### Deployment Checklist

- [ ] Verify all platform adapters (Telegram, LINE, Messenger, WhatsApp) construct `UnifiedMessage` with valid `Platform` and `MessageType` enum members before deploy
- [ ] Confirm no adapter passes raw string values for `platform` or `message_type` fields (must use enum members, not bare strings)
- [ ] Validate `unified_user_id` enrichment is applied before any cross-platform lookup
- [ ] Ensure `frozen=True` is preserved on both dataclasses — mutation attempts raise `FrozenInstanceError` and indicate a logic error in the caller
- [ ] Run adapter unit tests confirming `UnifiedMessage.to_json_dict()` produces ISO8601 `received_at` for downstream consumers

### Monitoring / Observability

Log the following fields on every inbound message for production observability:**: configuration record required
- **Do **not** log `raw_payload` at INFO or above — it may contain PII from platform webhooks.

### Security Notes

- `UnifiedMessage` is `frozen=True`; immutability prevents accidental mutation of verified message data as it passes through the processing pipeline.
- `raw_payload` is retained for audit/debugging but must not be forwarded to external services without scrubbing.
- No imports from `app/infrastructure/` are permitted in this module (pure domain model).

---

## FR-04: Input Sanitizer L2 Configuration

> **[FR-04]** Input Sanitizer L2 — Character Normalization
> Citations: SRS.md:59-68, 03-development/src/omnibot/sanitizer/__init__.py

### Environment Variables / Secrets

No environment variables are required for FR-04. The sanitizer is a pure function with no
configurable parameters in Phase 1. NFKC normalization is locale-independent and requires
no locale configuration.**: configuration record required
- **### Sanitization Pipeline (Phase 1)**: configuration record required
- **- **No external state**: the function holds no module-level mutable state and has no I/O side effects.
- **No infrastructure imports**: `app/infrastructure/` imports are forbidden in this module.

### Deployment Checklist

- [ ] Confirm sanitizer module has no imports from `app/infrastructure/` (pure domain function)
- [ ] Verify `unicodedata` is from the Python stdlib — no third-party Unicode library required
- [ ] Run unit tests covering: empty string, all-whitespace, mixed control characters, multi-codepoint Unicode (e.g. ligatures, full-width digits) to confirm NFKC decomposition
- [ ] Confirm `\n` (newline) and `\t` (tab) are preserved after sanitization
- [ ] Validate sanitizer is applied before any downstream processing (router, agent dispatch)

### Future Configuration (Phase 2)**: configuration record required
- **`MAX_INPUT_LENGTH` is intentionally omitted from Phase 1; introduce it as an environment variable
with a sensible default (e.g. `4096`) when DoS protection requirements are formalised.

### Monitoring / Observability**: configuration record required
- **Do **not** log raw input content at INFO or above — it may contain PII from platform webhooks.

### Security Notes

- NFKC normalization prevents homoglyph / Unicode-smuggling attacks by collapsing compatibility
  equivalents before any content inspection.
- Non-printable character removal reduces the surface for control-character injection into
  downstream log sinks or terminals.
- Phase 1 applies no length cap; operators should monitor for unusually long inputs and plan
  `MAX_INPUT_LENGTH` enforcement for Phase 2.

---

## FR-05: PII Masking L4 Configuration

> **[FR-05]** PII Masking L4 — Phone/Email/Address
> Citations: SRS.md:74-87, 03-development/src/omnibot/pii/__init__.py:25-93

### Environment Variables / Secrets

No environment variables are required for FR-05. All regex patterns and sensitive keyword lists
are hardcoded in Phase 1. PII masking is always on — there is no runtime toggle.**: configuration record required
- **### Implicit Configuration (Phase 1 — Hardcoded)**: configuration record required

### FR Configuration Evaluation (13 total)

#### FR-01: Configuration Record
- [ ] Confirm FR-01 configuration items are documented in CONFIG_RECORDS.md
- [ ] Confirm environment variables / secrets are managed (not hardcoded)
- [ ] Confirm deployment checklist entries for FR-01

**A/B Work — FR-01** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVOPS): Document config items → verify env vars/secrets → update CONFIG_RECORDS.md
  - Docstrings: `[FR-01]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-01 \
    --prompt "Document config items → verify env vars/secrets → update CONFIG_RECORDS.md for FR-01" --phase 8 --project $REPO
  ```
- [ ] **[B-1]** Agent B (ARCHITECT) for FR-01 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md`
  - `08-config/CONFIG_RECORDS.md (draft)`
  - `ops/ relevant configs`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-01.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (draft)] ===
  {paste full content here}

  === [DOC 3: ops/ relevant configs] ===
  {paste full content here}

  Review checklist:
  - All config items documented?
  - Secrets correctly externalized?
  - No hardcoded credentials?

  Return JSON only:
  {"status":"STAGE_PASS"|"REJECT","review_status":"APPROVE"|"REJECT",
   "reason":"...","confidence":1-10,"citations":["file:line"],"gaps":[...]}
  ```

- [ ] **[B-2]** Agent B returns JSON — parse `review_status`:
  - `APPROVE` → continue to next step
  - `REJECT` → Agent A fixes gaps → re-dispatch B. Max 5 rounds (HR-12).

- [ ] **[B-DISPATCH]** Dispatch Agent B:
  ```bash
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-01 \
    --prompt "Review FR-01 against SRS + SAD" --phase 8 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-1: Gate 1 — FR-01
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-01 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- $(python3 -c "from scripts.generate_full_plan import _fr_source_paths; print(' '.join(_fr_source_paths('FR-01')))" 2>/dev/null || echo '.')
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-01:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 8 --fr-id FR-01 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-01 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-01:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 8 --fr-id FR-01
  ```
  **If FAIL** (any dim below threshold): fix code → repeat G1a→G1b→G1c until PASS.
  **Do NOT proceed to G1d until all dims PASS.**

- [ ] **[SAB-SYNC]** Re-sync SAB.json after adding/moving source files:
  ```bash
  python3 scripts/generate_sab.py --project $REPO
  ```
  _(Keeps M2 SAB drift < 15% — postflight blocks gate finalization if exceeded)_

- [ ] **G1d** ✅ Verify local commit saved (finalize-gate above already committed):
  ```bash
  git log --oneline -1
  ```
  > `finalize-gate --gate 1` calls `commit_fr_gate1()` — **local commit only, no push**.
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p8-mid` / `p8-pre-ssi` / Gate exit.

#### FR-02: Configuration Record
- [ ] Confirm FR-02 configuration items are documented in CONFIG_RECORDS.md
- [ ] Confirm environment variables / secrets are managed (not hardcoded)
- [ ] Confirm deployment checklist entries for FR-02

**A/B Work — FR-02** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVOPS): Document config items → verify env vars/secrets → update CONFIG_RECORDS.md
  - Docstrings: `[FR-02]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-02 \
    --prompt "Document config items → verify env vars/secrets → update CONFIG_RECORDS.md for FR-02" --phase 8 --project $REPO
  ```
- [ ] **[B-1]** Agent B (ARCHITECT) for FR-02 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md`
  - `08-config/CONFIG_RECORDS.md (draft)`
  - `ops/ relevant configs`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-02.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (draft)] ===
  {paste full content here}

  === [DOC 3: ops/ relevant configs] ===
  {paste full content here}

  Review checklist:
  - All config items documented?
  - Secrets correctly externalized?
  - No hardcoded credentials?

  Return JSON only:
  {"status":"STAGE_PASS"|"REJECT","review_status":"APPROVE"|"REJECT",
   "reason":"...","confidence":1-10,"citations":["file:line"],"gaps":[...]}
  ```

- [ ] **[B-2]** Agent B returns JSON — parse `review_status`:
  - `APPROVE` → continue to next step
  - `REJECT` → Agent A fixes gaps → re-dispatch B. Max 5 rounds (HR-12).

- [ ] **[B-DISPATCH]** Dispatch Agent B:
  ```bash
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-02 \
    --prompt "Review FR-02 against SRS + SAD" --phase 8 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-2: Gate 1 — FR-02
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-02 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- $(python3 -c "from scripts.generate_full_plan import _fr_source_paths; print(' '.join(_fr_source_paths('FR-02')))" 2>/dev/null || echo '.')
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-02:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 8 --fr-id FR-02 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-02 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-02:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 8 --fr-id FR-02
  ```
  **If FAIL** (any dim below threshold): fix code → repeat G1a→G1b→G1c until PASS.
  **Do NOT proceed to G1d until all dims PASS.**

- [ ] **[SAB-SYNC]** Re-sync SAB.json after adding/moving source files:
  ```bash
  python3 scripts/generate_sab.py --project $REPO
  ```
  _(Keeps M2 SAB drift < 15% — postflight blocks gate finalization if exceeded)_

- [ ] **G1d** ✅ Verify local commit saved (finalize-gate above already committed):
  ```bash
  git log --oneline -1
  ```
  > `finalize-gate --gate 1` calls `commit_fr_gate1()` — **local commit only, no push**.
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p8-mid` / `p8-pre-ssi` / Gate exit.

#### FR-03: Configuration Record
- [ ] Confirm FR-03 configuration items are documented in CONFIG_RECORDS.md
- [ ] Confirm environment variables / secrets are managed (not hardcoded)
- [ ] Confirm deployment checklist entries for FR-03

**A/B Work — FR-03** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVOPS): Document config items → verify env vars/secrets → update CONFIG_RECORDS.md
  - Docstrings: `[FR-03]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-03 \
    --prompt "Document config items → verify env vars/secrets → update CONFIG_RECORDS.md for FR-03" --phase 8 --project $REPO
  ```
- [ ] **[B-1]** Agent B (ARCHITECT) for FR-03 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md`
  - `08-config/CONFIG_RECORDS.md (draft)`
  - `ops/ relevant configs`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-03.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (draft)] ===
  {paste full content here}

  === [DOC 3: ops/ relevant configs] ===
  {paste full content here}

  Review checklist:
  - All config items documented?
  - Secrets correctly externalized?
  - No hardcoded credentials?

  Return JSON only:
  {"status":"STAGE_PASS"|"REJECT","review_status":"APPROVE"|"REJECT",
   "reason":"...","confidence":1-10,"citations":["file:line"],"gaps":[...]}
  ```

- [ ] **[B-2]** Agent B returns JSON — parse `review_status`:
  - `APPROVE` → continue to next step
  - `REJECT` → Agent A fixes gaps → re-dispatch B. Max 5 rounds (HR-12).

- [ ] **[B-DISPATCH]** Dispatch Agent B:
  ```bash
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-03 \
    --prompt "Review FR-03 against SRS + SAD" --phase 8 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-3: Gate 1 — FR-03
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-03 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- $(python3 -c "from scripts.generate_full_plan import _fr_source_paths; print(' '.join(_fr_source_paths('FR-03')))" 2>/dev/null || echo '.')
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-03:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 8 --fr-id FR-03 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-03 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-03:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 8 --fr-id FR-03
  ```
  **If FAIL** (any dim below threshold): fix code → repeat G1a→G1b→G1c until PASS.
  **Do NOT proceed to G1d until all dims PASS.**

- [ ] **[SAB-SYNC]** Re-sync SAB.json after adding/moving source files:
  ```bash
  python3 scripts/generate_sab.py --project $REPO
  ```
  _(Keeps M2 SAB drift < 15% — postflight blocks gate finalization if exceeded)_

- [ ] **G1d** ✅ Verify local commit saved (finalize-gate above already committed):
  ```bash
  git log --oneline -1
  ```
  > `finalize-gate --gate 1` calls `commit_fr_gate1()` — **local commit only, no push**.
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p8-mid` / `p8-pre-ssi` / Gate exit.

#### FR-04: Configuration Record
- [ ] Confirm FR-04 configuration items are documented in CONFIG_RECORDS.md
- [ ] Confirm environment variables / secrets are managed (not hardcoded)
- [ ] Confirm deployment checklist entries for FR-04

**A/B Work — FR-04** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVOPS): Document config items → verify env vars/secrets → update CONFIG_RECORDS.md
  - Docstrings: `[FR-04]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-04 \
    --prompt "Document config items → verify env vars/secrets → update CONFIG_RECORDS.md for FR-04" --phase 8 --project $REPO
  ```
- [ ] **[B-1]** Agent B (ARCHITECT) for FR-04 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md`
  - `08-config/CONFIG_RECORDS.md (draft)`
  - `ops/ relevant configs`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-04.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (draft)] ===
  {paste full content here}

  === [DOC 3: ops/ relevant configs] ===
  {paste full content here}

  Review checklist:
  - All config items documented?
  - Secrets correctly externalized?
  - No hardcoded credentials?

  Return JSON only:
  {"status":"STAGE_PASS"|"REJECT","review_status":"APPROVE"|"REJECT",
   "reason":"...","confidence":1-10,"citations":["file:line"],"gaps":[...]}
  ```

- [ ] **[B-2]** Agent B returns JSON — parse `review_status`:
  - `APPROVE` → continue to next step
  - `REJECT` → Agent A fixes gaps → re-dispatch B. Max 5 rounds (HR-12).

- [ ] **[B-DISPATCH]** Dispatch Agent B:
  ```bash
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-04 \
    --prompt "Review FR-04 against SRS + SAD" --phase 8 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-4: Gate 1 — FR-04
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-04 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- $(python3 -c "from scripts.generate_full_plan import _fr_source_paths; print(' '.join(_fr_source_paths('FR-04')))" 2>/dev/null || echo '.')
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-04:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 8 --fr-id FR-04 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-04 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-04:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 8 --fr-id FR-04
  ```
  **If FAIL** (any dim below threshold): fix code → repeat G1a→G1b→G1c until PASS.
  **Do NOT proceed to G1d until all dims PASS.**

- [ ] **[SAB-SYNC]** Re-sync SAB.json after adding/moving source files:
  ```bash
  python3 scripts/generate_sab.py --project $REPO
  ```
  _(Keeps M2 SAB drift < 15% — postflight blocks gate finalization if exceeded)_

- [ ] **G1d** ✅ Verify local commit saved (finalize-gate above already committed):
  ```bash
  git log --oneline -1
  ```
  > `finalize-gate --gate 1` calls `commit_fr_gate1()` — **local commit only, no push**.
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p8-mid` / `p8-pre-ssi` / Gate exit.

#### FR-05: Configuration Record
- [ ] Confirm FR-05 configuration items are documented in CONFIG_RECORDS.md
- [ ] Confirm environment variables / secrets are managed (not hardcoded)
- [ ] Confirm deployment checklist entries for FR-05

**A/B Work — FR-05** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVOPS): Document config items → verify env vars/secrets → update CONFIG_RECORDS.md
  - Docstrings: `[FR-05]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-05 \
    --prompt "Document config items → verify env vars/secrets → update CONFIG_RECORDS.md for FR-05" --phase 8 --project $REPO
  ```
- [ ] **[B-1]** Agent B (ARCHITECT) for FR-05 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md`
  - `08-config/CONFIG_RECORDS.md (draft)`
  - `ops/ relevant configs`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-05.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (draft)] ===
  {paste full content here}

  === [DOC 3: ops/ relevant configs] ===
  {paste full content here}

  Review checklist:
  - All config items documented?
  - Secrets correctly externalized?
  - No hardcoded credentials?

  Return JSON only:
  {"status":"STAGE_PASS"|"REJECT","review_status":"APPROVE"|"REJECT",
   "reason":"...","confidence":1-10,"citations":["file:line"],"gaps":[...]}
  ```

- [ ] **[B-2]** Agent B returns JSON — parse `review_status`:
  - `APPROVE` → continue to next step
  - `REJECT` → Agent A fixes gaps → re-dispatch B. Max 5 rounds (HR-12).

- [ ] **[B-DISPATCH]** Dispatch Agent B:
  ```bash
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-05 \
    --prompt "Review FR-05 against SRS + SAD" --phase 8 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-5: Gate 1 — FR-05
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-05 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- $(python3 -c "from scripts.generate_full_plan import _fr_source_paths; print(' '.join(_fr_source_paths('FR-05')))" 2>/dev/null || echo '.')
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-05:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 8 --fr-id FR-05 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-05 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-05:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 8 --fr-id FR-05
  ```
  **If FAIL** (any dim below threshold): fix code → repeat G1a→G1b→G1c until PASS.
  **Do NOT proceed to G1d until all dims PASS.**

- [ ] **[SAB-SYNC]** Re-sync SAB.json after adding/moving source files:
  ```bash
  python3 scripts/generate_sab.py --project $REPO
  ```
  _(Keeps M2 SAB drift < 15% — postflight blocks gate finalization if exceeded)_

- [ ] **G1d** ✅ Verify local commit saved (finalize-gate above already committed):
  ```bash
  git log --oneline -1
  ```
  > `finalize-gate --gate 1` calls `commit_fr_gate1()` — **local commit only, no push**.
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p8-mid` / `p8-pre-ssi` / Gate exit.

#### FR-06: Configuration Record
- [ ] Confirm FR-06 configuration items are documented in CONFIG_RECORDS.md
- [ ] Confirm environment variables / secrets are managed (not hardcoded)
- [ ] Confirm deployment checklist entries for FR-06

**A/B Work — FR-06** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVOPS): Document config items → verify env vars/secrets → update CONFIG_RECORDS.md
  - Docstrings: `[FR-06]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-06 \
    --prompt "Document config items → verify env vars/secrets → update CONFIG_RECORDS.md for FR-06" --phase 8 --project $REPO
  ```
- [ ] **[B-1]** Agent B (ARCHITECT) for FR-06 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md`
  - `08-config/CONFIG_RECORDS.md (draft)`
  - `ops/ relevant configs`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-06.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (draft)] ===
  {paste full content here}

  === [DOC 3: ops/ relevant configs] ===
  {paste full content here}

  Review checklist:
  - All config items documented?
  - Secrets correctly externalized?
  - No hardcoded credentials?

  Return JSON only:
  {"status":"STAGE_PASS"|"REJECT","review_status":"APPROVE"|"REJECT",
   "reason":"...","confidence":1-10,"citations":["file:line"],"gaps":[...]}
  ```

- [ ] **[B-2]** Agent B returns JSON — parse `review_status`:
  - `APPROVE` → continue to next step
  - `REJECT` → Agent A fixes gaps → re-dispatch B. Max 5 rounds (HR-12).

- [ ] **[B-DISPATCH]** Dispatch Agent B:
  ```bash
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-06 \
    --prompt "Review FR-06 against SRS + SAD" --phase 8 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-6: Gate 1 — FR-06
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-06 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- $(python3 -c "from scripts.generate_full_plan import _fr_source_paths; print(' '.join(_fr_source_paths('FR-06')))" 2>/dev/null || echo '.')
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-06:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 8 --fr-id FR-06 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-06 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-06:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 8 --fr-id FR-06
  ```
  **If FAIL** (any dim below threshold): fix code → repeat G1a→G1b→G1c until PASS.
  **Do NOT proceed to G1d until all dims PASS.**

- [ ] **[SAB-SYNC]** Re-sync SAB.json after adding/moving source files:
  ```bash
  python3 scripts/generate_sab.py --project $REPO
  ```
  _(Keeps M2 SAB drift < 15% — postflight blocks gate finalization if exceeded)_

- [ ] **G1d** ✅ Verify local commit saved (finalize-gate above already committed):
  ```bash
  git log --oneline -1
  ```
  > `finalize-gate --gate 1` calls `commit_fr_gate1()` — **local commit only, no push**.
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p8-mid` / `p8-pre-ssi` / Gate exit.

#### FR-07: Configuration Record
- [ ] Confirm FR-07 configuration items are documented in CONFIG_RECORDS.md
- [ ] Confirm environment variables / secrets are managed (not hardcoded)
- [ ] Confirm deployment checklist entries for FR-07

**A/B Work — FR-07** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVOPS): Document config items → verify env vars/secrets → update CONFIG_RECORDS.md
  - Docstrings: `[FR-07]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-07 \
    --prompt "Document config items → verify env vars/secrets → update CONFIG_RECORDS.md for FR-07" --phase 8 --project $REPO
  ```
- [ ] **[B-1]** Agent B (ARCHITECT) for FR-07 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md`
  - `08-config/CONFIG_RECORDS.md (draft)`
  - `ops/ relevant configs`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-07.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (draft)] ===
  {paste full content here}

  === [DOC 3: ops/ relevant configs] ===
  {paste full content here}

  Review checklist:
  - All config items documented?
  - Secrets correctly externalized?
  - No hardcoded credentials?

  Return JSON only:
  {"status":"STAGE_PASS"|"REJECT","review_status":"APPROVE"|"REJECT",
   "reason":"...","confidence":1-10,"citations":["file:line"],"gaps":[...]}
  ```

- [ ] **[B-2]** Agent B returns JSON — parse `review_status`:
  - `APPROVE` → continue to next step
  - `REJECT` → Agent A fixes gaps → re-dispatch B. Max 5 rounds (HR-12).

- [ ] **[B-DISPATCH]** Dispatch Agent B:
  ```bash
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-07 \
    --prompt "Review FR-07 against SRS + SAD" --phase 8 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-7: Gate 1 — FR-07
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-07 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- $(python3 -c "from scripts.generate_full_plan import _fr_source_paths; print(' '.join(_fr_source_paths('FR-07')))" 2>/dev/null || echo '.')
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-07:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 8 --fr-id FR-07 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-07 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-07:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 8 --fr-id FR-07
  ```
  **If FAIL** (any dim below threshold): fix code → repeat G1a→G1b→G1c until PASS.
  **Do NOT proceed to G1d until all dims PASS.**

- [ ] **[SAB-SYNC]** Re-sync SAB.json after adding/moving source files:
  ```bash
  python3 scripts/generate_sab.py --project $REPO
  ```
  _(Keeps M2 SAB drift < 15% — postflight blocks gate finalization if exceeded)_

- [ ] **G1d** ✅ Verify local commit saved (finalize-gate above already committed):
  ```bash
  git log --oneline -1
  ```
  > `finalize-gate --gate 1` calls `commit_fr_gate1()` — **local commit only, no push**.
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p8-mid` / `p8-pre-ssi` / Gate exit.

#### FR-08: Configuration Record
- [ ] Confirm FR-08 configuration items are documented in CONFIG_RECORDS.md
- [ ] Confirm environment variables / secrets are managed (not hardcoded)
- [ ] Confirm deployment checklist entries for FR-08

**A/B Work — FR-08** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVOPS): Document config items → verify env vars/secrets → update CONFIG_RECORDS.md
  - Docstrings: `[FR-08]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-08 \
    --prompt "Document config items → verify env vars/secrets → update CONFIG_RECORDS.md for FR-08" --phase 8 --project $REPO
  ```
- [ ] **[B-1]** Agent B (ARCHITECT) for FR-08 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md`
  - `08-config/CONFIG_RECORDS.md (draft)`
  - `ops/ relevant configs`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-08.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (draft)] ===
  {paste full content here}

  === [DOC 3: ops/ relevant configs] ===
  {paste full content here}

  Review checklist:
  - All config items documented?
  - Secrets correctly externalized?
  - No hardcoded credentials?

  Return JSON only:
  {"status":"STAGE_PASS"|"REJECT","review_status":"APPROVE"|"REJECT",
   "reason":"...","confidence":1-10,"citations":["file:line"],"gaps":[...]}
  ```

- [ ] **[B-2]** Agent B returns JSON — parse `review_status`:
  - `APPROVE` → continue to next step
  - `REJECT` → Agent A fixes gaps → re-dispatch B. Max 5 rounds (HR-12).

- [ ] **[B-DISPATCH]** Dispatch Agent B:
  ```bash
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-08 \
    --prompt "Review FR-08 against SRS + SAD" --phase 8 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-8: Gate 1 — FR-08
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-08 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- $(python3 -c "from scripts.generate_full_plan import _fr_source_paths; print(' '.join(_fr_source_paths('FR-08')))" 2>/dev/null || echo '.')
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-08:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 8 --fr-id FR-08 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-08 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-08:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 8 --fr-id FR-08
  ```
  **If FAIL** (any dim below threshold): fix code → repeat G1a→G1b→G1c until PASS.
  **Do NOT proceed to G1d until all dims PASS.**

- [ ] **[SAB-SYNC]** Re-sync SAB.json after adding/moving source files:
  ```bash
  python3 scripts/generate_sab.py --project $REPO
  ```
  _(Keeps M2 SAB drift < 15% — postflight blocks gate finalization if exceeded)_

- [ ] **G1d** ✅ Verify local commit saved (finalize-gate above already committed):
  ```bash
  git log --oneline -1
  ```
  > `finalize-gate --gate 1` calls `commit_fr_gate1()` — **local commit only, no push**.
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p8-mid` / `p8-pre-ssi` / Gate exit.

#### FR-09: Configuration Record
- [ ] Confirm FR-09 configuration items are documented in CONFIG_RECORDS.md
- [ ] Confirm environment variables / secrets are managed (not hardcoded)
- [ ] Confirm deployment checklist entries for FR-09

**A/B Work — FR-09** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVOPS): Document config items → verify env vars/secrets → update CONFIG_RECORDS.md
  - Docstrings: `[FR-09]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-09 \
    --prompt "Document config items → verify env vars/secrets → update CONFIG_RECORDS.md for FR-09" --phase 8 --project $REPO
  ```
- [ ] **[B-1]** Agent B (ARCHITECT) for FR-09 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md`
  - `08-config/CONFIG_RECORDS.md (draft)`
  - `ops/ relevant configs`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-09.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (draft)] ===
  {paste full content here}

  === [DOC 3: ops/ relevant configs] ===
  {paste full content here}

  Review checklist:
  - All config items documented?
  - Secrets correctly externalized?
  - No hardcoded credentials?

  Return JSON only:
  {"status":"STAGE_PASS"|"REJECT","review_status":"APPROVE"|"REJECT",
   "reason":"...","confidence":1-10,"citations":["file:line"],"gaps":[...]}
  ```

- [ ] **[B-2]** Agent B returns JSON — parse `review_status`:
  - `APPROVE` → continue to next step
  - `REJECT` → Agent A fixes gaps → re-dispatch B. Max 5 rounds (HR-12).

- [ ] **[B-DISPATCH]** Dispatch Agent B:
  ```bash
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-09 \
    --prompt "Review FR-09 against SRS + SAD" --phase 8 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-9: Gate 1 — FR-09
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-09 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- $(python3 -c "from scripts.generate_full_plan import _fr_source_paths; print(' '.join(_fr_source_paths('FR-09')))" 2>/dev/null || echo '.')
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-09:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 8 --fr-id FR-09 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-09 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-09:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 8 --fr-id FR-09
  ```
  **If FAIL** (any dim below threshold): fix code → repeat G1a→G1b→G1c until PASS.
  **Do NOT proceed to G1d until all dims PASS.**

- [ ] **[SAB-SYNC]** Re-sync SAB.json after adding/moving source files:
  ```bash
  python3 scripts/generate_sab.py --project $REPO
  ```
  _(Keeps M2 SAB drift < 15% — postflight blocks gate finalization if exceeded)_

- [ ] **G1d** ✅ Verify local commit saved (finalize-gate above already committed):
  ```bash
  git log --oneline -1
  ```
  > `finalize-gate --gate 1` calls `commit_fr_gate1()` — **local commit only, no push**.
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p8-mid` / `p8-pre-ssi` / Gate exit.

#### FR-10: Configuration Record
- [ ] Confirm FR-10 configuration items are documented in CONFIG_RECORDS.md
- [ ] Confirm environment variables / secrets are managed (not hardcoded)
- [ ] Confirm deployment checklist entries for FR-10

**A/B Work — FR-10** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVOPS): Document config items → verify env vars/secrets → update CONFIG_RECORDS.md
  - Docstrings: `[FR-10]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-10 \
    --prompt "Document config items → verify env vars/secrets → update CONFIG_RECORDS.md for FR-10" --phase 8 --project $REPO
  ```
- [ ] **[B-1]** Agent B (ARCHITECT) for FR-10 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md`
  - `08-config/CONFIG_RECORDS.md (draft)`
  - `ops/ relevant configs`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-10.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (draft)] ===
  {paste full content here}

  === [DOC 3: ops/ relevant configs] ===
  {paste full content here}

  Review checklist:
  - All config items documented?
  - Secrets correctly externalized?
  - No hardcoded credentials?

  Return JSON only:
  {"status":"STAGE_PASS"|"REJECT","review_status":"APPROVE"|"REJECT",
   "reason":"...","confidence":1-10,"citations":["file:line"],"gaps":[...]}
  ```

- [ ] **[B-2]** Agent B returns JSON — parse `review_status`:
  - `APPROVE` → continue to next step
  - `REJECT` → Agent A fixes gaps → re-dispatch B. Max 5 rounds (HR-12).

- [ ] **[B-DISPATCH]** Dispatch Agent B:
  ```bash
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-10 \
    --prompt "Review FR-10 against SRS + SAD" --phase 8 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-10: Gate 1 — FR-10
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-10 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- $(python3 -c "from scripts.generate_full_plan import _fr_source_paths; print(' '.join(_fr_source_paths('FR-10')))" 2>/dev/null || echo '.')
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-10:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 8 --fr-id FR-10 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-10 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-10:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 8 --fr-id FR-10
  ```
  **If FAIL** (any dim below threshold): fix code → repeat G1a→G1b→G1c until PASS.
  **Do NOT proceed to G1d until all dims PASS.**

- [ ] **[SAB-SYNC]** Re-sync SAB.json after adding/moving source files:
  ```bash
  python3 scripts/generate_sab.py --project $REPO
  ```
  _(Keeps M2 SAB drift < 15% — postflight blocks gate finalization if exceeded)_

- [ ] **G1d** ✅ Verify local commit saved (finalize-gate above already committed):
  ```bash
  git log --oneline -1
  ```
  > `finalize-gate --gate 1` calls `commit_fr_gate1()` — **local commit only, no push**.
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p8-mid` / `p8-pre-ssi` / Gate exit.

#### FR-11: Configuration Record
- [ ] Confirm FR-11 configuration items are documented in CONFIG_RECORDS.md
- [ ] Confirm environment variables / secrets are managed (not hardcoded)
- [ ] Confirm deployment checklist entries for FR-11

**A/B Work — FR-11** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVOPS): Document config items → verify env vars/secrets → update CONFIG_RECORDS.md
  - Docstrings: `[FR-11]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-11 \
    --prompt "Document config items → verify env vars/secrets → update CONFIG_RECORDS.md for FR-11" --phase 8 --project $REPO
  ```
- [ ] **[B-1]** Agent B (ARCHITECT) for FR-11 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md`
  - `08-config/CONFIG_RECORDS.md (draft)`
  - `ops/ relevant configs`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-11.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (draft)] ===
  {paste full content here}

  === [DOC 3: ops/ relevant configs] ===
  {paste full content here}

  Review checklist:
  - All config items documented?
  - Secrets correctly externalized?
  - No hardcoded credentials?

  Return JSON only:
  {"status":"STAGE_PASS"|"REJECT","review_status":"APPROVE"|"REJECT",
   "reason":"...","confidence":1-10,"citations":["file:line"],"gaps":[...]}
  ```

- [ ] **[B-2]** Agent B returns JSON — parse `review_status`:
  - `APPROVE` → continue to next step
  - `REJECT` → Agent A fixes gaps → re-dispatch B. Max 5 rounds (HR-12).

- [ ] **[B-DISPATCH]** Dispatch Agent B:
  ```bash
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-11 \
    --prompt "Review FR-11 against SRS + SAD" --phase 8 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-11: Gate 1 — FR-11
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-11 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- $(python3 -c "from scripts.generate_full_plan import _fr_source_paths; print(' '.join(_fr_source_paths('FR-11')))" 2>/dev/null || echo '.')
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-11:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 8 --fr-id FR-11 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-11 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-11:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 8 --fr-id FR-11
  ```
  **If FAIL** (any dim below threshold): fix code → repeat G1a→G1b→G1c until PASS.
  **Do NOT proceed to G1d until all dims PASS.**

- [ ] **[SAB-SYNC]** Re-sync SAB.json after adding/moving source files:
  ```bash
  python3 scripts/generate_sab.py --project $REPO
  ```
  _(Keeps M2 SAB drift < 15% — postflight blocks gate finalization if exceeded)_

- [ ] **G1d** ✅ Verify local commit saved (finalize-gate above already committed):
  ```bash
  git log --oneline -1
  ```
  > `finalize-gate --gate 1` calls `commit_fr_gate1()` — **local commit only, no push**.
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p8-mid` / `p8-pre-ssi` / Gate exit.

#### FR-12: Configuration Record
- [ ] Confirm FR-12 configuration items are documented in CONFIG_RECORDS.md
- [ ] Confirm environment variables / secrets are managed (not hardcoded)
- [ ] Confirm deployment checklist entries for FR-12

**A/B Work — FR-12** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVOPS): Document config items → verify env vars/secrets → update CONFIG_RECORDS.md
  - Docstrings: `[FR-12]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-12 \
    --prompt "Document config items → verify env vars/secrets → update CONFIG_RECORDS.md for FR-12" --phase 8 --project $REPO
  ```
- [ ] **[B-1]** Agent B (ARCHITECT) for FR-12 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md`
  - `08-config/CONFIG_RECORDS.md (draft)`
  - `ops/ relevant configs`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-12.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (draft)] ===
  {paste full content here}

  === [DOC 3: ops/ relevant configs] ===
  {paste full content here}

  Review checklist:
  - All config items documented?
  - Secrets correctly externalized?
  - No hardcoded credentials?

  Return JSON only:
  {"status":"STAGE_PASS"|"REJECT","review_status":"APPROVE"|"REJECT",
   "reason":"...","confidence":1-10,"citations":["file:line"],"gaps":[...]}
  ```

- [ ] **[B-2]** Agent B returns JSON — parse `review_status`:
  - `APPROVE` → continue to next step
  - `REJECT` → Agent A fixes gaps → re-dispatch B. Max 5 rounds (HR-12).

- [ ] **[B-DISPATCH]** Dispatch Agent B:
  ```bash
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-12 \
    --prompt "Review FR-12 against SRS + SAD" --phase 8 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-12: Gate 1 — FR-12
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-12 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- $(python3 -c "from scripts.generate_full_plan import _fr_source_paths; print(' '.join(_fr_source_paths('FR-12')))" 2>/dev/null || echo '.')
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-12:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 8 --fr-id FR-12 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-12 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-12:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 8 --fr-id FR-12
  ```
  **If FAIL** (any dim below threshold): fix code → repeat G1a→G1b→G1c until PASS.
  **Do NOT proceed to G1d until all dims PASS.**

- [ ] **[SAB-SYNC]** Re-sync SAB.json after adding/moving source files:
  ```bash
  python3 scripts/generate_sab.py --project $REPO
  ```
  _(Keeps M2 SAB drift < 15% — postflight blocks gate finalization if exceeded)_

- [ ] **G1d** ✅ Verify local commit saved (finalize-gate above already committed):
  ```bash
  git log --oneline -1
  ```
  > `finalize-gate --gate 1` calls `commit_fr_gate1()` — **local commit only, no push**.
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p8-mid` / `p8-pre-ssi` / Gate exit.

#### FR-13: Configuration Record
- [ ] Confirm FR-13 configuration items are documented in CONFIG_RECORDS.md
- [ ] Confirm environment variables / secrets are managed (not hardcoded)
- [ ] Confirm deployment checklist entries for FR-13

**A/B Work — FR-13** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVOPS): Document config items → verify env vars/secrets → update CONFIG_RECORDS.md
  - Docstrings: `[FR-13]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-13 \
    --prompt "Document config items → verify env vars/secrets → update CONFIG_RECORDS.md for FR-13" --phase 8 --project $REPO
  ```
- [ ] **[B-1]** Agent B (ARCHITECT) for FR-13 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md`
  - `08-config/CONFIG_RECORDS.md (draft)`
  - `ops/ relevant configs`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-13.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (draft)] ===
  {paste full content here}

  === [DOC 3: ops/ relevant configs] ===
  {paste full content here}

  Review checklist:
  - All config items documented?
  - Secrets correctly externalized?
  - No hardcoded credentials?

  Return JSON only:
  {"status":"STAGE_PASS"|"REJECT","review_status":"APPROVE"|"REJECT",
   "reason":"...","confidence":1-10,"citations":["file:line"],"gaps":[...]}
  ```

- [ ] **[B-2]** Agent B returns JSON — parse `review_status`:
  - `APPROVE` → continue to next step
  - `REJECT` → Agent A fixes gaps → re-dispatch B. Max 5 rounds (HR-12).

- [ ] **[B-DISPATCH]** Dispatch Agent B:
  ```bash
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-13 \
    --prompt "Review FR-13 against SRS + SAD" --phase 8 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-13: Gate 1 — FR-13
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-13 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- $(python3 -c "from scripts.generate_full_plan import _fr_source_paths; print(' '.join(_fr_source_paths('FR-13')))" 2>/dev/null || echo '.')
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-13:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 8 --fr-id FR-13 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-13 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-13:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 8 --fr-id FR-13
  ```
  **If FAIL** (any dim below threshold): fix code → repeat G1a→G1b→G1c until PASS.
  **Do NOT proceed to G1d until all dims PASS.**

- [ ] **[SAB-SYNC]** Re-sync SAB.json after adding/moving source files:
  ```bash
  python3 scripts/generate_sab.py --project $REPO
  ```
  _(Keeps M2 SAB drift < 15% — postflight blocks gate finalization if exceeded)_

- [ ] **G1d** ✅ Verify local commit saved (finalize-gate above already committed):
  ```bash
  git log --oneline -1
  ```
  > `finalize-gate --gate 1` calls `commit_fr_gate1()` — **local commit only, no push**.
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p8-mid` / `p8-pre-ssi` / Gate exit.

### P8 Milestone Push (10-Push Strategy ⑩)

- [ ] **PUSH ⑩ — P8 exit** (after config records are complete):
  ```bash
  python3 harness_cli.py push-milestone --type p8 --project .
  ```
  > Writes HANDOVER.md + commits + pushes. Pipeline complete.

### Phase 8 Deliverables
- [ ] `CONFIG_RECORDS.md` - Configuration records
- [ ] `RELEASE_CHECKLIST.md` - Release checklist
- [x] `sessions_spawn.log` — auto-populated by AgentSpawner (HR-10)
- [ ] Gate 1 PASS for every FR

#### ASPICE Traceability Requirements (enforced by postflight)

- [ ] **[ASPICE]** Artifact for Phase 8 MUST reference `07-risk/RISK_ASSESSMENT.md` by filename keyword `RISK_ASSESSMENT` (ASPICE traceability — `postflight_artifact_links()` enforces this)
- [ ] **[ASPICE]** Artifact for Phase 8 MUST reference `07-risk/RISK_REGISTER.md` by filename keyword `RISK_REGISTER` (ASPICE traceability — `postflight_artifact_links()` enforces this)


### 🎉 Pipeline Complete

- [ ] All 8 phases complete. Archive `.methodology/` for the audit trail.
