# Phase 4 Full Execution Plan -- omnibot-full

> **Version**: v2.3.0 (project plan)
> **Project**: omnibot-full
> **Date**: 2026-05-16
> **Framework**: harness-methodology v2.3.0
> **Phase**: 4 - Testing
> **Status**: Full version (including Phase 4 detailed tasks)

---

## Phase 4 Tasks: Test Planning & Execution

### Phase 4 Overview
Phase 4 formulates and executes a complete test plan based on Phase 3 code.
Each FR ends with a Gate 1 re-evaluation (CHECKPOINT). Phase exits via Gate 3 (12 dims).

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
> - CHECKPOINT-14: Gate 3 (Phase 4 Exit) → **push + HANDOVER.md**

### Entry Gate Verification

- [ ] **[ENTRY-CHECK]** Gate 2 PASS:
  Proof: .methodology/quality_manifest.json records Gate 2 PASS from P3.
  If NOT confirmed: return to Phase 3 and complete exit gate first.

### Pre-Phase Preflight

- [ ] **[PREFLIGHT]** Run phase hooks (FSM, Constitution, Kill-Switch, Drift, CI Readiness):
  ```bash
  python3 harness_cli.py run-phase --phase 4 --project $REPO
  ```
  If FAILED: fix FSM/Constitution issues. There is no gate bypass flag.

- [ ] **[PREFLIGHT-CI]** Confirm CI wiring unchanged (should be set since P1):
  1. `.github/workflows/harness_quality_gate.yml` exists
  2. Git hooks installed (`ls .git/hooks/prepare-commit-msg`)
  3. harness importable (submodule, PYTHONPATH, or vendored `quality_gate/`)
  4. GitHub repo variable `CURRENT_PHASE` = 4 (updated by `advance-phase`)
  > If stale: run `python3 harness_cli.py init-project --phase 4 --project $REPO --overwrite`

### CHECKPOINT-0: Generate TEST_PLAN.md

> Generate `04-testing/TEST_PLAN.md` from SRS.md FR acceptance criteria.
> This step runs once before per-FR test execution.

**A/B Work — TEST_PLAN.md Generation** (HR-01: A≠B · HR-04: HybridWorkflow ON):
- [ ] **[A-TP]** Agent A (QA_ENGINEER): Read SRS.md FR acceptance criteria → write TEST_PLAN.md with per-FR test cases
  - For each FR: test case ID, description, input, expected output, priority
  - Include positive, negative, boundary, and edge case categories
  - Output: `04-testing/TEST_PLAN.md`
- [ ] **[A-DISPATCH-TP]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id ALL \
    --prompt "Generate TEST_PLAN.md from SRS.md FR acceptance criteria" --phase 4 --project .
  ```
- [ ] **[B-TP]** Agent B (ARCHITECT): Review TEST_PLAN.md for completeness and correctness
- [ ] **[TP-DONE]** TEST_PLAN.md written and reviewed: all FRs have ≥1 test case, NFRs addressed

### FR Test Coverage

#### FR-01: Platform Adapter — Telegram + LINE Webhook
**Test Target**: Verify 系統必須接收來自 Telegram Bot API 和 LINE Messaging API 的 webhook 請求，轉換為內部統一消息格式（UnifiedMessage）。

**A/B Work — FR-01** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (QA_ENGINEER): Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage
  - Docstrings: `[FR-01]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-01 \
    --prompt "Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage for FR-01" --phase 4 --project $REPO
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
  - `02-architecture/SAD.md module spec`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_PLAN.md entry for FR-XX`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-01.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 02-architecture/SAD.md module spec] ===
  {paste full content here}

  === [DOC 3: 03-development/src/…/fr_xx.py] ===
  {paste full content here}

  === [DOC 4: tests/…/test_fr_xx.py] ===
  {paste full content here}

  === [DOC 5: 04-testing/TEST_PLAN.md entry for FR-XX] ===
  {paste full content here}

  Review checklist:
  - Test coverage ≥80% for this FR?
  - Edge cases covered?
  - Results match TEST_PLAN.md expected outcomes?

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
    --prompt "Review FR-01 against SRS + SAD" --phase 4 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-1: Gate 1 — FR-01
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-01:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 4 --fr-id FR-01
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-01 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-01:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 4 --fr-id FR-01
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p4-mid` / `p4-pre-ssi` / Gate exit.

#### FR-02: Webhook Signature Verification
**Test Target**: Verify 每個 webhook 請求必須先通過簽名驗證，未通過者拒絕處理。

**A/B Work — FR-02** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (QA_ENGINEER): Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage
  - Docstrings: `[FR-02]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-02 \
    --prompt "Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage for FR-02" --phase 4 --project $REPO
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
  - `02-architecture/SAD.md module spec`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_PLAN.md entry for FR-XX`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-02.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 02-architecture/SAD.md module spec] ===
  {paste full content here}

  === [DOC 3: 03-development/src/…/fr_xx.py] ===
  {paste full content here}

  === [DOC 4: tests/…/test_fr_xx.py] ===
  {paste full content here}

  === [DOC 5: 04-testing/TEST_PLAN.md entry for FR-XX] ===
  {paste full content here}

  Review checklist:
  - Test coverage ≥80% for this FR?
  - Edge cases covered?
  - Results match TEST_PLAN.md expected outcomes?

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
    --prompt "Review FR-02 against SRS + SAD" --phase 4 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-2: Gate 1 — FR-02
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-02:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 4 --fr-id FR-02
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-02 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-02:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 4 --fr-id FR-02
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p4-mid` / `p4-pre-ssi` / Gate exit.

#### FR-03: Unified Message Format
**Test Target**: Verify 所有平台消息必須轉換為統一的 `UnifiedMessage` dataclass，對下游模組隱藏平台差異。

**A/B Work — FR-03** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (QA_ENGINEER): Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage
  - Docstrings: `[FR-03]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-03 \
    --prompt "Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage for FR-03" --phase 4 --project $REPO
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
  - `02-architecture/SAD.md module spec`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_PLAN.md entry for FR-XX`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-03.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 02-architecture/SAD.md module spec] ===
  {paste full content here}

  === [DOC 3: 03-development/src/…/fr_xx.py] ===
  {paste full content here}

  === [DOC 4: tests/…/test_fr_xx.py] ===
  {paste full content here}

  === [DOC 5: 04-testing/TEST_PLAN.md entry for FR-XX] ===
  {paste full content here}

  Review checklist:
  - Test coverage ≥80% for this FR?
  - Edge cases covered?
  - Results match TEST_PLAN.md expected outcomes?

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
    --prompt "Review FR-03 against SRS + SAD" --phase 4 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-3: Gate 1 — FR-03
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-03:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 4 --fr-id FR-03
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-03 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-03:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 4 --fr-id FR-03
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p4-mid` / `p4-pre-ssi` / Gate exit.

#### FR-04: Input Sanitizer L2 — Character Normalization
**Test Target**: Verify 所有使用者輸入文字必須經過 NFKC 正規化，移除非列印控制字元。

**A/B Work — FR-04** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (QA_ENGINEER): Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage
  - Docstrings: `[FR-04]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-04 \
    --prompt "Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage for FR-04" --phase 4 --project $REPO
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
  - `02-architecture/SAD.md module spec`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_PLAN.md entry for FR-XX`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-04.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 02-architecture/SAD.md module spec] ===
  {paste full content here}

  === [DOC 3: 03-development/src/…/fr_xx.py] ===
  {paste full content here}

  === [DOC 4: tests/…/test_fr_xx.py] ===
  {paste full content here}

  === [DOC 5: 04-testing/TEST_PLAN.md entry for FR-XX] ===
  {paste full content here}

  Review checklist:
  - Test coverage ≥80% for this FR?
  - Edge cases covered?
  - Results match TEST_PLAN.md expected outcomes?

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
    --prompt "Review FR-04 against SRS + SAD" --phase 4 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-4: Gate 1 — FR-04
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-04:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 4 --fr-id FR-04
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-04 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-04:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 4 --fr-id FR-04
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p4-mid` / `p4-pre-ssi` / Gate exit.

#### FR-05: PII Masking L4 — Phone / Email / Address
**Test Target**: Verify 使用者訊息中的台灣電話、Email、地址必須在記錄或輸出前遮蔽。敏感關鍵字觸發轉接。

**A/B Work — FR-05** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (QA_ENGINEER): Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage
  - Docstrings: `[FR-05]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-05 \
    --prompt "Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage for FR-05" --phase 4 --project $REPO
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
  - `02-architecture/SAD.md module spec`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_PLAN.md entry for FR-XX`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-05.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 02-architecture/SAD.md module spec] ===
  {paste full content here}

  === [DOC 3: 03-development/src/…/fr_xx.py] ===
  {paste full content here}

  === [DOC 4: tests/…/test_fr_xx.py] ===
  {paste full content here}

  === [DOC 5: 04-testing/TEST_PLAN.md entry for FR-XX] ===
  {paste full content here}

  Review checklist:
  - Test coverage ≥80% for this FR?
  - Edge cases covered?
  - Results match TEST_PLAN.md expected outcomes?

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
    --prompt "Review FR-05 against SRS + SAD" --phase 4 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-5: Gate 1 — FR-05
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-05:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 4 --fr-id FR-05
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-05 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-05:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 4 --fr-id FR-05
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p4-mid` / `p4-pre-ssi` / Gate exit.

#### FR-06: Rate Limiter — Token Bucket
**Test Target**: Verify 每個平台用戶必須有獨立的請求速率限制，防止濫用。

**A/B Work — FR-06** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (QA_ENGINEER): Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage
  - Docstrings: `[FR-06]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-06 \
    --prompt "Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage for FR-06" --phase 4 --project $REPO
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
  - `02-architecture/SAD.md module spec`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_PLAN.md entry for FR-XX`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-06.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 02-architecture/SAD.md module spec] ===
  {paste full content here}

  === [DOC 3: 03-development/src/…/fr_xx.py] ===
  {paste full content here}

  === [DOC 4: tests/…/test_fr_xx.py] ===
  {paste full content here}

  === [DOC 5: 04-testing/TEST_PLAN.md entry for FR-XX] ===
  {paste full content here}

  Review checklist:
  - Test coverage ≥80% for this FR?
  - Edge cases covered?
  - Results match TEST_PLAN.md expected outcomes?

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
    --prompt "Review FR-06 against SRS + SAD" --phase 4 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-6: Gate 1 — FR-06
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-06:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 4 --fr-id FR-06
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-06 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-06:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 4 --fr-id FR-06
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p4-mid` / `p4-pre-ssi` / Gate exit.

#### FR-07: Knowledge Layer V1 — Rule Match + Escalate
**Test Target**: Verify 查詢知識庫時先執行 SQL 精確/模糊匹配（Layer 1），信心度 > 0.7 直接回覆，否則轉接人工。

**A/B Work — FR-07** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (QA_ENGINEER): Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage
  - Docstrings: `[FR-07]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-07 \
    --prompt "Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage for FR-07" --phase 4 --project $REPO
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
  - `02-architecture/SAD.md module spec`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_PLAN.md entry for FR-XX`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-07.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 02-architecture/SAD.md module spec] ===
  {paste full content here}

  === [DOC 3: 03-development/src/…/fr_xx.py] ===
  {paste full content here}

  === [DOC 4: tests/…/test_fr_xx.py] ===
  {paste full content here}

  === [DOC 5: 04-testing/TEST_PLAN.md entry for FR-XX] ===
  {paste full content here}

  Review checklist:
  - Test coverage ≥80% for this FR?
  - Edge cases covered?
  - Results match TEST_PLAN.md expected outcomes?

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
    --prompt "Review FR-07 against SRS + SAD" --phase 4 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-7: Gate 1 — FR-07
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-07:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 4 --fr-id FR-07
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-07 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-07:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 4 --fr-id FR-07
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p4-mid` / `p4-pre-ssi` / Gate exit.

#### FR-08: Basic Escalation Manager — No SLA
**Test Target**: Verify 無法匹配的查詢必須進入轉接佇列，支援指派與結案。

**A/B Work — FR-08** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (QA_ENGINEER): Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage
  - Docstrings: `[FR-08]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-08 \
    --prompt "Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage for FR-08" --phase 4 --project $REPO
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
  - `02-architecture/SAD.md module spec`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_PLAN.md entry for FR-XX`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-08.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 02-architecture/SAD.md module spec] ===
  {paste full content here}

  === [DOC 3: 03-development/src/…/fr_xx.py] ===
  {paste full content here}

  === [DOC 4: tests/…/test_fr_xx.py] ===
  {paste full content here}

  === [DOC 5: 04-testing/TEST_PLAN.md entry for FR-XX] ===
  {paste full content here}

  Review checklist:
  - Test coverage ≥80% for this FR?
  - Edge cases covered?
  - Results match TEST_PLAN.md expected outcomes?

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
    --prompt "Review FR-08 against SRS + SAD" --phase 4 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-8: Gate 1 — FR-08
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-08:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 4 --fr-id FR-08
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-08 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-08:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 4 --fr-id FR-08
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p4-mid` / `p4-pre-ssi` / Gate exit.

#### FR-09: Structured Logger — JSON Format
**Test Target**: Verify 所有日誌必須以 JSON 結構化格式輸出，包含 timestamp / level / service / message。

**A/B Work — FR-09** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (QA_ENGINEER): Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage
  - Docstrings: `[FR-09]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-09 \
    --prompt "Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage for FR-09" --phase 4 --project $REPO
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
  - `02-architecture/SAD.md module spec`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_PLAN.md entry for FR-XX`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-09.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 02-architecture/SAD.md module spec] ===
  {paste full content here}

  === [DOC 3: 03-development/src/…/fr_xx.py] ===
  {paste full content here}

  === [DOC 4: tests/…/test_fr_xx.py] ===
  {paste full content here}

  === [DOC 5: 04-testing/TEST_PLAN.md entry for FR-XX] ===
  {paste full content here}

  Review checklist:
  - Test coverage ≥80% for this FR?
  - Edge cases covered?
  - Results match TEST_PLAN.md expected outcomes?

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
    --prompt "Review FR-09 against SRS + SAD" --phase 4 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-9: Gate 1 — FR-09
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-09:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 4 --fr-id FR-09
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-09 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-09:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 4 --fr-id FR-09
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p4-mid` / `p4-pre-ssi` / Gate exit.

#### FR-10: API Response Format — ApiResponse / PaginatedResponse
**Test Target**: Verify 所有 API 回應必須使用統一的 `ApiResponse[T]` 或 `PaginatedResponse[T]` 泛型格式。

**A/B Work — FR-10** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (QA_ENGINEER): Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage
  - Docstrings: `[FR-10]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-10 \
    --prompt "Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage for FR-10" --phase 4 --project $REPO
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
  - `02-architecture/SAD.md module spec`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_PLAN.md entry for FR-XX`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-10.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 02-architecture/SAD.md module spec] ===
  {paste full content here}

  === [DOC 3: 03-development/src/…/fr_xx.py] ===
  {paste full content here}

  === [DOC 4: tests/…/test_fr_xx.py] ===
  {paste full content here}

  === [DOC 5: 04-testing/TEST_PLAN.md entry for FR-XX] ===
  {paste full content here}

  Review checklist:
  - Test coverage ≥80% for this FR?
  - Edge cases covered?
  - Results match TEST_PLAN.md expected outcomes?

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
    --prompt "Review FR-10 against SRS + SAD" --phase 4 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-10: Gate 1 — FR-10
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-10:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 4 --fr-id FR-10
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-10 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-10:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 4 --fr-id FR-10
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p4-mid` / `p4-pre-ssi` / Gate exit.

#### FR-11: Health Check Endpoint
**Test Target**: Verify 系統必須提供健康檢查端點供 Docker / 監控系統使用。

**A/B Work — FR-11** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (QA_ENGINEER): Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage
  - Docstrings: `[FR-11]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-11 \
    --prompt "Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage for FR-11" --phase 4 --project $REPO
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
  - `02-architecture/SAD.md module spec`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_PLAN.md entry for FR-XX`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-11.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 02-architecture/SAD.md module spec] ===
  {paste full content here}

  === [DOC 3: 03-development/src/…/fr_xx.py] ===
  {paste full content here}

  === [DOC 4: tests/…/test_fr_xx.py] ===
  {paste full content here}

  === [DOC 5: 04-testing/TEST_PLAN.md entry for FR-XX] ===
  {paste full content here}

  Review checklist:
  - Test coverage ≥80% for this FR?
  - Edge cases covered?
  - Results match TEST_PLAN.md expected outcomes?

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
    --prompt "Review FR-11 against SRS + SAD" --phase 4 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-11: Gate 1 — FR-11
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-11:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 4 --fr-id FR-11
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-11 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-11:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 4 --fr-id FR-11
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p4-mid` / `p4-pre-ssi` / Gate exit.

#### FR-12: Database Schema — All Core Tables
**Test Target**: Verify 必須建立所有核心資料表，包含 Phase 2/3 預留欄位，避免後續 ALTER TABLE。

**A/B Work — FR-12** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (QA_ENGINEER): Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage
  - Docstrings: `[FR-12]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-12 \
    --prompt "Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage for FR-12" --phase 4 --project $REPO
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
  - `02-architecture/SAD.md module spec`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_PLAN.md entry for FR-XX`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-12.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 02-architecture/SAD.md module spec] ===
  {paste full content here}

  === [DOC 3: 03-development/src/…/fr_xx.py] ===
  {paste full content here}

  === [DOC 4: tests/…/test_fr_xx.py] ===
  {paste full content here}

  === [DOC 5: 04-testing/TEST_PLAN.md entry for FR-XX] ===
  {paste full content here}

  Review checklist:
  - Test coverage ≥80% for this FR?
  - Edge cases covered?
  - Results match TEST_PLAN.md expected outcomes?

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
    --prompt "Review FR-12 against SRS + SAD" --phase 4 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-12: Gate 1 — FR-12
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-12:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 4 --fr-id FR-12
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-12 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-12:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 4 --fr-id FR-12
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p4-mid` / `p4-pre-ssi` / Gate exit.

#### FR-13: Docker Compose Development Environment
**Test Target**: Verify 提供一鍵啟動的開發環境，包含 API、PostgreSQL (pgvector)、Redis。

**A/B Work — FR-13** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (QA_ENGINEER): Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage
  - Docstrings: `[FR-13]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-13 \
    --prompt "Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage for FR-13" --phase 4 --project $REPO
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
  - `02-architecture/SAD.md module spec`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_PLAN.md entry for FR-XX`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-13.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md §FR-XX section] ===
  {paste full content here}

  === [DOC 2: 02-architecture/SAD.md module spec] ===
  {paste full content here}

  === [DOC 3: 03-development/src/…/fr_xx.py] ===
  {paste full content here}

  === [DOC 4: tests/…/test_fr_xx.py] ===
  {paste full content here}

  === [DOC 5: 04-testing/TEST_PLAN.md entry for FR-XX] ===
  {paste full content here}

  Review checklist:
  - Test coverage ≥80% for this FR?
  - Edge cases covered?
  - Results match TEST_PLAN.md expected outcomes?

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
    --prompt "Review FR-13 against SRS + SAD" --phase 4 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-13: Gate 1 — FR-13
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-13:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 4 --fr-id FR-13
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-13 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-13:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 4 --fr-id FR-13
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p4-mid` / `p4-pre-ssi` / Gate exit.

### P4 Milestone Pushes

> Per-FR Gate 1 only commits locally. The two **milestone pushes** below
> write `HANDOVER.md` and push to origin — these are the crash-recovery checkpoints.
> All FR IDs in this project: FR-01,FR-02,FR-03,FR-04,FR-05,…+8

- [ ] **P4-mid** (trigger when ≥6/13 FRs have Gate 1 PASS):
  ```bash
  python3 harness_cli.py push-milestone --type p4-mid --project . \
    --fr-done 6 --fr-total 13 --fr-ids FR-01,FR-02,FR-03,FR-04,FR-05,FR-06
  ```
  > `--fr-ids` lists the FRs with Gate 1 PASS so far. Replace `FR-01,FR-02,FR-03,FR-04,FR-05,FR-06` with actual.
  > Writes HANDOVER.md + commits + pushes. Next session reads HANDOVER.md to resume.

- [ ] **P4-pre-SSI** (trigger when all 13 FRs Gate 1 PASS, before SSI):
  ```bash
  python3 harness_cli.py push-milestone --type p4-pre-ssi --project . \
    --fr-ids FR-01,FR-02,FR-03,FR-04,FR-05,FR-06,FR-07,FR-08,FR-09,FR-10,FR-11,FR-12,FR-13
  ```
  > Last stable snapshot before SSI modifies files. HANDOVER.md + push.


### 🔒 CHECKPOINT-14: Gate 3 — Phase 4 Exit
> linting(90) · type_safety(85) · test_coverage(80) · security(80) · secrets_scanning(100) · license_compliance(100) · mutation_testing(70) · architecture(80) · readability(80) · error_handling(80) · documentation(75) · performance(75)  [CRG recon inside run-gate]

- [ ] **G3a** Prepare Gate 3:
  ```bash
  python3 harness_cli.py run-gate --gate 3 --phase 4
  ```
  Read the evaluation prompt printed above.
  (CRG recon triggered inside run-gate automatically — no separate action needed)

- [ ] **G3b** Evaluate all Gate 3 dimensions inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate3_result.json`
  - Failing dim: fix code → re-evaluate → re-score

- [ ] **G3c** Finalize Gate 3:
  ```bash
  python3 harness_cli.py finalize-gate --gate 3 --phase 4
  ```
  **Early-stop cases after G3c:**
  - CASE 1 PASS:     score ≥ score_gate AND critical==0 → `quality_complete=True` → G3d
  - CASE 2 CONTINUE: score ≥ score_gate BUT issues remain → fix → repeat G3a
  - CASE 3 PLATEAU:  3 consecutive rounds, no new issues → `deferred_fixes.md` → proceed to push
  - CASE 4 BLOCKED:  max_rounds exhausted, not PASS → `GateBlockedError` → escalate to human

- [ ] **G3d** ✅ Verify checkpoint saved (finalize-gate above already pushed + wrote HANDOVER.md):
  ```bash
  # Confirm HANDOVER.md exists at project root (written by finalize-gate → commit_and_push_gate)
  ls -la HANDOVER.md
  git log --oneline -1
  ```
  > `finalize-gate --gate 3` (G3c) calls `commit_and_push_gate()` which writes
  > `HANDOVER.md` **before** committing + pushing. No separate push needed here.
  > If HANDOVER.md is missing, re-run `finalize-gate` (do **not** raw-push).

- [ ] **[PHASE-TRUTH]** Verify Phase Truth ≥ 90% (HR-11):
  ```bash
  python3 harness_cli.py run-pipeline --phase-from 4
  ```
  Exit 0 = PASS, 11 = Phase Truth < 90%. Fix gaps before advancing.

### Phase 4 Deliverables
- [ ] `TEST_PLAN.md` - Test plan
- [ ] `TEST_RESULTS.md` - Test results
- [ ] `COVERAGE_REPORT.md` - Coverage report
- [x] `sessions_spawn.log` — auto-populated by AgentSpawner (HR-10)
- [ ] Gate 1 PASS for every FR
- [ ] Gate 3 PASS (phase exit, composite ≥ 80, 12 dims)

#### ASPICE Traceability Requirements (enforced by postflight)

- [ ] **[ASPICE]** Artifact for Phase 4 MUST reference `01-requirements/SRS.md` by filename keyword `SRS` (ASPICE traceability — `postflight_artifact_links()` enforces this)
- [ ] **[ASPICE]** Artifact for Phase 4 MUST reference `01-requirements/SPEC_TRACKING.md` by filename keyword `SPEC_TRACKING` (ASPICE traceability — `postflight_artifact_links()` enforces this)
- [ ] **[ASPICE]** Artifact for Phase 4 MUST reference `01-requirements/TRACEABILITY_MATRIX.md` by filename keyword `TRACEABILITY_MATRIX` (ASPICE traceability — `postflight_artifact_links()` enforces this)
- [ ] **[ASPICE]** Artifact for Phase 4 MUST reference `02-architecture/SAD.md` by filename keyword `SAD` (ASPICE traceability — `postflight_artifact_links()` enforces this)


### Phase 4 → Phase 5: Verification & Delivery

- [ ] Confirm ALL checkpoints in this plan are ✓  (no skips — HR-03)
- [ ] Generate Phase 5 plan:
  ```bash
  python3 harness_cli.py plan-phase --phase 5 --project $REPO \
    --output $REPO/.methodology/phase5_plan.md
  ```
- [ ] Advance FSM to Phase 5 (writes new HANDOVER.md + local commit):
  ```bash
  python3 harness_cli.py advance-phase --completed 4 --project .
  ```
- [ ] Confirm `HANDOVER.md` reflects Phase 5 entry (`P5-entry` checkpoint, correct plan path)
- [ ] Open `phase5_plan.md` and follow from the top.
- [ ] If session crashes during Phase 5: read `HANDOVER.md` or run `generate-next-plan`
