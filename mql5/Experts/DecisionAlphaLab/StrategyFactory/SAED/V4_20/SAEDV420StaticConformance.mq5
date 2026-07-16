#property strict
#define SAED_V4_20_PHASE "SAED_V4_20"
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_20/SAEDV420Authority.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_20/SAEDV420TreatmentUniverse.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_20/SAEDV420Abstention.mqh>
int OnInit(){ if(!SAEDV420ResearchOnly()) return INIT_FAILED; if(SAEDV420ExecutionAuthority()) return INIT_FAILED; if(!SAEDV420ClosedWorld()) return INIT_FAILED; return INIT_SUCCEEDED; }
void OnTick(){ }
