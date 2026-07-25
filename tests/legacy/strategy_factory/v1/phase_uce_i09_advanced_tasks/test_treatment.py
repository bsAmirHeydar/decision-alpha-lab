from strategy_factory_advanced_tasks_v3.golden import treatment_rows,mask
from strategy_factory_advanced_tasks_v3.treatment import DirectOutcomeSelector

def test_selector_respects_action_mask_and_support():
 rows,actions=treatment_rows();m=DirectOutcomeSelector(5).fit(rows,actions);row=rows[0];p=m.predict_one(row,mask(row.row_id,('wide_stop','tight_stop')));assert p.chosen_action_key in ('wide_stop','tight_stop');assert 'trail_runner' not in p.allowed_action_keys
