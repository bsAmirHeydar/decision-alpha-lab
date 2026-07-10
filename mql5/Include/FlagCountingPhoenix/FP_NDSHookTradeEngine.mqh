#ifndef __FP_NDS_HOOK_TRADE_ENGINE_MQH__
#define __FP_NDS_HOOK_TRADE_ENGINE_MQH__
#property strict

#include "FP_NDSHookTradeExecutionCore.mqh"
#include "FP_NDSHookTradeExport.mqh"

void FP_RunNDSHookLimitF123Execution(const string symbol,
                                     const ENUM_TIMEFRAMES period,
                                     const FP_FlagEvent &events[],
                                     const int event_count,
                                     const FP_NDSHookTradeConfig &cfg,
                                     FP_NDSHookTradeReport &report)
{
   FP_RunNDSHookLimitF123ExecutionCore(symbol, period,
                                      events, event_count,
                                      cfg, report);
   FP_NDSHookTradeExportReport(cfg, report);
}

void FP_PrintNDSHookTradeReport(const string tag,
                                const FP_NDSHookTradeReport &report)
{
   Print(tag,
         " attempted=", FP_NDSHookTradeBool(report.attempted),
         " ok=", FP_NDSHookTradeBool(report.ok),
         " action=", report.action_label,
         " status=", report.status,
         " reason=", report.reason,
         " pending=", report.managed_pending_count,
         " positions=", report.managed_position_count,
         " seq=", report.setup.sequence_id,
         " family=", report.setup.family,
         " entry=", DoubleToString(report.setup.entry_price, _Digits),
         " stop=", DoubleToString(report.setup.stop_price, _Digits),
         " exit_f3=", report.exit_signal.event_id);
}

#endif // __FP_NDS_HOOK_TRADE_ENGINE_MQH__
