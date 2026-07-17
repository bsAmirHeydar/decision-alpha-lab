#property strict
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_29/SAEDV429Facade.mqh>
int OnInit(){
   if(SAEDV429NetworkAccess()) return INIT_FAILED;
   if(SAEDV429PromotionAuthority()) return INIT_FAILED;
   if(SAEDV429ExecutionAuthority()) return INIT_FAILED;
   return INIT_SUCCEEDED;
}
void OnTick(){}
