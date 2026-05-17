# Architecture Decision Records — OmniBot Phase 2

> **Project**: OmniBot — 多平台客服機器人
> **Phase**: 2 (智慧化 + 安全強化)
> **Version**: 2.0
> **Date**: 2026-05-17
> **Authored by**: Agent A (ARCHITECT)
> **Input**: SRS.md v2.0, SAD.md v2.0, archive/phase1/02-architecture/adr/ADR.md v1.0
> **Supersedes (partial)**: archive/phase1/02-architecture/adr/ADR.md entries noted per ADR below

> **Phase 1 ADRs in effect**: ADR-001 through ADR-012 (see archive/phase1/02-architecture/adr/ADR.md) remain
> accepted unless explicitly superseded or extended below.

---

## Index

| ADR-ID     | Title                                                            | Status   | Citation Anchor                  |
|------------|------------------------------------------------------------------|----------|----------------------------------|
| ADR-P2-01  | Hybrid Knowledge Layer V2 — four-tier with RRF k=60             | Accepted | [→](#adr-p2-01)                  |
| ADR-P2-02  | pgvector ivfflat index — lists=100 for RAG retrieval             | Accepted | [→](#adr-p2-02)                  |
| ADR-P2-03  | Embedding model `paraphrase-multilingual-MiniLM-L12-v2` (384-dim) | Accepted | [→](#adr-p2-03)                |
| ADR-P2-04  | L3 Prompt Injection Defense — Sandwich + 10 regex patterns       | Accepted | [→](#adr-p2-04)                  |
| ADR-P2-05  | L3 LLM execution order — check_input → LLM → grounding-on-output | Accepted | [→](#adr-p2-05)                 |
| ADR-P2-06  | EmotionClassifier strategy — Option A rule-based lexicon         | Accepted | [→](#adr-p2-06)                  |
| ADR-P2-07  | Emotion decay half-life = 24 hours                               | Accepted | [→](#adr-p2-07)                  |
| ADR-P2-08  | DST as 7-state machine with max 3 slot-filling rounds            | Accepted | [→](#adr-p2-08)                  |
| ADR-P2-09  | Grounding threshold = 0.75 cosine similarity                     | Accepted | [→](#adr-p2-09)                  |
| ADR-P2-10  | Escalation priority-to-reason mapping                            | Accepted | [→](#adr-p2-10)                  |
| ADR-P2-11  | Phase 1 modules extended via inheritance, not replacement        | Accepted | [→](#adr-p2-11)                  |
| ADR-P2-12  | Database — incremental migration: two new tables + column activation | Accepted | [→](#adr-p2-12)              |
| ADR-P2-13  | Observability — Prometheus only in Phase 2; OpenTelemetry deferred | Accepted | [→](#adr-p2-13)               |

---

## ADR-P2-01

### Title: Hybrid Knowledge Layer V2 — four-tier architecture with RRF k=60

### Status
Accepted

### Context
Phase 1 Knowledge Layer activated only Layer 1 (SQL rule match) and Layer 4 (human escalation), achieving a First Contact Resolution (FCR) rate of ~50% (SAD.md:27, §1.1). SRS FR-19 (SRS.md:139–167) requires a full four-layer architecture to reach 80% FCR (NFR-07). Two design questions arose: (1) how to fuse L1 rule results and L2 RAG results before deciding whether to call the LLM; (2) what confidence thresholds gate each layer's fast-return.

Alternatives considered for L1+L2 fusion: simple max-score selection, score-weighted linear combination, Reciprocal Rank Fusion (RRF).

### Decision
Implement **HybridKnowledgeV2** (`src/omnibot/knowledge/v2.py`) as a four-layer cascade with the following distribution and thresholds (SAD.md:27, §1.1; SAD.md:523–537, §3.9):

| Layer | Strategy | Expected contribution | Fast-return threshold |
|-------|----------|-----------------------|-----------------------|
| L1 | SQL rule match (ILIKE + ANY(keywords)) | 40% | confidence > 0.9 → return immediately (`source="rule"`) |
| L2 | RAG pgvector cosine search (Top-5) | 40% | — |
| L1+L2 | **RRF fusion** `_reciprocal_rank_fusion(k=60)` → Top-3 | — | RRF Top-1 confidence > 0.7 → return (`source="rag"`) |
| L3 | LLM generation + Sandwich Prompt + Grounding check | 10% | grounded=True → return (`source="llm"`) |
| L4 | Human escalation | 10% | fallback when L1–L3 all fail |

RRF score formula: for each document id, accumulate `1 / (rank + k)` across all result lists; sort descending; return Top-3.

### Rationale
- RRF k=60 is a well-established fusion constant (Robertson & Zaragoza, 2009) that dampens noise from low-ranked results; it outperforms linear combination for heterogeneous result lists (SQL ranking vs. cosine distance)
- Threshold 0.9 on L1 enables fast-path return (~10ms) without invoking the embedding pipeline for high-confidence rule matches
- Threshold 0.7 post-RRF balances false-acceptance risk vs. unnecessary LLM escalation
- The 40/40/10/10 split is a target distribution; actual traffic splits emerge from threshold calibration against the 500-entry golden dataset (FR-24)

### Consequences
- **Positive**: FCR uplift from 50% → 80%; two fast-exit paths before the expensive LLM path; RRF k is externally configurable
- **Negative**: `_reciprocal_rank_fusion()` introduces a second retrieval stage; all L2 RAG results (Top-5) must be held in memory through the RRF step before thresholding

**Citations**: SAD.md:15–28 (§1.1), SAD.md:496–541 (§3.9); SRS.md:139–167 (FR-19)

---

## ADR-P2-02

### Title: pgvector ivfflat index — lists=100 for RAG retrieval

### Status
Accepted

### Context
Phase 2 activates vector similarity search on `knowledge_base.embeddings vector(384)` (pre-provisioned in Phase 1, see ADR-002). Without an index, pgvector performs a sequential scan that exceeds the p95 < 1.5 s budget (NFR-08) at the target corpus size of 10K entries. Two pgvector index types are available: **ivfflat** (Inverted File with Flat quantization) and **hnsw** (Hierarchical Navigable Small World).

### Decision
Create an **ivfflat** index with `lists=100` and `vector_cosine_ops` distance (SAD.md:859–863, §5.1.3):

```sql
CREATE INDEX idx_kb_embeddings ON knowledge_base
    USING ivfflat (embeddings vector_cosine_ops)
    WITH (lists = 100);
```

hnsw deferred to Phase 3.

### Rationale
- **Build speed**: ivfflat index build is O(n) vs. hnsw O(n log n); at 10K entries, ivfflat builds in seconds vs. minutes for hnsw
- **Query latency**: ivfflat with lists=100 achieves < 200 ms cosine query at 10K entries (SRS.md:257–258), meeting the NFR-08 p95 < 1.5 s requirement
- **Operational simplicity**: ivfflat requires only `lists` to tune; hnsw requires tuning both `m` and `ef_construction`, adding Phase 2 operational complexity without a demonstrated need
- **Scale headroom**: hnsw's recall and throughput advantages manifest at >> 100K entries; Phase 2 corpus target is 10K
- `lists=100` is the pgvector-recommended starting value for a corpus in the low-thousands-to-tens-of-thousands range

### Consequences
- **Positive**: Sub-200ms RAG query latency at target scale; single parameter to tune; forward-only Alembic migration (`CREATE INDEX` is non-destructive)
- **Negative**: Recall degrades at higher `probes` / larger corpus; migration to hnsw in Phase 3 requires dropping and rebuilding the index during a maintenance window

**Citations**: SAD.md:858–866 (§5.1.3); SRS.md:234–264 (FR-23), SRS.md:256–258

---

## ADR-P2-03

### Title: Embedding model `paraphrase-multilingual-MiniLM-L12-v2` (384-dim)

### Status
Accepted

### Context
Layer 2 RAG and Layer 5 Grounding Check both require a text embedding model. OmniBot serves Chinese (ZH) and English (EN) users. Model selection must balance multilingual capability, model size (affects startup time and memory), embedding dimensionality (affects index size), and inference latency.

Candidates evaluated:

| Model | Languages | Dim | Size | CPU inference |
|-------|-----------|-----|------|---------------|
| `paraphrase-multilingual-MiniLM-L12-v2` | 50+ (ZH+EN) | 384 | ~120 MB | ~50 ms |
| `text-embedding-ada-002` (OpenAI API) | Multilingual | 1536 | N/A (API) | ~100–300 ms |
| `multilingual-e5-large` | 100+ | 1024 | ~560 MB | ~200 ms |

### Decision
Use **`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`** for both HybridKnowledgeV2 (SAD.md:501–503, §3.9) and GroundingChecker (SAD.md:580–581, §3.10). A single model instance is loaded once at application startup and shared between both modules.

Embed dimensionality = **384**, aligning with the pre-provisioned `knowledge_base.embeddings vector(384)` column (ADR-002) without requiring an `ALTER TABLE`.

Cross-model safety is enforced by filtering on `embedding_model = 'paraphrase-multilingual-MiniLM-L12-v2'` in all vector queries (SAD.md:526, §3.9), preventing silently incorrect results if the model is later swapped.

### Rationale
- ZH+EN multilingual coverage meets the OmniBot user base requirement
- ~120 MB footprint fits a single-node Docker container; no GPU required
- 384-dim exactly matches the pre-provisioned schema — no ALTER TABLE, preserving ADR-002
- ~50 ms CPU inference is accounted for in the p95 < 1.5 s latency budget (NFR-08); the model is loaded once at startup, not per-request
- External API models (ada-002) introduce network latency, rate limits, and cost that violate the zero-external-vector-service constraint (ADR-002)

### Consequences
- **Positive**: No schema migration; zero API cost; single startup load; shared instance between RAG and Grounding reduces memory footprint
- **Negative**: Future model upgrade (Phase 3) requires re-embedding the entire `knowledge_base`; the `embedding_model` column filter is the safety gate — all insertions must set this column correctly

**Citations**: SAD.md:496–541 (§3.9), SAD.md:543–582 (§3.10); SRS.md:139–167 (FR-19), SRS.md:191–211 (FR-21)

---

## ADR-P2-04

### Title: L3 Prompt Injection Defense — Sandwich Defense + 10 regex patterns

### Status
Accepted

### Context
SRS FR-15 (SRS.md:37–61) requires detection and blocking of prompt injection attacks before any text reaches the LLM. Phase 1 InputSanitizerL2 performs only NFKC normalization and control character stripping (FR-04); it has no security semantics. A question arose about responsibility boundaries: should L2 Sanitizer be extended with security patterns, or should injection defense be a separate pipeline stage?

### Decision
**Layer 2 (InputSanitizerL2) retains NFKC normalization only.** A new **Layer 3 (`PromptInjectionDefense`)** owns all security logic: 10-pattern regex detection + Sandwich Prompt wrapping (SAD.md:307–349, §3.6; SRS.md:37–61, FR-15).

The 10 case-insensitive patterns (compiled against NFKC-normalized text) are:

1. `ignore\s+(previous|above|all)\s+(instructions?|prompts?)`
2. `system\s*:\s*`
3. `` ```\s*(system|admin|root) ``
4. `you\s+are\s+now\s+`
5. `pretend\s+(you|to)\s+`
6. `act\s+as\s+(a\s+)?`
7. `forget\s+(everything|all|your)`
8. `new\s+instructions?\s*:`
9. `override\s+(your|the|all)`
10. `disregard\s+(your|the|all|previous)`

Any match → `SecurityCheckResult(is_safe=False, risk_level="high")` → blocked request logged to `security_logs(layer="L3", blocked=TRUE)`.

`build_sandwich_prompt()` wraps safe inputs with structure: `[SYSTEM INSTRUCTION] → [RETRIEVED CONTEXT] → [USER MESSAGE] → [SYSTEM REMINDER]`.

### Rationale
- **Separation of concerns**: L2 is a character-level normalizer; mixing security pattern matching into it would violate single-responsibility and make L2 harder to test. OWASP LLM01 (Prompt Injection) is a distinct threat requiring its own auditable layer
- **NFKC-before-match ordering**: applying normalization before regex ensures Unicode homoglyph attacks (e.g., fullwidth characters) are canonicalized before pattern evaluation, eliminating a common bypass vector
- **Sandwich Defense**: placing the system reminder after the user message closes the "last instruction wins" attack surface — attackers cannot append override instructions after the reminder

### Consequences
- **Positive**: L2 remains a pure normalizer; L3 is independently auditable; blocked-request logging is isolated to one module; NFR-12 (>= 95% block rate) is achievable against the 10-pattern red-team set
- **Negative**: Two pipeline stages now touch text normalization (L2 and L3 both call NFKC); L3 must be the authoritative source of blocked_reason for security incident analysis

**Citations**: SAD.md:307–349 (§3.6), SAD.md:243–258 (§3.3); SRS.md:37–61 (FR-15)

---

## ADR-P2-05

### Title: L3 LLM execution order — check_input → sandwich+LLM → grounding-on-output

### Status
Accepted

### Context
SRS FR-19 (SRS.md:157–163) describes Layer 3 LLM generation steps but lists them in an order that is logically inconsistent: the original FR-19 draft implied `GroundingChecker.check()` should execute *before* the LLM call. `GroundingChecker.check(llm_output, source_texts)` requires `llm_output` as its first argument — the LLM output cannot exist before the LLM call. This ambiguity was flagged during SAD review round 1 and needed an explicit architectural resolution.

### Decision
The **strictly ordered** L3 execution sequence within `HybridKnowledgeV2._llm_generate()` is (SAD.md:528–536, §3.9; SAD.md:740–750, §4.1):

1. `PromptInjectionDefense.check_input(query)` → `is_safe=False` → return `BlockedResult` immediately; do NOT call LLM
2. Retrieve `source_texts` from L1 + L2 results (already available from prior pipeline stages)
3. `build_sandwich_prompt(system_instruction, query, context)` — wraps `source_texts` as sandwich context
4. **Call LLM** (with timeout + retry); timeout or empty response → fallthrough to L4
5. `GroundingChecker.check(llm_output, source_texts)` — applied to the **generated output** (step 4 must precede step 5)
6. `grounded=True` → return `KnowledgeResult(source="llm")`
7. `grounded=False` → return `None` → fallthrough to L4

**SAD Conformance Constraint**: Any implementation reversing steps 4 and 5 is non-conformant. Steps 4 then 5 are strictly ordered.

### Rationale
- `GroundingChecker.check(llm_output, source_texts)` is logically impossible before the LLM call — `llm_output` does not exist until step 4 completes
- Placing injection check (step 1) before the LLM call ensures adversarial inputs are blocked before any LLM cost is incurred
- The sandwich prompt (step 3) encapsulates both the source context and the injection-safe user message, so the LLM call at step 4 already operates on a secured, grounded context
- This ordering resolves the SRS FR-19 ambiguity and becomes the normative specification; all test cases must verify this sequence

### Consequences
- **Positive**: Logical consistency enforced at architecture level; clear failure modes (blocked vs. ungrounded vs. timeout each fall through to L4); no LLM cost on injection-blocked inputs
- **Negative**: `source_texts` must be materialized before step 3, meaning L1+L2 results are always computed even when L3 is eventually invoked (no lazy evaluation shortcut)

**Citations**: SAD.md:496–541 (§3.9), SAD.md:729–762 (§4.1); SRS.md:139–167 (FR-19, lines 157–163)

---

## ADR-P2-06

### Title: EmotionClassifier strategy — Option A rule-based lexicon for Phase 2

### Status
Accepted

### Context
SRS FR-17 (SRS.md:87–106) requires sentiment classification of each user message into POSITIVE / NEUTRAL / NEGATIVE with an intensity score. Three implementation strategies were evaluated for Phase 2 (SAD.md:406–414, §3.7):

| Option | Strategy | Latency | External dep |
|--------|----------|---------|--------------|
| **A** | Keyword lexicon: matched keyword count × 0.2, capped at 1.0 | ~0 ms | None |
| B | Pretrained transformer `cardiffnlp/twitter-xlm-roberta-base-sentiment` | ~400 ms CPU | HuggingFace model (~500 MB) |
| C | LLM call sharing Layer 3 infrastructure | ~200 ms | LLM API |

### Decision
Adopt **Option A — rule-based keyword lexicon** for Phase 2. POSITIVE keywords: `謝謝, 好的, 太棒了, 滿意, great, thank`; NEGATIVE keywords: `問題, 投訴, 憤怒, 差勁, terrible, complaint`. Intensity = `matched_keyword_count × 0.2`, capped at 1.0. No match → NEUTRAL, intensity = 0.0 (SAD.md:410, §3.7).

### Rationale
- **Latency**: Option A adds ~0 ms to the pipeline; Options B and C add 200–400 ms, which — combined with other pipeline stages — would threaten the p95 < 1.5 s target (NFR-08; SRS.md:305–309)
- **Zero external dependencies**: Option A is pure-Python; Option B requires downloading a ~500 MB model with a separate startup penalty; Option C adds LLM API calls and cost
- **Sufficient for Phase 2 scope**: EmotionTracker uses emotion history primarily for consecutive-negative escalation detection (threshold: 3 consecutive negatives), not fine-grained sentiment analysis. A binary POS/NEG/NEU classifier with intensity is adequate for this use case
- Options B and C are explicitly deferred to Phase 3 (SAD.md:412–413, §3.7) when higher accuracy is justified by FCR analysis

### Consequences
- **Positive**: Zero latency cost; no model download; lexicon is auditable and easily extended with new keywords; meets p95 budget
- **Negative**: No semantic understanding — paraphrases, sarcasm, and dialect expressions outside the lexicon will be classified as NEUTRAL; accuracy ceiling is lower than transformer models

**Citations**: SAD.md:396–422 (§3.7); SRS.md:87–106 (FR-17)

---

## ADR-P2-07

### Title: Emotion decay half-life = 24 hours

### Status
Accepted

### Context
`EmotionTracker.current_weighted_score()` applies exponential decay so that older emotion scores contribute less to the current emotional context. The decay formula is `decay = e^(-0.693 × hours_ago / half_life_hours)` (SRS.md:97, FR-17). The half-life value determines how quickly past emotional context fades: too short (e.g., 1 hour) and the system forgets a user's distress within a single session; too long (e.g., 7 days) and old grievances persist and may incorrectly trigger escalation on a new session.

### Decision
Set `half_life_hours = 24.0` as the default for `EmotionTracker` (SAD.md:388–391, §3.7; SRS.md:103, FR-17). The value is **overridable via constructor** to allow per-tenant configuration in future phases.

### Rationale
- 24 hours aligns with a natural daily cycle: emotion context from a previous day's interaction decays to 50% weight by the following day, avoiding carrying yesterday's distress into a fresh session while still retaining same-session emotional history at full weight
- A configurable `half_life_hours` parameter avoids hardcoding, enabling future tenant-level customization (e.g., a high-stakes financial services tenant may prefer a 48-hour half-life)
- The escalation trigger (`consecutive_negative_count >= 3`) is count-based, not score-based, so the decay primarily affects `current_weighted_score()` used for trend reporting rather than the escalation gate itself

### Consequences
- **Positive**: Reasonable recency bias; configurable for future tenants; formula is deterministic and testable
- **Negative**: 24 hours is an empirical default, not derived from user research; may require recalibration based on Phase 2 production data

**Citations**: SAD.md:354–422 (§3.7); SRS.md:87–106 (FR-17, lines 96–103)

---

## ADR-P2-08

### Title: DST as 7-state machine with max 3 slot-filling rounds

### Status
Accepted

### Context
SRS FR-18 (SRS.md:110–136) requires a Dialogue State Tracker (DST) with intent detection and slot filling. Key design questions: (1) what states adequately represent the dialogue lifecycle without over-engineering; (2) what bounds user frustration during slot filling; (3) what triggers automatic escalation when slot filling stalls.

### Decision
Implement `ConversationState` as a **7-state enum** (SAD.md:432–440, §3.8):

```
IDLE → INTENT_DETECTED → SLOT_FILLING ↔ AWAITING_CONFIRMATION → PROCESSING → RESOLVED
                    ↘                    ↘                       ↘
                 ESCALATED          ESCALATED                 ESCALATED
```

Full transition table (SRS.md:121–131, FR-18):

| From | To | Trigger |
|------|----|---------|
| `IDLE` | `INTENT_DETECTED` | message received |
| `INTENT_DETECTED` | `PROCESSING` | all required slots filled |
| `INTENT_DETECTED` | `SLOT_FILLING` | missing required slots |
| `SLOT_FILLING` | `AWAITING_CONFIRMATION` | all required slots filled |
| `SLOT_FILLING` | **`ESCALATED`** | `turn_count >= 3` AND missing slots remain |
| `AWAITING_CONFIRMATION` | `PROCESSING` | user confirms |
| `AWAITING_CONFIRMATION` | `SLOT_FILLING` | user denies |
| `PROCESSING` | `RESOLVED` | successful reply |
| `PROCESSING` | **`ESCALATED`** | confidence < 0.65 |
| `ESCALATED` | `RESOLVED` | human intervention |

The **3-round maximum** is enforced by `turn_count >= 3` in the `SLOT_FILLING → ESCALATED` transition.

`DialogueState.transition()` is **immutable**: returns a new `DialogueState` object with `turn_count += 1` and `last_updated = datetime.utcnow()`.

### Rationale
- 7 states capture the complete happy path and all failure modes without unnecessary complexity; fewer states (e.g., collapsing SLOT_FILLING and AWAITING_CONFIRMATION) would lose the confirmation handshake required for multi-slot intents
- The 3-round bound prevents infinite slot-filling loops that frustrate users; after 3 failed attempts, human escalation is the correct fallback (observable failure mode with a defined SLA via `EscalationManagerV2`)
- Immutable `transition()` makes state history auditable and simplifies concurrent access patterns

### Consequences
- **Positive**: Bounded user friction; all failure paths terminate at ESCALATED (observable); immutable state is safe to serialize to `conversations.dst_state` JSONB
- **Negative**: 3-round limit may be too aggressive for complex multi-slot intents; the value is hardcoded in the transition rule rather than configurable (Phase 3 backlog item)

**Citations**: SAD.md:424–491 (§3.8); SRS.md:110–136 (FR-18)

---

## ADR-P2-09

### Title: Grounding threshold = 0.75 cosine similarity

### Status
Accepted

### Context
`GroundingChecker.check(llm_output, source_texts)` computes maximum cosine similarity between the LLM-generated output and the retrieval source texts, then applies a binary threshold: `grounded=True` if `max_score >= threshold`, `grounded=False` otherwise (SAD.md:565–578, §3.10). An ungrounded response falls through to L4 human escalation — the user never receives an ungrounded LLM response (NFR-13; SRS.md:342–347). The threshold value is the primary tuning parameter: too low (e.g., 0.5) accepts hallucinations; too high (e.g., 0.95) rejects valid paraphrases and degrades FCR.

### Decision
Set `GroundingChecker` default `threshold = 0.75` (SAD.md:557–560, §3.10; SRS.md:197, FR-21). The threshold is **overridable via constructor**.

### Rationale
- 0.75 is an empirically chosen balance for `paraphrase-multilingual-MiniLM-L12-v2` at 384-dim: it is above the typical noise floor for unrelated ZH/EN sentence pairs (~0.3–0.5) and below the near-duplicate threshold (~0.95)
- Multilingual models have slightly lower same-language alignment scores than monolingual models; 0.75 was selected (rather than a higher threshold used for monolingual EN models) to accommodate cross-lingual paraphrase cases where ZH source is compared to an EN LLM output
- NFR-13 requires 100% coverage: every L3 LLM output must pass through the check. Setting the threshold as a constructor parameter allows future offline calibration against the golden dataset (FR-24) without a code change

### Consequences
- **Positive**: 100% LLM output verification is architecturally guaranteed (no code path bypasses grounding on the L3 path); threshold is recalibratable without code change
- **Negative**: 0.75 is an empirical baseline; it may produce false rejections for legitimate LLM outputs on low-resource ZH dialects or domain-specific vocabulary not well-represented in the MiniLM training corpus

**Citations**: SAD.md:543–582 (§3.10); SRS.md:191–211 (FR-21), SRS.md:342–347 (NFR-13)

---

## ADR-P2-10

### Title: Escalation priority-to-reason mapping

### Status
Accepted

### Context
SRS FR-20 (SRS.md:170–188) specifies `EscalationManagerV2` with three SLA tiers (`SLA_BY_PRIORITY = {0: 30, 1: 15, 2: 5}` minutes) and three `reason` codes (`out_of_scope`, `low_confidence`, `emotion_trigger`). However, FR-20 does not specify which reason maps to which priority level. This mapping is an architectural decision with direct user-impact consequences (SAD.md:616–619, §3.11).

This ADR also resolves the Round-1 review LOW gap: "FR-20 traceability incomplete — priority-to-reason assignment undocumented."

### Decision
The authoritative **priority-to-reason mapping** is (SAD.md:617–619, §3.11):

| Priority | Level | SLA | Reason | Trigger |
|----------|-------|-----|--------|---------|
| 2 | urgent | 5 min | `emotion_trigger` | `EmotionTracker.should_escalate()` — consecutive_negative >= 3 |
| 1 | high | 15 min | `low_confidence` | DST confidence < 0.65 OR HybridKnowledgeV2 L4 fallthrough |
| 0 | normal | 30 min | `out_of_scope` | General L4 fallthrough with no emotional context |

Configured as `SLA_BY_PRIORITY: dict[int, int] = {0: 30, 1: 15, 2: 5}`.

### Rationale
The mapping is ordered by user-impact severity:
1. **emotion_trigger → urgent (2)**: User is in active emotional distress (3+ consecutive negative signals); immediate human intervention minimizes harm and prevents churn. Five-minute SLA reflects the highest user-welfare urgency
2. **low_confidence → high (1)**: User is actively blocked — the system cannot answer their query. Fifteen-minute SLA ensures timely resolution of a service gap
3. **out_of_scope → normal (0)**: User inquiry is outside the bot's domain; the request is deferred, not blocked. Thirty-minute SLA is appropriate for a non-urgent referral

This ordering is not constrained by FR-20 (which only specifies the SLA values, not the mapping) and is therefore an architectural decision requiring explicit documentation.

### Consequences
- **Positive**: Explicit documented mapping; configurable via `SLA_BY_PRIORITY` dict for future tenant customization; closes the Round-1 FR-20 traceability gap
- **Negative**: The mapping assumes emotion distress is always higher severity than a knowledge gap; this ordering may need revision for low-empathy support domains (e.g., automated billing queries where emotional context is less relevant)

**Citations**: SAD.md:586–621 (§3.11); SRS.md:170–188 (FR-20)

---

## ADR-P2-11

### Title: Phase 1 modules extended via inheritance, not replacement

### Status
Accepted

### Context
Phase 2 upgrades three Phase 1 modules (PIIMasking, EscalationManager, KnowledgeBase) and adds four new platform adapters to the VERIFIERS registry. Two extension strategies were considered: (1) replace Phase 1 modules in-place (modify existing files); (2) extend via Python class inheritance into new `v2.py` sibling files.

### Decision
All Phase 2 module upgrades use **Python class inheritance into new sibling files** with no modification to Phase 1 source files (SAD.md:1214–1271, §9):

| Phase 1 Module | Phase 2 Extension | Extension Point |
|----------------|------------------|-----------------|
| `PIIMasking` (`pii/__init__.py:13`) | `PIIMaskingV2` (`pii/v2.py`) | Subclass, adds `credit_card` + `_luhn_check()` |
| `EscalationManager` (`escalation/__init__.py:30`) | `EscalationManagerV2` (`escalation/v2.py`) | Subclass, activates `sla_deadline`, adds SLA priority logic |
| `KnowledgeBase` (`knowledge/__init__.py:25`) | `HybridKnowledgeV2` (`knowledge/v2.py`) | Subclass, adds L2 RAG + L3 LLM + RRF on top of L1 |
| `VERIFIERS` dict | `VERIFIERS["messenger"]`, `VERIFIERS["whatsapp"]` | Module-level registration at import time |

New standalone modules (EmotionTracker, DialogueStateTracker, GroundingChecker, PrometheusMetrics) are placed in new directories with no Phase 1 parent.

### Rationale
- **No breaking changes**: Phase 1 regression test suite remains valid — all Phase 1 module paths, class names, and public API signatures are unchanged
- **Auditability**: Phase 2 changes are isolated to `v2.py` sibling files; a diff of Phase 1 source shows zero changes, making security review of Phase 1 baseline straightforward
- **Open-Closed Principle**: Phase 1 modules are closed for modification, open for extension — aligns with ADR-005's registry pattern

### Consequences
- **Positive**: Full Phase 1 test suite passes without modification; Phase 2 modules have independent test files; rollback of a Phase 2 module does not affect Phase 1 behavior
- **Negative**: Two versions of some modules coexist (e.g., `PIIMasking` and `PIIMaskingV2`); callers must be updated to reference the V2 class; over multiple phases, the inheritance chain may become deep

**Citations**: SAD.md:1214–1271 (§9.1–§9.4); SRS.md:19–35 (FR-14), SRS.md:65–83 (FR-16), SRS.md:139–167 (FR-19), SRS.md:170–188 (FR-20)

---

## ADR-P2-12

### Title: Database — incremental migration via two new tables + two column activations

### Status
Accepted

### Context
Phase 2 requires new persistence for emotion history (FR-17), edge cases (FR-23/FR-24), and a vector index for RAG (FR-23). Additionally, three columns pre-declared in Phase 1 (`conversations.dst_state`, `messages.knowledge_source`, `escalation_queue.sla_deadline`) need to be activated. The migration approach must preserve Phase 1 data integrity and be reversible if Phase 2 is rolled back. See ADR-011 (Alembic) for the migration toolchain.

### Decision
Phase 2 database changes are **non-destructive and additive** only (SAD.md:1272–1281, §9.5):

**New tables** (Alembic scripts 0002–0003):
- `emotion_history` — `CREATE TABLE` + `CREATE INDEX idx_emotion_user`
- `edge_cases` — `CREATE TABLE`

**New index** (Alembic script 0004):
- `CREATE INDEX idx_kb_embeddings ON knowledge_base USING ivfflat (embeddings vector_cosine_ops) WITH (lists = 100)`

**Column activations** (no ALTER required):
- `conversations.dst_state JSONB` — pre-declared NULL in Phase 1; Phase 2 `DialogueStateTracker` starts writing to it
- `messages.knowledge_source VARCHAR` — pre-declared NULL in Phase 1; Phase 2 `HybridKnowledgeV2` starts writing to it
- `escalation_queue.sla_deadline TIMESTAMPTZ` — pre-declared NULL in Phase 1; Phase 2 `EscalationManagerV2.create()` starts writing to it

**No `DROP TABLE`, no `ALTER COLUMN TYPE`, no `ALTER COLUMN NOT NULL`** on existing columns.

Alembic autogenerate remains disabled (per ADR-011) because `ivfflat` is not recognized by SQLAlchemy's reflection layer.

### Rationale
- **Forward-only migrations**: `CREATE TABLE` and `CREATE INDEX` are non-destructive; Phase 2 can be deployed without a schema rollback risk for Phase 1 tables
- **Pre-declared columns**: Phase 1 deliberately reserved `dst_state`, `knowledge_source`, and `sla_deadline` as nullable columns (ADR-002) precisely to avoid ALTER TABLE in Phase 2 — this strategy is now exercised
- **Alembic version control**: three discrete migration scripts (`0002`, `0003`, `0004`) provide granular rollback capability and CI validation via `alembic upgrade head`

### Consequences
- **Positive**: Zero risk to Phase 1 relational data; migration is run-in-place with no downtime on existing tables; rollback is possible by dropping Phase 2 tables and index
- **Negative**: The three pre-declared nullable columns remain NULL for any record created before Phase 2 deployment, requiring `IS NULL` guards in Phase 2 query logic for backwards compatibility

**Citations**: SAD.md:810–878 (§5), SAD.md:1272–1281 (§9.5); SRS.md:234–264 (FR-23)

---

## ADR-P2-13

### Title: Observability — Prometheus metrics only in Phase 2; OpenTelemetry deferred

### Status
Accepted

### Context
Phase 2 adds five new pipeline stages (Injection Defense, EmotionTracker, DST, HybridKnowledgeV2, GroundingChecker) and upgrades two (PIIMaskingV2, EscalationManagerV2). Comprehensive observability requires both metrics (counters, histograms, gauges) and distributed traces. Full observability stack options evaluated: (A) Prometheus metrics only; (B) OpenTelemetry SDK with Prometheus + Jaeger/Tempo traces + Grafana dashboards; (C) Prometheus + lightweight span logging.

### Decision
Phase 2 implements **Prometheus metrics only** via `PrometheusMetrics` (`src/omnibot/metrics/__init__.py`), exposing 8 instruments at `GET /metrics` (SAD.md:624–653, §3.12). **OpenTelemetry tracing and Grafana dashboards are deferred to Phase 3** (SRS.md:364–376, Out-of-Scope table).

The 8 instruments cover all Phase 2 KPIs:

| Metric | Type | Purpose |
|--------|------|---------|
| `omnibot_response_duration_seconds` | Histogram | p95 latency per platform (NFR-08) |
| `omnibot_requests_total` | Counter | Request volume + error rate |
| `omnibot_fcr_total` | Counter | First Contact Resolution (NFR-07) |
| `omnibot_knowledge_hit_total` | Counter | Layer distribution (L1/L2/L3/L4) |
| `omnibot_pii_masked_total` | Counter | PII masking coverage (NFR-11) |
| `omnibot_escalation_queue_size` | Gauge | Queue depth for SLA monitoring (NFR-14) |
| `omnibot_emotion_escalation_total` | Counter | Emotion-triggered escalation count |
| `omnibot_llm_tokens_total` | Counter | LLM cost tracking (input/output) |

### Rationale
- **Scope discipline**: The 8-metric set is sufficient to validate all Phase 2 NFRs (NFR-07 through NFR-14) without over-engineering; adding OpenTelemetry SDK in Phase 2 would introduce ~2 weeks of instrumentation + Grafana dashboard work outside the Phase 2 scope boundary
- **Prometheus-native**: `prometheus_client` integrates with FastAPI via a single `GET /metrics` route, requiring no external collector in Phase 2; existing ops tooling (if any) can scrape it immediately
- **Incremental**: OpenTelemetry and Grafana dashboards are explicit Phase 3 items (SRS.md:367–368); deferring them does not block any Phase 2 acceptance criteria

### Consequences
- **Positive**: Phase 2 observability is complete for all KPI measurements; zero additional infrastructure services required; Prometheus metrics compose cleanly with Phase 3 OTel traces (both use the same instrument names)
- **Negative**: No distributed traces in Phase 2 — root-cause analysis of cross-layer latency regressions requires log correlation rather than trace visualization; Grafana alerting rules must be manually written in Phase 3

**Citations**: SAD.md:624–653 (§3.12); SRS.md:214–231 (FR-22), SRS.md:364–376 (Out-of-Scope)

---

*ADR.md v2.0 — OmniBot Phase 2 — Agent A (ARCHITECT) — 2026-05-17*
