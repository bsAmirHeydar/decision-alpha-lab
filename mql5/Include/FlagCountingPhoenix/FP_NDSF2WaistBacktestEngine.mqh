#ifndef __FP_NDS_F2_WAIST_BACKTEST_ENGINE_MQH__
#define __FP_NDS_F2_WAIST_BACKTEST_ENGINE_MQH__
#property strict

#include "FP_Timebase.mqh"
#include "FP_NodeScaleList.mqh"
#include "FP_NDSF2FastDetector.mqh"
#include "FP_NDSF2WaistTradeEngine.mqh"
#include "FP_NDSF2WaistBacktestTypes.mqh"
#include "FP_NDSF2HigherTimeframePhaseFilter.mqh"

void FP_NDSF2BacktestApplyProfile(FP_NDSBacktestRuntimeConfig &cfg)
{
   if(cfg.profile == FP_NDS_BACKTEST_PROFILE_FAST)
   {
      cfg.requested_bars = 420;
      cfg.min_closed_bars = 140;
      cfg.use_multi_scale = true;
      cfg.scale_l1 = 2;
      cfg.scale_l2 = 3;
      cfg.scale_l3 = 5;
      cfg.scale_l4 = 0;
      cfg.scale_l5 = 0;
      cfg.scale_l6 = 0;
      cfg.scale_l7 = 0;
      cfg.scale_l8 = 0;
      cfg.max_events = 900;
      cfg.max_hooks = 0;
   }
   else if(cfg.profile == FP_NDS_BACKTEST_PROFILE_PARITY)
   {
      cfg.requested_bars = 2500;
      cfg.min_closed_bars = 200;
      cfg.use_multi_scale = true;
      cfg.scale_l1 = 2;
      cfg.scale_l2 = 3;
      cfg.scale_l3 = 5;
      cfg.scale_l4 = 8;
      cfg.scale_l5 = 13;
      cfg.scale_l6 = 21;
      cfg.scale_l7 = 0;
      cfg.scale_l8 = 0;
      cfg.max_events = 4000;
      cfg.max_hooks = 0;
   }

   if(cfg.requested_bars < 140) cfg.requested_bars = 140;
   if(cfg.min_closed_bars < 50) cfg.min_closed_bars = 50;
   if(cfg.max_events < 100) cfg.max_events = 100;
   cfg.max_hooks = 0;
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

FP_NDSF2WaistRunResult FP_RunNDSF2WaistBacktestCycle(
   const string symbol,
   const ENUM_TIMEFRAMES period,
   const FP_NDSBacktestRuntimeConfig &runtime_cfg,
   const FP_Config &detector_cfg,
   const FP_NDSF2WaistTradeConfig &trade_cfg,
   const FP_NDSF2HigherTimeframePhaseConfig &htf_cfg,
   FP_NDSF2HigherTimeframePhaseSnapshot &htf_snapshot)
{
   // Higher-timeframe context is cached by its current open-bar timestamp. The
   // expensive canonical F/Hook pass therefore runs only once per new HTF bar,
   // while the lower-timeframe detector remains once per lower-timeframe bar.
   FP_NDSF2RefreshHigherTimeframePhase(symbol, htf_cfg, htf_snapshot);

   bool entry_gate_open = (!htf_cfg.enabled || htf_snapshot.gate_open);
   int allowed_entry_direction =
      (!htf_cfg.enabled ? FP_DIR_NONE : htf_snapshot.allowed_direction);

   int phase_cancel_errors = 0;
   int phase_cancelled = 0;
   if(htf_cfg.enabled && htf_cfg.cancel_disallowed_pending_orders)
   {
      phase_cancelled = FP_NDSF2CancelPendingOrdersOutsideDirection(
         symbol,
         trade_cfg,
         entry_gate_open,
         allowed_entry_direction,
         phase_cancel_errors);
   }

   int target_cancel_errors = 0;
   int target_cancelled = 0;
   if(trade_cfg.cancel_pending_if_target_touched_before_fill)
      target_cancelled = FP_NDSF2CancelConsumedPendingOrders(symbol, period,
                                                              trade_cfg,
                                                              target_cancel_errors);

   int cancel_errors = phase_cancel_errors + target_cancel_errors;
   int active_orders = FP_NDSF2CountManagedOrdersOnSymbol(symbol, trade_cfg, FP_DIR_NONE);
   int active_positions = FP_NDSF2CountManagedPositionsOnSymbol(symbol, trade_cfg, FP_DIR_NONE);
   int active_total = active_orders + active_positions;

   // A blocked HTF gate does not close live positions. It only prevents new
   // entries and, when enabled, removes still-unfilled pending orders. Dynamic
   // F3-retest positions still require the lower-timeframe F2 event stream to
   // discover their confirmation node, so only that case continues to detector.
   bool needs_dynamic_exit_detection =
      (active_positions > 0 &&
       trade_cfg.exit_mode == FP_NDS_F2_EXIT_F3_FLAG_RETEST);

   if(!entry_gate_open && !needs_dynamic_exit_detection)
   {
      if(cancel_errors > 0) return FP_NDS_F2_RUN_ERROR;
      if(phase_cancelled > 0)
         return FP_NDS_F2_RUN_PENDING_CANCELLED_HTF_FILTER;
      if(target_cancelled > 0)
         return FP_NDS_F2_RUN_PENDING_CANCELLED_TARGET_CONSUMED;
      if(active_orders > 0) return FP_NDS_F2_RUN_PENDING_HELD;
      if(active_positions > 0) return FP_NDS_F2_RUN_POSITION_HELD;
      return FP_NDS_F2_RUN_BLOCKED;
   }

   // Preserve the ultra-light hold path whenever no additional context can be
   // admitted. One exception is a still-pending order: overlap arbitration may
   // need the detector to discover a wider replacement. Open dynamic-exit
   // positions also continue to receive the F2 confirmation stream.
   bool pending_replacement_scan =
      (trade_cfg.use_stop_space_overlap_deduplication &&
       active_orders > 0 && active_positions == 0 && entry_gate_open);

   bool hard_parallel_block = false;
   if(active_total > 0 && !pending_replacement_scan && !needs_dynamic_exit_detection)
   {
      if(!FP_NDSF2AccountSupportsIndependentContexts()) hard_parallel_block = true;
      if(trade_cfg.max_concurrent_managed_exposures > 0 &&
         active_total >= trade_cfg.max_concurrent_managed_exposures)
         hard_parallel_block = true;
      if(!trade_cfg.allow_same_direction_multiple_contexts &&
         !trade_cfg.allow_opposite_direction_hedge)
         hard_parallel_block = true;
   }
   if(hard_parallel_block)
   {
      if(cancel_errors > 0) return FP_NDS_F2_RUN_ERROR;
      if(phase_cancelled > 0)
         return FP_NDS_F2_RUN_PENDING_CANCELLED_HTF_FILTER;
      if(target_cancelled > 0)
         return FP_NDS_F2_RUN_PENDING_CANCELLED_TARGET_CONSUMED;
      if(active_orders > 0) return FP_NDS_F2_RUN_PENDING_HELD;
      if(active_positions > 0) return FP_NDS_F2_RUN_POSITION_HELD;
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
   if((!timebase_report.ok && runtime_cfg.strict_timebase) ||
      copied < runtime_cfg.min_closed_bars)
   {
      if(cancel_errors > 0) return FP_NDS_F2_RUN_ERROR;
      if(phase_cancelled > 0)
         return FP_NDS_F2_RUN_PENDING_CANCELLED_HTF_FILTER;
      if(target_cancelled > 0)
         return FP_NDS_F2_RUN_PENDING_CANCELLED_TARGET_CONSUMED;
      int orders = FP_NDSF2CountManagedOrdersOnSymbol(symbol, trade_cfg, FP_DIR_NONE);
      int positions = FP_NDSF2CountManagedPositionsOnSymbol(symbol, trade_cfg, FP_DIR_NONE);
      if(orders > 0) return FP_NDS_F2_RUN_PENDING_HELD;
      if(positions > 0) return FP_NDS_F2_RUN_POSITION_HELD;
      return FP_NDS_F2_RUN_IDLE;
   }

   int scales[];
   int scale_count = FP_NDSF2BacktestBuildScales(runtime_cfg, scales);
   if(scale_count <= 0) return FP_NDS_F2_RUN_ERROR;

   FP_FlagEvent events[];
   int event_count = FP_DetectF2ExecutionScales(rates, copied,
                                                scales, scale_count,
                                                detector_cfg, events);
   FP_NDSF2WaistRunResult result = FP_RunNDSF2WaistTradeCore(
      symbol,
      period,
      rates,
      copied,
      events,
      event_count,
      detector_cfg.boundary_epsilon_points,
      trade_cfg,
      entry_gate_open,
      allowed_entry_direction);

   // The new-bar detector may have just exposed the F2 confirmation node. Run
   // the lightweight tick manager once immediately so the dynamic F3 TP can be
   // armed without waiting for the next market tick.
   FP_NDSF2ManageDynamicExitOnTick(symbol, period, trade_cfg);

   if(result == FP_NDS_F2_RUN_IDLE && cancel_errors > 0)
      return FP_NDS_F2_RUN_ERROR;
   if(result == FP_NDS_F2_RUN_IDLE && phase_cancelled > 0)
      return FP_NDS_F2_RUN_PENDING_CANCELLED_HTF_FILTER;
   if(result == FP_NDS_F2_RUN_IDLE && target_cancelled > 0)
      return FP_NDS_F2_RUN_PENDING_CANCELLED_TARGET_CONSUMED;
   return result;
}

#endif // __FP_NDS_F2_WAIST_BACKTEST_ENGINE_MQH__
