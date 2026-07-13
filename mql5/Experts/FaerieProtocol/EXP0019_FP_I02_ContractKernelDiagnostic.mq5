#property strict
#property version   "1.00"
#property description "EXP0019 FP-I02 read-only contract-kernel diagnostic"

#include <FaerieProtocol/EXP0019/Core/FP_I02_All.mqh>

input string InpPrimarySymbol="SPXUSD";
input string InpSecondarySymbol="NDXUSD";
input ENUM_TIMEFRAMES InpConfirmationTimeframe=PERIOD_CURRENT;
input int InpHistoricalNDepth=13;

int OnInit()
  {
   int tf_seconds=PeriodSeconds(InpConfirmationTimeframe==PERIOD_CURRENT ? (ENUM_TIMEFRAMES)_Period : InpConfirmationTimeframe);
   string pair_id=FP_I02_BuildPairId(InpPrimarySymbol,InpSecondarySymbol,"1.0.0");
   PrintFormat("FP-I02 Diagnostic context=%s version=%s pair=%s timeframe_seconds=%d n_depth=%d relation_count=%d reason_count=%d authority=NONE q12=OPEN",
               FP_I02_CONTEXT_ID,FP_I02_CONTEXT_VERSION,pair_id,tf_seconds,InpHistoricalNDepth,
               FP_I02_RelationCount(),FP_I02_ReasonCodeCount());
   return (pair_id!="" && tf_seconds>0 && InpHistoricalNDepth>0) ? INIT_SUCCEEDED : INIT_PARAMETERS_INCORRECT;
  }

void OnTick() {}
