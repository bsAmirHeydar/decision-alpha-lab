#ifndef __FP_NDS_F2_WAIST_TRADE_RULES_MQH__
#define __FP_NDS_F2_WAIST_TRADE_RULES_MQH__
#property strict

#include "FP_NDSF2WaistBreakSetupRules.mqh"
#include "FP_NDSHookTradeRules.mqh"

// Tester-only in-memory body-version registry. No terminal global variables,
// filesystem persistence, renderer state, CSV or mutex is used.
long g_fp_nds_f2_used_hashes[];

void FP_NDSF2ResetUsedSetups()
{
   ArrayResize(g_fp_nds_f2_used_hashes, 0);
}

bool FP_NDSF2SetupUsed(const FP_NDSF2WaistTradeConfig &cfg,
                       const long setup_hash)
{
   if(!cfg.one_attempt_per_f2_body) return false;
   for(int i=0; i<ArraySize(g_fp_nds_f2_used_hashes); i++)
      if(g_fp_nds_f2_used_hashes[i] == setup_hash) return true;
   return false;
}

bool FP_NDSF2MarkSetupUsed(const FP_NDSF2WaistTradeConfig &cfg,
                           const long setup_hash)
{
   if(!cfg.one_attempt_per_f2_body) return true;
   if(FP_NDSF2SetupUsed(cfg, setup_hash)) return true;
   int n = ArraySize(g_fp_nds_f2_used_hashes);
   if(ArrayResize(g_fp_nds_f2_used_hashes, n + 1) != n + 1) return false;
   g_fp_nds_f2_used_hashes[n] = setup_hash;
   return true;
}

void FP_NDSF2BuildSharedTradeConfig(const FP_NDSF2WaistTradeConfig &src,
                                    FP_NDSHookTradeConfig &dst)
{
   FP_ResetNDSHookTradeConfig(dst);
   dst.enabled = src.enabled;
   dst.send_live_orders = src.send_tester_orders;
   dst.one_attempt_per_hook = src.one_attempt_per_f2_body;
   dst.sizing_mode = src.sizing_mode;
   dst.fixed_volume = src.fixed_volume;
   dst.risk_cash = src.risk_cash;
   dst.commission_per_lot_round_turn = src.commission_per_lot_round_turn;
   dst.allow_min_lot_if_risk_too_small = src.allow_min_lot_if_risk_too_small;
   dst.max_deviation_points = src.max_deviation_points;
   dst.magic = src.magic;
   dst.comment_prefix = src.comment_prefix;
   dst.export_csv = false;
   dst.print_summary = false;
}

int FP_NDSF2OrderDirection(const ENUM_ORDER_TYPE type)
{
   if(type == ORDER_TYPE_BUY_LIMIT || type == ORDER_TYPE_BUY_STOP ||
      type == ORDER_TYPE_BUY_STOP_LIMIT || type == ORDER_TYPE_BUY)
      return FP_DIR_BULLISH;
   if(type == ORDER_TYPE_SELL_LIMIT || type == ORDER_TYPE_SELL_STOP ||
      type == ORDER_TYPE_SELL_STOP_LIMIT || type == ORDER_TYPE_SELL)
      return FP_DIR_BEARISH;
   return FP_DIR_NONE;
}

int FP_NDSF2PositionDirection(const ENUM_POSITION_TYPE type)
{
   if(type == POSITION_TYPE_BUY) return FP_DIR_BULLISH;
   if(type == POSITION_TYPE_SELL) return FP_DIR_BEARISH;
   return FP_DIR_NONE;
}

bool FP_NDSF2AccountSupportsIndependentContexts()
{
   ENUM_ACCOUNT_MARGIN_MODE mode =
      (ENUM_ACCOUNT_MARGIN_MODE)AccountInfoInteger(ACCOUNT_MARGIN_MODE);
   return (mode == ACCOUNT_MARGIN_MODE_RETAIL_HEDGING);
}

int FP_NDSF2CountManagedOrders(const FP_NDSF2WaistTradeConfig &cfg,
                               ulong &first_ticket)
{
   first_ticket = 0;
   int count = 0;
   for(int i=OrdersTotal()-1; i>=0; i--)
   {
      ulong ticket = OrderGetTicket(i);
      if(ticket == 0) continue;
      if((long)OrderGetInteger(ORDER_MAGIC) != cfg.magic) continue;
      count++;
      if(first_ticket == 0) first_ticket = ticket;
   }
   return count;
}

int FP_NDSF2CountManagedPositions(const FP_NDSF2WaistTradeConfig &cfg,
                                  ulong &first_ticket)
{
   first_ticket = 0;
   int count = 0;
   for(int i=PositionsTotal()-1; i>=0; i--)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !PositionSelectByTicket(ticket)) continue;
      if((long)PositionGetInteger(POSITION_MAGIC) != cfg.magic) continue;
      count++;
      if(first_ticket == 0) first_ticket = ticket;
   }
   return count;
}

int FP_NDSF2CountManagedOrdersOnSymbol(const string symbol,
                                       const FP_NDSF2WaistTradeConfig &cfg,
                                       const int direction)
{
   int count = 0;
   for(int i=OrdersTotal()-1; i>=0; i--)
   {
      ulong ticket = OrderGetTicket(i);
      if(ticket == 0) continue;
      if((long)OrderGetInteger(ORDER_MAGIC) != cfg.magic) continue;
      if(OrderGetString(ORDER_SYMBOL) != symbol) continue;
      int d = FP_NDSF2OrderDirection((ENUM_ORDER_TYPE)OrderGetInteger(ORDER_TYPE));
      if(direction != FP_DIR_NONE && d != direction) continue;
      count++;
   }
   return count;
}

int FP_NDSF2CountManagedPositionsOnSymbol(const string symbol,
                                          const FP_NDSF2WaistTradeConfig &cfg,
                                          const int direction)
{
   int count = 0;
   for(int i=PositionsTotal()-1; i>=0; i--)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !PositionSelectByTicket(ticket)) continue;
      if((long)PositionGetInteger(POSITION_MAGIC) != cfg.magic) continue;
      if(PositionGetString(POSITION_SYMBOL) != symbol) continue;
      int d = FP_NDSF2PositionDirection((ENUM_POSITION_TYPE)PositionGetInteger(POSITION_TYPE));
      if(direction != FP_DIR_NONE && d != direction) continue;
      count++;
   }
   return count;
}

int FP_NDSF2CountForeignPositionsOnSymbol(const string symbol,
                                          const FP_NDSF2WaistTradeConfig &cfg)
{
   int count = 0;
   for(int i=PositionsTotal()-1; i>=0; i--)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !PositionSelectByTicket(ticket)) continue;
      if(PositionGetString(POSITION_SYMBOL) != symbol) continue;
      if((long)PositionGetInteger(POSITION_MAGIC) == cfg.magic) continue;
      count++;
   }
   return count;
}

bool FP_NDSF2ExposurePolicyAllows(const string symbol,
                                  const FP_NDSF2WaistTradeConfig &cfg,
                                  const FP_NDSF2WaistTradeSetup &setup,
                                  string &reason)
{
   reason = "none";
   if(FP_NDSF2CountForeignPositionsOnSymbol(symbol, cfg) > 0)
   {
      reason = "foreign_position_on_symbol";
      return false;
   }

   int buy_count = FP_NDSF2CountManagedOrdersOnSymbol(symbol, cfg, FP_DIR_BULLISH) +
                   FP_NDSF2CountManagedPositionsOnSymbol(symbol, cfg, FP_DIR_BULLISH);
   int sell_count = FP_NDSF2CountManagedOrdersOnSymbol(symbol, cfg, FP_DIR_BEARISH) +
                    FP_NDSF2CountManagedPositionsOnSymbol(symbol, cfg, FP_DIR_BEARISH);
   int total = buy_count + sell_count;
   if(total <= 0) return true;

   if(!FP_NDSF2AccountSupportsIndependentContexts())
   {
      reason = "parallel_context_requires_hedging_account";
      return false;
   }

   if(cfg.max_concurrent_managed_exposures > 0 &&
      total >= cfg.max_concurrent_managed_exposures)
   {
      reason = "max_concurrent_managed_exposures";
      return false;
   }

   int same = (setup.direction == FP_DIR_BULLISH ? buy_count : sell_count);
   int opposite = (setup.direction == FP_DIR_BULLISH ? sell_count : buy_count);
   if(same > 0 && !cfg.allow_same_direction_multiple_contexts)
   {
      reason = "same_direction_context_disabled";
      return false;
   }
   if(opposite > 0 && !cfg.allow_opposite_direction_hedge)
   {
      reason = "opposite_direction_hedge_disabled";
      return false;
   }
   return true;
}

bool FP_NDSF2PendingTargetConsumed(const string symbol,
                                   const ENUM_TIMEFRAMES period,
                                   const ulong order_ticket)
{
   if(order_ticket == 0 || !OrderSelect(order_ticket)) return false;
   if(OrderGetString(ORDER_SYMBOL) != symbol) return false;

   ENUM_ORDER_TYPE order_type = (ENUM_ORDER_TYPE)OrderGetInteger(ORDER_TYPE);
   double target = OrderGetDouble(ORDER_TP);
   if(target <= 0.0) return false;

   MqlRates last_closed[];
   if(CopyRates(symbol, period, 1, 1, last_closed) != 1) return false;

   double tick = FP_NDSHookTradeTickSize(symbol);
   double eps = (tick > 0.0 ? tick * 0.25 : 0.0);
   if(order_type == ORDER_TYPE_BUY_LIMIT)
      return (last_closed[0].high >= target - eps);
   if(order_type == ORDER_TYPE_SELL_LIMIT)
      return (last_closed[0].low <= target + eps);
   return false;
}

bool FP_NDSF2DeletePendingOrder(const FP_NDSF2WaistTradeConfig &cfg,
                                const ulong order_ticket)
{
   if(order_ticket == 0 || !OrderSelect(order_ticket)) return false;
   if((long)OrderGetInteger(ORDER_MAGIC) != cfg.magic) return false;

   MqlTradeRequest request;
   MqlTradeResult result;
   ZeroMemory(request);
   ZeroMemory(result);
   request.action = TRADE_ACTION_REMOVE;
   request.order = order_ticket;
   request.symbol = OrderGetString(ORDER_SYMBOL);
   request.magic = (ulong)cfg.magic;

   if(!OrderSend(request, result)) return false;
   return FP_NDSHookTradeRetcodeAccepted(result.retcode);
}

int FP_NDSF2CancelConsumedPendingOrders(const string symbol,
                                        const ENUM_TIMEFRAMES period,
                                        const FP_NDSF2WaistTradeConfig &cfg,
                                        int &error_count)
{
   error_count = 0;
   ulong tickets[];
   ArrayResize(tickets, 0);
   for(int i=OrdersTotal()-1; i>=0; i--)
   {
      ulong ticket = OrderGetTicket(i);
      if(ticket == 0) continue;
      if((long)OrderGetInteger(ORDER_MAGIC) != cfg.magic) continue;
      if(OrderGetString(ORDER_SYMBOL) != symbol) continue;
      int n = ArraySize(tickets);
      if(ArrayResize(tickets, n + 1) != n + 1) break;
      tickets[n] = ticket;
   }

   int cancelled = 0;
   for(int i=0; i<ArraySize(tickets); i++)
   {
      if(!FP_NDSF2PendingTargetConsumed(symbol, period, tickets[i])) continue;
      if(FP_NDSF2DeletePendingOrder(cfg, tickets[i])) cancelled++;
      else error_count++;
   }
   return cancelled;
}

bool FP_NDSF2SendLimit(const string symbol,
                       const FP_NDSF2WaistTradeConfig &cfg,
                       FP_NDSF2WaistTradeSetup &setup,
                       ulong &ticket)
{
   ticket = 0;
   if(cfg.magic <= 0 || !setup.eligible) return false;
   if(FP_NDSF2SetupUsed(cfg, setup.setup_hash)) return false;

   string reason;
   if(!FP_NDSHookTradeCanSend(symbol, setup.direction, reason)) return false;
   if(!FP_NDSF2ExposurePolicyAllows(symbol, cfg, setup, reason)) return false;

   FP_NDSHookTradeConfig shared_cfg;
   FP_NDSF2BuildSharedTradeConfig(cfg, shared_cfg);
   string volume_reason;
   if(!FP_NDSHookTradeComputeVolume(symbol, shared_cfg,
                                    setup.entry_price, setup.stop_price,
                                    setup.volume, volume_reason))
      return false;

   MqlTradeRequest request;
   MqlTradeResult result;
   MqlTradeCheckResult check;
   ZeroMemory(request);
   ZeroMemory(result);
   ZeroMemory(check);

   request.action = TRADE_ACTION_PENDING;
   request.magic = (ulong)cfg.magic;
   request.symbol = symbol;
   request.volume = setup.volume;
   request.price = setup.entry_price;
   request.sl = setup.stop_price;
   request.tp = setup.target_price;
   request.deviation = (ulong)MathMax(0, cfg.max_deviation_points);
   request.type = (setup.direction == FP_DIR_BULLISH ? ORDER_TYPE_BUY_LIMIT : ORDER_TYPE_SELL_LIMIT);
   request.type_filling = ORDER_FILLING_RETURN;
   request.type_time = ORDER_TIME_GTC;
   request.expiration = 0;
   request.comment = setup.broker_comment;

   if(!OrderCheck(request, check)) return false;
   if(!OrderSend(request, result)) return false;
   if(!FP_NDSHookTradeRetcodeAccepted(result.retcode)) return false;

   ticket = result.order;
   if(ticket == 0)
   {
      // A placed pending order normally returns result.order. For tester/broker
      // variants that return zero, broker acceptance is still authoritative.
      ticket = (result.deal > 0 ? result.deal : (ulong)1);
   }

   // Consume the exact F2 context only after broker/tester acceptance.
   return FP_NDSF2MarkSetupUsed(cfg, setup.setup_hash);
}

#endif // __FP_NDS_F2_WAIST_TRADE_RULES_MQH__
