#property strict
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_28/SAEDV428Facade.mqh>
int OnInit(){ if(SAEDV428DecisionAuthority()) return INIT_FAILED; return INIT_SUCCEEDED; }
void OnTick(){}
