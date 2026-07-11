#property strict
#property version "1.00"
#include <AlphaLab/StrategyFactory/Research/SF10_AllResearch.mqh>

int g_failures=0;
void Check(const bool condition,const string message){if(!condition){Print("FAIL: ",message);g_failures++;}}

SF09_OutcomeRecord FixtureOutcome(const string suffix,const double net_r,const bool filled)
{
   SF09_OutcomeRecord o;ZeroMemory(o);o.schema="alpha_lab.strategy_factory/outcome_record@1.0.0";
   o.candidate_id="cand_"+suffix;o.event_id="evt_"+suffix;o.strategy_id="sf10_fixture";o.symbol="EURUSD";o.direction=SF01_DIRECTION_LONG;
   o.terminal_state=filled?SF09_STATE_CLOSED:SF09_STATE_EXPIRED;o.exit_reason=filled?(net_r>=0.0?SF09_EXIT_TARGET:SF09_EXIT_STOP):SF09_EXIT_ENTRY_EXPIRED;
   o.fidelity=SF09_FIDELITY_TICK;o.filled=filled;o.ambiguous=false;o.partial_exit_used=false;
   o.registered_at.utc_epoch_milliseconds=1000;o.registered_at.source_timezone_id="UTC";o.registered_at.source_utc_offset_minutes=0;o.registered_at.source_clock_id="fixture";o.registered_at.precision=SF01_TIME_MILLISECONDS;
   o.fill_time=o.registered_at;o.fill_time.utc_epoch_milliseconds=2000;o.fill_price=100.0;o.exit_time=o.fill_time;o.exit_time.utc_epoch_milliseconds=3000;o.exit_price=100.0+net_r;
   o.remaining_fraction=0.0;o.gross_points=net_r;o.gross_r=net_r;o.net_r=net_r;o.mfe_points=MathMax(0.0,net_r);o.mae_points=MathMax(0.0,-net_r);o.mfe_r=o.mfe_points;o.mae_r=o.mae_points;
   o.holding_milliseconds=1000;o.time_to_fill_milliseconds=1000;o.costs.model_id="fixture";o.costs.model_version="1";o.costs.total_cost_r=0.0;o.costs.cost_hash=SF09_DeriveCostHash(o.costs);
   o.simulation_policy_hash="sim_1";o.cost_registry_hash="cost_1";o.path_hash="path_1";o.source_hash="src_1";o.outcome_id=SF09_DeriveOutcomeId(o);return o;
}

int OnInit()
{
   CSF10ResearchAccumulator acc;acc.Reset(32);string error="";
   Check(acc.Observe(FixtureOutcome("1",1.5,true),"cluster_1",error),"observe win");
   Check(acc.Observe(FixtureOutcome("2",-1.0,true),"cluster_2",error),"observe loss");
   Check(acc.Observe(FixtureOutcome("3",0.0,false),"cluster_3",error),"observe no-fill");
   SF10_ResearchMetrics m=acc.Snapshot();Check(m.outcome_count==3,"outcome count");Check(m.filled_count==2,"filled count");
   Check(MathAbs(m.expectancy_r-0.25)<0.000001,"expectancy");Check(MathAbs(m.fill_rate-(2.0/3.0))<0.000001,"fill rate");
   SF10_ObjectiveConfig c;ZeroMemory(c);c.schema="alpha_lab.strategy_factory/objective_config@1.0.0";c.mode=SF10_OBJECTIVE_CONSERVATIVE;
   c.minimum_unique_events=2;c.minimum_filled_outcomes=2;c.minimum_fill_rate=0.5;c.minimum_expectancy_r=0.0;c.drawdown_penalty_weight=1.0;
   c.dispersion_penalty_weight=0.1;c.tail_dependency_penalty_weight=1.0;c.minimum_fold_survival=0.5;c.minimum_cost_survival=0.5;c.minimum_stability=0.5;
   SF10_ObjectiveResult r=SF10_EvaluateObjective(m,c);Check(r.status==SF10_PASS_VALID,"objective accepted");Check(r.score>0.0,"objective positive");
   SF10_PassSummary s;ZeroMemory(s);s.schema="alpha_lab.strategy_factory/optimization_pass_summary@1.0.0";s.public_id=42;s.run_id="run_1";s.manifest_hash="rman_1";s.parameter_hash="param_1";s.objective_score=r.score;s.status=r.status;s.metrics=m;s.summary_hash=SF10_DerivePassSummaryHash(s);
   double data[];SF10_PassSummaryToFrame(s,data);Check(ArraySize(data)==SF10_FRAME_DATA_SIZE,"frame size");
   SF10_DifferentialTolerance t;t.net_r_absolute=0.01;t.fill_rate_absolute=0.01;t.drawdown_absolute=0.01;t.count_absolute=0;
   SF10_DifferentialResult d=SF10_CompareResearchMetrics(m,m,t);Check(d.status==SF10_DIFF_MATCH,"differential exact");
   if(g_failures>0){Print("SF10 self-test failed: ",g_failures);return INIT_FAILED;}
   Print("SF10 research harness self-test PASS");return INIT_SUCCEEDED;
}
void OnTick(){}
