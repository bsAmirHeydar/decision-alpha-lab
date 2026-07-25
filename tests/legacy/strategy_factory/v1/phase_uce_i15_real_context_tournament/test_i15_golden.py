from strategy_factory_tournament_v3.golden import golden_run
from strategy_factory_tournament_v3.enums import DecisionStatus,DataMode

def test_golden_reference_run_is_explicit_rejection():
 inv,contexts,occ,t,a,freeze,report,plan,paper,decision=golden_run()
 assert inv.mode is DataMode.FIXTURE
 assert report.declared_trial_count==486
 assert report.succeeded_trial_count==486
 assert decision.status is DecisionStatus.REJECT
 assert 'tournament_not_reference_only' in decision.reasons
 assert 'paper_mode_prospective' in decision.reasons

def test_golden_hashes_repeat():
 a=golden_run();b=golden_run()
 assert a[0].inventory_hash==b[0].inventory_hash
 assert a[5].freeze_hash==b[5].freeze_hash
 assert a[6].report_hash==b[6].report_hash
 assert a[-1].decision_hash==b[-1].decision_hash
