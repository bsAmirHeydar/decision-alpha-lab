from __future__ import annotations

import hashlib
from dataclasses import replace

from saed_v4_multimodal_views.catalog import institutional_view_catalog
from saed_v4_multimodal_views.enums import EvidenceRole as ViewEvidenceRole
from saed_v4_multimodal_views.models import SourceValue, ViewBuildRequest
from saed_v4_multimodal_views.service import MultimodalViewService
from saed_v4_semantic_hypergraph.builder import SemanticTemporalHypergraphBuilder
from saed_v4_semantic_hypergraph.catalog import institutional_policy, institutional_registry

TWIN = "twin_golden"
EVENT_AS_OF = "2026-01-05T14:30:00Z"
KNOWN_AS_OF = "2026-01-05T14:30:01Z"


def source(
    namespace,
    path,
    value,
    event_time=EVENT_AS_OF,
    known_time=KNOWN_AS_OF,
    quality=1.0,
    role=ViewEvidenceRole.DEVELOPMENT,
    artifact=None,
    conflict=False,
):
    artifact = artifact or f"artifact_{namespace}"
    return SourceValue(
        namespace,
        path,
        value,
        event_time,
        known_time,
        quality,
        role,
        artifact,
        hashlib.sha256(artifact.encode()).hexdigest(),
        (f"lineage_{namespace}",),
        conflict,
    )


def golden_sources():
    return (
        source("projection", "bid", 20000.0),
        source("projection", "ask", 20000.5),
        source("projection", "last_trade_price", 20000.25),
        source("projection", "previous_trade_price", 19999.75, "2026-01-05T14:29:58Z"),
        source("projection", "reference_touch_count", 2),
        source("projection", "last_event_marker", 1),
        source("projection", "related_symbol_score", 0.65, "2026-01-05T14:29:59Z"),
        source("projection", "quote_rate", 42.0),
        source("projection", "trade_rate", 12.0),
        source("projection", "gap_count", 0),
        source("projection", "session_boundary_recent", False),
        source("twin", "lifecycle_state", "valid"),
        source("twin", "twin_state", "observing"),
        source("twin", "context_fresh", True),
        source("twin", "support_score", 0.96),
        source("twin", "context_start_time", "2026-01-05T14:00:00Z", "2026-01-05T14:00:00Z"),
        source("twin", "htf_alignment", 0.8),
        source("twin", "htf_phase", "bullish"),
        source("twin", "htf_fresh", True),
        source("twin", "context_family", "F2"),
        source("twin", "parent_context_id", "ctx_parent"),
        source("twin", "generation_depth", 2),
        source("twin", "transition_code_1", 1),
        source("twin", "transition_code_2", 3),
        source("static", "hour_utc", 14),
        source("static", "weekday_utc", 0),
        source("static", "cross_market_state", "confirming"),
        source("static", "liquidity_state", "normal"),
        source("static", "session_id", "new_york"),
        source("static", "session_open", True),
        source("static", "minutes_from_open", 0),
        source("execution", "spread_points", 0.5),
        source("execution", "estimated_slippage_points", 0.1),
        source("execution", "latency_ms", 25.0),
        source("execution", "broker_state", "normal"),
        source("approved_treatment", "descriptor_id", "treatment_approved_001"),
        source("approved_treatment", "payoff_profile", "P3"),
        source("approved_treatment", "entry_mechanism", "breakout"),
        source("approved_treatment", "path_dependent", True),
    )


def build_package(sources=None, include_views=None, request_id="v405-test"):
    service = MultimodalViewService()
    specs = institutional_view_catalog(TWIN)
    if include_views is not None:
        specs = tuple(spec for spec in specs if spec.view_name in set(include_views))
    for spec in specs:
        service.register_specification(spec)
    request = ViewBuildRequest(
        TWIN,
        KNOWN_AS_OF,
        EVENT_AS_OF,
        ViewEvidenceRole.DEVELOPMENT,
        tuple(sources or golden_sources()),
        request_id,
    )
    views = tuple(service.build_view(spec, request) for spec in specs)
    required = tuple(spec.view_name for spec in specs if spec.required_view)
    return service.build_package(views, "1.0.0", required)


def build_graph(package=None, registry=None, policy=None):
    package = package or build_package()
    registry = registry or institutional_registry()
    policy = policy or institutional_policy()
    return SemanticTemporalHypergraphBuilder().build(package, registry, policy)


def changed_sources(namespace, path, value):
    return tuple(
        replace(item, value=value)
        if item.namespace == namespace and item.path == path
        else item
        for item in golden_sources()
    )
