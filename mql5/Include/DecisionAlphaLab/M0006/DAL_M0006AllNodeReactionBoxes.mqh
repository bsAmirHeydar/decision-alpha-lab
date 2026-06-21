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
   bool include_live_bar;
   bool preserve_existing_on_empty_update;
   bool preserve_matured_boxes;
   int min_bars_for_update;
   string object_prefix;
   int max_boxes;                 // 0 = draw all boxes/markers
   int max_levels;                // 0 = draw all levels
   bool draw_back;
   bool fill;
   int line_width;
   bool draw_node_levels;
   bool boxes_only_mode;

   bool draw_boxes_only_after_horizon;
   bool show_pre_stage;
   bool show_red_stage;
   bool show_green_stage;
   bool show_purple_stage;
   bool show_consumed_boxes;
   bool show_origin_touch_markers;
   bool show_untouched_levels;
   int box_left_anchor_mode;       // 0=node pivot/origin time, 1=known/active_from time
   int box_right_anchor_mode;      // 0=touch candle open time, 1=touch candle close time

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
   color color_untouched_level;
};

void DAL_M0006DefaultReactionBoxConfig(DALM0006ReactionBoxConfig &cfg)
{
   cfg.symbol = _Symbol;
   cfg.timeframe = (ENUM_TIMEFRAMES)_Period;
   cfg.requested_closed_bars = 50000;
   cfg.L = 5;

   cfg.draw_chart = true;
   cfg.include_live_bar = true;
   cfg.preserve_existing_on_empty_update = true;
   cfg.preserve_matured_boxes = true;
   cfg.min_bars_for_update = 0;
   cfg.object_prefix = "DAL_H6_BOX_";
   cfg.max_boxes = 0;
   cfg.max_levels = 0;
   cfg.draw_back = true;
   cfg.fill = true;
   cfg.line_width = 2;
   cfg.draw_node_levels = true;
   cfg.boxes_only_mode = false;

   cfg.draw_boxes_only_after_horizon = true;
   cfg.show_pre_stage = false;
   cfg.show_red_stage = true;
   cfg.show_green_stage = true;
   cfg.show_purple_stage = true;
   cfg.show_consumed_boxes = false;
   cfg.show_origin_touch_markers = true;
   cfg.show_untouched_levels = false;
   cfg.box_left_anchor_mode = 0;
   cfg.box_right_anchor_mode = 0;

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
   cfg.color_untouched_level = clrDeepSkyBlue;
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

void DAL_M0006DeleteVolatileObjectsByPrefix(
   const string prefix,
   const bool preserve_matured_boxes
)
{
   int total = ObjectsTotal(0);
   string box_prefix = prefix + "BOX_";
   for(int i = total - 1; i >= 0; i--)
   {
      string name = ObjectName(0, i);
      if(StringFind(name, prefix) != 0)
         continue;

      // Matured reaction boxes are persistent. Once created, they are never deleted by live updates.
      // They are only color-updated if the same node reaches a higher horizon.
      if(preserve_matured_boxes && StringFind(name, box_prefix) == 0)
         continue;

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

string DAL_M0006TouchStateName(
   const bool touched,
   const bool away_ok,
   const bool consumed,
   const int stage
)
{
   if(!touched) return "UNTOUCHED_LEVEL";
   if(!away_ok) return "TOUCHED_NO_REVERSAL_CONFIRM";
   if(consumed) return "CONSUMED_ZONE_END_RETOUCHED";
   if(stage <= 0) return "WATCHING_AFTER_TOUCH_NOT_MATURED";
   return "MATURED_DRAW_BOX";
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

color DAL_M0006ColorForLevel(
   const int stage,
   const bool active,
   const bool away_ok,
   const DALM0006ReactionBoxConfig &cfg
)
{
   // Levels are only live references. The official maturity/stage signal is the box.
   // This prevents the chart from looking like a zone has matured before the post-touch input horizon is reached.
   return cfg.color_untouched_level;
}

string DAL_M0006StageText(const int stage, const int h1, const int h2, const int h3)
{
   if(stage >= 3) return "H" + IntegerToString(h3);
   if(stage == 2) return "H" + IntegerToString(h2);
   if(stage == 1) return "H" + IntegerToString(h1);
   return "PRE_H" + IntegerToString(h1);
}

bool DAL_M0006StageVisible(const int stage, const DALM0006ReactionBoxConfig &cfg)
{
   if(stage >= 3) return cfg.show_purple_stage;
   if(stage == 2) return cfg.show_green_stage;
   if(stage == 1) return cfg.show_red_stage;
   return cfg.show_pre_stage;
}

datetime DAL_M0006BoxLeftTime(const DALLRuleNode &node, const DALM0006ReactionBoxConfig &cfg)
{
   if(cfg.box_left_anchor_mode == 1)
      return node.active_from_time;
   return node.time;
}

datetime DAL_M0006BoxRightTime(
   const DALBar &bars[],
   const int bars_count,
   const int touch_index,
   const DALM0006ReactionBoxConfig &cfg
)
{
   datetime t = bars[touch_index].time;
   if(cfg.box_right_anchor_mode == 1)
   {
      int sec = PeriodSeconds(cfg.timeframe);
      if(sec <= 0) sec = 60;
      t += sec;
   }
   return t;
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

   if(ObjectFind(0, name) >= 0)
   {
      // Persistent box update: do not move it and do not recreate it.
      // Only the maturity color and metadata are updated when a higher horizon is reached.
      ObjectSetInteger(0, name, OBJPROP_COLOR, c);
      ObjectSetInteger(0, name, OBJPROP_WIDTH, MathMax(1, cfg.line_width));
      ObjectSetString(0, name, OBJPROP_TOOLTIP, tooltip + " persistentBox=1 colorOnlyUpdate=1");
      return true;
   }

   if(!ObjectCreate(0, name, OBJ_RECTANGLE, 0, t1, top, right_time, bottom))
      return false;

   ObjectSetInteger(0, name, OBJPROP_COLOR, c);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, MathMax(1, cfg.line_width));
   ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_SOLID);
   ObjectSetInteger(0, name, OBJPROP_FILL, cfg.fill ? 1 : 0);
   ObjectSetInteger(0, name, OBJPROP_BACK, cfg.draw_back ? 1 : 0);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetString(0, name, OBJPROP_TOOLTIP, tooltip + " persistentBox=1 createdOnce=1");
   return true;
}

bool DAL_M0006CreateHorizontalLevel(
   const string name,
   const datetime t1,
   const datetime t2,
   const double price,
   const color c,
   const DALM0006ReactionBoxConfig &cfg,
   const string tooltip
)
{
   if(!cfg.draw_chart || !cfg.draw_node_levels)
      return false;

   datetime right_time = t2;
   if(right_time <= t1)
   {
      int sec = PeriodSeconds(cfg.timeframe);
      if(sec <= 0) sec = 60;
      right_time = t1 + sec;
   }

   ResetLastError();
   ObjectDelete(0, name);
   if(!ObjectCreate(0, name, OBJ_TREND, 0, t1, price, right_time, price))
      return false;

   ObjectSetInteger(0, name, OBJPROP_COLOR, c);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, MathMax(1, cfg.line_width));
   ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_SOLID);
   ObjectSetInteger(0, name, OBJPROP_RAY_RIGHT, false);
   ObjectSetInteger(0, name, OBJPROP_RAY_LEFT, false);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_BACK, cfg.draw_back ? 1 : 0);
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
   int bars_count = DAL_LoadBarsChronological(cfg.symbol, cfg.timeframe, cfg.requested_closed_bars, !cfg.include_live_bar, bars);
   if(bars_count <= 0)
   {
      Print("DAL_M0006_DIRECT_VISUAL_AUDIT *** update=SKIP_PRESERVE_EXISTING*reason=no_bars_loaded*symbol=", cfg.symbol, "*tf=", EnumToString(cfg.timeframe));
      return false;
   }

   int min_required_bars = MathMax(cfg.min_bars_for_update, MathMax(2 * MathMax(1, cfg.L) + 3, 10));
   if(cfg.preserve_existing_on_empty_update && bars_count < min_required_bars)
   {
      Print("DAL_M0006_DIRECT_VISUAL_AUDIT *** update=SKIP_PRESERVE_EXISTING*reason=not_enough_bars"
         + string("*symbol=") + cfg.symbol
         + "*tf=" + EnumToString(cfg.timeframe)
         + "*bars=" + IntegerToString(bars_count)
         + "*minRequiredBars=" + IntegerToString(min_required_bars));
      return false;
   }

   DALLRuleNode nodes[];
   int nodes_count = DAL_DetectLRuleNodes(bars, bars_count, MathMax(1, cfg.L), nodes);

   if(cfg.preserve_existing_on_empty_update && nodes_count <= 0)
   {
      Print("DAL_M0006_DIRECT_VISUAL_AUDIT *** update=SKIP_PRESERVE_EXISTING*reason=no_nodes_yet"
         + string("*symbol=") + cfg.symbol
         + "*tf=" + EnumToString(cfg.timeframe)
         + "*bars=" + IntegerToString(bars_count)
         + "*L=" + IntegerToString(cfg.L));
      return false;
   }

   DAL_M0006DeleteVolatileObjectsByPrefix(cfg.object_prefix, cfg.preserve_matured_boxes);

   int h1 = MathMax(1, cfg.horizon_red);
   int h2 = MathMax(h1 + 1, cfg.horizon_green);
   int h3 = MathMax(h2 + 1, cfg.horizon_purple);

   double point = DAL_M0006PointSafe(cfg.symbol);
   double touch_buffer = MathMax(0.0, cfg.touch_buffer_points) * point;
   double retouch_buffer = MathMax(0.0, cfg.zone_end_retouch_buffer_points) * point;

   int max_boxes = (cfg.max_boxes <= 0 ? 2147483647 : cfg.max_boxes);
   int max_levels = (cfg.max_levels <= 0 ? 2147483647 : cfg.max_levels);
   int touched = 0;
   int drawn = 0;
   int level_drawn = 0;
   int no_touch = 0;
   int away_confirmed = 0;
   int object_failures = 0;
   int level_failures = 0;
   int retouched = 0;
   int active = 0;
   int untouched = 0;
   int red = 0;
   int green = 0;
   int purple = 0;
   int pre = 0;
   int last_error = 0;

   int skipped_consumed = 0;
   int skipped_level = 0;
   int skipped_touch_no_away = 0;
   int skipped_untouched = 0;
   int skipped_pre_touch_draw = 0;
   int skipped_box_not_matured = 0;
   int skipped_box_layer = 0;

   int sec = PeriodSeconds(cfg.timeframe);
   if(sec <= 0) sec = 60;
   datetime live_right_time = bars[bars_count - 1].time + sec;

   for(int n = nodes_count - 1; n >= 0 && (drawn < max_boxes || level_drawn < max_levels); n--)
   {
      datetime left_time = DAL_M0006BoxLeftTime(nodes[n], cfg);
      int touch_index = DAL_M0006FindFirstTouch(bars, bars_count, nodes[n], touch_buffer);
      string side = (nodes[n].type == DAL_NODE_HIGH ? "HIGH" : "LOW");

      if(touch_index < 0)
      {
         no_touch++;
         untouched++;

         // Official policy: before the first touch there is no zone and no pre-touch visual object by default.
         // Optional untouched reference levels can still be enabled for debugging only.
         if((!cfg.boxes_only_mode) && cfg.draw_node_levels && cfg.show_untouched_levels && level_drawn < max_levels)
         {
            string level_tip = "H6 DEBUG UNTOUCHED LEVEL side=" + side
               + " nodeId=" + IntegerToString(nodes[n].id)
               + " nodeIndex=" + IntegerToString(nodes[n].index)
               + " activeFromIndex=" + IntegerToString(nodes[n].active_from_index)
               + " origin=" + TimeToString(nodes[n].time)
               + " known=" + TimeToString(nodes[n].active_from_time)
               + " levelEnd=" + TimeToString(live_right_time)
               + " nodePrice=" + DoubleToString(nodes[n].price, _Digits)
               + " officialZone=0"
               + " debugOnly=1";
            string level_name = cfg.object_prefix + "DEBUG_LEVEL_UNTOUCHED_" + IntegerToString(nodes[n].id) + "_" + side;
            if(DAL_M0006CreateHorizontalLevel(level_name, left_time, live_right_time, nodes[n].price, cfg.color_untouched_level, cfg, level_tip))
               level_drawn++;
            else
            {
               level_failures++;
               last_error = GetLastError();
            }
         }
         else
         {
            skipped_untouched++;
            skipped_pre_touch_draw++;
         }
         continue;
      }

      touched++;

      int away_index = DAL_M0006FindAwayConfirm(bars, bars_count, nodes[n], touch_index, cfg.max_away_scan_bars);
      bool away_ok = (!cfg.require_close_away_after_touch || away_index > 0);
      if(away_index > 0) away_confirmed++;
      if(!away_ok)
      {
         skipped_touch_no_away++;
         continue;
      }

      double zone_end = DAL_M0006TouchExtreme(bars[touch_index], nodes[n]);
      int retouch_index = DAL_M0006FindZoneEndRetouch(bars, bars_count, nodes[n], touch_index, zone_end, retouch_buffer);
      bool is_active = (retouch_index < 0);
      if(is_active) active++; else retouched++;

      if(!is_active && !cfg.show_consumed_boxes)
      {
         skipped_consumed++;
         continue;
      }

      int effective_end = is_active ? (bars_count - 1) : (retouch_index - 1);
      if(effective_end < touch_index) effective_end = touch_index;
      int age_after_touch = effective_end - touch_index;
      int stage = DAL_M0006StageFromAge(age_after_touch, h1, h2, h3);
      if(stage >= 3) purple++;
      else if(stage == 2) green++;
      else if(stage == 1) red++;
      else pre++;

      color level_color = DAL_M0006ColorForLevel(stage, is_active, away_ok, cfg);
      color box_color = DAL_M0006ColorForBox(stage, is_active, away_ok, cfg);
      string stage_text = DAL_M0006StageText(stage, h1, h2, h3);
      bool consumed = !is_active;
      string state_text = is_active ? "ACTIVE" : "CONSUMED";
      string touch_state = DAL_M0006TouchStateName(true, away_ok, consumed, stage);
      datetime right_time = DAL_M0006BoxRightTime(bars, bars_count, touch_index, cfg);

      string tip = "H6 CANDLE-BY-CANDLE ZONE STATE"
         + " side=" + side
         + " nodeId=" + IntegerToString(nodes[n].id)
         + " nodeIndex=" + IntegerToString(nodes[n].index)
         + " activeFromIndex=" + IntegerToString(nodes[n].active_from_index)
         + " origin=" + TimeToString(nodes[n].time)
         + " known=" + TimeToString(nodes[n].active_from_time)
         + " boxLeft=" + TimeToString(left_time)
         + " touch=" + TimeToString(bars[touch_index].time)
         + " boxRight=" + TimeToString(right_time)
         + " awayConfirm=" + (away_index > 0 ? TimeToString(bars[away_index].time) : "NONE")
         + " retouch=" + (retouch_index > 0 ? TimeToString(bars[retouch_index].time) : "NONE")
         + " state=" + touch_state
         + " active=" + IntegerToString(is_active ? 1 : 0)
         + " candlesAfterTouchNoZoneEndRetouch=" + IntegerToString(age_after_touch)
         + " maturedForBox=" + IntegerToString(stage > 0 ? 1 : 0)
         + " boxDrawCondition=(touched && reversal_confirmed && !zone_end_retouched && age_after_touch >= selected_horizon)"
         + " nodePrice=" + DoubleToString(nodes[n].price, _Digits)
         + " zoneStart=" + DoubleToString(nodes[n].price, _Digits)
         + " zoneEnd=" + DoubleToString(zone_end, _Digits)
         + " leftAnchorMode=" + IntegerToString(cfg.box_left_anchor_mode)
         + " rightAnchorMode=" + IntegerToString(cfg.box_right_anchor_mode)
         + " noRegimeFilter=1";

      // Draw/update the live node level independently from the reaction box.
      // The level is a neutral reference only; it is not the maturity signal.
      // The colored box is created only when the candle-by-candle post-touch survival condition becomes true.
      if((!cfg.boxes_only_mode) && cfg.draw_node_levels && level_drawn < max_levels)
      {
         datetime level_start = bars[touch_index].time;
         datetime level_end = is_active ? live_right_time : bars[retouch_index].time;
         string level_name2 = cfg.object_prefix + "LEVEL_AFTER_TOUCH_" + stage_text + "_" + state_text + "_" + IntegerToString(nodes[n].id) + "_" + side;
         string level_tip2 = tip
            + " levelStart=" + TimeToString(level_start)
            + " levelEnd=" + TimeToString(level_end)
            + " officialPreTouchZone=0"
            + " levelDrawnAfterFirstTouch=1";
         if(DAL_M0006CreateHorizontalLevel(level_name2, level_start, level_end, nodes[n].price, level_color, cfg, level_tip2))
            level_drawn++;
         else
         {
            level_failures++;
            last_error = GetLastError();
         }
      }

      bool box_matured = (!cfg.draw_boxes_only_after_horizon || stage > 0);
      bool box_layer_visible = DAL_M0006StageVisible(stage, cfg);
      bool box_drawn = false;

      if(!box_matured)
      {
         // touched/reversal is being watched, but not enough candles have passed after touch.
         skipped_box_not_matured++;
      }
      else if(!box_layer_visible)
      {
         skipped_box_layer++;
         skipped_level++;
      }
      else if(drawn < max_boxes)
      {
          string name = cfg.object_prefix + "BOX_" + IntegerToString(nodes[n].id) + "_" + side;
         if(DAL_M0006CreateReactionRectangle(name, left_time, right_time, nodes[n].price, zone_end, nodes[n].type, box_color, cfg, tip))
         {
            drawn++;
            box_drawn = true;
         }
         else
         {
            object_failures++;
            last_error = GetLastError();
         }
      }

      if(box_drawn && cfg.show_origin_touch_markers && drawn < max_boxes)
      {
         string m1 = cfg.object_prefix + "O_" + IntegerToString(nodes[n].id) + "_" + side;
         if(DAL_M0006DrawTextMarker(m1, left_time, nodes[n].price, "O", clrWhite, tip + " marker=origin"))
            drawn++;
      }
      if(box_drawn && cfg.show_origin_touch_markers && drawn < max_boxes)
      {
         string m2 = cfg.object_prefix + "T_" + IntegerToString(nodes[n].id) + "_" + side;
         if(DAL_M0006DrawTextMarker(m2, bars[touch_index].time, zone_end, "T", box_color, tip + " marker=touch"))
            drawn++;
      }
   }

   ChartRedraw(0);

   string line = "DAL_M0006_DIRECT_VISUAL_AUDIT *** build=1.01"
      + "*engine=direct_lrule_nodes_no_event_dependency"
      + "*update=DELETE_AND_REDRAW_VALID_SNAPSHOT"
      + "*preserveExistingOnEmpty=" + IntegerToString(cfg.preserve_existing_on_empty_update ? 1 : 0)
      + "*preserveMaturedBoxes=" + IntegerToString(cfg.preserve_matured_boxes ? 1 : 0)
      + "*boxUpdatePolicy=persistent_stable_name_color_only_update"
      + "*symbol=" + cfg.symbol
      + "*tf=" + EnumToString(cfg.timeframe)
      + "*includeLiveBar=" + IntegerToString(cfg.include_live_bar ? 1 : 0)
      + "*bars=" + IntegerToString(bars_count)
      + "*nodes=" + IntegerToString(nodes_count)
      + "*touched=" + IntegerToString(touched)
      + "*noTouch=" + IntegerToString(no_touch)
      + "*untouched=" + IntegerToString(untouched)
      + "*drawnBoxesMarkers=" + IntegerToString(drawn)
      + "*drawnLevels=" + IntegerToString(level_drawn)
      + "*objectFailures=" + IntegerToString(object_failures)
      + "*levelFailures=" + IntegerToString(level_failures)
      + "*lastObjectError=" + IntegerToString(last_error)
      + "*awayConfirmed=" + IntegerToString(away_confirmed)
      + "*activeNoZoneEndRetouch=" + IntegerToString(active)
      + "*zoneEndRetouched=" + IntegerToString(retouched)
      + "*preH" + IntegerToString(h1) + "=" + IntegerToString(pre)
      + "*redH" + IntegerToString(h1) + "=" + IntegerToString(red)
      + "*greenH" + IntegerToString(h2) + "=" + IntegerToString(green)
      + "*purpleH" + IntegerToString(h3) + "=" + IntegerToString(purple)
      + "*skippedConsumed=" + IntegerToString(skipped_consumed)
      + "*skippedByLevelInput=" + IntegerToString(skipped_level)
      + "*skippedTouchNoAway=" + IntegerToString(skipped_touch_no_away)
      + "*skippedPreTouchDraw=" + IntegerToString(skipped_pre_touch_draw)
      + "*skippedBoxNotMatured=" + IntegerToString(skipped_box_not_matured)
      + "*skippedBoxLayer=" + IntegerToString(skipped_box_layer)
      + "*drawBoxesOnlyAfterHorizon=" + IntegerToString(cfg.draw_boxes_only_after_horizon ? 1 : 0)
      + "*showPre=" + IntegerToString(cfg.show_pre_stage ? 1 : 0)
      + "*showRed=" + IntegerToString(cfg.show_red_stage ? 1 : 0)
      + "*showGreen=" + IntegerToString(cfg.show_green_stage ? 1 : 0)
      + "*showPurple=" + IntegerToString(cfg.show_purple_stage ? 1 : 0)
      + "*showConsumed=" + IntegerToString(cfg.show_consumed_boxes ? 1 : 0)
      + "*showUntouchedLevels=" + IntegerToString(cfg.show_untouched_levels ? 1 : 0)
      + "*leftAnchorMode=" + IntegerToString(cfg.box_left_anchor_mode)
      + "*rightAnchorMode=" + IntegerToString(cfg.box_right_anchor_mode)
      + "*scope=all_raw_nodes_no_regime_filter"
      + "*box=drawn_only_after_horizon_elapsed_after_touch_and_price_zone_start_to_zone_end"
      + "*levels=live_horizontal_node_levels_update_before_box_maturity"
      + "*stateMachine=UNTOUCHED_NO_DRAW_TO_TOUCHED_LEVEL_AFTER_TOUCH_TO_WATCHING_TO_MATURED_BOX_OR_CONSUMED"
      + "*visualPolicy=" + (cfg.boxes_only_mode ? "ONLY_PERSISTENT_BOXES" : "BOXES_LEVELS_MARKERS")
      + "*preTouchDrawPolicy=OFF_BY_DEFAULT_NO_ZONE_BEFORE_FIRST_TOUCH"
      + "*levelPolicy=neutral_reference_starts_at_first_touch_not_node_origin"
      + "*boxDrawRule=draw_only_when_touch_confirmed_and_zone_end_not_retouched_and_age_after_touch_reaches_input_horizon"
      + "*boxPersistence=once_created_never_deleted_by_live_update"
      + "*colorRule=highest_reached_input_horizon_after_touch_without_zone_end_retouch";
   Print(line);

   return (drawn > 0 && object_failures == 0);
}

#endif
