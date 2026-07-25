import pytest

def test_authority_research_only(outputs): assert outputs["authority_boundary"]["research_only"]
@pytest.mark.parametrize("field",["decision","promotion","runtime","risk_allocation","execution","production","online_learning"])
def test_authority_zero(outputs,field): assert outputs["authority_boundary"]["authority"][field] is False
def test_certificate_accepted(outputs): assert outputs["certificate"]["accepted_for_complete_ledger_research"]
@pytest.mark.parametrize("field",["real_alpha_claim","prospective_success_claim","promotion_authority","runtime_executable","risk_allocation_authority","execution_authority","production_authority","online_learning_authority","online_fdr_claim","hidden_evaluation_air_gap_claim"])
def test_certificate_claims_denied(outputs,field): assert outputs["certificate"][field] is False
@pytest.mark.parametrize("gate",["upstream_verified","trial_ledger_complete","exposure_ledger_complete","multiplicity_universe_complete","completeness_audit_passed","integrity_report_passed","budget_respected","protected_exposure_zero","hidden_query_zero","authority_zero","security_passed"])
def test_certificate_gates(outputs,gate): assert outputs["certificate"]["gates"][gate]
def test_handoff_next(outputs): assert outputs["handoff"]["next_phase"]=="SAED_V4_28"
def test_handoff_research_only(outputs): assert outputs["handoff"]["research_only"]
def test_handoff_no_authority(outputs): assert not any(outputs["handoff"]["authority"].values())
def test_handoff_scope(outputs): assert "online_fdr_wealth_ledger" in outputs["handoff"]["allowed_next_work"]
