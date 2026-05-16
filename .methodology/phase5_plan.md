# Phase 5 Full Execution Plan -- omnibot-full

> **Version**: v2.3.0 (project plan)
> **Project**: omnibot-full
> **Date**: 2026-05-16
> **Framework**: harness-methodology v2.3.0
> **Phase**: 5 - Verification & Delivery
> **Status**: Full version (including Phase 5 detailed tasks)

---

## Phase 5 Tasks: Verification & Delivery

### Phase 5 Overview
Phase 5 verifies the system against test results, ensuring all FRs meet acceptance criteria.
Each FR ends with a Gate 1 re-evaluation (CHECKPOINT). No phase-exit gate — P5 was cleared by Gate 3 at P4 exit.

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
> - MILESTONE: P5-baseline push (BASELINE.md generated) → **HANDOVER.md**

### Entry Gate Verification

- [ ] **[ENTRY-CHECK]** Confirm Phase 4 exit (Gate 3 PASS) before proceeding (HR-03 — no phase skips):
  Proof: .methodology/quality_manifest.json records Gate 3 PASS from P4.
  If NOT confirmed: return to Phase 4 and complete exit gate first.

### Pre-Phase Preflight

- [ ] **[PREFLIGHT]** Run phase hooks (FSM, Constitution, Kill-Switch, Drift, CI Readiness):
  ```bash
  python3 harness_cli.py run-phase --phase 5 --project $REPO
  ```
  If FAILED: fix FSM/Constitution issues. There is no gate bypass flag.

- [ ] **[PREFLIGHT-CI]** Confirm CI wiring unchanged (should be set since P1):
  1. `.github/workflows/harness_quality_gate.yml` exists
  2. Git hooks installed (`ls .git/hooks/prepare-commit-msg`)
  3. harness importable (submodule, PYTHONPATH, or vendored `quality_gate/`)
  4. GitHub repo variable `CURRENT_PHASE` = 5 (updated by `advance-phase`)
  > If stale: run `python3 harness_cli.py init-project --phase 5 --project $REPO --overwrite`

### FR Verification Tasks (13 total)

#### FR-01: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-01
- [ ] Run integration tests for FR-01
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**A/B Work — FR-01** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVELOPER): Verify FR acceptance criteria → confirm results match SRS → sign off
  - Docstrings: `[FR-01]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-01 \
    --prompt "Verify FR acceptance criteria → confirm results match SRS → sign off for FR-01" --phase 5 --project $REPO
  ```
- [ ] **[B-1]** Agent B (REVIEWER) for FR-01 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md acceptance criteria for FR-XX`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_RESULTS.md entry`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are REVIEWER. Your task: review the following deliverable for FR-01.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md acceptance criteria for FR-XX] ===
  {paste full content here}

  === [DOC 2: 03-development/src/…/fr_xx.py] ===
  {paste full content here}

  === [DOC 3: tests/…/test_fr_xx.py] ===
  {paste full content here}

  === [DOC 4: 04-testing/TEST_RESULTS.md entry] ===
  {paste full content here}

  Review checklist:
  - Acceptance criteria fully met?
  - No regressions in related FRs?

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
    --prompt "Review FR-01 against SRS + SAD" --phase 5 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-1: Gate 1 — FR-01
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P5): skip if FR-01 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- $(python3 -c "from scripts.generate_full_plan import _fr_source_paths; print(' '.join(_fr_source_paths('FR-01')))" 2>/dev/null || echo '.')
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-01:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 5 --fr-id FR-01 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-01 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-01:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 5 --fr-id FR-01
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p5-mid` / `p5-pre-ssi` / Gate exit.

#### FR-02: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-02
- [ ] Run integration tests for FR-02
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**A/B Work — FR-02** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVELOPER): Verify FR acceptance criteria → confirm results match SRS → sign off
  - Docstrings: `[FR-02]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-02 \
    --prompt "Verify FR acceptance criteria → confirm results match SRS → sign off for FR-02" --phase 5 --project $REPO
  ```
- [ ] **[B-1]** Agent B (REVIEWER) for FR-02 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md acceptance criteria for FR-XX`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_RESULTS.md entry`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are REVIEWER. Your task: review the following deliverable for FR-02.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md acceptance criteria for FR-XX] ===
  {paste full content here}

  === [DOC 2: 03-development/src/…/fr_xx.py] ===
  {paste full content here}

  === [DOC 3: tests/…/test_fr_xx.py] ===
  {paste full content here}

  === [DOC 4: 04-testing/TEST_RESULTS.md entry] ===
  {paste full content here}

  Review checklist:
  - Acceptance criteria fully met?
  - No regressions in related FRs?

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
    --prompt "Review FR-02 against SRS + SAD" --phase 5 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-2: Gate 1 — FR-02
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P5): skip if FR-02 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- $(python3 -c "from scripts.generate_full_plan import _fr_source_paths; print(' '.join(_fr_source_paths('FR-02')))" 2>/dev/null || echo '.')
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-02:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 5 --fr-id FR-02 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-02 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-02:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 5 --fr-id FR-02
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p5-mid` / `p5-pre-ssi` / Gate exit.

#### FR-03: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-03
- [ ] Run integration tests for FR-03
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**A/B Work — FR-03** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVELOPER): Verify FR acceptance criteria → confirm results match SRS → sign off
  - Docstrings: `[FR-03]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-03 \
    --prompt "Verify FR acceptance criteria → confirm results match SRS → sign off for FR-03" --phase 5 --project $REPO
  ```
- [ ] **[B-1]** Agent B (REVIEWER) for FR-03 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md acceptance criteria for FR-XX`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_RESULTS.md entry`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are REVIEWER. Your task: review the following deliverable for FR-03.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md acceptance criteria for FR-XX] ===
  {paste full content here}

  === [DOC 2: 03-development/src/…/fr_xx.py] ===
  {paste full content here}

  === [DOC 3: tests/…/test_fr_xx.py] ===
  {paste full content here}

  === [DOC 4: 04-testing/TEST_RESULTS.md entry] ===
  {paste full content here}

  Review checklist:
  - Acceptance criteria fully met?
  - No regressions in related FRs?

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
    --prompt "Review FR-03 against SRS + SAD" --phase 5 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-3: Gate 1 — FR-03
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P5): skip if FR-03 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- $(python3 -c "from scripts.generate_full_plan import _fr_source_paths; print(' '.join(_fr_source_paths('FR-03')))" 2>/dev/null || echo '.')
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-03:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 5 --fr-id FR-03 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-03 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-03:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 5 --fr-id FR-03
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p5-mid` / `p5-pre-ssi` / Gate exit.

#### FR-04: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-04
- [ ] Run integration tests for FR-04
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**A/B Work — FR-04** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVELOPER): Verify FR acceptance criteria → confirm results match SRS → sign off
  - Docstrings: `[FR-04]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-04 \
    --prompt "Verify FR acceptance criteria → confirm results match SRS → sign off for FR-04" --phase 5 --project $REPO
  ```
- [ ] **[B-1]** Agent B (REVIEWER) for FR-04 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md acceptance criteria for FR-XX`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_RESULTS.md entry`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are REVIEWER. Your task: review the following deliverable for FR-04.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md acceptance criteria for FR-XX] ===
  {paste full content here}

  === [DOC 2: 03-development/src/…/fr_xx.py] ===
  {paste full content here}

  === [DOC 3: tests/…/test_fr_xx.py] ===
  {paste full content here}

  === [DOC 4: 04-testing/TEST_RESULTS.md entry] ===
  {paste full content here}

  Review checklist:
  - Acceptance criteria fully met?
  - No regressions in related FRs?

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
    --prompt "Review FR-04 against SRS + SAD" --phase 5 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-4: Gate 1 — FR-04
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P5): skip if FR-04 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- $(python3 -c "from scripts.generate_full_plan import _fr_source_paths; print(' '.join(_fr_source_paths('FR-04')))" 2>/dev/null || echo '.')
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-04:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 5 --fr-id FR-04 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-04 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-04:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 5 --fr-id FR-04
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p5-mid` / `p5-pre-ssi` / Gate exit.

#### FR-05: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-05
- [ ] Run integration tests for FR-05
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**A/B Work — FR-05** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVELOPER): Verify FR acceptance criteria → confirm results match SRS → sign off
  - Docstrings: `[FR-05]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-05 \
    --prompt "Verify FR acceptance criteria → confirm results match SRS → sign off for FR-05" --phase 5 --project $REPO
  ```
- [ ] **[B-1]** Agent B (REVIEWER) for FR-05 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md acceptance criteria for FR-XX`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_RESULTS.md entry`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are REVIEWER. Your task: review the following deliverable for FR-05.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md acceptance criteria for FR-XX] ===
  {paste full content here}

  === [DOC 2: 03-development/src/…/fr_xx.py] ===
  {paste full content here}

  === [DOC 3: tests/…/test_fr_xx.py] ===
  {paste full content here}

  === [DOC 4: 04-testing/TEST_RESULTS.md entry] ===
  {paste full content here}

  Review checklist:
  - Acceptance criteria fully met?
  - No regressions in related FRs?

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
    --prompt "Review FR-05 against SRS + SAD" --phase 5 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-5: Gate 1 — FR-05
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P5): skip if FR-05 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- $(python3 -c "from scripts.generate_full_plan import _fr_source_paths; print(' '.join(_fr_source_paths('FR-05')))" 2>/dev/null || echo '.')
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-05:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 5 --fr-id FR-05 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-05 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-05:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 5 --fr-id FR-05
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p5-mid` / `p5-pre-ssi` / Gate exit.

#### FR-06: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-06
- [ ] Run integration tests for FR-06
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**A/B Work — FR-06** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVELOPER): Verify FR acceptance criteria → confirm results match SRS → sign off
  - Docstrings: `[FR-06]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-06 \
    --prompt "Verify FR acceptance criteria → confirm results match SRS → sign off for FR-06" --phase 5 --project $REPO
  ```
- [ ] **[B-1]** Agent B (REVIEWER) for FR-06 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md acceptance criteria for FR-XX`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_RESULTS.md entry`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are REVIEWER. Your task: review the following deliverable for FR-06.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md acceptance criteria for FR-XX] ===
  {paste full content here}

  === [DOC 2: 03-development/src/…/fr_xx.py] ===
  {paste full content here}

  === [DOC 3: tests/…/test_fr_xx.py] ===
  {paste full content here}

  === [DOC 4: 04-testing/TEST_RESULTS.md entry] ===
  {paste full content here}

  Review checklist:
  - Acceptance criteria fully met?
  - No regressions in related FRs?

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
    --prompt "Review FR-06 against SRS + SAD" --phase 5 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-6: Gate 1 — FR-06
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P5): skip if FR-06 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- $(python3 -c "from scripts.generate_full_plan import _fr_source_paths; print(' '.join(_fr_source_paths('FR-06')))" 2>/dev/null || echo '.')
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-06:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 5 --fr-id FR-06 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-06 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-06:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 5 --fr-id FR-06
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p5-mid` / `p5-pre-ssi` / Gate exit.

#### FR-07: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-07
- [ ] Run integration tests for FR-07
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**A/B Work — FR-07** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVELOPER): Verify FR acceptance criteria → confirm results match SRS → sign off
  - Docstrings: `[FR-07]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-07 \
    --prompt "Verify FR acceptance criteria → confirm results match SRS → sign off for FR-07" --phase 5 --project $REPO
  ```
- [ ] **[B-1]** Agent B (REVIEWER) for FR-07 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md acceptance criteria for FR-XX`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_RESULTS.md entry`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are REVIEWER. Your task: review the following deliverable for FR-07.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md acceptance criteria for FR-XX] ===
  {paste full content here}

  === [DOC 2: 03-development/src/…/fr_xx.py] ===
  {paste full content here}

  === [DOC 3: tests/…/test_fr_xx.py] ===
  {paste full content here}

  === [DOC 4: 04-testing/TEST_RESULTS.md entry] ===
  {paste full content here}

  Review checklist:
  - Acceptance criteria fully met?
  - No regressions in related FRs?

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
    --prompt "Review FR-07 against SRS + SAD" --phase 5 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-7: Gate 1 — FR-07
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P5): skip if FR-07 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- $(python3 -c "from scripts.generate_full_plan import _fr_source_paths; print(' '.join(_fr_source_paths('FR-07')))" 2>/dev/null || echo '.')
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-07:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 5 --fr-id FR-07 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-07 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-07:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 5 --fr-id FR-07
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p5-mid` / `p5-pre-ssi` / Gate exit.

#### FR-08: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-08
- [ ] Run integration tests for FR-08
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**A/B Work — FR-08** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVELOPER): Verify FR acceptance criteria → confirm results match SRS → sign off
  - Docstrings: `[FR-08]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-08 \
    --prompt "Verify FR acceptance criteria → confirm results match SRS → sign off for FR-08" --phase 5 --project $REPO
  ```
- [ ] **[B-1]** Agent B (REVIEWER) for FR-08 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md acceptance criteria for FR-XX`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_RESULTS.md entry`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are REVIEWER. Your task: review the following deliverable for FR-08.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md acceptance criteria for FR-XX] ===
  {paste full content here}

  === [DOC 2: 03-development/src/…/fr_xx.py] ===
  {paste full content here}

  === [DOC 3: tests/…/test_fr_xx.py] ===
  {paste full content here}

  === [DOC 4: 04-testing/TEST_RESULTS.md entry] ===
  {paste full content here}

  Review checklist:
  - Acceptance criteria fully met?
  - No regressions in related FRs?

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
    --prompt "Review FR-08 against SRS + SAD" --phase 5 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-8: Gate 1 — FR-08
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P5): skip if FR-08 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- $(python3 -c "from scripts.generate_full_plan import _fr_source_paths; print(' '.join(_fr_source_paths('FR-08')))" 2>/dev/null || echo '.')
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-08:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 5 --fr-id FR-08 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-08 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-08:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 5 --fr-id FR-08
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p5-mid` / `p5-pre-ssi` / Gate exit.

#### FR-09: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-09
- [ ] Run integration tests for FR-09
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**A/B Work — FR-09** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVELOPER): Verify FR acceptance criteria → confirm results match SRS → sign off
  - Docstrings: `[FR-09]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-09 \
    --prompt "Verify FR acceptance criteria → confirm results match SRS → sign off for FR-09" --phase 5 --project $REPO
  ```
- [ ] **[B-1]** Agent B (REVIEWER) for FR-09 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md acceptance criteria for FR-XX`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_RESULTS.md entry`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are REVIEWER. Your task: review the following deliverable for FR-09.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md acceptance criteria for FR-XX] ===
  {paste full content here}

  === [DOC 2: 03-development/src/…/fr_xx.py] ===
  {paste full content here}

  === [DOC 3: tests/…/test_fr_xx.py] ===
  {paste full content here}

  === [DOC 4: 04-testing/TEST_RESULTS.md entry] ===
  {paste full content here}

  Review checklist:
  - Acceptance criteria fully met?
  - No regressions in related FRs?

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
    --prompt "Review FR-09 against SRS + SAD" --phase 5 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-9: Gate 1 — FR-09
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P5): skip if FR-09 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- $(python3 -c "from scripts.generate_full_plan import _fr_source_paths; print(' '.join(_fr_source_paths('FR-09')))" 2>/dev/null || echo '.')
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-09:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 5 --fr-id FR-09 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-09 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-09:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 5 --fr-id FR-09
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p5-mid` / `p5-pre-ssi` / Gate exit.

#### FR-10: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-10
- [ ] Run integration tests for FR-10
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**A/B Work — FR-10** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVELOPER): Verify FR acceptance criteria → confirm results match SRS → sign off
  - Docstrings: `[FR-10]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-10 \
    --prompt "Verify FR acceptance criteria → confirm results match SRS → sign off for FR-10" --phase 5 --project $REPO
  ```
- [ ] **[B-1]** Agent B (REVIEWER) for FR-10 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md acceptance criteria for FR-XX`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_RESULTS.md entry`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are REVIEWER. Your task: review the following deliverable for FR-10.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md acceptance criteria for FR-XX] ===
  {paste full content here}

  === [DOC 2: 03-development/src/…/fr_xx.py] ===
  {paste full content here}

  === [DOC 3: tests/…/test_fr_xx.py] ===
  {paste full content here}

  === [DOC 4: 04-testing/TEST_RESULTS.md entry] ===
  {paste full content here}

  Review checklist:
  - Acceptance criteria fully met?
  - No regressions in related FRs?

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
    --prompt "Review FR-10 against SRS + SAD" --phase 5 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-10: Gate 1 — FR-10
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P5): skip if FR-10 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- $(python3 -c "from scripts.generate_full_plan import _fr_source_paths; print(' '.join(_fr_source_paths('FR-10')))" 2>/dev/null || echo '.')
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-10:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 5 --fr-id FR-10 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-10 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-10:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 5 --fr-id FR-10
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p5-mid` / `p5-pre-ssi` / Gate exit.

#### FR-11: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-11
- [ ] Run integration tests for FR-11
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**A/B Work — FR-11** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVELOPER): Verify FR acceptance criteria → confirm results match SRS → sign off
  - Docstrings: `[FR-11]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-11 \
    --prompt "Verify FR acceptance criteria → confirm results match SRS → sign off for FR-11" --phase 5 --project $REPO
  ```
- [ ] **[B-1]** Agent B (REVIEWER) for FR-11 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md acceptance criteria for FR-XX`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_RESULTS.md entry`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are REVIEWER. Your task: review the following deliverable for FR-11.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md acceptance criteria for FR-XX] ===
  {paste full content here}

  === [DOC 2: 03-development/src/…/fr_xx.py] ===
  {paste full content here}

  === [DOC 3: tests/…/test_fr_xx.py] ===
  {paste full content here}

  === [DOC 4: 04-testing/TEST_RESULTS.md entry] ===
  {paste full content here}

  Review checklist:
  - Acceptance criteria fully met?
  - No regressions in related FRs?

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
    --prompt "Review FR-11 against SRS + SAD" --phase 5 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-11: Gate 1 — FR-11
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P5): skip if FR-11 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- $(python3 -c "from scripts.generate_full_plan import _fr_source_paths; print(' '.join(_fr_source_paths('FR-11')))" 2>/dev/null || echo '.')
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-11:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 5 --fr-id FR-11 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-11 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-11:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 5 --fr-id FR-11
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p5-mid` / `p5-pre-ssi` / Gate exit.

#### FR-12: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-12
- [ ] Run integration tests for FR-12
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**A/B Work — FR-12** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVELOPER): Verify FR acceptance criteria → confirm results match SRS → sign off
  - Docstrings: `[FR-12]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-12 \
    --prompt "Verify FR acceptance criteria → confirm results match SRS → sign off for FR-12" --phase 5 --project $REPO
  ```
- [ ] **[B-1]** Agent B (REVIEWER) for FR-12 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md acceptance criteria for FR-XX`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_RESULTS.md entry`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are REVIEWER. Your task: review the following deliverable for FR-12.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md acceptance criteria for FR-XX] ===
  {paste full content here}

  === [DOC 2: 03-development/src/…/fr_xx.py] ===
  {paste full content here}

  === [DOC 3: tests/…/test_fr_xx.py] ===
  {paste full content here}

  === [DOC 4: 04-testing/TEST_RESULTS.md entry] ===
  {paste full content here}

  Review checklist:
  - Acceptance criteria fully met?
  - No regressions in related FRs?

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
    --prompt "Review FR-12 against SRS + SAD" --phase 5 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-12: Gate 1 — FR-12
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P5): skip if FR-12 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- $(python3 -c "from scripts.generate_full_plan import _fr_source_paths; print(' '.join(_fr_source_paths('FR-12')))" 2>/dev/null || echo '.')
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-12:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 5 --fr-id FR-12 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-12 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-12:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 5 --fr-id FR-12
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p5-mid` / `p5-pre-ssi` / Gate exit.

#### FR-13: Verification
- [ ] Confirm all acceptance criteria from SRS.md are met for FR-13
- [ ] Run integration tests for FR-13
- [ ] Verify edge cases and error paths
- [ ] Confirm ≥80% branch coverage

**A/B Work — FR-13** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (DEVELOPER): Verify FR acceptance criteria → confirm results match SRS → sign off
  - Docstrings: `[FR-13]` tag + `Citations:` with line numbers (HR-15)
  - FORBIDDEN: `app/infrastructure/` · `@covers: L1 Error` · `@type: edge`
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[A-DISPATCH]** Dispatch Agent A:
  ```bash
  python3 harness_cli.py dispatch --role developer --fr-id FR-13 \
    --prompt "Verify FR acceptance criteria → confirm results match SRS → sign off for FR-13" --phase 5 --project $REPO
  ```
- [ ] **[B-1]** Agent B (REVIEWER) for FR-13 — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md acceptance criteria for FR-XX`
  - `03-development/src/…/fr_xx.py`
  - `tests/…/test_fr_xx.py`
  - `04-testing/TEST_RESULTS.md entry`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are REVIEWER. Your task: review the following deliverable for FR-13.
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md acceptance criteria for FR-XX] ===
  {paste full content here}

  === [DOC 2: 03-development/src/…/fr_xx.py] ===
  {paste full content here}

  === [DOC 3: tests/…/test_fr_xx.py] ===
  {paste full content here}

  === [DOC 4: 04-testing/TEST_RESULTS.md entry] ===
  {paste full content here}

  Review checklist:
  - Acceptance criteria fully met?
  - No regressions in related FRs?

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
    --prompt "Review FR-13 against SRS + SAD" --phase 5 --project $REPO
  ```
  > AgentSpawner auto-logs to `sessions_spawn.log` on dispatch (HR-10).


### 🔒 CHECKPOINT-13: Gate 1 — FR-13
> Dimensions: linting(90) · type_safety(85) · test_coverage(80)
> `gate1_result.json` is overwritten each FR — `finalize-gate` reads it immediately.


> **Delta-check mode** (P5): skip if FR-13 code unchanged since last Gate 1.
- [ ] **[DELTA-CHECK]** Check if FR code changed since last Gate 1:
  ```bash
  git diff --quiet HEAD -- $(python3 -c "from scripts.generate_full_plan import _fr_source_paths; print(' '.join(_fr_source_paths('FR-13')))" 2>/dev/null || echo '.')
  ```
  - Exit 0 (no changes) → skip G1a-G1c, re-use previous Gate 1 score from manifest
  - Exit 1 (changes detected) → proceed to full re-evaluation below

- [ ] **G1a** Prepare Gate 1 for FR-13:
  ```bash
  python3 harness_cli.py run-gate --gate 1 --phase 5 --fr-id FR-13 --delta
  ```
  Read the evaluation prompt printed above.

- [ ] **G1b** Evaluate all Gate 1 dimensions for FR-13 inline:
  - Follow `harness/ssi/prompts/evaluate_dimension.md`
  - Write result to `.sessi-work/gate1_result.json`
  - Schema: `harness/ssi/schemas/harness_gate_result.schema.json`

- [ ] **G1c** Finalize Gate 1 for FR-13:
  ```bash
  python3 harness_cli.py finalize-gate --gate 1 --phase 5 --fr-id FR-13
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
  > Push + HANDOVER.md happens at milestone: `push-milestone --type p5-mid` / `p5-pre-ssi` / Gate exit.

- [ ] Integration tests pass
- [ ] Performance tests meet targets
- [ ] Security scan passes
- [ ] Baseline established

### P5 Milestone Push (10-Push Strategy ⑦)

- [ ] **PUSH ⑦ — P5-baseline** (after BASELINE.md is generated):
  ```bash
  python3 harness_cli.py push-milestone --type p5-baseline --project .
  ```
  > Writes HANDOVER.md + commits + pushes.

### Phase 5 Deliverables
- [ ] `BASELINE.md` - System baseline
- [ ] `VERIFICATION_REPORT.md` - Verification report
- [x] `sessions_spawn.log` — auto-populated by AgentSpawner (HR-10)
- [ ] Gate 1 PASS for every FR

#### ASPICE Traceability Requirements (enforced by postflight)

- [ ] **[ASPICE]** Artifact for Phase 5 MUST reference `04-testing/TEST_PLAN.md` by filename keyword `TEST_PLAN` (ASPICE traceability — `postflight_artifact_links()` enforces this)
- [ ] **[ASPICE]** Artifact for Phase 5 MUST reference `04-testing/TEST_RESULTS.md` by filename keyword `TEST_RESULTS` (ASPICE traceability — `postflight_artifact_links()` enforces this)


### Phase 5 → Phase 6: Quality Assurance

- [ ] Confirm ALL checkpoints in this plan are ✓  (no skips — HR-03)
- [ ] Generate Phase 6 plan:
  ```bash
  python3 harness_cli.py plan-phase --phase 6 --project $REPO \
    --output $REPO/.methodology/phase6_plan.md
  ```
- [ ] Advance FSM to Phase 6 (writes new HANDOVER.md + local commit):
  ```bash
  python3 harness_cli.py advance-phase --completed 5 --project .
  ```
- [ ] Confirm `HANDOVER.md` reflects Phase 6 entry (`P6-entry` checkpoint, correct plan path)
- [ ] Open `phase6_plan.md` and follow from the top.
- [ ] If session crashes during Phase 6: read `HANDOVER.md` or run `generate-next-plan`
