def test_tail_summaries(load):
 t=load('lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_TAIL_RISK_SUMMARIES.JSON');assert t['row_count']==6 and all(x['expected_shortfall']<=x['value_at_risk']+1e-12 for x in t['rows'])
def test_tail_calibration_rows(load):
 t=load('lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_TAIL_CALIBRATION_REPORT.JSON');assert t['row_count']==10 and all(x['exceedance_error']>=0 for x in t['rows'])
def test_time_calibration_rows(load):
 t=load('lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_TIME_CALIBRATION_REPORT.JSON');assert t['row_count']==25 and all(0<=x['predicted_event_probability']<=1 and 0<=x['observed_event_rate']<=1 for x in t['rows'])
def test_distribution_calibration_rows(load):
 t=load('lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_DISTRIBUTION_CALIBRATION_REPORT.JSON');assert t['row_count']==45 and all(x['absolute_calibration_error']>=0 for x in t['rows'])
