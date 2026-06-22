//+------------------------------------------------------------------+
//| Decision Alpha Lab — E0006 All-Zone Touch Limit Executor          |
//| Places one limit order per live M0001 structural zone.            |
//+------------------------------------------------------------------+
#property strict
#property version   "1.10"
#property description "Execution module E0006: all M0001 zones with revisit secondary-node entry and three stop-anchor modes."

#include <Trade/Trade.mqh>
#include <DecisionAlphaLab/Market/DAL_Bars.mqh>
#include <DecisionAlphaLab/StructuralNodes/DAL_StructuralNodeEngine.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Config.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Engine.mqh>
#include <DecisionAlphaLab/Execution/DAL_ExecRisk.mqh>
#include <DecisionAlphaLab/Execution/DAL_ExecOrders.mqh>
#include <DecisionAlphaLab/Execution/DAL_ExecReversalOneToOne.mqh>

// Revisit entry anchor: normal revisit uses the origin zone; secondary-node mode uses
// the same-side internal node created during the first non-hunted touch cycle.
enum ENUM_E0006RevisitEntryAnchorMode
{
   E0006_REVISIT_ENTRY_ORIGIN_ZONE = 0,
   E0006_REVISIT_ENTRY_SECONDARY_NODE_ZONE = 1
};

// Stop anchor modes. The secondary-node mode is meaningful only for revisit entries
// where a first-touch same-side internal node exists.
enum ENUM_E0006StopAnchorMode
{
   E0006_STOP_ORIGIN_ZONE_BACK = 0,
   E0006_STOP_ORIGIN_NODE = 1,
   E0006_STOP_REVISIT_SECONDARY_NODE = 2
};

// Symbol / timeframe.
input string InpSymbol = "";
input ENUM_TIMEFRAMES InpTimeframe = PERIOD_CURRENT;
input int InpBars = 2500;

// M0001 structure. E0006 does not rebuild zone geometry; it uses M0001 live territory modules.
input int InpOriginNodeL = 5;                    // L for origin zones where limits are placed
input int InpInternalNodeL = 2;                  // L for smaller internal nodes used by the hunt filter
input double InpZoneRatio = 0.90;

// Internal same-side hunt qualification.
// 0 = off. Example 3 means a LOW origin needs at least 3 later internal LOW nodes hunted before it is eligible.
input int InpMinInternalHuntsForZone = 3;
input bool InpUseInternalHuntFilter = true;
input bool InpInternalHuntSameSideOnly = true;

// Revisit-only entry filter.
// OFF = original behavior: first eligible touch can receive a limit.
// ON  = require a qualified non-hunted first touch/cycle, then trade only the next revisit cycle.
input bool InpOnlyTradeRevisitZones = false;
input bool InpRevisitFirstCycleMustQualify = true;
input int InpRevisitMinInternalHunts = 0;        // 0 = use InpMinInternalHuntsForZone
input ENUM_E0006RevisitEntryAnchorMode InpRevisitEntryAnchorMode = E0006_REVISIT_ENTRY_ORIGIN_ZONE;

// Execution model: all valid live zones, no trade-count cap.
input long InpMagicNumber = 6006006;
input double InpRiskCash = 100.0;
input double InpRewardR = 0.0;              // 0 = no initial fixed-R TP; use internal opposite-node TP manager
input string InpOrderCommentPrefix = "DALE6";
input int InpPendingExpirationMinutes = 0;        // 0 = GTC
input int InpMaxNodesScan = 0;                    // 0 = scan all confirmed nodes
input int InpMaxBuyPendingOrders = 0;              // 0 = unlimited buy-side pending orders
input int InpMaxSellPendingOrders = 0;             // 0 = unlimited sell-side pending orders
input int InpMaxBuyOpenPositionsBeforeBlock = 0;   // 0 = off; if BUY positions >= this, delete/block BUY pending
input int InpMaxSellOpenPositionsBeforeBlock = 0;  // 0 = off; if SELL positions >= this, delete/block SELL pending
input bool InpDeleteSidePendingWhenOpenCapHit = true; // force-delete side pending orders when open-position cap is reached

// Exit model.
// For BUY positions: count valid internal HIGH nodes after entry; TP is placed at the N-th HIGH.
// For SELL positions: count valid internal LOW nodes after entry; TP is placed at the N-th LOW.
input bool InpUseInternalOppositeNodeTP = true;
input int InpExitOppositeInternalNodeCount = 3;
input bool InpModifyPositionTPOnEveryNewBar = true;

// Spread adjustments requested for the exact limit model.
input double InpBuyEntrySpreadMultiplier = 1.0;    // buy limit = LOW-zone upper edge + spread * multiplier
input double InpSellStopSpreadMultiplier = 1.0;    // sell SL = HIGH-zone upper edge + spread * multiplier
input double InpSellTpSpreadMultiplier = 1.0;      // used only when InpRewardR > 0

// Stop anchor.
// ORIGIN_ZONE_BACK: stop behind the origin frozen zone back edge.
// ORIGIN_NODE: stop behind the origin node price.
// REVISIT_SECONDARY_NODE: stop behind the same-side internal node created during first touch.
// BUY keeps entry shifted upward by spread. SELL stops are shifted upward by spread.
input ENUM_E0006StopAnchorMode InpStopAnchorMode = E0006_STOP_ORIGIN_ZONE_BACK;

// Risk and broker mechanics.
input bool InpAllowMinLotIfRiskTooSmall = false;
input double InpCommissionPerLotRoundTurn = 0.0;

// Sync policy. This is not a trade-count limit; it only keeps the live order grid correct.
input bool InpModifyExistingPendingOrders = true;
input bool InpDeleteStalePendingOrders = true;
input bool InpTradingEnabled = true;

// New-bar only. No tick-by-tick computation.
input bool InpRunOnInit = true;
input int InpUpdateEveryNBars = 1;
input bool InpPrintOrderLogs = false;

// Optional broker-time session gate.
input bool InpUseTradingSessionFilter = false;
input int InpTradingStartHour = 0;
input int InpTradingStartMinute = 0;
input int InpTradingEndHour = 23;
input int InpTradingEndMinute = 59;

#define DAL_E0006_BUILD "1.10"

CTrade g_trade;
datetime g_last_open_bar_time = 0;
int g_new_bar_counter = 0;

struct E0006ZoneSetup
{
   bool valid;
   string reason;
   int node_id;
   int node_index;
   ENUM_DALNodeType node_type;
   int direction;
   datetime node_time;
   datetime active_from_time;
   double node_price;
   double live_extreme;
   double origin_zone_lower;
   double origin_zone_upper;
   double zone_lower;
   double zone_upper;
   int entry_anchor_node_id;
   ENUM_DALNodeType entry_anchor_node_type;
   datetime entry_anchor_node_time;
   double entry_anchor_node_price;
   bool uses_secondary_entry_anchor;
   bool uses_secondary_stop_anchor;
   double spread;
   double entry;
   double sl;
   double tp;
   double reward_r;
   double risk_distance;
   int internal_hunt_count;
   int internal_hunt_required;
   bool internal_hunt_passed;
   string comment;
};

void E0006_ResetSetup(E0006ZoneSetup &s)
{
   s.valid = false;
   s.reason = "not_built";
   s.node_id = -1;
   s.node_index = -1;
   s.node_type = DAL_NODE_LOW;
   s.direction = 0;
   s.node_time = 0;
   s.active_from_time = 0;
   s.node_price = 0.0;
   s.live_extreme = 0.0;
   s.origin_zone_lower = 0.0;
   s.origin_zone_upper = 0.0;
   s.zone_lower = 0.0;
   s.zone_upper = 0.0;
   s.entry_anchor_node_id = -1;
   s.entry_anchor_node_type = DAL_NODE_LOW;
   s.entry_anchor_node_time = 0;
   s.entry_anchor_node_price = 0.0;
   s.uses_secondary_entry_anchor = false;
   s.uses_secondary_stop_anchor = false;
   s.spread = 0.0;
   s.entry = 0.0;
   s.sl = 0.0;
   s.tp = 0.0;
   s.reward_r = 0.0;
   s.risk_distance = 0.0;
   s.internal_hunt_count = 0;
   s.internal_hunt_required = 0;
   s.internal_hunt_passed = false;
   s.comment = "";
}

string E0006_Symbol()
{
   if(InpSymbol == "")
      return _Symbol;
   return InpSymbol;
}

ENUM_TIMEFRAMES E0006_Timeframe()
{
   if(InpTimeframe == PERIOD_CURRENT)
      return (ENUM_TIMEFRAMES)_Period;
   return InpTimeframe;
}

int E0006_ClampInt(const int value, const int lo, const int hi)
{
   if(value < lo)
      return lo;
   if(value > hi)
      return hi;
   return value;
}

string E0006_TwoDigits(const int value)
{
   if(value < 10)
      return "0" + IntegerToString(value);
   return IntegerToString(value);
}

string E0006_FormatDateTime(const datetime value)
{
   MqlDateTime dt;
   TimeToStruct(value, dt);
   return StringFormat("%04d.%02d.%02d %02d:%02d:%02d", dt.year, dt.mon, dt.day, dt.hour, dt.min, dt.sec);
}

string E0006_StopAnchorModeToString()
{
   if(InpStopAnchorMode == E0006_STOP_ORIGIN_NODE)
      return "ORIGIN_NODE";
   if(InpStopAnchorMode == E0006_STOP_REVISIT_SECONDARY_NODE)
      return "REVISIT_SECONDARY_NODE";
   return "ORIGIN_ZONE_BACK";
}

string E0006_RevisitEntryAnchorModeToString()
{
   if(InpRevisitEntryAnchorMode == E0006_REVISIT_ENTRY_SECONDARY_NODE_ZONE)
      return "SECONDARY_NODE_ZONE";
   return "ORIGIN_ZONE";
}

bool E0006_IsTradingSessionOpen(string &reason)
{
   if(!InpUseTradingSessionFilter)
   {
      reason = "timeFilter=OFF";
      return true;
   }

   int start_hour = E0006_ClampInt(InpTradingStartHour, 0, 23);
   int start_minute = E0006_ClampInt(InpTradingStartMinute, 0, 59);
   int end_hour = E0006_ClampInt(InpTradingEndHour, 0, 23);
   int end_minute = E0006_ClampInt(InpTradingEndMinute, 0, 59);
   int start = start_hour * 60 + start_minute;
   int finish = end_hour * 60 + end_minute;

   datetime now_time = TimeCurrent();
   MqlDateTime dt;
   TimeToStruct(now_time, dt);
   int now_minute = dt.hour * 60 + dt.min;

   bool open = false;
   if(start == finish)
      open = true;
   else if(start < finish)
      open = (now_minute >= start && now_minute < finish);
   else
      open = (now_minute >= start || now_minute < finish);

   reason = "timeFilter=ON*now=" + E0006_FormatDateTime(now_time)
      + "*window=" + E0006_TwoDigits(start_hour) + ":" + E0006_TwoDigits(start_minute)
      + "-" + E0006_TwoDigits(end_hour) + ":" + E0006_TwoDigits(end_minute)
      + "*open=" + DAL_BoolToString(open);
   return open;
}

bool E0006_HasNewOpenCandle()
{
   datetime current_open = iTime(E0006_Symbol(), E0006_Timeframe(), 0);
   if(current_open <= 0)
      return false;

   if(g_last_open_bar_time <= 0)
   {
      g_last_open_bar_time = current_open;
      return true;
   }

   if(current_open == g_last_open_bar_time)
      return false;

   g_last_open_bar_time = current_open;
   return true;
}

void E0006_BuildM0001Config(DALM0001Config &config)
{
   DAL_M0001DefaultConfig(config);
   config.L = MathMax(1, InpOriginNodeL);
   config.zone_ratio = InpZoneRatio;
   config.max_events = 0;
   config.min_rtv = 0.0;
}

bool E0006_LoadContext(
   DALBar &bars[],
   int &bars_count,
   DALLRuleNode &origin_nodes[],
   int &origin_nodes_count,
   DALLRuleNode &internal_nodes[],
   int &internal_nodes_count,
   string &reason
)
{
   ArrayResize(bars, 0);
   ArrayResize(origin_nodes, 0);
   ArrayResize(internal_nodes, 0);
   bars_count = 0;
   origin_nodes_count = 0;
   internal_nodes_count = 0;
   reason = "not_loaded";

   int origin_L = MathMax(1, InpOriginNodeL);
   int internal_L = MathMax(1, InpInternalNodeL);

   bars_count = DAL_LoadBarsChronological(E0006_Symbol(), E0006_Timeframe(), InpBars, true, bars);
   int min_required = MathMax(20, MathMax(origin_L, internal_L) * 2 + 10);
   if(bars_count <= min_required)
   {
      reason = "not_enough_closed_bars";
      return false;
   }

   origin_nodes_count = DAL_DetectConfirmedStructuralNodes(bars, bars_count, origin_L, origin_nodes);
   if(origin_nodes_count <= 0)
   {
      reason = "no_confirmed_origin_nodes";
      return false;
   }

   internal_nodes_count = DAL_DetectConfirmedStructuralNodes(bars, bars_count, internal_L, internal_nodes);
   if(internal_nodes_count <= 0)
   {
      reason = "no_confirmed_internal_nodes";
      return false;
   }

   reason = "ok";
   return true;
}

string E0006_ManagedCommentPrefix()
{
   return DAL_ExecManagedCommentPrefix(InpOrderCommentPrefix);
}

string E0006_BuildComment(const E0006ZoneSetup &s)
{
   return DAL_ExecBuildCompactSetupComment(E0006_ManagedCommentPrefix(), s.reward_r, s.node_id, s.direction);
}

bool E0006_InternalNodeSameSideAllowed(
   const DALLRuleNode &origin,
   const DALLRuleNode &internal_node
)
{
   if(!InpInternalHuntSameSideOnly)
      return true;
   return (origin.type == internal_node.type);
}

bool E0006_InternalNodeHuntedByIndex(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &internal_node,
   const int until_index
)
{
   if(!internal_node.confirmed)
      return false;

   int start = internal_node.active_from_index + 1;
   if(start < 0)
      start = internal_node.index + 1;
   if(start < 0)
      start = 0;

   int end = MathMin(until_index, bars_count - 1);
   if(end < start)
      return false;

   for(int i = start; i <= end; i++)
   {
      if(DAL_M0001Hunted(internal_node.type, internal_node.price, bars[i]))
         return true;
   }
   return false;
}

bool E0006_InternalNodeHuntedInRange(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &internal_node,
   const int range_start_index,
   const int range_end_index
)
{
   if(!internal_node.confirmed)
      return false;

   int start = internal_node.active_from_index + 1;
   if(start < 0)
      start = internal_node.index + 1;
   if(start < 0)
      start = 0;

   start = MathMax(start, range_start_index);
   int end = MathMin(range_end_index, bars_count - 1);
   if(end < start)
      return false;

   for(int i = start; i <= end; i++)
   {
      if(DAL_M0001Hunted(internal_node.type, internal_node.price, bars[i]))
         return true;
   }
   return false;
}

int E0006_CountInternalHuntedNodesForOriginRange(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &origin,
   const DALLRuleNode &internal_nodes[],
   const int internal_nodes_count,
   const int cycle_start_index,
   const int cycle_end_index
)
{
   int count = 0;

   int start_after_origin = origin.index;
   if(start_after_origin < 0)
      start_after_origin = origin.active_from_index;

   int start_index = MathMax(start_after_origin + 1, cycle_start_index);
   int end_index = MathMin(cycle_end_index, bars_count - 1);
   if(end_index < start_index)
      return 0;

   for(int k = 0; k < internal_nodes_count; k++)
   {
      DALLRuleNode inner = internal_nodes[k];
      if(!inner.confirmed)
         continue;
      if(inner.index < start_index || inner.index > end_index)
         continue;
      if(!E0006_InternalNodeSameSideAllowed(origin, inner))
         continue;
      if(E0006_InternalNodeHuntedInRange(bars, bars_count, inner, start_index, end_index))
         count++;
   }

   return count;
}

int E0006_RevisitRequiredInternalHunts()
{
   int req = MathMax(0, InpRevisitMinInternalHunts);
   if(req <= 0)
      req = MathMax(0, InpMinInternalHuntsForZone);
   return req;
}

bool E0006_FindFirstNonHuntedTouchEventForNode(
   const DALM0001Event &events[],
   const int events_count,
   const int node_id,
   DALM0001Event &out_event
)
{
   for(int i = 0; i < events_count; i++)
   {
      DALM0001Event ev = events[i];
      if(ev.node_id != node_id)
         continue;
      if(!ev.touch_confirmed)
         continue;
      if(ev.hunted)
         continue;
      out_event = ev;
      return true;
   }
   return false;
}

bool E0006_FindFirstTouchSecondarySameSideNode(
   const DALLRuleNode &origin,
   const DALLRuleNode &internal_nodes[],
   const int internal_nodes_count,
   const DALM0001Event &first_touch,
   DALLRuleNode &out_node,
   string &reason
)
{
   bool found = false;

   for(int i = 0; i < internal_nodes_count; i++)
   {
      DALLRuleNode inner = internal_nodes[i];
      if(!inner.confirmed)
         continue;
      if(inner.type != origin.type)
         continue;

      // The secondary node is the same-side internal pivot created during the
      // first non-hunted touch cycle. Confirmation may happen after the pivot,
      // so the pivot index defines whether it belongs to that touch cycle.
      if(inner.index < first_touch.entry_index || inner.index > first_touch.exit_index)
         continue;

      if(!found)
      {
         out_node = inner;
         found = true;
         continue;
      }

      // If multiple same-side nodes exist inside the first touch cycle, choose
      // the more extreme node: lower LOW for buys, higher HIGH for sells.
      if(origin.type == DAL_NODE_LOW && inner.price < out_node.price)
         out_node = inner;
      else if(origin.type == DAL_NODE_HIGH && inner.price > out_node.price)
         out_node = inner;
   }

   if(!found)
   {
      reason = "no_first_touch_secondary_same_side_node";
      return false;
   }

   reason = "ok_secondary_node_" + IntegerToString(out_node.id);
   return true;
}

bool E0006_RevisitOnlyQualificationPassed(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &origin,
   const DALLRuleNode &internal_nodes[],
   const int internal_nodes_count,
   const DALM0001Event &origin_events[],
   const int origin_events_count,
   int &first_cycle_hunts,
   int &current_cycle_hunts,
   int &required,
   string &reason
)
{
   first_cycle_hunts = 0;
   current_cycle_hunts = 0;
   required = E0006_RevisitRequiredInternalHunts();

   if(!InpOnlyTradeRevisitZones)
   {
      reason = "revisit_filter_off";
      return true;
   }

   if(required <= 0)
   {
      reason = "revisit_required_zero";
      return true;
   }

   DALM0001Event first_touch;
   if(!E0006_FindFirstNonHuntedTouchEventForNode(origin_events, origin_events_count, origin.id, first_touch))
   {
      reason = "revisit_only_no_prior_non_hunted_touch";
      return false;
   }

   // Cycle 1: before the first official touch of this origin zone.
   int pre_start = origin.index + 1;
   if(pre_start < 0)
      pre_start = origin.active_from_index;
   int pre_end = first_touch.entry_index - 1;
   first_cycle_hunts = E0006_CountInternalHuntedNodesForOriginRange(bars, bars_count, origin, internal_nodes, internal_nodes_count, pre_start, pre_end);

   if(InpRevisitFirstCycleMustQualify && first_cycle_hunts < required)
   {
      reason = "revisit_first_cycle_hunts_below_required_" + IntegerToString(first_cycle_hunts) + "_of_" + IntegerToString(required);
      return false;
   }

   // Revisit cycle: after the first non-hunted touch has closed, before the next touch.
   // The order is allowed only after this post-touch cycle has also hunted enough same-side internal nodes.
   int post_start = first_touch.exit_index + 1;
   if(post_start <= 0)
      post_start = first_touch.entry_index + 1;
   int post_end = bars_count - 1;
   current_cycle_hunts = E0006_CountInternalHuntedNodesForOriginRange(bars, bars_count, origin, internal_nodes, internal_nodes_count, post_start, post_end);

   if(current_cycle_hunts < required)
   {
      reason = "revisit_current_cycle_hunts_below_required_" + IntegerToString(current_cycle_hunts) + "_of_" + IntegerToString(required);
      return false;
   }

   reason = "revisit_only_ok_first_" + IntegerToString(first_cycle_hunts)
      + "_current_" + IntegerToString(current_cycle_hunts)
      + "_required_" + IntegerToString(required);
   return true;
}

int E0006_CountInternalHuntedNodesForOrigin(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &origin,
   const DALLRuleNode &internal_nodes[],
   const int internal_nodes_count,
   const int until_index
)
{
   int count = 0;

   int start_after_origin = origin.index;
   if(start_after_origin < 0)
      start_after_origin = origin.active_from_index;

   for(int k = 0; k < internal_nodes_count; k++)
   {
      DALLRuleNode inner = internal_nodes[k];
      if(!inner.confirmed)
         continue;

      if(inner.index <= start_after_origin)
         continue;

      if(inner.index >= until_index)
         continue;

      if(!E0006_InternalNodeSameSideAllowed(origin, inner))
         continue;

      if(E0006_InternalNodeHuntedByIndex(bars, bars_count, inner, until_index))
         count++;
   }

   return count;
}

bool E0006_InternalHuntQualificationPassed(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &origin,
   const DALLRuleNode &internal_nodes[],
   const int internal_nodes_count,
   int &hunt_count,
   int &required,
   string &reason
)
{
   hunt_count = 0;
   required = MathMax(0, InpMinInternalHuntsForZone);

   if(!InpUseInternalHuntFilter || required <= 0)
   {
      reason = "internal_hunt_filter_off";
      return true;
   }

   int until_index = bars_count - 1; // closed-candle decision point; E0006 is new-bar only
   hunt_count = E0006_CountInternalHuntedNodesForOrigin(bars, bars_count, origin, internal_nodes, internal_nodes_count, until_index);

   if(hunt_count < required)
   {
      reason = "internal_hunts_below_required_" + IntegerToString(hunt_count) + "_of_" + IntegerToString(required);
      return false;
   }

   reason = "internal_hunts_ok_" + IntegerToString(hunt_count) + "_of_" + IntegerToString(required);
   return true;
}

bool E0006_BuildZoneSetup(
   const string symbol,
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &node,
   const DALLRuleNode &internal_nodes[],
   const int internal_nodes_count,
   const DALM0001Event &origin_events[],
   const int origin_events_count,
   const double zone_ratio,
   E0006ZoneSetup &setup
)
{
   E0006_ResetSetup(setup);

   if(!node.confirmed)
   {
      setup.reason = "node_unconfirmed";
      return false;
   }
   if(node.active_from_index < 0 || node.active_from_index >= bars_count)
   {
      setup.reason = "node_not_active_in_window";
      return false;
   }

   double extreme = 0.0, lower = 0.0, upper = 0.0;
   bool hunted = false;
   if(!DAL_ExecBuildLiveNodeTerritory(bars, bars_count, node, zone_ratio, extreme, lower, upper, hunted))
   {
      setup.reason = "live_territory_build_failed";
      return false;
   }
   if(hunted)
   {
      setup.reason = "node_hunted_invalidated";
      return false;
   }

   int revisit_first_cycle_hunts = 0;
   int revisit_current_cycle_hunts = 0;
   int revisit_required = 0;
   string revisit_reason = "";
   if(!E0006_RevisitOnlyQualificationPassed(bars, bars_count, node, internal_nodes, internal_nodes_count, origin_events, origin_events_count, revisit_first_cycle_hunts, revisit_current_cycle_hunts, revisit_required, revisit_reason))
   {
      setup.internal_hunt_count = revisit_current_cycle_hunts;
      setup.internal_hunt_required = revisit_required;
      setup.internal_hunt_passed = false;
      setup.reason = revisit_reason;
      return false;
   }

   DALM0001Event first_touch_for_secondary;
   bool has_first_touch_for_secondary = E0006_FindFirstNonHuntedTouchEventForNode(origin_events, origin_events_count, node.id, first_touch_for_secondary);

   bool need_secondary_node = (InpOnlyTradeRevisitZones &&
      (InpRevisitEntryAnchorMode == E0006_REVISIT_ENTRY_SECONDARY_NODE_ZONE ||
       InpStopAnchorMode == E0006_STOP_REVISIT_SECONDARY_NODE));

   DALLRuleNode secondary_node;
   bool has_secondary_node = false;
   double secondary_extreme = 0.0;
   double secondary_lower = 0.0;
   double secondary_upper = 0.0;
   bool secondary_hunted = false;

   if(InpStopAnchorMode == E0006_STOP_REVISIT_SECONDARY_NODE && !InpOnlyTradeRevisitZones)
   {
      setup.reason = "secondary_stop_requires_revisit_mode";
      return false;
   }

   if(InpRevisitEntryAnchorMode == E0006_REVISIT_ENTRY_SECONDARY_NODE_ZONE && !InpOnlyTradeRevisitZones)
   {
      setup.reason = "secondary_entry_requires_revisit_mode";
      return false;
   }

   if(need_secondary_node)
   {
      if(!has_first_touch_for_secondary)
      {
         setup.reason = "secondary_anchor_no_first_non_hunted_touch";
         return false;
      }

      string secondary_reason = "";
      if(!E0006_FindFirstTouchSecondarySameSideNode(node, internal_nodes, internal_nodes_count, first_touch_for_secondary, secondary_node, secondary_reason))
      {
         setup.reason = secondary_reason;
         return false;
      }

      if(!DAL_ExecBuildLiveNodeTerritory(bars, bars_count, secondary_node, zone_ratio, secondary_extreme, secondary_lower, secondary_upper, secondary_hunted))
      {
         setup.reason = "secondary_live_territory_build_failed";
         return false;
      }
      if(secondary_hunted)
      {
         setup.reason = "secondary_node_hunted_invalidated";
         return false;
      }

      has_secondary_node = true;
   }

   int internal_count = 0;
   int internal_required = 0;
   string internal_reason = "";
   if(!InpOnlyTradeRevisitZones && !E0006_InternalHuntQualificationPassed(bars, bars_count, node, internal_nodes, internal_nodes_count, internal_count, internal_required, internal_reason))
   {
      setup.internal_hunt_count = internal_count;
      setup.internal_hunt_required = internal_required;
      setup.internal_hunt_passed = false;
      setup.reason = internal_reason;
      return false;
   }

   double spread = DAL_ExecCurrentSpreadPrice(symbol);
   double reward_r = (InpRewardR > 0.0 ? MathMax(0.01, InpRewardR) : 0.0);

   setup.node_id = node.id;
   setup.node_index = node.index;
   setup.node_type = node.type;
   setup.node_time = node.time;
   setup.active_from_time = node.active_from_time;
   setup.node_price = node.price;
   setup.live_extreme = extreme;
   setup.origin_zone_lower = lower;
   setup.origin_zone_upper = upper;

   double entry_zone_lower = lower;
   double entry_zone_upper = upper;
   double entry_node_price = node.price;
   int entry_node_id = node.id;
   ENUM_DALNodeType entry_node_type = node.type;
   datetime entry_node_time = node.time;

   if(has_secondary_node && InpRevisitEntryAnchorMode == E0006_REVISIT_ENTRY_SECONDARY_NODE_ZONE)
   {
      entry_zone_lower = secondary_lower;
      entry_zone_upper = secondary_upper;
      entry_node_price = secondary_node.price;
      entry_node_id = secondary_node.id;
      entry_node_type = secondary_node.type;
      entry_node_time = secondary_node.time;
      setup.uses_secondary_entry_anchor = true;
   }

   setup.zone_lower = entry_zone_lower;
   setup.zone_upper = entry_zone_upper;
   setup.entry_anchor_node_id = entry_node_id;
   setup.entry_anchor_node_type = entry_node_type;
   setup.entry_anchor_node_time = entry_node_time;
   setup.entry_anchor_node_price = entry_node_price;
   setup.uses_secondary_stop_anchor = (InpStopAnchorMode == E0006_STOP_REVISIT_SECONDARY_NODE);
   setup.spread = spread;
   setup.reward_r = reward_r;
   if(InpOnlyTradeRevisitZones)
   {
      setup.internal_hunt_count = revisit_current_cycle_hunts;
      setup.internal_hunt_required = revisit_required;
   }
   else
   {
      setup.internal_hunt_count = internal_count;
      setup.internal_hunt_required = internal_required;
   }
   setup.internal_hunt_passed = true;

   double raw_stop_anchor = 0.0;
   if(node.type == DAL_NODE_LOW)
   {
      setup.direction = +1;
      // Support/demand touch. Buy opens on Ask, so entry is shifted up by spread as requested.
      setup.entry = entry_zone_upper + spread * MathMax(0.0, InpBuyEntrySpreadMultiplier);

      if(InpStopAnchorMode == E0006_STOP_ORIGIN_ZONE_BACK)
         raw_stop_anchor = lower;
      else if(InpStopAnchorMode == E0006_STOP_ORIGIN_NODE)
         raw_stop_anchor = node.price;
      else
         raw_stop_anchor = secondary_node.price;

      setup.sl = raw_stop_anchor;
      setup.risk_distance = MathAbs(setup.entry - setup.sl);
      setup.tp = (InpRewardR > 0.0 ? setup.entry + setup.risk_distance * reward_r : 0.0);
   }
   else
   {
      setup.direction = -1;
      // Supply/resistance touch. Sell entry stays on lower zone edge.
      setup.entry = entry_zone_lower;

      if(InpStopAnchorMode == E0006_STOP_ORIGIN_ZONE_BACK)
         raw_stop_anchor = upper;
      else if(InpStopAnchorMode == E0006_STOP_ORIGIN_NODE)
         raw_stop_anchor = node.price;
      else
         raw_stop_anchor = secondary_node.price;

      // All SELL stop anchors are shifted upward by spread as requested.
      setup.sl = raw_stop_anchor + spread * MathMax(0.0, InpSellStopSpreadMultiplier);
      setup.risk_distance = MathAbs(setup.entry - setup.sl);
      setup.tp = (InpRewardR > 0.0 ? setup.entry - setup.risk_distance * reward_r + spread * MathMax(0.0, InpSellTpSpreadMultiplier) : 0.0);
   }

   if(setup.risk_distance <= 0.0)
   {
      setup.reason = "zero_stop_distance";
      return false;
   }

   setup.comment = E0006_BuildComment(setup);
   setup.valid = true;
   setup.reason = "ok";
   DAL_ExecNormalizePrices(symbol, setup.entry, setup.sl, setup.tp);
   return true;
}

bool E0006_PositionCommentExists(const string symbol, const long magic, const string comment)
{
   int pos_total = PositionsTotal();
   for(int i = 0; i < pos_total; i++)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !PositionSelectByTicket(ticket))
         continue;
      if(PositionGetString(POSITION_SYMBOL) != symbol)
         continue;
      if((long)PositionGetInteger(POSITION_MAGIC) != magic)
         continue;
      if(PositionGetString(POSITION_COMMENT) == comment)
         return true;
   }
   return false;
}

bool E0006_FindPendingByComment(const string symbol, const long magic, const string comment, DALExecPendingOrder &out)
{
   DAL_ExecResetPendingOrder(out);
   for(int i = 0; i < OrdersTotal(); i++)
   {
      ulong ticket = OrderGetTicket(i);
      if(ticket == 0 || !OrderSelect(ticket))
         continue;
      if(OrderGetString(ORDER_SYMBOL) != symbol)
         continue;
      if((long)OrderGetInteger(ORDER_MAGIC) != magic)
         continue;
      if(OrderGetString(ORDER_COMMENT) != comment)
         continue;
      return DAL_ExecReadPendingOrder(ticket, out);
   }
   return false;
}


int E0006_OrderDirectionFromType(const ENUM_ORDER_TYPE type)
{
   if(type == ORDER_TYPE_BUY_LIMIT || type == ORDER_TYPE_BUY_STOP || type == ORDER_TYPE_BUY_STOP_LIMIT)
      return +1;
   if(type == ORDER_TYPE_SELL_LIMIT || type == ORDER_TYPE_SELL_STOP || type == ORDER_TYPE_SELL_STOP_LIMIT)
      return -1;
   return 0;
}

int E0006_CountOpenPositionsByDirection(const string symbol, const long magic, const int direction)
{
   int count = 0;
   int pos_total = PositionsTotal();
   for(int i = 0; i < pos_total; i++)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !PositionSelectByTicket(ticket))
         continue;
      if(PositionGetString(POSITION_SYMBOL) != symbol)
         continue;
      if((long)PositionGetInteger(POSITION_MAGIC) != magic)
         continue;

      ENUM_POSITION_TYPE type = (ENUM_POSITION_TYPE)PositionGetInteger(POSITION_TYPE);
      if(direction > 0 && type == POSITION_TYPE_BUY)
         count++;
      else if(direction < 0 && type == POSITION_TYPE_SELL)
         count++;
   }
   return count;
}

void E0006_DeletePendingOrdersByDirection(
   const string symbol,
   const long magic,
   const int direction,
   int &deleted,
   int &kept,
   int &failed
)
{
   deleted = 0;
   kept = 0;
   failed = 0;

   string prefix = E0006_ManagedCommentPrefix();
   for(int i = OrdersTotal() - 1; i >= 0; i--)
   {
      ulong ticket = OrderGetTicket(i);
      if(ticket == 0 || !OrderSelect(ticket))
         continue;
      if(OrderGetString(ORDER_SYMBOL) != symbol)
         continue;
      if((long)OrderGetInteger(ORDER_MAGIC) != magic)
         continue;

      ENUM_ORDER_TYPE type = (ENUM_ORDER_TYPE)OrderGetInteger(ORDER_TYPE);
      if(!DAL_ExecOrderIsPendingLimit(type))
         continue;
      if(E0006_OrderDirectionFromType(type) != direction)
         continue;

      string comment = OrderGetString(ORDER_COMMENT);
      if(StringFind(comment, prefix, 0) != 0)
      {
         kept++;
         continue;
      }

      string reason = "";
      if(DAL_ExecDeletePendingOrder(ticket, g_trade, reason))
         deleted++;
      else
         failed++;
   }
}

bool E0006_PricesCloseEnough(const string symbol, const double a, const double b)
{
   double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
   if(point <= 0.0)
      point = 0.00000001;
   return (MathAbs(a - b) <= point * 0.5);
}

bool E0006_CheckLimitGeometryAllowOptionalTP(
   const string symbol,
   const int direction,
   const double entry,
   const double sl,
   const double tp,
   string &reason
)
{
   double bid = SymbolInfoDouble(symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(symbol, SYMBOL_ASK);
   double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
   int stops_level = (int)SymbolInfoInteger(symbol, SYMBOL_TRADE_STOPS_LEVEL);
   double min_dist = MathMax(0.0, stops_level * point);

   if(point <= 0.0 || bid <= 0.0 || ask <= 0.0)
   {
      reason = "invalid_market_quote";
      return false;
   }

   if(direction > 0)
   {
      if(!(sl < entry))
      {
         reason = "invalid_buy_sl_geometry";
         return false;
      }
      if(tp > 0.0 && !(tp > entry))
      {
         reason = "invalid_buy_tp_geometry";
         return false;
      }
      if(!(entry < ask - min_dist))
      {
         reason = "buy_limit_not_below_ask_or_too_close";
         return false;
      }
   }
   else if(direction < 0)
   {
      if(!(sl > entry))
      {
         reason = "invalid_sell_sl_geometry";
         return false;
      }
      if(tp > 0.0 && !(tp < entry))
      {
         reason = "invalid_sell_tp_geometry";
         return false;
      }
      if(!(entry > bid + min_dist))
      {
         reason = "sell_limit_not_above_bid_or_too_close";
         return false;
      }
   }
   else
   {
      reason = "zero_direction";
      return false;
   }

   reason = "ok";
   return true;
}

bool E0006_PlaceLimitOrderAllowOptionalTP(
   const string symbol,
   const long magic,
   const int direction,
   const double volume,
   double entry,
   double sl,
   double tp,
   const string comment,
   const int expiration_minutes,
   CTrade &trade,
   string &reason
)
{
   DAL_ExecNormalizePrices(symbol, entry, sl, tp);

   if(!E0006_CheckLimitGeometryAllowOptionalTP(symbol, direction, entry, sl, tp, reason))
      return false;

   if(volume <= 0.0)
   {
      reason = "volume_zero";
      return false;
   }

   datetime expiration = 0;
   ENUM_ORDER_TYPE_TIME type_time = ORDER_TIME_GTC;
   if(expiration_minutes > 0)
   {
      type_time = ORDER_TIME_SPECIFIED;
      expiration = TimeCurrent() + expiration_minutes * 60;
   }

   trade.SetExpertMagicNumber(magic);

   bool ok = false;
   if(direction > 0)
      ok = trade.BuyLimit(volume, entry, symbol, sl, tp, type_time, expiration, comment);
   else
      ok = trade.SellLimit(volume, entry, symbol, sl, tp, type_time, expiration, comment);

   if(!ok)
   {
      reason = "trade_send_failed_retcode_" + IntegerToString((int)trade.ResultRetcode()) + "_" + trade.ResultRetcodeDescription();
      return false;
   }

   reason = "ok_ticket_" + IntegerToString((int)trade.ResultOrder());
   return true;
}

bool E0006_CheckPositionTPGeometry(
   const string symbol,
   const int direction,
   const double tp,
   string &reason
)
{
   if(tp <= 0.0)
   {
      reason = "tp_zero";
      return false;
   }

   double bid = SymbolInfoDouble(symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(symbol, SYMBOL_ASK);
   double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
   int stops_level = (int)SymbolInfoInteger(symbol, SYMBOL_TRADE_STOPS_LEVEL);
   double min_dist = MathMax(0.0, stops_level * point);

   if(point <= 0.0 || bid <= 0.0 || ask <= 0.0)
   {
      reason = "invalid_market_quote";
      return false;
   }

   if(direction > 0)
   {
      if(!(tp > bid + min_dist))
      {
         reason = "buy_tp_not_above_bid_or_too_close";
         return false;
      }
   }
   else if(direction < 0)
   {
      if(!(tp < ask - min_dist))
      {
         reason = "sell_tp_not_below_ask_or_too_close";
         return false;
      }
   }
   else
   {
      reason = "zero_direction";
      return false;
   }

   reason = "ok";
   return true;
}

bool E0006_ModifyPendingOrder(const ulong ticket, double entry, double sl, double tp, string &reason)
{
   if(ticket == 0 || !OrderSelect(ticket))
   {
      reason = "pending_ticket_not_found";
      return false;
   }

   string symbol = OrderGetString(ORDER_SYMBOL);
   DAL_ExecNormalizePrices(symbol, entry, sl, tp);

   int direction = E0006_OrderDirectionFromType((ENUM_ORDER_TYPE)OrderGetInteger(ORDER_TYPE));
   string geometry_reason = "";
   if(!E0006_CheckLimitGeometryAllowOptionalTP(symbol, direction, entry, sl, tp, geometry_reason))
   {
      reason = "geometry_" + geometry_reason;
      return false;
   }

   datetime expiration = 0;
   ENUM_ORDER_TYPE_TIME type_time = ORDER_TIME_GTC;
   if(InpPendingExpirationMinutes > 0)
   {
      type_time = ORDER_TIME_SPECIFIED;
      expiration = TimeCurrent() + InpPendingExpirationMinutes * 60;
   }

   g_trade.SetExpertMagicNumber(InpMagicNumber);
   if(!g_trade.OrderModify(ticket, entry, sl, tp, type_time, expiration, 0.0))
   {
      reason = "modify_failed_retcode_" + IntegerToString((int)g_trade.ResultRetcode()) + "_" + g_trade.ResultRetcodeDescription();
      return false;
   }

   reason = "ok_modified_" + IntegerToString((int)ticket);
   return true;
}

bool E0006_UpsertLimitOrder(const E0006ZoneSetup &s, string &reason)
{
   reason = "not_sent";
   if(!s.valid)
   {
      reason = s.reason;
      return false;
   }

   string symbol = E0006_Symbol();

   if(E0006_PositionCommentExists(symbol, InpMagicNumber, s.comment))
   {
      reason = "position_exists_for_zone";
      return false;
   }

   string geometry_reason = "";
   if(!E0006_CheckLimitGeometryAllowOptionalTP(symbol, s.direction, s.entry, s.sl, s.tp, geometry_reason))
   {
      reason = "geometry_" + geometry_reason;
      return false;
   }

   DALExecRiskSizing risk;
   if(!DAL_ExecCalculateRiskVolume(symbol, s.entry, s.sl, InpRiskCash, InpCommissionPerLotRoundTurn, InpAllowMinLotIfRiskTooSmall, risk))
   {
      reason = "risk_" + risk.reason;
      return false;
   }

   DALExecPendingOrder existing;
   if(E0006_FindPendingByComment(symbol, InpMagicNumber, s.comment, existing))
   {
      if(existing.direction != s.direction)
      {
         string del_reason = "";
         DAL_ExecDeletePendingOrder(existing.ticket, g_trade, del_reason);
      }
      else
      {
         bool same = E0006_PricesCloseEnough(symbol, existing.price, s.entry)
            && E0006_PricesCloseEnough(symbol, existing.sl, s.sl)
            && E0006_PricesCloseEnough(symbol, existing.tp, s.tp)
            && E0006_PricesCloseEnough(symbol, existing.volume, risk.volume);

         if(same || !InpModifyExistingPendingOrders)
         {
            reason = same ? "ok_existing_same" : "existing_pending_no_modify";
            return true;
         }

         string mod_reason = "";
         if(E0006_ModifyPendingOrder(existing.ticket, s.entry, s.sl, s.tp, mod_reason))
         {
            reason = mod_reason;
            return true;
         }

         reason = mod_reason;
         return false;
      }
   }

   if(!InpTradingEnabled)
   {
      reason = "trading_disabled";
      return false;
   }

   string place_reason = "";
   bool ok = E0006_PlaceLimitOrderAllowOptionalTP(symbol, InpMagicNumber, s.direction, risk.volume, s.entry, s.sl, s.tp, s.comment, InpPendingExpirationMinutes, g_trade, place_reason);
   reason = place_reason;
   return ok;
}

bool E0006_StringInArray(const string value, const string &arr[])
{
   for(int i = 0; i < ArraySize(arr); i++)
   {
      if(arr[i] == value)
         return true;
   }
   return false;
}

void E0006_AppendStringUnique(string &arr[], const string value)
{
   if(value == "" || E0006_StringInArray(value, arr))
      return;
   int n = ArraySize(arr);
   ArrayResize(arr, n + 1);
   arr[n] = value;
}

void E0006_DeleteStalePendingOrders(const string &desired_comments[], int &deleted, int &kept, int &failed)
{
   deleted = 0;
   kept = 0;
   failed = 0;

   if(!InpDeleteStalePendingOrders)
      return;

   string symbol = E0006_Symbol();
   string prefix = E0006_ManagedCommentPrefix();

   for(int i = OrdersTotal() - 1; i >= 0; i--)
   {
      ulong ticket = OrderGetTicket(i);
      if(ticket == 0 || !OrderSelect(ticket))
         continue;
      if(OrderGetString(ORDER_SYMBOL) != symbol)
         continue;
      if((long)OrderGetInteger(ORDER_MAGIC) != InpMagicNumber)
         continue;

      ENUM_ORDER_TYPE type = (ENUM_ORDER_TYPE)OrderGetInteger(ORDER_TYPE);
      if(!DAL_ExecOrderIsPendingLimit(type))
         continue;

      string comment = OrderGetString(ORDER_COMMENT);
      if(StringFind(comment, prefix, 0) != 0)
         continue;

      if(E0006_StringInArray(comment, desired_comments))
      {
         kept++;
         continue;
      }

      string reason = "";
      if(DAL_ExecDeletePendingOrder(ticket, g_trade, reason))
         deleted++;
      else
         failed++;
   }
}

bool E0006_FindNthOppositeInternalNodeAfterEntry(
   const DALLRuleNode &internal_nodes[],
   const int internal_nodes_count,
   const int position_direction,
   const datetime entry_time,
   const double entry_price,
   const int required_count,
   DALLRuleNode &target_node,
   int &found_count,
   string &reason
)
{
   found_count = 0;
   reason = "not_found";

   int required = MathMax(1, required_count);
   ENUM_DALNodeType target_type = (position_direction > 0 ? DAL_NODE_HIGH : DAL_NODE_LOW);

   for(int i = 0; i < internal_nodes_count; i++)
   {
      DALLRuleNode node = internal_nodes[i];
      if(!node.confirmed)
         continue;
      if(node.type != target_type)
         continue;

      // "after entry" means the internal node must become valid after the position entry time.
      if(node.active_from_time <= entry_time)
         continue;

      // TP geometry relative to the actual filled entry.
      if(position_direction > 0 && node.price <= entry_price)
         continue;
      if(position_direction < 0 && node.price >= entry_price)
         continue;

      found_count++;
      if(found_count >= required)
      {
         target_node = node;
         reason = "ok";
         return true;
      }
   }

   reason = "opposite_internal_nodes_" + IntegerToString(found_count) + "_of_" + IntegerToString(required);
   return false;
}

bool E0006_ModifyPositionTPByTicket(
   const ulong ticket,
   const double sl,
   const double tp,
   string &reason
)
{
   g_trade.SetExpertMagicNumber(InpMagicNumber);
   if(!g_trade.PositionModify(ticket, sl, tp))
   {
      reason = "position_modify_failed_retcode_" + IntegerToString((int)g_trade.ResultRetcode()) + "_" + g_trade.ResultRetcodeDescription();
      return false;
   }

   reason = "ok_modified_" + IntegerToString((int)ticket);
   return true;
}

void E0006_SyncOpenPositionInternalNodeTP(
   const string symbol,
   const DALLRuleNode &internal_nodes[],
   const int internal_nodes_count,
   const string run_mode,
   int &tp_checked,
   int &tp_waiting,
   int &tp_modified,
   int &tp_rejected
)
{
   tp_checked = 0;
   tp_waiting = 0;
   tp_modified = 0;
   tp_rejected = 0;

   if(!InpUseInternalOppositeNodeTP || !InpModifyPositionTPOnEveryNewBar)
      return;

   int required_count = MathMax(1, InpExitOppositeInternalNodeCount);
   string prefix = E0006_ManagedCommentPrefix();

   for(int i = 0; i < PositionsTotal(); i++)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !PositionSelectByTicket(ticket))
         continue;
      if(PositionGetString(POSITION_SYMBOL) != symbol)
         continue;
      if((long)PositionGetInteger(POSITION_MAGIC) != InpMagicNumber)
         continue;

      string comment = PositionGetString(POSITION_COMMENT);
      if(StringFind(comment, prefix, 0) != 0)
         continue;

      ENUM_POSITION_TYPE type = (ENUM_POSITION_TYPE)PositionGetInteger(POSITION_TYPE);
      int direction = (type == POSITION_TYPE_BUY ? +1 : (type == POSITION_TYPE_SELL ? -1 : 0));
      if(direction == 0)
         continue;

      tp_checked++;

      datetime entry_time = (datetime)PositionGetInteger(POSITION_TIME);
      double entry_price = PositionGetDouble(POSITION_PRICE_OPEN);
      double sl = PositionGetDouble(POSITION_SL);
      double old_tp = PositionGetDouble(POSITION_TP);

      DALLRuleNode target;
      int found_count = 0;
      string find_reason = "";
      if(!E0006_FindNthOppositeInternalNodeAfterEntry(internal_nodes, internal_nodes_count, direction, entry_time, entry_price, required_count, target, found_count, find_reason))
      {
         tp_waiting++;
         continue;
      }

      double new_tp = target.price;
      int digits = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
      new_tp = NormalizeDouble(new_tp, digits);

      if(E0006_PricesCloseEnough(symbol, old_tp, new_tp))
         continue;

      string geometry_reason = "";
      if(!E0006_CheckPositionTPGeometry(symbol, direction, new_tp, geometry_reason))
      {
         tp_rejected++;
         if(InpPrintOrderLogs)
            Print("DAL_E0006_TP_SKIP *** build=", DAL_E0006_BUILD,
               "*runMode=", run_mode,
               "*ticket=", ticket,
               "*dir=", direction,
               "*requiredOppositeNodes=", required_count,
               "*foundOppositeNodes=", found_count,
               "*targetNodeId=", target.id,
               "*targetPrice=", DoubleToString(new_tp, digits),
               "*reason=", geometry_reason);
         continue;
      }

      string mod_reason = "";
      if(E0006_ModifyPositionTPByTicket(ticket, sl, new_tp, mod_reason))
      {
         tp_modified++;
         if(InpPrintOrderLogs)
            Print("DAL_E0006_TP_SET *** build=", DAL_E0006_BUILD,
               "*runMode=", run_mode,
               "*ticket=", ticket,
               "*dir=", direction,
               "*requiredOppositeNodes=", required_count,
               "*targetNodeId=", target.id,
               "*targetNodeTime=", E0006_FormatDateTime(target.time),
               "*targetActiveFrom=", E0006_FormatDateTime(target.active_from_time),
               "*tp=", DoubleToString(new_tp, digits),
               "*reason=", mod_reason);
      }
      else
      {
         tp_rejected++;
         if(InpPrintOrderLogs)
            Print("DAL_E0006_TP_MODIFY_FAIL *** build=", DAL_E0006_BUILD,
               "*runMode=", run_mode,
               "*ticket=", ticket,
               "*dir=", direction,
               "*targetNodeId=", target.id,
               "*tp=", DoubleToString(new_tp, digits),
               "*reason=", mod_reason);
      }
   }
}

void E0006_ProcessNewBar(const string run_mode)
{
   string session_reason = "";
   if(!E0006_IsTradingSessionOpen(session_reason))
      return;

   DALBar bars[];
   DALLRuleNode nodes[];
   DALLRuleNode internal_nodes[];
   int bars_count = 0;
   int nodes_count = 0;
   int internal_nodes_count = 0;
   string load_reason = "";
   if(!E0006_LoadContext(bars, bars_count, nodes, nodes_count, internal_nodes, internal_nodes_count, load_reason))
   {
      if(InpPrintOrderLogs)
         Print("DAL_E0006_SKIP *** build=", DAL_E0006_BUILD, "*runMode=", run_mode, "*reason=", load_reason);
      return;
   }

   int tp_checked = 0, tp_waiting = 0, tp_modified = 0, tp_rejected = 0;
   E0006_SyncOpenPositionInternalNodeTP(E0006_Symbol(), internal_nodes, internal_nodes_count, run_mode, tp_checked, tp_waiting, tp_modified, tp_rejected);

   DALM0001Config m1;
   E0006_BuildM0001Config(m1);

   DALM0001Event origin_events[];
   int origin_events_count = DAL_M0001ComputeEvents(bars, bars_count, nodes, nodes_count, m1, origin_events);

   string desired_comments[];
   ArrayResize(desired_comments, 0);

   int scanned = 0;
   int built = 0;
   int sent_or_synced = 0;
   int skipped = 0;
   int build_reject = 0;
   int order_reject = 0;
   int buy_desired = 0;
   int sell_desired = 0;
   int side_cap_skip = 0;
   int internal_hunt_filter_skip = 0;
   int max_buy_pending = MathMax(0, InpMaxBuyPendingOrders);
   int max_sell_pending = MathMax(0, InpMaxSellPendingOrders);
   int max_buy_open_before_block = MathMax(0, InpMaxBuyOpenPositionsBeforeBlock);
   int max_sell_open_before_block = MathMax(0, InpMaxSellOpenPositionsBeforeBlock);
   int open_buy_positions = E0006_CountOpenPositionsByDirection(E0006_Symbol(), InpMagicNumber, +1);
   int open_sell_positions = E0006_CountOpenPositionsByDirection(E0006_Symbol(), InpMagicNumber, -1);
   bool buy_side_blocked_by_open_cap = (max_buy_open_before_block > 0 && open_buy_positions >= max_buy_open_before_block);
   bool sell_side_blocked_by_open_cap = (max_sell_open_before_block > 0 && open_sell_positions >= max_sell_open_before_block);
   int side_block_deleted_buy = 0, side_block_kept_buy = 0, side_block_failed_buy = 0;
   int side_block_deleted_sell = 0, side_block_kept_sell = 0, side_block_failed_sell = 0;

   if(InpDeleteSidePendingWhenOpenCapHit && buy_side_blocked_by_open_cap)
      E0006_DeletePendingOrdersByDirection(E0006_Symbol(), InpMagicNumber, +1, side_block_deleted_buy, side_block_kept_buy, side_block_failed_buy);
   if(InpDeleteSidePendingWhenOpenCapHit && sell_side_blocked_by_open_cap)
      E0006_DeletePendingOrdersByDirection(E0006_Symbol(), InpMagicNumber, -1, side_block_deleted_sell, side_block_kept_sell, side_block_failed_sell);

   for(int i = nodes_count - 1; i >= 0; i--)
   {
      DALLRuleNode node = nodes[i];
      if(!node.confirmed)
      {
         skipped++;
         continue;
      }

      scanned++;
      if(InpMaxNodesScan > 0 && scanned > InpMaxNodesScan)
         break;

      E0006ZoneSetup setup;
      if(!E0006_BuildZoneSetup(E0006_Symbol(), bars, bars_count, node, internal_nodes, internal_nodes_count, origin_events, origin_events_count, m1.zone_ratio, setup))
      {
         build_reject++;
         if(StringFind(setup.reason, "internal_hunts_below_required", 0) == 0
            || StringFind(setup.reason, "revisit_", 0) == 0)
            internal_hunt_filter_skip++;
         continue;
      }

      built++;

      if(setup.direction > 0 && buy_side_blocked_by_open_cap)
      {
         side_cap_skip++;
         if(InpPrintOrderLogs)
            Print("DAL_E0006_OPEN_SIDE_BLOCK_SKIP *** build=", DAL_E0006_BUILD,
               "*nodeId=", setup.node_id,
               "*side=BUY",
               "*openBuyPositions=", open_buy_positions,
               "*maxBuyOpenBeforeBlock=", max_buy_open_before_block,
               "*deletedBuyPending=", side_block_deleted_buy);
         continue;
      }
      if(setup.direction < 0 && sell_side_blocked_by_open_cap)
      {
         side_cap_skip++;
         if(InpPrintOrderLogs)
            Print("DAL_E0006_OPEN_SIDE_BLOCK_SKIP *** build=", DAL_E0006_BUILD,
               "*nodeId=", setup.node_id,
               "*side=SELL",
               "*openSellPositions=", open_sell_positions,
               "*maxSellOpenBeforeBlock=", max_sell_open_before_block,
          "*originL=", MathMax(1, InpOriginNodeL),
          "*internalL=", MathMax(1, InpInternalNodeL),
          "*useInternalHuntFilter=", DAL_BoolToString(InpUseInternalHuntFilter),
          "*minInternalHuntsForZone=", MathMax(0, InpMinInternalHuntsForZone),
          "*sameSideOnly=", DAL_BoolToString(InpInternalHuntSameSideOnly),
               "*deletedSellPending=", side_block_deleted_sell);
         continue;
      }

      if(setup.direction > 0 && max_buy_pending > 0 && buy_desired >= max_buy_pending)
      {
         side_cap_skip++;
         if(InpPrintOrderLogs)
            Print("DAL_E0006_SIDE_CAP_SKIP *** build=", DAL_E0006_BUILD, "*nodeId=", setup.node_id, "*side=BUY*maxBuyPending=", max_buy_pending);
         continue;
      }
      if(setup.direction < 0 && max_sell_pending > 0 && sell_desired >= max_sell_pending)
      {
         side_cap_skip++;
         if(InpPrintOrderLogs)
            Print("DAL_E0006_SIDE_CAP_SKIP *** build=", DAL_E0006_BUILD, "*nodeId=", setup.node_id, "*side=SELL*maxSellPending=", max_sell_pending);
         continue;
      }

      if(setup.direction > 0)
         buy_desired++;
      else if(setup.direction < 0)
         sell_desired++;

      E0006_AppendStringUnique(desired_comments, setup.comment);

      string order_reason = "";
      if(E0006_UpsertLimitOrder(setup, order_reason))
      {
         sent_or_synced++;
         if(InpPrintOrderLogs)
         {
            int digits = (int)SymbolInfoInteger(E0006_Symbol(), SYMBOL_DIGITS);
            Print("DAL_E0006_ALL_ZONE_LIMIT *** build=", DAL_E0006_BUILD,
               "*runMode=", run_mode,
               "*action=UPSERT_OK",
               "*nodeId=", setup.node_id,
               "*side=", DAL_NodeTypeToString(setup.node_type),
               "*dir=", setup.direction,
               "*zoneLower=", DoubleToString(setup.zone_lower, digits),
               "*zoneUpper=", DoubleToString(setup.zone_upper, digits),
               "*entry=", DoubleToString(setup.entry, digits),
               "*sl=", DoubleToString(setup.sl, digits),
               "*tp=", DoubleToString(setup.tp, digits),
               "*rewardR=", DoubleToString(setup.reward_r, 2),
               "*spread=", DoubleToString(setup.spread, digits),
               "*revisitEntryAnchor=", E0006_RevisitEntryAnchorModeToString(),
               "*stopAnchor=", E0006_StopAnchorModeToString(),
               "*originNodePrice=", DoubleToString(setup.node_price, digits),
               "*entryAnchorNodeId=", setup.entry_anchor_node_id,
               "*entryAnchorNodePrice=", DoubleToString(setup.entry_anchor_node_price, digits),
               "*usesSecondaryEntry=", DAL_BoolToString(setup.uses_secondary_entry_anchor),
               "*usesSecondaryStop=", DAL_BoolToString(setup.uses_secondary_stop_anchor),
               "*internalHunts=", setup.internal_hunt_count,
               "*internalHuntsRequired=", setup.internal_hunt_required,
               "*comment=", setup.comment,
               "*reason=", order_reason);
         }
      }
      else
      {
         order_reject++;
         if(InpPrintOrderLogs)
            Print("DAL_E0006_SIGNAL_SKIP *** build=", DAL_E0006_BUILD, "*nodeId=", setup.node_id, "*reason=", order_reason);
      }
   }

   int stale_deleted = 0, stale_kept = 0, stale_failed = 0;
   E0006_DeleteStalePendingOrders(desired_comments, stale_deleted, stale_kept, stale_failed);

   if(InpPrintOrderLogs)
   {
      string audit = "DAL_E0006_AUDIT *** build=" + string(DAL_E0006_BUILD)
         + "*runMode=" + run_mode
         + "*bars=" + IntegerToString(bars_count)
         + "*originNodes=" + IntegerToString(nodes_count)
         + "*internalNodes=" + IntegerToString(internal_nodes_count)
         + "*originEvents=" + IntegerToString(origin_events_count)
         + "*scanned=" + IntegerToString(scanned)
         + "*built=" + IntegerToString(built)
         + "*synced=" + IntegerToString(sent_or_synced)
         + "*buildReject=" + IntegerToString(build_reject)
         + "*orderReject=" + IntegerToString(order_reject)
         + "*sideCapSkip=" + IntegerToString(side_cap_skip)
         + "*internalHuntFilterSkip=" + IntegerToString(internal_hunt_filter_skip)
         + "*buyDesired=" + IntegerToString(buy_desired)
         + "*sellDesired=" + IntegerToString(sell_desired)
         + "*originL=" + IntegerToString(MathMax(1, InpOriginNodeL))
         + "*internalL=" + IntegerToString(MathMax(1, InpInternalNodeL))
         + "*onlyTradeRevisits=" + DAL_BoolToString(InpOnlyTradeRevisitZones)
         + "*revisitEntryAnchor=" + E0006_RevisitEntryAnchorModeToString()
         + "*revisitMinInternalHunts=" + IntegerToString(E0006_RevisitRequiredInternalHunts())
         + "*stopAnchor=" + E0006_StopAnchorModeToString()
         + "*rewardR=" + DoubleToString(InpRewardR, 2)
         + "*useInternalOppositeNodeTP=" + DAL_BoolToString(InpUseInternalOppositeNodeTP)
         + "*exitOppositeInternalNodeCount=" + IntegerToString(MathMax(1, InpExitOppositeInternalNodeCount))
         + "*tpChecked=" + IntegerToString(tp_checked)
         + "*tpWaiting=" + IntegerToString(tp_waiting)
         + "*tpModified=" + IntegerToString(tp_modified)
         + "*tpRejected=" + IntegerToString(tp_rejected)
         + "*staleDeleted=" + IntegerToString(stale_deleted)
         + "*staleKept=" + IntegerToString(stale_kept)
         + "*staleFailed=" + IntegerToString(stale_failed)
         + "*mode=ALL_LIVE_M0001_ZONES_WITH_REVISIT_SECONDARY_ANCHORS_NEW_BAR_ONLY";
      Print(audit);
   }
}

int OnInit()
{
   g_trade.SetExpertMagicNumber(InpMagicNumber);

   string sanity = "DAL_E0006_BUILD_SANITY *** build=" + string(DAL_E0006_BUILD)
      + "*symbol=" + E0006_Symbol()
      + "*tf=" + EnumToString(E0006_Timeframe())
      + "*module=EXECUTION_E0006_ALL_ZONE_TOUCH_LIMIT_FIXED_R"
      + "*source=M0001_LIVE_TERRITORY"
      + "*originL=" + IntegerToString(InpOriginNodeL)
      + "*internalL=" + IntegerToString(InpInternalNodeL)
      + "*onlyTradeRevisits=" + DAL_BoolToString(InpOnlyTradeRevisitZones)
      + "*revisitEntryAnchor=" + E0006_RevisitEntryAnchorModeToString()
      + "*stopAnchor=" + E0006_StopAnchorModeToString()
      + "*rewardR=" + DoubleToString(InpRewardR, 2)
      + "*newBarOnly=true";
   Print(sanity);

   if(InpRunOnInit)
      E0006_ProcessNewBar("init_backfill_sync");

   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   Comment("");
}

void OnTick()
{
   if(!E0006_HasNewOpenCandle())
      return;

   g_new_bar_counter++;
   int every = MathMax(1, InpUpdateEveryNBars);
   if((g_new_bar_counter % every) != 0)
      return;

   E0006_ProcessNewBar("new_closed_candle_sync");
}
