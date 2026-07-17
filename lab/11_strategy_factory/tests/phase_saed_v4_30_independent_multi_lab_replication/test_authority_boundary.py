import pytest
AUTH=["research_decision","promotion","runtime","risk_allocation","execution","production","online_learning","live_trading","raw_hidden_data_export","adaptive_replication","rerun_authority"]
@pytest.mark.parametrize("key",AUTH)
def test_every_authority_false(result,key): assert result["authority"]["authority"][key] is False
@pytest.mark.parametrize("key",["promotion_authority","runtime_executable","risk_allocation_authority","execution_authority","production_authority","online_learning_authority","live_trading_authority"])
def test_certificate_authority_false(result,key): assert result["certificate"][key] is False
@pytest.mark.parametrize("forbidden",["claim_external_replication_from_synthetic_fixture","promotion_authorization","runtime_compilation","risk_allocation","order_submission","production_release","online_policy_mutation"])
def test_handoff_forbidden(result,forbidden): assert forbidden in result["handoff"]["forbidden_next_work"]
