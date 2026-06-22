#ifndef __DAL_E0009_123_HOOK_ENGINE_MQH__
#define __DAL_E0009_123_HOOK_ENGINE_MQH__

#include <DecisionAlphaLab/Execution/E0009/DAL_E0009Types.mqh>
#include <DecisionAlphaLab/Market/DAL_Bars.mqh>
#include <DecisionAlphaLab/StructuralNodes/DAL_StructuralNodeEngine.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Engine.mqh>

double DAL_E0009SpreadPrice(const string symbol)
{
   double ask = SymbolInfoDouble(symbol, SYMBOL_ASK);
   double bid = SymbolInfoDouble(symbol, SYMBOL_BID);
   if(ask > 0.0 && bid > 0.0 && ask >= bid)
      return ask - bid;

   double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
   int spread_points = (int)SymbolInfoInteger(symbol, SYMBOL_SPREAD);
   return MathMax(0.0, spread_points * point);
}

bool DAL_E0009LoadNodes(
   const string symbol,
   const ENUM_TIMEFRAMES tf,
   const int bars_requested,
   const int L,
   DALBar &bars[],
   int &bars_count,
   DALLRuleNode &nodes[],
   int &nodes_count,
   string &reason
)
{
   bars_count = DAL_LoadBarsChronological(symbol, tf, bars_requested, true, bars);
   if(bars_count <= 0)
   {
      reason = "bars_load_failed";
      return false;
   }

   nodes_count = DAL_DetectConfirmedStructuralNodes(bars, bars_count, MathMax(1, L), nodes);
   if(nodes_count <= 0)
   {
      reason = "no_nodes";
      return false;
   }

   reason = "ok";
   return true;
}

bool DAL_E0009CollectNodesOfTypeChronological(
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const ENUM_DALNodeType type,
   DALLRuleNode &selected[]
)
{
   ArrayResize(selected, 0);

   for(int i = 0; i < nodes_count; i++)
   {
      DALLRuleNode n = nodes[i];
      if(!n.confirmed)
         continue;
      if(n.type != type)
         continue;

      int k = ArraySize(selected);
      ArrayResize(selected, k + 1);
      selected[k] = n; // chronological: oldest -> newest
   }

   return (ArraySize(selected) > 0);
}

bool DAL_E0009WindowIsMonotonicChronological(
   const DALLRuleNode &selected[],
   const int start_index,
   const int required_count,
   const ENUM_DAL_E0009_HTF_123_DIRECTION direction
)
{
   int required = MathMax(1, required_count);
   if(start_index < 0 || start_index + required > ArraySize(selected))
      return false;

   for(int i = start_index + 1; i < start_index + required; i++)
   {
      double prev_price = selected[i - 1].price;
      double curr_price = selected[i].price;

      if(direction == DAL_E0009_123_HIGHER_HIGHS)
      {
         if(!(prev_price < curr_price))
            return false;
      }
      else if(direction == DAL_E0009_123_LOWER_LOWS)
      {
         if(!(prev_price > curr_price))
            return false;
      }
      else
         return false;
   }

   return true;
}

void DAL_E0009FillPatternFromChronologicalWindow(
   const DALLRuleNode &selected[],
   const int start_index,
   const int required_count,
   const int bars_count,
   const ENUM_TIMEFRAMES tf,
   const ENUM_DAL_E0009_HTF_123_DIRECTION direction,
   DALE0009PatternState &out
)
{
   int required = MathMax(1, required_count);

   DAL_E0009_ResetPattern(out);
   out.valid = true;
   out.reason = "ok";
   out.tf = tf;
   out.direction = direction;
   out.required_count = required;

   out.p1 = selected[start_index];
   out.p2 = selected[start_index + (required / 2)];
   out.p3 = selected[start_index + required - 1]; // newest node in the selected valid sequence

   out.closed_time = out.p3.active_from_time;
   out.age_bars = bars_count - 1 - out.p3.active_from_index;
   out.amplitude = MathAbs(out.p3.price - out.p1.price);
}

bool DAL_E0009FindNearestLiveMonotonicWindow(
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const int bars_count,
   const ENUM_TIMEFRAMES tf,
   const int required_count,
   const int max_age_bars,
   const ENUM_DAL_E0009_HTF_123_DIRECTION direction,
   DALE0009PatternState &out
)
{
   DAL_E0009_ResetPattern(out);
   out.tf = tf;
   out.direction = direction;
   out.required_count = required_count;

   int required = MathMax(1, required_count);
   ENUM_DALNodeType type = (direction == DAL_E0009_123_HIGHER_HIGHS ? DAL_NODE_HIGH : DAL_NODE_LOW);

   DALLRuleNode selected[];
   if(!DAL_E0009CollectNodesOfTypeChronological(nodes, nodes_count, type, selected))
   {
      out.reason = "no_nodes_of_type";
      return false;
   }

   int count = ArraySize(selected);
   if(count < required)
   {
      out.reason = "not_enough_nodes_of_type";
      return false;
   }

   // Critical release 110 behavior:
   // Scan backwards from the live edge. Do NOT require the latest N nodes to be monotonic.
   // If the newest high breaks the chain, the previous valid 4-high chain can still define macro mode.
   for(int start_index = count - required; start_index >= 0; start_index--)
   {
      if(!DAL_E0009WindowIsMonotonicChronological(selected, start_index, required, direction))
         continue;

      DALLRuleNode newest = selected[start_index + required - 1];
      int age = bars_count - 1 - newest.active_from_index;
      if(max_age_bars > 0 && age > max_age_bars)
         continue;

      DAL_E0009FillPatternFromChronologicalWindow(selected, start_index, required, bars_count, tf, direction, out);
      return true;
   }

   out.reason = "no_nearest_live_monotonic_window";
   return false;
}

bool DAL_E0009FindLatestMonotonicPatternOfType(
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const int bars_count,
   const ENUM_TIMEFRAMES tf,
   const int required_count,
   const int max_age_bars,
   const ENUM_DAL_E0009_HTF_123_DIRECTION direction,
   DALE0009PatternState &out
)
{
   return DAL_E0009FindNearestLiveMonotonicWindow(
      nodes,
      nodes_count,
      bars_count,
      tf,
      required_count,
      max_age_bars,
      direction,
      out
   );
}

bool DAL_E0009FindLatestMonotonicPatternAny(
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const int bars_count,
   const ENUM_TIMEFRAMES tf,
   const int required_count,
   const int max_age_bars,
   DALE0009PatternState &out
)
{
   DALE0009PatternState highs;
   DALE0009PatternState lows;

   bool has_highs = DAL_E0009FindLatestMonotonicPatternOfType(nodes, nodes_count, bars_count, tf, required_count, max_age_bars,
                                                              DAL_E0009_123_HIGHER_HIGHS, highs);
   bool has_lows = DAL_E0009FindLatestMonotonicPatternOfType(nodes, nodes_count, bars_count, tf, required_count, max_age_bars,
                                                             DAL_E0009_123_LOWER_LOWS, lows);

   if(!has_highs && !has_lows)
   {
      DAL_E0009_ResetPattern(out);
      out.tf = tf;
      out.required_count = required_count;
      out.reason = "no_rising_highs_or_falling_lows";
      return false;
   }

   if(has_highs && has_lows)
   {
      if(highs.closed_time >= lows.closed_time)
         out = highs;
      else
         out = lows;
      return true;
   }

   if(has_highs)
      out = highs;
   else
      out = lows;

   return true;
}

bool DAL_E0009FindLatestClosed123(
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const int bars_count,
   const ENUM_TIMEFRAMES tf,
   const int max_age_bars,
   DALE0009HTF123State &out
)
{
   return DAL_E0009FindLatestMonotonicPatternAny(nodes, nodes_count, bars_count, tf, 3, max_age_bars, out);
}

bool DAL_E0009BuildNodeZoneLive(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &node,
   const double zone_ratio,
   double &lower,
   double &upper,
   bool &hunted
)
{
   lower = node.price;
   upper = node.price;
   hunted = false;

   if(node.active_from_index < 0 || node.active_from_index >= bars_count)
      return false;

   double extreme = DAL_M0001InitialExtreme(node.type, bars[node.active_from_index]);
   for(int i = node.active_from_index; i < bars_count; i++)
   {
      extreme = DAL_M0001UpdateExtreme(node.type, extreme, bars[i]);
      DAL_M0001Territory(node.type, node.price, extreme, zone_ratio, lower, upper);

      if(DAL_M0001Hunted(node.type, node.price, bars[i]))
         hunted = true;
   }

   return (upper > lower);
}

double DAL_E0009AverageRange(
   const DALBar &bars[],
   const int bars_count,
   const int lookback
)
{
   if(bars_count <= 0)
      return 0.0;

   int n = MathMax(1, lookback);
   int start = MathMax(0, bars_count - n);
   double sum = 0.0;
   int count = 0;

   for(int i = start; i < bars_count; i++)
   {
      double r = bars[i].high - bars[i].low;
      if(r > 0.0)
      {
         sum += r;
         count++;
      }
   }

   if(count <= 0)
      return 0.0;

   return sum / (double)count;
}

bool DAL_E0009HookIsMicroEnough(
   const string symbol,
   const DALBar &m1_bars[],
   const int m1_bars_count,
   const DALE0009PatternState &setup,
   const DALE0009Config &cfg,
   const double risk_distance,
   string &reason
)
{
   reason = "ok";

   if(!cfg.use_micro_only_filter)
      return true;

   if(risk_distance <= 0.0)
   {
      reason = "micro_zero_risk";
      return false;
   }

   if(cfg.max_hook_risk_to_setup_amplitude > 0.0 && setup.amplitude > 0.0)
   {
      double ratio = risk_distance / setup.amplitude;
      if(ratio > cfg.max_hook_risk_to_setup_amplitude)
      {
         reason = "hook_not_micro_setup_ratio_" + DoubleToString(ratio, 4);
         return false;
      }
   }

   if(cfg.max_hook_risk_to_m1_avg_range > 0.0 && cfg.micro_avg_range_bars > 0)
   {
      double avg_range = DAL_E0009AverageRange(m1_bars, m1_bars_count, cfg.micro_avg_range_bars);
      if(avg_range > 0.0)
      {
         double mult = risk_distance / avg_range;
         if(mult > cfg.max_hook_risk_to_m1_avg_range)
         {
            reason = "hook_not_micro_m1_range_" + DoubleToString(mult, 2);
            return false;
         }
      }
   }

   if(cfg.max_hook_risk_points > 0)
   {
      double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
      if(point > 0.0)
      {
         double points = risk_distance / point;
         if(points > (double)cfg.max_hook_risk_points)
         {
            reason = "hook_not_micro_points_" + DoubleToString(points, 1);
            return false;
         }
      }
   }

   return true;
}

ENUM_DAL_E0009_SIGNAL_ORDER_KIND DAL_E0009ResolveOrderKind(
   const string symbol,
   const int direction,
   const double trigger_price,
   const ENUM_DAL_E0009_ORDER_MODE mode
)
{
   if(mode == DAL_E0009_ORDER_MARKET_ON_CONFIRM)
      return DAL_E0009_KIND_MARKET;
   if(mode == DAL_E0009_ORDER_LIMIT_REVISIT)
      return DAL_E0009_KIND_LIMIT;
   if(mode == DAL_E0009_ORDER_STOP_RECLAIM)
      return DAL_E0009_KIND_STOP;

   double bid = SymbolInfoDouble(symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(symbol, SYMBOL_ASK);
   double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
   int stops_level = (int)SymbolInfoInteger(symbol, SYMBOL_TRADE_STOPS_LEVEL);
   double min_dist = MathMax(point, stops_level * point);

   if(direction > 0)
   {
      if(trigger_price < ask - min_dist)
         return DAL_E0009_KIND_LIMIT;
      if(trigger_price > ask + min_dist)
         return DAL_E0009_KIND_STOP;
      return DAL_E0009_KIND_MARKET;
   }
   else if(direction < 0)
   {
      if(trigger_price > bid + min_dist)
         return DAL_E0009_KIND_LIMIT;
      if(trigger_price < bid - min_dist)
         return DAL_E0009_KIND_STOP;
      return DAL_E0009_KIND_MARKET;
   }

   return DAL_E0009_KIND_NONE;
}

bool DAL_E0009BuildHookSignalFromNode(
   const string symbol,
   const DALBar &m1_bars[],
   const int m1_bars_count,
   const DALLRuleNode &hook,
   const DALE0009PatternState &setup,
   const int trade_direction,
   const DALE0009Config &cfg,
   DALE0009HookSignal &out
)
{
   DAL_E0009_ResetHook(out);

   if(!setup.valid)
   {
      out.reason = "setup_pattern_invalid";
      return false;
   }
   if(trade_direction == 0)
   {
      out.reason = "zero_trade_direction";
      return false;
   }

   double lower = 0.0, upper = 0.0;
   bool hunted = false;
   if(!DAL_E0009BuildNodeZoneLive(m1_bars, m1_bars_count, hook, cfg.zone_ratio, lower, upper, hunted))
   {
      out.reason = "hook_zone_failed";
      return false;
   }

   if(cfg.reject_hunted_m1_hook && hunted)
   {
      out.reason = "hook_already_hunted";
      return false;
   }

   double spread = DAL_E0009SpreadPrice(symbol);
   out.direction = trade_direction;
   out.order_mode = cfg.order_mode;
   out.hook_node = hook;
   out.zone_lower = lower;
   out.zone_upper = upper;

   double trigger_price = 0.0;

   if(trade_direction > 0)
   {
      trigger_price = upper + spread * MathMax(0.0, cfg.buy_entry_spread_mult);
      out.sl = hook.price;
   }
   else
   {
      trigger_price = lower;
      out.sl = hook.price + spread * MathMax(0.0, cfg.sell_stop_spread_mult);
   }

   out.order_kind = DAL_E0009ResolveOrderKind(symbol, trade_direction, trigger_price, cfg.order_mode);

   if(out.order_kind == DAL_E0009_KIND_MARKET)
   {
      if(trade_direction > 0)
         out.entry = SymbolInfoDouble(symbol, SYMBOL_ASK);
      else
         out.entry = SymbolInfoDouble(symbol, SYMBOL_BID);
   }
   else
      out.entry = trigger_price;

   int digits = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
   out.entry = NormalizeDouble(out.entry, digits);
   out.sl = NormalizeDouble(out.sl, digits);
   out.risk_distance = MathAbs(out.entry - out.sl);

   if(out.risk_distance <= 0.0)
   {
      out.reason = "zero_risk";
      return false;
   }

   string micro_reason = "";
   if(!DAL_E0009HookIsMicroEnough(symbol, m1_bars, m1_bars_count, setup, cfg, out.risk_distance, micro_reason))
   {
      out.reason = micro_reason;
      return false;
   }

   out.tp = 0.0;
   if(cfg.exit_mode == DAL_E0009_EXIT_FIXED_R && cfg.fixed_r > 0.0)
   {
      if(trade_direction > 0)
         out.tp = out.entry + out.risk_distance * cfg.fixed_r;
      else
         out.tp = out.entry - out.risk_distance * cfg.fixed_r;
      out.tp = NormalizeDouble(out.tp, digits);
      out.potential_r = cfg.fixed_r;
   }
   else
   {
      out.tp = 0.0;
      out.potential_r = 0.0;
   }

   out.comment = "DALE9_S_" + IntegerToString((int)setup.direction)
      + "_P_" + IntegerToString(setup.p3.id)
      + "_H_" + IntegerToString(hook.id)
      + "_" + DAL_E0009OrderKindName(out.order_kind);

   out.valid = true;
   out.reason = "ok";
   return true;
}

int DAL_E0009CollectHookSignals(
   const string symbol,
   const DALBar &m1_bars[],
   const int m1_bars_count,
   const DALLRuleNode &m1_nodes[],
   const int m1_nodes_count,
   const DALE0009PatternState &setup,
   const int trade_direction,
   const DALE0009Config &cfg,
   DALE0009HookSignal &signals[],
   DALE0009Diagnostics &diag
)
{
   ArrayResize(signals, 0);

   if(!setup.valid || trade_direction == 0)
      return 0;

   ENUM_DALNodeType wanted = (trade_direction > 0 ? DAL_NODE_LOW : DAL_NODE_HIGH);
   datetime after_time = (cfg.require_fresh_m1_hook_after_setup_close ? setup.closed_time : 0);
   int max_count = MathMax(1, cfg.max_hook_candidates_per_bar);

   for(int i = m1_nodes_count - 1; i >= 0; i--)
   {
      DALLRuleNode n = m1_nodes[i];
      if(!n.confirmed)
         continue;
      if(n.type != wanted)
         continue;

      diag.hook_seen++;

      if(after_time > 0 && n.active_from_time <= after_time)
      {
         diag.hook_after_time_reject++;
         continue;
      }

      if(cfg.m1_max_hook_age_bars > 0 && (m1_bars_count - 1 - n.active_from_index) > cfg.m1_max_hook_age_bars)
      {
         diag.hook_age_reject++;
         continue;
      }

      DALE0009HookSignal sig;
      if(!DAL_E0009BuildHookSignalFromNode(symbol, m1_bars, m1_bars_count, n, setup, trade_direction, cfg, sig))
      {
         if(sig.reason == "hook_zone_failed")
            diag.hook_zone_failed++;
         else if(sig.reason == "hook_already_hunted")
            diag.hook_hunted_reject++;
         else if(StringFind(sig.reason, "hook_not_micro", 0) == 0 || StringFind(sig.reason, "micro_", 0) == 0)
            diag.hook_micro_reject++;
         continue;
      }

      int k = ArraySize(signals);
      ArrayResize(signals, k + 1);
      signals[k] = sig;
      diag.hook_built++;

      if(ArraySize(signals) >= max_count)
         break;
   }

   return ArraySize(signals);
}

#endif
