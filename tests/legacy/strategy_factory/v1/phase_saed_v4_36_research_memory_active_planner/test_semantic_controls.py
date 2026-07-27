from copy import deepcopy
import pytest
from .conftest import FIXTURE
from saed_v4_research_memory_active_planner import run

def test_memory_chain_is_contiguous():
    c=run(deepcopy(FIXTURE))['memory']['chain'];assert c[0]['previous_hash']=='0'*64;assert all(c[i]['previous_hash']==c[i-1]['event_hash'] for i in range(1,len(c)))
def test_retrieval_includes_negative_knowledge():
    q=run(deepcopy(FIXTURE))['retrieval_receipt']['queries'][0];assert q['negative_recall_count']>=1
def test_blocking_contradiction_visible(): assert run(deepcopy(FIXTURE))['contradictions']['blocking_count']>=1
def test_runtime_claim_not_eligible():
    rows=run(deepcopy(FIXTURE))['knowledge_state']['claims'];r=next(x for x in rows if x['claim_id']=='claim_runtime_parity');assert r['eligible_for_runtime_use'] is False
def test_protected_floor_families_present():
    s=run(deepcopy(FIXTURE))['plan']['selected'];assert any(x['candidate_id']=='cand_neg_replay' for x in s);assert any(x['family']=='tail_stress_replication' for x in s)
def test_prerequisites_respected():
    s=run(deepcopy(FIXTURE))['schedule']['waves'];pos={cid:w['wave'] for w in s for cid in w['candidate_ids']};assert pos['cand_neg_replay']<pos['cand_regime_rep']
def test_baseline_unchanged():
    b=run(deepcopy(FIXTURE))['baseline'];assert b['live_runtime_unchanged'];assert b['orders_submitted']==0;assert b['automatic_experiments_started']==0
def test_no_network_retrieval(): assert run(deepcopy(FIXTURE))['retrieval_index']['network_access'] is False
def test_merkle_roots_present():
    o=run(deepcopy(FIXTURE));assert len(o['memory']['merkle_root'])==64;assert len(o['evidence_bundle']['merkle_root'])==64

@pytest.mark.parametrize('candidate_id',[x['candidate_id'] for x in FIXTURE['candidate_experiments']])
def test_every_candidate_accounted(candidate_id):
    p=run(deepcopy(FIXTURE))['plan'];ids={x['candidate_id'] for x in p['selected']}|{x['candidate_id'] for x in p['rejected']};assert candidate_id in ids
@pytest.mark.parametrize('memory_id',[x['memory_id'] for x in FIXTURE['memory_entries']])
def test_every_memory_covered(memory_id):
    rows=run(deepcopy(FIXTURE))['evidence_coverage']['rows'];assert any(x['memory_id']==memory_id and x['covered'] for x in rows)
@pytest.mark.parametrize('claim_id',[x['claim_id'] for x in FIXTURE['claims']])
def test_every_claim_in_knowledge_state(claim_id): assert any(x['claim_id']==claim_id for x in run(deepcopy(FIXTURE))['knowledge_state']['claims'])
