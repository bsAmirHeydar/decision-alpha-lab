from .conftest import jl
def test_only_cutover_ready_context_can_be_canonical_reference():
 b=jl("bindings/setup_context_binding_registry.jsonl"); assert all(x["canonical_context_identity_id"] in {None,"CTX_EXP0015_INTERMARKET_TIME_EXPERIMENT_3CD87586_V1"} for x in b)
def test_blocked_context_candidates_are_noncanonical_evidence():
 b=jl("bindings/setup_context_binding_registry.jsonl"); assert all(not x["legacy_candidates_are_canonical_references"] for x in b); assert sum(x["canonical_context_identity_id"] is not None for x in b)==0
