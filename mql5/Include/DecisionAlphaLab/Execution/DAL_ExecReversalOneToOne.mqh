#ifndef __DAL_EXEC_REVERSAL_ONE_TO_ONE_MQH__
#define __DAL_EXEC_REVERSAL_ONE_TO_ONE_MQH__

// Decision Alpha Lab — E0001 reversal fixed-R execution setup builder.
// Execution is intentionally separated from hypotheses. It mirrors the H0005
// reversal fixed-reward test: LAST_ONLY reversal regime -> next structural
// zone touch -> zone-edge stop -> fixed-R take-profit.

#include <DecisionAlphaLab/M0001/DAL_M0001Engine.mqh>
#include <DecisionAlphaLab/M0002/DAL_M0002Reports.mqh>
#include <DecisionAlphaLab/M0005/DAL_M0005Reports.mqh>
#include <DecisionAlphaLab/Execution/DAL_ExecOrders.mqh>

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
   double stop_distance;
   double reward_r;
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
   s.stop_distance = 0.0;
   s.reward_r = 1.0;
   s.comment = "";
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


bool DAL_ExecBuildReversalOneToOneSetupFromNode(
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

   // H0005 reversal fixed-R test uses the reversal direction, the frozen
   // structural zone edge as entry proxy for live limits, and the far edge
   // of the same zone as the structural stop. The research report uses the
   // touch bar close as the measured entry; live execution cannot know that
   // close in advance, so the limit is parked exactly at the touch edge.
   if(node.type == DAL_NODE_LOW)
   {
      setup.direction = +1;
      setup.entry_price = upper;
      setup.stop_price = lower;
   }
   else
   {
      setup.direction = -1;
      setup.entry_price = lower;
      setup.stop_price = upper;
   }

   setup.stop_distance = MathAbs(setup.entry_price - setup.stop_price);
   if(setup.stop_distance <= 0.0)
   {
      setup.reason = "zero_stop_distance";
      return false;
   }

   setup.tp_price = setup.entry_price + setup.direction * setup.stop_distance * reward_r;
   setup.comment = comment_prefix
      + "_R" + DoubleToString(reward_r, 1)
      + "_node" + IntegerToString(setup.node_id)
      + "_last" + IntegerToString(setup.last_branch_sample_id);
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

   int scanned = 0;
   int current_index = bars_count - 1;
   for(int n = nodes_count - 1; n >= 0; n--)
   {
      DALLRuleNode node = nodes[n];
      if(!node.confirmed)
         continue;
      if(node.active_from_index < 0 || node.active_from_index > current_index)
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

      DALExecReversalSetup setup;
      if(!DAL_ExecBuildReversalOneToOneSetupFromNode(node, extreme, lower, upper, last_branch_sample, reward_r, comment_prefix, setup))
         continue;

      DAL_ExecAppendReversalSetup(setups, setup);
   }

   if(ArraySize(setups) <= 0)
   {
      reason = "no_active_h5_reversal_zone";
      return 0;
   }

   DAL_ExecSortReversalSetupsByMarketDistance(symbol, setups);
   reason = "ok";
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

   if(node.type == DAL_NODE_LOW)
   {
      setup.direction = +1;
      setup.entry_price = upper; // first touch edge from above
      setup.stop_price = lower;  // far edge / structural stop
   }
   else
   {
      setup.direction = -1;
      setup.entry_price = lower; // first touch edge from below
      setup.stop_price = upper;  // far edge / structural stop
   }

   setup.stop_distance = MathAbs(setup.entry_price - setup.stop_price);
   if(setup.stop_distance <= 0.0)
   {
      setup.reason = "zero_stop_distance";
      return false;
   }

   setup.tp_price = setup.entry_price + setup.direction * setup.stop_distance * reward_r;
   setup.comment = comment_prefix + "_node" + IntegerToString(setup.node_id) + "_last" + IntegerToString(setup.last_branch_sample_id);
   setup.valid = true;
   setup.reason = "ok";
   return true;
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
      + "*stopDistance=" + DoubleToString(s.stop_distance, 8)
      + "*comment=" + s.comment;
}

#endif
