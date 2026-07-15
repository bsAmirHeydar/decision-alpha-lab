#property strict
#property script_show_inputs
#include <AlphaLab/StrategyFactory/SAEDV4TreatmentDsl/SAEDV4TreatmentDsl.mqh>

void OnStart()
  {
   SAEDV4DslAuthority authority=SAEDV4DslInstitutionalAuthority();
   if(!SAEDV4DslAuthorityIsBounded(authority)) Print("SAED V4-06 authority self-test failed");
   if(!SAEDV4DslBudgetValid(12,24,4,4,3)) Print("SAED V4-06 budget self-test failed");
   if(SAEDV4DslContainsProhibitedToken("context.breakout.p3")) Print("SAED V4-06 token self-test failed");
  }
