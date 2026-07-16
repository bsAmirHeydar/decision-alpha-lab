#property strict
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_14/SAEDV414Conformance.mqh>
int OnInit(){Print(SAED_V4_14_PHASE," static conformance=",SAEDV414StaticConformance());return SAEDV414StaticConformance()?INIT_SUCCEEDED:INIT_FAILED;}
void OnTick(){}
