import copy
from saed_v4_federated_confidential_research.service import run

def test_future_suffix_ignored(inputs):
 a=run(inputs);x=copy.deepcopy(inputs);x["local_updates"].append({"update_id":"FUT","cell_id":"CELL-AMS-001","round_id":"ROUND-001","known_time":"2028-01-01T00:00:00Z","sample_count":999999,"vector":[999,999,999],"local_loss_before":9,"local_loss_after":0,"synthetic_fixture":True});b=run(x);assert a["global_model"]["global_model_hash"]==b["global_model"]["global_model_hash"]
def test_exact_determinism(inputs): assert run(inputs)==run(copy.deepcopy(inputs))
def test_no_raw_vectors_in_export(result):
 text=str(result["envelopes"])+str(result["aggregation_transcript"])+str(result["provenance"])
 assert "1.8" not in text and "raw_payload_present': True" not in text
def test_outlier_is_accounted(result): assert result["screening"]["records"] and result["incidents"]["all_contained"]
def test_global_model_non_executable(result): assert result["global_model"]["runtime_executable"] is False and result["global_model"]["promotion_eligible"] is False
