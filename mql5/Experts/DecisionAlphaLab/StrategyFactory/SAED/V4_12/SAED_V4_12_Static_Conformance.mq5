#property strict
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_12/SAED_V4_12_All.mqh>
int OnInit(){ SAEDV412State state; SAEDV412Reset(state); if(SAEDV412MaySendOrder()) return INIT_FAILED; return INIT_SUCCEEDED; }
void OnTick(){ /* SAED_V4_12 static conformance harness; no trading authority. */ }
