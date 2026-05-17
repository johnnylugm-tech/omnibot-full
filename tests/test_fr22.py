"""[FR-22] Prometheus Metrics — Core Instrumentation tests.

Tests all 8 Prometheus metrics: registration, observe, inc, set, and labels.
No FastAPI app startup required — uses prometheus_client directly.

Citations: SRS.md:214-230, SAD.md:511-531
"""

from __future__ import annotations

import re
from typing import List

import pytest
from prometheus_client import CollectorRegistry, Histogram, REGISTRY, generate_latest

from omnibot.metrics import PrometheusMetrics


@pytest.fixture(autouse=True)
def _clear_registry() -> None:
    """Clear default registry before each test to avoid duplicate registration."""
    collectors = list(REGISTRY._collector_to_names.keys())
    for collector in collectors:
        REGISTRY.unregister(collector)


EXPECTED_METRIC_NAMES: List[str] = [
    "omnibot_response_duration_seconds",
    "omnibot_requests_total",
    "omnibot_fcr_total",
    "omnibot_knowledge_hit_total",
    "omnibot_pii_masked_total",
    "omnibot_escalation_queue_size",
    "omnibot_emotion_escalation_total",
    "omnibot_llm_tokens_total",
]


# -- registration --


def test_all_eight_metrics_registered():
    """All 8 metrics are registered in the default registry after init."""
    PrometheusMetrics()
    output = generate_latest(REGISTRY).decode()

    for name in EXPECTED_METRIC_NAMES:
        assert f"# TYPE {name}" in output, f"Metric {name} not found in registry"


def test_no_extra_metrics_registered():
    """Only the 8 expected metrics exist in the default registry (excluding auto _created)."""
    PrometheusMetrics()
    output = generate_latest(REGISTRY).decode()
    type_lines = re.findall(r"# TYPE (\S+) ", output)
    # Filter out auto-generated _created timestamp metrics
    type_lines = [n for n in type_lines if not n.endswith("_created")]
    assert sorted(type_lines) == sorted(EXPECTED_METRIC_NAMES)


def test_metrics_registry_contains_all_names():
    """REGISTRY._names_to_collectors has entries for all 8 metric names."""
    PrometheusMetrics()
    for name in EXPECTED_METRIC_NAMES:
        assert name in REGISTRY._names_to_collectors, f"{name} missing from _names_to_collectors"


# -- histogram --


def test_histogram_observe_and_buckets():
    """response_duration histogram: observe records and correct buckets are used."""
    m = PrometheusMetrics()
    m.response_duration.labels(platform="telegram", knowledge_source="rag").observe(0.4)
    m.response_duration.labels(platform="line", knowledge_source="rule").observe(2.0)

    output = generate_latest(REGISTRY).decode()

    # Check the +Inf bucket is present for each label combination
    # prometheus_client sorts labels alphabetically
    assert 'omnibot_response_duration_seconds_bucket{knowledge_source="rag",le="+Inf",platform="telegram"} 1.0' in output
    assert 'omnibot_response_duration_seconds_bucket{knowledge_source="rule",le="+Inf",platform="line"} 1.0' in output

    # Verify the sum is recorded
    assert 'omnibot_response_duration_seconds_sum{knowledge_source="rag",platform="telegram"} 0.4' in output
    assert 'omnibot_response_duration_seconds_sum{knowledge_source="rule",platform="line"} 2.0' in output


def test_histogram_bucket_boundaries():
    """Response duration histogram uses the specified bucket boundaries."""
    m = PrometheusMetrics()
    expected_buckets = [0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0]
    actual_buckets = list(m.response_duration._upper_bounds)
    # Exclude the auto-added +Inf sentinel
    assert actual_buckets[:-1] == expected_buckets


# -- counters --


def test_requests_total_counter():
    """requests_total counter increments with platform and status labels."""
    m = PrometheusMetrics()
    m.requests_total.labels(platform="whatsapp", status="success").inc()
    m.requests_total.labels(platform="whatsapp", status="success").inc()
    m.requests_total.labels(platform="messenger", status="error").inc()

    output = generate_latest(REGISTRY).decode()
    assert 'omnibot_requests_total{platform="whatsapp",status="success"} 2.0' in output
    assert 'omnibot_requests_total{platform="messenger",status="error"} 1.0' in output


def test_fcr_total_counter():
    """fcr_total counter with resolved label ("true"/"false")."""
    m = PrometheusMetrics()
    m.fcr_total.labels(resolved="true").inc()
    m.fcr_total.labels(resolved="true").inc()
    m.fcr_total.labels(resolved="false").inc()

    output = generate_latest(REGISTRY).decode()
    assert 'omnibot_fcr_total{resolved="true"} 2.0' in output
    assert 'omnibot_fcr_total{resolved="false"} 1.0' in output


def test_knowledge_hit_total_counter():
    """knowledge_hit_total counter with layer label."""
    m = PrometheusMetrics()
    m.knowledge_hit_total.labels(layer="rule").inc(3)
    m.knowledge_hit_total.labels(layer="rag").inc()
    m.knowledge_hit_total.labels(layer="llm").inc()

    output = generate_latest(REGISTRY).decode()
    assert 'omnibot_knowledge_hit_total{layer="rule"} 3.0' in output
    assert 'omnibot_knowledge_hit_total{layer="rag"} 1.0' in output
    assert 'omnibot_knowledge_hit_total{layer="llm"} 1.0' in output


def test_pii_masked_total_counter():
    """pii_masked_total counter with pii_type label."""
    m = PrometheusMetrics()
    m.pii_masked_total.labels(pii_type="email").inc()
    m.pii_masked_total.labels(pii_type="phone").inc(2)
    m.pii_masked_total.labels(pii_type="ssn").inc()

    output = generate_latest(REGISTRY).decode()
    assert 'omnibot_pii_masked_total{pii_type="email"} 1.0' in output
    assert 'omnibot_pii_masked_total{pii_type="phone"} 2.0' in output
    assert 'omnibot_pii_masked_total{pii_type="ssn"} 1.0' in output


def test_llm_tokens_total_counter():
    """llm_tokens_total counter with model and direction labels."""
    m = PrometheusMetrics()
    m.llm_tokens_total.labels(model="claude-opus-4", direction="input").inc(150)
    m.llm_tokens_total.labels(model="claude-opus-4", direction="output").inc(80)

    output = generate_latest(REGISTRY).decode()
    # prometheus_client sorts labels alphabetically
    assert 'omnibot_llm_tokens_total{direction="input",model="claude-opus-4"} 150.0' in output
    assert 'omnibot_llm_tokens_total{direction="output",model="claude-opus-4"} 80.0' in output


# -- gauge --


def test_escalation_queue_size_gauge():
    """escalation_queue_size gauge: set and read current queue length."""
    m = PrometheusMetrics()
    m.escalation_queue_size.set(5)
    output = generate_latest(REGISTRY).decode()
    assert "omnibot_escalation_queue_size 5.0" in output

    m.escalation_queue_size.set(0)
    output = generate_latest(REGISTRY).decode()
    assert "omnibot_escalation_queue_size 0.0" in output

    m.escalation_queue_size.inc(3)
    output = generate_latest(REGISTRY).decode()
    assert "omnibot_escalation_queue_size 3.0" in output

    m.escalation_queue_size.dec()
    output = generate_latest(REGISTRY).decode()
    assert "omnibot_escalation_queue_size 2.0" in output


def test_emotion_escalation_total_counter():
    """emotion_escalation_total counter (no labels)."""
    m = PrometheusMetrics()
    m.emotion_escalation_total.inc()
    m.emotion_escalation_total.inc()

    output = generate_latest(REGISTRY).decode()
    assert "omnibot_emotion_escalation_total 2.0" in output


# -- text format --


def test_get_metrics_returns_bytes():
    """get_metrics() returns bytes (Prometheus text format)."""
    m = PrometheusMetrics()
    result = m.get_metrics()
    assert isinstance(result, bytes)
    text = result.decode()
    assert text.startswith("# HELP")


def test_get_metrics_includes_help_and_type():
    """Output includes HELP and TYPE lines for each metric."""
    m = PrometheusMetrics()
    text = m.get_metrics().decode()
    for name in EXPECTED_METRIC_NAMES:
        assert f"# HELP {name}" in text
        assert f"# TYPE {name}" in text


# -- label validation --


def test_histogram_labels_must_match():
    """Histogram raises ValueError when observing with wrong label names."""
    m = PrometheusMetrics()
    with pytest.raises(ValueError):
        m.response_duration.labels(wrong="label").observe(1.0)


def test_counter_labels_must_match():
    """Counter raises ValueError when incrementing with wrong label names."""
    m = PrometheusMetrics()
    with pytest.raises(ValueError):
        m.requests_total.labels(wrong="label").inc()


def test_gauge_no_labels():
    """Gauge without labelnames can be set directly."""
    m = PrometheusMetrics()
    m.escalation_queue_size.set(10)
    output = generate_latest(REGISTRY).decode()
    assert "omnibot_escalation_queue_size 10.0" in output


# -- separate registry --


def test_custom_registry_isolation():
    """Metrics registered on a custom registry do not appear in default REGISTRY."""
    custom = CollectorRegistry()
    h = Histogram(
        "test_custom_histogram",
        "Custom metric",
        registry=custom,
    )
    h.observe(0.5)
    assert "test_custom_histogram" not in generate_latest(REGISTRY).decode()
    assert "test_custom_histogram" in generate_latest(custom).decode()
