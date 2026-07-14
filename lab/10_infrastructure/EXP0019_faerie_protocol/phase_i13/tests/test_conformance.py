from fp_i13_release.conformance import run_conformance
def test_all_conformance_checks_pass():assert all(run_conformance().values())
