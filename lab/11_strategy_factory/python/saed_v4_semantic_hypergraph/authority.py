from __future__ import annotations

from .errors import AuthorityError
from .models import HypergraphAuthorityBoundary


def validate_authority(boundary: HypergraphAuthorityBoundary) -> None:
    required_true = (
        "read_multimodal_package",
        "read_view_lineage",
        "build_hypergraph",
        "replay_hypergraph",
        "query_hypergraph",
        "project_baseline",
    )
    forbidden_true = (
        "mutate_ucee_truth",
        "mutate_view_artifacts",
        "infer_canonical_relations",
        "fit_adaptive_statistics",
        "learn_edges",
        "train_model",
        "generate_treatment",
        "select_treatment",
        "allocate_risk",
        "activate_runtime",
        "send_order",
        "network_access",
    )
    missing = [name for name in required_true if not getattr(boundary, name)]
    forbidden = [name for name in forbidden_true if getattr(boundary, name)]
    if missing or forbidden:
        raise AuthorityError(
            f"invalid V4-05 authority boundary; missing={sorted(missing)} forbidden={sorted(forbidden)}"
        )
