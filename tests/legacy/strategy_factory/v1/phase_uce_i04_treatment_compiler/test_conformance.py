from strategy_factory_treatment_compiler_v3.conformance import run_conformance
def test_conformance():
 r=run_conformance(); assert r['passed'],r
