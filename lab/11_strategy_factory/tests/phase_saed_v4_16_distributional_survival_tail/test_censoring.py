def test_censoring_audit_pass(load):
 a=load('lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_CENSORING_AUDIT.JSON');assert a['passed'] and a['violation_count']==0 and a['censored_as_outcome_count']==0
def test_censoring_exists(load):
 a=load('lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_CENSORING_AUDIT.JSON');assert a['right_censored_count']>0 and a['interval_censored_count']>0
def test_ipcw_bounded(load):
 x=load('lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_IPCW_WEIGHTS.JSON');assert all(0<x['floor']<=r['censor_survival']<=1 and 0<r['ipcw_weight']<=x['ceiling'] for r in x['items'])
def test_risk_sets_valid(load):
 x=load('lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_RISK_SET_LEDGER.JSON');assert x['all_risk_sets_nonnegative'] and all(sum(r['cause_events'].values())==r['observed_events'] for r in x['rows'])
def test_censored_never_labeled_outcome(load):
 d=load('lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_SURVIVAL_DATASET.JSON');assert all(not r['outcome_observed'] for r in d['rows'] if not r['event_observed'])
