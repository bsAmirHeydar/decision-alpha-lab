from __future__ import annotations
import pytest

def test_dictionary_control(outputs): assert outputs["sparse_dictionary"]["reference_gate_passed"]
def test_counterfactual_no_authority(outputs): assert outputs["counterfactuals"]["decision_authority"] is False
@pytest.mark.parametrize("i",range(20))
def test_counterfactual_rows_are_bounded(outputs,i):
 row=outputs["counterfactuals"]["records"][i]
 if row["counterfactual"] is not None: assert abs(row["counterfactual"]["delta"])<=1.0
