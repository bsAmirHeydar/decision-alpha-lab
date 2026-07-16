#property strict
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_21/SAEDV421Types.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_21/SAEDV421Authority.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_21/SAEDV421Optimizer.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_21/SAEDV421Fallback.mqh>
int OnInit(){if(SAEDV421HasDecisionAuthority())return INIT_FAILED;if(SAEDV421HasExecutionAuthority())return INIT_FAILED;if(SAEDV421FailClosedAllocation()!="allocation::SKIP:1.000000")return INIT_FAILED;return INIT_SUCCEEDED;}
void OnTick(){}
