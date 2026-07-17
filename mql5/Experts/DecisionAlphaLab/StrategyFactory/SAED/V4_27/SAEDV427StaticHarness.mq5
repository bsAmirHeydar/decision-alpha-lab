#property strict
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_27/SAEDV427Facade.mqh>
int OnInit(){ if(!SAEDV427ResearchOnly()) return INIT_FAILED; if(SAEDV427CanExecute()) return INIT_FAILED; return INIT_SUCCEEDED; }
void OnTick(){}
