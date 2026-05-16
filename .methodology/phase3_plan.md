# Phase 3 Full Execution Plan -- omnibot-full

> **Version**: v2.3.0 (project plan)
> **Project**: omnibot-full
> **Date**: 2026-05-16
> **Framework**: harness-methodology v2.3.0
> **Phase**: 3 - Implementation
> **Status**: Full version (including Phase 3 detailed tasks)

---

## Phase 3 Tasks: Implementation

### Phase 3 Overview
Phase 3 implements all FR modules according to SAD, including unit tests.
Each FR ends with a Gate 1 quality evaluation (CHECKPOINT). Phase exits via Gate 2.

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
> - MILESTONE: P3-mid push (≥50% FRs Gate 1 PASS) → **HANDOVER.md**
> - MILESTONE: P3-pre-SSI push (all FRs done) → **HANDOVER.md**
> - CHECKPOINT-14: Gate 2 (Phase 3 Exit) → **push + HANDOVER.md**

### Entry Gate Verification

- [ ] **[ENTRY-CHECK]** P2 human APPROVE:
  Proof: git log contains commit 'phase2(human-review): Phase 2 deliverables APPROVED'.
  If NOT confirmed: return to Phase 2 and complete exit gate first.

### Pre-Phase Preflight

- [ ] **[PREFLIGHT]** Run phase hooks (FSM, Constitution, Kill-Switch, Drift, CI Readiness):
  ```bash
  python3 harness_cli.py run-phase --phase 3 --project $REPO
  ```
  If FAILED: fix FSM/Constitution issues. There is no gate bypass flag.

- [ ] **[PREFLIGHT-CI]** Confirm CI wiring unchanged (should be set since P1):
  1. `.github/workflows/harness_quality_gate.yml` exists
  2. Git hooks installed (`ls .git/hooks/prepare-commit-msg`)
  3. harness importable (submodule, PYTHONPATH, or vendored `quality_gate/`)
  4. GitHub repo variable `CURRENT_PHASE` = 3 (updated by `advance-phase`)
  > If stale: run `python3 harness_cli.py init-project --phase 3 --project $REPO --overwrite`

### FR Implementation Tasks (13 total)

#### FR-01: Platform Adapter — Telegram + LINE Webhook
**Task**: 系統必須接收來自 Telegram Bot API 和 LINE Messaging API 的 webhook 請求，轉換為內部統一消息格式（UnifiedMessage）。
**Forbidden**:
- app/infrastructure/ (deprecated)
- @covers: L1 Error
- @type: edge

**A/B Work — FR-01** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVELOPER): TDD: write failing test → implement → refactor (RED→GREEN→IMPROVE)
  - Docstrings: `[FR-01]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-01 \
    --prompt "TDD: write failing test → implement → refactor (RED→GREEN→IMPROVE) for FR-01" --phase 3 --project $REPO
  ```
- [ ] **[B-1]** Agent B (REVIEWER) for FR-01 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md §FR-XX section`
  - `02-architecture/SAD.md module spec for FR-XX`
  - `03-development/src/…/fr_xx.py (implemented code + tests)`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are REVIEWER. Your task: review the following deliverable for FR-01.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 02-architecture/SAD.md module spec for FR-XX] ===
  {paste full content here}

  === [DOC 3: 03-development/src/…/fr_xx.py (implemented code + tests)] ===
  {paste full content here}

  Review checklist:
  - Code matches SRS acceptance criteria?
  - Tests actually test the spec (not the impl)?
  - No forbidden patterns (app/infrastructure/, @covers: L1 Error)?
  - Docstrings have [FR-XX] tag + Citations?

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
    --prompt "Review FR-01 against SRS + SAD" --phase 3 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-1: Gate 1 — FR-01
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-01:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 3 --fr-id FR-01
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-01 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-01:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 3 --fr-id FR-01
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p3-mid` / `p3-pre-ssi` / Gate exit.

#### FR-02: Webhook Signature Verification
**Task**: 每個 webhook 請求必須先通過簽名驗證，未通過者拒絕處理。
**Forbidden**:
- app/infrastructure/ (deprecated)
- @covers: L1 Error
- @type: edge

**A/B Work — FR-02** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVELOPER): TDD: write failing test → implement → refactor (RED→GREEN→IMPROVE)
  - Docstrings: `[FR-02]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-02 \
    --prompt "TDD: write failing test → implement → refactor (RED→GREEN→IMPROVE) for FR-02" --phase 3 --project $REPO
  ```
- [ ] **[B-1]** Agent B (REVIEWER) for FR-02 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md §FR-XX section`
  - `02-architecture/SAD.md module spec for FR-XX`
  - `03-development/src/…/fr_xx.py (implemented code + tests)`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are REVIEWER. Your task: review the following deliverable for FR-02.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 02-architecture/SAD.md module spec for FR-XX] ===
  {paste full content here}

  === [DOC 3: 03-development/src/…/fr_xx.py (implemented code + tests)] ===
  {paste full content here}

  Review checklist:
  - Code matches SRS acceptance criteria?
  - Tests actually test the spec (not the impl)?
  - No forbidden patterns (app/infrastructure/, @covers: L1 Error)?
  - Docstrings have [FR-XX] tag + Citations?

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
    --prompt "Review FR-02 against SRS + SAD" --phase 3 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-2: Gate 1 — FR-02
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-02:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 3 --fr-id FR-02
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-02 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-02:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 3 --fr-id FR-02
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p3-mid` / `p3-pre-ssi` / Gate exit.

#### FR-03: Unified Message Format
**Task**: 所有平台消息必須轉換為統一的 `UnifiedMessage` dataclass，對下游模組隱藏平台差異。
**Forbidden**:
- app/infrastructure/ (deprecated)
- @covers: L1 Error
- @type: edge

**A/B Work — FR-03** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVELOPER): TDD: write failing test → implement → refactor (RED→GREEN→IMPROVE)
  - Docstrings: `[FR-03]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-03 \
    --prompt "TDD: write failing test → implement → refactor (RED→GREEN→IMPROVE) for FR-03" --phase 3 --project $REPO
  ```
- [ ] **[B-1]** Agent B (REVIEWER) for FR-03 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md §FR-XX section`
  - `02-architecture/SAD.md module spec for FR-XX`
  - `03-development/src/…/fr_xx.py (implemented code + tests)`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are REVIEWER. Your task: review the following deliverable for FR-03.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 02-architecture/SAD.md module spec for FR-XX] ===
  {paste full content here}

  === [DOC 3: 03-development/src/…/fr_xx.py (implemented code + tests)] ===
  {paste full content here}

  Review checklist:
  - Code matches SRS acceptance criteria?
  - Tests actually test the spec (not the impl)?
  - No forbidden patterns (app/infrastructure/, @covers: L1 Error)?
  - Docstrings have [FR-XX] tag + Citations?

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
    --prompt "Review FR-03 against SRS + SAD" --phase 3 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-3: Gate 1 — FR-03
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-03:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 3 --fr-id FR-03
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-03 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-03:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 3 --fr-id FR-03
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p3-mid` / `p3-pre-ssi` / Gate exit.

#### FR-04: Input Sanitizer L2 — Character Normalization
**Task**: 所有使用者輸入文字必須經過 NFKC 正規化，移除非列印控制字元。
**Forbidden**:
- app/infrastructure/ (deprecated)
- @covers: L1 Error
- @type: edge

**A/B Work — FR-04** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVELOPER): TDD: write failing test → implement → refactor (RED→GREEN→IMPROVE)
  - Docstrings: `[FR-04]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-04 \
    --prompt "TDD: write failing test → implement → refactor (RED→GREEN→IMPROVE) for FR-04" --phase 3 --project $REPO
  ```
- [ ] **[B-1]** Agent B (REVIEWER) for FR-04 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md §FR-XX section`
  - `02-architecture/SAD.md module spec for FR-XX`
  - `03-development/src/…/fr_xx.py (implemented code + tests)`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are REVIEWER. Your task: review the following deliverable for FR-04.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 02-architecture/SAD.md module spec for FR-XX] ===
  {paste full content here}

  === [DOC 3: 03-development/src/…/fr_xx.py (implemented code + tests)] ===
  {paste full content here}

  Review checklist:
  - Code matches SRS acceptance criteria?
  - Tests actually test the spec (not the impl)?
  - No forbidden patterns (app/infrastructure/, @covers: L1 Error)?
  - Docstrings have [FR-XX] tag + Citations?

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
    --prompt "Review FR-04 against SRS + SAD" --phase 3 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-4: Gate 1 — FR-04
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-04:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 3 --fr-id FR-04
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-04 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-04:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 3 --fr-id FR-04
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p3-mid` / `p3-pre-ssi` / Gate exit.

#### FR-05: PII Masking L4 — Phone / Email / Address
**Task**: 使用者訊息中的台灣電話、Email、地址必須在記錄或輸出前遮蔽。敏感關鍵字觸發轉接。
**Forbidden**:
- app/infrastructure/ (deprecated)
- @covers: L1 Error
- @type: edge

**A/B Work — FR-05** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVELOPER): TDD: write failing test → implement → refactor (RED→GREEN→IMPROVE)
  - Docstrings: `[FR-05]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-05 \
    --prompt "TDD: write failing test → implement → refactor (RED→GREEN→IMPROVE) for FR-05" --phase 3 --project $REPO
  ```
- [ ] **[B-1]** Agent B (REVIEWER) for FR-05 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md §FR-XX section`
  - `02-architecture/SAD.md module spec for FR-XX`
  - `03-development/src/…/fr_xx.py (implemented code + tests)`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are REVIEWER. Your task: review the following deliverable for FR-05.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 02-architecture/SAD.md module spec for FR-XX] ===
  {paste full content here}

  === [DOC 3: 03-development/src/…/fr_xx.py (implemented code + tests)] ===
  {paste full content here}

  Review checklist:
  - Code matches SRS acceptance criteria?
  - Tests actually test the spec (not the impl)?
  - No forbidden patterns (app/infrastructure/, @covers: L1 Error)?
  - Docstrings have [FR-XX] tag + Citations?

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
    --prompt "Review FR-05 against SRS + SAD" --phase 3 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-5: Gate 1 — FR-05
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-05:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 3 --fr-id FR-05
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-05 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-05:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 3 --fr-id FR-05
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p3-mid` / `p3-pre-ssi` / Gate exit.

#### FR-06: Rate Limiter — Token Bucket
**Task**: 每個平台用戶必須有獨立的請求速率限制，防止濫用。
**Forbidden**:
- app/infrastructure/ (deprecated)
- @covers: L1 Error
- @type: edge

**A/B Work — FR-06** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVELOPER): TDD: write failing test → implement → refactor (RED→GREEN→IMPROVE)
  - Docstrings: `[FR-06]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-06 \
    --prompt "TDD: write failing test → implement → refactor (RED→GREEN→IMPROVE) for FR-06" --phase 3 --project $REPO
  ```
- [ ] **[B-1]** Agent B (REVIEWER) for FR-06 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md §FR-XX section`
  - `02-architecture/SAD.md module spec for FR-XX`
  - `03-development/src/…/fr_xx.py (implemented code + tests)`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are REVIEWER. Your task: review the following deliverable for FR-06.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 02-architecture/SAD.md module spec for FR-XX] ===
  {paste full content here}

  === [DOC 3: 03-development/src/…/fr_xx.py (implemented code + tests)] ===
  {paste full content here}

  Review checklist:
  - Code matches SRS acceptance criteria?
  - Tests actually test the spec (not the impl)?
  - No forbidden patterns (app/infrastructure/, @covers: L1 Error)?
  - Docstrings have [FR-XX] tag + Citations?

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
    --prompt "Review FR-06 against SRS + SAD" --phase 3 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-6: Gate 1 — FR-06
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-06:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 3 --fr-id FR-06
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-06 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-06:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 3 --fr-id FR-06
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p3-mid` / `p3-pre-ssi` / Gate exit.

#### FR-07: Knowledge Layer V1 — Rule Match + Escalate
**Task**: 查詢知識庫時先執行 SQL 精確/模糊匹配（Layer 1），信心度 > 0.7 直接回覆，否則轉接人工。
**Forbidden**:
- app/infrastructure/ (deprecated)
- @covers: L1 Error
- @type: edge

**A/B Work — FR-07** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVELOPER): TDD: write failing test → implement → refactor (RED→GREEN→IMPROVE)
  - Docstrings: `[FR-07]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-07 \
    --prompt "TDD: write failing test → implement → refactor (RED→GREEN→IMPROVE) for FR-07" --phase 3 --project $REPO
  ```
- [ ] **[B-1]** Agent B (REVIEWER) for FR-07 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md §FR-XX section`
  - `02-architecture/SAD.md module spec for FR-XX`
  - `03-development/src/…/fr_xx.py (implemented code + tests)`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are REVIEWER. Your task: review the following deliverable for FR-07.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 02-architecture/SAD.md module spec for FR-XX] ===
  {paste full content here}

  === [DOC 3: 03-development/src/…/fr_xx.py (implemented code + tests)] ===
  {paste full content here}

  Review checklist:
  - Code matches SRS acceptance criteria?
  - Tests actually test the spec (not the impl)?
  - No forbidden patterns (app/infrastructure/, @covers: L1 Error)?
  - Docstrings have [FR-XX] tag + Citations?

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
    --prompt "Review FR-07 against SRS + SAD" --phase 3 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-7: Gate 1 — FR-07
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-07:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 3 --fr-id FR-07
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-07 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-07:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 3 --fr-id FR-07
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p3-mid` / `p3-pre-ssi` / Gate exit.

#### FR-08: Basic Escalation Manager — No SLA
**Task**: 無法匹配的查詢必須進入轉接佇列，支援指派與結案。
**Forbidden**:
- app/infrastructure/ (deprecated)
- @covers: L1 Error
- @type: edge

**A/B Work — FR-08** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVELOPER): TDD: write failing test → implement → refactor (RED→GREEN→IMPROVE)
  - Docstrings: `[FR-08]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-08 \
    --prompt "TDD: write failing test → implement → refactor (RED→GREEN→IMPROVE) for FR-08" --phase 3 --project $REPO
  ```
- [ ] **[B-1]** Agent B (REVIEWER) for FR-08 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md §FR-XX section`
  - `02-architecture/SAD.md module spec for FR-XX`
  - `03-development/src/…/fr_xx.py (implemented code + tests)`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are REVIEWER. Your task: review the following deliverable for FR-08.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 02-architecture/SAD.md module spec for FR-XX] ===
  {paste full content here}

  === [DOC 3: 03-development/src/…/fr_xx.py (implemented code + tests)] ===
  {paste full content here}

  Review checklist:
  - Code matches SRS acceptance criteria?
  - Tests actually test the spec (not the impl)?
  - No forbidden patterns (app/infrastructure/, @covers: L1 Error)?
  - Docstrings have [FR-XX] tag + Citations?

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
    --prompt "Review FR-08 against SRS + SAD" --phase 3 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-8: Gate 1 — FR-08
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-08:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 3 --fr-id FR-08
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-08 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-08:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 3 --fr-id FR-08
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p3-mid` / `p3-pre-ssi` / Gate exit.

#### FR-09: Structured Logger — JSON Format
**Task**: 所有日誌必須以 JSON 結構化格式輸出，包含 timestamp / level / service / message。
**Forbidden**:
- app/infrastructure/ (deprecated)
- @covers: L1 Error
- @type: edge

**A/B Work — FR-09** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVELOPER): TDD: write failing test → implement → refactor (RED→GREEN→IMPROVE)
  - Docstrings: `[FR-09]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-09 \
    --prompt "TDD: write failing test → implement → refactor (RED→GREEN→IMPROVE) for FR-09" --phase 3 --project $REPO
  ```
- [ ] **[B-1]** Agent B (REVIEWER) for FR-09 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md §FR-XX section`
  - `02-architecture/SAD.md module spec for FR-XX`
  - `03-development/src/…/fr_xx.py (implemented code + tests)`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are REVIEWER. Your task: review the following deliverable for FR-09.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 02-architecture/SAD.md module spec for FR-XX] ===
  {paste full content here}

  === [DOC 3: 03-development/src/…/fr_xx.py (implemented code + tests)] ===
  {paste full content here}

  Review checklist:
  - Code matches SRS acceptance criteria?
  - Tests actually test the spec (not the impl)?
  - No forbidden patterns (app/infrastructure/, @covers: L1 Error)?
  - Docstrings have [FR-XX] tag + Citations?

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
    --prompt "Review FR-09 against SRS + SAD" --phase 3 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-9: Gate 1 — FR-09
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-09:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 3 --fr-id FR-09
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-09 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-09:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 3 --fr-id FR-09
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p3-mid` / `p3-pre-ssi` / Gate exit.

#### FR-10: API Response Format — ApiResponse / PaginatedResponse
**Task**: 所有 API 回應必須使用統一的 `ApiResponse[T]` 或 `PaginatedResponse[T]` 泛型格式。
**Forbidden**:
- app/infrastructure/ (deprecated)
- @covers: L1 Error
- @type: edge

**A/B Work — FR-10** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVELOPER): TDD: write failing test → implement → refactor (RED→GREEN→IMPROVE)
  - Docstrings: `[FR-10]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-10 \
    --prompt "TDD: write failing test → implement → refactor (RED→GREEN→IMPROVE) for FR-10" --phase 3 --project $REPO
  ```
- [ ] **[B-1]** Agent B (REVIEWER) for FR-10 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md §FR-XX section`
  - `02-architecture/SAD.md module spec for FR-XX`
  - `03-development/src/…/fr_xx.py (implemented code + tests)`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are REVIEWER. Your task: review the following deliverable for FR-10.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 02-architecture/SAD.md module spec for FR-XX] ===
  {paste full content here}

  === [DOC 3: 03-development/src/…/fr_xx.py (implemented code + tests)] ===
  {paste full content here}

  Review checklist:
  - Code matches SRS acceptance criteria?
  - Tests actually test the spec (not the impl)?
  - No forbidden patterns (app/infrastructure/, @covers: L1 Error)?
  - Docstrings have [FR-XX] tag + Citations?

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
    --prompt "Review FR-10 against SRS + SAD" --phase 3 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-10: Gate 1 — FR-10
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-10:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 3 --fr-id FR-10
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-10 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-10:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 3 --fr-id FR-10
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p3-mid` / `p3-pre-ssi` / Gate exit.

#### FR-11: Health Check Endpoint
**Task**: 系統必須提供健康檢查端點供 Docker / 監控系統使用。
**Forbidden**:
- app/infrastructure/ (deprecated)
- @covers: L1 Error
- @type: edge

**A/B Work — FR-11** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVELOPER): TDD: write failing test → implement → refactor (RED→GREEN→IMPROVE)
  - Docstrings: `[FR-11]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-11 \
    --prompt "TDD: write failing test → implement → refactor (RED→GREEN→IMPROVE) for FR-11" --phase 3 --project $REPO
  ```
- [ ] **[B-1]** Agent B (REVIEWER) for FR-11 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md §FR-XX section`
  - `02-architecture/SAD.md module spec for FR-XX`
  - `03-development/src/…/fr_xx.py (implemented code + tests)`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are REVIEWER. Your task: review the following deliverable for FR-11.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 02-architecture/SAD.md module spec for FR-XX] ===
  {paste full content here}

  === [DOC 3: 03-development/src/…/fr_xx.py (implemented code + tests)] ===
  {paste full content here}

  Review checklist:
  - Code matches SRS acceptance criteria?
  - Tests actually test the spec (not the impl)?
  - No forbidden patterns (app/infrastructure/, @covers: L1 Error)?
  - Docstrings have [FR-XX] tag + Citations?

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
    --prompt "Review FR-11 against SRS + SAD" --phase 3 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-11: Gate 1 — FR-11
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-11:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 3 --fr-id FR-11
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-11 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-11:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 3 --fr-id FR-11
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p3-mid` / `p3-pre-ssi` / Gate exit.

#### FR-12: Database Schema — All Core Tables
**Task**: 必須建立所有核心資料表，包含 Phase 2/3 預留欄位，避免後續 ALTER TABLE。
**Forbidden**:
- app/infrastructure/ (deprecated)
- @covers: L1 Error
- @type: edge

**A/B Work — FR-12** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVELOPER): TDD: write failing test → implement → refactor (RED→GREEN→IMPROVE)
  - Docstrings: `[FR-12]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-12 \
    --prompt "TDD: write failing test → implement → refactor (RED→GREEN→IMPROVE) for FR-12" --phase 3 --project $REPO
  ```
- [ ] **[B-1]** Agent B (REVIEWER) for FR-12 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md §FR-XX section`
  - `02-architecture/SAD.md module spec for FR-XX`
  - `03-development/src/…/fr_xx.py (implemented code + tests)`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are REVIEWER. Your task: review the following deliverable for FR-12.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 02-architecture/SAD.md module spec for FR-XX] ===
  {paste full content here}

  === [DOC 3: 03-development/src/…/fr_xx.py (implemented code + tests)] ===
  {paste full content here}

  Review checklist:
  - Code matches SRS acceptance criteria?
  - Tests actually test the spec (not the impl)?
  - No forbidden patterns (app/infrastructure/, @covers: L1 Error)?
  - Docstrings have [FR-XX] tag + Citations?

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
    --prompt "Review FR-12 against SRS + SAD" --phase 3 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-12: Gate 1 — FR-12
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-12:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 3 --fr-id FR-12
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-12 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-12:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 3 --fr-id FR-12
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p3-mid` / `p3-pre-ssi` / Gate exit.

#### FR-13: Docker Compose Development Environment
**Task**: 提供一鍵啟動的開發環境，包含 API、PostgreSQL (pgvector)、Redis。
**Forbidden**:
- app/infrastructure/ (deprecated)
- @covers: L1 Error
- @type: edge

**A/B Work — FR-13** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVELOPER): TDD: write failing test → implement → refactor (RED→GREEN→IMPROVE)
  - Docstrings: `[FR-13]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-13 \
    --prompt "TDD: write failing test → implement → refactor (RED→GREEN→IMPROVE) for FR-13" --phase 3 --project $REPO
  ```
- [ ] **[B-1]** Agent B (REVIEWER) for FR-13 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md §FR-XX section`
  - `02-architecture/SAD.md module spec for FR-XX`
  - `03-development/src/…/fr_xx.py (implemented code + tests)`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are REVIEWER. Your task: review the following deliverable for FR-13.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 02-architecture/SAD.md module spec for FR-XX] ===
  {paste full content here}

  === [DOC 3: 03-development/src/…/fr_xx.py (implemented code + tests)] ===
  {paste full content here}

  Review checklist:
  - Code matches SRS acceptance criteria?
  - Tests actually test the spec (not the impl)?
  - No forbidden patterns (app/infrastructure/, @covers: L1 Error)?
  - Docstrings have [FR-XX] tag + Citations?

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
    --prompt "Review FR-13 against SRS + SAD" --phase 3 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-13: Gate 1 — FR-13
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-13:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 3 --fr-id FR-13
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-13 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-13:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 3 --fr-id FR-13
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p3-mid` / `p3-pre-ssi` / Gate exit.

### P3 Milestone Pushes (10-Push Strategy ③④)

> Per-FR Gate 1 only commits locally. The two **milestone pushes** below
> write `HANDOVER.md` and push to origin — these are the crash-recovery checkpoints.
> All FR IDs in this project: FR-01,FR-02,FR-03,FR-04,FR-05,…+8

- [ ] **PUSH ③ — P3-mid** (trigger when ≥6/13 FRs have Gate 1 PASS):
  ```bash
  python3 harness_cli.py push-milestone --type p3-mid --project . \
    --fr-done 6 --fr-total 13 --fr-ids FR-01,FR-02,FR-03,FR-04,FR-05,FR-06
  ```
  > `--fr-ids` lists the FRs with Gate 1 PASS so far. Replace `FR-01,FR-02,FR-03,FR-04,FR-05,FR-06` with actual.
  > Writes HANDOVER.md + commits + pushes. Next session reads HANDOVER.md to resume.

- [ ] **PUSH ④ — P3-pre-SSI** (trigger when all 13 FRs Gate 1 PASS, before SSI):
  ```bash
  python3 harness_cli.py push-milestone --type p3-pre-ssi --project . \
    --fr-ids FR-01,FR-02,FR-03,FR-04,FR-05,FR-06,FR-07,FR-08,FR-09,FR-10,FR-11,FR-12,FR-13
  ```
  > Last stable snapshot before SSI modifies files. HANDOVER.md + push.


### 🔒 CHECKPOINT-14: Gate 2 — Phase 3 Exit
> linting(90) · type_safety(85) · test_coverage(80) · security(80) · secrets_scanning(100) · license_compliance(100) · mutation_testing(70)

- [ ] **G2a** Prepare Gate 2:
  ```bash
  python3 harness_cli.py run-gate --gate 2 --phase 3
  ```
  Read the evaluation prompt printed above.

- [ ] **G2b** Evaluate all Gate 2 dimensions inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate2_result.json`
  - Failing dim: fix code → re-evaluate → re-score

- [ ] **G2c** Finalize Gate 2:
  ```bash
  python3 harness_cli.py finalize-gate --gate 2 --phase 3
  ```
  **Early-stop cases after G2c:**
  - CASE 1 PASS:     score ≥ score_gate AND critical==0 → `quality_complete=True` → G2d
  - CASE 2 CONTINUE: score ≥ score_gate BUT issues remain → fix → repeat G2a
  - CASE 3 PLATEAU:  3 consecutive rounds, no new issues → `deferred_fixes.md` → proceed to push
  - CASE 4 BLOCKED:  max_rounds exhausted, not PASS → `GateBlockedError` → escalate to human

- [ ] **G2d** ✅ Verify checkpoint saved (finalize-gate above already pushed + wrote HANDOVER.md):
  ```bash
  # Confirm HANDOVER.md exists at project root (written by finalize-gate → commit_and_push_gate)
  ls -la HANDOVER.md
  git log --oneline -1
  ```
  > `finalize-gate --gate 2` (G2c) calls `commit_and_push_gate()` which writes
  > `HANDOVER.md` **before** committing + pushing. No separate push needed here.
  > If HANDOVER.md is missing, re-run `finalize-gate` (do **not** raw-push).

- [ ] **[PHASE-TRUTH]** Verify Phase Truth ≥ 90% (HR-11):
  ```bash
  python3 harness_cli.py run-pipeline --phase-from 3
  ```
  Exit 0 = PASS, 11 = Phase Truth < 90%. Fix gaps before advancing.

### Phase 3 Deliverables
- [ ] `03-development/src/` - All FR modules implemented
- [ ] `tests/` - Unit tests (≥80% coverage per FR)
- [x] `sessions_spawn.log` — auto-populated by AgentSpawner (HR-10)
- [ ] Gate 1 PASS for every FR
- [ ] Gate 2 PASS (phase exit, composite ≥ 75)

### Phase 3 → Phase 4: Testing

- [ ] Confirm ALL checkpoints in this plan are ✓  (no skips — HR-03)
- [ ] Generate Phase 4 plan:
  ```bash
  python3 harness_cli.py plan-phase --phase 4 --project $REPO \
    --output $REPO/.methodology/phase4_plan.md
  ```
- [ ] Advance FSM to Phase 4 (writes new HANDOVER.md + local commit):
  ```bash
  python3 harness_cli.py advance-phase --completed 3 --project .
  ```
- [ ] Confirm `HANDOVER.md` reflects Phase 4 entry (`P4-entry` checkpoint, correct plan path)
- [ ] Open `phase4_plan.md` and follow from the top.
- [ ] If session crashes during Phase 4: read `HANDOVER.md` or run `generate-next-plan`
