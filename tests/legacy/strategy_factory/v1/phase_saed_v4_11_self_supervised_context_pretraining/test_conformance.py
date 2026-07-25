def test_conformance_passes(load):
 r=load('releases/history/strategy_factory/artifacts/saed_v4_11/CONFORMANCE_RESULTS.JSON');assert r['passed'];assert r['case_count']==8
def test_negative_cases_observed_invalid(load):
 r=load('releases/history/strategy_factory/artifacts/saed_v4_11/CONFORMANCE_RESULTS.JSON');neg=[x for x in r['results'] if not x['expected_valid']];assert neg and all(not x['observed_valid'] for x in neg)
def test_positive_cases_observed_valid(load):
 r=load('releases/history/strategy_factory/artifacts/saed_v4_11/CONFORMANCE_RESULTS.JSON');pos=[x for x in r['results'] if x['expected_valid']];assert pos and all(x['observed_valid'] for x in pos)
