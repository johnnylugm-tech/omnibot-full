# Phase 1 Full Execution Plan -- omnibot-full

> **Version**: v2.3.0 (project plan)
> **Project**: omnibot-full
> **Date**: 2026-05-16
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
  If FAILED: fix FSM/Constitution issues. There is no gate bypass flag.

- [ ] **[PREFLIGHT-CI]** ⛔ HARD STOP if any item below is missing — complete SKILL.md §0.1 Step 0 first:
  1. `git config quality.phase` returns `1`  ← set by `init-project`
  2. `.github/workflows/harness_quality_gate.yml` exists in project root  ← set by `init-project`
  3. Git hooks installed (`ls .git/hooks/prepare-commit-msg`)  ← set by `init-project`
  4. GitHub repo variable `CURRENT_PHASE = 1` (Settings → Variables)  ← optional (fallback '1')
  5. `HERMES_REVIEWER_TARGET` exported in shell  ← required
  If any required item (1-3, 5) is missing: stop, run `python3 harness_cli.py init-project --phase 1 --project $REPO`, then set manual items.

### Task Decomposition (Dependency Analysis)

**Phase 1 has 3 deliverables with sequential dependencies:**

| Order | Deliverable | Depends On | Agent A | Agent B |
|-------|------------|------------|---------|---------|
| 1 | `SRS.md` | (none — starting point) | REQUIREMENTS_ENGINEER | BUSINESS_ANALYST |
| 2 | `SPEC_TRACKING.md` | SRS.md | REQUIREMENTS_ENGINEER | BUSINESS_ANALYST |
| 3 | `TRACEABILITY_MATRIX.md` | SRS.md, SPEC_TRACKING.md | REQUIREMENTS_ENGINEER | BUSINESS_ANALYST |

**Execution rule**: Each deliverable must pass Agent B review BEFORE starting the next.
If a deliverable is REJECTED, fix only that deliverable — earlier APPROVED deliverables
are not re-opened. This bounds backtracking to a single step.

### Requirements Authoring (Serial A/B per Deliverable)

### Sub-Task 1/3: SRS.md — Software Requirements Specification — functional + non-functional requirements

**Depends on**: none — starting point
**Agent A**: REQUIREMENTS_ENGINEER
**Agent B**: BUSINESS_ANALYST

**A/B Work** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (REQUIREMENTS_ENGINEER): Elicit requirements → write FRs/NFRs in SRS.md (### FR-XX: format) → validate completeness
  - FORBIDDEN: vague/non-testable acceptance criteria
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[B-1]** Agent B (BUSINESS_ANALYST) — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `Project description / stakeholder brief`
  - `draft 01-requirements/SRS.md (full content)`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are BUSINESS_ANALYST. Your task: review the following deliverable (SRS.md).
  You have NO access to any files — all context is provided below.

  === [DOC 1: Project description / stakeholder brief] ===
  {paste full content here}

  === [DOC 2: draft 01-requirements/SRS.md (full content)] ===
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

- [ ] **[B-2]** Agent B returns JSON — parse `review_status` **AND** `gaps` severity:
  - `APPROVE` + all gaps are `low` → continue to Sub-Task 2/3
  - `APPROVE` + any gap is `medium` or `high` → fix gaps → **re-dispatch B as round 2**
    (embed same docs as B-1 above, replacing `SRS.md` with its updated content)
    → continue to Sub-Task 2/3 only after round-2 APPROVE
  - `REJECT` → Agent A fixes gaps → re-dispatch B. Max 5 rounds (HR-12).

  > ⚠️ **BLOCKING**: Do NOT start the next Sub-Task until this sub-task's current
  > round is fully APPROVED (including any required round 2).
  > AgentSpawner auto-logs round-2 re-dispatch to `sessions_spawn.log` (HR-10).

  > fr_id uses P1 as phase-level placeholder; replace with FR-XX for FR-specific plans.

### Sub-Task 2/3: SPEC_TRACKING.md — Spec Tracking Matrix — maps every FR to its current status, owner, and acceptance state

**Depends on**: SRS.md (+ Sub-Task 1/3 review: previous review gaps carry forward)
**Agent A**: REQUIREMENTS_ENGINEER
**Agent B**: BUSINESS_ANALYST

**A/B Work** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (REQUIREMENTS_ENGINEER): Build spec tracking matrix from SRS.md FRs → assign status/owner per FR → validate completeness
  - FORBIDDEN: vague/non-testable acceptance criteria
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[B-1]** Agent B (BUSINESS_ANALYST) — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `Previous Sub-Task B-2 review JSON — SRS.md (Sub-Task 1/3, gaps field may contain non-blocking caveats)`
  - `01-requirements/SRS.md (APPROVED — full content)`
  - `draft 01-requirements/SPEC_TRACKING.md (full content)`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are BUSINESS_ANALYST. Your task: review the following deliverable (SPEC_TRACKING.md).
  You have NO access to any files — all context is provided below.

  === [DOC 1: Previous Sub-Task B-2 review JSON — SRS.md (Sub-Task 1/3, gaps field may contain non-blocking caveats)] ===
  {paste full content here}

  === [DOC 2: 01-requirements/SRS.md (APPROVED — full content)] ===
  {paste full content here}

  === [DOC 3: draft 01-requirements/SPEC_TRACKING.md (full content)] ===
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

- [ ] **[B-2]** Agent B returns JSON — parse `review_status` **AND** `gaps` severity:
  - `APPROVE` + all gaps are `low` → continue to Sub-Task 3/3
  - `APPROVE` + any gap is `medium` or `high` → fix gaps → **re-dispatch B as round 2**
    (embed same docs as B-1 above, replacing `SPEC_TRACKING.md` with its updated content)
    → continue to Sub-Task 3/3 only after round-2 APPROVE
  - `REJECT` → Agent A fixes gaps → re-dispatch B. Max 5 rounds (HR-12).

  > ⚠️ **BLOCKING**: Do NOT start the next Sub-Task until this sub-task's current
  > round is fully APPROVED (including any required round 2).
  > AgentSpawner auto-logs round-2 re-dispatch to `sessions_spawn.log` (HR-10).

  > fr_id uses P1 as phase-level placeholder; replace with FR-XX for FR-specific plans.

### Sub-Task 3/3: TRACEABILITY_MATRIX.md — Requirements Traceability Matrix — bidirectional traceability from FRs through design to tests

**Depends on**: SRS.md, SPEC_TRACKING.md (+ Sub-Task 1/3, 2/3 review: previous review gaps carry forward)
**Agent A**: REQUIREMENTS_ENGINEER
**Agent B**: BUSINESS_ANALYST

**A/B Work** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (REQUIREMENTS_ENGINEER): Build bidirectional traceability matrix → link FRs → design elements → test cases → validate coverage
  - FORBIDDEN: vague/non-testable acceptance criteria
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[B-1]** Agent B (BUSINESS_ANALYST) — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `Previous Sub-Task B-2 review JSON — SRS.md (Sub-Task 1/3, gaps field may contain non-blocking caveats)`
  - `Previous Sub-Task B-2 review JSON — SPEC_TRACKING.md (Sub-Task 2/3, gaps field may contain non-blocking caveats)`
  - `01-requirements/SRS.md (APPROVED — full content)`
  - `01-requirements/SPEC_TRACKING.md (APPROVED — full content)`
  - `draft 01-requirements/TRACEABILITY_MATRIX.md (full content)`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are BUSINESS_ANALYST. Your task: review the following deliverable (TRACEABILITY_MATRIX.md).
  You have NO access to any files — all context is provided below.

  === [DOC 1: Previous Sub-Task B-2 review JSON — SRS.md (Sub-Task 1/3, gaps field may contain non-blocking caveats)] ===
  {paste full content here}

  === [DOC 2: Previous Sub-Task B-2 review JSON — SPEC_TRACKING.md (Sub-Task 2/3, gaps field may contain non-blocking caveats)] ===
  {paste full content here}

  === [DOC 3: 01-requirements/SRS.md (APPROVED — full content)] ===
  {paste full content here}

  === [DOC 4: 01-requirements/SPEC_TRACKING.md (APPROVED — full content)] ===
  {paste full content here}

  === [DOC 5: draft 01-requirements/TRACEABILITY_MATRIX.md (full content)] ===
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

- [ ] **[B-2]** Agent B returns JSON — parse `review_status` **AND** `gaps` severity:
  - `APPROVE` + all gaps are `low` → all deliverables complete; proceed to Human Peer Review
  - `APPROVE` + any gap is `medium` or `high` → fix gaps → **re-dispatch B as round 2**
    (embed same docs as B-1 above, replacing `TRACEABILITY_MATRIX.md` with its updated content)
    → all deliverables complete; proceed to Human Peer Review only after round-2 APPROVE
  - `REJECT` → Agent A fixes gaps → re-dispatch B. Max 5 rounds (HR-12).

  > ⚠️ **BLOCKING**: Do NOT start the next Sub-Task until this sub-task's current
  > round is fully APPROVED (including any required round 2).
  > AgentSpawner auto-logs round-2 re-dispatch to `sessions_spawn.log` (HR-10).

  > fr_id uses P1 as phase-level placeholder; replace with FR-XX for FR-specific plans.

### FR Requirements (13 total)

#### FR-01: Platform Adapter — Telegram + LINE Webhook
**Task**: 系統必須接收來自 Telegram Bot API 和 LINE Messaging API 的 webhook 請求，轉換為內部統一消息格式（UnifiedMessage）。

#### FR-02: Webhook Signature Verification
**Task**: 每個 webhook 請求必須先通過簽名驗證，未通過者拒絕處理。

#### FR-03: Unified Message Format
**Task**: 所有平台消息必須轉換為統一的 `UnifiedMessage` dataclass，對下游模組隱藏平台差異。

#### FR-04: Input Sanitizer L2 — Character Normalization
**Task**: 所有使用者輸入文字必須經過 NFKC 正規化，移除非列印控制字元。

#### FR-05: PII Masking L4 — Phone / Email / Address
**Task**: 使用者訊息中的台灣電話、Email、地址必須在記錄或輸出前遮蔽。敏感關鍵字觸發轉接。

#### FR-06: Rate Limiter — Token Bucket
**Task**: 每個平台用戶必須有獨立的請求速率限制，防止濫用。

#### FR-07: Knowledge Layer V1 — Rule Match + Escalate
**Task**: 查詢知識庫時先執行 SQL 精確/模糊匹配（Layer 1），信心度 > 0.7 直接回覆，否則轉接人工。

#### FR-08: Basic Escalation Manager — No SLA
**Task**: 無法匹配的查詢必須進入轉接佇列，支援指派與結案。

#### FR-09: Structured Logger — JSON Format
**Task**: 所有日誌必須以 JSON 結構化格式輸出，包含 timestamp / level / service / message。

#### FR-10: API Response Format — ApiResponse / PaginatedResponse
**Task**: 所有 API 回應必須使用統一的 `ApiResponse[T]` 或 `PaginatedResponse[T]` 泛型格式。

#### FR-11: Health Check Endpoint
**Task**: 系統必須提供健康檢查端點供 Docker / 監控系統使用。

#### FR-12: Database Schema — All Core Tables
**Task**: 必須建立所有核心資料表，包含 Phase 2/3 預留欄位，避免後續 ALTER TABLE。

#### FR-13: Docker Compose Development Environment
**Task**: 提供一鍵啟動的開發環境，包含 API、PostgreSQL (pgvector)、Redis。

### NFR Non-Functional Requirements (6 total)

#### NFR-01: NFR-01: First Contact Resolution (FCR) >= 50%
**Requirement**: **Category**: Performance
**Description**: 以 30 天滾動窗口計算，in_scope 對話中 `first_contact_resolution = TRUE` 的比例需 >= 50%。
**Measurement**: ODD SQL 查詢 (SPEC/omnibot-phase-1.md L811-L822)

#### NFR-02: NFR-02: p95 Response Latency < 3.0s
**Requirement**: **Category**: Performance
**Description**: 從 webhook 接收到回覆發送之間，p95 延遲 < 3.0 秒。以 platform 分組計算。
**Measurement**: ODD SQL 查詢 (SPEC/omnibot-phase-1.md L824-L832)

#### NFR-03: NFR-03: Platform Support — Telegram + LINE
**Requirement**: **Category**: Compatibility
**Description**: Phase 1 支援 Telegram Bot API 與 LINE Messaging API 兩個平台。

#### NFR-04: NFR-04: Webhook Verification 100%
**Requirement**: **Category**: Security
**Description**: 每個 webhook 請求必須通過簽名驗證，不得有未驗證請求進入業務邏輯。

#### NFR-05: NFR-05: JSON Structured Logging
**Requirement**: **Category**: Observability
**Description**: 所有日誌必須為 JSON 結構化格式（NDJSON），含 timestamp / level / service / message。

#### NFR-06: NFR-06: PII Masking Coverage
**Requirement**: **Category**: Security
**Description**: 台灣格式電話、Email、地址必須在儲存或輸出前遮蔽。敏感關鍵字（密碼、銀行帳戶等）觸發轉接。

### Phase 1 Deliverables
- [ ] `SRS.md` - Software Requirements Specification (FRs + NFRs)
- [ ] `SPEC_TRACKING.md` - Spec tracking matrix
- [ ] `TRACEABILITY_MATRIX.md` - Requirements traceability matrix
- [x] `sessions_spawn.log` — auto-populated by AgentSpawner (HR-10)


### 🔒 CHECKPOINT-1: Human Peer Review — Phase 1 Exit
> Phase 1/2 exit gate = human document review (NOT `harness run-gate --gate 1`).
> APPROVE criteria: all FRs addressed, no critical gaps, terminology consistent.

- [ ] **[HR-READ]** Reviewer reads all deliverables:
  - `01-requirements/SRS.md`
  - `01-requirements/SPEC_TRACKING.md`
  - `01-requirements/TRACEABILITY_MATRIX.md`
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
- [ ] Generate Phase 2 plan:
  ```bash
  python3 harness_cli.py plan-phase --phase 2 --project $REPO \
    --output $REPO/.methodology/phase2_plan.md
  ```
- [ ] Advance FSM to Phase 2 (writes new HANDOVER.md + local commit):
  ```bash
  python3 harness_cli.py advance-phase --completed 1 --project .
  ```
- [ ] Confirm `HANDOVER.md` reflects Phase 2 entry (`P2-entry` checkpoint, correct plan path)
- [ ] Open `phase2_plan.md` and follow from the top.
- [ ] If session crashes during Phase 2: read `HANDOVER.md` or run `generate-next-plan`
