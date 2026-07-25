from saed_v4_self_supervised_pretraining.models import CorpusRecord
from saed_v4_self_supervised_pretraining.splits import assign_splits
from saed_v4_self_supervised_pretraining.tokenization import build_token_streams,build_tokenizer_spec

def setup(records,load):
 o=[CorpusRecord.from_mapping(x) for x in records];s=assign_splits(o,load('examples/legacy/strategy_factory/saed_v4_11/reference_split_policy.json'));streams=build_token_streams(o,s);return streams,build_tokenizer_spec(streams)
def test_all_records_tokenized(records,load):assert len(setup(records,load)[0])==len(records)
def test_special_tokens_present(records,load):assert '[MASK]' in setup(records,load)[1]['vocabulary']
def test_token_hash_deterministic(records,load):
 a,b=setup(records,load)[0],setup(records,load)[0];assert [x.token_hash for x in a]==[x.token_hash for x in b]
def test_no_forbidden_tokens(records,load):
 vocab=setup(records,load)[1]['vocabulary'];assert not any('outcome_cube' in x.lower() or 'net_r' in x.lower() for x in vocab)
def test_closed_unknown_policy(records,load):assert setup(records,load)[1]['unknown_policy']=='fail_closed_to_[UNK]'
