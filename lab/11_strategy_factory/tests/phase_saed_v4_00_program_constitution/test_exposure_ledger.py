from saed_v4_constitution.enums import DecisionStatus
from saed_v4_constitution.exposure import ExposureBudget,ExposureLedger
from saed_v4_constitution.models import ExposureEvent

def e(i,kind='trial'):
 return ExposureEvent('p',f'a{i}',kind,'family',f'2026-07-13T00:{i:02d}:00Z',str(i%10)*64,str((i+1)%10)*64)

def test_deduplicates_same_event():
 l=ExposureLedger(); l.append(e(1)); l.append(e(1)); assert len(l.events())==1

def test_deterministic_digest_order():
 assert ExposureLedger([e(2),e(1)]).digest()==ExposureLedger([e(1),e(2)]).digest()

def test_budget_allows_within_limit(): assert ExposureLedger([e(1)]).evaluate(ExposureBudget('family',2,1)).status==DecisionStatus.ALLOW

def test_total_budget_rejects(): assert ExposureLedger([e(1),e(2)]).evaluate(ExposureBudget('family',1,1)).status==DecisionStatus.REJECT

def test_hidden_budget_rejects():
 l=ExposureLedger([e(1,'hidden_evaluation_submission'),e(2,'hidden_evaluation_submission')])
 assert l.evaluate(ExposureBudget('family',10,1)).status==DecisionStatus.REJECT
