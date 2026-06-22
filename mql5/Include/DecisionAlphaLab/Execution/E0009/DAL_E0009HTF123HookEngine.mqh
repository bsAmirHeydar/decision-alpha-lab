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

bool DAL_E0009FindLatestClosed123(
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const int bars_count,
   const ENUM_TIMEFRAMES tf,
   const int max_age_bars,
   DALE0009HTF123State &out
)
{
   DAL_E0009_Reset123(out);
   out.tf = tf;

   if(nodes_count < 3)
   {
      out.reason = "not_enough_nodes";
      return false;
   }

   DALLRuleNode highs[3];
   DALLRuleNode lows[3];
   int high_count = 0;
   int low_count = 0;

   // Collect the latest 3 confirmed HIGH nodes and latest 3 confirmed LOW nodes separately.
   for(int i = nodes_count - 1; i >= 0 && (high_count < 3 || low_count < 3); i--)
   {
      DALLRuleNode n = nodes[i];
      if(!n.confirmed)
         continue;

      if(n.type == DAL_NODE_HIGH && high_count < 3)
      {
         highs[high_count] = n;
         high_count++;
      }
      else if(n.type == DAL_NODE_LOW && low_count < 3)
      {
         lows[low_count] = n;
         low_count++;
      }
   }

   bool has_higher_highs = false;
   bool has_lower_lows = false;

   DALLRuleNode hh1, hh2, hh3;
   DALLRuleNode ll1, ll2, ll3;

   if(high_count >= 3)
   {
      // highs[2] is oldest, highs[0] is newest.
      hh1 = highs[2];
      hh2 = highs[1];
      hh3 = highs[0];

      int age_hh = bars_count - 1 - hh3.active_from_index;
      if((max_age_bars <= 0 || age_hh <= max_age_bars) && hh1.price < hh2.price && hh2.price < hh3.price)
         has_higher_highs = true;
   }

   if(low_count >= 3)
   {
      // lows[2] is oldest, lows[0] is newest.
      ll1 = lows[2];
      ll2 = lows[1];
      ll3 = lows[0];

      int age_ll = bars_count - 1 - ll3.active_from_index;
      if((max_age_bars <= 0 || age_ll <= max_age_bars) && ll1.price > ll2.price && ll2.price > ll3.price)
         has_lower_lows = true;
   }

   if(!has_higher_highs && !has_lower_lows)
   {
      out.reason = "no_three_higher_highs_or_three_lower_lows";
      return false;
   }

   // If both patterns exist, choose the one whose 3rd point was confirmed later.
   bool choose_hh = has_higher_highs;
   if(has_higher_highs && has_lower_lows)
      choose_hh = (hh3.active_from_time >= ll3.active_from_time);

   out.valid = true;
   out.reason = "ok";

   if(choose_hh)
   {
      out.direction = DAL_E0009_123_HIGHER_HIGHS;
      out.p1 = hh1;
      out.p2 = hh2;
      out.p3 = hh3;
   }
   else
   {
      out.direction = DAL_E0009_123_LOWER_LOWS;
      out.p1 = ll1;
      out.p2 = ll2;
      out.p3 = ll3;
   }

   out.closed_time = out.p3.active_from_time;
   out.age_bars = bars_count - 1 - out.p3.active_from_index;
   out.amplitude = MathAbs(out.p3.price - out.p1.price);
   return true;
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

bool DAL_E0009FindLatestHookForDirection(
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const int trade_direction,
   const datetime after_time,
   const int max_hook_age_bars,
   const int current_index,
   DALLRuleNode &hook
)
{
   ENUM_DALNodeType wanted = (trade_direction > 0 ? DAL_NODE_LOW : DAL_NODE_HIGH);

   for(int i = nodes_count - 1; i >= 0; i--)
   {
      DALLRuleNode n = nodes[i];
      if(!n.confirmed)
         continue;
      if(n.type != wanted)
         continue;
      if(after_time > 0 && n.active_from_time <= after_time)
         continue;
      if(max_hook_age_bars > 0 && current_index - n.active_from_index > max_hook_age_bars)
         continue;

      hook = n;
      return true;
   }

   return false;
}

int DAL_E0009TradeDirectionFrom123(
   const DALE0009HTF123State &state,
   const ENUM_DAL_E0009_COUNTER_MODE mode
)
{
   if(!state.valid)
      return 0;

   if(mode == DAL_E0009_COUNTER_BOTH_FOR_TEST)
      return 0;

   // Counter-direction:
   // 3 higher highs => look for SELL hooks
   // 3 lower lows   => look for BUY hooks
   if(state.direction == DAL_E0009_123_HIGHER_HIGHS)
      return -1;
   if(state.direction == DAL_E0009_123_LOWER_LOWS)
      return +1;

   return 0;
}

bool DAL_E0009BuildHookSignal(
   const string symbol,
   const DALBar &m1_bars[],
   const int m1_bars_count,
   const DALLRuleNode &m1_nodes[],
   const int m1_nodes_count,
   const DALE0009HTF123State &htf123,
   const int trade_direction,
   const DALE0009Config &cfg,
   DALE0009HookSignal &out
)
{
   DAL_E0009_ResetHook(out);

   if(!htf123.valid)
   {
      out.reason = "htf_123_invalid";
      return false;
   }
   if(trade_direction == 0)
   {
      out.reason = "zero_trade_direction";
      return false;
   }

   DALLRuleNode hook;
   datetime after_time = (cfg.require_fresh_m1_hook_after_htf_close ? htf123.closed_time : 0);
   if(!DAL_E0009FindLatestHookForDirection(m1_nodes, m1_nodes_count, trade_direction, after_time,
                                           cfg.m1_max_hook_age_bars, m1_bars_count - 1, hook))
   {
      out.reason = "m1_hook_missing";
      return false;
   }

   double lower = 0.0, upper = 0.0;
   bool hunted = false;
   if(!DAL_E0009BuildNodeZoneLive(m1_bars, m1_bars_count, hook, cfg.zone_ratio, lower, upper, hunted))
   {
      out.reason = "hook_zone_failed";
      return false;
   }

   if(hunted)
   {
      out.reason = "hook_already_hunted";
      return false;
   }

   double spread = DAL_E0009SpreadPrice(symbol);
   out.direction = trade_direction;
   out.hook_node = hook;
   out.zone_lower = lower;
   out.zone_upper = upper;

   if(trade_direction > 0)
   {
      // BUY on a LOW hook.
      out.entry = upper + spread * MathMax(0.0, cfg.buy_entry_spread_mult);
      out.sl = hook.price;
   }
   else
   {
      // SELL on a HIGH hook.
      out.entry = lower;
      out.sl = hook.price + spread * MathMax(0.0, cfg.sell_stop_spread_mult);
   }

   int digits = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
   out.entry = NormalizeDouble(out.entry, digits);
   out.sl = NormalizeDouble(out.sl, digits);
   out.risk_distance = MathAbs(out.entry - out.sl);

   if(out.risk_distance <= 0.0)
   {
      out.reason = "zero_risk";
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
   else if(cfg.exit_mode == DAL_E0009_EXIT_HTF_POINT_2)
   {
      out.tp = NormalizeDouble(htf123.p2.price, digits);
      out.potential_r = MathAbs(out.tp - out.entry) / out.risk_distance;
   }
   else
   {
      out.tp = 0.0;
      out.potential_r = 0.0;
   }

   out.comment = "DALE9_123_" + IntegerToString((int)htf123.direction)
      + "_P3_" + IntegerToString(htf123.p3.id)
      + "_H_" + IntegerToString(hook.id);

   out.valid = true;
   out.reason = "ok";
   return true;
}

#endif
