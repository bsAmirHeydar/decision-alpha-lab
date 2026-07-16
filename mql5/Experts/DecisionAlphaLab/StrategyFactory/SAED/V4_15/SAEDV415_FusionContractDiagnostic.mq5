#property strict
// SAED_V4_15 static diagnostic only; no trading calls.
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_15/FusionAll.mqh>
int OnInit(){ if(SAEDV415DecisionAuthority() || SAEDV415RuntimeAuthority() || SAEDV415ExecutionAuthority()) return INIT_FAILED; return INIT_SUCCEEDED; }
void OnTick(){}
