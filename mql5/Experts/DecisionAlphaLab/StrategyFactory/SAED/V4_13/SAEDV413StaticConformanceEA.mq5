#property strict
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_13/SAEDV413Version.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_13/SAEDV413TemporalGuard.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_13/SAEDV413AuthorityBoundary.mqh>
int OnInit(){ SAEDV413Authority a=SAEDV413ReferenceAuthority(); if(a.decision_authority||a.runtime_authority||a.execution_authority) return INIT_FAILED; return INIT_SUCCEEDED; }
void OnTick(){}
