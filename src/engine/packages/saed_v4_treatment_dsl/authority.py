from __future__ import annotations

from .errors import AuthorityError
from .models import TreatmentDslAuthorityBoundary


def validate_authority(boundary: TreatmentDslAuthorityBoundary) -> None:
    required = (
        "read_hypergraph",
        "read_handoff",
        "define_finite_dsl",
        "canonicalize_program",
        "validate_program",
        "bind_external_descriptor",
        "replay_and_diff",
    )
    forbidden = (
        "mutate_ucee_truth",
        "mutate_hypergraph",
        "infer_context_truth",
        "generate_unbounded_actions",
        "solve_action_lattice",
        "select_treatment",
        "train_model",
        "allocate_risk",
        "activate_runtime",
        "send_order",
        "network_access",
    )
    missing = sorted(name for name in required if not getattr(boundary, name))
    excess = sorted(name for name in forbidden if getattr(boundary, name))
    if missing or excess:
        raise AuthorityError(f"invalid V4-06 authority boundary; missing={missing} forbidden={excess}")
