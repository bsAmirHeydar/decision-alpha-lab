#property strict
#property version "1.00"
#property description "SAED V4-30 static replication contract harness; no trading authority"
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_30/FP_SAEDV430Constants.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_30/FP_SAEDV430Authority.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_30/FP_SAEDV430Protocol.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_30/FP_SAEDV430Package.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_30/FP_SAEDV430Lab.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_30/FP_SAEDV430Independence.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_30/FP_SAEDV430Environment.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_30/FP_SAEDV430Run.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_30/FP_SAEDV430Result.mqh>
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_30/FP_SAEDV430Certificate.mqh>

int OnInit()
{
   FP_SAEDV430Authority authority;
   authority.promotion=false; authority.runtime=false; authority.risk_allocation=false;
   authority.execution=false; authority.production=false; authority.online_learning=false;
   if(!FP_SAEDV430AuthorityIsZero(authority)) return(INIT_FAILED);
   Print(FP_SAEDV430_PHASE," static harness initialized; research only; no order operations");
   return(INIT_SUCCEEDED);
}
void OnTick() { }
