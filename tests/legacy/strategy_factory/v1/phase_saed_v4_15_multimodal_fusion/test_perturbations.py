def test_future_suffix_all_pass(load):
 a=load('releases/history/strategy_factory/artifacts/saed_v4_15/GOLDEN_FUTURE_SUFFIX_AUDITS.JSON');assert a['item_count']==10 and all(x['passed'] and not x['future_suffix_accessed'] for x in a['items'])
def test_fail_closed_all_pass(load):
 a=load('releases/history/strategy_factory/artifacts/saed_v4_15/GOLDEN_FAIL_CLOSED_AUDITS.JSON');assert all(x['all_passed'] for x in a['items'])
def test_corrupt_routes_quarantine(load):
 a=load('releases/history/strategy_factory/artifacts/saed_v4_15/GOLDEN_FAIL_CLOSED_AUDITS.JSON');assert all(next(r for r in x['rows'] if r['case']=='corrupt_dimension')['directive']=='quarantine' for x in a['items'])
def test_missing_critical_abstains(load):
 a=load('releases/history/strategy_factory/artifacts/saed_v4_15/GOLDEN_FAIL_CLOSED_AUDITS.JSON');assert all(next(r for r in x['rows'] if r['case']=='missing_critical_view')['directive']=='abstain' for x in a['items'])
