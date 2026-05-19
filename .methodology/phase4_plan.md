# Phase 4 Full Execution Plan -- omnibot-full

> **Version**: v2.3.0 (project plan)
> **Project**: omnibot-full
> **Date**: 2026-05-19
> **Framework**: harness-methodology v2.3.0
> **Phase**: 4 - Testing
> **Status**: Full version (including Phase 4 detailed tasks)

---

## Phase 4 Tasks: Test Planning & Execution

### Phase 4 Overview
Phase 4 formulates and executes a complete test plan based on Phase 3 code.
Each FR ends with a Gate 1 re-evaluation (CHECKPOINT). Phase exits via Gate 3 (15 dims).

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
> - CHECKPOINT-25: Gate 3 (Phase 4 Exit) → **push + HANDOVER.md**

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
  4. Phase 4 confirmed in `.methodology/state.json` (`advance-phase` already run)
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

#### FR-14: Platform Adapter — Messenger + WhatsApp Webhook
**Test Target**: Verify Phase 1 已支援 Telegram 和 LINE webhook。Phase 2 新增 Messenger 和 WhatsApp 兩個平台的 webhook 接收端點，使用 HMAC-SHA256 驗證，轉換為 UnifiedMessage。

**A/B Work — FR-14** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (QA_ENGINEER): Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage
  - Docstrings: `[FR-14]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-14 \
    --prompt "Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage for FR-14" --phase 4 --project $REPO
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
  - `02-architecture/SAD.md module spec`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_PLAN.md entry for FR-XX`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-14.
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
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-14 \
    --prompt "Review FR-14 against SRS + SAD" --phase 4 --project $REPO
  ```
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-14: Gate 1 — FR-14
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-14:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 4 --fr-id FR-14
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-14 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-14:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 4 --fr-id FR-14
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

#### FR-15: Prompt Injection Defense L3 — Sandwich Defense
**Test Target**: Verify 在 Input Sanitizer L2（字元正規化）之後，L3 層偵測 10 種可疑 prompt injection pattern，阻擋攻擊並記錄至 security_logs。安全輸入使用 Sandwich Defense 格式包裹後傳遞給 LLM。

**A/B Work — FR-15** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (QA_ENGINEER): Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage
  - Docstrings: `[FR-15]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-15 \
    --prompt "Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage for FR-15" --phase 4 --project $REPO
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
  - `02-architecture/SAD.md module spec`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_PLAN.md entry for FR-XX`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-15.
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
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-15 \
    --prompt "Review FR-15 against SRS + SAD" --phase 4 --project $REPO
  ```
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-15: Gate 1 — FR-15
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-15:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 4 --fr-id FR-15
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-15 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-15:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 4 --fr-id FR-15
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

#### FR-16: PII Masking V2 — Credit Card + Luhn Check
**Test Target**: Verify 在 Phase 1 PII Masking L4 基礎上新增信用卡號偵測與 Luhn 校驗，確保僅遮蔽有效信用卡號。

**A/B Work — FR-16** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (QA_ENGINEER): Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage
  - Docstrings: `[FR-16]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-16 \
    --prompt "Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage for FR-16" --phase 4 --project $REPO
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
  - `02-architecture/SAD.md module spec`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_PLAN.md entry for FR-XX`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-16.
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
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-16 \
    --prompt "Review FR-16 against SRS + SAD" --phase 4 --project $REPO
  ```
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-16: Gate 1 — FR-16
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-16:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 4 --fr-id FR-16
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-16 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-16:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 4 --fr-id FR-16
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

#### FR-17: Emotion Analyzer — Sentiment Classification + Decay
**Test Target**: Verify 分析每條使用者訊息的情緒類別與強度，追蹤情緒歷史並以 24 小時半衰期進行指數衰減加權。連續 >= 3 次負面情緒自動觸發人工轉接。

**A/B Work — FR-17** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (QA_ENGINEER): Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage
  - Docstrings: `[FR-17]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-17 \
    --prompt "Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage for FR-17" --phase 4 --project $REPO
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
  - `02-architecture/SAD.md module spec`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_PLAN.md entry for FR-XX`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-17.
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
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-17 \
    --prompt "Review FR-17 against SRS + SAD" --phase 4 --project $REPO
  ```
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-17: Gate 1 — FR-17
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-17:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 4 --fr-id FR-17
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-17 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-17:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 4 --fr-id FR-17
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

#### FR-18: Intent Router + Dialogue State Tracker (DST)
**Test Target**: Verify 實作 7 狀態對話狀態機（DST），支援意圖偵測、slot filling 與自動轉接。最多 3 輪未完成 slot filling 觸發轉接。

**A/B Work — FR-18** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (QA_ENGINEER): Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage
  - Docstrings: `[FR-18]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-18 \
    --prompt "Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage for FR-18" --phase 4 --project $REPO
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
  - `02-architecture/SAD.md module spec`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_PLAN.md entry for FR-XX`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-18.
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
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-18 \
    --prompt "Review FR-18 against SRS + SAD" --phase 4 --project $REPO
  ```
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-18: Gate 1 — FR-18
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-18:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 4 --fr-id FR-18
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-18 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-18:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 4 --fr-id FR-18
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

#### FR-19: Hybrid Knowledge Layer V2 — Four-Layer Architecture
**Test Target**: Verify 升級 Phase 1 的 Knowledge Layer V1（僅 Layer 1+4）為完整四層架構（HybridKnowledgeV2）：Layer 1 規則匹配 (40%)、Layer 2 RAG 向量檢索 (40%)、Layer 3 LLM 生成 (10%)、Layer 4 人工轉接 (10%)。Layer 1 + Layer 2 結果透過 RRF k=60 融合排序。實作類別命名為 HybridKnowledgeV2（Phase 2 對應版本）。

**A/B Work — FR-19** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (QA_ENGINEER): Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage
  - Docstrings: `[FR-19]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-19 \
    --prompt "Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage for FR-19" --phase 4 --project $REPO
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
  - `02-architecture/SAD.md module spec`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_PLAN.md entry for FR-XX`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-19.
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
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-19 \
    --prompt "Review FR-19 against SRS + SAD" --phase 4 --project $REPO
  ```
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-19: Gate 1 — FR-19
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-19:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 4 --fr-id FR-19
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-19 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-19:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 4 --fr-id FR-19
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

#### FR-20: Escalation Manager V2 — SLA Priority Levels
**Test Target**: Verify 從 Phase 1 BasicEscalationManager 升級，新增 SLA 優先級分級、sla_deadline 計算與違規查詢。

**A/B Work — FR-20** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (QA_ENGINEER): Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage
  - Docstrings: `[FR-20]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-20 \
    --prompt "Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage for FR-20" --phase 4 --project $REPO
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
  - `02-architecture/SAD.md module spec`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_PLAN.md entry for FR-XX`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-20.
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
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-20 \
    --prompt "Review FR-20 against SRS + SAD" --phase 4 --project $REPO
  ```
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-20: Gate 1 — FR-20
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-20:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 4 --fr-id FR-20
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-20 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-20:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 4 --fr-id FR-20
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

#### FR-21: Grounding Checks L5 — Semantic Alignment Verification
**Test Target**: Verify 驗證 LLM 生成輸出與知識庫來源內容的語義相似度，cosine similarity >= 0.75 視為 grounded，低於閾值拒絕輸出並轉接人工。

**A/B Work — FR-21** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (QA_ENGINEER): Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage
  - Docstrings: `[FR-21]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-21 \
    --prompt "Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage for FR-21" --phase 4 --project $REPO
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
  - `02-architecture/SAD.md module spec`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_PLAN.md entry for FR-XX`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-21.
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
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-21 \
    --prompt "Review FR-21 against SRS + SAD" --phase 4 --project $REPO
  ```
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-21: Gate 1 — FR-21
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-21:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 4 --fr-id FR-21
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-21 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-21:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 4 --fr-id FR-21
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

#### FR-22: Prometheus Metrics — Core Instrumentation
**Test Target**: Verify 匯出 8 個核心 Prometheus metrics，覆蓋延遲、請求量、FCR、知識層命中、PII 遮蔽、轉接佇列、情緒觸發與 LLM token 用量。

**A/B Work — FR-22** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (QA_ENGINEER): Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage
  - Docstrings: `[FR-22]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-22 \
    --prompt "Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage for FR-22" --phase 4 --project $REPO
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
  - `02-architecture/SAD.md module spec`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_PLAN.md entry for FR-XX`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-22.
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
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-22 \
    --prompt "Review FR-22 against SRS + SAD" --phase 4 --project $REPO
  ```
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-22: Gate 1 — FR-22
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-22:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 4 --fr-id FR-22
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-22 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-22:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 4 --fr-id FR-22
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

#### FR-23: Database Schema — Phase 2 Incremental Tables + Index
**Test Target**: Verify 在 Phase 1 核心表基礎上新增 emotion_history、edge_cases 表，並啟用 knowledge_base 的 pgvector ivfflat 索引。

**A/B Work — FR-23** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (QA_ENGINEER): Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage
  - Docstrings: `[FR-23]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-23 \
    --prompt "Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage for FR-23" --phase 4 --project $REPO
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
  - `02-architecture/SAD.md module spec`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_PLAN.md entry for FR-XX`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-23.
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
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-23 \
    --prompt "Review FR-23 against SRS + SAD" --phase 4 --project $REPO
  ```
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-23: Gate 1 — FR-23
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-23:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 4 --fr-id FR-23
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-23 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-23:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 4 --fr-id FR-23
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

#### FR-24: Golden Dataset — Edge Case Collection + Regression Baseline
**Test Target**: Verify 建立 500 筆黃金數據集，涵蓋 6 種邊界案例類型，用於回歸測試自動化驗證。

**A/B Work — FR-24** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (QA_ENGINEER): Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage
  - Docstrings: `[FR-24]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-24 \
    --prompt "Execute TEST_PLAN.md test cases for this FR → record results in TEST_RESULTS.md → verify ≥80% branch coverage for FR-24" --phase 4 --project $REPO
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
  - `02-architecture/SAD.md module spec`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_PLAN.md entry for FR-XX`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are ARCHITECT. Your task: review the following deliverable for FR-24.
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
  python3 harness_cli.py dispatch --role reviewer --fr-id FR-24 \
    --prompt "Review FR-24 against SRS + SAD" --phase 4 --project $REPO
  ```
  > AgentSpawner auto-logs to `.methodology/sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-24: Gate 1 — FR-24
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.

- [ ] **G1a** Prepare Gate 1 for FR-24:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 4 --fr-id FR-24
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-24 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-24:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 4 --fr-id FR-24
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
> All FR IDs in this project: FR-01,FR-02,FR-03,FR-04,FR-05,…+19

- [ ] **P4-mid** (trigger when ≥12/24 FRs have Gate 1 PASS):
  ```bash
  python3 harness_cli.py push-milestone --type p4-mid --project . \
    --fr-done 12 --fr-total 24 --fr-ids FR-01,FR-02,FR-03,FR-04,FR-05,FR-06,FR-07,FR-08,FR-09,FR-10,FR-11,FR-12
  ```
  > `--fr-ids` lists the FRs with Gate 1 PASS so far. Replace `FR-01,FR-02,FR-03,FR-04,FR-05,FR-06,FR-07,FR-08,FR-09,FR-10,FR-11,FR-12` with actual.
  > Writes HANDOVER.md + commits + pushes. Next session reads HANDOVER.md to resume.

- [ ] **P4-pre-SSI** (trigger when all 24 FRs Gate 1 PASS, before SSI):
  ```bash
  python3 harness_cli.py push-milestone --type p4-pre-ssi --project . \
    --fr-ids FR-01,FR-02,FR-03,FR-04,FR-05,FR-06,FR-07,FR-08,FR-09,FR-10,FR-11,FR-12,FR-13,FR-14,FR-15,FR-16,FR-17,FR-18,FR-19,FR-20,FR-21,FR-22,FR-23,FR-24
  ```
  > Last stable snapshot before SSI modifies files. HANDOVER.md + push.


### 🔒 CHECKPOINT-25: Gate 3 — Phase 4 Exit
> linting(90) · type_safety(85) · test_coverage(80) · security(80) · secrets_scanning(100) · license_compliance(100) · mutation_testing(70) · integration_coverage(60) · architecture(80) · readability(80) · error_handling(80) · documentation(75) · test_assertion_quality(60) · performance(75)  [CRG recon inside run-gate · D4 TEST_INVENTORY.yaml imperative check ≥80%]

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

- [ ] **[PHASE-TRUTH]** Phase Truth ≥ 90% (HR-11) — verified by advance-phase

### Phase 4 Deliverables
- [ ] `TEST_PLAN.md` - Test plan
- [ ] `TEST_RESULTS.md` - Test results
- [ ] `COVERAGE_REPORT.md` - Coverage report
- [x] `.methodology/sessions_spawn.log` — auto-populated by AgentSpawner (HR-10)
- [ ] Gate 1 PASS for every FR
- [ ] Gate 3 PASS (phase exit, composite ≥ 80, 15 dims)

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
