#property strict
// SAED_V4_15 static missing-view diagnostic only.
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_15/FusionAll.mqh>
int OnInit(){ if(SAEDV415SupportDirective(false,false,false)!=SAEDV415_ABSTAIN) return INIT_FAILED; if(SAEDV415FoundationDirective(0,true)!=SAEDV415_BASELINE) return INIT_FAILED; return INIT_SUCCEEDED; }
void OnTick(){}
