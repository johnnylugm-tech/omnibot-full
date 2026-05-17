# Phase 1 Full Execution Plan -- omnibot-full

> **Version**: v2.3.0 (project plan)
> **Project**: omnibot-full
> **Date**: 2026-05-17
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
> - CHECKPOINT-1: Agent B Peer Review (Phase 1 Exit) → `push-checkpoint --phase 1`

### Pre-Phase Preflight

- [x] **[PREFLIGHT]** Run phase hooks (FSM, Constitution, Kill-Switch, Drift, CI Readiness):
  ```bash
  python3 harness_cli.py run-phase --phase 1 --project $REPO
  ```
  If FAILED: fix FSM/Constitution issues. There is no gate bypass flag.

- [x] **[PREFLIGHT-CI]** ⛔ HARD STOP if any item below is missing — complete SKILL.md §0.1 Step 0 first:
  1. `.methodology/state.json` exists with `current_phase = 1`  ← set by `init-project`
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
- [x] **[A-1]** Agent A (REQUIREMENTS_ENGINEER): Elicit requirements → write FRs/NFRs in SRS.md (### FR-XX: format) → validate completeness
  - FORBIDDEN: vague/non-testable acceptance criteria
- [x] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [x] **[B-1]** Agent B (BUSINESS_ANALYST) — dispatch as **STATELESS** subagent:
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

- [x] **[B-2]** Agent B returns JSON — parse `review_status` **AND** `gaps` severity:
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
- [x] **[A-1]** Agent A (REQUIREMENTS_ENGINEER): Build spec tracking matrix from SRS.md FRs → assign status/owner per FR → validate completeness
  - FORBIDDEN: vague/non-testable acceptance criteria
- [x] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [x] **[B-1]** Agent B (BUSINESS_ANALYST) — dispatch as **STATELESS** subagent:
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

- [x] **[B-2]** Agent B returns JSON — parse `review_status` **AND** `gaps` severity:
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
- [x] **[A-1]** Agent A (REQUIREMENTS_ENGINEER): Build bidirectional traceability matrix → link FRs → design elements → test cases → validate coverage
  - FORBIDDEN: vague/non-testable acceptance criteria
- [x] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [x] **[B-1]** Agent B (BUSINESS_ANALYST) — dispatch as **STATELESS** subagent:
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

- [x] **[B-2]** Agent B returns JSON — parse `review_status` **AND** `gaps` severity:
  - `APPROVE` + all gaps are `low` → all deliverables complete; proceed to Agent B Peer Review
  - `APPROVE` + any gap is `medium` or `high` → fix gaps → **re-dispatch B as round 2**
    (embed same docs as B-1 above, replacing `TRACEABILITY_MATRIX.md` with its updated content)
    → all deliverables complete; proceed to Agent B Peer Review only after round-2 APPROVE
  - `REJECT` → Agent A fixes gaps → re-dispatch B. Max 5 rounds (HR-12).

  > ⚠️ **BLOCKING**: Do NOT start the next Sub-Task until this sub-task's current
  > round is fully APPROVED (including any required round 2).
  > AgentSpawner auto-logs round-2 re-dispatch to `sessions_spawn.log` (HR-10).

  > fr_id uses P1 as phase-level placeholder; replace with FR-XX for FR-specific plans.

### FR Requirements (11 total)

#### FR-14: Platform Adapter — Messenger + WhatsApp Webhook
**Task**: Phase 1 已支援 Telegram 和 LINE webhook。Phase 2 新增 Messenger 和 WhatsApp 兩個平台的 webhook 接收端點，使用 HMAC-SHA256 驗證，轉換為 UnifiedMessage。

#### FR-15: Prompt Injection Defense L3 — Sandwich Defense
**Task**: 在 Input Sanitizer L2（字元正規化）之後，L3 層偵測 10 種可疑 prompt injection pattern，阻擋攻擊並記錄至 security_logs。安全輸入使用 Sandwich Defense 格式包裹後傳遞給 LLM。

#### FR-16: PII Masking V2 — Credit Card + Luhn Check
**Task**: 在 Phase 1 PII Masking L4 基礎上新增信用卡號偵測與 Luhn 校驗，確保僅遮蔽有效信用卡號。

#### FR-17: Emotion Analyzer — Sentiment Classification + Decay
**Task**: 分析每條使用者訊息的情緒類別與強度，追蹤情緒歷史並以 24 小時半衰期進行指數衰減加權。連續 >= 3 次負面情緒自動觸發人工轉接。

#### FR-18: Intent Router + Dialogue State Tracker (DST)
**Task**: 實作 7 狀態對話狀態機（DST），支援意圖偵測、slot filling 與自動轉接。最多 3 輪未完成 slot filling 觸發轉接。

#### FR-19: Hybrid Knowledge Layer V2 — Four-Layer Architecture
**Task**: 升級 Phase 1 的 Knowledge Layer V1（僅 Layer 1+4）為完整四層架構（HybridKnowledgeV2）：Layer 1 規則匹配 (40%)、Layer 2 RAG 向量檢索 (40%)、Layer 3 LLM 生成 (10%)、Layer 4 人工轉接 (10%)。Layer 1 + Layer 2 結果透過 RRF k=60 融合排序。實作類別命名為 HybridKnowledgeV2（Phase 2 對應版本）。

#### FR-20: Escalation Manager V2 — SLA Priority Levels
**Task**: 從 Phase 1 BasicEscalationManager 升級，新增 SLA 優先級分級、sla_deadline 計算與違規查詢。

#### FR-21: Grounding Checks L5 — Semantic Alignment Verification
**Task**: 驗證 LLM 生成輸出與知識庫來源內容的語義相似度，cosine similarity >= 0.75 視為 grounded，低於閾值拒絕輸出並轉接人工。

#### FR-22: Prometheus Metrics — Core Instrumentation
**Task**: 匯出 8 個核心 Prometheus metrics，覆蓋延遲、請求量、FCR、知識層命中、PII 遮蔽、轉接佇列、情緒觸發與 LLM token 用量。

#### FR-23: Database Schema — Phase 2 Incremental Tables + Index
**Task**: 在 Phase 1 核心表基礎上新增 emotion_history、edge_cases 表，並啟用 knowledge_base 的 pgvector ivfflat 索引。

#### FR-24: Golden Dataset — Edge Case Collection + Regression Baseline
**Task**: 建立 500 筆黃金數據集，涵蓋 6 種邊界案例類型，用於回歸測試自動化驗證。

### NFR Non-Functional Requirements (9 total)

#### NFR-07: NFR-07: First Contact Resolution (FCR) >= 80%
**Requirement**: **Category**: Performance
**Description**: 以 30 天滾動窗口計算，in_scope 對話中 `first_contact_resolution = TRUE` 的比例需 >= 80%。由 Phase 1 的 50% 基準升級。
**Measurement**: ODD SQL 查詢 `messages` JOIN `conversations`，30 

#### NFR-08: NFR-08: p95 Response Latency < 1.5s
**Requirement**: **Category**: Performance
**Description**: 從 webhook 接收到回覆發送之間，p95 延遲 < 1.5 秒。以 platform 分組計算。由 Phase 1 的 < 3.0s 升級。
**Measurement**: `omnibot_response_duration_seconds` histogram，以 platform 分組計算 p95

#### NFR-09: NFR-09: Platform Support — 4 Platforms
**Requirement**: **Category**: Compatibility
**Description**: Phase 2 支援 Telegram、LINE、Messenger、WhatsApp 共 4 個平台的 webhook 接收與訊息回覆。

#### NFR-10: NFR-10: Webhook Signature Verification — 100% Coverage
**Requirement**: **Category**: Security
**Description**: 所有平台（Telegram、LINE、Messenger、WhatsApp）的每個 webhook 請求必須通過對應的 HMAC-SHA256 簽名驗證。不得有任何未驗證請求進入業務邏輯管道。

#### NFR-11: NFR-11: PII Masking — 100% Coverage Including Luhn
**Requirement**: **Category**: Security
**Description**: 台灣格式電話、Email、地址、有效信用卡號（經 Luhn 校驗）必須在儲存或輸出前 100% 遮蔽。敏感關鍵字（密碼、銀行帳戶等）觸發轉接。

#### NFR-12: NFR-12: Security Block Rate >= 95%
**Requirement**: **Category**: Security
**Description**: Prompt injection 攻擊（10 種 pattern）偵測率 >= 95%。透過紅隊測試對抗 100 組惡意輸入，至少 95 組被正確阻擋。
**Measurement**: `security_logs` 表 blocked rate (SPEC/omnibot-phase-2.md L923-L936)

#### NFR-13: NFR-13: Grounding Check — 100% LLM Output Verification
**Requirement**: **Category**: Reliability
**Description**: 所有 LLM Layer 3 生成的輸出必須通過 Grounding Checks L5 驗證（cosine similarity >= 0.75）。未接地輸出不得發送給使用者，改轉 Layer 4 人工處理。

#### NFR-14: NFR-14: SLA Compliance >= 90%
**Requirement**: **Category**: Reliability
**Description**: 轉接至人工的請求中，在 sla_deadline 前完成 resolved 的比例 >= 90%。依 priority 等級分別計算（normal/30min, high/15min, urgent/5min）。
**Measurement**: ODD SQL 查詢 (SPEC/omnibot-phase-2.

#### NFR-15: NFR-15: Golden Dataset >= 500 Edge Cases
**Requirement**: **Category**: Quality
**Description**: Phase 2 結束前黃金數據集累積 >= 500 筆已標註邊界案例，涵蓋 6 種邊界類型（每類至少 50 筆），用於回歸測試自動化。

### Phase 1 Deliverables
- [x] `SRS.md` - Software Requirements Specification (FRs + NFRs)
- [x] `SPEC_TRACKING.md` - Spec tracking matrix
- [x] `TRACEABILITY_MATRIX.md` - Requirements traceability matrix
- [x] `sessions_spawn.log` — auto-populated by AgentSpawner (HR-10)


### 🔒 CHECKPOINT-1: Agent B Peer Review — Phase 1 Exit
> Phase 1/2 exit gate = Agent B document review (NOT `harness run-gate --gate 1`).
> APPROVE criteria: all FRs addressed, no critical gaps, terminology consistent.

- [x] **[B-READ]** Reviewer reads all deliverables:
  - `01-requirements/SRS.md`
  - `01-requirements/SPEC_TRACKING.md`
  - `01-requirements/TRACEABILITY_MATRIX.md`
  - Checklist: All FRs covered? No contradictions? Each item testable/traceable?
- [x] **[B-DECIDE]** Reviewer records decision:
  ```json
  {"phase": 1, "reviewer": "XXXX", "status": "APPROVE", "reason": "..."}
  ```
  - If REJECT → author fixes → re-review. Max 5 rounds (HR-12).
- [x] **[B-PUSH]** ✅ Push to GitHub + HANDOVER.md (CHECKPOINT-1 saved):
  ```bash
  python3 harness_cli.py push-checkpoint --phase 1 --project . \
    --fr-ids FR-01,FR-02,FR-03
  ```
  > This writes `HANDOVER.md` (crash-recovery checkpoint) to project root,
  > then commits + pushes all changes to origin.
  > After a crash, read HANDOVER.md first — it tells you where you were.

### Phase 1 → Phase 2: Architecture Design

- [x] Confirm ALL checkpoints in this plan are ✓  (no skips — HR-03)
- [x] Generate Phase 2 plan:
  ```bash
  python3 harness_cli.py plan-phase --phase 2 --project $REPO \
    --output $REPO/.methodology/phase2_plan.md
  ```
- [x] Advance FSM to Phase 2 (writes new HANDOVER.md + local commit):
  ```bash
  python3 harness_cli.py advance-phase --completed 1 --project .
  ```
- [x] Confirm `HANDOVER.md` reflects Phase 2 entry (`P2-entry` checkpoint, correct plan path)
- [x] Open `phase2_plan.md` and follow from the top.
- [x] If session crashes during Phase 2: read `HANDOVER.md` or run `generate-next-plan`
