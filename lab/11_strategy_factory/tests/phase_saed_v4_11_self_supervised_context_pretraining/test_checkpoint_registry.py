import copy,pytest
from saed_v4_self_supervised_pretraining.checkpoint import validate_checkpoint
from saed_v4_self_supervised_pretraining.registry import admitted_checkpoint_hash
from saed_v4_self_supervised_pretraining.errors import CheckpointError

def test_checkpoint_valid(load):validate_checkpoint(load('lab/11_strategy_factory/artifacts/saed_v4_11/GOLDEN_ENCODER_CHECKPOINT.JSON'))
def test_registry_admits_one(load):
 r=load('lab/11_strategy_factory/artifacts/saed_v4_11/GOLDEN_CHECKPOINT_REGISTRY.JSON');assert r['admitted_count']==1 and r['rejected_count']==0
def test_registry_hash_matches_checkpoint(load):
 r=load('lab/11_strategy_factory/artifacts/saed_v4_11/GOLDEN_CHECKPOINT_REGISTRY.JSON');c=load('lab/11_strategy_factory/artifacts/saed_v4_11/GOLDEN_ENCODER_CHECKPOINT.JSON');assert admitted_checkpoint_hash(r)==c['checkpoint_hash']
def test_execution_authority_tamper_rejected(load):
 c=copy.deepcopy(load('lab/11_strategy_factory/artifacts/saed_v4_11/GOLDEN_ENCODER_CHECKPOINT.JSON'));c['execution_authority']=True
 with pytest.raises(CheckpointError):validate_checkpoint(c)
def test_checkpoint_json_not_pickle(load):assert load('lab/11_strategy_factory/artifacts/saed_v4_11/GOLDEN_ENCODER_CHECKPOINT.JSON')['checkpoint_format']=='json_embedding_table_v1'
