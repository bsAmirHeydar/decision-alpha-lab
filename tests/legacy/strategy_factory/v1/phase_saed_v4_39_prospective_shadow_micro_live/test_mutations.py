import copy,pytest
from saed_v4_prospective_shadow_micro_live import run_reference
from saed_v4_prospective_shadow_micro_live.errors import SAEDV439Error
M=[
("upstream_phase",lambda f:f["upstream_certificate"].__setitem__("phase","BAD")),("upstream_prod",lambda f:f["upstream_certificate"].__setitem__("production_authorized",True)),("upstream_hash",lambda f:f["upstream_handoff"].__setitem__("bundle_hash","0"*64)),
("constitution_order",lambda f:f["constitution"].__setitem__("automatic_order_submission_allowed",True)),("constitution_capital",lambda f:f["constitution"].__setitem__("capital_activation_allowed",True)),("constitution_unknown",lambda f:f["constitution"].__setitem__("unknown",1)),
("cohort_freeze",lambda f:f["cohort"].__setitem__("frozen_at","2026-06-02T00:00:00Z")),("cohort_outcomes",lambda f:f["cohort"]["outcome_fields_visible_at_freeze"].append("future_pnl")),("cohort_unlock",lambda f:f["cohort"].__setitem__("selection_locked",False)),("cohort_context",lambda f:f["observations"][0].__setitem__("context_id","UNFROZEN")),("cohort_duplicate",lambda f:f["observations"][1].__setitem__("observation_id",f["observations"][0]["observation_id"])),("cohort_future",lambda f:f["observations"][0].__setitem__("known_time","2026-07-01T00:00:00Z")),
("ladder_auto",lambda f:f["mode_ladder"].__setitem__("automatic_transition_allowed",True)),("ladder_live_manual",lambda f:f["mode_ladder"]["stages"][4].__setitem__("manual_authorization_required",False)),("ladder_pre_side_effect",lambda f:f["mode_ladder"]["stages"][2].__setitem__("side_effects_allowed",True)),("ladder_ordinal",lambda f:f["mode_ladder"]["stages"][2].__setitem__("ordinal",9)),
("broker_env",lambda f:f["broker_profile"].__setitem__("environment","LIVE")),("broker_creds",lambda f:f["broker_profile"].__setitem__("credentials_embedded",True)),("broker_cap",lambda f:f["broker_profile"]["capabilities"].remove("SHADOW_DECISIONS")),("broker_dup",lambda f:f["broker_profile"]["symbols"][1].__setitem__("symbol",f["broker_profile"]["symbols"][0]["symbol"])),
("risk_kill",lambda f:f["risk_envelope"].__setitem__("kill_switch_default_armed",False)),("risk_trade",lambda f:f["risk_envelope"].__setitem__("max_trade_risk_fraction",1.5)),("risk_latency",lambda f:f["risk_envelope"].__setitem__("max_latency_ms",0)),
("runbook_target",lambda f:f["incident_runbook"].__setitem__("rollback_target","LIVE")),("runbook_kill",lambda f:f["incident_runbook"].__setitem__("kill_switch_default_armed",False)),("runbook_dup",lambda f:f["incident_runbook"]["procedures"][1].__setitem__("procedure_id",f["incident_runbook"]["procedures"][0]["procedure_id"])),
("external_missing",lambda f:f["external_evidence"].pop()),("external_fake_pass",lambda f:(f["external_evidence"][0].__setitem__("status","PASSED"),f["external_evidence"][0].__setitem__("actual_external_evidence",False))),("external_hash",lambda f:f["external_evidence"][0].__setitem__("artifact_hash","bad")),
("reviews_missing",lambda f:f["reviews"].pop()),("reviews_duplicate",lambda f:f["reviews"][1].__setitem__("reviewer_id",f["reviews"][0]["reviewer_id"])),("reviews_not_independent",lambda f:f["reviews"][0].__setitem__("independent",False))]
@pytest.mark.parametrize("name,mut",M,ids=[x[0] for x in M])
def test_mutation_fails(fixture,name,mut):
 mut(fixture)
 with pytest.raises(SAEDV439Error):run_reference(fixture)
