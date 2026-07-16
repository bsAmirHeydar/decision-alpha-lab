#property strict
#define SAED_V4_16_PHASE "SAED_V4_16"
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_16/SAEDV416Version.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_16/SAEDV416Types.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_16/SAEDV416AuthorityBoundary.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_16/SAEDV416SurvivalGuard.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_16/SAEDV416QuantileGuard.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_16/SAEDV416Conformance.mqh>
int OnInit(){return SAEDV416StaticConformance()?INIT_SUCCEEDED:INIT_FAILED;}
void OnTick(){}
