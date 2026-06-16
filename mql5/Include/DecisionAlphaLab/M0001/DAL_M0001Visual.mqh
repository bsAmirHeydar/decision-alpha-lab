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
   bool show_hunts;
   bool show_expansion_extreme_lines;
   bool show_live_hunt_zones;
   bool show_invalidated_hunt_zones;
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
   config.show_hunts = true;
   config.show_expansion_extreme_lines = false;
   config.show_live_hunt_zones = false;
   config.show_invalidated_hunt_zones = false;
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

   for(int i = 0; i < limit; i++)
   {
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

void DAL_M0001DrawEvents(
   const DALM0001Event &events[],
   const int count,
   const DALM0001VisualConfig &visual
)
{
   int limit = count;
   if(visual.max_events > 0)
      limit = MathMin(limit, visual.max_events);

   for(int i = 0; i < limit; i++)
   {
      DALM0001Event e = events[i];
      string id = visual.prefix + "EV_" + IntegerToString(e.id);

      if(visual.show_events)
         DAL_DrawRectangle(id + "_BOX", e.entry_time, e.territory_upper, e.exit_time, e.territory_lower, DAL_RtvColor(e.rtv), true, false);

      if(visual.show_rtv_labels)
         DAL_DrawTextLabel(id + "_RTV", e.entry_time, e.territory_upper, "RTV " + DoubleToString(e.rtv, 2), DAL_RtvColor(e.rtv), 8);

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

void DAL_M0001DrawExtremeLink(
   const string prefix,
   const DALM0001NodeAuditState &state
)
{
   string id = prefix + "EXTREME_LINK_" + IntegerToString(state.node_id);
   color c = DAL_M0001AuditColor(state.node_type, state.invalidated);

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
   const bool show_invalidated
)
{
   if(state.invalidated && !show_invalidated)
      return;

   datetime end_time = state.current_time;
   color c = DAL_M0001AuditColor(state.node_type, state.invalidated);

   if(state.invalidated && state.invalidated_time > 0)
      end_time = state.invalidated_time;

   datetime start_time = state.node_time;

   if(end_time <= start_time)
      return;

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

void DAL_M0001DrawAuditStates(
   const DALM0001NodeAuditState &states[],
   const int count,
   const DALM0001VisualConfig &visual
)
{
   int limit = count;
   if(visual.max_audit_states > 0)
      limit = MathMin(limit, visual.max_audit_states);

   for(int i = 0; i < limit; i++)
   {
      if(visual.show_expansion_extreme_lines)
         DAL_M0001DrawExtremeLink(visual.prefix, states[i]);

      if(visual.show_live_hunt_zones)
         DAL_M0001DrawLiveHuntZone(visual.prefix, states[i], visual.show_invalidated_hunt_zones);
   }
}

void DAL_M0001DrawSummary(
   const string prefix,
   const int bars_count,
   const int nodes_count,
   const int events_count,
   const DALM0001Config &config
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
   ObjectSetString(
      0,
      name,
      OBJPROP_TEXT,
      "Decision Alpha Lab | M0001 MQL-native\n"
      + "bars=" + IntegerToString(bars_count)
      + " nodes=" + IntegerToString(nodes_count)
      + " events=" + IntegerToString(events_count)
      + "\nL=" + IntegerToString(config.L)
      + " zone=" + DoubleToString(config.zone_ratio, 2)
      + " gap=" + IntegerToString(config.exit_gap)
   );
}

#endif
