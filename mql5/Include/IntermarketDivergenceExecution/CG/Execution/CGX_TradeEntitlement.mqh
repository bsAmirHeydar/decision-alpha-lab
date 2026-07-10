#ifndef __CGX_TRADE_ENTITLEMENT_MQH__
#define __CGX_TRADE_ENTITLEMENT_MQH__

#include <IntermarketDivergenceExecution/CG/Execution/CGX_Types.mqh>

string CGX_EntitlementSideText(const ECGCSignalSide side)
{
   if(side==CGC_SIDE_LOW) return "LOW";
   if(side==CGC_SIDE_HIGH) return "HIGH";
   return "NONE";
}

string CGX_BuildTradeEntitlementKey(const SCGCFinalSignal &signal)
{
   if(signal.group_name=="" || signal.group_minutes<=0 ||
      signal.trading_day_start_ny<=0 || signal.current_cycle_start_ny<=0 ||
      signal.reference_cycle_start_ny<=0 || signal.side==CGC_SIDE_NONE ||
      signal.hunter_symbol=="" || signal.clean_symbol=="")
      return "";

   string pair_left=signal.hunter_symbol;
   string pair_right=signal.clean_symbol;
   if(StringCompare(pair_left,pair_right)>0)
   {
      string swap=pair_left;
      pair_left=pair_right;
      pair_right=swap;
   }

   // Deliberately excludes confirmation_time_broker and every lower-timeframe candle field.
   // The entitlement belongs to divergence anatomy, not to each candle that redetects it.
   return StringFormat("EXP0017|CGX_ONCE_V1|PAIR:%s~%s|G:%s|TD:%d|C:%d|R:%d|S:%s",
                       pair_left,
                       pair_right,
                       signal.group_name,
                       signal.trading_day_start_ny,
                       signal.current_cycle_start_ny,
                       signal.reference_cycle_start_ny,
                       CGX_EntitlementSideText(signal.side));
}

#endif
