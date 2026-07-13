import pytest
from dataclasses import replace
from strategy_factory_tournament_v3.golden import golden_run
from strategy_factory_tournament_v3.contracts import PaperObservation
from strategy_factory_tournament_v3.prospective import build_paper_report,reconcile_observation
from strategy_factory_tournament_v3.decision import decide_champion
from strategy_factory_tournament_v3.enums import DataMode,DecisionStatus,ReconciliationStatus
from strategy_factory_tournament_v3.errors import TournamentError
BASE=golden_run();PLAN=BASE[7]
def obs(i,delta=0.0):return PaperObservation(f'obs{i}','%064x'%(i+1),f'occ{i}',14000+i,100.0,100.0+delta,0.1,0.1+delta,'filled','normal')
@pytest.mark.parametrize('delta,status',[(0.0,ReconciliationStatus.MATCH),(0.01,ReconciliationStatus.MATCH),(0.1,ReconciliationStatus.MISMATCH)])
def test_reconciliation(delta,status):assert reconcile_observation(PLAN,obs(1,delta))[0] is status

def test_complete_real_paper_can_promote_with_bundle():
 observations=tuple(obs(i) for i in range(20));paper=build_paper_report(PLAN,observations,DataMode.PROSPECTIVE_PAPER,True,True);t=replace(BASE[6],reference_only=False,critical_findings=());d=decide_champion(t,paper,'a'*64);assert d.status is DecisionStatus.PROMOTE

def test_complete_real_paper_without_bundle_pending():
 observations=tuple(obs(i) for i in range(20));paper=build_paper_report(PLAN,observations,DataMode.PROSPECTIVE_PAPER,True,True);t=replace(BASE[6],reference_only=False,critical_findings=());d=decide_champion(t,paper,None);assert d.status is DecisionStatus.PENDING
@pytest.mark.parametrize('mode,completed',[(DataMode.FIXTURE,False),(DataMode.HISTORICAL_REAL,False),(DataMode.FIXTURE,True)])
def test_non_prospective_cannot_complete(mode,completed):
 observations=tuple(obs(i) for i in range(20))
 if completed:
  with pytest.raises(TournamentError):build_paper_report(PLAN,observations,mode,True,True)
 else:assert build_paper_report(PLAN,observations,mode,False,True).critical_findings

def test_duplicate_decision_hash_detected():
 o=obs(1);p=build_paper_report(PLAN,(o,o),DataMode.PROSPECTIVE_PAPER,False,True);assert 'duplicate_decision_hash' in p.critical_findings

def test_touched_paper_refused():
 with pytest.raises(TournamentError):build_paper_report(PLAN,(),DataMode.FIXTURE,False,False)
