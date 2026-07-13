import pytest
from strategy_factory_tournament_v3.golden import golden_run
from strategy_factory_tournament_v3.tournament import run_reference_tournament,declared_trial_count
from strategy_factory_tournament_v3.confirmatory import confirmatory_findings,bounded_challengers
from strategy_factory_tournament_v3.enums import TrialStatus
BASE=golden_run()
def test_declared_cartesian_universe():
 _,ctx,_,t,a,f,*_=BASE;assert declared_trial_count(tuple(x.context_id for x in ctx),t.treatments,a.algorithms,f.folds)==486
def test_repeat_is_deterministic():
 _,ctx,_,t,a,f,*_=BASE;r1=run_reference_tournament(f,tuple(x.context_id for x in ctx),t,a);r2=run_reference_tournament(f,tuple(x.context_id for x in ctx),t,a);assert r1.report_hash==r2.report_hash
@pytest.mark.parametrize('position',[0,1,50,100,200,400])
def test_injected_failure_retained(position):
 _,ctx,_,t,a,f,*_=BASE;r0=run_reference_tournament(f,tuple(x.context_id for x in ctx),t,a);trial=r0.trial_results[position].trial_id;r=run_reference_tournament(f,tuple(x.context_id for x in ctx),t,a,fail_trial_ids={trial});assert any(x.trial_id==trial and x.status is TrialStatus.FAILED for x in r.trial_results);assert r.failed_trial_count==1
@pytest.mark.parametrize('limit',[0,1,2,3,10])
def test_bounded_challengers(limit):
 report=BASE[6];assert len(bounded_challengers(report,limit))<=limit

def test_reference_report_is_not_confirmatory_evidence():
 assert 'reference_fixture_not_confirmatory_real_data' in confirmatory_findings(BASE[6])
