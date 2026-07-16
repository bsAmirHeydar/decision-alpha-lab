#ifndef __FP_NDS_HOOK_TRADE_ENGINE_MQH__
#define __FP_NDS_HOOK_TRADE_ENGINE_MQH__
#property strict

#include "FP_NDSHookTradeExecutionCore.mqh"
#include "FP_NDSHookTradeExport.mqh"

void FP_RunNDSHookTradeExecution(const string symbol,
                                 const ENUM_TIMEFRAMES period,
                                 const FP_FlagEvent &events[],
                                 const int event_count,
                                 const FP_NDSHookTradeConfig &cfg,
                                 FP_NDSHookTradeReport &report)
{
   FP_RunNDSHookTradeExecutionCore(symbol, period,
                                      events, event_count,
                                      cfg, report);
   FP_NDSHookTradeExportReport(cfg, report);
}

// Backward-compatible Phase 52 public API. Existing callers retain terminal/F123
// behavior because that profile remains the reset/default profile.
void FP_RunNDSHookLimitF123Execution(const string symbol,
                                     const ENUM_TIMEFRAMES period,
                                     const FP_FlagEvent &events[],
                                     const int event_count,
                                     const FP_NDSHookTradeConfig &cfg,
                                     FP_NDSHookTradeReport &report)
{
   FP_RunNDSHookTradeExecution(symbol, period, events, event_count, cfg, report);
}

void FP_PrintNDSHookTradeReport(const string tag,
                                const FP_NDSHookTradeReport &report)
{
   string message = tag;
   message += " attempted=" + FP_NDSHookTradeBool(report.attempted);
   message += " ok=" + FP_NDSHookTradeBool(report.ok);
   message += " action=" + report.action_label;
   message += " status=" + report.status;
   message += " reason=" + report.reason;
   message += " pending=" + IntegerToString(report.managed_pending_count);
   message += " positions=" + IntegerToString(report.managed_position_count);
   message += " profile=" + report.setup.profile_label;
   message += " seq=" + IntegerToString(report.setup.sequence_id);
   message += " family=" + report.setup.family;
   message += " x_count=" + IntegerToString(report.setup.x_count);
   message += " p04_closed=" + FP_NDSHookTradeBool(report.setup.phase04_x_closed);
   message += " first_864_touch=" + FP_NDSHookTradeBool(report.setup.first_864_touch_found);
   message += " funnel={" + FP_NDSHook864CycleR1FunnelSummary(report.funnel) + "}";
   message += " entry=" + DoubleToString(report.setup.entry_price, _Digits);
   message += " stop=" + DoubleToString(report.setup.stop_price, _Digits);
   message += " target=" + DoubleToString(report.setup.target_price, _Digits);
   message += " rr=" + DoubleToString(report.setup.reward_r, 2);
   message += " exit_f3=" + IntegerToString(report.exit_signal.event_id);
   Print(message);
}

#endif // __FP_NDS_HOOK_TRADE_ENGINE_MQH__
