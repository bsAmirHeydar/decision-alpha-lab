import copy,pytest
from saed_v4_formal_verification_safety_case.service import run
from saed_v4_formal_verification_safety_case.canonical import content_hash
@pytest.mark.parametrize("iteration",range(12))
def test_full_run_deterministic(inputs,iteration): assert content_hash(run(copy.deepcopy(inputs)))==content_hash(run(copy.deepcopy(inputs)))
@pytest.mark.parametrize("field",["research_decision","promotion","runtime","risk_allocation","execution","production","online_learning","live_trading","specification_override","counterexample_suppression","residual_risk_waiver","external_proof_claim"])
def test_all_authority_fields_false(result,field): assert result["authority"]["authority"][field] is False
