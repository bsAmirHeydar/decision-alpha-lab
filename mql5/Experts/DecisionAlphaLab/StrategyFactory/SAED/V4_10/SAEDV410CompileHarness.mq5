#property strict
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_10/SAEDV410Version.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_10/SAEDV410Types.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_10/SAEDV410Authority.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_10/SAEDV410Canonical.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_10/SAEDV410Program.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_10/SAEDV410Interpreter.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_10/SAEDV410Baseline.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_10/SAEDV410Conformance.mqh>
int OnInit(){return SAEDV410AuthorityConforms()?INIT_SUCCEEDED:INIT_FAILED;}
void OnTick(){}
