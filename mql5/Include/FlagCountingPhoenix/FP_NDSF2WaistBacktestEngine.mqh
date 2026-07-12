#ifndef __FP_NDS_F2_WAIST_BACKTEST_ENGINE_MQH__
#define __FP_NDS_F2_WAIST_BACKTEST_ENGINE_MQH__
#property strict

#include "FP_Timebase.mqh"
#include "FP_NodeScaleList.mqh"
#include "FP_NDSF2FastDetector.mqh"
#include "FP_NDSF2WaistTradeEngine.mqh"
#include "FP_NDSF2WaistBacktestTypes.mqh"

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

FP_NDSF2WaistRunResult FP_RunNDSF2WaistBacktestCycle(const string symbol,
                                                      const ENUM_TIMEFRAMES period,
                                                      const FP_NDSBacktestRuntimeConfig &runtime_cfg,
                                                      const FP_Config &detector_cfg,
                                                      const FP_NDSF2WaistTradeConfig &trade_cfg)
{
   int cancel_errors = 0;
   int cancelled = 0;
   if(trade_cfg.cancel_pending_if_target_touched_before_fill)
      cancelled = FP_NDSF2CancelConsumedPendingOrders(symbol, period,
                                                       trade_cfg, cancel_errors);

   int active_orders = FP_NDSF2CountManagedOrdersOnSymbol(symbol, trade_cfg, FP_DIR_NONE);
   int active_positions = FP_NDSF2CountManagedPositionsOnSymbol(symbol, trade_cfg, FP_DIR_NONE);
   int active_total = active_orders + active_positions;

   // Preserve the old ultra-light hold path whenever another independent
   // context cannot legally be added. This avoids unnecessary detector rebuilds
   // on netting accounts, under a reached cap, or when both parallel switches
   // are disabled.
   bool hard_parallel_block = false;
   if(active_total > 0)
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
      if(cancelled > 0) return FP_NDS_F2_RUN_PENDING_CANCELLED_TARGET_CONSUMED;
      if(active_orders > 0) return FP_NDS_F2_RUN_PENDING_HELD;
      if(active_positions > 0) return FP_NDS_F2_RUN_POSITION_HELD;
   }

   // Parallel same-direction contexts and opposite-direction hedge contexts can
   // be created while existing orders/positions are active. Therefore the fast
   // F1/F2 detector still runs once per closed bar only when policy/account mode
   // can admit another context. Heavy Hook/F3/visual branches remain absent.
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
      if(cancelled > 0) return FP_NDS_F2_RUN_PENDING_CANCELLED_TARGET_CONSUMED;
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
   FP_NDSF2WaistRunResult result = FP_RunNDSF2WaistTradeCore(symbol, period,
                                                             rates, copied,
                                                             events, event_count,
                                                             detector_cfg.boundary_epsilon_points,
                                                             trade_cfg);
   if(result == FP_NDS_F2_RUN_IDLE && cancel_errors > 0)
      return FP_NDS_F2_RUN_ERROR;
   if(result == FP_NDS_F2_RUN_IDLE && cancelled > 0)
      return FP_NDS_F2_RUN_PENDING_CANCELLED_TARGET_CONSUMED;
   return result;
}

#endif // __FP_NDS_F2_WAIST_BACKTEST_ENGINE_MQH__
