import copy,pytest
from saed_v4_hidden_evaluation_air_gap.metrics import sigmoid,predict,calculate
from saed_v4_hidden_evaluation_air_gap.disclosure import release
from saed_v4_hidden_evaluation_air_gap.errors import DisclosureError

@pytest.mark.parametrize("x",[-100,-2,-1,0,1,2,100])
def test_sigmoid_bounded(x): assert 0.0<=sigmoid(x)<=1.0
def test_reference_candidate_passes(result): assert result["sealed_result"]["decision"]=="pass"
def test_all_pass_gates_true(result): assert all(result["sealed_result"]["pass_gates"].values())
def test_evaluation_exactly_once(result): assert result["sealed_result"]["evaluation_count"]==1
def test_evaluator_no_future_suffix(result): assert result["sealed_result"]["future_suffix_records_seen"]==0
def test_evaluator_no_network(result): assert result["sealed_result"]["network_access"] is False
def test_evaluator_no_raw_export(result): assert result["sealed_result"]["raw_rows_exported"] is False
def test_baseline_preserved(result): assert result["sealed_result"]["aggregate_metrics"]["delta_balanced_accuracy_vs_baseline"]>0
def test_disclosure_exact_allowlist(config,result): assert set(result["disclosure_envelope"])==set(config["disclosure_policy"]["allowed_fields"])
@pytest.mark.parametrize("forbidden",["record_id","hidden_label","prediction","probability","rows","confusion_matrix","feature_vector","key_share","plaintext"])
def test_disclosure_contains_no_forbidden_field(result,forbidden): assert forbidden not in str(result["disclosure_envelope"]).lower()
def test_disclosure_metrics_are_rounded(result): assert all(round(v,4)==v for v in result["disclosure_envelope"]["aggregate_metrics"].values())
def test_disclosure_hash_present(result): assert len(result["disclosure_envelope"]["release_hash"])==64
def test_release_policy_mutation_fails(config,result):
    bad=copy.deepcopy(config["disclosure_policy"]); bad["allowed_fields"].append("row")
    with pytest.raises(DisclosureError): release(result["sealed_result"],bad)
def test_metric_calculation_perfect():
    m=calculate([0,0,1,1],[0.1,0.2,0.8,0.9],[0,0,1,1]); assert m["accuracy"]==1 and m["balanced_accuracy"]==1 and m["roc_auc"]==1
