import copy
from saed_v4_self_supervised_pretraining.contamination import audit_contamination,membership_audit

def test_golden_contamination_passes(load):assert load('lab/11_strategy_factory/artifacts/saed_v4_11/GOLDEN_CONTAMINATION_AUDIT.JSON')['passed']
def test_canaries_absent(load):assert load('lab/11_strategy_factory/artifacts/saed_v4_11/GOLDEN_MEMBERSHIP_AUDIT.JSON')['passed']
def test_canary_detected(records,load):
 split=load('lab/11_strategy_factory/artifacts/saed_v4_11/GOLDEN_SPLIT_MANIFEST.JSON');streams=load('lab/11_strategy_factory/artifacts/saed_v4_11/GOLDEN_TOKEN_STREAMS.JSON')['streams'];streams=copy.deepcopy(streams);streams[0]['tokens'].append('CANARY::X');a=audit_contamination(records,split,streams,['CANARY::X']);assert not a['passed']
def test_checkpoint_canary_detected(load):
 c=load('lab/11_strategy_factory/artifacts/saed_v4_11/GOLDEN_ENCODER_CHECKPOINT.JSON');assert not membership_audit(c,[c['vocabulary'][0]])['passed']
def test_no_cross_split_hash_issue(load):
 a=load('lab/11_strategy_factory/artifacts/saed_v4_11/GOLDEN_CONTAMINATION_AUDIT.JSON');assert not any(x['code']=='SOURCE_HASH_CROSS_SPLIT' for x in a['issues'])
