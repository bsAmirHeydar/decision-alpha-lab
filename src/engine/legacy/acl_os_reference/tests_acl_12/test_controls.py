import json
from src.engine.tooling.strategy_factory.acl_os.acl_12.registries import security_control_registry,threat_registry
def load(ACL12,rel): return json.loads((ACL12/rel).read_text())
def test_control_registry_closed():
    r=security_control_registry(); assert r['closed'] and r['control_count']==33
def test_threat_registry_closed():
    r=threat_registry(); assert r['closed'] and r['threat_count']==14
def test_matrix_count(ACL12):
    m=load(ACL12,'assessment/security_control_matrix.json'); assert m['control_count']==33
def test_unknown_blocks_production(ACL12):
    m=load(ACL12,'assessment/security_control_matrix.json'); assert m['status_counts']['UNKNOWN']>0 and not m['all_production_controls_satisfied']
def test_reference_hardening_passes(ACL12):
    m=load(ACL12,'assessment/security_control_matrix.json'); assert m['reference_hardening_passed'] and m['status_counts']['UNSATISFIED']==0
def test_risk_not_auto_accepted(ACL12):
    r=load(ACL12,'risk/security_risk_register.json'); assert not r['automatic_risk_acceptance_allowed']
