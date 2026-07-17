#property strict
#property version "1.00"
#property description "SAED_V4_31 RESEARCH_ONLY formal-verification static harness"
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_31/FP_SAEDV431Constants.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_31/FP_SAEDV431Authority.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_31/FP_SAEDV431State.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_31/FP_SAEDV431Transition.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_31/FP_SAEDV431Invariant.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_31/FP_SAEDV431Temporal.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_31/FP_SAEDV431Expression.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_31/FP_SAEDV431ModelChecker.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_31/FP_SAEDV431ProofObligation.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_31/FP_SAEDV431ProofLedger.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_31/FP_SAEDV431Mutation.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_31/FP_SAEDV431Counterexample.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_31/FP_SAEDV431Hazard.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_31/FP_SAEDV431Mitigation.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_31/FP_SAEDV431SafetyConstraint.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_31/FP_SAEDV431ResidualRisk.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_31/FP_SAEDV431AssuranceCase.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_31/FP_SAEDV431Traceability.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_31/FP_SAEDV431Coverage.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_31/FP_SAEDV431Certificate.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_31/FP_SAEDV431Handoff.mqh>

int OnInit()
{
   if(!FP_SAEDV431Authority_IsResearchOnly()) return INIT_FAILED;
   if(FP_SAEDV431Authority_HasExecutionAuthority()) return INIT_FAILED;
   Print("SAED_V4_31 RESEARCH_ONLY static harness initialized; no execution authority.");
   return INIT_SUCCEEDED;
}
void OnTick() { /* RESEARCH_ONLY: deliberately no order placement. */ }
