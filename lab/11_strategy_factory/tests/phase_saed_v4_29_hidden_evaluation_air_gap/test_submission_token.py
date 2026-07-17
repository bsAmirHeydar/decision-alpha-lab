import copy,pytest
from saed_v4_hidden_evaluation_air_gap.submission import commit
from saed_v4_hidden_evaluation_air_gap.token import issue,consume
from saed_v4_hidden_evaluation_air_gap.errors import TokenError

def test_submission_commitment_is_irreversible(result): assert result["submission_commitment"]["irreversible"] and result["submission_commitment"]["frozen"]
def test_submission_has_zero_network_dependencies(result): assert result["submission_commitment"]["network_dependency_count"]==0
def test_token_bound_to_candidate_dataset_protocol(result):
    t=result["issued_token"]; c=result["submission_commitment"]; assert t["candidate_commitment_hash"]==c["commitment_hash"] and t["dataset_commitment_hash"]==c["dataset_commitment_hash"] and t["protocol_hash"]==c["protocol_hash"]
def test_token_consumed_once(result): assert result["consumed_token"]["used_count"]==1
def test_token_reuse_rejected(result):
    with pytest.raises(TokenError): consume(result["consumed_token"],result["submission_commitment"],result["custody_receipt"],"2026-07-16T09:02:00Z")
def test_token_candidate_mismatch_rejected(result):
    bad=copy.deepcopy(result["submission_commitment"]); bad["commitment_hash"]="0"*64
    with pytest.raises(TokenError): consume(result["issued_token"],bad,result["custody_receipt"],"2026-07-16T09:02:00Z")
def test_token_dataset_mismatch_rejected(result):
    bad=copy.deepcopy(result["custody_receipt"]); bad["plaintext_commitment_hash"]="0"*64
    with pytest.raises(TokenError): consume(result["issued_token"],result["submission_commitment"],bad,"2026-07-16T09:02:00Z")
def test_candidate_mutation_changes_commitment(config,candidate,manifest):
    from saed_v4_hidden_evaluation_air_gap.contracts import parse_config
    p=parse_config(config); a=commit(candidate,p["evaluation_protocol"],manifest["plaintext_commitment_hash"]); bad=copy.deepcopy(candidate); bad["model_spec"]["weights"][0]+=0.01; b=commit(bad,p["evaluation_protocol"],manifest["plaintext_commitment_hash"]); assert a["commitment_hash"]!=b["commitment_hash"]
def test_protocol_mutation_changes_commitment(config,candidate,manifest):
    from saed_v4_hidden_evaluation_air_gap.contracts import parse_config
    p=parse_config(config); a=commit(candidate,p["evaluation_protocol"],manifest["plaintext_commitment_hash"]); proto=copy.deepcopy(p["evaluation_protocol"]); proto["random_seed"]+=1; b=commit(candidate,proto,manifest["plaintext_commitment_hash"]); assert a["commitment_hash"]!=b["commitment_hash"]
def test_dataset_mutation_changes_commitment(config,candidate,manifest):
    from saed_v4_hidden_evaluation_air_gap.contracts import parse_config
    p=parse_config(config); a=commit(candidate,p["evaluation_protocol"],manifest["plaintext_commitment_hash"]); b=commit(candidate,p["evaluation_protocol"],"0"*64); assert a["commitment_hash"]!=b["commitment_hash"]
