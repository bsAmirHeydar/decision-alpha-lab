from fp_i12_operator import *
def test_conformance():assert all(run_conformance().values())
def test_contract_registry():assert 'OperatorOutput' in PUBLIC_CONTRACTS
def test_reason_registry_closed():assert len(REASON_CODES)==len(set(REASON_CODES))
