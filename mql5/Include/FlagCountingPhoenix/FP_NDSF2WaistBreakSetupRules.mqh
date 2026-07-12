#ifndef __FP_NDS_F2_WAIST_BREAK_SETUP_RULES_MQH__
#define __FP_NDS_F2_WAIST_BREAK_SETUP_RULES_MQH__
#property strict

#include "FP_SequenceEngine.mqh"
#include "FP_NDSF2WaistTradeTypes.mqh"

// Canonical setup contract:
//   F2 body = Origin -> Leg1 -> Waist -> Leg2.
//   Point 1 = F2 Waist.
//   The F2 Waist is structural Point 1.
//   A strict penetration beyond that Waist is structural Point 2.
//   The pending limit is staged one or more ticks beyond the Waist, therefore
//   the order fill is the executable Point 2.
//   Stop = beyond the direct parent F1 Waist.
//   Target = F2 Leg2 / end of the two-leg F2 flag.
//   F2 confirmation is NOT the entry trigger; reaching the target is the event
//   that would confirm F2 after the waist-break branch.

bool FP_NDSF2IsWaistBreakArmedBody(const FP_FlagEvent &f2,
                                   const FP_NDSF2WaistTradeConfig &cfg)
{
   if(f2.level != FP_LEVEL_F2) return false;
   if(f2.direction != FP_DIR_BULLISH && f2.direction != FP_DIR_BEARISH) return false;
   if(!f2.f2_parent_ready || !f2.f2_origin_found) return false;
   if(!f2.f2_body_complete) return false;
   if(cfg.require_f2_size_gate && !f2.f2_size_gate_passed) return false;

   if(f2.status == FP_STATUS_INVALIDATED || f2.f2_lifecycle_status == FP_F2_LC_INVALIDATED)
      return false;

   // A confirmed F2 has already re-broken Leg2. That is the target event, so the
   // waist-break Point-2 setup is already consumed and must not be armed.
   if(f2.status == FP_STATUS_CONFIRMED ||
      f2.f2_lifecycle_status == FP_F2_LC_CONFIRMED ||
      f2.has_confirm || f2.f2_can_spawn_f3)
      return false;

   if(!f2.has_origin || !f2.has_waist || !f2.has_leg2) return false;
   if(f2.origin.price <= 0.0 || f2.waist.price <= 0.0 || f2.leg2.price <= 0.0) return false;
   if(f2.pos_waist < 0 || f2.pos_leg2 < 0 || f2.pos_leg2 <= f2.pos_waist) return false;
   return true;
}

bool FP_NDSF2IsDirectConfirmedParentF1(const FP_FlagEvent &f1,
                                       const FP_FlagEvent &f2)
{
   if(f1.level != FP_LEVEL_F1) return false;
   if(f1.direction != f2.direction) return false;
   if(!FP_IsF1Confirmed(f1)) return false;
   if(!f1.has_waist || f1.waist.price <= 0.0) return false;
   return true;
}

// Exact closed-bar index at which a confirmed node becomes observable without
// future information. Equal touches do not count as right-side clearance.
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

bool FP_NDSF2SelectLatestWaistBreakPair(const FP_FlagEvent &events[],
                                        const int event_count,
                                        const MqlRates &rates[],
                                        const int rates_total,
                                        const FP_NDSF2WaistTradeConfig &cfg,
                                        const double epsilon_points,
                                        int &f1_index,
                                        int &f2_index,
                                        int &body_available_index)
{
   f1_index = -1;
   f2_index = -1;
   body_available_index = -1;
   int latest_closed = rates_total - 1;
   int n = MathMin(event_count, ArraySize(events));

   for(int i=0; i<n; i++)
   {
      if(!FP_NDSF2IsWaistBreakArmedBody(events[i], cfg)) continue;

      int parent = FP_CanonicalFindParentIndex(events, n, events[i]);
      if(parent < 0) continue;
      if(!FP_NDSF2IsDirectConfirmedParentF1(events[parent], events[i])) continue;

      // The setup becomes knowable when the F2 Leg2 node, and therefore the
      // complete two-leg F2 body, becomes observable. Waiting for F2.confirm is
      // prohibited because confirmation is the target event, not the trigger.
      int available_at = FP_NDSF2NodeAvailabilityIndex(rates, rates_total,
                                                       events[i].leg2,
                                                       epsilon_points);
      if(available_at < 0 || available_at > latest_closed) continue;
      int age = latest_closed - available_at;
      if(cfg.max_setup_age_bars >= 0 && age > cfg.max_setup_age_bars) continue;

      bool better = false;
      if(f2_index < 0) better = true;
      else if(available_at > body_available_index) better = true;
      else if(available_at == body_available_index &&
              events[i].leg2.index_anchor > events[f2_index].leg2.index_anchor) better = true;
      else if(available_at == body_available_index &&
              events[i].leg2.index_anchor == events[f2_index].leg2.index_anchor &&
              events[i].origin.index_anchor > events[f2_index].origin.index_anchor) better = true;
      else if(available_at == body_available_index &&
              events[i].leg2.index_anchor == events[f2_index].leg2.index_anchor &&
              events[i].origin.index_anchor == events[f2_index].origin.index_anchor &&
              events[i].scale_L < events[f2_index].scale_L) better = true;

      if(better)
      {
         f1_index = parent;
         f2_index = i;
         body_available_index = available_at;
      }
   }
   return (f1_index >= 0 && f2_index >= 0 && body_available_index >= 0);
}

long FP_NDSF2BuildSetupHash(const string symbol,
                            const ENUM_TIMEFRAMES period,
                            const FP_FlagEvent &f1,
                            const FP_FlagEvent &f2)
{
   // Leg2 belongs in the identity because a pre-entry Leg2 extension creates a
   // new current F2 flag endpoint and therefore a new target/body version.
   string key = symbol + "|" + EnumToString(period);
   key += "|D=" + IntegerToString(f2.direction);
   key += "|L=" + IntegerToString(f2.scale_L);
   key += "|F1W=" + IntegerToString((long)f1.waist.time_anchor);
   key += "|F2O=" + IntegerToString((long)f2.origin.time_anchor);
   key += "|F2W=" + IntegerToString((long)f2.waist.time_anchor);
   key += "|F2L2=" + IntegerToString((long)f2.leg2.time_anchor);
   key += "|F2L2P=" + DoubleToString(f2.leg2.price, _Digits);
   return (long)FP_NDSHookTradeHash(key);
}

string FP_NDSF2BuildComment(const FP_NDSF2WaistTradeConfig &cfg,
                            const FP_FlagEvent &f2)
{
   string comment = cfg.comment_prefix + "|WB2|L" + IntegerToString(f2.scale_L);
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

bool FP_NDSF2BuildWaistBreakSetup(const string symbol,
                                  const ENUM_TIMEFRAMES period,
                                  const MqlRates &rates[],
                                  const int rates_total,
                                  const FP_FlagEvent &f1,
                                  const FP_FlagEvent &f2,
                                  const int body_available_index,
                                  const FP_NDSF2WaistTradeConfig &cfg,
                                  FP_NDSF2WaistTradeSetup &setup)
{
   FP_ResetNDSF2WaistTradeSetup(setup);
   if(rates_total <= 0 || body_available_index < 0 || body_available_index >= rates_total)
      return false;
   if(!FP_NDSF2IsWaistBreakArmedBody(f2, cfg)) return false;
   if(!FP_NDSF2IsDirectConfirmedParentF1(f1, f2)) return false;

   MqlTick market;
   if(!SymbolInfoTick(symbol, market) || market.bid <= 0.0 || market.ask <= 0.0)
      return false;

   double trade_tick = FP_NDSHookTradeTickSize(symbol);
   double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
   if(trade_tick <= 0.0 || point <= 0.0) return false;

   setup.direction = f2.direction;
   setup.scale_L = f2.scale_L;
   setup.f1_event_id = f1.event_id;
   setup.f2_event_id = f2.event_id;
   setup.sequence_id = f2.sequence_id;
   setup.body_available_index = body_available_index;
   setup.age_bars = rates_total - 1 - body_available_index;
   setup.body_available_time = rates[body_available_index].time;
   setup.point_1_price = f2.waist.price;
   setup.parent_f1_waist_price = f1.waist.price;
   setup.f2_flag_end_price = f2.leg2.price;
   setup.setup_hash = FP_NDSF2BuildSetupHash(symbol, period, f1, f2);
   setup.broker_comment = FP_NDSF2BuildComment(cfg, f2);

   double entry_ticks = MathMax(1.0, cfg.entry_behind_f2_waist_ticks);
   double stop_ticks = MathMax(1.0, cfg.stop_behind_f1_waist_ticks);
   double entry_offset = entry_ticks * trade_tick;
   double stop_offset = stop_ticks * trade_tick;
   int stops_level = MathMax(0, (int)SymbolInfoInteger(symbol, SYMBOL_TRADE_STOPS_LEVEL));
   double min_dist = stops_level * point;

   if(setup.direction == FP_DIR_BULLISH)
   {
      // Point 1 = F2 waist. Buy Limit strictly behind/below it. A fill is the
      // executable Point 2 of the canonical F2 waist-break branch.
      setup.entry_price = FP_NDSHookTradeNormalizePrice(symbol,
                                                        f2.waist.price - entry_offset,
                                                        false);
      setup.stop_price = FP_NDSHookTradeNormalizePrice(symbol,
                                                       f1.waist.price - stop_offset,
                                                       false);
      setup.target_price = FP_NDSF2NormalizeNearest(symbol, f2.leg2.price);
      setup.point_2_limit_price = setup.entry_price;

      if(!(setup.stop_price < setup.entry_price && setup.entry_price < setup.target_price))
         return false;
      if(!(setup.entry_price < market.ask - min_dist)) return false;
      if(setup.entry_price - setup.stop_price < min_dist) return false;
      if(setup.target_price - setup.entry_price < min_dist) return false;

      // If price is already at/above the F2 flag end, target has been consumed.
      if(market.bid >= setup.target_price) return false;
   }
   else if(setup.direction == FP_DIR_BEARISH)
   {
      setup.entry_price = FP_NDSHookTradeNormalizePrice(symbol,
                                                        f2.waist.price + entry_offset,
                                                        true);
      setup.stop_price = FP_NDSHookTradeNormalizePrice(symbol,
                                                       f1.waist.price + stop_offset,
                                                       true);
      setup.target_price = FP_NDSF2NormalizeNearest(symbol, f2.leg2.price);
      setup.point_2_limit_price = setup.entry_price;

      if(!(setup.target_price < setup.entry_price && setup.entry_price < setup.stop_price))
         return false;
      if(!(setup.entry_price > market.bid + min_dist)) return false;
      if(setup.stop_price - setup.entry_price < min_dist) return false;
      if(setup.entry_price - setup.target_price < min_dist) return false;
      if(market.ask <= setup.target_price) return false;
   }
   else return false;

   setup.eligible = true;
   return true;
}

#endif // __FP_NDS_F2_WAIST_BREAK_SETUP_RULES_MQH__
