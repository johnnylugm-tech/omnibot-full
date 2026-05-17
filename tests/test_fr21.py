"""[FR-21] GroundingChecker L5 -- Semantic Alignment Verification.

Acceptance criteria:
  - GroundingResult(grounded, score, reason, best_match_index) frozen dataclass
  - GroundingChecker uses injectable embedding_fn, default threshold=0.75
  - check(llm_output, source_texts) -> GroundingResult
  - Empty source_texts -> grounded=False, reason="no_source"
  - Cosine similarity: embed both, compute max, compare to threshold
  - Threshold configurable via constructor

Citations: SRS.md:191-209, SAD.md:311-332
"""

from __future__ import annotations

import math

import pytest

from omnibot.grounding import GroundingChecker, GroundingResult, _cosine_similarity


# -- mock embedding functions --

def _mock_embed_identity(text: str) -> list[float]:
    """Returns embeddings that produce predictable cosine similarities.

    output:  [1.0, 0.0]
    source0: [1.0, 0.0]  -> cos=1.0
    source1: [0.0, 1.0]  -> cos=0.0
    source2: [0.6, 0.8]  -> cos=0.6
    default:             -> cos≈0.5 (using hash)
    """
    mapping = {
        "output": [1.0, 0.0],
        "source0": [1.0, 0.0],
        "source1": [0.0, 1.0],
        "source2": [0.6, 0.8],
    }
    return mapping.get(text, [0.5, math.sqrt(1 - 0.25)])


def _mock_embed_tracking() -> tuple[list, callable]:
    """Returns (calls_list, embedding_fn) where calls_list records every call."""
    calls: list = []

    def embed(text: str) -> list[float]:
        calls.append(text)
        return [1.0, 0.0]

    return calls, embed


# -- pure function tests --

def test_cosine_similarity_identical():
    a = [1.0, 2.0, 3.0]
    assert math.isclose(_cosine_similarity(a, a), 1.0)


def test_cosine_similarity_orthogonal():
    assert math.isclose(_cosine_similarity([1.0, 0.0], [0.0, 1.0]), 0.0)


def test_cosine_similarity_opposite():
    assert math.isclose(_cosine_similarity([1.0, 0.0], [-1.0, 0.0]), -1.0)


def test_cosine_similarity_zero_vector():
    assert _cosine_similarity([0.0, 0.0], [1.0, 2.0]) == 0.0
    assert _cosine_similarity([1.0, 2.0], [0.0, 0.0]) == 0.0


# -- GroundingResult dataclass --

def test_grounding_result_fields():
    r = GroundingResult(grounded=True, score=0.85, reason="grounded", best_match_index=2)
    assert r.grounded is True
    assert r.score == 0.85
    assert r.reason == "grounded"
    assert r.best_match_index == 2


def test_grounding_result_is_frozen():
    r = GroundingResult(grounded=False, score=0.0, reason="no_source", best_match_index=-1)
    with pytest.raises(Exception):
        r.grounded = True  # type: ignore[misc]


def test_grounding_result_not_grounded():
    r = GroundingResult(grounded=False, score=0.42, reason="below_threshold", best_match_index=0)
    assert r.grounded is False
    assert r.reason == "below_threshold"


# -- GroundingChecker --

def test_empty_source_texts():
    checker = GroundingChecker(embedding_fn=_mock_embed_identity)
    result = checker.check("output", [])
    assert result.grounded is False
    assert result.reason == "no_source"
    assert result.score == 0.0
    assert result.best_match_index == -1


def test_perfect_grounding():
    checker = GroundingChecker(embedding_fn=_mock_embed_identity)
    result = checker.check("output", ["source0"])
    assert result.grounded is True
    assert math.isclose(result.score, 1.0)
    assert result.reason == "grounded"
    assert result.best_match_index == 0


def test_no_match():
    checker = GroundingChecker(embedding_fn=_mock_embed_identity)
    result = checker.check("output", ["source1"])
    assert result.grounded is False
    assert math.isclose(result.score, 0.0)
    assert result.reason == "below_threshold"
    assert result.best_match_index == 0


def test_below_threshold():
    checker = GroundingChecker(embedding_fn=_mock_embed_identity)
    result = checker.check("output", ["source2"])
    assert result.grounded is False
    assert math.isclose(result.score, 0.6)
    assert result.reason == "below_threshold"
    assert result.best_match_index == 0


def test_multiple_sources_selects_best():
    checker = GroundingChecker(embedding_fn=_mock_embed_identity)
    result = checker.check("output", ["source1", "source0", "source2"])
    assert result.grounded is True
    assert math.isclose(result.score, 1.0)
    assert result.best_match_index == 1  # source0 is at index 1


def test_custom_threshold():
    checker = GroundingChecker(threshold=0.5, embedding_fn=_mock_embed_identity)
    result = checker.check("output", ["source2"])  # cos=0.6
    assert result.grounded is True
    assert result.reason == "grounded"


def test_custom_threshold_strict():
    checker = GroundingChecker(threshold=0.9, embedding_fn=_mock_embed_identity)
    result = checker.check("output", ["source2"])
    assert result.grounded is False


def test_threshold_exact_boundary():
    checker = GroundingChecker(threshold=0.6, embedding_fn=_mock_embed_identity)
    result = checker.check("output", ["source2"])  # cos=0.6
    assert result.grounded is True


def test_embedding_fn_called_for_output_and_sources():
    calls, embed_fn = _mock_embed_tracking()
    checker = GroundingChecker(embedding_fn=embed_fn)
    checker.check("hello", ["src_a", "src_b"])
    assert calls == ["hello", "src_a", "src_b"]


def test_default_threshold():
    checker = GroundingChecker(embedding_fn=_mock_embed_identity)
    assert checker._threshold == 0.75
