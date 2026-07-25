def test_handoff_targets_v412(load):assert load('releases/history/strategy_factory/artifacts/saed_v4_11/V4_11_TO_V4_12_HANDOFF.JSON')['next_phase']=='SAED_V4_12'
def test_handoff_freezes_checkpoint(load):
 h=load('releases/history/strategy_factory/artifacts/saed_v4_11/V4_11_TO_V4_12_HANDOFF.JSON');c=load('releases/history/strategy_factory/artifacts/saed_v4_11/GOLDEN_ENCODER_CHECKPOINT.JSON');assert h['encoder_checkpoint_hash']==c['checkpoint_hash']
def test_handoff_entry_gates(load):assert all(load('releases/history/strategy_factory/artifacts/saed_v4_11/V4_11_TO_V4_12_HANDOFF.JSON')['entry_gates'].values())
def test_handoff_denies_decision_authority(load):
 a=load('releases/history/strategy_factory/artifacts/saed_v4_11/V4_11_TO_V4_12_HANDOFF.JSON')['authority'];assert not a['rank_treatments'] and not a['select_treatment'] and not a['send_order']
def test_handoff_preserves_tokenizer(load):assert len(load('releases/history/strategy_factory/artifacts/saed_v4_11/V4_11_TO_V4_12_HANDOFF.JSON')['tokenizer_hash'])==64
