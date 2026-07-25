import json
def load(ACL12,rel): return json.loads((ACL12/rel).read_text())
def test_non_production_decision(ACL12): assert load(ACL12,'decision/security_readiness_decision.json')['decision']=='REFERENCE_SECURITY_HARDENED_PRODUCTION_NOT_READY'
def test_production_not_ready(ACL12): assert load(ACL12,'decision/security_readiness_decision.json')['production_security_ready'] is False
def test_assessment_handoff_allowed(ACL12): assert load(ACL12,'decision/security_readiness_decision.json')['assessment_product_handoff_allowed'] is True
def test_no_runtime_authority(ACL12):
    d=load(ACL12,'decision/security_readiness_decision.json'); assert not d['runtime_generation_allowed'] and not d['runtime_activation_allowed']
def test_no_capital_authority(ACL12):
    d=load(ACL12,'decision/security_readiness_decision.json'); assert not d['live_order_submission_allowed'] and not d['capital_activation_allowed']
