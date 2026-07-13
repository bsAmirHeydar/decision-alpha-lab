from fp_i04_data.conformance import run_conformance
from fp_i04_data.registry import contract_registry,reason_registry

def test_contract_registry_closed_count():
    r=contract_registry();assert r['contract_count']==15 and len(r['registry_hash'])==64

def test_reason_registry_closed_count():
    r=reason_registry();assert r['reason_count']==30 and len(r['registry_hash'])==64

def test_conformance_passes():
    r=run_conformance();assert r['passed'] and r['check_count']==10
