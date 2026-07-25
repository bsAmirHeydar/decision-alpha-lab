from __future__ import annotations
import copy, pytest
from saed_v4_mechanistic_interpretability import run

def test_attributions_complete(outputs,records): assert len(outputs["attributions"]["records"])==len(records)
def test_pathways_exact(outputs): assert {x["pathway"] for x in outputs["pathways"]["records"][0]["pathways"]}=={"transfer","adaptation","calibration","view_fusion","treatment_interaction"}
@pytest.mark.parametrize("record_index",range(12))
def test_future_target_mutation_does_not_change_decision_time_artifacts(config,upstream,records,outputs,record_index):
 m=copy.deepcopy(records); m[record_index]["observed_target"]+=1000; second=run(config,upstream,m)
 for key in ["attributions","pathways","adaptation_mechanisms","calibration_mechanisms","concept_probes","causal_traces","activation_patches","counterfactuals","sparse_dictionary"]: assert outputs[key]==second[key]
