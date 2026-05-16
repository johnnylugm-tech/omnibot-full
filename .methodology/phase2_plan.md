# Phase 2 Full Execution Plan -- omnibot-full

> **Version**: v2.3.0 (project plan)
> **Project**: omnibot-full
> **Date**: 2026-05-16
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
> - CHECKPOINT-1: Human Peer Review (Phase 2 Exit) → `push-checkpoint --phase 2`

### Entry Gate Verification

- [ ] **[ENTRY-CHECK]** Confirm Phase 1 exit (P1 human APPROVE) before proceeding (HR-03 — no phase skips):
  Proof: git log contains commit 'phase1(human-review): Phase 1 deliverables APPROVED'.
  If NOT confirmed: return to Phase 1 and complete exit gate first.

### Pre-Phase Preflight

- [ ] **[PREFLIGHT]** Run phase hooks (FSM, Constitution, Kill-Switch, Drift, CI Readiness):
  ```bash
  python3 harness_cli.py run-phase --phase 2 --project $REPO
  ```
  If FAILED: fix FSM/Constitution issues. There is no gate bypass flag.

- [ ] **[PREFLIGHT-CI]** Confirm CI wiring unchanged (should be set since P1):
  1. `.github/workflows/harness_quality_gate.yml` exists
  2. Git hooks installed (`ls .git/hooks/prepare-commit-msg`)
  3. harness importable (submodule, PYTHONPATH, or vendored `quality_gate/`)
  4. GitHub repo variable `CURRENT_PHASE` = 2 (updated by `advance-phase`)
  > If stale: run `python3 harness_cli.py init-project --phase 2 --project $REPO --overwrite`

### Task Decomposition (Dependency Analysis)

**Phase 2 has 1 deliverables with sequential dependencies:**

| Order | Deliverable | Depends On | Agent A | Agent B |
|-------|------------|------------|---------|---------|
| 1 | `SAD.md` | (none — starting point) | ARCHITECT | TECH_LEAD |

**Execution rule**: Each deliverable must pass Agent B review BEFORE starting the next.
If a deliverable is REJECTED, fix only that deliverable — earlier APPROVED deliverables
are not re-opened. This bounds backtracking to a single step.

### Architecture Design (Serial A/B per Deliverable)

### Sub-Task 1/1: SAD.md — Software Architecture Document — components, interfaces, FR→module mapping, data flows

**Depends on**: none — starting point
**Agent A**: ARCHITECT
**Agent B**: TECH_LEAD

**A/B Work** (HR-01: A≠B · HR-04: HybridWorkflow ON · HR-10: log required):
- [ ] **[A-1]** Agent A (ARCHITECT): Design system architecture → write SAD.md → validate every FR has a module mapping
  - FORBIDDEN: vague/non-testable acceptance criteria
- [ ] **[A-2]** Agent A returns `{status, files, confidence, citations, summary}`
- [ ] **[B-1]** Agent B (TECH_LEAD) — dispatch as **STATELESS** subagent:
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

- [ ] **[B-2]** Agent B returns JSON — parse `review_status` **AND** `gaps` severity:
  - `APPROVE` + all gaps are `low` → all deliverables complete; proceed to Human Peer Review
  - `APPROVE` + any gap is `medium` or `high` → fix gaps → **re-dispatch B as round 2**
    (embed same docs as B-1 above, replacing `SAD.md` with its updated content)
    → all deliverables complete; proceed to Human Peer Review only after round-2 APPROVE
  - `REJECT` → Agent A fixes gaps → re-dispatch B. Max 5 rounds (HR-12).

  > ⚠️ **BLOCKING**: Do NOT start the next Sub-Task until this sub-task's current
  > round is fully APPROVED (including any required round 2).
  > AgentSpawner auto-logs round-2 re-dispatch to `sessions_spawn.log` (HR-10).

  > fr_id uses P2 as phase-level placeholder; replace with FR-XX for FR-specific plans.

### FR Architecture Mapping (13 total)

#### FR-01: Platform Adapter — Telegram + LINE Webhook
**Requirement**: 系統必須接收來自 Telegram Bot API 和 LINE Messaging API 的 webhook 請求，轉換為內部統一消息格式（UnifiedMessage）。

#### FR-02: Webhook Signature Verification
**Requirement**: 每個 webhook 請求必須先通過簽名驗證，未通過者拒絕處理。

#### FR-03: Unified Message Format
**Requirement**: 所有平台消息必須轉換為統一的 `UnifiedMessage` dataclass，對下游模組隱藏平台差異。

#### FR-04: Input Sanitizer L2 — Character Normalization
**Requirement**: 所有使用者輸入文字必須經過 NFKC 正規化，移除非列印控制字元。

#### FR-05: PII Masking L4 — Phone / Email / Address
**Requirement**: 使用者訊息中的台灣電話、Email、地址必須在記錄或輸出前遮蔽。敏感關鍵字觸發轉接。

#### FR-06: Rate Limiter — Token Bucket
**Requirement**: 每個平台用戶必須有獨立的請求速率限制，防止濫用。

#### FR-07: Knowledge Layer V1 — Rule Match + Escalate
**Requirement**: 查詢知識庫時先執行 SQL 精確/模糊匹配（Layer 1），信心度 > 0.7 直接回覆，否則轉接人工。

#### FR-08: Basic Escalation Manager — No SLA
**Requirement**: 無法匹配的查詢必須進入轉接佇列，支援指派與結案。

#### FR-09: Structured Logger — JSON Format
**Requirement**: 所有日誌必須以 JSON 結構化格式輸出，包含 timestamp / level / service / message。

#### FR-10: API Response Format — ApiResponse / PaginatedResponse
**Requirement**: 所有 API 回應必須使用統一的 `ApiResponse[T]` 或 `PaginatedResponse[T]` 泛型格式。

#### FR-11: Health Check Endpoint
**Requirement**: 系統必須提供健康檢查端點供 Docker / 監控系統使用。

#### FR-12: Database Schema — All Core Tables
**Requirement**: 必須建立所有核心資料表，包含 Phase 2/3 預留欄位，避免後續 ALTER TABLE。

#### FR-13: Docker Compose Development Environment
**Requirement**: 提供一鍵啟動的開發環境，包含 API、PostgreSQL (pgvector)、Redis。

### SAB Generation (Machine-Readable Architecture Baseline)

- [ ] **[SAB]** Generate `.methodology/SAB.json` from SAD.md §6 SAB block:
  ```bash
  python3 scripts/generate_sab.py --project $REPO
  ```
  - SAB.json contains: layers, modules, allowed_dependencies, quality_targets
  - Used by: drift detector (M2), gate architecture dimension, constitution check
  - Also embedded inline in `quality_manifest.json` via `harness_bridge`

### Phase 2 Deliverables
- [ ] `SAD.md` - Software Architecture Document (every FR has module mapping)
- [ ] `.methodology/quality_manifest.json` — Quality manifest (FR list + SAB data)
- [ ] `.methodology/SAB.json` — Machine-readable architecture baseline
- [x] `sessions_spawn.log` — auto-populated by AgentSpawner (HR-10)


### 🔒 CHECKPOINT-1: Human Peer Review — Phase 2 Exit
> Phase 1/2 exit gate = human document review (NOT `harness run-gate --gate 1`).
> APPROVE criteria: all FRs addressed, no critical gaps, terminology consistent.

- [ ] **[HR-READ]** Reviewer reads all deliverables:
  - `02-architecture/SAD.md`
  - Checklist: All FRs covered? No contradictions? Each item testable/traceable?
- [ ] **[HR-DECIDE]** Reviewer records decision:
  ```json
  {"phase": 2, "reviewer": "XXXX", "status": "APPROVE", "reason": "..."}
  ```
  - If REJECT → author fixes → re-review. Max 5 rounds (HR-12).
- [ ] **[HR-PUSH]** ✅ Push to GitHub + HANDOVER.md (CHECKPOINT-1 saved):
  ```bash
  python3 harness_cli.py push-checkpoint --phase 2 --project . \
    --fr-ids FR-01,FR-02,FR-03
  ```
  > This writes `HANDOVER.md` (crash-recovery checkpoint) to project root,
  > then commits + pushes all changes to origin.
  > After a crash, read HANDOVER.md first — it tells you where you were.

### Phase 2 → Phase 3: Implementation

- [ ] Confirm ALL checkpoints in this plan are ✓  (no skips — HR-03)
- [ ] Generate Phase 3 plan:
  ```bash
  python3 harness_cli.py plan-phase --phase 3 --project $REPO \
    --output $REPO/.methodology/phase3_plan.md
  ```
- [ ] Advance FSM to Phase 3 (writes new HANDOVER.md + local commit):
  ```bash
  python3 harness_cli.py advance-phase --completed 2 --project .
  ```
- [ ] Confirm `HANDOVER.md` reflects Phase 3 entry (`P3-entry` checkpoint, correct plan path)
- [ ] Open `phase3_plan.md` and follow from the top.
- [ ] If session crashes during Phase 3: read `HANDOVER.md` or run `generate-next-plan`
