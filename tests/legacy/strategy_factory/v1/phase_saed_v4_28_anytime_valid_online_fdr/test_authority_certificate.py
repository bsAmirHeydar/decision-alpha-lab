import pytest

def test_certificate_accepted(outputs): assert outputs["certificate"]["accepted_for_online_fdr_research_reference"]
@pytest.mark.parametrize("claim",["real_world_fdr_guarantee_claim","real_alpha_claim","prospective_success_claim","hidden_evaluation_air_gap_claim","independent_replication_claim","promotion_authority","runtime_executable","risk_allocation_authority","execution_authority","production_authority","online_learning_authority"])
def test_forbidden_claims_false(outputs,claim): assert outputs["certificate"][claim] is False
@pytest.mark.parametrize("gate",["upstream_verified","anytime_registry_complete","known_time_enforced","family_allocation_frozen","family_weights_normalized","wealth_ledger_verified","wealth_nonnegative","rejection_ledger_verified","stopping_rules_safe","online_fdr_audit_passed","security_passed","authority_zero"])
def test_certificate_gate(outputs,gate): assert outputs["certificate"]["gates"][gate]
def test_authority_zero(outputs): assert not any(outputs["authority_boundary"]["authority"].values())
def test_ucee_preserved(outputs): assert outputs["authority_boundary"]["ucee_authority_preserved"]
def test_handoff_next_phase(outputs): assert outputs["handoff"]["next_phase"]=="SAED_V4_29"
def test_handoff_research_only(outputs): assert outputs["handoff"]["research_only"] and not any(outputs["handoff"]["authority"].values())
def test_hidden_access_forbidden(outputs): assert "unsealed_hidden_evaluation_access" in outputs["handoff"]["forbidden_next_work"]
def test_air_gap_allowed(outputs): assert "hidden_evaluation_air_gap_policy" in outputs["handoff"]["allowed_next_work"]
