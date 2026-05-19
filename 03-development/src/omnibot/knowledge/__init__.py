"""[FR-07] Knowledge Layer V1 — Rule Match + Escalate.

Implements SRS FR-07 acceptance criteria in-memory (Phase 1, no DB):
  - Keyword matching simulates SQL ILIKE + ANY(keywords)
  - Only active (is_active=True) rules
  - Exact match → confidence 0.95, partial → 0.7
  - Version ordering (highest wins)
  - No match → KnowledgeResult(id=-1, source="escalate")

Citations: SRS.md FR-07 section
"""

from typing import Any, Dict, List

from omnibot.knowledge.v2 import HybridKnowledgeV2, KnowledgeResult, _reciprocal_rank_fusion  # noqa: F401


class KnowledgeBase:
    """In-memory knowledge base matching SRS FR-07 semantics.

    Each rule has keywords, a canned response, is_active flag, version,
    and an optional question field for exact-match detection.
    """

    def __init__(self) -> None:
        self._rules: List[Dict[str, Any]] = []
        self._next_id = 1

    def add_rule(
        self,
        keywords: List[str],
        response: str,
        *,
        is_active: bool = True,
        version: int = 1,
        question: str = "",
    ) -> None:
        """Add a keyword-triggered response rule.

        Args:
            keywords: Trigger keywords (ANY match counts).
            response: Canned response text.
            is_active: If False the rule is skipped in queries.
            version: Higher version wins among equal-confidence rules.
            question: Full question text for exact-match (0.95) detection.
        """
        self._rules.append({
            "id": self._next_id,
            "keywords": keywords,
            "response": response,
            "is_active": is_active,
            "version": version,
            "question": question,
        })
        self._next_id += 1

    def query(self, text: str) -> KnowledgeResult:
        """Query the knowledge base and return the best matching result.

        Confidence scheme:
          - No active rule matches → 0.0, escalated
          - Partial keyword overlap → 0.7
          - All keywords matched or question substring found → 0.95
        """
        active_rules = [r for r in self._rules if r["is_active"]]

        best_confidence = 0.0
        best_result: Dict[str, Any] | None = None
        best_version = -1

        for rule in active_rules:
            matched = sum(1 for kw in rule["keywords"] if kw in text)
            question_match = rule["question"] and rule["question"] in text

            if matched == 0 and not question_match:
                continue

            if matched == len(rule["keywords"]) or question_match:
                confidence = 0.95
            else:
                confidence = 0.7

            if confidence > best_confidence or (confidence == best_confidence and rule["version"] > best_version):
                best_confidence = confidence
                best_result = rule
                best_version = rule["version"]

        if best_result is None:
            return KnowledgeResult(
                id=-1,
                query=text,
                response="無法回答您的問題，為您轉接專人。",
                confidence=0.0,
                source="escalate",
            )

        return KnowledgeResult(
            id=best_result["id"],
            query=text,
            response=best_result["response"],
            confidence=best_confidence,
            source="rule",
        )


# Default instance for convenience
_default_kb = KnowledgeBase()
_default_kb.add_rule(
    keywords=["退貨", "return"],
    response="退貨流程：請提供您的訂單編號，我們將盡快為您處理退貨事宜。",
    question="退貨",
)
_default_kb.add_rule(
    keywords=["訂單", "查詢", "order"],
    response="訂單查詢：請提供您的訂單編號或手機號碼，我們為您查詢最新狀態。",
    question="訂單查詢",
)
_default_kb.add_rule(
    keywords=["客服", "專人", "人工"],
    response="為您轉接專人，請稍候。",
)


def query_knowledge(text: str) -> KnowledgeResult:
    """Convenience function: query the default knowledge base."""
    return _default_kb.query(text)
