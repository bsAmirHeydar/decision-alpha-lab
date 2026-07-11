#property strict
#include <AlphaLab/StrategyFactory/Testing/SF09_OutcomeFixtures.mqh>
input double InpEntry=1.1000;
input double InpStop=1.0980;
input double InpTarget=1.1040;
int OnInit()
{
   string error="";CSF09FixedCostModel cost;cost.Configure("sf09.cost.diagnostic","1.0.0",true,0,0,0,0,0,0);
   CSF09CostRegistry registry;if(!registry.Register(&cost,error)||!registry.Compile(error)){Print(error);return INIT_FAILED;}
   CSF09OutcomeEngine engine;SF09_SimulationPolicy policy=SF09_ConservativeSimulationPolicy();
   if(!engine.Configure(32,policy,&registry,"sf09.cost.diagnostic","1.0.0",error)){Print(error);return INIT_FAILED;}
   SF08_TradeCandidate c=SF09_FixtureCandidate("diag",SF08_ORDER_MARKET,InpEntry,InpStop,InpTarget,0.0);
   if(!engine.RegisterCandidate(c,SF09_FixtureTime(1000),error)){Print(error);return INIT_FAILED;}
   Print("SF09 diagnostic ready candidate=",c.candidate_id," policy=",policy.policy_hash," cost_registry=",registry.RegistryHash());
   return INIT_SUCCEEDED;
}
void OnTick(){}
