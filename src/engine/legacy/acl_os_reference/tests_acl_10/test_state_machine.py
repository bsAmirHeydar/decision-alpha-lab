from tools.strategy_factory.acl_os.acl_10.handoff_input import load_acl09_bundle
from tools.strategy_factory.acl_os.acl_10.subject_projection import project_subjects
from tools.strategy_factory.acl_os.acl_10.prerequisite_evaluator import build_matrix
from tools.strategy_factory.acl_os.acl_10.decision_engine import build_decisions

def _all(acl09_root,policy):
    b=load_acl09_bundle(acl09_root); s=project_subjects(b); m=build_matrix(s,b,policy); return b,s,m,build_decisions(s,m,policy,'2026-07-18T03:00:00Z')
def test_subject_count(acl09_root,policy): assert _all(acl09_root,policy)[1]['subject_count']==12
def test_zero_eligible(acl09_root,policy): assert _all(acl09_root,policy)[2]['eligible_count']==0
def test_state_distribution(acl09_root,policy):
    bundle=_all(acl09_root,policy)[3][0]; assert bundle['state_counts']=={'BASELINE_REFERENCE_ONLY':4,'DIAGNOSTIC_QUARANTINED':1,'RESEARCH_HOLD':7}
def test_no_promotion_execution(acl09_root,policy):
    bundle=_all(acl09_root,policy)[3][0]; assert bundle['promotion_review_eligible_count']==0 and bundle['promotion_executed_count']==0
def test_diagnostic_quarantined(acl09_root,policy):
    decisions=_all(acl09_root,policy)[3][2]; assert sum(d['current_state']=='DIAGNOSTIC_QUARANTINED' for d in decisions)==1
def test_baselines_reference_only(acl09_root,policy):
    decisions=_all(acl09_root,policy)[3][2]; assert sum(d['current_state']=='BASELINE_REFERENCE_ONLY' for d in decisions)==4
def test_unknowns_preserved(acl09_root,policy):
    matrix=_all(acl09_root,policy)[2]; assert sum(r['status']=='UNKNOWN' for e in matrix['evaluations'] for r in e['results'])==28
def test_transition_attempts_denied_or_na(acl09_root,policy):
    attempts=_all(acl09_root,policy)[3][3]; assert all(a['status'] in {'DENIED','NOT_APPLICABLE'} for a in attempts)
