from __future__ import annotations
import pytest

def test_concept_control_gate(outputs): assert outputs["concept_probes"]["reference_gate_passed"]
def test_trace_claim_ceiling(outputs): assert outputs["causal_traces"]["claim_class"]=="causal_trace_challenger_not_causal_proof"
def test_patching_is_past_only(outputs): assert outputs["activation_patches"]["past_only"]
@pytest.mark.parametrize("i",range(20))
def test_trace_records_have_interventions(outputs,i): assert outputs["causal_traces"]["records"][i]["interventions"]
