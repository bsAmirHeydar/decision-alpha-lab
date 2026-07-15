import copy,pytest
from saed_v4_self_supervised_pretraining.validation import validate_upstream_manifest,validate_v4_10_handoff,validate_records,validate_training_config,scan_forbidden
from saed_v4_self_supervised_pretraining.errors import LeakageError,IntegrityError,ContractError

def test_upstream_contract(upstream):validate_upstream_manifest(upstream[0]);validate_v4_10_handoff(upstream[1],upstream[0])
def test_future_suffix_rejected(upstream):
 x=copy.deepcopy(upstream[0]);x['future_suffix_allowed']=True
 with pytest.raises(LeakageError):validate_upstream_manifest(x)
def test_handoff_hash_mismatch(upstream):
 x=copy.deepcopy(upstream[1]);x['pretraining_corpus_manifest_hash']='0'*64
 with pytest.raises(IntegrityError):validate_v4_10_handoff(x,upstream[0])
def test_records_valid(records):assert len(validate_records(records))==len(records)
def test_outcome_token_rejected(records):
 x=copy.deepcopy(records[:1]);x[0]['views']['price_view']['net_r']=1
 with pytest.raises(LeakageError):validate_records(x)
def test_config_valid(config):assert validate_training_config(config).deterministic
def test_nondeterminism_rejected(config):
 x=copy.deepcopy(config);x['deterministic']=False
 with pytest.raises(ContractError):validate_training_config(x)
def test_direct_forbidden_scan():
 with pytest.raises(LeakageError):scan_forbidden({'x':'protected_final'})
