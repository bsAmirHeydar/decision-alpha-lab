#property strict
#include <AlphaLab/StrategyFactory/Testing/SF09_OutcomeFixtures.mqh>

int g_failures=0;
void Check(const bool ok,const string message){if(!ok){Print("FAIL: ",message);g_failures++;}else Print("PASS: ",message);}

int OnInit()
{
   string error="";
   CSF09FixedCostModel cost;cost.Configure("sf09.cost.fixture","1.0.0",false,0.0,0.0,0.0,0.0,0.05,0.0);
   CSF09CostRegistry registry;Check(registry.Register(&cost,error),"register cost model");Check(registry.Compile(error),"compile cost registry");
   SF09_SimulationPolicy policy=SF09_ConservativeSimulationPolicy();
   CSF09OutcomeEngine engine;Check(engine.Configure(16,policy,&registry,"sf09.cost.fixture","1.0.0",error),"configure outcome engine");
   SF08_TradeCandidate c=SF09_FixtureCandidate("c1",SF08_ORDER_MARKET,1.1000,1.0980,1.1040,0.0);
   Check(engine.RegisterCandidate(c,SF09_FixtureTime(1000),error),"register candidate");
   SF09_PriceObservation fill=SF09_FixtureBar(1,2000,1.1000,1.1010,1.0995,1.1005);Check(engine.ProcessObservation(fill,error),"process fill bar");
   SF09_PriceObservation target=SF09_FixtureBar(2,3000,1.1005,1.1045,1.1000,1.1040);Check(engine.ProcessObservation(target,error),"process target bar");
   SF09_OutcomeRecord out;Check(engine.PopOutcome(out),"pop outcome");Check(out.filled,"outcome filled");Check(out.exit_reason==SF09_EXIT_TARGET,"target exit");
   Check(out.gross_r>1.9&&out.gross_r<2.1,"gross R near 2");Check(out.net_r<out.gross_r,"cost reduces net R");Check(out.mfe_r>=2.0,"MFE tracked");
   Check(SF09_ValidateOutcomeRecord(out,error),"outcome validates");

   CSF09OutcomeEngine amb;policy.ambiguity_policy=SF09_AMBIGUITY_STOP_FIRST;policy.policy_hash=SF09_DeriveSimulationPolicyHash(policy);
   Check(amb.Configure(16,policy,&registry,"sf09.cost.fixture","1.0.0",error),"configure ambiguity engine");
   SF08_TradeCandidate a=SF09_FixtureCandidate("c2",SF08_ORDER_MARKET,1.1000,1.0980,1.1040,0.0);Check(amb.RegisterCandidate(a,SF09_FixtureTime(1000),error),"register ambiguous candidate");
   Check(amb.ProcessObservation(SF09_FixtureBar(1,2000,1.1000,1.1045,1.0975,1.1000),error),"process ambiguous bar");
   SF09_OutcomeRecord ao;Check(amb.PopOutcome(ao),"pop ambiguous outcome");Check(ao.exit_reason==SF09_EXIT_STOP,"stop-first ambiguity");Check(ao.ambiguous,"ambiguity flag");

   Check(engine.Telemetry().terminal_outcomes==1,"telemetry terminal count");
   Print("SF09 self-test failures=",g_failures);
   return (g_failures==0)?INIT_SUCCEEDED:INIT_FAILED;
}
void OnTick(){}
