from fp_i09_ledger.conformance import run_conformance
def test_all_conformance_checks_pass(): assert all(run_conformance().values())
