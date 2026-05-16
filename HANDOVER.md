# Harness Methodology — Session Handover

**Checkpoint**: `P8-exit-20260516`  
**Phase**: P8 — Config & Records  
**Generated**: 2026-05-16T07:38:21Z

> ⚠️  **開始下一個工作階段前，請先執行 `/compact` 壓縮上下文**，再從「接下來的工作」繼續。

---

## ▶ 立即開始（三步）

```bash
# 1. Clone (if working directory cleared)
git clone --recurse-submodules https://github.com/johnnylugm-tech/omnibot-full.git && cd omnibot-full

# 2. Set required env vars
export HERMES_REVIEWER_TARGET=<value>

# 3. Read plan and start Phase 9
cat .methodology/phase9_plan.md
# Follow SKILL.md §0.1 Phase 9 entry check, then execute
```

---

## 快速接手指令（詳細）

```bash
# Clone (--recurse-submodules required for harness submodule)
git clone --recurse-submodules https://github.com/johnnylugm-tech/omnibot-full.git /tmp/omnibot-full && cd /tmp/omnibot-full

# Confirm latest commits
git log --oneline -3

# Confirm FSM state
cat .methodology/state.json   # expected: phase=8 state=ACTIVE last_gate=1 last_fr=FR-13

# Read active plan
cat .methodology/phase9_plan.md
```

| 欄位 | 值 |
|------|----|
| Remote | `https://github.com/johnnylugm-tech/omnibot-full.git` |
| Branch | `main` |
| State | `phase=8 state=ACTIVE last_gate=1 last_fr=FR-13` |
| Plan | `.methodology/phase9_plan.md` |

---

## 任務背景

P8 Config & Records: pipeline fully complete.

## 目前執行狀況

P8 Config & Records complete. All 8 phases done.

## 接下來的工作

1. Pipeline complete — all phases P1–P8 finished
2. Review final HANDOVER.md and git tag for Gate 4
3. Archive session via /compact

## 注意事項

- 100% follow SKILL.md
- Do NOT commit `.sessi-work/` or `.methodology/` runtime artifacts
- Git failures are warnings — they never block the pipeline

---
*由 `HandoverGenerator` 自動生成。下次 push 時此檔案將被覆寫。*
