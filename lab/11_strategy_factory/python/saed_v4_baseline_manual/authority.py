from .errors import AuthorityError

AUTHORITY = {
    "compile_manual_program": True,
    "evaluate_frozen_baseline": True,
    "emit_descriptive_decision_trace": True,
    "build_pretraining_corpus_manifest": True,
    "read_multimodal_views": True,
    "read_action_lattice": True,
    "read_execution_twin_for_offline_benchmark": True,
    "train_model": False,
    "rank_treatments": False,
    "select_treatment": False,
    "allocate_risk": False,
    "activate_runtime": False,
    "send_order": False,
    "replace_shadow_or_prospective": False,
}
FORBIDDEN_TRUE={k for k,v in AUTHORITY.items() if not v}

def assert_reference_authority(candidate: dict) -> None:
    for key in FORBIDDEN_TRUE:
        if candidate.get(key) is True:
            raise AuthorityError(f"forbidden authority requested: {key}")

def boundary_record() -> dict:
    return {"phase":"SAED_V4_10","authority":"reference_only","capabilities":dict(AUTHORITY),"fail_closed":True}
