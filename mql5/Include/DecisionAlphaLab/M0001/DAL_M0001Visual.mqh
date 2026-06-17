#ifndef __DAL_M0001_VISUAL_MQH__
#define __DAL_M0001_VISUAL_MQH__

#include <DecisionAlphaLab/Common/DAL_ChartObjects.mqh>
#include <DecisionAlphaLab/Market/DAL_Bars.mqh>
#include <DecisionAlphaLab/StructuralNodes/LRule/DAL_LRuleTypes.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Types.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001AuditState.mqh>

struct DALM0001VisualConfig
{
   string prefix;
   bool show_nodes;
   bool show_node_prices;
   bool show_node_price_lines;
   bool show_active_from;
   bool show_events;
   bool show_rtv_labels;
   bool show_revisit_labels;
   bool show_node_state_labels;
   bool show_hunts;
   bool show_node_visibility_debug;
   bool show_expansion_extreme_lines;
   bool show_consumed_extreme_history;
   bool show_live_hunt_zones;
   bool show_invalidated_hunt_zones;
   bool show_consumed_hunt_zone_history;
   bool show_consumed_node_markers;
   int max_nodes;
   int max_events;
   int max_audit_states;
   int node_marker_style; // 0 = arrow marker, 1 = chevron marker
   int node_arrow_width;
   double chevron_points;
   double chevron_bars;
   int chevron_width;
   double high_node_price_text_gap_points;
   double low_node_price_text_gap_points;
   int node_price_text_font_size;
   bool use_time_window;
   datetime time_window_from;
   datetime time_window_to;
};

void DAL_M0001DefaultVisualConfig(DALM0001VisualConfig &config)
{
   config.prefix = "DAL_MQL_M0001_";
   config.show_nodes = true;
   config.show_node_prices = true;
   config.show_node_price_lines = false;
   config.show_active_from = false;
   config.show_events = false;
   config.show_rtv_labels = false;
   config.show_revisit_labels = true;
   config.show_node_state_labels = true;
   config.show_hunts = true;
   config.show_node_visibility_debug = true;
   config.show_expansion_extreme_lines = false;
   config.show_consumed_extreme_history = true;
   config.show_live_hunt_zones = false;
   config.show_invalidated_hunt_zones = false;
   config.show_consumed_hunt_zone_history = true;
   config.show_consumed_node_markers = true;
   config.max_nodes = 120;
   config.max_events = 80;
   config.max_audit_states = 80;
   config.node_marker_style = 0;
   config.node_arrow_width = 2;
   config.chevron_points = 70.0;
   config.chevron_bars = 0.28;
   config.chevron_width = 2;
   config.high_node_price_text_gap_points = 120.0;
   config.low_node_price_text_gap_points = 120.0;
   config.node_price_text_font_size = 9;
   config.use_time_window = false;
   config.time_window_from = 0;
   config.time_window_to = 0;
}

double DAL_VisualPoint()
{
   double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
   if(point <= 0.0)
      point = 0.01;
   return point;
}

double DAL_NodeLabelPrice(
   const DALLRuleNode &node,
   const double high_gap_points,
   const double low_gap_points
)
{
   double point = DAL_VisualPoint();

   if(node.type == DAL_NODE_HIGH)
      return node.price + high_gap_points * point;

   return node.price - low_gap_points * point;
}


void DAL_DrawNodeArrow(
   const string prefix,
   const DALLRuleNode &node,
   const int width
)
{
   string id = prefix + "NODE_" + IntegerToString(node.id);
   color c = DAL_NodeColor(node.type);

   int arrow_code = 233;
   int anchor = ANCHOR_TOP;

   if(node.type == DAL_NODE_HIGH)
   {
      arrow_code = 234;      // down arrow
      anchor = ANCHOR_BOTTOM;
   }

   DAL_DrawArrowMarker(id, node.time, node.price, arrow_code, c, width, anchor);
}

void DAL_DrawNodeChevron(
   const string prefix,
   const DALLRuleNode &node,
   const ENUM_TIMEFRAMES timeframe,
   const double chevron_points,
   const double chevron_bars,
   const int width
)
{
   double point = DAL_VisualPoint();
   double gap = chevron_points * point;

   int seconds = PeriodSeconds(timeframe);
   if(seconds <= 0)
      seconds = 60;
   int wing_seconds = (int)MathRound((double)seconds * chevron_bars);
   if(wing_seconds < 1)
      wing_seconds = 1;

   double wing_price = node.price;
   if(node.type == DAL_NODE_HIGH)
      wing_price = node.price + gap;
   else
      wing_price = node.price - gap;

   string id = prefix + "NODE_" + IntegerToString(node.id);
   color c = DAL_NodeColor(node.type);

   DAL_DrawTrend(id + "_L", node.time, node.price, node.time - wing_seconds, wing_price, c, width);
   DAL_DrawTrend(id + "_R", node.time, node.price, node.time + wing_seconds, wing_price, c, width);
}

void DAL_DrawNodePriceLabel(
   const string prefix,
   const DALLRuleNode &node,
   const double high_gap_points,
   const double low_gap_points,
   const int font_size
)
{
   double label_price = DAL_NodeLabelPrice(node, high_gap_points, low_gap_points);

   ENUM_ANCHOR_POINT anchor = ANCHOR_CENTER;
   if(node.type == DAL_NODE_HIGH)
      anchor = ANCHOR_LOWER;
   else
      anchor = ANCHOR_UPPER;

   string id = prefix + "NODE_PRICE_TEXT_" + IntegerToString(node.id);
   string text = DoubleToString(node.price, _Digits);
   DAL_DrawTextLabelAnchored(id, node.time, label_price, text, DAL_NodeColor(node.type), font_size, anchor);
}


bool DAL_M0001TimeInVisualWindow(
   const DALM0001VisualConfig &visual,
   const datetime t
)
{
   if(!visual.use_time_window)
      return true;

   return (t >= visual.time_window_from && t <= visual.time_window_to);
}

bool DAL_M0001IntervalIntersectsVisualWindow(
   const DALM0001VisualConfig &visual,
   datetime t1,
   datetime t2
)
{
   if(!visual.use_time_window)
      return true;

   if(t1 > t2)
   {
      datetime tmp = t1;
      t1 = t2;
      t2 = tmp;
   }

   if(t2 < visual.time_window_from)
      return false;

   if(t1 > visual.time_window_to)
      return false;

   return true;
}

color DAL_RtvColor(const double rtv)
{
   if(rtv >= 1.50)
      return clrRed;
   if(rtv >= 1.20)
      return clrOrange;
   if(rtv >= 1.00)
      return clrGold;
   return clrDeepSkyBlue;
}

string DAL_M0001RtvLabelText(const DALM0001Event &event)
{
   if(!event.rtv_ready || event.rtv_sample_length <= 0)
      return "RTV n/a";

   return "RTV " + DoubleToString(event.rtv, 2);
}

color DAL_M0001RtvLabelColor(const DALM0001Event &event)
{
   if(!event.rtv_ready || event.rtv_sample_length <= 0)
      return clrSilver;

   return DAL_RtvColor(event.rtv);
}

void DAL_M0001DrawNodes(
   const DALLRuleNode &nodes[],
   const int count,
   const DALM0001VisualConfig &visual,
   const ENUM_TIMEFRAMES timeframe
)
{
   if(!visual.show_nodes)
      return;

   int limit = count;
   if(visual.max_nodes > 0)
      limit = MathMin(limit, visual.max_nodes);

   // Positive visual caps show the latest N nodes, not the oldest N nodes.
   int start = count - limit;
   if(start < 0)
      start = 0;

   for(int i = start; i < count; i++)
   {
      if(!DAL_M0001TimeInVisualWindow(visual, nodes[i].time))
         continue;

      // Strict clean-node mode:
      // arrow + optional local price text only.
      DAL_DrawNodeArrow(visual.prefix, nodes[i], visual.node_arrow_width);

      if(visual.show_node_prices)
         DAL_DrawNodePriceLabel(
            visual.prefix,
            nodes[i],
            visual.high_node_price_text_gap_points,
            visual.low_node_price_text_gap_points,
            visual.node_price_text_font_size
         );

      // Full horizontal node-price lines are intentionally disabled.
      // Price visibility is handled by local text labels via show_node_prices.
      if(visual.show_active_from)
         DAL_DrawVLine(visual.prefix + "ACTIVE_" + IntegerToString(nodes[i].id), nodes[i].active_from_time, clrSilver);
   }
}

bool DAL_M0001IsActualRevisit(
   const DALM0001Event &event,
   const DALM0001Config &config
)
{
   // TOUCH mode is one-shot, so it does not expose revisit labels.
   if(DAL_M0001ConsumesOnTouch(config))
      return false;

   // REV#0 is the first visit. True revisit starts from REV#1.
   return event.revisit_id > 0;
}

string DAL_M0001RevisitOnlyText(const DALM0001Event &event)
{
   return "REVISIT#" + IntegerToString(event.revisit_id);
}

color DAL_M0001RevisitOnlyColor(const DALM0001Event &event)
{
   // Color the revisit text by the structural side:
   // LOW / valley revisits  -> blue
   // HIGH / peak revisits   -> red
   if(event.node_type == DAL_NODE_LOW)
      return clrDeepSkyBlue;

   return clrRed;
}

double DAL_M0001EventLabelPrice(const DALM0001Event &event)
{
   double gap = 60.0 * DAL_VisualPoint();

   if(event.node_type == DAL_NODE_HIGH)
      return event.territory_lower - gap;

   return event.territory_upper + gap;
}

void DAL_M0001DrawRevisitLabel(
   const string prefix,
   const DALM0001Event &event,
   const DALM0001Config &config
)
{
   if(!DAL_M0001IsActualRevisit(event, config))
      return;

   string id = prefix + "REV_LABEL_" + IntegerToString(event.id);
   color c = DAL_M0001RevisitOnlyColor(event);

   ENUM_ANCHOR_POINT anchor = ANCHOR_CENTER;
   if(event.node_type == DAL_NODE_HIGH)
      anchor = ANCHOR_UPPER;
   else
      anchor = ANCHOR_LOWER;

   DAL_DrawTextLabelAnchored(
      id,
      event.entry_time,
      DAL_M0001EventLabelPrice(event),
      DAL_M0001RevisitOnlyText(event),
      c,
      8,
      anchor
   );
}

void DAL_M0001DrawEvents(
   const DALM0001Event &events[],
   const int count,
   const DALM0001VisualConfig &visual,
   const DALM0001Config &config
)
{
   int limit = count;
   if(visual.max_events > 0)
      limit = MathMin(limit, visual.max_events);

   // Positive visual caps show the latest N events.
   int start = count - limit;
   if(start < 0)
      start = 0;

   for(int i = start; i < count; i++)
   {
      DALM0001Event e = events[i];

      if(!DAL_M0001IntervalIntersectsVisualWindow(visual, e.entry_time, e.exit_time))
         continue;

      string id = visual.prefix + "EV_" + IntegerToString(e.id);

      if(visual.show_events)
         DAL_DrawRectangle(id + "_BOX", e.entry_time, e.territory_upper, e.exit_time, e.territory_lower, DAL_RtvColor(e.rtv), true, false);

      if(visual.show_revisit_labels)
         DAL_M0001DrawRevisitLabel(visual.prefix, e, config);

      if(visual.show_rtv_labels)
         DAL_DrawTextLabel(id + "_RTV", e.exit_time, e.territory_upper, DAL_M0001RtvLabelText(e), DAL_M0001RtvLabelColor(e), 8);

      if(visual.show_hunts && e.hunted)
         DAL_DrawTextLabel(id + "_HUNT", e.exit_time, e.node_price, "HUNT", clrRed, 8);
   }
}


color DAL_M0001AuditColor(const ENUM_DALNodeType node_type, const bool invalidated)
{
   if(invalidated)
      return clrDimGray;

   return DAL_NodeColor(node_type);
}

color DAL_M0001RevisitedZoneColor(const DALM0001NodeAuditState &state)
{
   // After at least one confirmed revisit, the live zone changes color so the
   // chart distinguishes revisited territory from fresh territory.
   // Peak / HIGH revisited zones   -> purple
   // Valley / LOW revisited zones  -> blue
   if(state.consumed)
      return DAL_M0001AuditColor(state.node_type, true);

   if(state.confirmed_touch_count > 0)
   {
      if(state.node_type == DAL_NODE_HIGH)
         return clrPurple;

      return clrDeepSkyBlue;
   }

   return DAL_M0001AuditColor(state.node_type, false);
}

void DAL_M0001DrawExtremeLink(
   const string prefix,
   const DALM0001NodeAuditState &state,
   const bool show_consumed_history
)
{
   // Active node: draw live node -> current expansion extreme link.
   // Consumed node: keep the final historical extreme link, but do not
   // continue updating/extending it after the consume candle.
   if(state.consumed || !state.active)
   {
      if(!show_consumed_history)
         return;

      if(state.consumed_time <= 0)
         return;
   }

   string id = prefix + "EXTREME_LINK_" + IntegerToString(state.node_id);
   color c = DAL_M0001AuditColor(state.node_type, state.consumed);

   DAL_DrawTrend(
      id,
      state.node_time,
      state.node_price,
      state.extreme_time,
      state.expansion_extreme,
      c,
      1,
      STYLE_DASH
   );

   string text_id = prefix + "EXTREME_TEXT_" + IntegerToString(state.node_id);
   string text = "EXT " + DoubleToString(state.expansion_extreme, _Digits);
   DAL_DrawTextLabelAnchored(text_id, state.extreme_time, state.expansion_extreme, text, c, 7, ANCHOR_CENTER);
}

void DAL_M0001DrawLiveHuntZone(
   const string prefix,
   const DALM0001NodeAuditState &state,
   const bool show_consumed_history
)
{
   // Visual rule:
   // The rectangle's time origin is always the structural node itself.
   //
   // Calculation rule remains separate:
   // after a confirmed revisit, tracking_cycle_start_time still resets the
   // post-visit extreme/zone calculation, but the visible rectangle continues
   // to start from the node candle so the structural origin stays obvious.
   datetime start_time = state.node_time;
   if(start_time <= 0)
      start_time = state.active_from_time;
   if(start_time <= 0)
      start_time = state.tracking_cycle_start_time;

   datetime end_time = state.current_time;

   // Active node: draw live territory from the node-origin time to current bar.
   // Revisit extreme reset changes the price geometry, not the time origin.
   // Consumed node: keep historical zone drawn, but terminate it at consume candle.
   if(state.consumed || !state.active)
   {
      if(!show_consumed_history)
         return;

      if(state.consumed_time <= 0)
         return;

      end_time = state.consumed_time;
   }

   if(end_time <= start_time)
      return;

   color c = DAL_M0001RevisitedZoneColor(state);

   string id = prefix + "LIVE_HUNT_ZONE_" + IntegerToString(state.node_id);
   DAL_DrawRectangle(
      id,
      start_time,
      state.territory_upper,
      end_time,
      state.territory_lower,
      c,
      true,
      false
   );
}

string DAL_M0001NodeStateText(
   const DALM0001NodeAuditState &state,
   const DALM0001Config &config
)
{
   bool touch_mode = DAL_M0001ConsumesOnTouch(config);

   if(state.consumed)
   {
      if(touch_mode)
         return "CONSUMED:" + DAL_M0001ConsumeReasonToString(state.consume_reason);

      return "CONSUMED:" + DAL_M0001ConsumeReasonToString(state.consume_reason)
         + " revs=" + IntegerToString(state.confirmed_touch_count);
   }

   if(state.pending_touch)
   {
      if(touch_mode)
         return "PENDING TOUCH_EVENT out="
            + IntegerToString(state.pending_touch_outside_count)
            + "/" + IntegerToString(config.exit_gap);

      return "PENDING REV#" + IntegerToString(state.pending_touch_revisit_id)
         + " out=" + IntegerToString(state.pending_touch_outside_count)
         + "/" + IntegerToString(config.exit_gap);
   }

   if(state.confirmed_touch_count > 0)
   {
      if(touch_mode)
         return "ACTIVE_AFTER_TOUCH? revs="
            + IntegerToString(state.confirmed_touch_count);

      return "REVISITED LIVE revs="
         + IntegerToString(state.confirmed_touch_count)
         + " next=REV#" + IntegerToString(state.next_revisit_id)
         + " age=" + IntegerToString(state.bars_since_last_touch_confirmed)
         + " reset@" + IntegerToString(state.tracking_cycle_start_index);
   }

   if(touch_mode)
      return "FRESH LIVE TOUCH_EVENT";

   return "FRESH LIVE next=REV#0";
}

double DAL_M0001NodeStateLabelPrice(const DALM0001NodeAuditState &state)
{
   double gap = 180.0 * DAL_VisualPoint();

   if(state.node_type == DAL_NODE_HIGH)
      return state.node_price + gap;

   return state.node_price - gap;
}

void DAL_M0001DrawNodeStateLabel(
   const string prefix,
   const DALM0001NodeAuditState &state,
   const DALM0001Config &config
)
{
   string id = prefix + "NODE_STATE_" + IntegerToString(state.node_id);

   color c = DAL_M0001AuditColor(state.node_type, state.consumed);
   if(state.pending_touch)
      c = clrGold;
   if(state.revisited_live)
      c = clrDeepSkyBlue;
   if(state.hunted)
      c = clrRed;
   if(state.consumed && state.consume_reason == DAL_M0001_CONSUMED_TOUCH)
      c = clrSilver;

   ENUM_ANCHOR_POINT anchor = ANCHOR_CENTER;
   if(state.node_type == DAL_NODE_HIGH)
      anchor = ANCHOR_LOWER;
   else
      anchor = ANCHOR_UPPER;

   DAL_DrawTextLabelAnchored(
      id,
      state.current_time,
      DAL_M0001NodeStateLabelPrice(state),
      DAL_M0001NodeStateText(state, config),
      c,
      7,
      anchor
   );
}

void DAL_M0001DrawConsumedMarker(
   const string prefix,
   const DALM0001NodeAuditState &state
)
{
   if(!state.consumed || state.consumed_time <= 0)
      return;

   string id = prefix + "CONSUMED_" + IntegerToString(state.node_id);
   string text = "CONSUMED:" + DAL_M0001ConsumeReasonToString(state.consume_reason);

   double y = state.node_price;
   double gap = 80.0 * DAL_VisualPoint();

   ENUM_ANCHOR_POINT anchor = ANCHOR_CENTER;
   if(state.node_type == DAL_NODE_HIGH)
   {
      y = state.node_price - gap;
      anchor = ANCHOR_UPPER;
   }
   else
   {
      y = state.node_price + gap;
      anchor = ANCHOR_LOWER;
   }

   DAL_DrawTextLabelAnchored(id, state.consumed_time, y, text, clrSilver, 7, anchor);
}

void DAL_M0001DrawAuditStates(
   const DALM0001NodeAuditState &states[],
   const int count,
   const DALM0001VisualConfig &visual,
   const DALM0001Config &config
)
{
   int limit = count;
   if(visual.max_audit_states > 0)
      limit = MathMin(limit, visual.max_audit_states);

   // Positive visual caps show the latest N audit states.
   int start = count - limit;
   if(start < 0)
      start = 0;

   for(int i = start; i < count; i++)
   {
      if(visual.show_expansion_extreme_lines
         && DAL_M0001IntervalIntersectsVisualWindow(visual, states[i].node_time, states[i].extreme_time))
      {
         DAL_M0001DrawExtremeLink(visual.prefix, states[i], visual.show_consumed_extreme_history);
      }

      datetime zone_end = states[i].current_time;
      if(states[i].consumed && states[i].consumed_time > 0)
         zone_end = states[i].consumed_time;

      if(visual.show_live_hunt_zones
         && DAL_M0001IntervalIntersectsVisualWindow(visual, states[i].node_time, zone_end))
      {
         DAL_M0001DrawLiveHuntZone(visual.prefix, states[i], visual.show_consumed_hunt_zone_history);
      }

      if(visual.show_consumed_node_markers
         && DAL_M0001TimeInVisualWindow(visual, states[i].consumed_time))
      {
         DAL_M0001DrawConsumedMarker(visual.prefix, states[i]);
      }

      if(visual.show_node_state_labels
         && DAL_M0001TimeInVisualWindow(visual, states[i].current_time))
      {
         DAL_M0001DrawNodeStateLabel(visual.prefix, states[i], config);
      }
   }
}

string DAL_NodeTypeShortText(const ENUM_DALNodeType node_type)
{
   if(node_type == DAL_NODE_HIGH)
      return "HIGH";
   return "LOW";
}

string DAL_VisualCapText(const int total, const int max_items)
{
   if(max_items <= 0)
      return "all/" + IntegerToString(total);

   int shown = MathMin(total, max_items);
   return "latest " + IntegerToString(shown) + "/" + IntegerToString(total);
}

string DAL_LatestNodeDebugText(const DALLRuleNode &nodes[], const int nodes_count)
{
   if(nodes_count <= 0)
      return "last_node=none";

   DALLRuleNode node = nodes[nodes_count - 1];

   return "last_node="
      + DAL_NodeTypeShortText(node.type)
      + " id=" + IntegerToString(node.id)
      + " idx=" + IntegerToString(node.index)
      + " t=" + TimeToString(node.time, TIME_DATE | TIME_MINUTES)
      + " p=" + DoubleToString(node.price, _Digits)
      + " active=" + TimeToString(node.active_from_time, TIME_DATE | TIME_MINUTES);
}

void DAL_M0001DrawSummary(
   const string prefix,
   const int bars_count,
   const int nodes_count,
   const int events_count,
   const int audit_states_count,
   const DALM0001Config &config,
   const DALM0001VisualConfig &visual,
   const DALLRuleNode &nodes[]
)
{
   string name = prefix + "SUMMARY";
   ObjectCreate(0, name, OBJ_LABEL, 0, 0, 0);
   ObjectSetInteger(0, name, OBJPROP_CORNER, CORNER_LEFT_UPPER);
   ObjectSetInteger(0, name, OBJPROP_XDISTANCE, 12);
   ObjectSetInteger(0, name, OBJPROP_YDISTANCE, 18);
   ObjectSetInteger(0, name, OBJPROP_COLOR, clrLightSteelBlue);
   ObjectSetInteger(0, name, OBJPROP_FONTSIZE, 10);
   ObjectSetString(0, name, OBJPROP_FONT, "Consolas");

   string text =
      "Decision Alpha Lab | M0001 MQL-native\n"
      + "bars=" + IntegerToString(bars_count)
      + " nodes=" + IntegerToString(nodes_count)
      + " events=" + IntegerToString(events_count)
      + " audit=" + IntegerToString(audit_states_count)
      + "\nL=" + IntegerToString(config.L)
      + " zone=" + DoubleToString(config.zone_ratio, 2)
      + " gap=" + IntegerToString(config.exit_gap)
      + " consume=" + DAL_M0001ConsumeModeToString(config.consume_mode);

   if(visual.show_node_visibility_debug)
   {
      text = text
         + "\nnode_draw=" + DAL_VisualCapText(nodes_count, visual.max_nodes)
         + " audit_draw=" + DAL_VisualCapText(audit_states_count, visual.max_audit_states)
         + "\nviewport=" + (visual.use_time_window ? "on" : "off")
         + (visual.use_time_window ? (" " + TimeToString(visual.time_window_from, TIME_DATE | TIME_MINUTES) + " -> " + TimeToString(visual.time_window_to, TIME_DATE | TIME_MINUTES)) : "")
         + "\n" + DAL_LatestNodeDebugText(nodes, nodes_count);
   }

   ObjectSetString(0, name, OBJPROP_TEXT, text);
}


#endif
