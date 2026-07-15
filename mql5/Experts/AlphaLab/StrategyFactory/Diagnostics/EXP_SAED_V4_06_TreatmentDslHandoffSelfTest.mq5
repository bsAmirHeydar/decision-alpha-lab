#property strict
#include <AlphaLab/StrategyFactory/SAEDV4TreatmentDsl/SAEDV4TreatmentDsl.mqh>

void OnStart()
  {
   const bool bounded=SAEDV4DslV407AuthorityBounded(true,true,false,false,false,false,false,false);
   if(!bounded) Print("SAED V4-06 to V4-07 handoff self-test failed");
  }
