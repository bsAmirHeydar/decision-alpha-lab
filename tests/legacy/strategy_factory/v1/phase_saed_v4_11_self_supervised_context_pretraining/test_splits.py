import copy,pytest
from saed_v4_self_supervised_pretraining.models import CorpusRecord
from saed_v4_self_supervised_pretraining.splits import assign_splits
from saed_v4_self_supervised_pretraining.errors import LeakageError,SplitError

def objs(records):return [CorpusRecord.from_mapping(x) for x in records]
def test_split_counts(records,load):
 m=assign_splits(objs(records),load('examples/legacy/strategy_factory/saed_v4_11/reference_split_policy.json'));assert m['counts']=={'train':12,'validation':4,'test':4,'quarantine':2}
def test_identity_disjoint(records,load):assert assign_splits(objs(records),load('examples/legacy/strategy_factory/saed_v4_11/reference_split_policy.json'))['identity_disjoint']
def test_unknown_root_rejected(records,load):
 x=copy.deepcopy(records[:1]);x[0]['root_context_id']='unknown'
 with pytest.raises(SplitError):assign_splits(objs(x),load('examples/legacy/strategy_factory/saed_v4_11/reference_split_policy.json'))
def test_time_cutoff_rejected(records,load):
 x=copy.deepcopy(records);x[0]['known_time']='2026-01-06T00:00:00Z'
 with pytest.raises(LeakageError):assign_splits(objs(x),load('examples/legacy/strategy_factory/saed_v4_11/reference_split_policy.json'))
