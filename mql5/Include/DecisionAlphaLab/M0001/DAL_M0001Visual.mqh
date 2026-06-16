#ifndef __DAL_M0001_VISUAL_MQH__
#define __DAL_M0001_VISUAL_MQH__

#include <DecisionAlphaLab/Common/DAL_ChartObjects.mqh>
#include <DecisionAlphaLab/Market/DAL_Bars.mqh>
#include <DecisionAlphaLab/StructuralNodes/LRule/DAL_LRuleTypes.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Types.mqh>

struct DALM0001VisualConfig
{
   string prefix;
   bool show_nodes;
   bool show_node_prices;
   bool show_active_from;
   bool show_events;
   bool show_rtv_labels;
   bool show_hunts;
   int max_nodes;
   int max_events;
   double chevron_points;
   double chevron_bars;
   int chevron_width;
};

void DAL_M0001DefaultVisualConfig(DALM0001VisualConfig &config)
{
   config.prefix = "DAL_MQL_M0001_";
   config.show_nodes = true;
   config.show_node_prices = false;
   config.show_active_from = false;
   config.show_events = false;
   config.show_rtv_labels = false;
   config.show_hunts = true;
   config.max_nodes = 120;
   config.max_events = 80;
   config.chevron_points = 70.0;
   config.chevron_bars = 0.28;
   config.chevron_width = 2;
}

double DAL_VisualPoint()
{
   double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
   if(point <= 0.0)
      point = 0.01;
   return point;
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
      DAL_DrawNodeChevron(visual.prefix, nodes[i], timeframe, visual.chevron_points, visual.chevron_bars, visual.chevron_width);

      if(visual.show_node_prices)
         DAL_DrawHLine(visual.prefix + "NODE_PRICE_" + IntegerToString(nodes[i].id), nodes[i].price, DAL_NodeColor(nodes[i].type));

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
