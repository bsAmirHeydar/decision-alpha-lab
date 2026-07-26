from src.engine.tooling.strategy_factory.acl_os.acl_11.handoff_input import load_acl10_bundle
from src.engine.tooling.strategy_factory.acl_os.acl_11.registries import parity_registry
from src.engine.tooling.strategy_factory.acl_os.acl_11.parity import assess
from src.engine.tooling.strategy_factory.acl_os.acl_11.custody import *
def make(acl10):
    b=load_acl10_bundle(acl10); a=assess(b,parity_registry(),'2026-07-18T04:00:00Z'); g=build_generation_manifest(b,a); s=build_signing_plan(g); c=build_conformance_matrix(a); d=issue_decision(b,a,g,s,c,'2026-07-18T04:00:00Z'); return b,a,g,s,c,d
def test_empty_generation_manifest(acl10): assert make(acl10)[2]['generation_count']==0
def test_no_signing_material(acl10): assert make(acl10)[3]['key_material_present'] is False
def test_no_conformance_claim(acl10): assert make(acl10)[4]['decision_parity_proven'] is False
def test_non_executable_decision(acl10): assert make(acl10)[5]['decision']=='NON_EXECUTABLE_NO_RUNTIME_CANDIDATES'
def test_all_authorities_denied(acl10):
    d=make(acl10)[5]; assert not any(d[k] for k in ['runtime_generation_allowed','signature_creation_allowed','runtime_activation_allowed','live_order_submission_allowed','capital_activation_allowed'])
