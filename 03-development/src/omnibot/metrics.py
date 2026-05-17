"""[FR-22] Prometheus Metrics — Core Instrumentation.

Exports 8 core Prometheus metrics via the prometheus-client library.
Metrics are registered at import time on the default REGISTRY.

Citations: SRS.md:214-230, SAD.md:511-531
"""

from prometheus_client import Counter, Gauge, Histogram, generate_latest, REGISTRY


class PrometheusMetrics:
    """Prometheus metrics instrumentation for Omnibot.

    All 8 metrics are registered on the default REGISTRY at init time.
    Use get_metrics() to produce the Prometheus text format for scraping.

    Citations: SRS.md FR-22, SAD.md 2.5.9 PrometheusMetrics
    """

    def __init__(self) -> None:
        self.response_duration = Histogram(
            "omnibot_response_duration_seconds",
            "Response duration in seconds by platform and knowledge source",
            labelnames=["platform", "knowledge_source"],
            buckets=[0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0],
            registry=REGISTRY,
        )
        self.requests_total = Counter(
            "omnibot_requests_total",
            "Total requests by platform and status",
            labelnames=["platform", "status"],
            registry=REGISTRY,
        )
        self.fcr_total = Counter(
            "omnibot_fcr_total",
            "First contact resolution totals",
            labelnames=["resolved"],
            registry=REGISTRY,
        )
        self.knowledge_hit_total = Counter(
            "omnibot_knowledge_hit_total",
            "Knowledge layer hit counts",
            labelnames=["layer"],
            registry=REGISTRY,
        )
        self.pii_masked_total = Counter(
            "omnibot_pii_masked_total",
            "PII masking events by PII type",
            labelnames=["pii_type"],
            registry=REGISTRY,
        )
        self.escalation_queue_size = Gauge(
            "omnibot_escalation_queue_size",
            "Current escalation queue length",
            registry=REGISTRY,
        )
        self.emotion_escalation_total = Counter(
            "omnibot_emotion_escalation_total",
            "Total emotion escalation events",
            registry=REGISTRY,
        )
        self.llm_tokens_total = Counter(
            "omnibot_llm_tokens_total",
            "Total LLM tokens by model and direction",
            labelnames=["model", "direction"],
            registry=REGISTRY,
        )

    def get_metrics(self) -> bytes:
        """Return all metrics in Prometheus text format."""
        return generate_latest(REGISTRY)
