"""[FR-17] EmotionAnalyzer with exponential decay and escalation trigger.

Acceptance criteria:
  - EmotionCategory enum: POSITIVE, NEUTRAL, NEGATIVE
  - EmotionScore(category, intensity, timestamp) frozen dataclass, intensity 0.0-1.0
  - EmotionTracker.add(score) appends to history
  - EmotionTracker.current_weighted_score(): exponential decay formula
    decay = e^(-0.693 * hours_ago / half_life_hours)
    POSITIVE +intensity*decay, NEGATIVE -intensity*decay; weighted average; 0.0 if no history
  - EmotionTracker.consecutive_negative_count(): count from tail, stop at non-NEGATIVE
  - EmotionTracker.should_escalate(): consecutive_negative_count() >= 3 → True
  - half_life_hours default 24.0, configurable

Citations: SRS.md:87-106, SAD.md:336-359
"""

from datetime import datetime, timedelta, timezone

import pytest

from omnibot.emotion import EmotionCategory, EmotionScore, EmotionTracker


# ── EmotionCategory enum ────────────────────────────────────────────────────────

def test_emotion_category_values():
    """EmotionCategory has POSITIVE, NEUTRAL, NEGATIVE."""
    assert EmotionCategory.POSITIVE.value == "POSITIVE"
    assert EmotionCategory.NEUTRAL.value == "NEUTRAL"
    assert EmotionCategory.NEGATIVE.value == "NEGATIVE"


# ── EmotionScore frozen dataclass ────────────────────────────────────────────────

def test_emotion_score_construction():
    """EmotionScore can be constructed with category, intensity, timestamp."""
    ts = datetime.now(timezone.utc)
    score = EmotionScore(category=EmotionCategory.POSITIVE, intensity=0.8, timestamp=ts)
    assert score.category == EmotionCategory.POSITIVE
    assert score.intensity == 0.8
    assert score.timestamp == ts


def test_emotion_score_is_frozen():
    """EmotionScore is frozen — mutation raises FrozenInstanceError."""
    from dataclasses import FrozenInstanceError
    ts = datetime.now(timezone.utc)
    score = EmotionScore(category=EmotionCategory.NEUTRAL, intensity=0.5, timestamp=ts)
    try:
        score.intensity = 1.0
        assert False, "Expected FrozenInstanceError"
    except FrozenInstanceError:
        pass


# ── EmotionTracker.add() ────────────────────────────────────────────────────────

def test_add_appends_to_history():
    """add() appends EmotionScore to the tracker's history."""
    tracker = EmotionTracker()
    ts = datetime.now(timezone.utc)
    score = EmotionScore(category=EmotionCategory.POSITIVE, intensity=0.9, timestamp=ts)
    tracker.add(score)
    assert len(tracker.history) == 1
    assert tracker.history[0] is score


def test_add_multiple_scores():
    """Multiple add() calls accumulate scores in order."""
    tracker = EmotionTracker()
    ts1 = datetime.now(timezone.utc)
    ts2 = ts1 + timedelta(hours=1)
    tracker.add(EmotionScore(category=EmotionCategory.POSITIVE, intensity=0.5, timestamp=ts1))
    tracker.add(EmotionScore(category=EmotionCategory.NEGATIVE, intensity=0.3, timestamp=ts2))
    assert len(tracker.history) == 2
    assert tracker.history[0].category == EmotionCategory.POSITIVE
    assert tracker.history[1].category == EmotionCategory.NEGATIVE


# ── current_weighted_score() ────────────────────────────────────────────────────

def test_weighted_score_empty_history():
    """Weighted score is 0.0 when there is no history."""
    tracker = EmotionTracker()
    assert tracker.current_weighted_score() == 0.0


def test_weighted_score_single_positive_now():
    """A single recent positive contributes its full intensity."""
    tracker = EmotionTracker()
    tracker.add(EmotionScore(
        category=EmotionCategory.POSITIVE, intensity=0.8,
        timestamp=datetime.now(timezone.utc)
    ))
    assert tracker.current_weighted_score() == pytest.approx(0.8, abs=0.01)


def test_weighted_score_single_negative_now():
    """A single recent negative contributes negative intensity."""
    tracker = EmotionTracker()
    tracker.add(EmotionScore(
        category=EmotionCategory.NEGATIVE, intensity=0.6,
        timestamp=datetime.now(timezone.utc)
    ))
    assert tracker.current_weighted_score() == pytest.approx(-0.6, abs=0.01)


def test_weighted_score_neutral_is_zero_weight():
    """NEUTRAL scores contribute 0 regardless of intensity."""
    tracker = EmotionTracker()
    tracker.add(EmotionScore(
        category=EmotionCategory.NEUTRAL, intensity=0.9,
        timestamp=datetime.now(timezone.utc)
    ))
    assert tracker.current_weighted_score() == 0.0


def test_weighted_score_mixed_now():
    """Mixed positive and negative at the same time are averaged."""
    tracker = EmotionTracker()
    now = datetime.now(timezone.utc)
    tracker.add(EmotionScore(category=EmotionCategory.POSITIVE, intensity=0.8, timestamp=now))
    tracker.add(EmotionScore(category=EmotionCategory.NEGATIVE, intensity=0.4, timestamp=now))
    # (0.8 + (-0.4)) / 2 = 0.2
    assert tracker.current_weighted_score() == pytest.approx(0.2, abs=0.01)


def test_weighted_score_decay_at_half_life():
    """At exactly half_life hours, intensity contribution is halved (weighted avg)."""
    import math
    anchor = datetime.now(timezone.utc)
    half_life_ago = anchor - timedelta(hours=24.0)
    tracker = EmotionTracker(half_life_hours=24.0)
    tracker.add(EmotionScore(
        category=EmotionCategory.POSITIVE, intensity=1.0,
        timestamp=half_life_ago
    ))
    tracker.add(EmotionScore(
        category=EmotionCategory.NEUTRAL, intensity=0.0,
        timestamp=anchor
    ))
    # weighted_sum = 1.0 * e^(-0.693) ≈ 0.500
    # total_weight = e^(-0.693) + 1.0 ≈ 1.500
    # result = 0.500 / 1.500 ≈ 0.333
    expected_decay = math.exp(-0.693)
    expected = expected_decay / (1.0 + expected_decay)
    assert tracker.current_weighted_score() == pytest.approx(expected, abs=0.01)


def test_weighted_score_respects_configurable_half_life():
    """A shorter half-life causes faster decay (weighted avg)."""
    import math
    anchor = datetime.now(timezone.utc)
    one_hour_ago = anchor - timedelta(hours=1.0)
    tracker = EmotionTracker(half_life_hours=1.0)
    tracker.add(EmotionScore(
        category=EmotionCategory.POSITIVE, intensity=1.0,
        timestamp=one_hour_ago
    ))
    tracker.add(EmotionScore(
        category=EmotionCategory.NEUTRAL, intensity=0.0,
        timestamp=anchor
    ))
    expected_decay = math.exp(-0.693)
    expected = expected_decay / (1.0 + expected_decay)
    assert tracker.current_weighted_score() == pytest.approx(expected, abs=0.01)
    assert tracker.current_weighted_score() < 1.0


def test_weighted_score_very_old_decays_to_near_zero():
    """A score from far in the past has negligible weight (weighted avg)."""
    tracker = EmotionTracker(half_life_hours=24.0)
    anchor = datetime.now(timezone.utc)
    old = anchor - timedelta(hours=240)  # 10 half-lives
    now_neg = anchor - timedelta(hours=0.1)  # recent negative
    tracker.add(EmotionScore(
        category=EmotionCategory.POSITIVE, intensity=1.0,
        timestamp=old
    ))
    tracker.add(EmotionScore(
        category=EmotionCategory.NEGATIVE, intensity=1.0,
        timestamp=now_neg
    ))
    result = tracker.current_weighted_score()
    # The negative at now dominates because the old positive has decayed to ~0.001
    # weighted_sum ≈ 0.001 + (-1.0) = -0.999, total_weight ≈ 0.001 + 1.0 = 1.001
    # result ≈ -0.999 / 1.001 ≈ -0.998 (< -0.9 means negative dominates)
    assert result < -0.9


# ── consecutive_negative_count() ────────────────────────────────────────────────

def test_consecutive_negative_empty():
    """Empty history returns 0."""
    tracker = EmotionTracker()
    assert tracker.consecutive_negative_count() == 0


def test_consecutive_negative_single():
    """Single negative returns 1."""
    tracker = EmotionTracker()
    tracker.add(EmotionScore(
        category=EmotionCategory.NEGATIVE, intensity=0.5,
        timestamp=datetime.now(timezone.utc)
    ))
    assert tracker.consecutive_negative_count() == 1


def test_consecutive_negative_stops_at_positive():
    """Counting stops at the first non-NEGATIVE from the tail."""
    tracker = EmotionTracker()
    now = datetime.now(timezone.utc)
    tracker.add(EmotionScore(category=EmotionCategory.POSITIVE, intensity=0.5, timestamp=now))
    tracker.add(EmotionScore(category=EmotionCategory.NEGATIVE, intensity=0.3, timestamp=now))
    tracker.add(EmotionScore(category=EmotionCategory.NEGATIVE, intensity=0.4, timestamp=now))
    # Tail: NEG, NEG — only 2 consecutives from the end
    assert tracker.consecutive_negative_count() == 2


def test_consecutive_negative_stops_at_neutral():
    """NEUTRAL also breaks the consecutive negative chain."""
    tracker = EmotionTracker()
    now = datetime.now(timezone.utc)
    tracker.add(EmotionScore(category=EmotionCategory.NEGATIVE, intensity=0.5, timestamp=now))
    tracker.add(EmotionScore(category=EmotionCategory.NEUTRAL, intensity=0.2, timestamp=now))
    tracker.add(EmotionScore(category=EmotionCategory.NEGATIVE, intensity=0.3, timestamp=now))
    assert tracker.consecutive_negative_count() == 1


def test_consecutive_negative_all_three():
    """3 consecutive negatives returns 3."""
    tracker = EmotionTracker()
    now = datetime.now(timezone.utc)
    for _ in range(3):
        tracker.add(EmotionScore(
            category=EmotionCategory.NEGATIVE, intensity=0.5,
            timestamp=now
        ))
    assert tracker.consecutive_negative_count() == 3


def test_consecutive_negative_four_followed_by_positive():
    """Only the suffix of negative scores after the last non-negative is counted."""
    tracker = EmotionTracker()
    now = datetime.now(timezone.utc)
    tracker.add(EmotionScore(category=EmotionCategory.NEGATIVE, intensity=0.5, timestamp=now))
    tracker.add(EmotionScore(category=EmotionCategory.NEGATIVE, intensity=0.5, timestamp=now))
    tracker.add(EmotionScore(category=EmotionCategory.POSITIVE, intensity=0.5, timestamp=now))
    tracker.add(EmotionScore(category=EmotionCategory.NEGATIVE, intensity=0.5, timestamp=now))
    # Tail: NEG only 1 consecutive from end
    assert tracker.consecutive_negative_count() == 1


# ── should_escalate() ───────────────────────────────────────────────────────────

def test_should_escalate_empty_history():
    """Empty history does not escalate."""
    tracker = EmotionTracker()
    assert tracker.should_escalate() is False


def test_should_escalate_one_negative():
    """Single negative does not escalate."""
    tracker = EmotionTracker()
    tracker.add(EmotionScore(
        category=EmotionCategory.NEGATIVE, intensity=0.5,
        timestamp=datetime.now(timezone.utc)
    ))
    assert tracker.should_escalate() is False


def test_should_escalate_two_negatives():
    """Two consecutive negatives do not escalate."""
    tracker = EmotionTracker()
    now = datetime.now(timezone.utc)
    tracker.add(EmotionScore(category=EmotionCategory.NEGATIVE, intensity=0.3, timestamp=now))
    tracker.add(EmotionScore(category=EmotionCategory.NEGATIVE, intensity=0.5, timestamp=now))
    assert tracker.should_escalate() is False


def test_should_escalate_three_negatives():
    """Three consecutive negatives trigger escalation."""
    tracker = EmotionTracker()
    now = datetime.now(timezone.utc)
    for _ in range(3):
        tracker.add(EmotionScore(
            category=EmotionCategory.NEGATIVE, intensity=0.5,
            timestamp=now
        ))
    assert tracker.should_escalate() is True


def test_should_escalate_four_negatives():
    """Four consecutive negatives also trigger escalation."""
    tracker = EmotionTracker()
    now = datetime.now(timezone.utc)
    for _ in range(4):
        tracker.add(EmotionScore(
            category=EmotionCategory.NEGATIVE, intensity=0.5,
            timestamp=now
        ))
    assert tracker.should_escalate() is True


def test_should_escalate_broken_chain():
    """A non-negative breaking the chain prevents escalation."""
    tracker = EmotionTracker()
    now = datetime.now(timezone.utc)
    tracker.add(EmotionScore(category=EmotionCategory.NEGATIVE, intensity=0.5, timestamp=now))
    tracker.add(EmotionScore(category=EmotionCategory.NEGATIVE, intensity=0.5, timestamp=now))
    tracker.add(EmotionScore(category=EmotionCategory.POSITIVE, intensity=0.5, timestamp=now))
    assert tracker.should_escalate() is False


def test_should_escalate_three_negatives_then_neutral():
    """Three negatives followed by neutral → no escalation (chain broken)."""
    tracker = EmotionTracker()
    now = datetime.now(timezone.utc)
    tracker.add(EmotionScore(category=EmotionCategory.NEGATIVE, intensity=0.5, timestamp=now))
    tracker.add(EmotionScore(category=EmotionCategory.NEGATIVE, intensity=0.5, timestamp=now))
    tracker.add(EmotionScore(category=EmotionCategory.NEGATIVE, intensity=0.5, timestamp=now))
    tracker.add(EmotionScore(category=EmotionCategory.NEUTRAL, intensity=0.2, timestamp=now))
    assert tracker.should_escalate() is False


# ── Default half_life_hours ─────────────────────────────────────────────────────

def test_default_half_life_hours():
    """Default half_life is 24.0 hours."""
    tracker = EmotionTracker()
    assert tracker.half_life_hours == 24.0


def test_custom_half_life_hours():
    """half_life_hours can be set via constructor."""
    tracker = EmotionTracker(half_life_hours=12.0)
    assert tracker.half_life_hours == 12.0


# ── Integrity ───────────────────────────────────────────────────────────────────

def test_history_is_list():
    """Tracker.history is a plain list."""
    tracker = EmotionTracker()
    assert isinstance(tracker.history, list)
    assert len(tracker.history) == 0


def test_tracker_independent_state():
    """Trackers have independent state."""
    t1 = EmotionTracker()
    t2 = EmotionTracker()
    now = datetime.now(timezone.utc)
    t1.add(EmotionScore(category=EmotionCategory.NEGATIVE, intensity=0.5, timestamp=now))
    assert len(t1.history) == 1
    assert len(t2.history) == 0
