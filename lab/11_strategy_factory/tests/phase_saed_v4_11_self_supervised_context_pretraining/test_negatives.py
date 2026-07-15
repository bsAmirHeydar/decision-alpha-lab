from saed_v4_self_supervised_pretraining.models import CorpusRecord
from saed_v4_self_supervised_pretraining.splits import assign_splits
from saed_v4_self_supervised_pretraining.tokenization import build_token_streams,build_tokenizer_spec
from saed_v4_self_supervised_pretraining.negatives import sample_token_negatives,sample_temporal_negative,build_negative_plan

def setup(records,load):
 o=[CorpusRecord.from_mapping(x) for x in records];sp=assign_splits(o,load('lab/11_strategy_factory/examples/saed_v4_11/reference_split_policy.json'));ss=build_token_streams(o,sp);return ss,build_tokenizer_spec(ss)
def test_negative_excludes_positive(records,load):
 ss,t=setup(records,load);p=next(x for x in ss[0].tokens if not x.startswith('['));assert p not in sample_token_negatives(t['vocabulary'],p,3,'x')
def test_temporal_negative_different_root(records,load):
 ss,_=setup(records,load);a=next(x for x in ss if x.split=='train');n=sample_temporal_negative(a,ss,'x');assert a.root_context_id!=n.root_context_id
def test_plan_dependency_safe(records,load):
 ss,t=setup(records,load);assert build_negative_plan(ss,t['vocabulary'],3,1)['dependency_safe']
def test_plan_deterministic(records,load):
 ss,t=setup(records,load);assert build_negative_plan(ss,t['vocabulary'],3,1)['plan_hash']==build_negative_plan(ss,t['vocabulary'],3,1)['plan_hash']
