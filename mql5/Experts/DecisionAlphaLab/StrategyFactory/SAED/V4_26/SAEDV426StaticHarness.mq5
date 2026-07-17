#property strict
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_26/SAEDV426Facade.mqh>
int OnInit(){ return SAEDV426AuthorityIsZero()?INIT_SUCCEEDED:INIT_FAILED; }
void OnTick(){ /* Research-only static harness. No execution surface. */ }
