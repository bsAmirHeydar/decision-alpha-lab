import copy, pytest
from saed_v4_complete_search_exposure_ledger import run
from saed_v4_complete_search_exposure_ledger.chain import verify_chain
from saed_v4_complete_search_exposure_ledger.errors import IntegrityError, StateTransitionError

def test_trial_complete(outputs): assert outputs["trial_ledger"]["complete"]
def test_trial_count(outputs): assert outputs["trial_ledger"]["observed_trial_count"]==36
def test_trial_chain(outputs): assert verify_chain(outputs["trial_ledger"]["entries"],"trial_ledger")["verified"]
@pytest.mark.parametrize("state",["selected","rejected","pruned","failed","timed_out","duplicate"])
def test_terminal_state_present(outputs,state): assert outputs["trial_ledger"]["terminal_state_counts"][state]>0
def test_retry_accounted(outputs): assert outputs["trial_ledger"]["retry_edges"]
def test_duplicate_accounted(outputs): assert outputs["trial_ledger"]["duplicate_edges"]
def test_orphan_rejected(config,upstream,manifests,trials,exposures):
    bad=copy.deepcopy(trials); bad[0]["trial_id"]="orphan"
    with pytest.raises(IntegrityError): run(config,upstream,manifests,bad,exposures)
def test_invalid_transition_rejected(config,upstream,manifests,trials,exposures):
    bad=copy.deepcopy(trials); bad[1]["state"]="selected"
    with pytest.raises(StateTransitionError): run(config,upstream,manifests,bad,exposures)
def test_trial_tamper_detected(outputs):
    bad=copy.deepcopy(outputs["trial_ledger"]["entries"]); bad[0]["reason"]="tampered"
    with pytest.raises(IntegrityError): verify_chain(bad,"trial_ledger")
def test_trial_reordering_detected(outputs):
    bad=copy.deepcopy(outputs["trial_ledger"]["entries"]); bad[0],bad[1]=bad[1],bad[0]
    with pytest.raises(IntegrityError): verify_chain(bad,"trial_ledger")
def test_trial_actor_mismatch_rejected(config,upstream,manifests,trials,exposures):
    bad=copy.deepcopy(trials); bad[0]["actor_id"]="unknown"
    with pytest.raises(IntegrityError): run(config,upstream,manifests,bad,exposures)
def test_trial_known_time_rejected(config,upstream,manifests,trials,exposures):
    bad=copy.deepcopy(trials); bad[0]["known_at"]="2026-07-17T00:00:00Z"
    with pytest.raises(IntegrityError): run(config,upstream,manifests,bad,exposures)
