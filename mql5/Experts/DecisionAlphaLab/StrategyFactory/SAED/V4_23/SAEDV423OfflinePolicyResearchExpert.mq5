#property strict
#property version "1.00"
// SAED_V4_23 reference shell. Deliberately non-executable.
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_23/SAEDV423Version.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_23/SAEDV423Authority.mqh>
int OnInit(){ if(SAEDV423RuntimeAllowed()) return INIT_FAILED; return INIT_SUCCEEDED; }
void OnTick(){ /* research-only: no trade action */ }
