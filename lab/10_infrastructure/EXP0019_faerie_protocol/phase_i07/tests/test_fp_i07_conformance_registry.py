from fp_i07_confirmation.conformance import run_conformance
from fp_i07_confirmation.registry import validate_registry,REASON_CODES

def test_conformance_all_pass(): assert all(x[2] for x in run_conformance())
def test_conformance_has_five_pair_states(): assert len(run_conformance())==5
def test_registry_valid(): assert validate_registry()
def test_reason_registry_closed_and_sized(): assert len(REASON_CODES)>=19
