# Phase 8 Full Execution Plan -- omnibot-full

> **Version**: v2.3.0 (project plan)
> **Project**: omnibot-full
> **Date**: 2026-05-19
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
> - CHECKPOINT-14: Gate 1 / FR-14 *(local commit)*
> - CHECKPOINT-15: Gate 1 / FR-15 *(local commit)*
> - CHECKPOINT-16: Gate 1 / FR-16 *(local commit)*
> - CHECKPOINT-17: Gate 1 / FR-17 *(local commit)*
> - CHECKPOINT-18: Gate 1 / FR-18 *(local commit)*
> - CHECKPOINT-19: Gate 1 / FR-19 *(local commit)*
> - CHECKPOINT-20: Gate 1 / FR-20 *(local commit)*
> - CHECKPOINT-21: Gate 1 / FR-21 *(local commit)*
> - CHECKPOINT-22: Gate 1 / FR-22 *(local commit)*
> - CHECKPOINT-23: Gate 1 / FR-23 *(local commit)*
> - CHECKPOINT-24: Gate 1 / FR-24 *(local commit)*
> - MILESTONE: P8 exit push (config records complete) → **HANDOVER.md**

### Entry Gate Verification

- [ ] **[ENTRY-CHECK]** Gate 4 PASS (P6 exit — P7 has no exit gate, P7 completed stands between):
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
  4. Phase 8 confirmed in `.methodology/state.json` (`advance-phase` already run)
  > If stale: run `python3 harness_cli.py init-project --phase 8 --project $REPO --overwrite`

### Configuration Items (2 total)

- **Date: 2026-05-17

## Repository Configuration**: Document value/source/access method → update CONFIG_RECORDS.md
- **## Environment Variables Required**: Document value/source/access method → update CONFIG_RECORDS.md

### FR Configuration Evaluation (24 total)

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
  - `01-requirements/SRS.md §FR-XX section`
  - `08-config/CONFIG_RECORDS.md (FR-XX draft entry)`
  - `03-development/src/.../fr_xx.py`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following configuration record for FR-01.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (FR-XX draft entry)] ===
  {paste full content here}

  === [DOC 3: 03-development/src/.../fr_xx.py] ===
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
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-1: Gate 1 — FR-01
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-01 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- "03-development/src/**/*fr_01*" "03-development/src/**/*fr-01*" "tests/**/test_fr_01*" "tests/**/test_fr-01*" 2>/dev/null || echo '.'
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
  - `01-requirements/SRS.md §FR-XX section`
  - `08-config/CONFIG_RECORDS.md (FR-XX draft entry)`
  - `03-development/src/.../fr_xx.py`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following configuration record for FR-02.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (FR-XX draft entry)] ===
  {paste full content here}

  === [DOC 3: 03-development/src/.../fr_xx.py] ===
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
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-2: Gate 1 — FR-02
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-02 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- "03-development/src/**/*fr_02*" "03-development/src/**/*fr-02*" "tests/**/test_fr_02*" "tests/**/test_fr-02*" 2>/dev/null || echo '.'
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
  - `01-requirements/SRS.md §FR-XX section`
  - `08-config/CONFIG_RECORDS.md (FR-XX draft entry)`
  - `03-development/src/.../fr_xx.py`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following configuration record for FR-03.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (FR-XX draft entry)] ===
  {paste full content here}

  === [DOC 3: 03-development/src/.../fr_xx.py] ===
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
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-3: Gate 1 — FR-03
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-03 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- "03-development/src/**/*fr_03*" "03-development/src/**/*fr-03*" "tests/**/test_fr_03*" "tests/**/test_fr-03*" 2>/dev/null || echo '.'
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
  - `01-requirements/SRS.md §FR-XX section`
  - `08-config/CONFIG_RECORDS.md (FR-XX draft entry)`
  - `03-development/src/.../fr_xx.py`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following configuration record for FR-04.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (FR-XX draft entry)] ===
  {paste full content here}

  === [DOC 3: 03-development/src/.../fr_xx.py] ===
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
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-4: Gate 1 — FR-04
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-04 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- "03-development/src/**/*fr_04*" "03-development/src/**/*fr-04*" "tests/**/test_fr_04*" "tests/**/test_fr-04*" 2>/dev/null || echo '.'
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
  - `01-requirements/SRS.md §FR-XX section`
  - `08-config/CONFIG_RECORDS.md (FR-XX draft entry)`
  - `03-development/src/.../fr_xx.py`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following configuration record for FR-05.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (FR-XX draft entry)] ===
  {paste full content here}

  === [DOC 3: 03-development/src/.../fr_xx.py] ===
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
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-5: Gate 1 — FR-05
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-05 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- "03-development/src/**/*fr_05*" "03-development/src/**/*fr-05*" "tests/**/test_fr_05*" "tests/**/test_fr-05*" 2>/dev/null || echo '.'
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
  - `01-requirements/SRS.md §FR-XX section`
  - `08-config/CONFIG_RECORDS.md (FR-XX draft entry)`
  - `03-development/src/.../fr_xx.py`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following configuration record for FR-06.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (FR-XX draft entry)] ===
  {paste full content here}

  === [DOC 3: 03-development/src/.../fr_xx.py] ===
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
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-6: Gate 1 — FR-06
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-06 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- "03-development/src/**/*fr_06*" "03-development/src/**/*fr-06*" "tests/**/test_fr_06*" "tests/**/test_fr-06*" 2>/dev/null || echo '.'
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
  - `01-requirements/SRS.md §FR-XX section`
  - `08-config/CONFIG_RECORDS.md (FR-XX draft entry)`
  - `03-development/src/.../fr_xx.py`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following configuration record for FR-07.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (FR-XX draft entry)] ===
  {paste full content here}

  === [DOC 3: 03-development/src/.../fr_xx.py] ===
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
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-7: Gate 1 — FR-07
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-07 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- "03-development/src/**/*fr_07*" "03-development/src/**/*fr-07*" "tests/**/test_fr_07*" "tests/**/test_fr-07*" 2>/dev/null || echo '.'
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
  - `01-requirements/SRS.md §FR-XX section`
  - `08-config/CONFIG_RECORDS.md (FR-XX draft entry)`
  - `03-development/src/.../fr_xx.py`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following configuration record for FR-08.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (FR-XX draft entry)] ===
  {paste full content here}

  === [DOC 3: 03-development/src/.../fr_xx.py] ===
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
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-8: Gate 1 — FR-08
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-08 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- "03-development/src/**/*fr_08*" "03-development/src/**/*fr-08*" "tests/**/test_fr_08*" "tests/**/test_fr-08*" 2>/dev/null || echo '.'
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
  - `01-requirements/SRS.md §FR-XX section`
  - `08-config/CONFIG_RECORDS.md (FR-XX draft entry)`
  - `03-development/src/.../fr_xx.py`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following configuration record for FR-09.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (FR-XX draft entry)] ===
  {paste full content here}

  === [DOC 3: 03-development/src/.../fr_xx.py] ===
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
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-9: Gate 1 — FR-09
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-09 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- "03-development/src/**/*fr_09*" "03-development/src/**/*fr-09*" "tests/**/test_fr_09*" "tests/**/test_fr-09*" 2>/dev/null || echo '.'
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
  - `01-requirements/SRS.md §FR-XX section`
  - `08-config/CONFIG_RECORDS.md (FR-XX draft entry)`
  - `03-development/src/.../fr_xx.py`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following configuration record for FR-10.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (FR-XX draft entry)] ===
  {paste full content here}

  === [DOC 3: 03-development/src/.../fr_xx.py] ===
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
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-10: Gate 1 — FR-10
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-10 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- "03-development/src/**/*fr_10*" "03-development/src/**/*fr-10*" "tests/**/test_fr_10*" "tests/**/test_fr-10*" 2>/dev/null || echo '.'
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
  - `01-requirements/SRS.md §FR-XX section`
  - `08-config/CONFIG_RECORDS.md (FR-XX draft entry)`
  - `03-development/src/.../fr_xx.py`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following configuration record for FR-11.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (FR-XX draft entry)] ===
  {paste full content here}

  === [DOC 3: 03-development/src/.../fr_xx.py] ===
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
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-11: Gate 1 — FR-11
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-11 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- "03-development/src/**/*fr_11*" "03-development/src/**/*fr-11*" "tests/**/test_fr_11*" "tests/**/test_fr-11*" 2>/dev/null || echo '.'
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
  - `01-requirements/SRS.md §FR-XX section`
  - `08-config/CONFIG_RECORDS.md (FR-XX draft entry)`
  - `03-development/src/.../fr_xx.py`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following configuration record for FR-12.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (FR-XX draft entry)] ===
  {paste full content here}

  === [DOC 3: 03-development/src/.../fr_xx.py] ===
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
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-12: Gate 1 — FR-12
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-12 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- "03-development/src/**/*fr_12*" "03-development/src/**/*fr-12*" "tests/**/test_fr_12*" "tests/**/test_fr-12*" 2>/dev/null || echo '.'
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
  - `01-requirements/SRS.md §FR-XX section`
  - `08-config/CONFIG_RECORDS.md (FR-XX draft entry)`
  - `03-development/src/.../fr_xx.py`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following configuration record for FR-13.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (FR-XX draft entry)] ===
  {paste full content here}

  === [DOC 3: 03-development/src/.../fr_xx.py] ===
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
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-13: Gate 1 — FR-13
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-13 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- "03-development/src/**/*fr_13*" "03-development/src/**/*fr-13*" "tests/**/test_fr_13*" "tests/**/test_fr-13*" 2>/dev/null || echo '.'
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

#### FR-14: Configuration Record
- [ ] Confirm FR-14 configuration items are documented in CONFIG_RECORDS.md
- [ ] Confirm environment variables / secrets are managed (not hardcoded)
- [ ] Confirm deployment checklist entries for FR-14

**A/B Work — FR-14** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVOPS): Document config items → verify env vars/secrets → update CONFIG_RECORDS.md
  - Docstrings: `[FR-14]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-14 \
    --prompt "Document config items → verify env vars/secrets → update CONFIG_RECORDS.md for FR-14" --phase 8 --project $REPO
  ```
- [ ] **[B-1]** Agent B (ARCHITECT) for FR-14 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md §FR-XX section`
  - `08-config/CONFIG_RECORDS.md (FR-XX draft entry)`
  - `03-development/src/.../fr_xx.py`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following configuration record for FR-14.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (FR-XX draft entry)] ===
  {paste full content here}

  === [DOC 3: 03-development/src/.../fr_xx.py] ===
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
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-14 \
    --prompt "Review FR-14 against SRS + SAD" --phase 8 --project $REPO
  ```
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-14: Gate 1 — FR-14
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-14 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- "03-development/src/**/*fr_14*" "03-development/src/**/*fr-14*" "tests/**/test_fr_14*" "tests/**/test_fr-14*" 2>/dev/null || echo '.'
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-14:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 8 --fr-id FR-14 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-14 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-14:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 8 --fr-id FR-14
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

#### FR-15: Configuration Record
- [ ] Confirm FR-15 configuration items are documented in CONFIG_RECORDS.md
- [ ] Confirm environment variables / secrets are managed (not hardcoded)
- [ ] Confirm deployment checklist entries for FR-15

**A/B Work — FR-15** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVOPS): Document config items → verify env vars/secrets → update CONFIG_RECORDS.md
  - Docstrings: `[FR-15]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-15 \
    --prompt "Document config items → verify env vars/secrets → update CONFIG_RECORDS.md for FR-15" --phase 8 --project $REPO
  ```
- [ ] **[B-1]** Agent B (ARCHITECT) for FR-15 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md §FR-XX section`
  - `08-config/CONFIG_RECORDS.md (FR-XX draft entry)`
  - `03-development/src/.../fr_xx.py`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following configuration record for FR-15.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (FR-XX draft entry)] ===
  {paste full content here}

  === [DOC 3: 03-development/src/.../fr_xx.py] ===
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
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-15 \
    --prompt "Review FR-15 against SRS + SAD" --phase 8 --project $REPO
  ```
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-15: Gate 1 — FR-15
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-15 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- "03-development/src/**/*fr_15*" "03-development/src/**/*fr-15*" "tests/**/test_fr_15*" "tests/**/test_fr-15*" 2>/dev/null || echo '.'
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-15:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 8 --fr-id FR-15 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-15 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-15:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 8 --fr-id FR-15
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

#### FR-16: Configuration Record
- [ ] Confirm FR-16 configuration items are documented in CONFIG_RECORDS.md
- [ ] Confirm environment variables / secrets are managed (not hardcoded)
- [ ] Confirm deployment checklist entries for FR-16

**A/B Work — FR-16** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVOPS): Document config items → verify env vars/secrets → update CONFIG_RECORDS.md
  - Docstrings: `[FR-16]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-16 \
    --prompt "Document config items → verify env vars/secrets → update CONFIG_RECORDS.md for FR-16" --phase 8 --project $REPO
  ```
- [ ] **[B-1]** Agent B (ARCHITECT) for FR-16 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md §FR-XX section`
  - `08-config/CONFIG_RECORDS.md (FR-XX draft entry)`
  - `03-development/src/.../fr_xx.py`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following configuration record for FR-16.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (FR-XX draft entry)] ===
  {paste full content here}

  === [DOC 3: 03-development/src/.../fr_xx.py] ===
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
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-16 \
    --prompt "Review FR-16 against SRS + SAD" --phase 8 --project $REPO
  ```
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-16: Gate 1 — FR-16
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-16 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- "03-development/src/**/*fr_16*" "03-development/src/**/*fr-16*" "tests/**/test_fr_16*" "tests/**/test_fr-16*" 2>/dev/null || echo '.'
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-16:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 8 --fr-id FR-16 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-16 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-16:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 8 --fr-id FR-16
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

#### FR-17: Configuration Record
- [ ] Confirm FR-17 configuration items are documented in CONFIG_RECORDS.md
- [ ] Confirm environment variables / secrets are managed (not hardcoded)
- [ ] Confirm deployment checklist entries for FR-17

**A/B Work — FR-17** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVOPS): Document config items → verify env vars/secrets → update CONFIG_RECORDS.md
  - Docstrings: `[FR-17]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-17 \
    --prompt "Document config items → verify env vars/secrets → update CONFIG_RECORDS.md for FR-17" --phase 8 --project $REPO
  ```
- [ ] **[B-1]** Agent B (ARCHITECT) for FR-17 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md §FR-XX section`
  - `08-config/CONFIG_RECORDS.md (FR-XX draft entry)`
  - `03-development/src/.../fr_xx.py`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following configuration record for FR-17.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (FR-XX draft entry)] ===
  {paste full content here}

  === [DOC 3: 03-development/src/.../fr_xx.py] ===
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
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-17 \
    --prompt "Review FR-17 against SRS + SAD" --phase 8 --project $REPO
  ```
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-17: Gate 1 — FR-17
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-17 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- "03-development/src/**/*fr_17*" "03-development/src/**/*fr-17*" "tests/**/test_fr_17*" "tests/**/test_fr-17*" 2>/dev/null || echo '.'
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-17:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 8 --fr-id FR-17 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-17 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-17:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 8 --fr-id FR-17
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

#### FR-18: Configuration Record
- [ ] Confirm FR-18 configuration items are documented in CONFIG_RECORDS.md
- [ ] Confirm environment variables / secrets are managed (not hardcoded)
- [ ] Confirm deployment checklist entries for FR-18

**A/B Work — FR-18** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVOPS): Document config items → verify env vars/secrets → update CONFIG_RECORDS.md
  - Docstrings: `[FR-18]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-18 \
    --prompt "Document config items → verify env vars/secrets → update CONFIG_RECORDS.md for FR-18" --phase 8 --project $REPO
  ```
- [ ] **[B-1]** Agent B (ARCHITECT) for FR-18 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md §FR-XX section`
  - `08-config/CONFIG_RECORDS.md (FR-XX draft entry)`
  - `03-development/src/.../fr_xx.py`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following configuration record for FR-18.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (FR-XX draft entry)] ===
  {paste full content here}

  === [DOC 3: 03-development/src/.../fr_xx.py] ===
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
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-18 \
    --prompt "Review FR-18 against SRS + SAD" --phase 8 --project $REPO
  ```
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-18: Gate 1 — FR-18
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-18 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- "03-development/src/**/*fr_18*" "03-development/src/**/*fr-18*" "tests/**/test_fr_18*" "tests/**/test_fr-18*" 2>/dev/null || echo '.'
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-18:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 8 --fr-id FR-18 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-18 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-18:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 8 --fr-id FR-18
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

#### FR-19: Configuration Record
- [ ] Confirm FR-19 configuration items are documented in CONFIG_RECORDS.md
- [ ] Confirm environment variables / secrets are managed (not hardcoded)
- [ ] Confirm deployment checklist entries for FR-19

**A/B Work — FR-19** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVOPS): Document config items → verify env vars/secrets → update CONFIG_RECORDS.md
  - Docstrings: `[FR-19]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-19 \
    --prompt "Document config items → verify env vars/secrets → update CONFIG_RECORDS.md for FR-19" --phase 8 --project $REPO
  ```
- [ ] **[B-1]** Agent B (ARCHITECT) for FR-19 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md §FR-XX section`
  - `08-config/CONFIG_RECORDS.md (FR-XX draft entry)`
  - `03-development/src/.../fr_xx.py`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following configuration record for FR-19.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (FR-XX draft entry)] ===
  {paste full content here}

  === [DOC 3: 03-development/src/.../fr_xx.py] ===
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
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-19 \
    --prompt "Review FR-19 against SRS + SAD" --phase 8 --project $REPO
  ```
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-19: Gate 1 — FR-19
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-19 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- "03-development/src/**/*fr_19*" "03-development/src/**/*fr-19*" "tests/**/test_fr_19*" "tests/**/test_fr-19*" 2>/dev/null || echo '.'
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-19:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 8 --fr-id FR-19 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-19 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-19:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 8 --fr-id FR-19
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

#### FR-20: Configuration Record
- [ ] Confirm FR-20 configuration items are documented in CONFIG_RECORDS.md
- [ ] Confirm environment variables / secrets are managed (not hardcoded)
- [ ] Confirm deployment checklist entries for FR-20

**A/B Work — FR-20** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVOPS): Document config items → verify env vars/secrets → update CONFIG_RECORDS.md
  - Docstrings: `[FR-20]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-20 \
    --prompt "Document config items → verify env vars/secrets → update CONFIG_RECORDS.md for FR-20" --phase 8 --project $REPO
  ```
- [ ] **[B-1]** Agent B (ARCHITECT) for FR-20 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md §FR-XX section`
  - `08-config/CONFIG_RECORDS.md (FR-XX draft entry)`
  - `03-development/src/.../fr_xx.py`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following configuration record for FR-20.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (FR-XX draft entry)] ===
  {paste full content here}

  === [DOC 3: 03-development/src/.../fr_xx.py] ===
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
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-20 \
    --prompt "Review FR-20 against SRS + SAD" --phase 8 --project $REPO
  ```
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-20: Gate 1 — FR-20
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-20 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- "03-development/src/**/*fr_20*" "03-development/src/**/*fr-20*" "tests/**/test_fr_20*" "tests/**/test_fr-20*" 2>/dev/null || echo '.'
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-20:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 8 --fr-id FR-20 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-20 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-20:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 8 --fr-id FR-20
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

#### FR-21: Configuration Record
- [ ] Confirm FR-21 configuration items are documented in CONFIG_RECORDS.md
- [ ] Confirm environment variables / secrets are managed (not hardcoded)
- [ ] Confirm deployment checklist entries for FR-21

**A/B Work — FR-21** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVOPS): Document config items → verify env vars/secrets → update CONFIG_RECORDS.md
  - Docstrings: `[FR-21]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-21 \
    --prompt "Document config items → verify env vars/secrets → update CONFIG_RECORDS.md for FR-21" --phase 8 --project $REPO
  ```
- [ ] **[B-1]** Agent B (ARCHITECT) for FR-21 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md §FR-XX section`
  - `08-config/CONFIG_RECORDS.md (FR-XX draft entry)`
  - `03-development/src/.../fr_xx.py`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following configuration record for FR-21.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (FR-XX draft entry)] ===
  {paste full content here}

  === [DOC 3: 03-development/src/.../fr_xx.py] ===
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
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-21 \
    --prompt "Review FR-21 against SRS + SAD" --phase 8 --project $REPO
  ```
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-21: Gate 1 — FR-21
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-21 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- "03-development/src/**/*fr_21*" "03-development/src/**/*fr-21*" "tests/**/test_fr_21*" "tests/**/test_fr-21*" 2>/dev/null || echo '.'
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-21:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 8 --fr-id FR-21 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-21 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-21:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 8 --fr-id FR-21
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

#### FR-22: Configuration Record
- [ ] Confirm FR-22 configuration items are documented in CONFIG_RECORDS.md
- [ ] Confirm environment variables / secrets are managed (not hardcoded)
- [ ] Confirm deployment checklist entries for FR-22

**A/B Work — FR-22** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVOPS): Document config items → verify env vars/secrets → update CONFIG_RECORDS.md
  - Docstrings: `[FR-22]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-22 \
    --prompt "Document config items → verify env vars/secrets → update CONFIG_RECORDS.md for FR-22" --phase 8 --project $REPO
  ```
- [ ] **[B-1]** Agent B (ARCHITECT) for FR-22 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md §FR-XX section`
  - `08-config/CONFIG_RECORDS.md (FR-XX draft entry)`
  - `03-development/src/.../fr_xx.py`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following configuration record for FR-22.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (FR-XX draft entry)] ===
  {paste full content here}

  === [DOC 3: 03-development/src/.../fr_xx.py] ===
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
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-22 \
    --prompt "Review FR-22 against SRS + SAD" --phase 8 --project $REPO
  ```
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-22: Gate 1 — FR-22
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-22 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- "03-development/src/**/*fr_22*" "03-development/src/**/*fr-22*" "tests/**/test_fr_22*" "tests/**/test_fr-22*" 2>/dev/null || echo '.'
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-22:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 8 --fr-id FR-22 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-22 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-22:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 8 --fr-id FR-22
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

#### FR-23: Configuration Record
- [ ] Confirm FR-23 configuration items are documented in CONFIG_RECORDS.md
- [ ] Confirm environment variables / secrets are managed (not hardcoded)
- [ ] Confirm deployment checklist entries for FR-23

**A/B Work — FR-23** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVOPS): Document config items → verify env vars/secrets → update CONFIG_RECORDS.md
  - Docstrings: `[FR-23]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-23 \
    --prompt "Document config items → verify env vars/secrets → update CONFIG_RECORDS.md for FR-23" --phase 8 --project $REPO
  ```
- [ ] **[B-1]** Agent B (ARCHITECT) for FR-23 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md §FR-XX section`
  - `08-config/CONFIG_RECORDS.md (FR-XX draft entry)`
  - `03-development/src/.../fr_xx.py`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following configuration record for FR-23.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (FR-XX draft entry)] ===
  {paste full content here}

  === [DOC 3: 03-development/src/.../fr_xx.py] ===
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
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-23 \
    --prompt "Review FR-23 against SRS + SAD" --phase 8 --project $REPO
  ```
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-23: Gate 1 — FR-23
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-23 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- "03-development/src/**/*fr_23*" "03-development/src/**/*fr-23*" "tests/**/test_fr_23*" "tests/**/test_fr-23*" 2>/dev/null || echo '.'
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-23:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 8 --fr-id FR-23 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-23 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-23:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 8 --fr-id FR-23
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

#### FR-24: Configuration Record
- [ ] Confirm FR-24 configuration items are documented in CONFIG_RECORDS.md
- [ ] Confirm environment variables / secrets are managed (not hardcoded)
- [ ] Confirm deployment checklist entries for FR-24

**A/B Work — FR-24** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVOPS): Document config items → verify env vars/secrets → update CONFIG_RECORDS.md
  - Docstrings: `[FR-24]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-24 \
    --prompt "Document config items → verify env vars/secrets → update CONFIG_RECORDS.md for FR-24" --phase 8 --project $REPO
  ```
- [ ] **[B-1]** Agent B (ARCHITECT) for FR-24 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md §FR-XX section`
  - `08-config/CONFIG_RECORDS.md (FR-XX draft entry)`
  - `03-development/src/.../fr_xx.py`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following configuration record for FR-24.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 08-config/CONFIG_RECORDS.md (FR-XX draft entry)] ===
  {paste full content here}

  === [DOC 3: 03-development/src/.../fr_xx.py] ===
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
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-24 \
    --prompt "Review FR-24 against SRS + SAD" --phase 8 --project $REPO
  ```
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-24: Gate 1 — FR-24
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P8): skip if FR-24 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- "03-development/src/**/*fr_24*" "03-development/src/**/*fr-24*" "tests/**/test_fr_24*" "tests/**/test_fr-24*" 2>/dev/null || echo '.'
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-24:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 8 --fr-id FR-24 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-24 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-24:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 8 --fr-id FR-24
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
- [x] `.methodology/sessions_spawn.log` — auto-populated by AgentSpawner (HR-10)
- [ ] Gate 1 PASS for every FR

#### ASPICE Traceability Requirements (enforced by postflight)

- [ ] **[ASPICE]** Artifact for Phase 8 MUST reference `07-risk/RISK_STATUS_REPORT.md` by filename keyword `RISK_STATUS_REPORT` (ASPICE traceability — `postflight_artifact_links()` enforces this)
- [ ] **[ASPICE]** Artifact for Phase 8 MUST reference `07-risk/RISK_REGISTER.md` by filename keyword `RISK_REGISTER` (ASPICE traceability — `postflight_artifact_links()` enforces this)


- [ ] **[PHASE-TRUTH]** Phase Truth ≥ 90% (HR-11) — verified by advance-phase

### 🎉 Pipeline Complete

- [ ] All 8 phases complete. Archive `.methodology/` for the audit trail.
