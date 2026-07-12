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

bool FP_NDSF2BacktestHasManagedExposure(const FP_NDSF2WaistTradeConfig &cfg)
{
   ulong order_ticket = 0;
   ulong position_ticket = 0;
   return (FP_NDSF2CountManagedOrders(cfg, order_ticket) > 0 ||
           FP_NDSF2CountManagedPositions(cfg, position_ticket) > 0);
}

FP_NDSF2WaistRunResult FP_RunNDSF2WaistBacktestCycle(const string symbol,
                                                      const ENUM_TIMEFRAMES period,
                                                      const FP_NDSBacktestRuntimeConfig &runtime_cfg,
                                                      const FP_Config &detector_cfg,
                                                      const FP_NDSF2WaistTradeConfig &trade_cfg)
{
   if(FP_NDSF2BacktestHasManagedExposure(trade_cfg))
   {
      ulong order_ticket = 0;
      ulong position_ticket = 0;
      if(FP_NDSF2CountManagedPositions(trade_cfg, position_ticket) > 0)
         return FP_NDS_F2_RUN_POSITION_HELD;
      if(FP_NDSF2CountManagedOrders(trade_cfg, order_ticket) > 0)
         return FP_NDS_F2_RUN_PENDING_HELD;
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
      return FP_NDS_F2_RUN_IDLE;

   int scales[];
   int scale_count = FP_NDSF2BacktestBuildScales(runtime_cfg, scales);
   if(scale_count <= 0) return FP_NDS_F2_RUN_ERROR;

   FP_FlagEvent events[];
   int event_count = FP_DetectF2ExecutionScales(rates, copied,
                                                scales, scale_count,
                                                detector_cfg, events);
   return FP_RunNDSF2WaistTradeCore(symbol, period,
                                    rates, copied,
                                    events, event_count,
                                    detector_cfg.boundary_epsilon_points,
                                    trade_cfg);
}

#endif // __FP_NDS_F2_WAIST_BACKTEST_ENGINE_MQH__
