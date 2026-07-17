import pytest

def test_universe_complete(outputs): assert outputs["multiplicity_universe"]["complete_materially_related_universe"]
def test_universe_family_count(outputs): assert outputs["multiplicity_universe"]["family_count"]==6
def test_universe_trial_count(outputs): assert outputs["multiplicity_universe"]["trial_count"]==36
def test_universe_exposure_count(outputs): assert outputs["multiplicity_universe"]["exposure_count"]==44
@pytest.mark.parametrize("field",["failed_trials_included","pruned_trials_included","duplicates_included","retries_included","human_exposures_included","agent_exposures_included","selection_risk_ready"])
def test_universe_inclusion_flags(outputs,field): assert outputs["multiplicity_universe"][field]
def test_completeness_passes(outputs): assert outputs["completeness_audit"]["passed"]
@pytest.mark.parametrize("field",["all_manifests_hash_bound","expected_trials_equal_observed","all_trials_terminal","no_orphan_trials","no_missing_trials","failure_states_accounted","duplicates_accounted","retries_accounted","trial_chain_verified","exposure_chain_verified","protected_exposure_zero","hidden_query_zero","multiplicity_complete"])
def test_completeness_checks(outputs,field): assert outputs["completeness_audit"]["checks"][field]
def test_integrity_passes(outputs): assert outputs["integrity_report"]["passed"]
@pytest.mark.parametrize("field",["trial_hash_chain","exposure_hash_chain","trial_head_present","exposure_head_present","append_only_claim","content_addressed"])
def test_integrity_checks(outputs,field): assert outputs["integrity_report"]["checks"][field]
