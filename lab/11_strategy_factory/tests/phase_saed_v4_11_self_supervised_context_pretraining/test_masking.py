from saed_v4_self_supervised_pretraining.models import CorpusRecord
from saed_v4_self_supervised_pretraining.splits import assign_splits
from saed_v4_self_supervised_pretraining.tokenization import build_token_streams
from saed_v4_self_supervised_pretraining.masking import deterministic_mask_positions,apply_mask,build_masking_plan

def streams(records,load):
 o=[CorpusRecord.from_mapping(x) for x in records];s=assign_splits(o,load('lab/11_strategy_factory/examples/saed_v4_11/reference_split_policy.json'));return build_token_streams(o,s)
def test_mask_deterministic(records,load):
 s=streams(records,load)[0];assert deterministic_mask_positions(s,1)==deterministic_mask_positions(s,1)
def test_mask_has_target(records,load):
 s=streams(records,load)[0];m=apply_mask(s,deterministic_mask_positions(s,1));assert len(m['targets'])>=1
def test_special_tokens_not_masked(records,load):
 s=streams(records,load)[0];pos=deterministic_mask_positions(s,1);assert all(not s.tokens[i].startswith('[') for i in pos)
def test_plan_train_only(records,load):
 ss=streams(records,load);p=build_masking_plan(ss,1);assert p['record_count']==sum(x.split=='train' for x in ss)
