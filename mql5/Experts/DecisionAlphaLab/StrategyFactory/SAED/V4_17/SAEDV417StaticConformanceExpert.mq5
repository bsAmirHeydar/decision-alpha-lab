#property strict
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_17/SAEDV417Version.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_17/SAEDV417Conformance.mqh>
int OnInit(){return SAEDV417StaticConformance()?INIT_SUCCEEDED:INIT_FAILED;}
void OnTick(){}
