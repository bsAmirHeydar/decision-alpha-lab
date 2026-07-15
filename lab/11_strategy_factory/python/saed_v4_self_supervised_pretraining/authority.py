from .errors import AuthorityError

AUTHORITY = {
    "read_frozen_v4_10_handoff": True,
    "build_role_safe_corpus": True,
    "tokenize_known_time_inputs": True,
    "train_reference_synthetic_encoder": True,
    "evaluate_representation_offline": True,
    "register_research_checkpoint": True,
    "emit_v4_12_reference_handoff": True,
    "use_outcome_cube_as_input": False,
    "use_execution_twin_as_input": False,
    "use_protected_final": False,
    "use_prospective_shadow_live": False,
    "train_production_model": False,
    "predict_outcomes": False,
    "rank_treatments": False,
    "select_treatment": False,
    "allocate_risk": False,
    "activate_runtime": False,
    "send_order": False,
}
FORBIDDEN_TRUE={k for k,v in AUTHORITY.items() if not v}

def assert_reference_authority(candidate: dict) -> None:
    unknown=set(candidate)-set(AUTHORITY)
    if unknown: raise AuthorityError(f"unknown authority keys: {sorted(unknown)}")
    for key in FORBIDDEN_TRUE:
        if candidate.get(key) is True:
            raise AuthorityError(f"forbidden authority requested: {key}")

def boundary_record() -> dict:
    return {
      "phase":"SAED_V4_11","authority":"reference_synthetic_only",
      "capabilities":dict(AUTHORITY),"fail_closed":True,
      "runtime_authority":False,"execution_authority":False
    }
