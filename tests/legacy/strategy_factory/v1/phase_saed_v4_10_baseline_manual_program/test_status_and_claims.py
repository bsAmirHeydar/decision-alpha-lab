def test_status_is_reference_only(load):
 s=load('releases/history/strategy_factory/program/status/SAED_V4_10.json');assert s['implementation_status']=='implemented_reference';assert not s['claims']['model_training'];assert not s['claims']['real_alpha'];assert not s['claims']['production_authorization'];assert s['next_phase']=='SAED_V4_11'
def test_claim_ledger_denies_alpha(load):
 c=load('releases/history/strategy_factory/artifacts/saed_v4_10/CLAIM_LEDGER.JSON');m={x['claim']:x['supported'] for x in c['claims']};assert not m['real_alpha'];assert not m['model_training'];assert not m['treatment_selection']
