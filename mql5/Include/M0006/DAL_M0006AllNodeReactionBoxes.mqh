#ifndef __DAL_M0006_ALL_NODE_REACTION_BOXES_MQH__
#define __DAL_M0006_ALL_NODE_REACTION_BOXES_MQH__

#include <Market/DAL_Bars.mqh>
#include <StructuralNodes/LRule/DAL_LRuleDetector.mqh>
#include <M0001/DAL_M0001Config.mqh>
#include <M0001/DAL_M0001Engine.mqh>

enum ENUM_DALM0006ZoneProjectionMode
{
   DAL_M0006_ZONE_FULL_M0001_TERRITORY = 0, // existing behavior: use frozen M0001 territory lower/upper
   DAL_M0006_ZONE_NODE_CAPPED_90_TO_NODE = 1 // visual/valid zone is the inner territory edge to exact node price
};

string DAL_M0006FastZoneProjectionModeName(const ENUM_DALM0006ZoneProjectionMode mode)
{
   if(mode == DAL_M0006_ZONE_NODE_CAPPED_90_TO_NODE)
      return "NODE_CAPPED_90_TO_NODE";
   return "FULL_M0001_TERRITORY";
}

// H6 FAST official visual contract:
// - M0001 is the only source of truth for extreme / territory / touch / revisit / invalidation.
// - H6 does not rebuild any market logic.
// - H6 draws one persistent box for every confirmed M0001 event by default.
// - Box time range is fixed: left=node time, right=first M0001 touch/revisit time, even if touch is wick-only.
// - Box color is checked every new candle until the zone back side is hit or purple horizon is reached.
// - If zone back side is hit before purple, the box is invalid and removed/hidden.
// - No lines, no markers, no circles, no per-candle delete/rebuild, no tick execution.

struct DALM0006FastBoxConfig
{
   string symbol;
   ENUM_TIMEFRAMES timeframe;
   int requested_bars;
   int L;

   double m0001_zone_ratio;
   int m0001_exit_gap;
   ENUM_DALM0001ConsumeMode m0001_consume_mode;
   int m0001_max_events;
   double m0001_min_rtv;

   ENUM_DALM0006ZoneProjectionMode zone_projection_mode;
   bool node_capped_invalidate_on_touch_candle;

   int horizon_red;
   int horizon_green;
   int horizon_purple;

   bool draw_chart;
   bool include_live_bar;
   bool draw_pre_horizon_boxes;
   bool draw_only_reversal_events;
   bool show_consumed_events;
   bool update_existing_geometry;
   bool never_downgrade_box_color;
   bool invalidate_on_zone_back_hit_before_max;
   bool print_audit;

   string box_prefix;
   int max_boxes;
   bool fill;
   bool back;
   int line_width;

   color color_pre;
   color color_red;
   color color_green;
   color color_purple;
};

void DAL_M0006FastDefaultConfig(DALM0006FastBoxConfig &cfg)
{
   cfg.symbol = _Symbol;
   cfg.timeframe = (ENUM_TIMEFRAMES)_Period;
   cfg.requested_bars = 50000;
   cfg.L = 5;

   cfg.m0001_zone_ratio = 0.90;
   cfg.m0001_exit_gap = 6;
   cfg.m0001_consume_mode = DAL_M0001_CONSUME_BY_HUNT;
   cfg.m0001_max_events = 0;
   cfg.m0001_min_rtv = 0.0;

   cfg.zone_projection_mode = DAL_M0006_ZONE_FULL_M0001_TERRITORY;
   cfg.node_capped_invalidate_on_touch_candle = true;

   cfg.horizon_red = 20;
   cfg.horizon_green = 50;
   cfg.horizon_purple = 100;

   cfg.draw_chart = true;
   cfg.include_live_bar = false;          // official: closed-candle/new-bar updates only
   cfg.draw_pre_horizon_boxes = true;       // critical: every confirmed touch/revisit event gets a box
   cfg.draw_only_reversal_events = false;   // false = draw every M0001 confirmed event; true = strict rejection side only
   cfg.show_consumed_events = true;
   cfg.update_existing_geometry = true;
   cfg.never_downgrade_box_color = true;
   cfg.invalidate_on_zone_back_hit_before_max = true;
   cfg.print_audit = false;

   cfg.box_prefix = "DAL_H6_PERSIST_BOX_";
   cfg.max_boxes = 0;
   cfg.fill = true;
   cfg.back = true;
   cfg.line_width = 2;

   cfg.color_pre = clrOrange;
   cfg.color_red = clrRed;
   cfg.color_green = clrLime;
   cfg.color_purple = clrPurple;
}

void DAL_M0006FastDeleteObjectsByPrefix(const string prefix)
{
   int total = ObjectsTotal(0);
   for(int i = total - 1; i >= 0; i--)
   {
      string name = ObjectName(0, i);
      if(StringFind(name, prefix) == 0)
         ObjectDelete(0, name);
   }
}

bool DAL_M0006FastDeleteBoxIfExists(const string name)
{
   if(ObjectFind(0, name) < 0)
      return false;
   return ObjectDelete(0, name);
}

int DAL_M0006FastStage(const int age, const int h1, const int h2, const int h3)
{
   if(age >= h3) return 3;
   if(age >= h2) return 2;
   if(age >= h1) return 1;
   return 0;
}

int DAL_M0006FastStageHorizon(const int stage, const int h1, const int h2, const int h3)
{
   if(stage >= 3) return h3;
   if(stage == 2) return h2;
   if(stage == 1) return h1;
   return 0;
}

color DAL_M0006FastColor(const int stage, const DALM0006FastBoxConfig &cfg)
{
   if(stage >= 3) return cfg.color_purple;
   if(stage == 2) return cfg.color_green;
   if(stage == 1) return cfg.color_red;
   return cfg.color_pre;
}

int DAL_M0006FastStageFromColor(const color c, const DALM0006FastBoxConfig &cfg)
{
   if(c == cfg.color_purple) return 3;
   if(c == cfg.color_green) return 2;
   if(c == cfg.color_red) return 1;
   if(c == cfg.color_pre) return 0;
   return -1;
}

int DAL_M0006FastExistingBoxStage(const string name, const DALM0006FastBoxConfig &cfg)
{
   if(ObjectFind(0, name) < 0)
      return -1;

   long z = ObjectGetInteger(0, name, OBJPROP_ZORDER);
   if(z >= 0 && z <= 3)
      return (int)z;

   color existing_color = (color)ObjectGetInteger(0, name, OBJPROP_COLOR);
   return DAL_M0006FastStageFromColor(existing_color, cfg);
}

bool DAL_M0006FastProjectedZone(
   const DALM0001Event &event,
   const DALM0006FastBoxConfig &cfg,
   double &lower,
   double &upper
)
{
   lower = event.territory_lower;
   upper = event.territory_upper;

   if(cfg.zone_projection_mode == DAL_M0006_ZONE_NODE_CAPPED_90_TO_NODE)
   {
      // New H6 projection:
      // - The far/back side is the exact node price.
      // - The opposite edge remains the inner M0001 territory/touch edge.
      // LOW  node: box = [node_price, territory_upper]
      // HIGH node: box = [territory_lower, node_price]
      // This isolates cases that reach the territory edge but do not hit the node itself.
      if(event.node_type == DAL_NODE_HIGH)
      {
         lower = event.territory_lower;
         upper = event.node_price;
      }
      else
      {
         lower = event.node_price;
         upper = event.territory_upper;
      }
   }

   if(upper < lower)
   {
      double tmp = lower;
      lower = upper;
      upper = tmp;
   }

   return (upper > lower);
}

bool DAL_M0006FastZoneBackHit(
   const DALM0001Event &event,
   const DALBar &bar,
   const DALM0006FastBoxConfig &cfg
)
{
   // Official color lifecycle uses only high/low.
   if(cfg.zone_projection_mode == DAL_M0006_ZONE_NODE_CAPPED_90_TO_NODE)
   {
      // In node-capped mode the box dies as soon as the real node price itself is hit.
      if(event.node_type == DAL_NODE_HIGH)
         return (bar.high >= event.node_price);
      return (bar.low <= event.node_price);
   }

   // Existing full-territory mode:
   // HIGH node: far/back side of the territory is the upper bound.
   // LOW node: far/back side of the territory is the lower bound.
   if(event.node_type == DAL_NODE_HIGH)
      return (bar.high >= event.territory_upper);
   return (bar.low <= event.territory_lower);
}

int DAL_M0006FastLiveAgeAfterTouchUntilBackHit(
   const DALM0001Event &event,
   const DALBar &bars[],
   const int bars_count,
   const DALM0006FastBoxConfig &cfg,
   int &back_hit_index,
   bool &max_horizon_reached
)
{
   // Official dynamic color age:
   // - touch candle is zero
   // - first closed candle after touch is one
   // - keep checking the event until either:
   //   a) the far/back side of the frozen M0001 territory is hit, or
   //   b) the highest horizon has been reached.
   // This deliberately does NOT use M0001 exit_index/rtv_sample_length, because
   // exit-gap completion is only touch/revisit confirmation, not the end of H6 color tracking.
   back_hit_index = -1;
   max_horizon_reached = false;

   if(event.entry_index < 0 || event.entry_index >= bars_count)
      return 0;

   int max_age = MathMax(1, cfg.horizon_purple);
   int age = 0;

   int scan_start = event.entry_index + 1;
   if(cfg.zone_projection_mode == DAL_M0006_ZONE_NODE_CAPPED_90_TO_NODE && cfg.node_capped_invalidate_on_touch_candle)
      scan_start = event.entry_index;

   for(int i = scan_start; i < bars_count; i++)
   {
      if(DAL_M0006FastZoneBackHit(event, bars[i], cfg))
      {
         back_hit_index = i;
         break;
      }

      age++;
      if(age >= max_age)
      {
         max_horizon_reached = true;
         break;
      }
   }

   return age;
}

bool DAL_M0006FastEventIsReversal(
   const DALM0001Event &event,
   const DALBar &bars[],
   const int bars_count
)
{
   if(event.exit_index < 0 || event.exit_index >= bars_count)
      return false;

   // M0001 exit is high/low outside frozen territory. H6 can optionally keep
   // only rejection exits: high-node rejected downward, low-node rejected upward.
   if(event.node_type == DAL_NODE_HIGH)
      return (bars[event.exit_index].high < event.territory_lower);

   return (bars[event.exit_index].low > event.territory_upper);
}

string DAL_M0006FastBoxName(const DALM0001Event &event, const DALM0006FastBoxConfig &cfg)
{
   double point = SymbolInfoDouble(cfg.symbol, SYMBOL_POINT);
   if(point <= 0.0) point = 0.01;

   long price_key = (long)MathRound(event.node_price / point);
   string side = (event.node_type == DAL_NODE_HIGH ? "HIGH" : "LOW");

   string mode_tag = "";
   if(cfg.zone_projection_mode == DAL_M0006_ZONE_NODE_CAPPED_90_TO_NODE)
      mode_tag = "NODECAP_";

   return cfg.box_prefix
      + mode_tag
      + IntegerToString((long)event.node_time) + "_"
      + IntegerToString((long)event.entry_time) + "_"
      + IntegerToString(price_key) + "_"
      + side;
}

bool DAL_M0006FastUpsertBox(
   const string name,
   const datetime left_time,
   const datetime right_time_in,
   const double lower,
   const double upper,
   const int requested_stage,
   const DALM0006FastBoxConfig &cfg,
   const string tooltip
)
{
   if(!cfg.draw_chart)
      return false;

   datetime right_time = right_time_in;
   if(right_time <= left_time)
   {
      int sec = PeriodSeconds(cfg.timeframe);
      if(sec <= 0) sec = 60;
      right_time = left_time + sec;
   }

   double top = MathMax(lower, upper);
   double bottom = MathMin(lower, upper);
   if(top <= bottom)
   {
      double point = SymbolInfoDouble(cfg.symbol, SYMBOL_POINT);
      if(point <= 0.0) point = 0.01;
      top += point;
      bottom -= point;
   }

   ResetLastError();

   int safe_requested_stage = MathMax(0, MathMin(3, requested_stage));
   int final_stage = safe_requested_stage;

   if(ObjectFind(0, name) >= 0)
   {
      int previous_stage = DAL_M0006FastExistingBoxStage(name, cfg);
      if(cfg.never_downgrade_box_color && previous_stage > final_stage)
         final_stage = previous_stage;

      color final_color = DAL_M0006FastColor(final_stage, cfg);

      if(cfg.update_existing_geometry)
      {
         ObjectMove(0, name, 0, left_time, top);
         ObjectMove(0, name, 1, right_time, bottom);
      }

      ObjectSetInteger(0, name, OBJPROP_COLOR, final_color);
      ObjectSetInteger(0, name, OBJPROP_ZORDER, final_stage);
      ObjectSetInteger(0, name, OBJPROP_WIDTH, MathMax(1, cfg.line_width));
      ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_SOLID);
      ObjectSetInteger(0, name, OBJPROP_FILL, cfg.fill ? 1 : 0);
      ObjectSetInteger(0, name, OBJPROP_BACK, cfg.back ? 1 : 0);
      ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
      ObjectSetString(0, name, OBJPROP_TOOLTIP, tooltip
         + " upsert=1 lifecycle=no_delete"
         + " requestedStage=" + IntegerToString(safe_requested_stage)
         + " finalStage=" + IntegerToString(final_stage)
         + " previousStage=" + IntegerToString(previous_stage));
      return true;
   }

   color final_color = DAL_M0006FastColor(final_stage, cfg);

   if(!ObjectCreate(0, name, OBJ_RECTANGLE, 0, left_time, top, right_time, bottom))
      return false;

   ObjectSetInteger(0, name, OBJPROP_COLOR, final_color);
   ObjectSetInteger(0, name, OBJPROP_ZORDER, final_stage);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, MathMax(1, cfg.line_width));
   ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_SOLID);
   ObjectSetInteger(0, name, OBJPROP_FILL, cfg.fill ? 1 : 0);
   ObjectSetInteger(0, name, OBJPROP_BACK, cfg.back ? 1 : 0);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetString(0, name, OBJPROP_TOOLTIP, tooltip + " created=1 lifecycle=no_delete");
   return true;
}

int DAL_M0006FastDrawEventBoxes(const DALM0006FastBoxConfig &cfg)
{
   if(!cfg.draw_chart)
      return 0;

   DALBar bars[];
   int bars_count = DAL_LoadBarsChronological(
      cfg.symbol,
      cfg.timeframe,
      cfg.requested_bars,
      !cfg.include_live_bar,
      bars
   );

   if(bars_count < MathMax(2 * cfg.L + 2, cfg.m0001_exit_gap + 2))
      return 0;

   DALLRuleNode nodes[];
   int nodes_count = DAL_DetectLRuleNodes(bars, bars_count, cfg.L, nodes);
   if(nodes_count <= 0)
      return 0;

   DALM0001Config m1;
   DAL_M0001DefaultConfig(m1);
   m1.L = cfg.L;
   m1.zone_ratio = cfg.m0001_zone_ratio;
   m1.exit_gap = cfg.m0001_exit_gap;
   m1.consume_mode = cfg.m0001_consume_mode;
   m1.consume_on_touch = (cfg.m0001_consume_mode == DAL_M0001_CONSUME_BY_TOUCH);
   m1.max_events = cfg.m0001_max_events;
   m1.min_rtv = cfg.m0001_min_rtv;

   DALM0001Event events[];
   int events_count = DAL_M0001ComputeEvents(bars, bars_count, nodes, nodes_count, m1, events);
   if(events_count <= 0)
      return 0;

   int max_boxes = (cfg.max_boxes <= 0 ? events_count : MathMin(cfg.max_boxes, events_count));
   int drawn = 0;
   int failures = 0;
   int skipped_pre = 0;
   int skipped_consumed = 0;
   int skipped_reversal = 0;
   int active_color_watch = 0;
   int back_hit_count = 0;
   int max_horizon_count = 0;
   int skipped_invalid_back_hit = 0;
   int deleted_invalid = 0;

   for(int e = 0; e < events_count && drawn < max_boxes; e++)
   {
      DALM0001Event event = events[e];

      if(!event.touch_confirmed)
         continue;

      if(event.consumed && !cfg.show_consumed_events)
      {
         skipped_consumed++;
         continue;
      }

      if(cfg.draw_only_reversal_events && !DAL_M0006FastEventIsReversal(event, bars, bars_count))
      {
         skipped_reversal++;
         continue;
      }

      // Touch candle is zero. Color age is updated dynamically every new candle
      // until the far/back side of the M0001 frozen territory is hit or purple horizon is reached.
      int back_hit_index = -1;
      bool max_horizon_reached = false;
      int age_after_touch = DAL_M0006FastLiveAgeAfterTouchUntilBackHit(event, bars, bars_count, cfg, back_hit_index, max_horizon_reached);
      int stage = DAL_M0006FastStage(age_after_touch, cfg.horizon_red, cfg.horizon_green, cfg.horizon_purple);
      if(back_hit_index >= 0) back_hit_count++;
      if(max_horizon_reached) max_horizon_count++;
      if(back_hit_index < 0 && !max_horizon_reached) active_color_watch++;

      double projected_lower = event.territory_lower;
      double projected_upper = event.territory_upper;
      if(!DAL_M0006FastProjectedZone(event, cfg, projected_lower, projected_upper))
      {
         failures++;
         continue;
      }

      string name = DAL_M0006FastBoxName(event, cfg);

      // Official invalidation rule:
      // If the far/back side of the zone is hit BEFORE the max horizon, the box has no value.
      // It must not be shown; if an orange/red/green box existed from earlier live updates, delete it.
      if(cfg.invalidate_on_zone_back_hit_before_max && back_hit_index >= 0 && !max_horizon_reached)
      {
         if(DAL_M0006FastDeleteBoxIfExists(name))
            deleted_invalid++;
         skipped_invalid_back_hit++;
         continue;
      }

      if(stage <= 0 && !cfg.draw_pre_horizon_boxes)
      {
         skipped_pre++;
         continue;
      }

      // Official H6 visual time range:
      // left  = exact node candle time
      // right = exact first M0001 touch/revisit candle time, including wick/shadow touches.
      datetime box_left_time = event.node_time;
      datetime box_right_time = event.entry_time;

      string side = (event.node_type == DAL_NODE_HIGH ? "HIGH" : "LOW");
      string tip = "H6 FAST M0001 BOX"
         + string(" side=") + side
         + " nodeId=" + IntegerToString(event.node_id)
         + " revisitId=" + IntegerToString(event.revisit_id)
         + " nodeTime=" + TimeToString(event.node_time)
         + " firstTouch=" + TimeToString(event.entry_time)
         + " exit=" + TimeToString(event.exit_time)
         + " timePolicy=node_time_to_first_touch_time"
         + " colorAgeAfterTouch=" + IntegerToString(age_after_touch)
         + " colorStage=" + IntegerToString(stage)
         + " colorBackHit=" + (back_hit_index >= 0 ? TimeToString(bars[back_hit_index].time) : "NONE")
         + " colorMaxHorizonReached=" + IntegerToString(max_horizon_reached ? 1 : 0)
         + " invalidatesOnBackHitBeforeMax=" + IntegerToString(cfg.invalidate_on_zone_back_hit_before_max ? 1 : 0)
         + " zoneProjectionMode=" + DAL_M0006FastZoneProjectionModeName(cfg.zone_projection_mode)
         + " nodeCappedTouchCandleInvalidation=" + IntegerToString(cfg.node_capped_invalidate_on_touch_candle ? 1 : 0)
         + " colorAgePolicy=dynamic_until_zone_back_hit_or_purple"
         + " rtvSampleLength=" + IntegerToString(event.rtv_sample_length)
         + " reversal=" + IntegerToString(DAL_M0006FastEventIsReversal(event, bars, bars_count) ? 1 : 0)
         + " node=" + DoubleToString(event.node_price, _Digits)
         + " originalLower=" + DoubleToString(event.territory_lower, _Digits)
         + " originalUpper=" + DoubleToString(event.territory_upper, _Digits)
         + " projectedLower=" + DoubleToString(projected_lower, _Digits)
         + " projectedUpper=" + DoubleToString(projected_upper, _Digits)
         + " extreme=" + DoubleToString(event.expansion_extreme, _Digits)
         + " consumed=" + IntegerToString(event.consumed ? 1 : 0)
         + " source=M0001";

      if(DAL_M0006FastUpsertBox(name, box_left_time, box_right_time, projected_lower, projected_upper, stage, cfg, tip))
         drawn++;
      else
         failures++;
   }

   if(drawn > 0)
      ChartRedraw(0);

   if(cfg.print_audit)
   {
      Print("DAL_M0006_FAST_BOX_AUDIT *** build=3.04"
         + string("*engine=M0001_EVENT_FAST_BOX_ONLY")
         + "*symbol=" + cfg.symbol
         + "*tf=" + EnumToString(cfg.timeframe)
         + "*bars=" + IntegerToString(bars_count)
         + "*nodes=" + IntegerToString(nodes_count)
         + "*events=" + IntegerToString(events_count)
         + "*drawn=" + IntegerToString(drawn)
         + "*failures=" + IntegerToString(failures)
         + "*skippedPre=" + IntegerToString(skipped_pre)
         + "*skippedConsumed=" + IntegerToString(skipped_consumed)
         + "*skippedReversal=" + IntegerToString(skipped_reversal)
         + "*activeColorWatch=" + IntegerToString(active_color_watch)
         + "*backHit=" + IntegerToString(back_hit_count)
         + "*maxHorizonReached=" + IntegerToString(max_horizon_count)
         + "*skippedInvalidBackHit=" + IntegerToString(skipped_invalid_back_hit)
         + "*deletedInvalid=" + IntegerToString(deleted_invalid)
         + "*drawPre=" + IntegerToString(cfg.draw_pre_horizon_boxes ? 1 : 0)
         + "*onlyReversal=" + IntegerToString(cfg.draw_only_reversal_events ? 1 : 0)
         + "*timePolicy=NODE_TIME_TO_FIRST_TOUCH_TIME"
         + "*colorAgePolicy=DYNAMIC_CHECK_UNTIL_ZONE_BACK_HIT_OR_PURPLE"
         + "*invalidBackHitPolicy=DELETE_OR_HIDE_IF_BACK_HIT_BEFORE_PURPLE"
         + "*zoneProjectionMode=" + DAL_M0006FastZoneProjectionModeName(cfg.zone_projection_mode)
         + "*nodeCappedInvalidateOnTouchCandle=" + IntegerToString(cfg.node_capped_invalidate_on_touch_candle ? 1 : 0)
         + "*boxNamePolicy=NODE_TIME_ENTRY_TIME_PRICE_SIDE_NO_REVISIT_ID"
         + "*lifecycle=UPSERT_VALID_BOXES_DELETE_ONLY_INVALID_BACK_HIT_BEFORE_MAX"
         + "*tickExecution=OFF");
   }

   return drawn;
}

#endif
