//+------------------------------------------------------------------+
//| Decision Alpha Lab — H6 Fast M0001 Event Boxes                    |
//| Boxes only. New-bar only. M0001 is the source of truth.            |
//+------------------------------------------------------------------+
#property strict
#property version   "1.29"
#property description "Fast H0006 valid-zone boxes with selectable full/node-capped zone projection"

#include <M0006/DAL_M0006AllNodeReactionBoxes.mqh>
#include <AlphaLab/UC04/AL_UC04CorePrimitives.mqh>

input string InpSymbol = "";                    // empty = chart symbol
input ENUM_TIMEFRAMES InpTimeframe = PERIOD_CURRENT;
input int InpBars = 50000;                       // init/backfill scan window; 0 = all available
input int InpH6LiveUpdateBars = 2000;             // new-bar update window
input int InpH6UpdateEveryNBars = 1;              // 1 = every new candle
input int InpL = 5;

input double InpM0001ZoneRatio = 0.90;
input ENUM_DALM0006ZoneProjectionMode InpH6ZoneProjectionMode = DAL_M0006_ZONE_FULL_M0001_TERRITORY;
input bool InpH6NodeCappedInvalidateOnTouchCandle = true; // NODE_CAPPED: node-price hit on touch candle kills the box
input int InpM0001ExitGap = 6;
input ENUM_DALM0001ConsumeMode InpM0001ConsumeMode = DAL_M0001_CONSUME_BY_HUNT;
input int InpM0001MaxEvents = 0;                 // 0 = all events

input int InpH6NodeHorizonRed = 20;
input int InpH6NodeHorizonGreen = 50;
input int InpH6NodeHorizonPurple = 100;

input bool InpH6DrawPreHorizonBoxes = true;      // critical: every confirmed M0001 touch/revisit event gets a box
input bool InpH6OnlyReversalEvents = false;      // optional strict filter; default false draws all M0001 confirmed events
input bool InpH6ShowConsumedEvents = true;
input int InpH6ReactionMaxChartObjects = 0;      // 0 = no cap

input bool InpH6IncludeLiveBar = false;          // official: closed-candle/new-bar only; no forming tick candle
input bool InpH6UpdateExistingBoxGeometry = true;
input bool InpH6NeverDowngradeBoxColor = true;   // color can only move pre->red->green->purple
input bool InpH6InvalidateOnZoneBackHitBeforeMax = true; // if zone back is hit before purple, hide/delete that box
input bool InpH6ClearPersistentBoxesOnInit = false;
input bool InpH6RunOnInit = true;
input bool InpH6PrintAudit = false;

input bool InpH6ReactionBoxFill = true;
input bool InpH6ReactionBoxBack = true;
input int InpH6NodeLineWidth = 2;

input color InpH6ColorPreHorizon = clrOrange;
input color InpH6ColorRed = clrRed;
input color InpH6ColorGreen = clrLime;
input color InpH6ColorPurple = clrPurple;

#define DAL_M0006_NODE_BUILD "1.29"

datetime g_m6_last_bar_time = 0;
int g_m6_new_bar_counter = 0;

string M6Symbol()
{
   if(InpSymbol == "") return _Symbol;
   return InpSymbol;
}

ENUM_TIMEFRAMES M6Timeframe()
{
   return AL_UC04ResolveTimeframe(
      InpTimeframe,
      (ENUM_TIMEFRAMES)_Period
   );
}

void RunM0006NodeSurvivalMap(const int bars_override = -1, const string run_mode = "manual")
{
   DALM0006FastBoxConfig cfg;
   DAL_M0006FastDefaultConfig(cfg);

   cfg.symbol = M6Symbol();
   cfg.timeframe = M6Timeframe();
   cfg.requested_bars = (bars_override > 0 ? bars_override : InpBars);
   cfg.L = MathMax(1, InpL);

   cfg.m0001_zone_ratio = MathMax(0.0, MathMin(0.9999, InpM0001ZoneRatio));
   cfg.zone_projection_mode = InpH6ZoneProjectionMode;
   cfg.node_capped_invalidate_on_touch_candle = InpH6NodeCappedInvalidateOnTouchCandle;
   cfg.m0001_exit_gap = MathMax(1, InpM0001ExitGap);
   cfg.m0001_consume_mode = InpM0001ConsumeMode;
   cfg.m0001_max_events = MathMax(0, InpM0001MaxEvents);
   cfg.m0001_min_rtv = 0.0;

   cfg.horizon_red = MathMax(1, InpH6NodeHorizonRed);
   cfg.horizon_green = MathMax(cfg.horizon_red + 1, InpH6NodeHorizonGreen);
   cfg.horizon_purple = MathMax(cfg.horizon_green + 1, InpH6NodeHorizonPurple);

   cfg.draw_chart = true;
   cfg.include_live_bar = InpH6IncludeLiveBar;
   cfg.draw_pre_horizon_boxes = InpH6DrawPreHorizonBoxes;
   cfg.draw_only_reversal_events = InpH6OnlyReversalEvents;
   cfg.show_consumed_events = InpH6ShowConsumedEvents;
   cfg.update_existing_geometry = InpH6UpdateExistingBoxGeometry;
   cfg.never_downgrade_box_color = InpH6NeverDowngradeBoxColor;
   cfg.invalidate_on_zone_back_hit_before_max = InpH6InvalidateOnZoneBackHitBeforeMax;
   cfg.print_audit = InpH6PrintAudit;
   cfg.max_boxes = MathMax(0, InpH6ReactionMaxChartObjects);
   cfg.fill = InpH6ReactionBoxFill;
   cfg.back = InpH6ReactionBoxBack;
   cfg.line_width = MathMax(1, InpH6NodeLineWidth);

   cfg.color_pre = InpH6ColorPreHorizon;
   cfg.color_red = InpH6ColorRed;
   cfg.color_green = InpH6ColorGreen;
   cfg.color_purple = InpH6ColorPurple;

   if(InpH6PrintAudit)
   {
      Print("DAL_M0006_FAST_BUILD *** build=" + string(DAL_M0006_NODE_BUILD)
         + "*runMode=" + run_mode
         + "*bars=" + IntegerToString(cfg.requested_bars)
         + "*newBarOnly=1"
         + "*tickExecution=0"
         + "*drawPre=" + IntegerToString(cfg.draw_pre_horizon_boxes ? 1 : 0)
         + "*onlyReversal=" + IntegerToString(cfg.draw_only_reversal_events ? 1 : 0)
         + "*source=M0001_EVENTS"
         + "*timePolicy=NODE_TIME_TO_FIRST_TOUCH_TIME"
         + "*colorAgePolicy=DYNAMIC_CHECK_UNTIL_ZONE_BACK_HIT_OR_PURPLE"
         + "*includeLiveBar=" + IntegerToString(InpH6IncludeLiveBar ? 1 : 0)
         + "*colorMonotonic=" + IntegerToString(InpH6NeverDowngradeBoxColor ? 1 : 0)
         + "*invalidBackHitPolicy=" + IntegerToString(InpH6InvalidateOnZoneBackHitBeforeMax ? 1 : 0)
         + "*zoneProjectionMode=" + DAL_M0006FastZoneProjectionModeName(cfg.zone_projection_mode)
         + "*nodeCappedInvalidateOnTouchCandle=" + IntegerToString(InpH6NodeCappedInvalidateOnTouchCandle ? 1 : 0));
   }

   DAL_M0006FastDrawEventBoxes(cfg);
}

int OnInit()
{
   g_m6_last_bar_time = iTime(M6Symbol(), M6Timeframe(), 0);
   g_m6_new_bar_counter = 0;

   if(InpH6ClearPersistentBoxesOnInit)
      DAL_M0006FastDeleteObjectsByPrefix("DAL_H6_PERSIST_BOX_");

   if(InpH6RunOnInit)
      RunM0006NodeSurvivalMap(InpBars, "init_backfill");

   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   // Boxes are persistent visual facts. Never clear them on deinit.
}

void OnTick()
{
   // Official H6 is new-bar only. No tick-level processing.
   datetime t = iTime(M6Symbol(), M6Timeframe(), 0);
   if(t <= 0 || t == g_m6_last_bar_time)
      return;

   g_m6_last_bar_time = t;
   g_m6_new_bar_counter++;

   int every_n = MathMax(1, InpH6UpdateEveryNBars);
   if((g_m6_new_bar_counter % every_n) != 0)
      return;

   int live_bars = (InpH6LiveUpdateBars > 0 ? InpH6LiveUpdateBars : InpBars);
   RunM0006NodeSurvivalMap(live_bars, "live_new_bar_window");
}
