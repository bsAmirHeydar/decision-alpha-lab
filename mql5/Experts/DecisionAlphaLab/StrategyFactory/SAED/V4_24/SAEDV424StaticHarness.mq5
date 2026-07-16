#property strict
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_24/SAEDV424Facade.mqh>
int OnInit(){ if(!SAEDV424AuthorityIsZero()) return INIT_FAILED; return INIT_SUCCEEDED; }
void OnTick(){ /* Static research mirror only. No order authority. */ }
