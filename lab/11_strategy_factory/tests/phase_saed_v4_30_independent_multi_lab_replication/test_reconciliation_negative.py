import copy,pytest
from saed_v4_independent_multi_lab_replication.reconciliation import reconcile
from saed_v4_independent_multi_lab_replication.adjudication import adjudicate
@pytest.mark.parametrize("lab_index",[0,1,2])
def test_semantic_disagreement_quarantines(result,lab_index):
 results=copy.deepcopy(result["results"]); results["records"][lab_index]["semantic_output_hash"]="f"*64
 semantic,metrics=reconcile(results,result["protocol"])
 report,_=adjudicate(result["registry"],result["independence"],result["runs"],results,semantic,metrics,result["protocol"])
 assert not report["accepted"] and report["decision"]=="quarantine"
@pytest.mark.parametrize("lab_index",[0,1,2])
@pytest.mark.parametrize("metric",["accuracy","brier","mean_probability"])
def test_metric_disagreement_quarantines(result,lab_index,metric):
 results=copy.deepcopy(result["results"]); results["records"][lab_index]["aggregate_metrics"][metric]+=0.1
 semantic,metrics=reconcile(results,result["protocol"])
 report,_=adjudicate(result["registry"],result["independence"],result["runs"],results,semantic,metrics,result["protocol"])
 assert not report["accepted"] and report["unresolved_disagreements"]>=1
