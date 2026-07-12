#ifndef __FP_NDS_F2_WAIST_TRADE_RULES_MQH__
#define __FP_NDS_F2_WAIST_TRADE_RULES_MQH__
#property strict

#include "FP_SequenceEngine.mqh"
#include "FP_NDSHookTradeRules.mqh"
#include "FP_NDSF2WaistTradeTypes.mqh"

// Tester-only in-memory one-attempt registry. No terminal global-variable I/O.
long g_fp_nds_f2_used_hashes[];

void FP_NDSF2ResetUsedSetups()
{
   ArrayResize(g_fp_nds_f2_used_hashes, 0);
}

bool FP_NDSF2SetupUsed(const FP_NDSF2WaistTradeConfig &cfg,
                       const long setup_hash)
{
   if(!cfg.one_attempt_per_f2) return false;
   for(int i=0; i<ArraySize(g_fp_nds_f2_used_hashes); i++)
      if(g_fp_nds_f2_used_hashes[i] == setup_hash) return true;
   return false;
}

bool FP_NDSF2MarkSetupUsed(const FP_NDSF2WaistTradeConfig &cfg,
                           const long setup_hash)
{
   if(!cfg.one_attempt_per_f2) return true;
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
   dst.one_attempt_per_hook = src.one_attempt_per_f2;
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

bool FP_NDSF2IsConfirmed(const FP_FlagEvent &f2)
{
   if(f2.level != FP_LEVEL_F2) return false;
   if(f2.direction != FP_DIR_BULLISH && f2.direction != FP_DIR_BEARISH) return false;
   if(!f2.f2_parent_ready || !f2.f2_size_gate_passed || !f2.f2_can_spawn_f3) return false;
   if(f2.f2_lifecycle_status != FP_F2_LC_CONFIRMED) return false;
   if(f2.status != FP_STATUS_CONFIRMED) return false;
   if(!f2.has_waist || !f2.has_leg2 || !f2.has_confirm) return false;
   if(f2.waist.price <= 0.0 || f2.leg2.price <= 0.0 || f2.confirm.price <= 0.0) return false;
   return true;
}

// Exact bar where a confirmed node became observable. Equal-price touches do not
// count as right-side clearance, matching Phoenix Level-02 node semantics.
int FP_NDSF2NodeAvailabilityIndex(const MqlRates &rates[],
                                  const int total,
                                  const FP_Node &node,
                                  const double epsilon_points)
{
   if(!node.confirmed || node.L < 1 || node.index_end < 0 || node.index_end >= total)
      return -1;

   double eps = FP_EpsilonPrice(epsilon_points);
   int cleared = 0;
   for(int i=node.index_end + 1; i<total; i++)
   {
      if(node.kind == FP_NODE_HIGH)
      {
         if(FP_BreaksAbove(rates[i].high, node.price, eps)) return -1;
         if(FP_AlmostEqual(rates[i].high, node.price, eps)) continue;
      }
      else if(node.kind == FP_NODE_LOW)
      {
         if(FP_BreaksBelow(rates[i].low, node.price, eps)) return -1;
         if(FP_AlmostEqual(rates[i].low, node.price, eps)) continue;
      }
      else return -1;

      cleared++;
      if(cleared >= node.L) return i;
   }
   return -1;
}

bool FP_NDSF2SelectLatestPair(const FP_FlagEvent &events[],
                              const int event_count,
                              const MqlRates &rates[],
                              const int rates_total,
                              const FP_NDSF2WaistTradeConfig &cfg,
                              const double epsilon_points,
                              int &f1_index,
                              int &f2_index,
                              int &availability_index)
{
   f1_index = -1;
   f2_index = -1;
   availability_index = -1;
   int latest_closed = rates_total - 1;
   int n = MathMin(event_count, ArraySize(events));

   for(int i=0; i<n; i++)
   {
      if(!FP_NDSF2IsConfirmed(events[i])) continue;
      int parent = FP_CanonicalFindParentIndex(events, n, events[i]);
      if(parent < 0) continue;
      if(events[parent].level != FP_LEVEL_F1 ||
         events[parent].direction != events[i].direction ||
         !events[parent].has_waist || events[parent].waist.price <= 0.0)
         continue;

      int available_at = FP_NDSF2NodeAvailabilityIndex(rates, rates_total,
                                                       events[i].confirm,
                                                       epsilon_points);
      if(available_at < 0 || available_at > latest_closed) continue;
      int age = latest_closed - available_at;
      if(cfg.max_setup_age_bars >= 0 && age > cfg.max_setup_age_bars) continue;

      bool better = false;
      if(f2_index < 0) better = true;
      else if(available_at > availability_index) better = true;
      else if(available_at == availability_index &&
              events[i].confirm.index_anchor > events[f2_index].confirm.index_anchor) better = true;
      else if(available_at == availability_index &&
              events[i].confirm.index_anchor == events[f2_index].confirm.index_anchor &&
              events[i].origin.index_anchor > events[f2_index].origin.index_anchor) better = true;
      else if(available_at == availability_index &&
              events[i].confirm.index_anchor == events[f2_index].confirm.index_anchor &&
              events[i].origin.index_anchor == events[f2_index].origin.index_anchor &&
              events[i].scale_L < events[f2_index].scale_L) better = true;

      if(better)
      {
         f1_index = parent;
         f2_index = i;
         availability_index = available_at;
      }
   }
   return (f1_index >= 0 && f2_index >= 0 && availability_index >= 0);
}

long FP_NDSF2BuildSetupHash(const string symbol,
                            const ENUM_TIMEFRAMES period,
                            const FP_FlagEvent &f1,
                            const FP_FlagEvent &f2)
{
   string key = symbol + "|" + EnumToString(period);
   key += "|D=" + IntegerToString(f2.direction);
   key += "|F1W=" + IntegerToString((long)f1.waist.time_anchor);
   key += "|F2O=" + IntegerToString((long)f2.origin.time_anchor);
   key += "|F2W=" + IntegerToString((long)f2.waist.time_anchor);
   key += "|F2L2=" + IntegerToString((long)f2.leg2.time_anchor);
   key += "|F2C=" + IntegerToString((long)f2.confirm.time_anchor);
   return (long)FP_NDSHookTradeHash(key);
}

string FP_NDSF2BuildComment(const FP_NDSF2WaistTradeConfig &cfg,
                            const FP_FlagEvent &f2)
{
   string comment = cfg.comment_prefix + "|F2|L" + IntegerToString(f2.scale_L);
   if(StringLen(comment) > 31) comment = StringSubstr(comment, 0, 31);
   return comment;
}

double FP_NDSF2NormalizeNearest(const string symbol, const double price)
{
   double tick = FP_NDSHookTradeTickSize(symbol);
   int digits = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
   if(tick <= 0.0) return NormalizeDouble(price, digits);
   return NormalizeDouble(MathRound(price / tick) * tick, digits);
}

bool FP_NDSF2BuildSetup(const string symbol,
                        const ENUM_TIMEFRAMES period,
                        const MqlRates &rates[],
                        const int rates_total,
                        const FP_FlagEvent &f1,
                        const FP_FlagEvent &f2,
                        const int availability_index,
                        const FP_NDSF2WaistTradeConfig &cfg,
                        FP_NDSF2WaistTradeSetup &setup)
{
   FP_ResetNDSF2WaistTradeSetup(setup);
   if(rates_total <= 0 || availability_index < 0 || availability_index >= rates_total) return false;
   if(!FP_NDSF2IsConfirmed(f2)) return false;
   if(f1.level != FP_LEVEL_F1 || f1.direction != f2.direction ||
      !f1.has_waist || f1.waist.price <= 0.0) return false;

   MqlTick tick;
   if(!SymbolInfoTick(symbol, tick) || tick.bid <= 0.0 || tick.ask <= 0.0) return false;

   double trade_tick = FP_NDSHookTradeTickSize(symbol);
   double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
   if(trade_tick <= 0.0 || point <= 0.0) return false;

   setup.direction = f2.direction;
   setup.scale_L = f2.scale_L;
   setup.f1_event_id = f1.event_id;
   setup.f2_event_id = f2.event_id;
   setup.sequence_id = f2.sequence_id;
   setup.availability_index = availability_index;
   setup.age_bars = rates_total - 1 - availability_index;
   setup.availability_time = rates[availability_index].time;
   setup.f1_waist_price = f1.waist.price;
   setup.f2_waist_price = f2.waist.price;
   setup.f2_leg2_price = f2.leg2.price;
   setup.setup_hash = FP_NDSF2BuildSetupHash(symbol, period, f1, f2);
   setup.broker_comment = FP_NDSF2BuildComment(cfg, f2);

   if(FP_NDSF2SetupUsed(cfg, setup.setup_hash)) return false;

   double offset = MathMax(0.0, cfg.entry_offset_ticks) * trade_tick;
   int stops_level = MathMax(0, (int)SymbolInfoInteger(symbol, SYMBOL_TRADE_STOPS_LEVEL));
   double min_dist = stops_level * point;

   if(setup.direction == FP_DIR_BULLISH)
   {
      setup.entry_price = FP_NDSHookTradeNormalizePrice(symbol, f2.waist.price - offset, false);
      setup.stop_price = FP_NDSF2NormalizeNearest(symbol, f1.waist.price);
      setup.target_price = FP_NDSF2NormalizeNearest(symbol, f2.leg2.price);
      if(!(setup.stop_price < setup.entry_price && setup.entry_price < setup.target_price)) return false;
      if(!(setup.entry_price < tick.ask - min_dist)) return false;
      if(setup.entry_price - setup.stop_price < min_dist) return false;
      if(setup.target_price - setup.entry_price < min_dist) return false;
   }
   else if(setup.direction == FP_DIR_BEARISH)
   {
      setup.entry_price = FP_NDSHookTradeNormalizePrice(symbol, f2.waist.price + offset, true);
      setup.stop_price = FP_NDSF2NormalizeNearest(symbol, f1.waist.price);
      setup.target_price = FP_NDSF2NormalizeNearest(symbol, f2.leg2.price);
      if(!(setup.target_price < setup.entry_price && setup.entry_price < setup.stop_price)) return false;
      if(!(setup.entry_price > tick.bid + min_dist)) return false;
      if(setup.stop_price - setup.entry_price < min_dist) return false;
      if(setup.entry_price - setup.target_price < min_dist) return false;
   }
   else return false;

   FP_NDSHookTradeConfig shared_cfg;
   FP_NDSF2BuildSharedTradeConfig(cfg, shared_cfg);
   string volume_reason;
   if(!FP_NDSHookTradeComputeVolume(symbol, shared_cfg,
                                    setup.entry_price, setup.stop_price,
                                    setup.volume, volume_reason)) return false;

   setup.eligible = true;
   return true;
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

bool FP_NDSF2SendLimit(const string symbol,
                       const FP_NDSF2WaistTradeConfig &cfg,
                       const FP_NDSF2WaistTradeSetup &setup,
                       ulong &ticket)
{
   ticket = 0;
   if(cfg.magic <= 0 || !setup.eligible) return false;

   string reason;
   if(!FP_NDSHookTradeCanSend(symbol, setup.direction, reason)) return false;

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
   if(ticket > 0) return true;

   ulong managed_order = 0;
   ulong managed_position = 0;
   if(FP_NDSF2CountManagedOrders(cfg, managed_order) > 0)
   {
      ticket = managed_order;
      return true;
   }
   if(FP_NDSF2CountManagedPositions(cfg, managed_position) > 0)
   {
      ticket = managed_position;
      return true;
   }
   return false;
}

#endif // __FP_NDS_F2_WAIST_TRADE_RULES_MQH__
