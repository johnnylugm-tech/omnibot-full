# Phase 1 Full Execution Plan -- omnibot-full

> **Version**: v2.3.0 (project plan)
> **Project**: omnibot-full
> **Date**: 2026-05-13
> **Framework**: harness-methodology v2.3.0
> **Phase**: 1 - Requirements Specification
> **Status**: Full version (including Phase 1 detailed tasks)

---

## Phase 1 Tasks: Requirements Specification

### Phase 1 Overview
Phase 1 is the project starting point. Define complete SRS.
**Exit gate = human peer review of deliverables** (not `harness run-gate --gate 1`).

> **Crash Recovery**: after each push, `HANDOVER.md` is written to project root.
> If context is lost, read `HANDOVER.md` first — it contains phase, status, and next steps.

> **Checkpoint Index** (push to GitHub = checkpoint + HANDOVER.md saved):
> - CHECKPOINT-1: Human Peer Review (Phase 1 Exit) → `push-checkpoint --phase 1`

### Pre-Phase Preflight

- [ ] **[PREFLIGHT]** Run phase hooks (FSM, Constitution, Kill-Switch, Drift, CI Readiness):
  ```bash
  python3 harness_cli.py run-phase --phase 1 --project $REPO
  ```
  If FAILED non-critically: use `--force`. If BLOCKED: fix FSM/Constitution first.

- [ ] **[PREFLIGHT-CI]** ⛔ HARD STOP if any item below is missing — complete SKILL.md §0.1 Step 0 first:
  1. `git config quality.phase` returns `1`  ← set by `init-project`
  2. `.github/workflows/harness_quality_gate.yml` exists in project root  ← set by `init-project`
  3. Git hooks installed (`ls .git/hooks/prepare-commit-msg`)  ← set by `init-project`
  4. GitHub repo variable `CURRENT_PHASE = 1` (Settings → Variables)  ← optional (fallback '1')
  5. `HERMES_REVIEWER_TARGET` exported in shell  ← required
  If any required item (1-3, 5) is missing: stop, run `python3 harness_cli.py init-project --phase 1 --project $REPO`, then set manual items.

### Task Decomposition (Dependency Analysis)

**Phase 1 has 4 deliverables with sequential dependencies:**

| Order | Deliverable | Depends On | Agent A | Agent B |
|-------|------------|------------|---------|---------|
| 1 | `SRS.md` | (none — starting point) | REQUIREMENTS_ENGINEER | BUSINESS_ANALYST |
| 2 | `CONSTRAINTS.md` | SRS.md | REQUIREMENTS_ENGINEER | BUSINESS_ANALYST |
| 3 | `SPEC_TRACKING.md` | SRS.md | REQUIREMENTS_ENGINEER | BUSINESS_ANALYST |
| 4 | `TRACEABILITY_MATRIX.md` | SRS.md, SPEC_TRACKING.md | REQUIREMENTS_ENGINEER | BUSINESS_ANALYST |

**Execution rule**: Each deliverable must pass Agent B review BEFORE starting the next.
If a deliverable is REJECTED, fix only that deliverable — earlier APPROVED deliverables
are not re-opened. This bounds backtracking to a single step.

### Requirements Authoring (Serial A/B per Deliverable)

### Sub-Task 1/4: SRS.md — Software Requirements Specification — functional + non-functional requirements

**Depends on**: none — starting point
**Agent A**: REQUIREMENTS_ENGINEER
**Agent B**: BUSINESS_ANALYST

**A/B Work** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (REQUIREMENTS_ENGINEER): Elicit requirements → write FRs/NFRs in SRS.md (### FR-XX: format) → validate completeness
  - FORBIDDEN: vague/non-testable acceptance criteria
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[B-1]** Agent B (BUSINESS_ANALYST) — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read docs/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `Project description / stakeholder brief`
  - `draft docs/SRS.md (full content)`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are BUSINESS_ANALYST. Your task: review the following deliverable (SRS.md).
  You have NO access to any files — all context is provided below.

  === [DOC 1: Project description / stakeholder brief] ===
  {paste full content here}

  === [DOC 2: draft docs/SRS.md (full content)] ===
  {paste full content here}

  Review checklist:
  - All FRs testable? (no vague criteria)
  - NFRs measurable?
  - No contradictions between FRs?
  - Every stakeholder need covered?

  Return JSON only:
  {"status":"STAGE_PASS"|"REJECT","review_status":"APPROVE"|"REJECT",
   "reason":"...","confidence":1-10,"citations":["file:line"],"gaps":[...]}
  ```

- [ ] **[B-2]** Agent B returns JSON — parse `review_status`:
  - `APPROVE` → continue to Sub-Task 2/4
  - `REJECT` → Agent A fixes gaps → re-dispatch B. Max 5 rounds (HR-12).

- [ ] **[LOG]** Append to `sessions_spawn.log` (HR-10 — 2 entries per sub-task):
  ```json
  {"fr_id":"P1","sub_task":"SRS.md","role":"requirements_engineer","session_id":"dev-XXXX","status":"success","confidence":8}
  {"fr_id":"P1","sub_task":"SRS.md","role":"business_analyst","session_id":"rev-XXXX","review_status":"APPROVE"}
  ```
  > fr_id uses P1 as phase-level placeholder; replace with FR-XX for FR-specific plans.

### Sub-Task 2/4: CONSTRAINTS.md — Technical Constraints — technology stack, SLA targets, cost model, regulatory requirements

**Depends on**: SRS.md (+ Sub-Task 1/4 review: previous review gaps carry forward)
**Agent A**: REQUIREMENTS_ENGINEER
**Agent B**: BUSINESS_ANALYST

**A/B Work** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (REQUIREMENTS_ENGINEER): Analyze constraints from SRS → document tech stack, SLA, cost model, compliance → validate completeness
  - FORBIDDEN: vague/non-testable acceptance criteria
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[B-1]** Agent B (BUSINESS_ANALYST) — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read docs/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `Previous Sub-Task B-2 review JSON — SRS.md (Sub-Task 1/4, gaps field may contain non-blocking caveats)`
  - `docs/SRS.md (APPROVED — full content)`
  - `draft docs/CONSTRAINTS.md (full content)`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are BUSINESS_ANALYST. Your task: review the following deliverable (CONSTRAINTS.md).
  You have NO access to any files — all context is provided below.

  === [DOC 1: Previous Sub-Task B-2 review JSON — SRS.md (Sub-Task 1/4, gaps field may contain non-blocking caveats)] ===
  {paste full content here}

  === [DOC 2: docs/SRS.md (APPROVED — full content)] ===
  {paste full content here}

  === [DOC 3: draft docs/CONSTRAINTS.md (full content)] ===
  {paste full content here}

  Review checklist:
  - Upstream deliverable review caveats addressed? (check previous B-2 gaps field)
  - All technical constraints documented?
  - SLA targets defined and measurable?
  - Cost model complete?
  - Constraints consistent with SRS requirements?

  Return JSON only:
  {"status":"STAGE_PASS"|"REJECT","review_status":"APPROVE"|"REJECT",
   "reason":"...","confidence":1-10,"citations":["file:line"],"gaps":[...]}
  ```

- [ ] **[B-2]** Agent B returns JSON — parse `review_status`:
  - `APPROVE` → continue to Sub-Task 3/4
  - `REJECT` → Agent A fixes gaps → re-dispatch B. Max 5 rounds (HR-12).

- [ ] **[LOG]** Append to `sessions_spawn.log` (HR-10 — 2 entries per sub-task):
  ```json
  {"fr_id":"P1","sub_task":"CONSTRAINTS.md","role":"requirements_engineer","session_id":"dev-XXXX","status":"success","confidence":8}
  {"fr_id":"P1","sub_task":"CONSTRAINTS.md","role":"business_analyst","session_id":"rev-XXXX","review_status":"APPROVE"}
  ```
  > fr_id uses P1 as phase-level placeholder; replace with FR-XX for FR-specific plans.

### Sub-Task 3/4: SPEC_TRACKING.md — Spec Tracking Matrix — maps every FR to its current status, owner, and acceptance state

**Depends on**: SRS.md (+ Sub-Task 1/4 review: previous review gaps carry forward)
**Agent A**: REQUIREMENTS_ENGINEER
**Agent B**: BUSINESS_ANALYST

**A/B Work** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (REQUIREMENTS_ENGINEER): Build spec tracking matrix from SRS.md FRs → assign status/owner per FR → validate completeness
  - FORBIDDEN: vague/non-testable acceptance criteria
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[B-1]** Agent B (BUSINESS_ANALYST) — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read docs/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `Previous Sub-Task B-2 review JSON — SRS.md (Sub-Task 1/4, gaps field may contain non-blocking caveats)`
  - `docs/SRS.md (APPROVED — full content)`
  - `draft docs/SPEC_TRACKING.md (full content)`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are BUSINESS_ANALYST. Your task: review the following deliverable (SPEC_TRACKING.md).
  You have NO access to any files — all context is provided below.

  === [DOC 1: Previous Sub-Task B-2 review JSON — SRS.md (Sub-Task 1/4, gaps field may contain non-blocking caveats)] ===
  {paste full content here}

  === [DOC 2: docs/SRS.md (APPROVED — full content)] ===
  {paste full content here}

  === [DOC 3: draft docs/SPEC_TRACKING.md (full content)] ===
  {paste full content here}

  Review checklist:
  - Upstream deliverable review caveats addressed? (check previous B-2 gaps field)
  - Every FR from SRS.md listed?
  - Status field populated per FR?
  - Owner assigned per FR?
  - No orphan FRs (in SRS but not tracked)?

  Return JSON only:
  {"status":"STAGE_PASS"|"REJECT","review_status":"APPROVE"|"REJECT",
   "reason":"...","confidence":1-10,"citations":["file:line"],"gaps":[...]}
  ```

- [ ] **[B-2]** Agent B returns JSON — parse `review_status`:
  - `APPROVE` → continue to Sub-Task 4/4
  - `REJECT` → Agent A fixes gaps → re-dispatch B. Max 5 rounds (HR-12).

- [ ] **[LOG]** Append to `sessions_spawn.log` (HR-10 — 2 entries per sub-task):
  ```json
  {"fr_id":"P1","sub_task":"SPEC_TRACKING.md","role":"requirements_engineer","session_id":"dev-XXXX","status":"success","confidence":8}
  {"fr_id":"P1","sub_task":"SPEC_TRACKING.md","role":"business_analyst","session_id":"rev-XXXX","review_status":"APPROVE"}
  ```
  > fr_id uses P1 as phase-level placeholder; replace with FR-XX for FR-specific plans.

### Sub-Task 4/4: TRACEABILITY_MATRIX.md — Requirements Traceability Matrix — bidirectional traceability from FRs through design to tests

**Depends on**: SRS.md, SPEC_TRACKING.md (+ Sub-Task 1/4, 3/4 review: previous review gaps carry forward)
**Agent A**: REQUIREMENTS_ENGINEER
**Agent B**: BUSINESS_ANALYST

**A/B Work** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (REQUIREMENTS_ENGINEER): Build bidirectional traceability matrix → link FRs → design elements → test cases → validate coverage
  - FORBIDDEN: vague/non-testable acceptance criteria
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[B-1]** Agent B (BUSINESS_ANALYST) — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read docs/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `Previous Sub-Task B-2 review JSON — SRS.md (Sub-Task 1/4, gaps field may contain non-blocking caveats)`
  - `Previous Sub-Task B-2 review JSON — SPEC_TRACKING.md (Sub-Task 3/4, gaps field may contain non-blocking caveats)`
  - `docs/SRS.md (APPROVED — full content)`
  - `docs/SPEC_TRACKING.md (APPROVED — full content)`
  - `draft docs/TRACEABILITY_MATRIX.md (full content)`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are BUSINESS_ANALYST. Your task: review the following deliverable (TRACEABILITY_MATRIX.md).
  You have NO access to any files — all context is provided below.

  === [DOC 1: Previous Sub-Task B-2 review JSON — SRS.md (Sub-Task 1/4, gaps field may contain non-blocking caveats)] ===
  {paste full content here}

  === [DOC 2: Previous Sub-Task B-2 review JSON — SPEC_TRACKING.md (Sub-Task 3/4, gaps field may contain non-blocking caveats)] ===
  {paste full content here}

  === [DOC 3: docs/SRS.md (APPROVED — full content)] ===
  {paste full content here}

  === [DOC 4: docs/SPEC_TRACKING.md (APPROVED — full content)] ===
  {paste full content here}

  === [DOC 5: draft docs/TRACEABILITY_MATRIX.md (full content)] ===
  {paste full content here}

  Review checklist:
  - Upstream deliverable review caveats addressed? (check previous B-2 gaps field)
  - Bidirectional traceability established? (FR→design→test and back)
  - Every FR has ≥1 downstream link?
  - No orphan requirements?
  - Coverage complete (all FRs traceable)?
  - All upstream deliverables consistent with each other? No contradictory decisions?

  Return JSON only:
  {"status":"STAGE_PASS"|"REJECT","review_status":"APPROVE"|"REJECT",
   "reason":"...","confidence":1-10,"citations":["file:line"],"gaps":[...]}
  ```

- [ ] **[B-2]** Agent B returns JSON — parse `review_status`:
  - `APPROVE` → all deliverables complete; proceed to Human Peer Review
  - `REJECT` → Agent A fixes gaps → re-dispatch B. Max 5 rounds (HR-12).

- [ ] **[LOG]** Append to `sessions_spawn.log` (HR-10 — 2 entries per sub-task):
  ```json
  {"fr_id":"P1","sub_task":"TRACEABILITY_MATRIX.md","role":"requirements_engineer","session_id":"dev-XXXX","status":"success","confidence":8}
  {"fr_id":"P1","sub_task":"TRACEABILITY_MATRIX.md","role":"business_analyst","session_id":"rev-XXXX","review_status":"APPROVE"}
  ```
  > fr_id uses P1 as phase-level placeholder; replace with FR-XX for FR-specific plans.

### Phase 1 Deliverables
- [ ] `SRS.md` - Software Requirements Specification (FRs + NFRs)
- [ ] `CONSTRAINTS.md` - Technical constraints, SLA, cost model
- [ ] `SPEC_TRACKING.md` - Spec tracking matrix
- [ ] `TRACEABILITY_MATRIX.md` - Requirements traceability matrix
- [ ] `sessions_spawn.log` - 4 sub-tasks × 2 entries = 8 entries for P1 A/B work (HR-10)


### 🔒 CHECKPOINT-1: Human Peer Review — Phase 1 Exit
> Phase 1/2 exit gate = human document review (NOT `harness run-gate --gate 1`).
> APPROVE criteria: all FRs addressed, no critical gaps, terminology consistent.

- [ ] **[HR-READ]** Reviewer reads all deliverables:
  - `SRS.md`
  - `CONSTRAINTS.md`
  - `SPEC_TRACKING.md`
  - `TRACEABILITY_MATRIX.md`
  - Checklist: All FRs covered? No contradictions? Each item testable/traceable?
- [ ] **[HR-DECIDE]** Reviewer records decision:
  ```json
  {"phase": 1, "reviewer": "XXXX", "status": "APPROVE", "reason": "..."}
  ```
  - If REJECT → author fixes → re-review. Max 5 rounds (HR-12).
- [ ] **[HR-PUSH]** ✅ Push to GitHub + HANDOVER.md (CHECKPOINT-1 saved):
  ```bash
  python3 harness_cli.py push-checkpoint --phase 1 --project . \
    --fr-ids FR-01,FR-02,FR-03
  ```
  > This writes `HANDOVER.md` (crash-recovery checkpoint) to project root,
  > then commits + pushes all changes to origin.
  > After a crash, read HANDOVER.md first — it tells you where you were.

### Phase 1 → Phase 2: Architecture Design

- [ ] Confirm ALL checkpoints in this plan are ✓  (no skips — HR-03)
- [ ] Verify `HANDOVER.md` exists at project root (written by `push-checkpoint`)
- [ ] Generate Phase 2 plan:
  ```bash
  python3 harness_cli.py plan-phase --phase 2 --project $REPO \
    --output $REPO/.methodology/phase2_plan.md
  ```
- [ ] Open `phase2_plan.md` and follow from the top.
- [ ] If session crashes during Phase 2: read `HANDOVER.md` or run `generate-next-plan`
