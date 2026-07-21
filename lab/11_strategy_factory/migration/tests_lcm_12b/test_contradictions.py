from tools.strategy_factory.lcm.lcm_12b.io import load_json
def test_contradictions_and_unknowns_remain_explicit(reconciliation_root):
    residual=load_json(reconciliation_root/"residual_documentation_issues.json")
    assert residual["upstream_contradiction_count"]>=1
    assert residual["upstream_unknown_count"]>=1
    assert residual["silent_harmonization_count"]==0
    assert residual["global_unknown_waiver_count"]==0
