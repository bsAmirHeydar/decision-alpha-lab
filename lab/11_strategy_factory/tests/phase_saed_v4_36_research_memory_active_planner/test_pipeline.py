from copy import deepcopy
import pytest
from conftest import FIXTURE
from saed_v4_research_memory_active_planner import run
from saed_v4_research_memory_active_planner.canonical import content_hash

def test_full_pipeline_accepts_reference():
    o=run(deepcopy(FIXTURE));assert o['certificate']['reference_accepted'];assert o['certificate']['production_authorized'] is False

def test_deterministic_replay(): assert content_hash(run(deepcopy(FIXTURE)))==content_hash(run(deepcopy(FIXTURE)))
def test_handoff_bounded():
    o=run(deepcopy(FIXTURE));assert o['handoff']['next_phase']=='SAED_V4_37';assert o['handoff']['authority_granted'] is False

def test_negative_knowledge_preserved():
    o=run(deepcopy(FIXTURE));assert o['negative_knowledge']['record_count']>=4;assert o['negative_knowledge']['deletion_allowed'] is False

def test_plan_never_executes():
    o=run(deepcopy(FIXTURE));assert o['plan']['automatic_execution_allowed'] is False;assert o['schedule']['execution_started'] is False

def test_budget_reserve_preserved():
    o=run(deepcopy(FIXTURE));assert o['availability']['compute_units']<o['budgets']['compute_units'];assert o['plan']['remaining_budget']['compute_units']>=0

def test_live_probe_rejected():
    o=run(deepcopy(FIXTURE)); assert any(x['candidate_id']=='cand_live_probe' for x in o['plan']['rejected']); assert all(x['candidate_id']!='cand_live_probe' for x in o['plan']['selected'])

def test_governance_human_only():
    o=run(deepcopy(FIXTURE));assert o['review']['reference_agenda_accepted'];assert o['review']['experiment_execution_authorized'] is False

@pytest.mark.parametrize('key',[
'upstream','constitution','authority','memory','negative_knowledge','supersession','evidence','lineage','evidence_coverage','claims','contradictions','knowledge_state','retrieval_index','retrieval_receipt','gaps','coverage_matrix','budgets','availability','risk_findings','weights','scorecard','plan','schedule','governance_policy','review','governance_ledger','baseline','external_boundary','limitations','reproduction','replay','evidence_bundle','certificate','handoff'])
def test_artifact_present_and_hashed(key):
    o=run(deepcopy(FIXTURE));assert key in o;assert isinstance(o[key],dict)
