def test_status_reference_synthetic(load):assert load('releases/history/strategy_factory/program/status/SAED_V4_11.json')['implementation_status']=='implemented_reference_synthetic'
def test_learned_reference_claim(load):assert load('releases/history/strategy_factory/program/status/SAED_V4_11.json')['claims']['learned_reference_representation']
def test_real_training_not_claimed(load):assert not load('releases/history/strategy_factory/program/status/SAED_V4_11.json')['claims']['real_corpus_training']
def test_alpha_not_claimed(load):
 c=load('releases/history/strategy_factory/artifacts/saed_v4_11/CLAIM_LEDGER.JSON');m={x['claim']:x['supported'] for x in c['claims']};assert not m['real_alpha'];assert not m['production_authorization'];assert not m['live_trading']
def test_metaeditor_pending(load):assert load('releases/history/strategy_factory/program/status/SAED_V4_11.json')['external_evidence']['metaeditor_compile']=='pending_local_windows'
