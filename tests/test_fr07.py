"""FR-07: Knowledge Layer V1 — Rule Match + Escalate.

[FR-07] Acceptance criteria:
  - Query knowledge base with exact/fuzzy SQL-equivalent match
  - Exact match (all keywords / question match) → confidence 0.95
  - Partial match → confidence 0.7
  - Only is_active=True rules considered
  - Higher version wins among same-confidence rules
  - No match → KnowledgeResult(id=-1, source="escalate")

Citations: SRS.md FR-07 section
"""

from omnibot.knowledge import KnowledgeBase, query_knowledge
from omnibot.knowledge.v2 import KnowledgeResult


def test_exact_match_confidence_095():
    """All keywords matched → confidence 0.95."""
    kb = KnowledgeBase()
    kb.add_rule(keywords=["退貨"], response="退貨流程：請提供訂單編號...")
    result = kb.query("我要退貨")
    assert result.confidence == 0.95
    assert "退貨" in result.response


def test_no_match_confidence_000():
    """Unmatched query returns source='escalate', id=-1."""
    kb = KnowledgeBase()
    kb.add_rule(keywords=["退貨"], response="退貨流程")
    result = kb.query("今天天氣如何")
    assert result.confidence == 0.0
    assert result.source == "escalate"
    assert result.id == -1


def test_partial_match_confidence_07():
    """Partial keyword overlap gives confidence 0.7."""
    kb = KnowledgeBase()
    kb.add_rule(keywords=["訂單", "查詢"], response="請提供訂單編號")
    result = kb.query("訂單")  # only 1/2 keywords matched
    assert result.confidence == 0.7


def test_question_exact_match_095():
    """Matching question field gives confidence 0.95 even with partial keywords."""
    kb = KnowledgeBase()
    kb.add_rule(keywords=["returns", "refund"], response="退貨流程", question="退貨")
    result = kb.query("退貨")  # 0/2 keywords but question matches
    assert result.confidence == 0.95


def test_multiple_rules_best_confidence():
    """Highest-confidence rule is returned."""
    kb = KnowledgeBase()
    kb.add_rule(keywords=["低"], response="低優先規則")
    kb.add_rule(keywords=["高", "優先"], response="高優先規則")
    result = kb.query("高優先測試")
    assert result.confidence == 0.95
    assert "高優先" in result.response


def test_version_tiebreaking():
    """Same confidence — higher version wins."""
    kb = KnowledgeBase()
    kb.add_rule(keywords=["退貨"], response="舊版回應", version=1)
    kb.add_rule(keywords=["退貨"], response="新版回應", version=2)
    result = kb.query("我要退貨")
    assert result.response == "新版回應"


def test_inactive_rule_skipped():
    """is_active=False rules are excluded from queries."""
    kb = KnowledgeBase()
    kb.add_rule(keywords=["退貨"], response="退貨流程", is_active=False)
    result = kb.query("我要退貨")
    assert result.confidence == 0.0
    assert result.source == "escalate"


def test_active_rule_included():
    """is_active=True (default) rules are included."""
    kb = KnowledgeBase()
    kb.add_rule(keywords=["退貨"], response="退貨流程", is_active=True)
    result = kb.query("我要退貨")
    assert result.confidence == 0.95


def test_knowledge_result_dataclass():
    """query returns KnowledgeResult with correct fields."""
    kb = KnowledgeBase()
    kb.add_rule(keywords=["test"], response="test ok")
    result = kb.query("test")
    assert isinstance(result, KnowledgeResult)
    assert result.id >= 1
    assert result.query == "test"
    assert result.response == "test ok"
    assert result.confidence == 0.95
    assert result.source == "rule"


def test_escalate_result_dataclass():
    """No-match returns KnowledgeResult with id=-1, source='escalate'."""
    kb = KnowledgeBase()
    result = kb.query("no match")
    assert isinstance(result, KnowledgeResult)
    assert result.id == -1
    assert result.source == "escalate"
    assert result.confidence == 0.0


def test_convenience_function():
    """query_knowledge() convenience function returns KnowledgeResult."""
    result = query_knowledge("退貨查詢")
    assert isinstance(result, KnowledgeResult)
