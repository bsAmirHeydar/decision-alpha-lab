#ifndef __DAL_EXEC_REVERSAL_ONE_TO_ONE_MQH__
#define __DAL_EXEC_REVERSAL_ONE_TO_ONE_MQH__

// Decision Alpha Lab — E0001 reversal fixed-R execution setup builder.
// Execution is intentionally separated from hypotheses. It mirrors the H0005
// reversal fixed-reward test: LAST_ONLY reversal regime -> next structural
// zone touch -> far zone-edge stop -> fixed-R take-profit.
// Release 1.24 implements the per-candle live contract, strict touch/revisit ledger, and opposite-node TP policy:
//   - select the nearest LOW-node buy limits below market and nearest HIGH-node sell limits above market;
//   - buy limit at the first-touch upper zone edge plus current spread;
//   - buy stop at the far/lower zone edge;
//   - sell limit at the first-touch lower zone edge;
//   - sell stop at the far/upper zone edge plus current spread;
//   - TP defaults to the first opposite-node touch;
//   - optional fixed-R cap can close earlier only when it is closer than the opposite touch;
//   - optional sub-R filter can reject trades whose first opposite touch is below the configured R threshold;
//   - keep structural candidates in the cache even when the current tick is no
//     longer orderable, so the EA can detect and lock an already-started touch
//     episode instead of repeatedly planting limits inside the same touch;
//   - build an execution-matched H5 research report for directional memory and fixed-R reversal outcomes.

#include <M0001/DAL_M0001Engine.mqh>
#include <M0002/DAL_M0002Reports.mqh>
#include <M0005/DAL_M0005Reports.mqh>
#include <Execution/DAL_ExecOrders.mqh>

struct DALExecReversalSetup
{
   bool valid;
   string reason;
   int node_id;
   int node_index;
   int last_branch_sample_id;
   int last_branch_label;
   ENUM_DALNodeType node_type;
   int direction;
   datetime node_time;
   datetime active_from_time;
   double node_price;
   double live_extreme;
   double zone_lower;
   double zone_upper;
   double entry_price;
   double stop_price;
   double tp_price;
   double fixed_r_tp_price;
   double opposite_touch_tp_price;
   int opposite_touch_node_id;
   bool has_opposite_touch_tp;
   string tp_model;
   double opposite_touch_r;
   bool tp_rejected;
   string tp_reject_reason;
   double stop_distance;
   double reward_r;
   double spread_price;
   double raw_entry_edge;
   double raw_stop_edge;
   string comment;
};

void DAL_ExecResetReversalSetup(DALExecReversalSetup &s)
{
   s.valid = false;
   s.reason = "not_built";
   s.node_id = -1;
   s.node_index = -1;
   s.last_branch_sample_id = -1;
   s.last_branch_label = -1;
   s.node_type = DAL_NODE_LOW;
   s.direction = 0;
   s.node_time = 0;
   s.active_from_time = 0;
   s.node_price = 0.0;
   s.live_extreme = 0.0;
   s.zone_lower = 0.0;
   s.zone_upper = 0.0;
   s.entry_price = 0.0;
   s.stop_price = 0.0;
   s.tp_price = 0.0;
   s.fixed_r_tp_price = 0.0;
   s.opposite_touch_tp_price = 0.0;
   s.opposite_touch_node_id = -1;
   s.has_opposite_touch_tp = false;
   s.tp_model = "not_resolved";
   s.opposite_touch_r = 0.0;
   s.tp_rejected = false;
   s.tp_reject_reason = "";
   s.stop_distance = 0.0;
   s.reward_r = 1.0;
   s.spread_price = 0.0;
   s.raw_entry_edge = 0.0;
   s.raw_stop_edge = 0.0;
   s.comment = "";
}

struct DALExecH5FixedRReport
{
   int sample_count;
   int reversal_sample_count;
   int continuation_sample_count;
   int transition_count;
   int rev_to_rev;
   int rev_to_cont;
   int cont_to_rev;
   int cont_to_cont;
   int memory_hits;
   int planned_trades;
   int buy_planned;
   int sell_planned;
   int filled_trades;
   int unfilled_trades;
   int target_hits;
   int stop_hits;
   int ambiguous_hits;
   int open_after_fill;
   double sum_r_conservative;
   double gross_win_r;
   double gross_loss_r;
   int setup_reject_samples;
   int simulation_rejects;
};

void DAL_ExecResetH5FixedRReport(DALExecH5FixedRReport &r)
{
   r.sample_count = 0;
   r.reversal_sample_count = 0;
   r.continuation_sample_count = 0;
   r.transition_count = 0;
   r.rev_to_rev = 0;
   r.rev_to_cont = 0;
   r.cont_to_rev = 0;
   r.cont_to_cont = 0;
   r.memory_hits = 0;
   r.planned_trades = 0;
   r.buy_planned = 0;
   r.sell_planned = 0;
   r.filled_trades = 0;
   r.unfilled_trades = 0;
   r.target_hits = 0;
   r.stop_hits = 0;
   r.ambiguous_hits = 0;
   r.open_after_fill = 0;
   r.sum_r_conservative = 0.0;
   r.gross_win_r = 0.0;
   r.gross_loss_r = 0.0;
   r.setup_reject_samples = 0;
   r.simulation_rejects = 0;
}


bool DAL_ExecNodeHasEvent(const DALM0001Event &events[], const int events_count, const int node_id)
{
   for(int i = 0; i < events_count; i++)
   {
      if(events[i].node_id == node_id)
         return true;
   }
   return false;
}

bool DAL_ExecNodeTouchedOrConsumedBeforeNow(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &node,
   const double zone_ratio,
   double &last_extreme,
   double &last_lower,
   double &last_upper
)
{
   last_extreme = 0.0;
   last_lower = node.price;
   last_upper = node.price;

   if(bars_count <= 0 || node.active_from_index < 0 || node.active_from_index >= bars_count)
      return true;

   last_extreme = DAL_M0001InitialExtreme(node.type, bars[node.active_from_index]);

   for(int i = node.active_from_index; i < bars_count; i++)
   {
      last_extreme = DAL_M0001UpdateExtreme(node.type, last_extreme, bars[i]);
      DAL_M0001Territory(node.type, node.price, last_extreme, zone_ratio, last_lower, last_upper);

      bool touched_zone = DAL_CandleIntersectsZone(bars[i].low, bars[i].high, last_lower, last_upper);
      bool hunted_now = DAL_M0001Hunted(node.type, node.price, bars[i]);

      if(touched_zone)
         return true;

      if(hunted_now && !touched_zone)
         return true;
   }

   return false;
}

bool DAL_ExecBuildLiveNodeTerritory(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &node,
   const double zone_ratio,
   double &last_extreme,
   double &last_lower,
   double &last_upper,
   bool &hunted
)
{
   last_extreme = 0.0;
   last_lower = node.price;
   last_upper = node.price;
   hunted = false;

   if(bars_count <= 0 || node.active_from_index < 0 || node.active_from_index >= bars_count)
      return false;

   last_extreme = DAL_M0001InitialExtreme(node.type, bars[node.active_from_index]);
   for(int i = node.active_from_index; i < bars_count; i++)
   {
      last_extreme = DAL_M0001UpdateExtreme(node.type, last_extreme, bars[i]);
      DAL_M0001Territory(node.type, node.price, last_extreme, zone_ratio, last_lower, last_upper);

      if(DAL_M0001Hunted(node.type, node.price, bars[i]))
         hunted = true;
   }

   return true;
}

bool DAL_ExecSetupLimitOrderableNow(
   const string symbol,
   const DALExecReversalSetup &setup,
   string &reason
)
{
   double entry = setup.entry_price;
   double sl = setup.stop_price;
   double tp = setup.tp_price;
   DAL_ExecNormalizePrices(symbol, entry, sl, tp);
   return DAL_ExecCheckLimitGeometry(symbol, setup.direction, entry, sl, tp, reason);
}

bool DAL_ExecLatestBranchIsReversal(
   const DALM0002BranchSample &samples[],
   const int sample_count,
   int &last_sample_index
)
{
   last_sample_index = -1;
   if(sample_count <= 0)
      return false;

   for(int i = sample_count - 1; i >= 0; i--)
   {
      if(samples[i].outcome == DAL_M0002_OUTCOME_REVERSAL_AFTER_EXIT || samples[i].outcome == DAL_M0002_OUTCOME_CONTINUATION_AFTER_EXIT)
      {
         last_sample_index = i;
         return (samples[i].outcome == DAL_M0002_OUTCOME_REVERSAL_AFTER_EXIT);
      }
   }

   return false;
}

int DAL_ExecFindNewestUntouchedNodeAfterIndex(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const DALM0001Event &events[],
   const int events_count,
   const double zone_ratio,
   const int after_index,
   const int max_nodes_scan,
   double &out_extreme,
   double &out_lower,
   double &out_upper
)
{
   out_extreme = 0.0;
   out_lower = 0.0;
   out_upper = 0.0;

   int scanned = 0;
   for(int n = nodes_count - 1; n >= 0; n--)
   {
      DALLRuleNode node = nodes[n];
      if(!node.confirmed)
         continue;
      if(node.active_from_index <= after_index)
         continue;
      if(node.active_from_index < 0 || node.active_from_index >= bars_count)
         continue;

      scanned++;
      if(max_nodes_scan > 0 && scanned > max_nodes_scan)
         break;

      if(DAL_ExecNodeHasEvent(events, events_count, node.id))
         continue;

      double extreme = 0.0, lower = 0.0, upper = 0.0;
      bool already_touched_or_consumed = DAL_ExecNodeTouchedOrConsumedBeforeNow(bars, bars_count, node, zone_ratio, extreme, lower, upper);
      if(already_touched_or_consumed)
         continue;

      out_extreme = extreme;
      out_lower = lower;
      out_upper = upper;
      return n;
   }

   return -1;
}

bool DAL_ExecFindLatestBranchSampleFast(
   const DALM0001Event &events[],
   const int events_count,
   const DALBar &bars[],
   const int bars_count,
   const datetime min_entry_time,
   const DALM0002Config &config,
   DALM0002BranchSample &sample,
   int &event_index
)
{
   event_index = -1;
   int analysis_start_index = DAL_M0001FirstIndexAtOrAfter(bars, bars_count, min_entry_time);

   for(int i = events_count - 1; i >= 0; i--)
   {
      ENUM_DALM0002Outcome outcome = DAL_M0002_OUTCOME_UNKNOWN;
      DALM0002BranchSample candidate;
      bool ok = DAL_M0002BuildBranchSample(
         events[i],
         bars,
         bars_count,
         analysis_start_index,
         min_entry_time,
         config,
         events[i].id,
         candidate,
         outcome
      );

      if(!ok)
         continue;

      if(candidate.outcome == DAL_M0002_OUTCOME_REVERSAL_AFTER_EXIT || candidate.outcome == DAL_M0002_OUTCOME_CONTINUATION_AFTER_EXIT)
      {
         sample = candidate;
         event_index = i;
         return true;
      }
   }

   return false;
}



string DAL_ExecManagedCommentPrefix(const string comment_prefix)
{
   string prefix = comment_prefix;
   if(prefix == "")
      prefix = "DALR";

   // Broker order comments are often capped/truncated. Keep the managed
   // identity prefix short and use the same normalized prefix for both order
   // creation and later pending-order synchronization.
   if(StringLen(prefix) > 10)
      prefix = StringSubstr(prefix, 0, 10);
   return prefix;
}

string DAL_ExecBuildCompactSetupComment(
   const string comment_prefix,
   const double reward_r,
   const int node_id,
   const int direction
)
{
   string prefix = DAL_ExecManagedCommentPrefix(comment_prefix);
   string rr = "R" + IntegerToString((int)MathRound(reward_r * 10.0));
   string side = "S";
   if(direction > 0)
      side = "B";

   // Stable identity is essential for live order management:
   // one structural zone/touch = one comment = one pending/position ledger key.
   // Do not include the latest branch-sample id here; that id can change while
   // the same structural zone is still the active execution candidate, which
   // would make the engine delete/recreate orders instead of modifying them.
   string c = prefix + rr + side + "N" + IntegerToString(node_id);

   // Keep full setup identity inside common broker limits so duplicate
   // detection and pending sync do not break because of server-side truncation.
   if(StringLen(c) > 31)
      c = StringSubstr(c, 0, 31);
   return c;
}

double DAL_ExecCurrentSpreadPrice(const string symbol)
{
   double bid = SymbolInfoDouble(symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(symbol, SYMBOL_ASK);
   double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
   double spread = 0.0;

   if(bid > 0.0 && ask > 0.0 && ask >= bid)
      spread = ask - bid;

   if(spread <= 0.0 && point > 0.0)
   {
      long spread_points = SymbolInfoInteger(symbol, SYMBOL_SPREAD);
      if(spread_points > 0)
         spread = (double)spread_points * point;
   }

   if(spread < 0.0)
      spread = 0.0;
   return spread;
}

double DAL_ExecFixedRTpPrice(
   const int direction,
   const double entry_price,
   const double stop_price,
   const double reward_r
)
{
   double stop_distance = MathAbs(entry_price - stop_price);
   if(stop_distance <= 0.0 || reward_r <= 0.0 || direction == 0)
      return entry_price;
   return entry_price + direction * stop_distance * reward_r;
}

bool DAL_ExecPriceInProfitDirection(
   const int direction,
   const double entry_price,
   const double target_price
)
{
   if(direction > 0)
      return (target_price > entry_price);
   if(direction < 0)
      return (target_price < entry_price);
   return false;
}

double DAL_ExecTargetRMultiple(
   const int direction,
   const double entry_price,
   const double stop_price,
   const double target_price
)
{
   double risk = MathAbs(entry_price - stop_price);
   if(risk <= 0.0)
      return 0.0;
   if(!DAL_ExecPriceInProfitDirection(direction, entry_price, target_price))
      return 0.0;
   return MathAbs(target_price - entry_price) / risk;
}

bool DAL_ExecResolveOppositeNodeTouchTpPolicy(
   const int direction,
   const double entry_price,
   const double stop_price,
   const double reward_r,
   const bool has_opposite_touch,
   const double opposite_touch_tp,
   const bool use_fixed_r_exit_if_closer,
   const bool allow_opposite_touch_below_reward_r,
   double &resolved_tp,
   double &fixed_r_tp,
   double &opposite_touch_r,
   string &tp_model,
   string &reject_reason
)
{
   resolved_tp = 0.0;
   fixed_r_tp = DAL_ExecFixedRTpPrice(direction, entry_price, stop_price, reward_r);
   opposite_touch_r = 0.0;
   tp_model = "not_resolved";
   reject_reason = "";

   if(direction == 0)
   {
      reject_reason = "invalid_direction";
      return false;
   }
   if(reward_r <= 0.0)
   {
      reject_reason = "invalid_reward_r";
      return false;
   }
   if(!DAL_ExecPriceInProfitDirection(direction, entry_price, fixed_r_tp))
   {
      reject_reason = "invalid_fixed_r_reference";
      return false;
   }
   if(!has_opposite_touch)
   {
      reject_reason = "missing_opposite_node_touch_target";
      return false;
   }
   if(!DAL_ExecPriceInProfitDirection(direction, entry_price, opposite_touch_tp))
   {
      reject_reason = "opposite_touch_not_in_profit_path";
      return false;
   }

   double risk = MathAbs(entry_price - stop_price);
   double fixed_dist = MathAbs(fixed_r_tp - entry_price);
   double opposite_dist = MathAbs(opposite_touch_tp - entry_price);
   if(risk <= 0.0 || fixed_dist <= 0.0 || opposite_dist <= 0.0)
   {
      reject_reason = "invalid_tp_distance";
      return false;
   }

   opposite_touch_r = opposite_dist / risk;
   if(!allow_opposite_touch_below_reward_r && opposite_touch_r < reward_r)
   {
      reject_reason = "opposite_touch_below_reward_r";
      return false;
   }

   if(use_fixed_r_exit_if_closer && fixed_dist < opposite_dist)
   {
      resolved_tp = fixed_r_tp;
      tp_model = "fixed_r_exit_closer_than_opposite_touch";
      return true;
   }

   resolved_tp = opposite_touch_tp;
   if(use_fixed_r_exit_if_closer)
      tp_model = "first_opposite_node_touch_fixed_r_not_closer";
   else
      tp_model = "first_opposite_node_touch";
   return true;
}

bool DAL_ExecFindFirstOppositeNodeTouchTarget(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const double zone_ratio,
   const DALExecReversalSetup &setup,
   double &target_price,
   int &target_node_id,
   string &reason
)
{
   target_price = 0.0;
   target_node_id = -1;
   reason = "not_found";

   if(!setup.valid || setup.direction == 0)
   {
      reason = "invalid_setup";
      return false;
   }

   ENUM_DALNodeType wanted_type = (setup.direction > 0 ? DAL_NODE_HIGH : DAL_NODE_LOW);
   double best_distance = 0.0;
   bool found = false;
   int skipped_wrong_type = 0;
   int skipped_inactive = 0;
   int skipped_hunted = 0;
   int skipped_not_in_profit_path = 0;

   for(int n = nodes_count - 1; n >= 0; n--)
   {
      DALLRuleNode node = nodes[n];
      if(!node.confirmed)
         continue;
      if(node.id == setup.node_id)
         continue;
      if(node.type != wanted_type)
      {
         skipped_wrong_type++;
         continue;
      }
      if(node.active_from_index < 0 || node.active_from_index >= bars_count)
      {
         skipped_inactive++;
         continue;
      }

      double extreme = 0.0, lower = 0.0, upper = 0.0;
      bool hunted = false;
      if(!DAL_ExecBuildLiveNodeTerritory(bars, bars_count, node, zone_ratio, extreme, lower, upper, hunted))
      {
         skipped_inactive++;
         continue;
      }
      if(hunted)
      {
         skipped_hunted++;
         continue;
      }

      // Opposite touch edge:
      //   buy from LOW node -> first opposing HIGH-node touch is its lower edge;
      //   sell from HIGH node -> first opposing LOW-node touch is its upper edge.
      double candidate_touch = (setup.direction > 0 ? lower : upper);
      if(!DAL_ExecPriceInProfitDirection(setup.direction, setup.entry_price, candidate_touch))
      {
         skipped_not_in_profit_path++;
         continue;
      }

      double d = MathAbs(candidate_touch - setup.entry_price);
      if(d <= 0.0)
      {
         skipped_not_in_profit_path++;
         continue;
      }

      if(!found || d < best_distance)
      {
         found = true;
         best_distance = d;
         target_price = candidate_touch;
         target_node_id = node.id;
      }
   }

   if(!found)
   {
      reason = "no_opposite_touch_target"
         + "_wrongType_" + IntegerToString(skipped_wrong_type)
         + "_inactive_" + IntegerToString(skipped_inactive)
         + "_hunted_" + IntegerToString(skipped_hunted)
         + "_notInProfitPath_" + IntegerToString(skipped_not_in_profit_path);
      return false;
   }

   reason = "ok_opposite_node_" + IntegerToString(target_node_id);
   return true;
}

bool DAL_ExecApplyOppositeNodeTouchTpPolicy(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const double zone_ratio,
   const bool use_fixed_r_exit_if_closer,
   const bool allow_opposite_touch_below_reward_r,
   DALExecReversalSetup &setup
)
{
   setup.fixed_r_tp_price = DAL_ExecFixedRTpPrice(setup.direction, setup.entry_price, setup.stop_price, setup.reward_r);
   setup.tp_price = 0.0;
   setup.has_opposite_touch_tp = false;
   setup.opposite_touch_tp_price = 0.0;
   setup.opposite_touch_node_id = -1;
   setup.opposite_touch_r = 0.0;
   setup.tp_model = "opposite_touch_pending_resolution";
   setup.tp_rejected = false;
   setup.tp_reject_reason = "";

   double opposite_tp = 0.0;
   int opposite_node_id = -1;
   string target_reason = "";
   if(DAL_ExecFindFirstOppositeNodeTouchTarget(bars, bars_count, nodes, nodes_count, zone_ratio, setup, opposite_tp, opposite_node_id, target_reason))
   {
      setup.has_opposite_touch_tp = true;
      setup.opposite_touch_tp_price = opposite_tp;
      setup.opposite_touch_node_id = opposite_node_id;
   }

   double resolved_tp = 0.0;
   double fixed_r_tp = 0.0;
   double opposite_touch_r = 0.0;
   string model = "";
   string reject_reason = "";
   if(!DAL_ExecResolveOppositeNodeTouchTpPolicy(
      setup.direction,
      setup.entry_price,
      setup.stop_price,
      setup.reward_r,
      setup.has_opposite_touch_tp,
      setup.opposite_touch_tp_price,
      use_fixed_r_exit_if_closer,
      allow_opposite_touch_below_reward_r,
      resolved_tp,
      fixed_r_tp,
      opposite_touch_r,
      model,
      reject_reason
   ))
   {
      setup.tp_rejected = true;
      setup.tp_reject_reason = reject_reason;
      setup.tp_model = "tp_rejected_" + reject_reason;
      setup.reason = "tp_reject_" + reject_reason;
      setup.fixed_r_tp_price = fixed_r_tp;
      setup.opposite_touch_r = opposite_touch_r;
      setup.valid = false;
      return false;
   }

   setup.fixed_r_tp_price = fixed_r_tp;
   setup.opposite_touch_r = opposite_touch_r;
   setup.tp_price = resolved_tp;
   setup.tp_model = model;
   return true;
}

bool DAL_ExecResolveTpForActualEntry(
   const DALExecReversalSetup &setup,
   const double actual_entry_price,
   const bool use_fixed_r_exit_if_closer,
   const bool allow_opposite_touch_below_reward_r,
   double &resolved_tp,
   double &fixed_r_tp,
   double &opposite_touch_r,
   string &tp_model,
   string &reject_reason
)
{
   return DAL_ExecResolveOppositeNodeTouchTpPolicy(
      setup.direction,
      actual_entry_price,
      setup.stop_price,
      setup.reward_r,
      setup.has_opposite_touch_tp,
      setup.opposite_touch_tp_price,
      use_fixed_r_exit_if_closer,
      allow_opposite_touch_below_reward_r,
      resolved_tp,
      fixed_r_tp,
      opposite_touch_r,
      tp_model,
      reject_reason
   );
}


bool DAL_ExecBuildReversalOneToOneSetupFromNode(
   const string symbol,
   const DALLRuleNode &node,
   const double extreme,
   const double lower,
   const double upper,
   const DALM0002BranchSample &last_branch_sample,
   const double reward_r,
   const string comment_prefix,
   DALExecReversalSetup &setup
)
{
   DAL_ExecResetReversalSetup(setup);
   setup.reward_r = reward_r;

   if(reward_r <= 0.0)
   {
      setup.reason = "invalid_reward_r";
      return false;
   }

   setup.last_branch_sample_id = last_branch_sample.id;
   setup.last_branch_label = DAL_M0004_LABEL_REVERSAL;
   setup.node_id = node.id;
   setup.node_index = node.index;
   setup.node_type = node.type;
   setup.node_time = node.time;
   setup.active_from_time = node.active_from_time;
   setup.node_price = node.price;
   setup.live_extreme = extreme;
   setup.zone_lower = lower;
   setup.zone_upper = upper;

   double spread = DAL_ExecCurrentSpreadPrice(symbol);
   setup.spread_price = spread;

   // Exact live H0005 reversal touch model:
   // - A LOW node is a demand/support revisit. The first-touch edge is the
   //   upper edge of the live zone; a buy opens on Ask, therefore the buy limit
   //   is parked one current spread above that Bid-side structural touch edge.
   //   The stop remains the far/lower structural edge.
   // - A HIGH node is a supply/resistance revisit. The first-touch edge is the
   //   lower edge of the live zone; a sell opens on Bid, so the sell limit stays
   //   at that edge. The stop closes on Ask, therefore it is moved one current
   //   spread above the far/upper structural edge.
   if(node.type == DAL_NODE_LOW)
   {
      setup.direction = +1;
      setup.raw_entry_edge = upper;
      setup.raw_stop_edge = lower;
      setup.entry_price = upper + spread;
      setup.stop_price = lower;
   }
   else
   {
      setup.direction = -1;
      setup.raw_entry_edge = lower;
      setup.raw_stop_edge = upper;
      setup.entry_price = lower;
      setup.stop_price = upper + spread;
   }

   setup.stop_distance = MathAbs(setup.entry_price - setup.stop_price);
   if(setup.stop_distance <= 0.0)
   {
      setup.reason = "zero_spread_adjusted_stop_distance";
      return false;
   }

   // The setup builder only establishes entry/stop/risk. The collector applies
   // the structural TP policy after all nodes are visible: default TP is the first
   // opposite-node touch, with optional fixed-R early exit / sub-R rejection.
   setup.fixed_r_tp_price = DAL_ExecFixedRTpPrice(setup.direction, setup.entry_price, setup.stop_price, reward_r);
   setup.tp_price = 0.0;
   setup.tp_model = "opposite_touch_pending_resolution";
   setup.comment = DAL_ExecBuildCompactSetupComment(comment_prefix, reward_r, setup.node_id, setup.direction);
   setup.valid = true;
   setup.reason = "ok";
   return true;
}

void DAL_ExecAppendReversalSetup(DALExecReversalSetup &setups[], const DALExecReversalSetup &setup)
{
   int n = ArraySize(setups);
   ArrayResize(setups, n + 1);
   setups[n] = setup;
}

void DAL_ExecSortReversalSetupsByMarketDistance(const string symbol, DALExecReversalSetup &setups[])
{
   int n = ArraySize(setups);
   for(int i = 0; i < n - 1; i++)
   {
      int best = i;
      double best_d = DAL_ExecPendingDistanceToMarket(symbol, setups[i].direction, setups[i].entry_price);
      for(int j = i + 1; j < n; j++)
      {
         double d = DAL_ExecPendingDistanceToMarket(symbol, setups[j].direction, setups[j].entry_price);
         if(d < best_d)
         {
            best = j;
            best_d = d;
         }
      }
      if(best != i)
      {
         DALExecReversalSetup tmp = setups[i];
         setups[i] = setups[best];
         setups[best] = tmp;
      }
   }
}

int DAL_ExecCollectH5ReversalRSetups(
   const string symbol,
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const DALM0001Event &events[],
   const int events_count,
   const DALM0002BranchSample &last_branch_sample,
   const bool has_last_branch_sample,
   const double zone_ratio,
   const double reward_r,
   const string comment_prefix,
   const bool use_fixed_r_exit_if_closer,
   const bool allow_opposite_touch_below_reward_r,
   const int buy_limit_slots,
   const int sell_limit_slots,
   const int max_nodes_scan,
   DALExecReversalSetup &setups[],
   string &reason
)
{
   ArrayResize(setups, 0);
   reason = "not_built";

   if(bars_count <= 0)
   {
      reason = "no_bars";
      return 0;
   }
   if(nodes_count <= 0)
   {
      reason = "no_nodes";
      return 0;
   }
   if(!has_last_branch_sample)
   {
      reason = "no_last_branch";
      return 0;
   }
   if(last_branch_sample.outcome != DAL_M0002_OUTCOME_REVERSAL_AFTER_EXIT)
   {
      reason = "last_regime_not_reversal";
      return 0;
   }
   if(reward_r <= 0.0)
   {
      reason = "invalid_reward_r";
      return 0;
   }

   int buy_slots = (int)MathMax(0.0, (double)buy_limit_slots);
   int sell_slots = (int)MathMax(0.0, (double)sell_limit_slots);
   bool buy_unlimited = (buy_slots <= 0);
   bool sell_unlimited = (sell_slots <= 0);

   DALExecReversalSetup all_setups[];
   ArrayResize(all_setups, 0);

   int scanned = 0;
   int skipped_unconfirmed = 0;
   int skipped_not_active = 0;
   int skipped_hunted = 0;
   int skipped_build = 0;
   int current_index = bars_count - 1;
   for(int n = nodes_count - 1; n >= 0; n--)
   {
      DALLRuleNode node = nodes[n];
      if(!node.confirmed)
      {
         skipped_unconfirmed++;
         continue;
      }
      if(node.active_from_index < 0 || node.active_from_index > current_index)
      {
         skipped_not_active++;
         continue;
      }

      scanned++;
      if(max_nodes_scan > 0 && scanned > max_nodes_scan)
         break;

      double extreme = 0.0, lower = 0.0, upper = 0.0;
      bool hunted = false;
      if(!DAL_ExecBuildLiveNodeTerritory(bars, bars_count, node, zone_ratio, extreme, lower, upper, hunted))
      {
         skipped_not_active++;
         continue;
      }

      // Touches are allowed to become future revisits in the live executor, so
      // a historical M0001 touch/event must not remove the zone forever. A true
      // hunt/structural invalidation still retires the node from the limit grid.
      if(hunted)
      {
         skipped_hunted++;
         continue;
      }

      DALExecReversalSetup setup;
      if(!DAL_ExecBuildReversalOneToOneSetupFromNode(symbol, node, extreme, lower, upper, last_branch_sample, reward_r, comment_prefix, setup))
      {
         skipped_build++;
         continue;
      }

      if(!DAL_ExecApplyOppositeNodeTouchTpPolicy(bars, bars_count, nodes, nodes_count, zone_ratio, use_fixed_r_exit_if_closer, allow_opposite_touch_below_reward_r, setup))
      {
         skipped_build++;
         continue;
      }

      // Keep the structural setup even if the current tick is already too close
      // for a fresh limit. Orderability belongs to the send/modify layer. The EA
      // must still see this setup so it can mark the current touch episode as
      // consumed and avoid re-planting another limit until a true exit/revisit.
      DAL_ExecAppendReversalSetup(all_setups, setup);
   }

   if(ArraySize(all_setups) <= 0)
   {
      reason = "no_active_h5_reversal_zone"
         + "_scanned_" + IntegerToString(scanned)
         + "_hunted_" + IntegerToString(skipped_hunted)
         + "_inactive_" + IntegerToString(skipped_not_active)
         + "_unconfirmed_" + IntegerToString(skipped_unconfirmed)
         + "_buildReject_" + IntegerToString(skipped_build);
      return 0;
   }

   DAL_ExecSortReversalSetupsByMarketDistance(symbol, all_setups);

   int buy_count = 0;
   int sell_count = 0;
   for(int i = 0; i < ArraySize(all_setups); i++)
   {
      if(all_setups[i].direction > 0)
      {
         if(!buy_unlimited && buy_count >= buy_slots)
            continue;
         DAL_ExecAppendReversalSetup(setups, all_setups[i]);
         buy_count++;
      }
      else if(all_setups[i].direction < 0)
      {
         if(!sell_unlimited && sell_count >= sell_slots)
            continue;
         DAL_ExecAppendReversalSetup(setups, all_setups[i]);
         sell_count++;
      }
   }

   if(ArraySize(setups) <= 0)
   {
      reason = "no_active_h5_reversal_zone_in_directional_slots";
      return 0;
   }

   reason = "ok_buy_" + IntegerToString(buy_count)
      + "_sell_" + IntegerToString(sell_count)
      + "_all_" + IntegerToString(ArraySize(all_setups))
      + "_scanned_" + IntegerToString(scanned)
      + "_hunted_" + IntegerToString(skipped_hunted)
      + "_inactive_" + IntegerToString(skipped_not_active)
      + "_unconfirmed_" + IntegerToString(skipped_unconfirmed)
      + "_buildReject_" + IntegerToString(skipped_build)
      + "_buySlots_" + (buy_unlimited ? "ALL" : IntegerToString(buy_slots))
      + "_sellSlots_" + (sell_unlimited ? "ALL" : IntegerToString(sell_slots));
   return ArraySize(setups);
}

bool DAL_ExecBuildReversalOneToOneSetup(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const DALM0001Event &events[],
   const int events_count,
   const DALM0002BranchSample &last_branch_sample,
   const bool has_last_branch_sample,
   const double zone_ratio,
   const double reward_r,
   const string comment_prefix,
   const int max_nodes_scan,
   DALExecReversalSetup &setup
)
{
   DAL_ExecResetReversalSetup(setup);
   setup.reward_r = reward_r;

   if(bars_count <= 0)
   {
      setup.reason = "no_bars";
      return false;
   }
   if(nodes_count <= 0)
   {
      setup.reason = "no_nodes";
      return false;
   }
   if(!has_last_branch_sample)
   {
      setup.reason = "no_last_branch";
      return false;
   }
   if(reward_r <= 0.0)
   {
      setup.reason = "invalid_reward_r";
      return false;
   }

   bool last_is_reversal = (last_branch_sample.outcome == DAL_M0002_OUTCOME_REVERSAL_AFTER_EXIT);
   setup.last_branch_sample_id = last_branch_sample.id;
   setup.last_branch_label = last_is_reversal ? DAL_M0004_LABEL_REVERSAL : DAL_M0004_LABEL_CONTINUATION;

   if(!last_is_reversal)
   {
      setup.reason = "last_regime_not_reversal";
      return false;
   }

   double extreme = 0.0, lower = 0.0, upper = 0.0;
   int node_i = DAL_ExecFindNewestUntouchedNodeAfterIndex(
      bars,
      bars_count,
      nodes,
      nodes_count,
      events,
      events_count,
      zone_ratio,
      last_branch_sample.outcome_index,
      max_nodes_scan,
      extreme,
      lower,
      upper
   );

   if(node_i < 0)
   {
      setup.reason = "no_eligible_future_zone";
      return false;
   }

   DALLRuleNode node = nodes[node_i];
   setup.node_id = node.id;
   setup.node_index = node.index;
   setup.node_type = node.type;
   setup.node_time = node.time;
   setup.active_from_time = node.active_from_time;
   setup.node_price = node.price;
   setup.live_extreme = extreme;
   setup.zone_lower = lower;
   setup.zone_upper = upper;

   double spread = DAL_ExecCurrentSpreadPrice(_Symbol);
   setup.spread_price = spread;

   if(node.type == DAL_NODE_LOW)
   {
      setup.direction = +1;
      setup.raw_entry_edge = upper;
      setup.raw_stop_edge = lower;
      setup.entry_price = upper + spread;
      setup.stop_price = lower;
   }
   else
   {
      setup.direction = -1;
      setup.raw_entry_edge = lower;
      setup.raw_stop_edge = upper;
      setup.entry_price = lower;
      setup.stop_price = upper + spread;
   }

   setup.stop_distance = MathAbs(setup.entry_price - setup.stop_price);
   if(setup.stop_distance <= 0.0)
   {
      setup.reason = "zero_spread_adjusted_stop_distance";
      return false;
   }

   setup.fixed_r_tp_price = DAL_ExecFixedRTpPrice(setup.direction, setup.entry_price, setup.stop_price, reward_r);
   setup.tp_price = 0.0;
   setup.tp_model = "opposite_touch_pending_resolution";
   setup.comment = DAL_ExecBuildCompactSetupComment(comment_prefix, reward_r, setup.node_id, setup.direction);
   setup.valid = true;
   if(!DAL_ExecApplyOppositeNodeTouchTpPolicy(bars, bars_count, nodes, nodes_count, zone_ratio, false, true, setup))
      return false;
   setup.reason = "ok";
   return true;
}


bool DAL_ExecM0002OutcomeMeasured(const ENUM_DALM0002Outcome outcome)
{
   return (outcome == DAL_M0002_OUTCOME_REVERSAL_AFTER_EXIT || outcome == DAL_M0002_OUTCOME_CONTINUATION_AFTER_EXIT);
}

int DAL_ExecOutcomeDirectionCode(const ENUM_DALM0002Outcome outcome)
{
   if(outcome == DAL_M0002_OUTCOME_REVERSAL_AFTER_EXIT)
      return 1;
   if(outcome == DAL_M0002_OUTCOME_CONTINUATION_AFTER_EXIT)
      return -1;
   return 0;
}

void DAL_ExecAppendBranchSample(DALM0002BranchSample &samples[], const DALM0002BranchSample &sample, const int max_samples)
{
   int n = ArraySize(samples);
   if(max_samples > 0 && n >= max_samples)
   {
      for(int i = 1; i < n; i++)
         samples[i - 1] = samples[i];
      samples[n - 1] = sample;
      return;
   }

   ArrayResize(samples, n + 1);
   samples[n] = sample;
}

string DAL_ExecPctString(const int numerator, const int denominator)
{
   if(denominator <= 0)
      return "NA";
   return DoubleToString(100.0 * (double)numerator / (double)denominator, 2);
}

string DAL_ExecDoubleRatioString(const double numerator, const double denominator)
{
   if(denominator <= 0.0)
      return "NA";
   return DoubleToString(numerator / denominator, 4);
}

void DAL_ExecSortReversalSetupsByReferencePrice(const double reference_price, DALExecReversalSetup &setups[])
{
   int n = ArraySize(setups);
   for(int i = 0; i < n - 1; i++)
   {
      int best = i;
      double best_d = MathAbs(setups[i].entry_price - reference_price);
      for(int j = i + 1; j < n; j++)
      {
         double d = MathAbs(setups[j].entry_price - reference_price);
         if(d < best_d)
         {
            best = j;
            best_d = d;
         }
      }
      if(best != i)
      {
         DALExecReversalSetup tmp = setups[i];
         setups[i] = setups[best];
         setups[best] = tmp;
      }
   }
}

int DAL_ExecCollectH5ReversalRSetupsForReport(
   const string symbol,
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const DALM0001Event &events[],
   const int events_count,
   const DALM0002BranchSample &last_branch_sample,
   const bool has_last_branch_sample,
   const double zone_ratio,
   const double reward_r,
   const string comment_prefix,
   const bool use_fixed_r_exit_if_closer,
   const bool allow_opposite_touch_below_reward_r,
   const int buy_limit_slots,
   const int sell_limit_slots,
   const int max_nodes_scan,
   DALExecReversalSetup &setups[],
   string &reason
)
{
   ArrayResize(setups, 0);
   reason = "not_built";

   if(bars_count <= 0)
   {
      reason = "no_bars";
      return 0;
   }
   if(nodes_count <= 0)
   {
      reason = "no_nodes";
      return 0;
   }
   if(!has_last_branch_sample)
   {
      reason = "no_last_branch";
      return 0;
   }
   if(last_branch_sample.outcome != DAL_M0002_OUTCOME_REVERSAL_AFTER_EXIT)
   {
      reason = "last_regime_not_reversal";
      return 0;
   }
   if(reward_r <= 0.0)
   {
      reason = "invalid_reward_r";
      return 0;
   }

   int current_index = bars_count - 1;
   if(current_index < 0)
   {
      reason = "invalid_current_index";
      return 0;
   }

   double reference_price = (bars[current_index].high + bars[current_index].low) * 0.5;
   int buy_slots = (int)MathMax(0.0, (double)buy_limit_slots);
   int sell_slots = (int)MathMax(0.0, (double)sell_limit_slots);
   bool buy_unlimited = (buy_slots <= 0);
   bool sell_unlimited = (sell_slots <= 0);

   DALExecReversalSetup all_setups[];
   ArrayResize(all_setups, 0);

   int scanned = 0;
   int skipped_hunted = 0;
   int skipped_build = 0;
   int skipped_wrong_side = 0;
   int skipped_inactive = 0;

   for(int n = nodes_count - 1; n >= 0; n--)
   {
      DALLRuleNode node = nodes[n];
      if(!node.confirmed)
         continue;
      if(node.active_from_index < 0 || node.active_from_index > current_index)
      {
         skipped_inactive++;
         continue;
      }

      scanned++;
      if(max_nodes_scan > 0 && scanned > max_nodes_scan)
         break;

      double extreme = 0.0, lower = 0.0, upper = 0.0;
      bool hunted = false;
      if(!DAL_ExecBuildLiveNodeTerritory(bars, bars_count, node, zone_ratio, extreme, lower, upper, hunted))
      {
         skipped_inactive++;
         continue;
      }
      if(hunted)
      {
         skipped_hunted++;
         continue;
      }

      DALExecReversalSetup setup;
      if(!DAL_ExecBuildReversalOneToOneSetupFromNode(symbol, node, extreme, lower, upper, last_branch_sample, reward_r, comment_prefix, setup))
      {
         skipped_build++;
         continue;
      }

      if(!DAL_ExecApplyOppositeNodeTouchTpPolicy(bars, bars_count, nodes, nodes_count, zone_ratio, use_fixed_r_exit_if_closer, allow_opposite_touch_below_reward_r, setup))
      {
         skipped_build++;
         continue;
      }

      // Historical report mirrors the per-candle execution contract: only nearby
      // valleys below the closed-bar reference price and nearby peaks above it.
      if(setup.direction > 0 && !(setup.entry_price < reference_price))
      {
         skipped_wrong_side++;
         continue;
      }
      if(setup.direction < 0 && !(setup.entry_price > reference_price))
      {
         skipped_wrong_side++;
         continue;
      }

      DAL_ExecAppendReversalSetup(all_setups, setup);
   }

   if(ArraySize(all_setups) <= 0)
   {
      reason = "no_report_setups_scanned_" + IntegerToString(scanned)
         + "_hunted_" + IntegerToString(skipped_hunted)
         + "_inactive_" + IntegerToString(skipped_inactive)
         + "_wrongSide_" + IntegerToString(skipped_wrong_side)
         + "_buildReject_" + IntegerToString(skipped_build);
      return 0;
   }

   DAL_ExecSortReversalSetupsByReferencePrice(reference_price, all_setups);

   int buy_count = 0;
   int sell_count = 0;
   for(int i = 0; i < ArraySize(all_setups); i++)
   {
      if(all_setups[i].direction > 0)
      {
         if(!buy_unlimited && buy_count >= buy_slots)
            continue;
         DAL_ExecAppendReversalSetup(setups, all_setups[i]);
         buy_count++;
      }
      else if(all_setups[i].direction < 0)
      {
         if(!sell_unlimited && sell_count >= sell_slots)
            continue;
         DAL_ExecAppendReversalSetup(setups, all_setups[i]);
         sell_count++;
      }
   }

   reason = "ok_report_buy_" + IntegerToString(buy_count)
      + "_sell_" + IntegerToString(sell_count)
      + "_all_" + IntegerToString(ArraySize(all_setups))
      + "_ref_" + DoubleToString(reference_price, 8)
      + "_wrongSide_" + IntegerToString(skipped_wrong_side);
   return ArraySize(setups);
}

int DAL_ExecSimulateH5PendingFixedR(
   const DALBar &bars[],
   const int bars_count,
   const int start_index,
   const DALExecReversalSetup &setup,
   const int max_bars_after_entry,
   int &fill_index,
   int &exit_index,
   double &r_result,
   string &path
)
{
   fill_index = -1;
   exit_index = -1;
   r_result = 0.0;
   path = "not_started";

   if(start_index < 0 || start_index >= bars_count)
   {
      path = "invalid_start_index";
      return -99;
   }
   if(!setup.valid || setup.direction == 0 || setup.stop_distance <= 0.0)
   {
      path = "invalid_setup";
      return -98;
   }

   int last_index = bars_count - 1;
   if(max_bars_after_entry > 0)
   {
      int capped_last = start_index + max_bars_after_entry - 1;
      if(capped_last < last_index)
         last_index = capped_last;
   }

   bool filled = false;
   for(int i = start_index; i <= last_index; i++)
   {
      if(!filled)
      {
         if(setup.direction > 0)
         {
            if(bars[i].low <= setup.entry_price)
            {
               filled = true;
               fill_index = i;
            }
         }
         else
         {
            if(bars[i].high >= setup.entry_price)
            {
               filled = true;
               fill_index = i;
            }
         }

         if(!filled)
            continue;
      }

      bool hit_stop = false;
      bool hit_target = false;
      if(setup.direction > 0)
      {
         hit_stop = (bars[i].low <= setup.stop_price);
         hit_target = (bars[i].high >= setup.tp_price);
      }
      else
      {
         hit_stop = (bars[i].high >= setup.stop_price);
         hit_target = (bars[i].low <= setup.tp_price);
      }

      if(hit_stop && hit_target)
      {
         exit_index = i;
         r_result = -1.0;
         path = "ambiguous_same_bar_stop_and_target_conservative_stop";
         return -2;
      }
      if(hit_target)
      {
         exit_index = i;
         r_result = setup.reward_r;
         path = "target_first";
         return 1;
      }
      if(hit_stop)
      {
         exit_index = i;
         r_result = -1.0;
         path = "stop_first";
         return -1;
      }
   }

   if(filled)
   {
      path = "open_after_fill";
      return 2;
   }

   path = "unfilled";
   return 0;
}

bool DAL_ExecBuildH5ReversalFixedRResearchReport(
   const string symbol,
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const DALM0001Event &events[],
   const int events_count,
   const DALM0002Config &config,
   const double zone_ratio,
   const double reward_r,
   const string comment_prefix,
   const bool use_fixed_r_exit_if_closer,
   const bool allow_opposite_touch_below_reward_r,
   const int buy_limit_slots,
   const int sell_limit_slots,
   const int max_nodes_scan,
   const int max_samples,
   const int max_bars_after_entry,
   DALExecH5FixedRReport &report,
   string &reason
)
{
   DAL_ExecResetH5FixedRReport(report);
   reason = "not_built";

   if(bars_count <= 0 || events_count <= 0 || nodes_count <= 0)
   {
      reason = "missing_bars_nodes_or_events";
      return false;
   }

   DALM0002BranchSample samples[];
   ArrayResize(samples, 0);
   int analysis_start_index = 0;
   datetime min_entry_time = 0;
   int max_keep = max_samples;
   if(max_keep < 0)
      max_keep = 0;

   for(int i = 0; i < events_count; i++)
   {
      ENUM_DALM0002Outcome outcome = DAL_M0002_OUTCOME_UNKNOWN;
      DALM0002BranchSample candidate;
      bool ok = DAL_M0002BuildBranchSample(
         events[i],
         bars,
         bars_count,
         analysis_start_index,
         min_entry_time,
         config,
         events[i].id,
         candidate,
         outcome
      );
      if(!ok)
         continue;
      if(!DAL_ExecM0002OutcomeMeasured(candidate.outcome))
         continue;
      DAL_ExecAppendBranchSample(samples, candidate, max_keep);
   }

   report.sample_count = ArraySize(samples);
   if(report.sample_count <= 0)
   {
      reason = "no_measured_m0002_samples";
      return false;
   }

   for(int i = 0; i < report.sample_count; i++)
   {
      int code = DAL_ExecOutcomeDirectionCode(samples[i].outcome);
      if(code > 0)
         report.reversal_sample_count++;
      else if(code < 0)
         report.continuation_sample_count++;

      if(i > 0)
      {
         int prev = DAL_ExecOutcomeDirectionCode(samples[i - 1].outcome);
         int curr = code;
         if(prev != 0 && curr != 0)
         {
            report.transition_count++;
            if(prev == curr)
               report.memory_hits++;
            if(prev > 0 && curr > 0)
               report.rev_to_rev++;
            else if(prev > 0 && curr < 0)
               report.rev_to_cont++;
            else if(prev < 0 && curr > 0)
               report.cont_to_rev++;
            else if(prev < 0 && curr < 0)
               report.cont_to_cont++;
         }
      }
   }

   for(int s = 0; s < report.sample_count; s++)
   {
      if(samples[s].outcome != DAL_M0002_OUTCOME_REVERSAL_AFTER_EXIT)
         continue;

      int setup_bars_count = samples[s].outcome_index + 1;
      if(setup_bars_count <= 0 || setup_bars_count >= bars_count)
      {
         report.setup_reject_samples++;
         continue;
      }

      DALExecReversalSetup setups[];
      string setup_reason = "";
      int setup_count = DAL_ExecCollectH5ReversalRSetupsForReport(
         symbol,
         bars,
         setup_bars_count,
         nodes,
         nodes_count,
         events,
         events_count,
         samples[s],
         true,
         zone_ratio,
         reward_r,
         comment_prefix,
         use_fixed_r_exit_if_closer,
         allow_opposite_touch_below_reward_r,
         buy_limit_slots,
         sell_limit_slots,
         max_nodes_scan,
         setups,
         setup_reason
      );

      if(setup_count <= 0)
      {
         report.setup_reject_samples++;
         continue;
      }

      int start_index = setup_bars_count;
      for(int j = 0; j < setup_count; j++)
      {
         report.planned_trades++;
         if(setups[j].direction > 0)
            report.buy_planned++;
         else if(setups[j].direction < 0)
            report.sell_planned++;

         int fill_i = -1, exit_i = -1;
         double r = 0.0;
         string path = "";
         int result = DAL_ExecSimulateH5PendingFixedR(bars, bars_count, start_index, setups[j], max_bars_after_entry, fill_i, exit_i, r, path);
         if(result == 1)
         {
            report.filled_trades++;
            report.target_hits++;
            report.sum_r_conservative += r;
            report.gross_win_r += r;
         }
         else if(result == -1)
         {
            report.filled_trades++;
            report.stop_hits++;
            report.sum_r_conservative += -1.0;
            report.gross_loss_r += 1.0;
         }
         else if(result == -2)
         {
            report.filled_trades++;
            report.ambiguous_hits++;
            report.sum_r_conservative += -1.0;
            report.gross_loss_r += 1.0;
         }
         else if(result == 2)
         {
            report.filled_trades++;
            report.open_after_fill++;
         }
         else if(result == 0)
         {
            report.unfilled_trades++;
         }
         else
         {
            report.simulation_rejects++;
         }
      }
   }

   reason = "ok";
   return true;
}

string DAL_ExecH5FixedRReportToLog(const DALExecH5FixedRReport &r)
{
   int rev_transitions = r.rev_to_rev + r.rev_to_cont;
   int cont_transitions = r.cont_to_rev + r.cont_to_cont;
   string pf = DAL_ExecDoubleRatioString(r.gross_win_r, r.gross_loss_r);
   string expectancy = "NA";
   if(r.filled_trades > 0)
      expectancy = DoubleToString(r.sum_r_conservative / (double)r.filled_trades, 4);

   return "h5Report=FIXED_R_REVERSAL_EXECUTION_MATCHED"
      + "*samples=" + IntegerToString(r.sample_count)
      + "*reversalSamples=" + IntegerToString(r.reversal_sample_count)
      + "*continuationSamples=" + IntegerToString(r.continuation_sample_count)
      + "*transitions=" + IntegerToString(r.transition_count)
      + "*directionMemoryHitPct=" + DAL_ExecPctString(r.memory_hits, r.transition_count)
      + "*memoryVsRandomEdgePct=" + (r.transition_count > 0 ? DoubleToString((100.0 * (double)r.memory_hits / (double)r.transition_count) - 50.0, 2) : "NA")
      + "*revToRev=" + IntegerToString(r.rev_to_rev)
      + "*revToCont=" + IntegerToString(r.rev_to_cont)
      + "*pRevAfterRevPct=" + DAL_ExecPctString(r.rev_to_rev, rev_transitions)
      + "*contToCont=" + IntegerToString(r.cont_to_cont)
      + "*contToRev=" + IntegerToString(r.cont_to_rev)
      + "*pContAfterContPct=" + DAL_ExecPctString(r.cont_to_cont, cont_transitions)
      + "*plannedTrades=" + IntegerToString(r.planned_trades)
      + "*buyPlanned=" + IntegerToString(r.buy_planned)
      + "*sellPlanned=" + IntegerToString(r.sell_planned)
      + "*filledTrades=" + IntegerToString(r.filled_trades)
      + "*unfilledTrades=" + IntegerToString(r.unfilled_trades)
      + "*fillRatePct=" + DAL_ExecPctString(r.filled_trades, r.planned_trades)
      + "*targetHits=" + IntegerToString(r.target_hits)
      + "*stopHits=" + IntegerToString(r.stop_hits)
      + "*ambiguousSameBar=" + IntegerToString(r.ambiguous_hits)
      + "*openAfterFill=" + IntegerToString(r.open_after_fill)
      + "*targetHitPctFilled=" + DAL_ExecPctString(r.target_hits, r.filled_trades)
      + "*targetHitPctPlanned=" + DAL_ExecPctString(r.target_hits, r.planned_trades)
      + "*expectancyRConservative=" + expectancy
      + "*profitFactorRConservative=" + pf
      + "*sumRConservative=" + DoubleToString(r.sum_r_conservative, 4)
      + "*setupRejectSamples=" + IntegerToString(r.setup_reject_samples)
      + "*simulationRejects=" + IntegerToString(r.simulation_rejects);
}

string DAL_ExecReversalSetupToLog(const DALExecReversalSetup &s)
{
   return "setupOk=" + DAL_BoolToString(s.valid)
      + "*setupReason=" + s.reason
      + "*nodeId=" + IntegerToString(s.node_id)
      + "*nodeType=" + DAL_NodeTypeToString(s.node_type)
      + "*direction=" + IntegerToString(s.direction)
      + "*lastBranchSampleId=" + IntegerToString(s.last_branch_sample_id)
      + "*entry=" + DoubleToString(s.entry_price, 8)
      + "*stop=" + DoubleToString(s.stop_price, 8)
      + "*tp=" + DoubleToString(s.tp_price, 8)
      + "*rewardR=" + DoubleToString(s.reward_r, 4)
      + "*zoneLower=" + DoubleToString(s.zone_lower, 8)
      + "*zoneUpper=" + DoubleToString(s.zone_upper, 8)
      + "*rawEntryEdge=" + DoubleToString(s.raw_entry_edge, 8)
      + "*rawStopEdge=" + DoubleToString(s.raw_stop_edge, 8)
      + "*spread=" + DoubleToString(s.spread_price, 8)
      + "*stopDistance=" + DoubleToString(s.stop_distance, 8)
      + "*comment=" + s.comment;
}

#endif
