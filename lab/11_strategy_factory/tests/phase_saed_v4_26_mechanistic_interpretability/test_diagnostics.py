from __future__ import annotations
import pytest
@pytest.mark.parametrize("key",["faithfulness","sanity","stability","shortcut_audit"])
def test_reference_diagnostic_gates(outputs,key): assert outputs[key]["reference_gate_passed"]
def test_no_critical_failure(outputs): assert outputs["failure_catalogue"]["critical_count"]==0
@pytest.mark.parametrize("i",range(16))
def test_attribution_rows_have_finite_values(outputs,i):
 row=outputs["attributions"]["records"][i]
 assert all(abs(x["integrated_gradient"])<10 for x in row["feature_attributions"])
