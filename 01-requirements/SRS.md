# Software Requirements Specification — OmniBot

> **Project**: OmniBot — 多平台客服機器人
> **Phase**: 1 (MVP 基礎)
> **Version**: 1.0
> **Date**: 2026-05-13
> **Input**: SPEC/omnibot-phase-1.md v7.0

---

## Functional Requirements

### FR-01: Platform Adapter — Telegram + LINE Webhook

**Priority**: P0
**Description**: 系統必須接收來自 Telegram Bot API 和 LINE Messaging API 的 webhook 請求，轉換為內部統一消息格式（UnifiedMessage）。

**Acceptance Criteria**:
- `POST /api/v1/webhook/telegram` 正確解析 Telegram Update 物件
- `POST /api/v1/webhook/line` 正確解析 LINE WebhookEvent 物件
- 兩個端點均回傳 `200 OK` 於 3 秒內（不含下游處理）
- 不支援的平台請求回傳 `400 Bad Request`

**Input**: SPEC/omnibot-phase-1.md L106-L136, L319-L360

---

### FR-02: Webhook Signature Verification

**Priority**: P0
**Description**: 每個 webhook 請求必須先通過簽名驗證，未通過者拒絕處理。

**Acceptance Criteria**:
- Telegram webhook 使用 SHA256( bot_token ) 作為 secret key 進行 HMAC 比對
- LINE webhook 使用 channel_secret 進行 HMAC-SHA256 + Base64 比對
- 驗證失敗回傳 `401 AUTH_INVALID_SIGNATURE`
- `hmac.compare_digest()` 防禦時序攻擊
- 支援新增平台驗證器（`VERIFIERS` dict 註冊）

**Input**: SPEC/omnibot-phase-1.md L276-L313

---

### FR-03: Unified Message Format

**Priority**: P0
**Description**: 所有平台消息必須轉換為統一的 `UnifiedMessage` dataclass，對下游模組隱藏平台差異。

**Acceptance Criteria**:
- `UnifiedMessage` 為 `frozen=True` dataclass，欄位包含 platform / platform_user_id / unified_user_id / message_type / content / raw_payload / received_at
- `Platform` enum 預定義 `TELEGRAM`, `LINE`, `MESSENGER`, `WHATSAPP`（後兩者 Phase 2 啟用）
- `MessageType` enum 包含 `TEXT`, `IMAGE`, `STICKER`, `LOCATION`, `FILE`
- `UnifiedResponse` 包含 content / source / confidence / knowledge_id

**Input**: SPEC/omnibot-phase-1.md L319-L360

---

### FR-04: Input Sanitizer L2 — Character Normalization

**Priority**: P1
**Description**: 所有使用者輸入文字必須經過 NFKC 正規化，移除非列印控制字元。

**Acceptance Criteria**:
- 輸入文字經過 `unicodedata.normalize("NFKC", text)`
- 移除所有非列印字元（保留 `\n`, `\t`）
- 結果 `strip()` 移除前後空白
- 不執行 pattern matching（Phase 2 L3 負責）

**Input**: SPEC/omnibot-phase-1.md L364-L379

---

### FR-05: PII Masking L4 — Phone / Email / Address

**Priority**: P1
**Description**: 使用者訊息中的台灣電話、Email、地址必須在記錄或輸出前遮蔽。敏感關鍵字觸發轉接。

**Acceptance Criteria**:
- 電話格式 `0XXX-XXX-XXX` 或 10-11 位連續數字 → `[phone_masked]`
- Email 格式 → `[email_masked]`
- 台灣地址（縣市 + 路/街/巷/弄/號/樓）→ `[address_masked]`
- 從後往前替換避免索引偏移
- `should_escalate()` 偵測敏感關鍵字（密碼、銀行帳戶、信用卡號、提款卡）
- 回傳 `PIIMaskResult(masked_text, mask_count, pii_types)`

**Input**: SPEC/omnibot-phase-1.md L383-L435

---

### FR-06: Rate Limiter — Token Bucket

**Priority**: P1
**Description**: 每個平台用戶必須有獨立的請求速率限制，防止濫用。

**Acceptance Criteria**:
- `TokenBucket` 支援 capacity 與 refill_rate 設定
- `consume()` 回傳 bool：token 足夠時扣減並回傳 True，不足回傳 False
- `RateLimiter` 以 `platform:user_id` 為 key 管理獨立 bucket
- 預設 `default_rps=100`
- 超出限制的請求回傳 `429 RATE_LIMIT_EXCEEDED`

**Input**: SPEC/omnibot-phase-1.md L440-L484

---

### FR-07: Knowledge Layer V1 — Rule Match + Escalate

**Priority**: P0
**Description**: 查詢知識庫時先執行 SQL 精確/模糊匹配（Layer 1），信心度 > 0.7 直接回覆，否則轉接人工。

**Acceptance Criteria**:
- SQL 使用 `ILIKE` 比對 question 欄位 + `ANY(keywords)` 比對關鍵字陣列
- 僅查詢 `is_active = TRUE` 的條目
- 精確匹配（query_text 完整出現於 question）信心度 0.95，部分匹配 0.7
- 結果依 version DESC 排序，取最高版本
- 無匹配 → `KnowledgeResult(id=-1, source="escalate")`

**Input**: SPEC/omnibot-phase-1.md L488-L546

---

### FR-08: Basic Escalation Manager — No SLA

**Priority**: P1
**Description**: 無法匹配的查詢必須進入轉接佇列，支援指派與結案。

**Acceptance Criteria**:
- `create()` 寫入 `escalation_queue` 表格，記錄 conversation_id + reason
- `assign()` 設定 assigned_agent + picked_at
- `resolve()` 設定 resolved_at
- Phase 1 無 SLA 追蹤（Phase 2 加入 sla_deadline）

**Input**: SPEC/omnibot-phase-1.md L552-L599

---

### FR-09: Structured Logger — JSON Format

**Priority**: P1
**Description**: 所有日誌必須以 JSON 結構化格式輸出，包含 timestamp / level / service / message。

**Acceptance Criteria**:
- 每行一條 JSON（NDJSON）
- 欄位包含 `timestamp`（ISO 8601 UTC）、`level`、`service`、`message`，其餘為 kwargs
- 支援 DEBUG / INFO / WARN / ERROR / CRITICAL 五級
- INFO: 業務事件（新對話、規則匹配成功）
- ERROR: 致命錯誤（DB 連線中斷）
- WARN: 非致命異常（低信心度匹配、PII 偵測）

**Input**: SPEC/omnibot-phase-1.md L605-L655

---

### FR-10: API Response Format — ApiResponse / PaginatedResponse

**Priority**: P1
**Description**: 所有 API 回應必須使用統一的 `ApiResponse[T]` 或 `PaginatedResponse[T]` 泛型格式。

**Acceptance Criteria**:
- `ApiResponse` 包含 success / data / error / error_code
- `PaginatedResponse` 繼承 ApiResponse，增加 total / page / limit / has_next
- 錯誤碼枚舉：`AUTH_INVALID_SIGNATURE`, `RATE_LIMIT_EXCEEDED`, `KNOWLEDGE_NOT_FOUND`, `VALIDATION_ERROR`, `INTERNAL_ERROR`

**Input**: SPEC/omnibot-phase-1.md L239-L271

---

### FR-11: Health Check Endpoint

**Priority**: P1
**Description**: 系統必須提供健康檢查端點供 Docker / 監控系統使用。

**Acceptance Criteria**:
- `GET /api/v1/health` 回傳 JSON `{status, postgres, redis, uptime_seconds}`
- status enum: `healthy` / `degraded` / `unhealthy`
- postgres 與 redis 為 bool 表示連線狀態

**Input**: SPEC/omnibot-phase-1.md L223-L237

---

### FR-12: Database Schema — All Core Tables

**Priority**: P0
**Description**: 必須建立所有核心資料表，包含 Phase 2/3 預留欄位，避免後續 ALTER TABLE。

**Acceptance Criteria**:
- `users` 表含 unified_user_id (UUID)、platform、platform_user_id，UNIQUE(platform, platform_user_id)
- `conversations` 表含 satisfaction_score、first_contact_resolution、scope_type、dst_state (JSONB)
- `messages` 表含 intent_detected、sentiment_category、sentiment_intensity、knowledge_source
- `knowledge_base` 表含 embeddings vector(384)、keywords TEXT[]、version
- `platform_configs` 表含 rate_limit_rps、webhook_secret_key_ref
- `escalation_queue` 表含 priority、sla_deadline (Phase 2 啟用)
- `user_feedback` 表含 feedback CHECK (thumbs_up / thumbs_down)
- `security_logs` 表含 layer、blocked、source_ip

**Input**: SPEC/omnibot-phase-1.md L658-L804

---

### FR-13: Docker Compose Development Environment

**Priority**: P2
**Description**: 提供一鍵啟動的開發環境，包含 API、PostgreSQL (pgvector)、Redis。

**Acceptance Criteria**:
- `docker compose up` 啟動 omnibot-api (port 8000)、postgres (pgvector/pg16)、redis (7-alpine)
- postgres 與 redis 有 healthcheck
- API 容器依賴 postgres 和 redis 的 healthy 狀態
- Redis 以密碼保護（`requirepass`）

**Input**: SPEC/omnibot-phase-1.md L848-L888

---

## Non-Functional Requirements

### NFR-01: First Contact Resolution (FCR) >= 50%

**Category**: Performance
**Description**: 以 30 天滾動窗口計算，in_scope 對話中 `first_contact_resolution = TRUE` 的比例需 >= 50%。
**Measurement**: ODD SQL 查詢 (SPEC/omnibot-phase-1.md L811-L822)

---

### NFR-02: p95 Response Latency < 3.0s

**Category**: Performance
**Description**: 從 webhook 接收到回覆發送之間，p95 延遲 < 3.0 秒。以 platform 分組計算。
**Measurement**: ODD SQL 查詢 (SPEC/omnibot-phase-1.md L824-L832)

---

### NFR-03: Platform Support — Telegram + LINE

**Category**: Compatibility
**Description**: Phase 1 支援 Telegram Bot API 與 LINE Messaging API 兩個平台。

---

### NFR-04: Webhook Verification 100%

**Category**: Security
**Description**: 每個 webhook 請求必須通過簽名驗證，不得有未驗證請求進入業務邏輯。

---

### NFR-05: JSON Structured Logging

**Category**: Observability
**Description**: 所有日誌必須為 JSON 結構化格式（NDJSON），含 timestamp / level / service / message。

---

### NFR-06: PII Masking Coverage

**Category**: Security
**Description**: 台灣格式電話、Email、地址必須在儲存或輸出前遮蔽。敏感關鍵字（密碼、銀行帳戶等）觸發轉接。

---

## Out of Scope (Phase 1)

| Item | Target Phase |
|------|-------------|
| RAG vector search (Layer 2) | Phase 2 |
| LLM generation (Layer 3) | Phase 2 |
| Messenger / WhatsApp platform adapters | Phase 2 |
| Prompt injection defense (L3) | Phase 2 |
| SLA tracking for escalation | Phase 2 |
| DST state machine | Phase 2 |
| Sentiment analysis | Phase 2 |
| RBAC / authentication | Phase 3 |
| Cost tracking (resolution_cost) | Phase 3 |
| pgvector index (ivfflat) | Phase 2 |

---

## Acceptance Criteria Summary

| FR | Key Metric | Threshold |
|----|-----------|-----------|
| FR-07 | Rule match confidence | > 0.7 |
| FR-06 | Default rate limit | 100 rps |
| FR-01 | Webhook response time | < 3.0s |
| NFR-01 | FCR (30-day rolling) | >= 50% |
| NFR-02 | p95 latency | < 3.0s |
| NFR-04 | Webhook verification rate | 100% |

---

*SRS.md v1.0 — generated from SPEC/omnibot-phase-1.md v7.0*
