from copy import deepcopy
import pytest
from conftest import FIXTURE
from saed_v4_research_memory_active_planner import run
from saed_v4_research_memory_active_planner.errors import SAEDV436Error

def test_future_known_memory_rejected():
    x=deepcopy(FIXTURE);x['memory_entries'][0]['known_time']='2028-01-01T00:00:00Z'
    with pytest.raises(SAEDV436Error):run(x)
def test_unknown_constitution_field_rejected():
    x=deepcopy(FIXTURE);x['constitution']['unknown']=1
    with pytest.raises(SAEDV436Error):run(x)
def test_authority_escalation_rejected():
    x=deepcopy(FIXTURE);x['constitution']['automatic_experiment_execution_allowed']=True
    with pytest.raises(SAEDV436Error):run(x)
def test_semantic_duplicate_rejected():
    x=deepcopy(FIXTURE);y=deepcopy(x['memory_entries'][0]);y['memory_id']='duplicate';y['supersedes']='';x['memory_entries'].append(y)
    with pytest.raises(SAEDV436Error):run(x)
def test_unknown_supersession_rejected():
    x=deepcopy(FIXTURE);x['memory_entries'][0]['supersedes']='missing'
    with pytest.raises(SAEDV436Error):run(x)
def test_invalid_evidence_hash_rejected():
    x=deepcopy(FIXTURE);x['evidence_records'][0]['artifact_hash']='bad'
    with pytest.raises(SAEDV436Error):run(x)
def test_claim_runtime_actionability_rejected():
    x=deepcopy(FIXTURE);x['claims'][0]['actionability']='RUNTIME'
    with pytest.raises(SAEDV436Error):run(x)
def test_governance_auto_approval_rejected():
    x=deepcopy(FIXTURE);x['governance_policy']['automatic_approval_allowed']=True
    with pytest.raises(SAEDV436Error):run(x)
def test_wrong_upstream_phase_rejected():
    x=deepcopy(FIXTURE);x['upstream_documents'][0]['phase']='SAED_V4_34'
    with pytest.raises(SAEDV436Error):run(x)
def test_no_feasible_plan_fails_closed():
    x=deepcopy(FIXTURE);x['candidate_experiments']=[deepcopy(x['candidate_experiments'][5])];x['risk_findings']=[deepcopy(x['risk_findings'][5])]
    with pytest.raises(SAEDV436Error):run(x)
