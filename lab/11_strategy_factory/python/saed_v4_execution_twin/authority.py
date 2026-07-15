from __future__ import annotations
from typing import Mapping, Any
from .errors import AuthorityError, IntegrityError

REQUIRED_HANDOFF_AUTHORITY = {
    "read_frozen_outcome_cube": True,
    "read_path_events": True,
    "read_cost_breakdowns": True,
    "build_execution_digital_twin": True,
    "mutate_outcome_cube": False,
    "rank_treatments": False,
    "select_treatment": False,
    "allocate_risk": False,
    "activate_runtime": False,
    "send_order": False,
    "use_future_information_at_decision_time": False,
}

OUTPUT_AUTHORITY = {
    "descriptive_execution_replay": True,
    "stress_execution_assumptions": True,
    "preserve_source_outcomes": True,
    "replace_shadow_or_prospective": False,
    "mutate_outcome_cube": False,
    "rank_treatments": False,
    "select_treatment": False,
    "allocate_risk": False,
    "activate_runtime": False,
    "send_order": False,
}


def validate_handoff(cube: Mapping[str, Any], handoff: Mapping[str, Any]) -> None:
    if handoff.get("phase") != "SAED_V4_08" or handoff.get("next_phase") != "SAED_V4_09":
        raise AuthorityError("handoff phase boundary is invalid")
    if handoff.get("cube_id") != cube.get("cube_id") or handoff.get("cube_hash") != cube.get("cube_hash"):
        raise IntegrityError("handoff does not bind the supplied cube")
    if not handoff.get("complete_exposure") or not cube.get("complete_exposure"):
        raise IntegrityError("incomplete V4-08 exposure cannot enter V4-09")
    authority = handoff.get("authority", {})
    if authority != REQUIRED_HANDOFF_AUTHORITY:
        raise AuthorityError("handoff authority matrix mismatch")
    if cube.get("selection_authority") or cube.get("execution_authority"):
        raise AuthorityError("V4-08 source cube carries prohibited authority")
