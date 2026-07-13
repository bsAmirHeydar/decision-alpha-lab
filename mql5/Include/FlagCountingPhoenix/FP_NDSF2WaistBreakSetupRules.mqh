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
//   Reward/Risk = abs(Target-Entry) / abs(Entry-Stop).

bool FP_NDSF2IsWaistBreakArmedBody(const FP_FlagEvent &f2,
                                   const FP_NDSF2WaistTradeConfig &cfg)
{
   if(f2.level != FP_LEVEL_F2) return false;
   if(f2.direction != FP_DIR_BULLISH && f2.direction != FP_DIR_BEARISH) return false;
   if(!f2.f2_parent_ready || !f2.f2_origin_found) return false;
   if(!f2.f2_body_complete) return false;
   if(cfg.require_f2_size_gate && !f2.f2_size_gate_passed) return false;

   // The exact local-F3 exit can only be owned by a source F2 that the
   // canonical lifecycle can later promote into F3. This dependency is an
   // explicit operator policy; fixed and independent HTF-F3 exits do not use it.
   if(FP_NDSF2ExitModeUsesEntryTimeframeF3(cfg.exit_mode) &&
      cfg.require_canonical_f3_spawn_for_local_exit &&
      !f2.f2_size_gate_passed)
      return false;

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


bool FP_NDSF2LevelTouchedSinceAvailability(const MqlRates &rates[],
                                            const int rates_total,
                                            const int available_index,
                                            const int direction,
                                            const double level,
                                            const bool target_level)
{
   if(rates_total <= 0 || available_index < 0 || available_index >= rates_total)
      return true;

   for(int i=available_index; i<rates_total; i++)
   {
      if(direction == FP_DIR_BULLISH)
      {
         if(target_level)
         {
            if(rates[i].high >= level) return true;
         }
         else
         {
            if(rates[i].low <= level) return true;
         }
      }
      else if(direction == FP_DIR_BEARISH)
      {
         if(target_level)
         {
            if(rates[i].low <= level) return true;
         }
         else
         {
            if(rates[i].high >= level) return true;
         }
      }
      else return true;
   }
   return false;
}

bool FP_NDSF2PairComesBefore(const FP_FlagEvent &events[],
                             const int f2_a,
                             const int available_a,
                             const int f2_b,
                             const int available_b)
{
   if(available_a != available_b) return (available_a > available_b);
   if(events[f2_a].leg2.index_anchor != events[f2_b].leg2.index_anchor)
      return (events[f2_a].leg2.index_anchor > events[f2_b].leg2.index_anchor);
   if(events[f2_a].origin.index_anchor != events[f2_b].origin.index_anchor)
      return (events[f2_a].origin.index_anchor > events[f2_b].origin.index_anchor);
   if(events[f2_a].scale_L != events[f2_b].scale_L)
      return (events[f2_a].scale_L < events[f2_b].scale_L);
   return (events[f2_a].event_id > events[f2_b].event_id);
}

int FP_NDSF2CollectWaistBreakPairs(const FP_FlagEvent &events[],
                                   const int event_count,
                                   const MqlRates &rates[],
                                   const int rates_total,
                                   const FP_NDSF2WaistTradeConfig &cfg,
                                   const double epsilon_points,
                                   int &f1_indices[],
                                   int &f2_indices[],
                                   int &body_available_indices[])
{
   ArrayResize(f1_indices, 0);
   ArrayResize(f2_indices, 0);
   ArrayResize(body_available_indices, 0);

   int latest_closed = rates_total - 1;
   int n = MathMin(event_count, ArraySize(events));
   for(int i=0; i<n; i++)
   {
      if(!FP_NDSF2IsWaistBreakArmedBody(events[i], cfg)) continue;

      int parent = FP_CanonicalFindParentIndex(events, n, events[i]);
      if(parent < 0) continue;
      if(!FP_NDSF2IsDirectConfirmedParentF1(events[parent], events[i])) continue;

      int available_at = FP_NDSF2NodeAvailabilityIndex(rates, rates_total,
                                                       events[i].leg2,
                                                       epsilon_points);
      if(available_at < 0 || available_at > latest_closed) continue;
      int age = latest_closed - available_at;
      if(cfg.max_setup_age_bars >= 0 && age > cfg.max_setup_age_bars) continue;

      int size = ArraySize(f2_indices);
      int next_size = size + 1;
      bool resized = (ArrayResize(f1_indices, next_size) == next_size &&
                      ArrayResize(f2_indices, next_size) == next_size &&
                      ArrayResize(body_available_indices, next_size) == next_size);
      if(!resized)
      {
         ArrayResize(f1_indices, size);
         ArrayResize(f2_indices, size);
         ArrayResize(body_available_indices, size);
         break;
      }
      f1_indices[size] = parent;
      f2_indices[size] = i;
      body_available_indices[size] = available_at;
   }

   int count = ArraySize(f2_indices);
   // Deterministic insertion sort: newest observable context first, then newest
   // Leg2/body, then smaller scale. This matters only when concurrency policy
   // blocks some otherwise valid contexts.
   for(int i=1; i<count; i++)
   {
      int f1_key = f1_indices[i];
      int f2_key = f2_indices[i];
      int av_key = body_available_indices[i];
      int j = i - 1;
      while(j >= 0 &&
            FP_NDSF2PairComesBefore(events, f2_key, av_key,
                                    f2_indices[j], body_available_indices[j]))
      {
         f1_indices[j + 1] = f1_indices[j];
         f2_indices[j + 1] = f2_indices[j];
         body_available_indices[j + 1] = body_available_indices[j];
         j--;
      }
      f1_indices[j + 1] = f1_key;
      f2_indices[j + 1] = f2_key;
      body_available_indices[j + 1] = av_key;
   }
   return count;
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
   int f1_indices[];
   int f2_indices[];
   int available_indices[];
   int count = FP_NDSF2CollectWaistBreakPairs(events, event_count,
                                              rates, rates_total,
                                              cfg, epsilon_points,
                                              f1_indices, f2_indices,
                                              available_indices);
   if(count <= 0)
   {
      f1_index = -1;
      f2_index = -1;
      body_available_index = -1;
      return false;
   }
   f1_index = f1_indices[0];
   f2_index = f2_indices[0];
   body_available_index = available_indices[0];
   return true;
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
                            const FP_FlagEvent &f2,
                            const long setup_hash)
{
   int short_hash = (int)(setup_hash % 10000000);
   string comment = cfg.comment_prefix + "|W2|L" + IntegerToString(f2.scale_L) +
                    "|" + IntegerToString(short_hash);
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

double FP_NDSF2RewardRiskAtEntry(const double entry,
                                      const double stop,
                                      const double target)
{
   double risk = MathAbs(entry - stop);
   double reward = MathAbs(target - entry);
   if(risk <= 0.0 || reward <= 0.0) return 0.0;
   return reward / risk;
}

bool FP_NDSF2AdjustEntryForMinimumRewardRisk(const string symbol,
                                             const FP_NDSF2WaistTradeConfig &cfg,
                                             FP_NDSF2WaistTradeSetup &setup)
{
   if(!cfg.use_min_reward_risk_filter) return true;

   double required_rr = MathMax(0.0, cfg.min_reward_risk);
   if(required_rr <= 0.0) return true;

   double current_rr = FP_NDSF2RewardRiskAtEntry(setup.entry_price,
                                                 setup.stop_price,
                                                 setup.target_price);
   if(current_rr + 1e-12 >= required_rr) return true;
   if(!cfg.adjust_entry_to_min_reward_risk) return false;

   // Solve the exact boundary:
   // abs(Target-Entry) / abs(Entry-Stop) = required_rr
   // Entry = (Target + required_rr * Stop) / (1 + required_rr)
   // For a Buy Limit we round down, and for a Sell Limit we round up. Both
   // round toward the stop, so the executable RR cannot fall below the request.
   double raw_entry = (setup.target_price + required_rr * setup.stop_price) /
                      (1.0 + required_rr);
   double adjusted = raw_entry;

   if(setup.direction == FP_DIR_BULLISH)
   {
      adjusted = FP_NDSHookTradeNormalizePrice(symbol, raw_entry, false);
      if(adjusted > setup.structural_entry_price)
         adjusted = setup.structural_entry_price;
   }
   else if(setup.direction == FP_DIR_BEARISH)
   {
      adjusted = FP_NDSHookTradeNormalizePrice(symbol, raw_entry, true);
      if(adjusted < setup.structural_entry_price)
         adjusted = setup.structural_entry_price;
   }
   else return false;

   double tick = FP_NDSHookTradeTickSize(symbol);
   setup.entry_adjusted_for_reward_risk =
      (MathAbs(adjusted - setup.structural_entry_price) > MathMax(1e-12, tick * 0.25));
   setup.entry_price = adjusted;
   setup.point_2_limit_price = adjusted;
   return true;
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
   setup.period = period;
   setup.f1_event_id = f1.event_id;
   setup.f2_event_id = f2.event_id;
   setup.sequence_id = f2.sequence_id;
   setup.parent_sequence_id = f2.parent_sequence_id;
   setup.f2_parent_event_id = f2.parent_event_id;
   setup.f2_chain_index = f2.chain_index;
   setup.body_available_index = body_available_index;
   setup.age_bars = rates_total - 1 - body_available_index;
   setup.body_available_time = rates[body_available_index].time;
   setup.f1_waist_node_id = f1.waist.id;
   setup.f2_origin_node_id = f2.origin.id;
   setup.f2_waist_node_id = f2.waist.id;
   setup.initial_f2_leg2_node_id = f2.leg2.id;
   setup.f1_waist_time = f1.waist.time_anchor;
   setup.f2_origin_time = f2.origin.time_anchor;
   setup.f2_waist_time = f2.waist.time_anchor;
   setup.f2_leg2_time = f2.leg2.time_anchor;
   setup.point_1_price = f2.waist.price;
   setup.parent_f1_waist_price = f1.waist.price;
   setup.f2_flag_end_price = f2.leg2.price;
   setup.setup_hash = FP_NDSF2BuildSetupHash(symbol, period, f1, f2);
   setup.broker_comment = FP_NDSF2BuildComment(cfg, f2, setup.setup_hash);

   double entry_ticks = MathMax(1.0, cfg.entry_behind_f2_waist_ticks);
   double stop_ticks = MathMax(1.0, cfg.stop_behind_f1_waist_ticks);
   double entry_offset = entry_ticks * trade_tick;
   double stop_offset = stop_ticks * trade_tick;
   int stops_level = MathMax(0, (int)SymbolInfoInteger(symbol, SYMBOL_TRADE_STOPS_LEVEL));
   double min_dist = stops_level * point;

   if(setup.direction == FP_DIR_BULLISH)
   {
      setup.structural_entry_price = FP_NDSHookTradeNormalizePrice(symbol,
                                                                   f2.waist.price - entry_offset,
                                                                   false);
      setup.entry_price = setup.structural_entry_price;
      setup.stop_price = FP_NDSHookTradeNormalizePrice(symbol,
                                                       f1.waist.price - stop_offset,
                                                       false);
      setup.target_price = FP_NDSF2NormalizeNearest(symbol, f2.leg2.price);
   }
   else if(setup.direction == FP_DIR_BEARISH)
   {
      setup.structural_entry_price = FP_NDSHookTradeNormalizePrice(symbol,
                                                                   f2.waist.price + entry_offset,
                                                                   true);
      setup.entry_price = setup.structural_entry_price;
      setup.stop_price = FP_NDSHookTradeNormalizePrice(symbol,
                                                       f1.waist.price + stop_offset,
                                                       true);
      setup.target_price = FP_NDSF2NormalizeNearest(symbol, f2.leg2.price);
   }
   else return false;

   // This original F2 two-leg endpoint is the economic reference target in
   // all exit modes. Both dynamic F3 exits deliberately keep RR and entry repricing
   // anchored here because the eventual F3 retest node does not yet exist.
   setup.rr_reference_target_price = setup.target_price;
   setup.initial_broker_take_profit_price =
      (cfg.exit_mode == FP_NDS_F2_EXIT_FIXED_F2_FLAG_END ? setup.target_price : 0.0);

   setup.point_2_limit_price = setup.entry_price;
   if(!FP_NDSF2AdjustEntryForMinimumRewardRisk(symbol, cfg, setup)) return false;

   // The body may remain structurally valid for many bars, but the order may not
   // be created retrospectively after its executable Point 2 or its original F2
   // target was already touched while no order existed. This preserves causal
   // timing when an HTF gate opens after the F2 body became observable.
   if(FP_NDSF2LevelTouchedSinceAvailability(rates, rates_total,
                                             body_available_index,
                                             setup.direction,
                                             setup.target_price,
                                             true))
      return false;
   if(FP_NDSF2LevelTouchedSinceAvailability(rates, rates_total,
                                             body_available_index,
                                             setup.direction,
                                             setup.entry_price,
                                             false))
      return false;

   // Validate the final executable geometry after any RR-based entry movement.
   if(setup.direction == FP_DIR_BULLISH)
   {
      if(!(setup.stop_price < setup.entry_price && setup.entry_price < setup.target_price))
         return false;
      if(!(setup.entry_price < market.ask - min_dist)) return false;
      if(setup.entry_price - setup.stop_price < min_dist) return false;
      if(setup.target_price - setup.entry_price < min_dist) return false;
      if(market.bid >= setup.target_price) return false;
   }
   else
   {
      if(!(setup.target_price < setup.entry_price && setup.entry_price < setup.stop_price))
         return false;
      if(!(setup.entry_price > market.bid + min_dist)) return false;
      if(setup.stop_price - setup.entry_price < min_dist) return false;
      if(setup.entry_price - setup.target_price < min_dist) return false;
      if(market.ask <= setup.target_price) return false;
   }

   setup.risk_distance = MathAbs(setup.entry_price - setup.stop_price);
   setup.reward_distance = MathAbs(setup.target_price - setup.entry_price);
   if(setup.risk_distance <= 0.0 || setup.reward_distance <= 0.0) return false;
   setup.reward_risk = setup.reward_distance / setup.risk_distance;

   if(cfg.use_min_reward_risk_filter &&
      setup.reward_risk + 1e-12 < MathMax(0.0, cfg.min_reward_risk))
      return false;

   setup.eligible = true;
   return true;
}

#endif // __FP_NDS_F2_WAIST_BREAK_SETUP_RULES_MQH__
