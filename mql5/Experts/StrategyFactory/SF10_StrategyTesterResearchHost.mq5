#property strict
#property version "1.00"
#include <AlphaLab/StrategyFactory/Research/SF10_AllResearch.mqh>

input long InpPassPublicId=1;
input int InpMinimumUniqueEvents=30;
input int InpMinimumFilledOutcomes=20;
input double InpMinimumFillRate=0.10;
input double InpMinimumExpectancyR=0.0;
input int InpTopPasses=20;
input bool InpEmitOptimizationFrame=true;
input string InpRunId="sf10_research_run";
input string InpParameterHash="params_default";

CSF10ResearchHarness g_harness;
CSF10SelectedPassCollector g_collector;
bool g_ready=false;

SF10_RunManifest BuildManifest()
{
   SF10_RunManifest m;ZeroMemory(m);m.schema="alpha_lab.strategy_factory/research_run_manifest@1.0.0";
   m.run_id=InpRunId;m.research_program_id="sf10_tester_research";m.strategy_id="central_engine_fixture";m.strategy_version="1.0.0";
   m.runtime_generation_id=0;m.runtime_generation_hash="gen_fixture";m.plugin_set_hash="plugins_fixture";m.candidate_matrix_hash="matrix_fixture";
   m.simulation_policy_hash="simulation_fixture";m.cost_registry_hash="cost_fixture";m.input_parameter_hash=InpParameterHash;
   m.data_source_id="meta_strategy_tester";m.symbol=_Symbol;m.timeframe_seconds=PeriodSeconds(_Period);m.test_start_utc_msc=1;m.test_end_utc_msc=2;
   m.fidelity_preset=SF10_FIDELITY_FAST_SCREEN;m.objective_mode=SF10_OBJECTIVE_CONSERVATIVE;m.export_detail=SF10_EXPORT_PASS_SUMMARY;
   m.random_seed=0;m.git_commit="unknown";m.terminal_build=IntegerToString((int)TerminalInfoInteger(TERMINAL_BUILD));m.source_hash="sf10_host";m.manifest_hash="";return m;
}
SF10_ObjectiveConfig BuildObjective()
{
   SF10_ObjectiveConfig c;ZeroMemory(c);c.schema="alpha_lab.strategy_factory/objective_config@1.0.0";c.mode=SF10_OBJECTIVE_CONSERVATIVE;
   c.minimum_unique_events=InpMinimumUniqueEvents;c.minimum_filled_outcomes=InpMinimumFilledOutcomes;c.minimum_fill_rate=InpMinimumFillRate;
   c.minimum_expectancy_r=InpMinimumExpectancyR;c.drawdown_penalty_weight=1.0;c.dispersion_penalty_weight=0.25;
   c.tail_dependency_penalty_weight=1.0;c.minimum_fold_survival=0.0;c.minimum_cost_survival=0.0;c.minimum_stability=0.0;return c;
}
int OnInit(){string error="";g_ready=g_harness.Initialize(BuildManifest(),BuildObjective(),8192,error);if(!g_ready){Print(error);return INIT_FAILED;}return INIT_SUCCEEDED;}
void OnTick(){/* Phase 10 central harness. Phase 11+ or an adapter registers canonical outcomes. */}
double OnTester(){string error="";SF10_PassSummary s=g_harness.Finalize(InpPassPublicId,InpParameterHash,InpEmitOptimizationFrame,error);if(error!=""&&s.status==SF10_PASS_VALID)Print(error);return s.objective_score;}
void OnTesterInit(){SF10_SelectedPassPolicy p;p.maximum_passes=InpTopPasses;p.minimum_score=-1.0e99;p.minimum_expectancy_r=InpMinimumExpectancyR;p.minimum_unique_events=InpMinimumUniqueEvents;g_collector.Configure(p);}
void DrainFrames()
{
   ulong pass=0;string name="";long id=0;double value=0.0;double data[];string error="";
   while(SF10_ReadNextOptimizationFrame(pass,name,id,value,data,error))
   {
      SF10_PassSummary s;string parse_error="";
      if(SF10_PassSummaryFromFrame(InpRunId,"unknown_manifest","unknown_parameters",id,value,data,s,parse_error))g_collector.Consider(s);
   }
}
void OnTesterPass(){DrainFrames();}
void OnTesterDeinit(){DrainFrames();string error="";if(!g_collector.ExportCsv("SF10_selected_passes.csv",error)&&error!="")Print(error);}
