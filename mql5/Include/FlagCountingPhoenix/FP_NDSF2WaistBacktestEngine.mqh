#ifndef __FP_NDS_F2_WAIST_BACKTEST_ENGINE_MQH__
#define __FP_NDS_F2_WAIST_BACKTEST_ENGINE_MQH__
#property strict

#include "FP_Timebase.mqh"
#include "FP_NodeScaleList.mqh"
#include "FP_SequenceEngine.mqh"
#include "FP_NDSF2WaistTradeEngine.mqh"
#include "FP_NDSF2WaistBacktestTypes.mqh"

void FP_NDSF2BacktestApplyProfile(FP_NDSBacktestRuntimeConfig &cfg)
{
   if(cfg.profile == FP_NDS_BACKTEST_PROFILE_FAST)
   {
      cfg.requested_bars = 800;
      cfg.min_closed_bars = 160;
      cfg.use_multi_scale = true;
      cfg.scale_l1 = 2;
      cfg.scale_l2 = 3;
      cfg.scale_l3 = 5;
      cfg.scale_l4 = 0;
      cfg.scale_l5 = 0;
      cfg.scale_l6 = 0;
      cfg.scale_l7 = 0;
      cfg.scale_l8 = 0;
      cfg.max_events = 1800;
      cfg.max_hooks = 1800;
   }
   else if(cfg.profile == FP_NDS_BACKTEST_PROFILE_PARITY)
   {
      cfg.requested_bars = 5000;
      cfg.min_closed_bars = 200;
      cfg.use_multi_scale = true;
      cfg.scale_l1 = 2;
      cfg.scale_l2 = 3;
      cfg.scale_l3 = 5;
      cfg.scale_l4 = 8;
      cfg.scale_l5 = 13;
      cfg.scale_l6 = 21;
      cfg.scale_l7 = 34;
      cfg.scale_l8 = 55;
      cfg.max_events = 6000;
      cfg.max_hooks = 6000;
   }

   if(cfg.requested_bars < 160) cfg.requested_bars = 160;
   if(cfg.min_closed_bars < 50) cfg.min_closed_bars = 50;
   if(cfg.max_events < 100) cfg.max_events = 100;
   if(cfg.max_hooks < 100) cfg.max_hooks = 100;
   if(cfg.print_every_n_runs < 1) cfg.print_every_n_runs = 1;
}

int FP_NDSF2BacktestBuildScales(const FP_NDSBacktestRuntimeConfig &cfg,
                                int &scales[])
{
   return FP_BuildScaleList(cfg.use_multi_scale,
                            cfg.scale_l1,
                            cfg.scale_l2,
                            cfg.scale_l3,
                            cfg.scale_l4,
                            cfg.scale_l5,
                            cfg.scale_l6,
                            cfg.scale_l7,
                            cfg.scale_l8,
                            scales);
}

bool FP_NDSF2BacktestHasManagedExposure(const FP_NDSF2WaistTradeConfig &cfg)
{
   FP_NDSHookTradeConfig shared_cfg;
   FP_NDSF2BuildSharedTradeConfig(cfg, shared_cfg);
   ulong order_ticket = 0;
   ulong position_ticket = 0;
   return (FP_NDSHookTradeCountManagedOrders(shared_cfg, order_ticket) > 0 ||
           FP_NDSHookTradeCountManagedPositions(shared_cfg, position_ticket) > 0);
}

void FP_NDSF2BacktestFinishTiming(const ulong started,
                                  FP_NDSF2WaistBacktestReport &report)
{
   ulong now = GetMicrosecondCount();
   report.elapsed_microseconds = (now >= started ? now - started : 0);
}

bool FP_RunNDSF2WaistBacktestCycle(const string symbol,
                                   const ENUM_TIMEFRAMES period,
                                   const FP_NDSBacktestRuntimeConfig &runtime_cfg,
                                   const FP_Config &detector_cfg,
                                   const FP_NDSF2WaistTradeConfig &trade_cfg,
                                   FP_NDSF2WaistBacktestReport &report)
{
   FP_ResetNDSF2WaistBacktestReport(report);
   ulong started = GetMicrosecondCount();

   if(FP_NDSF2BacktestHasManagedExposure(trade_cfg))
   {
      FP_FlagEvent empty_events[];
      FP_RunNDSF2WaistTradeCore(symbol, period, empty_events, 0, trade_cfg, report.trade_report);
      report.detector_skipped_for_exposure = true;
      report.ok = report.trade_report.ok;
      report.status = report.trade_report.status;
      report.reason = report.trade_report.reason;
      FP_NDSF2BacktestFinishTiming(started, report);
      return report.ok;
   }

   FP_TimebaseConfig timebase_cfg;
   FP_DefaultTimebaseConfig(timebase_cfg);
   timebase_cfg.symbol = symbol;
   timebase_cfg.period = period;
   timebase_cfg.requested_bars = runtime_cfg.requested_bars;
   timebase_cfg.min_closed_bars = runtime_cfg.min_closed_bars;
   timebase_cfg.exclude_live_bar = true;
   timebase_cfg.require_ascending_time = true;
   timebase_cfg.strict_contract = runtime_cfg.strict_timebase;
   timebase_cfg.print_sanity = false;
   timebase_cfg.print_samples = false;

   MqlRates rates[];
   FP_TimebaseReport timebase_report;
   int copied = FP_LoadCanonicalRates(timebase_cfg, rates, timebase_report);
   report.copied_bars = copied;
   if((!timebase_report.ok && runtime_cfg.strict_timebase) || copied < runtime_cfg.min_closed_bars)
   {
      report.ok = false;
      report.status = (!timebase_report.ok ? "TIMEBASE_FAILED" : "NOT_ENOUGH_CLOSED_BARS");
      report.reason = (!timebase_report.ok ? timebase_report.reason : "copied_bars_below_minimum");
      FP_NDSF2BacktestFinishTiming(started, report);
      return false;
   }

   int scales[];
   int scale_count = FP_NDSF2BacktestBuildScales(runtime_cfg, scales);
   report.scale_count = scale_count;
   if(scale_count <= 0)
   {
      report.ok = false;
      report.status = "NO_VALID_SCALES";
      report.reason = "profile_produced_empty_scale_list";
      FP_NDSF2BacktestFinishTiming(started, report);
      return false;
   }

   FP_FlagEvent events[];
   FP_HookBranch hooks[];
   FP_DetectResult detect_result;
   FP_DetectAllScales(rates, copied, scales, scale_count,
                      detector_cfg, events, hooks, detect_result);
   report.event_count = ArraySize(events);
   report.hook_count = ArraySize(hooks);

   FP_RunNDSF2WaistTradeCore(symbol, period,
                             events, ArraySize(events),
                             trade_cfg, report.trade_report);
   report.ok = report.trade_report.ok;
   report.status = report.trade_report.status;
   report.reason = report.trade_report.reason;
   FP_NDSF2BacktestFinishTiming(started, report);
   return report.ok;
}

void FP_NDSF2BacktestUpdateStats(const FP_NDSF2WaistBacktestReport &r,
                                 FP_NDSF2WaistBacktestStats &s)
{
   s.runs++;
   if(r.ok) s.successful_runs++;
   else s.failed_runs++;
   if(r.detector_skipped_for_exposure) s.exposure_fast_paths++;
   else s.detector_runs++;
   s.last_microseconds = r.elapsed_microseconds;
   s.total_microseconds += r.elapsed_microseconds;
   if(r.elapsed_microseconds > s.max_microseconds) s.max_microseconds = r.elapsed_microseconds;
}

void FP_PrintNDSF2BacktestRun(const string tag,
                              const FP_NDSBacktestRuntimeConfig &cfg,
                              const FP_NDSF2WaistBacktestReport &r)
{
   Print(tag,
         " profile=", FP_NDSBacktestProfileName(cfg.profile),
         " ok=", (r.ok ? "true" : "false"),
         " status=", r.status,
         " reason=", r.reason,
         " bars=", r.copied_bars,
         " scales=", r.scale_count,
         " events=", r.event_count,
         " exposure_fast_path=", (r.detector_skipped_for_exposure ? "true" : "false"),
         " elapsed_us=", r.elapsed_microseconds);
}

void FP_PrintNDSF2BacktestStats(const string tag,
                                const FP_NDSF2WaistBacktestStats &s)
{
   ulong avg = (s.runs > 0 ? s.total_microseconds / s.runs : 0);
   Print(tag,
         " runs=", s.runs,
         " ok=", s.successful_runs,
         " failed=", s.failed_runs,
         " detector_runs=", s.detector_runs,
         " exposure_fast_paths=", s.exposure_fast_paths,
         " avg_us=", avg,
         " max_us=", s.max_microseconds,
         " last_us=", s.last_microseconds);
}

#endif // __FP_NDS_F2_WAIST_BACKTEST_ENGINE_MQH__
