#ifndef __DAL_M0006_ALL_NODE_REACTION_BOXES_MQH__
#define __DAL_M0006_ALL_NODE_REACTION_BOXES_MQH__

#include <DecisionAlphaLab/Market/DAL_Bars.mqh>
#include <DecisionAlphaLab/StructuralNodes/LRule/DAL_LRuleDetector.mqh>

struct DALM0006ReactionBoxConfig
{
   string symbol;
   ENUM_TIMEFRAMES timeframe;
   int requested_closed_bars;
   int L;

   bool draw_chart;
   string object_prefix;
   int max_boxes;                 // 0 = draw all
   bool draw_back;
   bool fill;
   int line_width;

   int horizon_red;
   int horizon_green;
   int horizon_purple;

   double touch_buffer_points;
   double zone_end_retouch_buffer_points;
   double min_visual_box_points;   // 0 = exact zone height

   bool require_close_away_after_touch; // default false: draw every touched node
   int max_away_scan_bars;

   color color_pre_active;
   color color_pre_closed;
   color color_red;
   color color_green;
   color color_purple;
   color color_touch_no_away;
};

void DAL_M0006DefaultReactionBoxConfig(DALM0006ReactionBoxConfig &cfg)
{
   cfg.symbol = _Symbol;
   cfg.timeframe = (ENUM_TIMEFRAMES)_Period;
   cfg.requested_closed_bars = 50000;
   cfg.L = 5;

   cfg.draw_chart = true;
   cfg.object_prefix = "DAL_H6_BOX_";
   cfg.max_boxes = 0;
   cfg.draw_back = true;
   cfg.fill = true;
   cfg.line_width = 2;

   cfg.horizon_red = 20;
   cfg.horizon_green = 50;
   cfg.horizon_purple = 100;

   cfg.touch_buffer_points = 0.0;
   cfg.zone_end_retouch_buffer_points = 0.0;
   cfg.min_visual_box_points = 0.0;

   cfg.require_close_away_after_touch = false;
   cfg.max_away_scan_bars = 3;

   cfg.color_pre_active = clrOrange;
   cfg.color_pre_closed = clrSilver;
   cfg.color_red = clrRed;
   cfg.color_green = clrLime;
   cfg.color_purple = clrPurple;
   cfg.color_touch_no_away = clrYellow;
}

double DAL_M0006PointSafe(const string symbol)
{
   double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
   if(point <= 0.0)
      point = _Point;
   if(point <= 0.0)
      point = 0.01;
   return point;
}

void DAL_M0006DeleteObjectsByPrefix(const string prefix)
{
   int total = ObjectsTotal(0);
   for(int i = total - 1; i >= 0; i--)
   {
      string name = ObjectName(0, i);
      if(StringFind(name, prefix) == 0)
         ObjectDelete(0, name);
   }
}

bool DAL_M0006TouchedNode(
   const DALBar &bar,
   const DALLRuleNode &node,
   const double touch_buffer
)
{
   if(node.type == DAL_NODE_HIGH)
      return (bar.high >= node.price - touch_buffer);
   return (bar.low <= node.price + touch_buffer);
}

double DAL_M0006TouchExtreme(
   const DALBar &bar,
   const DALLRuleNode &node
)
{
   if(node.type == DAL_NODE_HIGH)
      return bar.high;
   return bar.low;
}

bool DAL_M0006RetouchedZoneEnd(
   const DALBar &bar,
   const DALLRuleNode &node,
   const double zone_end,
   const double retouch_buffer
)
{
   if(node.type == DAL_NODE_HIGH)
      return (bar.high >= zone_end - retouch_buffer);
   return (bar.low <= zone_end + retouch_buffer);
}

bool DAL_M0006CloseAwayConfirmed(
   const DALBar &bar,
   const DALLRuleNode &node
)
{
   if(node.type == DAL_NODE_HIGH)
      return (bar.close < node.price);
   return (bar.close > node.price);
}

int DAL_M0006FindAwayConfirm(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &node,
   const int touch_index,
   const int max_scan
)
{
   int end = MathMin(bars_count - 1, touch_index + MathMax(1, max_scan));
   for(int i = touch_index + 1; i <= end; i++)
   {
      if(DAL_M0006CloseAwayConfirmed(bars[i], node))
         return i;
   }
   return -1;
}

int DAL_M0006FindFirstTouch(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &node,
   const double touch_buffer
)
{
   int start = MathMax(0, node.active_from_index + 1);
   for(int i = start; i < bars_count; i++)
   {
      if(DAL_M0006TouchedNode(bars[i], node, touch_buffer))
         return i;
   }
   return -1;
}

int DAL_M0006FindZoneEndRetouch(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &node,
   const int touch_index,
   const double zone_end,
   const double retouch_buffer
)
{
   for(int i = touch_index + 1; i < bars_count; i++)
   {
      if(DAL_M0006RetouchedZoneEnd(bars[i], node, zone_end, retouch_buffer))
         return i;
   }
   return -1;
}

int DAL_M0006StageFromAge(const int age, const int h1, const int h2, const int h3)
{
   if(age >= h3) return 3;
   if(age >= h2) return 2;
   if(age >= h1) return 1;
   return 0;
}

color DAL_M0006ColorForBox(
   const int stage,
   const bool active,
   const bool away_ok,
   const DALM0006ReactionBoxConfig &cfg
)
{
   if(!away_ok)
      return cfg.color_touch_no_away;
   if(stage >= 3) return cfg.color_purple;
   if(stage == 2) return cfg.color_green;
   if(stage == 1) return cfg.color_red;
   if(active) return cfg.color_pre_active;
   return cfg.color_pre_closed;
}

string DAL_M0006StageText(const int stage, const int h1, const int h2, const int h3)
{
   if(stage >= 3) return "H" + IntegerToString(h3);
   if(stage == 2) return "H" + IntegerToString(h2);
   if(stage == 1) return "H" + IntegerToString(h1);
   return "PRE_H" + IntegerToString(h1);
}

bool DAL_M0006CreateReactionRectangle(
   const string name,
   const datetime t1,
   const datetime t2,
   const double node_price,
   const double touch_extreme,
   const ENUM_DALNodeType node_type,
   const color c,
   const DALM0006ReactionBoxConfig &cfg,
   const string tooltip
)
{
   if(!cfg.draw_chart)
      return false;

   datetime right_time = t2;
   if(right_time <= t1)
   {
      int sec = PeriodSeconds(cfg.timeframe);
      if(sec <= 0) sec = 60;
      right_time = t1 + sec;
   }

   double p1 = node_price;
   double p2 = touch_extreme;
   double point = DAL_M0006PointSafe(cfg.symbol);
   double min_h = MathMax(0.0, cfg.min_visual_box_points) * point;

   if(MathAbs(p2 - p1) < min_h)
   {
      if(node_type == DAL_NODE_HIGH)
         p2 = p1 + min_h;
      else
         p2 = p1 - min_h;
   }

   double top = MathMax(p1, p2);
   double bottom = MathMin(p1, p2);

   ResetLastError();
   ObjectDelete(0, name);
   if(!ObjectCreate(0, name, OBJ_RECTANGLE, 0, t1, top, right_time, bottom))
      return false;

   ObjectSetInteger(0, name, OBJPROP_COLOR, c);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, MathMax(1, cfg.line_width));
   ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_SOLID);
   ObjectSetInteger(0, name, OBJPROP_FILL, cfg.fill ? 1 : 0);
   ObjectSetInteger(0, name, OBJPROP_BACK, cfg.draw_back ? 1 : 0);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetString(0, name, OBJPROP_TOOLTIP, tooltip);
   return true;
}

bool DAL_M0006DrawTextMarker(
   const string name,
   const datetime t,
   const double price,
   const string txt,
   const color c,
   const string tooltip
)
{
   ResetLastError();
   ObjectDelete(0, name);
   if(!ObjectCreate(0, name, OBJ_TEXT, 0, t, price))
      return false;
   ObjectSetString(0, name, OBJPROP_TEXT, txt);
   ObjectSetString(0, name, OBJPROP_TOOLTIP, tooltip);
   ObjectSetInteger(0, name, OBJPROP_COLOR, c);
   ObjectSetInteger(0, name, OBJPROP_FONTSIZE, 8);
   ObjectSetInteger(0, name, OBJPROP_ANCHOR, ANCHOR_CENTER);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_BACK, false);
   return true;
}

bool DAL_M0006RunAllNodeReactionBoxes(const DALM0006ReactionBoxConfig &cfg)
{
   DALBar bars[];
   int bars_count = DAL_LoadBarsChronological(cfg.symbol, cfg.timeframe, cfg.requested_closed_bars, true, bars);
   if(bars_count <= 0)
   {
      Print("DAL_M0006_DIRECT_VISUAL_AUDIT *** error=no_bars_loaded*symbol=", cfg.symbol, "*tf=", EnumToString(cfg.timeframe));
      return false;
   }

   DALLRuleNode nodes[];
   int nodes_count = DAL_DetectLRuleNodes(bars, bars_count, MathMax(1, cfg.L), nodes);

   DAL_M0006DeleteObjectsByPrefix(cfg.object_prefix);

   int h1 = MathMax(1, cfg.horizon_red);
   int h2 = MathMax(h1 + 1, cfg.horizon_green);
   int h3 = MathMax(h2 + 1, cfg.horizon_purple);

   double point = DAL_M0006PointSafe(cfg.symbol);
   double touch_buffer = MathMax(0.0, cfg.touch_buffer_points) * point;
   double retouch_buffer = MathMax(0.0, cfg.zone_end_retouch_buffer_points) * point;

   int max_boxes = (cfg.max_boxes <= 0 ? 2147483647 : cfg.max_boxes);
   int touched = 0;
   int drawn = 0;
   int no_touch = 0;
   int away_confirmed = 0;
   int object_failures = 0;
   int retouched = 0;
   int active = 0;
   int red = 0;
   int green = 0;
   int purple = 0;
   int pre = 0;
   int last_error = 0;

   for(int n = nodes_count - 1; n >= 0 && drawn < max_boxes; n--)
   {
      int touch_index = DAL_M0006FindFirstTouch(bars, bars_count, nodes[n], touch_buffer);
      if(touch_index < 0)
      {
         no_touch++;
         continue;
      }

      touched++;

      int away_index = DAL_M0006FindAwayConfirm(bars, bars_count, nodes[n], touch_index, cfg.max_away_scan_bars);
      bool away_ok = (!cfg.require_close_away_after_touch || away_index > 0);
      if(away_index > 0) away_confirmed++;

      double zone_end = DAL_M0006TouchExtreme(bars[touch_index], nodes[n]);
      int retouch_index = DAL_M0006FindZoneEndRetouch(bars, bars_count, nodes[n], touch_index, zone_end, retouch_buffer);
      bool is_active = (retouch_index < 0);
      if(is_active) active++; else retouched++;

      int effective_end = is_active ? (bars_count - 1) : (retouch_index - 1);
      if(effective_end < touch_index) effective_end = touch_index;
      int age_after_touch = effective_end - touch_index;
      int stage = DAL_M0006StageFromAge(age_after_touch, h1, h2, h3);
      if(stage >= 3) purple++;
      else if(stage == 2) green++;
      else if(stage == 1) red++;
      else pre++;

      color c = DAL_M0006ColorForBox(stage, is_active, away_ok, cfg);
      string side = (nodes[n].type == DAL_NODE_HIGH ? "HIGH" : "LOW");
      string stage_text = DAL_M0006StageText(stage, h1, h2, h3);
      string state_text = is_active ? "ACTIVE" : "CLOSED";
      string name = cfg.object_prefix + "BOX_" + stage_text + "_" + state_text + "_" + IntegerToString(nodes[n].id) + "_" + side;

      string tip = "H6 ALL-NODE BOX"
         + " side=" + side
         + " nodeId=" + IntegerToString(nodes[n].id)
         + " origin=" + TimeToString(nodes[n].time)
         + " known=" + TimeToString(nodes[n].active_from_time)
         + " touch=" + TimeToString(bars[touch_index].time)
         + " awayConfirm=" + (away_index > 0 ? TimeToString(bars[away_index].time) : "NONE")
         + " retouch=" + (retouch_index > 0 ? TimeToString(bars[retouch_index].time) : "NONE")
         + " active=" + IntegerToString(is_active ? 1 : 0)
         + " candlesAfterTouchNoZoneEndRetouch=" + IntegerToString(age_after_touch)
         + " nodePrice=" + DoubleToString(nodes[n].price, _Digits)
         + " touchExtreme=" + DoubleToString(zone_end, _Digits)
         + " noRegimeFilter=1";

      if(DAL_M0006CreateReactionRectangle(name, nodes[n].time, bars[touch_index].time, nodes[n].price, zone_end, nodes[n].type, c, cfg, tip))
      {
         drawn++;
      }
      else
      {
         object_failures++;
         last_error = GetLastError();
      }

      // Small origin/touch markers only after the rectangle, and only if still under object budget.
      if(drawn < max_boxes)
      {
         string m1 = cfg.object_prefix + "O_" + IntegerToString(nodes[n].id) + "_" + side;
         if(DAL_M0006DrawTextMarker(m1, nodes[n].time, nodes[n].price, "O", clrWhite, tip + " marker=origin"))
            drawn++;
      }
      if(drawn < max_boxes)
      {
         string m2 = cfg.object_prefix + "T_" + IntegerToString(nodes[n].id) + "_" + side;
         if(DAL_M0006DrawTextMarker(m2, bars[touch_index].time, zone_end, "T", c, tip + " marker=touch"))
            drawn++;
      }
   }

   ChartRedraw(0);

   string line = "DAL_M0006_DIRECT_VISUAL_AUDIT *** build=1.00"
      + "*engine=direct_lrule_nodes_no_event_dependency"
      + "*symbol=" + cfg.symbol
      + "*tf=" + EnumToString(cfg.timeframe)
      + "*bars=" + IntegerToString(bars_count)
      + "*nodes=" + IntegerToString(nodes_count)
      + "*touched=" + IntegerToString(touched)
      + "*noTouch=" + IntegerToString(no_touch)
      + "*drawnObjects=" + IntegerToString(drawn)
      + "*objectFailures=" + IntegerToString(object_failures)
      + "*lastObjectError=" + IntegerToString(last_error)
      + "*awayConfirmed=" + IntegerToString(away_confirmed)
      + "*activeNoZoneEndRetouch=" + IntegerToString(active)
      + "*zoneEndRetouched=" + IntegerToString(retouched)
      + "*preH" + IntegerToString(h1) + "=" + IntegerToString(pre)
      + "*redH" + IntegerToString(h1) + "=" + IntegerToString(red)
      + "*greenH" + IntegerToString(h2) + "=" + IntegerToString(green)
      + "*purpleH" + IntegerToString(h3) + "=" + IntegerToString(purple)
      + "*scope=all_raw_nodes_no_regime_filter"
      + "*box=time_node_origin_to_first_touch_price_node_to_touch_extreme"
      + "*colorRule=candles_after_touch_without_zone_end_retouch";
   Print(line);

   return (drawn > 0 && object_failures == 0);
}

#endif
