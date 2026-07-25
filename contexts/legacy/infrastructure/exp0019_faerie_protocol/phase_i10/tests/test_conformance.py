from fp_i10_indicator import *

def test_all_conformance(engine): assert all(run_conformance(engine).values())
def test_registry_authority():
 from fp_i10_indicator.registry import contract_registry
 assert contract_registry()['runtime_authority']=='NONE'
def test_registry_upstream():
 from fp_i10_indicator.registry import contract_registry
 assert tuple(x[0] for x in contract_registry()['upstream'])==EXPECTED_UPSTREAM_PHASES
