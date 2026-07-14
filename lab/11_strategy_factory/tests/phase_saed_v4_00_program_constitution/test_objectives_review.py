from saed_v4_constitution.enums import DecisionStatus,EvidenceRole
from saed_v4_constitution.models import ObjectiveDefinition,ReviewApproval
from saed_v4_constitution.objectives import MANDATORY_BASELINES,detect_objective_change,validate_baselines
from saed_v4_constitution.review import evaluate_two_person_integrity

def obj(version='1',extra=()):
 return ObjectiveDefinition('o',version,('utility',)+tuple(extra),('known_time',),tuple(sorted(MANDATORY_BASELINES)),(EvidenceRole.DEVELOPMENT,),"2026-07-13T00:00:00Z")

def approval(i,unit='validation'):
 return ReviewApproval(i,unit,'reviewer','2026-07-13T00:00:00Z','approve','ok',str(i[-1] if i[-1].isdigit() else 1)*64)

def test_mandatory_baselines_complete(): assert validate_baselines(MANDATORY_BASELINES).status == DecisionStatus.ALLOW

def test_missing_baseline_rejected(): assert validate_baselines({'skip_all'}).status == DecisionStatus.REJECT

def test_same_objective_allowed(): assert detect_objective_change(obj(),obj()).status == DecisionStatus.ALLOW

def test_changed_objective_requires_amendment(): assert detect_objective_change(obj(),obj(extra=('tail',))).status == DecisionStatus.REQUIRE_REVIEW

def test_two_independent_approvals(researcher):
 assert evaluate_two_person_integrity(researcher,[approval('reviewer-1'),approval('reviewer-2','risk')]).status == DecisionStatus.ALLOW

def test_one_approval_insufficient(researcher): assert evaluate_two_person_integrity(researcher,[approval('reviewer-1')]).status == DecisionStatus.REQUIRE_REVIEW

def test_self_approval_rejected(researcher): assert evaluate_two_person_integrity(researcher,[approval(researcher.actor_id)]).status == DecisionStatus.REJECT

def test_same_unit_rejected(researcher): assert evaluate_two_person_integrity(researcher,[approval('reviewer-1','research'),approval('reviewer-2','risk')]).status == DecisionStatus.REJECT
