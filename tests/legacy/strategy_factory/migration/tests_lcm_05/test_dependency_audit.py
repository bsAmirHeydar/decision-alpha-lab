from src.engine.tooling.strategy_factory.lcm.lcm_05.io import read_json,read_jsonl

def test_dependency_audit_counts(topology_root):
    s=read_json(topology_root/'dependencies/dependency_direction_audit.json');v=read_jsonl(topology_root/'dependencies/dependency_direction_violations.jsonl');assert s['violation_count']==len(v);assert s['evaluated_edge_count']==s['allowed_edge_count']+s['prohibited_edge_count']
def test_legacy_violation_not_approval(topology_root):
    s=read_json(topology_root/'dependencies/dependency_direction_audit.json');assert s['current_legacy_violations_are_target_topology_approval'] is False
def test_no_violation_waiver(topology_root):
    rows=read_jsonl(topology_root/'dependencies/dependency_direction_violations.jsonl');assert rows;assert all(x['waiver_allowed'] is False for x in rows)
