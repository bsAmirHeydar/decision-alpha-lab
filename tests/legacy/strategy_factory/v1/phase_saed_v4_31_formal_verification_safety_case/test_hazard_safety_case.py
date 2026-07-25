import pytest
@pytest.mark.parametrize("index",range(10))
def test_each_hazard_controlled(result,index): assert result["mitigation_coverage"]["rows"][index]["controlled"]
@pytest.mark.parametrize("index",range(10))
def test_each_residual_risk_accepted(result,index):
 row=result["residual_risk"]["entries"][index]; assert row["accepted"] and row["residual_risk_score"]<=row["acceptance_threshold"] and row["production_acceptance"] is False
@pytest.mark.parametrize("index",range(12))
def test_each_safety_constraint_mandatory(result,index): assert result["constraints"]["constraints"][index]["mandatory"]
@pytest.mark.parametrize("index",range(22))
def test_each_assurance_node_satisfied(result,index): assert result["assurance_case"]["nodes"][index]["resolved_status"]=="satisfied"
@pytest.mark.parametrize("index",range(21))
def test_each_assurance_edge_closed(result,index): assert result["assurance_case"]["edges"][index]["relation"] in {"supported_by","in_context_of","solved_by","justified_by","assumed_by"}
