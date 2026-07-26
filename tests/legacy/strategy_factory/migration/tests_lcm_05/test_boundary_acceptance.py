from src.engine.tooling.strategy_factory.lcm.lcm_05.io import read_json

def test_generated_noncanonical(topology_root):
    b=read_json(topology_root/'topology/authored_generated_boundary.json');assert b['generated_can_be_domain_authority'] is False;assert b['generated_can_override_authored'] is False
def test_acceptance_reference_only(topology_root):
    a=read_json(topology_root/'reports/acceptance_report.json');assert a['acceptance_gate_passed'];assert a['acceptance_state']=='REFERENCE_TOPOLOGY_ACCEPTED_MATERIALIZATION_BLOCKED';assert a['broad_file_movement_performed'] is False
def test_summary_no_authority(topology_root):
    s=read_json(topology_root/'reports/topology_summary.json');assert not s['target_materialization_allowed'];assert not s['runtime_authority_created'];assert not s['live_order_authority_created'];assert not s['capital_authority_created']
def test_hostile_review(topology_root):
    h=read_json(topology_root/'reports/hostile_review.json');assert h['hostile_review_passed'];assert all(x['status']=='PASS' for x in h['checks'])
