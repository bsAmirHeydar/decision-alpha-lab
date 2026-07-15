from saed_v4_self_supervised_pretraining.integrity import verify_integrity_receipt

def test_replay_passes(load):assert load('lab/11_strategy_factory/artifacts/saed_v4_11/GOLDEN_REPLAY_RECEIPT.JSON')['passed']
def test_replay_checkpoint_hash_equal(load):
 r=load('lab/11_strategy_factory/artifacts/saed_v4_11/GOLDEN_REPLAY_RECEIPT.JSON');assert r['expected_checkpoint_hash']==r['actual_checkpoint_hash']
def test_semantic_self_diff_empty(load):assert load('lab/11_strategy_factory/artifacts/saed_v4_11/GOLDEN_SEMANTIC_DIFF.JSON')['change_count']==0
def test_integrity_complete(load):
 i=load('lab/11_strategy_factory/artifacts/saed_v4_11/GOLDEN_INTEGRITY_RECEIPT.JSON');assert i['complete'] and i['entry_count']>=15
def test_hash_lengths(load):
 i=load('lab/11_strategy_factory/artifacts/saed_v4_11/GOLDEN_INTEGRITY_RECEIPT.JSON');assert len(i['receipt_hash'])==64 and len(i['merkle_root'])==64
