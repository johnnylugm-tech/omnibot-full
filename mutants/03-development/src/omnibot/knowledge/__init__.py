"""[FR-07] Knowledge Layer V1 — Rule Match + Escalate.

Exact/fuzzy keyword matching with confidence scoring.
Confidence > 0.7 → direct reply; otherwise escalate.

Citations: SRS.md FR-07 section
"""

from dataclasses import dataclass
from typing import List
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


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

    def xǁKnowledgeBaseǁ__init____mutmut_orig(self):
        self._rules: List[dict] = []

    def xǁKnowledgeBaseǁ__init____mutmut_1(self):
        self._rules: List[dict] = None
    
    xǁKnowledgeBaseǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁKnowledgeBaseǁ__init____mutmut_1': xǁKnowledgeBaseǁ__init____mutmut_1
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁKnowledgeBaseǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁKnowledgeBaseǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁKnowledgeBaseǁ__init____mutmut_orig)
    xǁKnowledgeBaseǁ__init____mutmut_orig.__name__ = 'xǁKnowledgeBaseǁ__init__'

    def xǁKnowledgeBaseǁadd_rule__mutmut_orig(self, keywords: List[str], response: str) -> None:
        """Add a keyword-triggered response rule."""
        self._rules.append({"keywords": keywords, "response": response})

    def xǁKnowledgeBaseǁadd_rule__mutmut_1(self, keywords: List[str], response: str) -> None:
        """Add a keyword-triggered response rule."""
        self._rules.append(None)

    def xǁKnowledgeBaseǁadd_rule__mutmut_2(self, keywords: List[str], response: str) -> None:
        """Add a keyword-triggered response rule."""
        self._rules.append({"XXkeywordsXX": keywords, "response": response})

    def xǁKnowledgeBaseǁadd_rule__mutmut_3(self, keywords: List[str], response: str) -> None:
        """Add a keyword-triggered response rule."""
        self._rules.append({"KEYWORDS": keywords, "response": response})

    def xǁKnowledgeBaseǁadd_rule__mutmut_4(self, keywords: List[str], response: str) -> None:
        """Add a keyword-triggered response rule."""
        self._rules.append({"keywords": keywords, "XXresponseXX": response})

    def xǁKnowledgeBaseǁadd_rule__mutmut_5(self, keywords: List[str], response: str) -> None:
        """Add a keyword-triggered response rule."""
        self._rules.append({"keywords": keywords, "RESPONSE": response})
    
    xǁKnowledgeBaseǁadd_rule__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁKnowledgeBaseǁadd_rule__mutmut_1': xǁKnowledgeBaseǁadd_rule__mutmut_1, 
        'xǁKnowledgeBaseǁadd_rule__mutmut_2': xǁKnowledgeBaseǁadd_rule__mutmut_2, 
        'xǁKnowledgeBaseǁadd_rule__mutmut_3': xǁKnowledgeBaseǁadd_rule__mutmut_3, 
        'xǁKnowledgeBaseǁadd_rule__mutmut_4': xǁKnowledgeBaseǁadd_rule__mutmut_4, 
        'xǁKnowledgeBaseǁadd_rule__mutmut_5': xǁKnowledgeBaseǁadd_rule__mutmut_5
    }
    
    def add_rule(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁKnowledgeBaseǁadd_rule__mutmut_orig"), object.__getattribute__(self, "xǁKnowledgeBaseǁadd_rule__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_rule.__signature__ = _mutmut_signature(xǁKnowledgeBaseǁadd_rule__mutmut_orig)
    xǁKnowledgeBaseǁadd_rule__mutmut_orig.__name__ = 'xǁKnowledgeBaseǁadd_rule'

    def xǁKnowledgeBaseǁquery__mutmut_orig(self, text: str) -> QueryResult:
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

    def xǁKnowledgeBaseǁquery__mutmut_1(self, text: str) -> QueryResult:
        """Query the knowledge base and return the best matching result."""
        best_confidence = None
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

    def xǁKnowledgeBaseǁquery__mutmut_2(self, text: str) -> QueryResult:
        """Query the knowledge base and return the best matching result."""
        best_confidence = 1.0
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

    def xǁKnowledgeBaseǁquery__mutmut_3(self, text: str) -> QueryResult:
        """Query the knowledge base and return the best matching result."""
        best_confidence = 0.0
        best_response = None

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

    def xǁKnowledgeBaseǁquery__mutmut_4(self, text: str) -> QueryResult:
        """Query the knowledge base and return the best matching result."""
        best_confidence = 0.0
        best_response = "XXXX"

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

    def xǁKnowledgeBaseǁquery__mutmut_5(self, text: str) -> QueryResult:
        """Query the knowledge base and return the best matching result."""
        best_confidence = 0.0
        best_response = ""

        for rule in self._rules:
            matched = None
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

    def xǁKnowledgeBaseǁquery__mutmut_6(self, text: str) -> QueryResult:
        """Query the knowledge base and return the best matching result."""
        best_confidence = 0.0
        best_response = ""

        for rule in self._rules:
            matched = sum(None)
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

    def xǁKnowledgeBaseǁquery__mutmut_7(self, text: str) -> QueryResult:
        """Query the knowledge base and return the best matching result."""
        best_confidence = 0.0
        best_response = ""

        for rule in self._rules:
            matched = sum(2 for kw in rule["keywords"] if kw in text)
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

    def xǁKnowledgeBaseǁquery__mutmut_8(self, text: str) -> QueryResult:
        """Query the knowledge base and return the best matching result."""
        best_confidence = 0.0
        best_response = ""

        for rule in self._rules:
            matched = sum(1 for kw in rule["XXkeywordsXX"] if kw in text)
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

    def xǁKnowledgeBaseǁquery__mutmut_9(self, text: str) -> QueryResult:
        """Query the knowledge base and return the best matching result."""
        best_confidence = 0.0
        best_response = ""

        for rule in self._rules:
            matched = sum(1 for kw in rule["KEYWORDS"] if kw in text)
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

    def xǁKnowledgeBaseǁquery__mutmut_10(self, text: str) -> QueryResult:
        """Query the knowledge base and return the best matching result."""
        best_confidence = 0.0
        best_response = ""

        for rule in self._rules:
            matched = sum(1 for kw in rule["keywords"] if kw not in text)
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

    def xǁKnowledgeBaseǁquery__mutmut_11(self, text: str) -> QueryResult:
        """Query the knowledge base and return the best matching result."""
        best_confidence = 0.0
        best_response = ""

        for rule in self._rules:
            matched = sum(1 for kw in rule["keywords"] if kw in text)
            if matched >= 0:
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

    def xǁKnowledgeBaseǁquery__mutmut_12(self, text: str) -> QueryResult:
        """Query the knowledge base and return the best matching result."""
        best_confidence = 0.0
        best_response = ""

        for rule in self._rules:
            matched = sum(1 for kw in rule["keywords"] if kw in text)
            if matched > 1:
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

    def xǁKnowledgeBaseǁquery__mutmut_13(self, text: str) -> QueryResult:
        """Query the knowledge base and return the best matching result."""
        best_confidence = 0.0
        best_response = ""

        for rule in self._rules:
            matched = sum(1 for kw in rule["keywords"] if kw in text)
            if matched > 0:
                confidence = None
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

    def xǁKnowledgeBaseǁquery__mutmut_14(self, text: str) -> QueryResult:
        """Query the knowledge base and return the best matching result."""
        best_confidence = 0.0
        best_response = ""

        for rule in self._rules:
            matched = sum(1 for kw in rule["keywords"] if kw in text)
            if matched > 0:
                confidence = matched * len(rule["keywords"])
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

    def xǁKnowledgeBaseǁquery__mutmut_15(self, text: str) -> QueryResult:
        """Query the knowledge base and return the best matching result."""
        best_confidence = 0.0
        best_response = ""

        for rule in self._rules:
            matched = sum(1 for kw in rule["keywords"] if kw in text)
            if matched > 0:
                confidence = matched / len(rule["keywords"])
                if confidence >= best_confidence:
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

    def xǁKnowledgeBaseǁquery__mutmut_16(self, text: str) -> QueryResult:
        """Query the knowledge base and return the best matching result."""
        best_confidence = 0.0
        best_response = ""

        for rule in self._rules:
            matched = sum(1 for kw in rule["keywords"] if kw in text)
            if matched > 0:
                confidence = matched / len(rule["keywords"])
                if confidence > best_confidence:
                    best_confidence = None
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

    def xǁKnowledgeBaseǁquery__mutmut_17(self, text: str) -> QueryResult:
        """Query the knowledge base and return the best matching result."""
        best_confidence = 0.0
        best_response = ""

        for rule in self._rules:
            matched = sum(1 for kw in rule["keywords"] if kw in text)
            if matched > 0:
                confidence = matched / len(rule["keywords"])
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_response = None

        escalate = best_confidence <= 0.7
        if not best_response:
            best_response = "無法回答您的問題，為您轉接專人。"

        return QueryResult(
            response=best_response,
            confidence=best_confidence,
            source="rule_match" if best_confidence > 0.7 else "escalate",
            escalate=escalate,
        )

    def xǁKnowledgeBaseǁquery__mutmut_18(self, text: str) -> QueryResult:
        """Query the knowledge base and return the best matching result."""
        best_confidence = 0.0
        best_response = ""

        for rule in self._rules:
            matched = sum(1 for kw in rule["keywords"] if kw in text)
            if matched > 0:
                confidence = matched / len(rule["keywords"])
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_response = rule["XXresponseXX"]

        escalate = best_confidence <= 0.7
        if not best_response:
            best_response = "無法回答您的問題，為您轉接專人。"

        return QueryResult(
            response=best_response,
            confidence=best_confidence,
            source="rule_match" if best_confidence > 0.7 else "escalate",
            escalate=escalate,
        )

    def xǁKnowledgeBaseǁquery__mutmut_19(self, text: str) -> QueryResult:
        """Query the knowledge base and return the best matching result."""
        best_confidence = 0.0
        best_response = ""

        for rule in self._rules:
            matched = sum(1 for kw in rule["keywords"] if kw in text)
            if matched > 0:
                confidence = matched / len(rule["keywords"])
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_response = rule["RESPONSE"]

        escalate = best_confidence <= 0.7
        if not best_response:
            best_response = "無法回答您的問題，為您轉接專人。"

        return QueryResult(
            response=best_response,
            confidence=best_confidence,
            source="rule_match" if best_confidence > 0.7 else "escalate",
            escalate=escalate,
        )

    def xǁKnowledgeBaseǁquery__mutmut_20(self, text: str) -> QueryResult:
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

        escalate = None
        if not best_response:
            best_response = "無法回答您的問題，為您轉接專人。"

        return QueryResult(
            response=best_response,
            confidence=best_confidence,
            source="rule_match" if best_confidence > 0.7 else "escalate",
            escalate=escalate,
        )

    def xǁKnowledgeBaseǁquery__mutmut_21(self, text: str) -> QueryResult:
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

        escalate = best_confidence < 0.7
        if not best_response:
            best_response = "無法回答您的問題，為您轉接專人。"

        return QueryResult(
            response=best_response,
            confidence=best_confidence,
            source="rule_match" if best_confidence > 0.7 else "escalate",
            escalate=escalate,
        )

    def xǁKnowledgeBaseǁquery__mutmut_22(self, text: str) -> QueryResult:
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

        escalate = best_confidence <= 1.7
        if not best_response:
            best_response = "無法回答您的問題，為您轉接專人。"

        return QueryResult(
            response=best_response,
            confidence=best_confidence,
            source="rule_match" if best_confidence > 0.7 else "escalate",
            escalate=escalate,
        )

    def xǁKnowledgeBaseǁquery__mutmut_23(self, text: str) -> QueryResult:
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
        if best_response:
            best_response = "無法回答您的問題，為您轉接專人。"

        return QueryResult(
            response=best_response,
            confidence=best_confidence,
            source="rule_match" if best_confidence > 0.7 else "escalate",
            escalate=escalate,
        )

    def xǁKnowledgeBaseǁquery__mutmut_24(self, text: str) -> QueryResult:
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
            best_response = None

        return QueryResult(
            response=best_response,
            confidence=best_confidence,
            source="rule_match" if best_confidence > 0.7 else "escalate",
            escalate=escalate,
        )

    def xǁKnowledgeBaseǁquery__mutmut_25(self, text: str) -> QueryResult:
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
            best_response = "XX無法回答您的問題，為您轉接專人。XX"

        return QueryResult(
            response=best_response,
            confidence=best_confidence,
            source="rule_match" if best_confidence > 0.7 else "escalate",
            escalate=escalate,
        )

    def xǁKnowledgeBaseǁquery__mutmut_26(self, text: str) -> QueryResult:
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
            response=None,
            confidence=best_confidence,
            source="rule_match" if best_confidence > 0.7 else "escalate",
            escalate=escalate,
        )

    def xǁKnowledgeBaseǁquery__mutmut_27(self, text: str) -> QueryResult:
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
            confidence=None,
            source="rule_match" if best_confidence > 0.7 else "escalate",
            escalate=escalate,
        )

    def xǁKnowledgeBaseǁquery__mutmut_28(self, text: str) -> QueryResult:
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
            source=None,
            escalate=escalate,
        )

    def xǁKnowledgeBaseǁquery__mutmut_29(self, text: str) -> QueryResult:
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
            escalate=None,
        )

    def xǁKnowledgeBaseǁquery__mutmut_30(self, text: str) -> QueryResult:
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
            confidence=best_confidence,
            source="rule_match" if best_confidence > 0.7 else "escalate",
            escalate=escalate,
        )

    def xǁKnowledgeBaseǁquery__mutmut_31(self, text: str) -> QueryResult:
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
            source="rule_match" if best_confidence > 0.7 else "escalate",
            escalate=escalate,
        )

    def xǁKnowledgeBaseǁquery__mutmut_32(self, text: str) -> QueryResult:
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
            escalate=escalate,
        )

    def xǁKnowledgeBaseǁquery__mutmut_33(self, text: str) -> QueryResult:
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
            )

    def xǁKnowledgeBaseǁquery__mutmut_34(self, text: str) -> QueryResult:
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
            source="XXrule_matchXX" if best_confidence > 0.7 else "escalate",
            escalate=escalate,
        )

    def xǁKnowledgeBaseǁquery__mutmut_35(self, text: str) -> QueryResult:
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
            source="RULE_MATCH" if best_confidence > 0.7 else "escalate",
            escalate=escalate,
        )

    def xǁKnowledgeBaseǁquery__mutmut_36(self, text: str) -> QueryResult:
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
            source="rule_match" if best_confidence >= 0.7 else "escalate",
            escalate=escalate,
        )

    def xǁKnowledgeBaseǁquery__mutmut_37(self, text: str) -> QueryResult:
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
            source="rule_match" if best_confidence > 1.7 else "escalate",
            escalate=escalate,
        )

    def xǁKnowledgeBaseǁquery__mutmut_38(self, text: str) -> QueryResult:
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
            source="rule_match" if best_confidence > 0.7 else "XXescalateXX",
            escalate=escalate,
        )

    def xǁKnowledgeBaseǁquery__mutmut_39(self, text: str) -> QueryResult:
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
            source="rule_match" if best_confidence > 0.7 else "ESCALATE",
            escalate=escalate,
        )
    
    xǁKnowledgeBaseǁquery__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁKnowledgeBaseǁquery__mutmut_1': xǁKnowledgeBaseǁquery__mutmut_1, 
        'xǁKnowledgeBaseǁquery__mutmut_2': xǁKnowledgeBaseǁquery__mutmut_2, 
        'xǁKnowledgeBaseǁquery__mutmut_3': xǁKnowledgeBaseǁquery__mutmut_3, 
        'xǁKnowledgeBaseǁquery__mutmut_4': xǁKnowledgeBaseǁquery__mutmut_4, 
        'xǁKnowledgeBaseǁquery__mutmut_5': xǁKnowledgeBaseǁquery__mutmut_5, 
        'xǁKnowledgeBaseǁquery__mutmut_6': xǁKnowledgeBaseǁquery__mutmut_6, 
        'xǁKnowledgeBaseǁquery__mutmut_7': xǁKnowledgeBaseǁquery__mutmut_7, 
        'xǁKnowledgeBaseǁquery__mutmut_8': xǁKnowledgeBaseǁquery__mutmut_8, 
        'xǁKnowledgeBaseǁquery__mutmut_9': xǁKnowledgeBaseǁquery__mutmut_9, 
        'xǁKnowledgeBaseǁquery__mutmut_10': xǁKnowledgeBaseǁquery__mutmut_10, 
        'xǁKnowledgeBaseǁquery__mutmut_11': xǁKnowledgeBaseǁquery__mutmut_11, 
        'xǁKnowledgeBaseǁquery__mutmut_12': xǁKnowledgeBaseǁquery__mutmut_12, 
        'xǁKnowledgeBaseǁquery__mutmut_13': xǁKnowledgeBaseǁquery__mutmut_13, 
        'xǁKnowledgeBaseǁquery__mutmut_14': xǁKnowledgeBaseǁquery__mutmut_14, 
        'xǁKnowledgeBaseǁquery__mutmut_15': xǁKnowledgeBaseǁquery__mutmut_15, 
        'xǁKnowledgeBaseǁquery__mutmut_16': xǁKnowledgeBaseǁquery__mutmut_16, 
        'xǁKnowledgeBaseǁquery__mutmut_17': xǁKnowledgeBaseǁquery__mutmut_17, 
        'xǁKnowledgeBaseǁquery__mutmut_18': xǁKnowledgeBaseǁquery__mutmut_18, 
        'xǁKnowledgeBaseǁquery__mutmut_19': xǁKnowledgeBaseǁquery__mutmut_19, 
        'xǁKnowledgeBaseǁquery__mutmut_20': xǁKnowledgeBaseǁquery__mutmut_20, 
        'xǁKnowledgeBaseǁquery__mutmut_21': xǁKnowledgeBaseǁquery__mutmut_21, 
        'xǁKnowledgeBaseǁquery__mutmut_22': xǁKnowledgeBaseǁquery__mutmut_22, 
        'xǁKnowledgeBaseǁquery__mutmut_23': xǁKnowledgeBaseǁquery__mutmut_23, 
        'xǁKnowledgeBaseǁquery__mutmut_24': xǁKnowledgeBaseǁquery__mutmut_24, 
        'xǁKnowledgeBaseǁquery__mutmut_25': xǁKnowledgeBaseǁquery__mutmut_25, 
        'xǁKnowledgeBaseǁquery__mutmut_26': xǁKnowledgeBaseǁquery__mutmut_26, 
        'xǁKnowledgeBaseǁquery__mutmut_27': xǁKnowledgeBaseǁquery__mutmut_27, 
        'xǁKnowledgeBaseǁquery__mutmut_28': xǁKnowledgeBaseǁquery__mutmut_28, 
        'xǁKnowledgeBaseǁquery__mutmut_29': xǁKnowledgeBaseǁquery__mutmut_29, 
        'xǁKnowledgeBaseǁquery__mutmut_30': xǁKnowledgeBaseǁquery__mutmut_30, 
        'xǁKnowledgeBaseǁquery__mutmut_31': xǁKnowledgeBaseǁquery__mutmut_31, 
        'xǁKnowledgeBaseǁquery__mutmut_32': xǁKnowledgeBaseǁquery__mutmut_32, 
        'xǁKnowledgeBaseǁquery__mutmut_33': xǁKnowledgeBaseǁquery__mutmut_33, 
        'xǁKnowledgeBaseǁquery__mutmut_34': xǁKnowledgeBaseǁquery__mutmut_34, 
        'xǁKnowledgeBaseǁquery__mutmut_35': xǁKnowledgeBaseǁquery__mutmut_35, 
        'xǁKnowledgeBaseǁquery__mutmut_36': xǁKnowledgeBaseǁquery__mutmut_36, 
        'xǁKnowledgeBaseǁquery__mutmut_37': xǁKnowledgeBaseǁquery__mutmut_37, 
        'xǁKnowledgeBaseǁquery__mutmut_38': xǁKnowledgeBaseǁquery__mutmut_38, 
        'xǁKnowledgeBaseǁquery__mutmut_39': xǁKnowledgeBaseǁquery__mutmut_39
    }
    
    def query(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁKnowledgeBaseǁquery__mutmut_orig"), object.__getattribute__(self, "xǁKnowledgeBaseǁquery__mutmut_mutants"), args, kwargs, self)
        return result 
    
    query.__signature__ = _mutmut_signature(xǁKnowledgeBaseǁquery__mutmut_orig)
    xǁKnowledgeBaseǁquery__mutmut_orig.__name__ = 'xǁKnowledgeBaseǁquery'


# Default instance for convenience
_default_kb = KnowledgeBase()
_default_kb.add_rule(keywords=["退貨", "return"], response="退貨流程：請提供您的訂單編號，我們將盡快為您處理退貨事宜。")
_default_kb.add_rule(keywords=["訂單", "查詢", "order"], response="訂單查詢：請提供您的訂單編號或手機號碼，我們為您查詢最新狀態。")
_default_kb.add_rule(keywords=["客服", "專人", "人工"], response="為您轉接專人，請稍候。")


def x_query_knowledge__mutmut_orig(text: str) -> QueryResult:
    """Convenience function: query the default knowledge base."""
    return _default_kb.query(text)


def x_query_knowledge__mutmut_1(text: str) -> QueryResult:
    """Convenience function: query the default knowledge base."""
    return _default_kb.query(None)

x_query_knowledge__mutmut_mutants : ClassVar[MutantDict] = {
'x_query_knowledge__mutmut_1': x_query_knowledge__mutmut_1
}

def query_knowledge(*args, **kwargs):
    result = _mutmut_trampoline(x_query_knowledge__mutmut_orig, x_query_knowledge__mutmut_mutants, args, kwargs)
    return result 

query_knowledge.__signature__ = _mutmut_signature(x_query_knowledge__mutmut_orig)
x_query_knowledge__mutmut_orig.__name__ = 'x_query_knowledge'
