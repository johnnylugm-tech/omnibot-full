# Phase 2 Full Execution Plan -- omnibot-full

> **Version**: v2.3.0 (project plan)
> **Project**: omnibot-full
> **Date**: 2026-05-17
> **Framework**: harness-methodology v2.3.0
> **Phase**: 2 - Architecture Design
> **Status**: Full version (including Phase 2 detailed tasks)

---

## Phase 2 Tasks: Architecture Design

### Phase 2 Overview
Phase 2 designs the system architecture based on SRS, producing SAD and ADR.
**Exit gate = human peer review of deliverables** (not `harness run-gate --gate 1`).

> **Crash Recovery**: after each push, `HANDOVER.md` is written to project root.
> If context is lost, read `HANDOVER.md` first — it contains phase, status, and next steps.

> **Checkpoint Index** (push to GitHub = checkpoint + HANDOVER.md saved):
> - CHECKPOINT-1: Agent B Peer Review (Phase 2 Exit) → `push-checkpoint --phase 2`

### Entry Gate Verification

- [x] **[ENTRY-CHECK]** P1 review-complete:
  Proof: git log contains commit 'phase1(review-complete): Phase 1 deliverables APPROVED'.
  If NOT confirmed: return to Phase 1 and complete exit gate first.

### Pre-Phase Preflight

- [x] **[PREFLIGHT]** Run phase hooks (FSM, Constitution, Kill-Switch, Drift, CI Readiness):
  ```bash
  python3 harness_cli.py run-phase --phase 2 --project $REPO
  ```
  If FAILED: fix FSM/Constitution issues. There is no gate bypass flag.

- [x] **[PREFLIGHT-CI]** Confirm CI wiring unchanged (should be set since P1):
  1. `.github/workflows/harness_quality_gate.yml` exists
  2. Git hooks installed (`ls .git/hooks/prepare-commit-msg`)
  3. harness importable (submodule, PYTHONPATH, or vendored `quality_gate/`)
  4. GitHub repo variable `CURRENT_PHASE` = 2 (updated by `advance-phase`)
  > If stale: run `python3 harness_cli.py init-project --phase 2 --project $REPO --overwrite`

### Task Decomposition (Dependency Analysis)

**Phase 2 has 2 deliverables with sequential dependencies:**

| Order | Deliverable | Depends On | Agent A | Agent B |
|-------|------------|------------|---------|---------|
| 1 | `SAD.md` | (none — starting point) | ARCHITECT | TECH_LEAD |
| 2 | `ADR.md` | SAD.md | ARCHITECT | TECH_LEAD |

**Execution rule**: Each deliverable must pass Agent B review BEFORE starting the next.
If a deliverable is REJECTED, fix only that deliverable — earlier APPROVED deliverables
are not re-opened. This bounds backtracking to a single step.

### Architecture Design (Serial A/B per Deliverable)

### Sub-Task 1/2: SAD.md — Software Architecture Document — components, interfaces, FR→module mapping, data flows

**Depends on**: none — starting point
**Agent A**: ARCHITECT
**Agent B**: TECH_LEAD

**A/B Work** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [x] **[A-1]** Agent A (ARCHITECT): Design system architecture → write SAD.md → validate every FR has a module mapping
  - FORBIDDEN: vague/non-testable acceptance criteria
- [x] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [x] **[B-1]** Agent B (TECH_LEAD) — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `01-requirements/SRS.md (full)`
  - `draft 02-architecture/SAD.md (full)`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are TECH_LEAD. Your task: review the following deliverable (SAD.md).
  You have NO access to any files — all context is provided below.

  === [DOC 1: 01-requirements/SRS.md (full)] ===
  {paste full content here}

  === [DOC 2: draft 02-architecture/SAD.md (full)] ===
  {paste full content here}

  Review checklist:
  - Every FR maps to ≥1 module?
  - NFRs addressed (latency/security/cost)?
  - No circular dependencies?
  - Data flow diagrams consistent?

  Return JSON only:
  {"status":"STAGE_PASS"|"REJECT","review_status":"APPROVE"|"REJECT",
   "reason":"...","confidence":1-10,"citations":["file:line"],"gaps":[...]}
  ```

- [x] **[B-2]** Agent B returns JSON — parse `review_status` **AND** `gaps` severity:
  - `APPROVE` + all gaps are `low` → continue to Sub-Task 2/2
  - `APPROVE` + any gap is `medium` or `high` → fix gaps → **re-dispatch B as round 2**
    (embed same docs as B-1 above, replacing `SAD.md` with its updated content)
    → continue to Sub-Task 2/2 only after round-2 APPROVE
  - `REJECT` → Agent A fixes gaps → re-dispatch B. Max 5 rounds (HR-12).

  > ⚠️ **BLOCKING**: Do NOT start the next Sub-Task until this sub-task's current
  > round is fully APPROVED (including any required round 2).
  > AgentSpawner auto-logs round-2 re-dispatch to `sessions_spawn.log` (HR-10).

  > fr_id uses P2 as phase-level placeholder; replace with FR-XX for FR-specific plans.

### Sub-Task 2/2: ADR.md — Architecture Decision Records — document key design decisions (tech stack, patterns, interfaces, trade-offs) with context and consequences

**Depends on**: SAD.md (+ Sub-Task 1/2 review: previous review gaps carry forward)
**Agent A**: ARCHITECT
**Agent B**: TECH_LEAD

**A/B Work** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [x] **[A-1]** Agent A (ARCHITECT): Extract key architecture decisions from SAD.md → write individual ADR entries → validate rationale and consequences are recorded
  - FORBIDDEN: vague/non-testable acceptance criteria
- [x] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [x] **[B-1]** Agent B (TECH_LEAD) — dispatch as **STATELESS** subagent:
  > ⚠️  **STATELESS SANDBOX**: Agent B has ZERO access to local files or /tmp.
  > NEVER write 'read 01-requirements/SRS.md' in the prompt — it will fail silently.
  > ALL context must be pasted verbatim into the prompt text. This is mandatory.
  >
  > **Lesson (stateless agent)**: Rounds 2-3 failed because prompts used file paths.
  > Round 4 succeeded only after embedding full document content directly.

  **Embed these documents in full** (copy content, not paths):
  - `Previous Sub-Task B-2 review JSON — SAD.md (Sub-Task 1/2, gaps field may contain non-blocking caveats)`
  - `02-architecture/SAD.md (APPROVED — full content)`
  - `draft 02-architecture/ADR.md (full content)`
  - `templates/ADR.md (template format)`

  **Agent B prompt structure** (use this template verbatim):
  ```
  You are TECH_LEAD. Your task: review the following deliverable (ADR.md).
  You have NO access to any files — all context is provided below.

  === [DOC 1: Previous Sub-Task B-2 review JSON — SAD.md (Sub-Task 1/2, gaps field may contain non-blocking caveats)] ===
  {paste full content here}

  === [DOC 2: 02-architecture/SAD.md (APPROVED — full content)] ===
  {paste full content here}

  === [DOC 3: draft 02-architecture/ADR.md (full content)] ===
  {paste full content here}

  === [DOC 4: templates/ADR.md (template format)] ===
  {paste full content here}

  Review checklist:
  - Upstream deliverable review caveats addressed? (check previous B-2 gaps field)
  - All major decisions documented (tech stack, patterns, interfaces)?
  - Each ADR has clear context, decision, and consequences?
  - Alternatives considered documented?
  - Decision aligns with SAD.md architecture?
  - All upstream deliverables consistent with each other? No contradictory decisions?

  Return JSON only:
  {"status":"STAGE_PASS"|"REJECT","review_status":"APPROVE"|"REJECT",
   "reason":"...","confidence":1-10,"citations":["file:line"],"gaps":[...]}
  ```

- [x] **[B-2]** Agent B returns JSON — parse `review_status` **AND** `gaps` severity:
  - `APPROVE` + all gaps are `low` → all deliverables complete; proceed to Agent B Peer Review
  - `APPROVE` + any gap is `medium` or `high` → fix gaps → **re-dispatch B as round 2**
    (embed same docs as B-1 above, replacing `ADR.md` with its updated content)
    → all deliverables complete; proceed to Agent B Peer Review only after round-2 APPROVE
  - `REJECT` → Agent A fixes gaps → re-dispatch B. Max 5 rounds (HR-12).

  > ⚠️ **BLOCKING**: Do NOT start the next Sub-Task until this sub-task's current
  > round is fully APPROVED (including any required round 2).
  > AgentSpawner auto-logs round-2 re-dispatch to `sessions_spawn.log` (HR-10).

  > fr_id uses P2 as phase-level placeholder; replace with FR-XX for FR-specific plans.

### FR Architecture Mapping (11 total)

#### FR-14: Platform Adapter — Messenger + WhatsApp Webhook
**Requirement**: Phase 1 已支援 Telegram 和 LINE webhook。Phase 2 新增 Messenger 和 WhatsApp 兩個平台的 webhook 接收端點，使用 HMAC-SHA256 驗證，轉換為 UnifiedMessage。

#### FR-15: Prompt Injection Defense L3 — Sandwich Defense
**Requirement**: 在 Input Sanitizer L2（字元正規化）之後，L3 層偵測 10 種可疑 prompt injection pattern，阻擋攻擊並記錄至 security_logs。安全輸入使用 Sandwich Defense 格式包裹後傳遞給 LLM。

#### FR-16: PII Masking V2 — Credit Card + Luhn Check
**Requirement**: 在 Phase 1 PII Masking L4 基礎上新增信用卡號偵測與 Luhn 校驗，確保僅遮蔽有效信用卡號。

#### FR-17: Emotion Analyzer — Sentiment Classification + Decay
**Requirement**: 分析每條使用者訊息的情緒類別與強度，追蹤情緒歷史並以 24 小時半衰期進行指數衰減加權。連續 >= 3 次負面情緒自動觸發人工轉接。

#### FR-18: Intent Router + Dialogue State Tracker (DST)
**Requirement**: 實作 7 狀態對話狀態機（DST），支援意圖偵測、slot filling 與自動轉接。最多 3 輪未完成 slot filling 觸發轉接。

#### FR-19: Hybrid Knowledge Layer V2 — Four-Layer Architecture
**Requirement**: 升級 Phase 1 的 Knowledge Layer V1（僅 Layer 1+4）為完整四層架構（HybridKnowledgeV2）：Layer 1 規則匹配 (40%)、Layer 2 RAG 向量檢索 (40%)、Layer 3 LLM 生成 (10%)、Layer 4 人工轉接 (10%)。Layer 1 + Layer 2 結果透過 RRF k=60 融合排序。實作類別命名為 HybridKnowledgeV2（Phase 2 對應版本）。

#### FR-20: Escalation Manager V2 — SLA Priority Levels
**Requirement**: 從 Phase 1 BasicEscalationManager 升級，新增 SLA 優先級分級、sla_deadline 計算與違規查詢。

#### FR-21: Grounding Checks L5 — Semantic Alignment Verification
**Requirement**: 驗證 LLM 生成輸出與知識庫來源內容的語義相似度，cosine similarity >= 0.75 視為 grounded，低於閾值拒絕輸出並轉接人工。

#### FR-22: Prometheus Metrics — Core Instrumentation
**Requirement**: 匯出 8 個核心 Prometheus metrics，覆蓋延遲、請求量、FCR、知識層命中、PII 遮蔽、轉接佇列、情緒觸發與 LLM token 用量。

#### FR-23: Database Schema — Phase 2 Incremental Tables + Index
**Requirement**: 在 Phase 1 核心表基礎上新增 emotion_history、edge_cases 表，並啟用 knowledge_base 的 pgvector ivfflat 索引。

#### FR-24: Golden Dataset — Edge Case Collection + Regression Baseline
**Requirement**: 建立 500 筆黃金數據集，涵蓋 6 種邊界案例類型，用於回歸測試自動化驗證。

### SAB Generation (Machine-Readable Architecture Baseline)

- [x] **[SAB]** Generate `.methodology/SAB.json` from SAD.md §6 SAB block:
  ```bash
  python3 scripts/generate_sab.py --project $REPO
  ```
  - SAB.json contains: layers, modules, allowed_dependencies, quality_targets
  - Used by: drift detector (M2), gate architecture dimension, constitution check
  - Also embedded inline in `quality_manifest.json` via `harness_bridge`

### Phase 2 Deliverables
- [x] `SAD.md` — Software Architecture Document (every FR has module mapping)
- [x] `ADR.md` — Architecture Decision Records (tech stack, patterns, interfaces)
- [x] `.methodology/quality_manifest.json` — Quality manifest (FR list + SAB data)
- [x] `.methodology/SAB.json` — Machine-readable architecture baseline
- [x] `sessions_spawn.log` — auto-populated by AgentSpawner (HR-10)


### 🔒 CHECKPOINT-1: Agent B Peer Review — Phase 2 Exit
> Phase 1/2 exit gate = Agent B document review (NOT `harness run-gate --gate 1`).
> APPROVE criteria: all FRs addressed, no critical gaps, terminology consistent.

- [x] **[B-READ]** Reviewer reads all deliverables:
  - `02-architecture/SAD.md`
  - `02-architecture/ADR.md`
  - Checklist: All FRs covered? No contradictions? Each item testable/traceable?
- [x] **[B-DECIDE]** Reviewer records decision:
  ```json
  {"phase": 2, "reviewer": "XXXX", "status": "APPROVE", "reason": "..."}
  ```
  - If REJECT → author fixes → re-review. Max 5 rounds (HR-12).
- [x] **[B-PUSH]** ✅ Push to GitHub + HANDOVER.md (CHECKPOINT-1 saved):
  ```bash
  python3 harness_cli.py push-checkpoint --phase 2 --project . \
    --fr-ids FR-01,FR-02,FR-03
  ```
  > This writes `HANDOVER.md` (crash-recovery checkpoint) to project root,
  > then commits + pushes all changes to origin.
  > After a crash, read HANDOVER.md first — it tells you where you were.

### Phase 2 → Phase 3: Implementation

- [x] Confirm ALL checkpoints in this plan are ✓  (no skips — HR-03)
- [x] Generate Phase 3 plan:
  ```bash
  python3 harness_cli.py plan-phase --phase 3 --project $REPO \
    --output $REPO/.methodology/phase3_plan.md
  ```
- [x] Advance FSM to Phase 3 (writes new HANDOVER.md + local commit):
  ```bash
  python3 harness_cli.py advance-phase --completed 2 --project .
  ```
- [x] Confirm `HANDOVER.md` reflects Phase 3 entry (`P3-entry` checkpoint, correct plan path)
- [x] Open `phase3_plan.md` and follow from the top.
- [x] If session crashes during Phase 3: read `HANDOVER.md` or run `generate-next-plan`
