#ifndef __FP_NDS_F2_WAIST_TRADE_ENGINE_MQH__
#define __FP_NDS_F2_WAIST_TRADE_ENGINE_MQH__
#property strict

#include "FP_NDSF2WaistTradeRules.mqh"

FP_NDSF2WaistRunResult FP_RunNDSF2WaistTradeCore(const string symbol,
                                                  const ENUM_TIMEFRAMES period,
                                                  const MqlRates &rates[],
                                                  const int rates_total,
                                                  const FP_FlagEvent &events[],
                                                  const int event_count,
                                                  const double epsilon_points,
                                                  const FP_NDSF2WaistTradeConfig &cfg)
{
   if(!cfg.enabled) return FP_NDS_F2_RUN_IDLE;

   ulong first_order = 0;
   ulong first_position = 0;
   int managed_orders = FP_NDSF2CountManagedOrders(cfg, first_order);
   int managed_positions = FP_NDSF2CountManagedPositions(cfg, first_position);

   if(managed_positions > 1 || managed_orders > 1)
      return FP_NDS_F2_RUN_ERROR;
   if(managed_positions > 0)
      return FP_NDS_F2_RUN_POSITION_HELD;
   if(managed_orders > 0)
      return FP_NDS_F2_RUN_PENDING_HELD;
   if(FP_NDSF2CountForeignPositionsOnSymbol(symbol, cfg) > 0)
      return FP_NDS_F2_RUN_BLOCKED;

   int f1_index = -1;
   int f2_index = -1;
   int body_available_index = -1;
   if(!FP_NDSF2SelectLatestWaistBreakPair(events, event_count,
                                          rates, rates_total,
                                          cfg, epsilon_points,
                                          f1_index, f2_index,
                                          body_available_index))
      return FP_NDS_F2_RUN_IDLE;

   FP_NDSF2WaistTradeSetup setup;
   if(!FP_NDSF2BuildWaistBreakSetup(symbol, period,
                                    rates, rates_total,
                                    events[f1_index], events[f2_index],
                                    body_available_index,
                                    cfg, setup))
      return FP_NDS_F2_RUN_BLOCKED;

   if(FP_NDSF2SetupUsed(cfg, setup.setup_hash))
      return FP_NDS_F2_RUN_IDLE;

   if(!cfg.send_tester_orders)
   {
      if(!FP_NDSF2MarkSetupUsed(cfg, setup.setup_hash))
         return FP_NDS_F2_RUN_ERROR;
      return FP_NDS_F2_RUN_PAPER;
   }

   // Single-exposure recheck immediately before the request.
   managed_orders = FP_NDSF2CountManagedOrders(cfg, first_order);
   managed_positions = FP_NDSF2CountManagedPositions(cfg, first_position);
   if(managed_orders > 0 || managed_positions > 0)
      return FP_NDS_F2_RUN_BLOCKED;

   ulong ticket = 0;
   if(!FP_NDSF2SendLimit(symbol, cfg, setup, ticket))
      return FP_NDS_F2_RUN_ERROR;
   return FP_NDS_F2_RUN_ORDER_SENT;
}

#endif // __FP_NDS_F2_WAIST_TRADE_ENGINE_MQH__
