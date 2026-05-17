"""[FR-07] Knowledge Layer V1 — Rule Match + Escalate.

Exact/fuzzy keyword matching with confidence scoring.
Confidence > 0.7 → direct reply; otherwise escalate.

Citations: SRS.md FR-07 section
"""

from dataclasses import dataclass
from typing import List

from omnibot.knowledge.v2 import HybridKnowledgeV2, KnowledgeResult, _reciprocal_rank_fusion  # noqa: F401


@dataclass
class QueryResult:
    """Result of a knowledge base query.

    Citations: SRS.md FR-07, SAD.md UnifiedResponse
    """
    response: str
    confidence: float
    source: str = "rule_match"
    escalate: bool = False


class KnowledgeBase:
    """In-memory knowledge base with keyword-based rule matching.

    Each rule has a list of keywords and a canned response.
    Confidence = number of matched keywords / total keywords in the best rule.
    """

    def __init__(self):
        self._rules: List[dict] = []

    def add_rule(self, keywords: List[str], response: str) -> None:
        """Add a keyword-triggered response rule."""
        self._rules.append({"keywords": keywords, "response": response})

    def query(self, text: str) -> QueryResult:
        """Query the knowledge base and return the best matching result."""
        best_confidence = 0.0
        best_response = ""

        for rule in self._rules:
            matched = sum(1 for kw in rule["keywords"] if kw in text)
            if matched > 0:
                confidence = matched / len(rule["keywords"])
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_response = rule["response"]

        escalate = best_confidence <= 0.7
        if not best_response:
            best_response = "無法回答您的問題，為您轉接專人。"

        return QueryResult(
            response=best_response,
            confidence=best_confidence,
            source="rule_match" if best_confidence > 0.7 else "escalate",
            escalate=escalate,
        )


# Default instance for convenience
_default_kb = KnowledgeBase()
_default_kb.add_rule(keywords=["退貨", "return"], response="退貨流程：請提供您的訂單編號，我們將盡快為您處理退貨事宜。")
_default_kb.add_rule(keywords=["訂單", "查詢", "order"], response="訂單查詢：請提供您的訂單編號或手機號碼，我們為您查詢最新狀態。")
_default_kb.add_rule(keywords=["客服", "專人", "人工"], response="為您轉接專人，請稍候。")


def query_knowledge(text: str) -> QueryResult:
    """Convenience function: query the default knowledge base."""
    return _default_kb.query(text)
