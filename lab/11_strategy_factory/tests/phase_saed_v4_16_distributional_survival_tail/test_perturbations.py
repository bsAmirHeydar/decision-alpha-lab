def test_future_suffix_all_pass(load):
 a=load('lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_FUTURE_SUFFIX_AUDITS.JSON');assert a['all_passed'] and all(x['passed'] and not x['future_suffix_accessed'] for x in a['items'])
def test_fail_closed_all_pass(load):
 a=load('lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_FAIL_CLOSED_AUDITS.JSON');assert a['all_passed'] and all(x['passed'] for x in a['rows'])
def test_censored_as_loss_rejected(load):
 a=load('lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_FAIL_CLOSED_AUDITS.JSON');assert next(x for x in a['rows'] if x['case']=='censored_as_loss_attempt')['directive']=='reject'
def test_unsupported_extreme_quarantined(load):
 a=load('lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_FAIL_CLOSED_AUDITS.JSON');assert next(x for x in a['rows'] if x['case']=='unsupported_extreme_extrapolation')['directive']=='quarantine'
