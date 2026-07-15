#property strict
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_11/SAEDV411StaticMirror.mqh>
int OnInit()
{
   SAEDV411AuthorityBoundary authority=SAEDV411ReferenceAuthority();
   if(authority.predict_outcomes || authority.rank_treatments || authority.select_treatment || authority.allocate_risk || authority.activate_runtime || authority.send_order) return INIT_FAILED;
   if(StringCompare(SAED_V4_11_PHASE,"SAED_V4_11")!=0) return INIT_FAILED;
   if(StringCompare(SAED_V4_11_NEXT_PHASE,"SAED_V4_12")!=0) return INIT_FAILED;
   return INIT_SUCCEEDED;
}
void OnTick() {}
