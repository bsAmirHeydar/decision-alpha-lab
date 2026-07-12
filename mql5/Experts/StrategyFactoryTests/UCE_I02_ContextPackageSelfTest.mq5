#property strict
#property version   "1.00"
#property description "UCEE I02 context package, lifecycle, view and cluster self-test."
#include <AlphaLab/StrategyFactory/ContextPackage/UCE02_All.mqh>
int g_passed=0;int g_failed=0;
void Check(const bool condition,const string name){if(condition){g_passed++;Print("PASS: ",name);}else{g_failed++;Print("FAIL: ",name);}}
UCE02_SyntheticBreakInput Fixture(const double close,const string id)
{
   UCE02_SyntheticBreakInput x;x.source_event_id=id;x.symbol="EURUSD";x.timeframe_seconds=60;x.signal_bar_open_ms=1710000000000;x.event_time_ms=1710000059999;x.known_time_ms=1710000060000;x.confirmation_time_ms=1710000060000;x.observation_cut_ms=1710000060000;x.decision_time_ms=1710000060001;x.prior_high=1.1000;x.prior_low=1.0980;x.close=close;x.atr=0.0010;x.spread_points=12.0;x.session="london";x.trading_day="2024-03-09";return x;
}
int OnInit()
{
   string error="";CUCE02SyntheticBreakPackage synthetic;CUCE02EXP0017ReferencePackage exp0017;UCE02_ConformanceTelemetry telemetry;UCE02_ResetConformanceTelemetry(telemetry);
   Check(UCE02_LintPackage(GetPointer(synthetic),telemetry,error),"synthetic package lint");
   Check(UCE02_LintPackage(GetPointer(exp0017),telemetry,error),"EXP0017 package lint");
   CUCE02StaticPackageRegistry registry;Check(registry.Register(GetPointer(synthetic),false,error),"register synthetic exact version");Check(registry.Register(GetPointer(exp0017),false,error),"register EXP0017 exact version");Check(registry.Count()==2,"registry count");Check(CheckPointer(registry.Resolve("ucee.reference.synthetic_break","1.0.0"))!=POINTER_INVALID,"exact package resolution");
   UCE02_ContextObservation first;bool emitted=false;UCE02_SyntheticBreakInput input=Fixture(1.1010,"evt.synthetic.001");Check(synthetic.Observe(input,first,emitted,error)&&emitted,"long break observation emitted");
   UCE02_ContextObservation replay;bool replay_emitted=false;Check(synthetic.Observe(input,replay,replay_emitted,error)&&replay_emitted,"replay observation emitted");Check(UCE02_ReplayHashEqual(first,replay,telemetry,error),"replay identity and hash parity");
   UCE02_ContextObservation none;bool none_emitted=true;Check(synthetic.Observe(Fixture(1.0990,"evt.synthetic.none"),none,none_emitted,error)&&!none_emitted,"inside range abstains");
   CUCE02LifecycleEngine lifecycle;Check(lifecycle.Configure(8,error),"lifecycle configured");bool is_new=false;Check(lifecycle.Register(first,is_new,error)&&is_new,"first observation registered");Check(lifecycle.Register(replay,is_new,error)&&!is_new&&lifecycle.DuplicatesSuppressed()==1,"duplicate observation suppressed");
   UCE02_ObservationTransition transition;Check(lifecycle.Transition(first.observation_id,UCE02_CONTEXT_ACTIVE,1710000060002,"manual_reference_activation",transition,error),"confirmed to active transition");Check(lifecycle.Transition(first.observation_id,UCE02_CONTEXT_EXPIRED,1710000120000,"horizon_elapsed",transition,error),"active to expired transition");Check(!lifecycle.Transition(first.observation_id,UCE02_CONTEXT_ACTIVE,1710000120001,"illegal_reactivation",transition,error),"terminal reactivation rejected");
   UCE02_ClusterRule rule;Check(synthetic.GetClusterRule(0,rule),"cluster rule available");UCE02_ClusterAssignment assignment;Check(UCE02_CompileCluster(rule,first,"{\"direction\":\"long\",\"signal_bar_open_ms\":1710000000000,\"symbol\":\"EURUSD\",\"timeframe_seconds\":60}",assignment,error),"opportunity cluster compiled");Check(assignment.cluster_id!="","cluster identity present");
   PrintFormat("UCE-I02 self-test passed=%d failed=%d",g_passed,g_failed);return g_failed==0?INIT_SUCCEEDED:INIT_FAILED;
}
void OnTick(){}
