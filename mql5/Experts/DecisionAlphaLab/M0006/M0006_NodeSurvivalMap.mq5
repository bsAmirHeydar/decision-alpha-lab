//+------------------------------------------------------------------+
//| Decision Alpha Lab — M0006 All-Node Reaction Boxes                 |
//| Official H6 visual: draw every touched raw node as a reaction box.  |
//+------------------------------------------------------------------+
#property strict
#property version   "1.16"
#property description "Official H0006 boxes-only persistent zones with isolated non-deletable box namespace"

#include <DecisionAlphaLab/M0006/DAL_M0006AllNodeReactionBoxes.mqh>

input string InpSymbol = "";                    // empty = chart symbol
input ENUM_TIMEFRAMES InpTimeframe = PERIOD_CURRENT;
input int InpBars = 50000;                       // full/backfill closed bars to scan; 0 = all available
input int InpH6LiveUpdateBars = 3000;             // lightweight live/new-bar window; 0 = use InpBars
input int InpH6UpdateEveryNBars = 1;              // 1 = every new candle; 5 = every 5 candles
input int InpL = 5;

input int InpH6NodeHorizonRed = 20;
input int InpH6NodeHorizonGreen = 50;
input int InpH6NodeHorizonPurple = 100;

input double InpH6NodeTouchBufferPoints = 0.0;
input double InpH6ReactionZoneEndBufferPoints = 0.0;
input double InpH6ReactionMinBoxHeightPoints = 0.0;

input bool InpH6IncludeLiveBar = true;           // include current forming bar so levels/colors update live
input bool InpH6PreserveExistingOnEmptyUpdate = true; // don't wipe chart when tester has not built enough bars yet
input bool InpH6PreserveMaturedBoxes = true;     // once a box appears, never delete it during live updates
input bool InpH6ClearAllObjectsOnInit = true;    // clears volatile/debug objects only; never deletes persistent boxes
input bool InpH6ClearPersistentBoxesOnInit = false; // manual cleanup only; keep false to never delete boxes
input int InpH6MinBarsForUpdate = 0;             // 0 = automatic safe minimum from L
input bool InpH6DrawNodeChart = true;
input bool InpH6DrawReactionBoxes = true;
input bool InpH6BoxesOnlyMode = true;           // official: only persistent boxes, no levels, no markers
input bool InpH6DrawNodeLevels = false;
input int InpH6ReactionMaxChartObjects = 0;      // 0 = draw all boxes/markers
input int InpH6LevelMaxChartObjects = 0;         // 0 = draw all node levels

input bool InpH6ShowPreHBoxes = false;
input bool InpH6ShowRedHorizonBoxes = true;
input bool InpH6ShowGreenHorizonBoxes = true;
input bool InpH6ShowPurpleHorizonBoxes = true;
input bool InpH6ShowConsumedBoxes = false;       // false = hide boxes whose zone end was retouched/consumed
input bool InpH6ShowOriginTouchMarkers = false;
input bool InpH6ShowUntouchedLevels = false;       // official: no zones/levels before first touch
input bool InpH6DrawBoxesOnlyAfterHorizon = true; // box appears only after H1/H2/H3 candles pass after touch

input int InpH6BoxLeftAnchorMode = 0;            // 0=node pivot/origin time, 1=known/active_from time
input int InpH6BoxRightAnchorMode = 0;           // 0=touch candle time, 1=touch candle end time

input bool InpH6ReactionBoxFill = true;
input bool InpH6ReactionBoxBack = true;
input int InpH6NodeLineWidth = 2;

input bool InpH6RequireCloseAwayAfterTouch = true;  // official reversal confirmation: later close must move away from touched node
input int InpH6MaxAwayScanBars = 3;

input color InpH6ColorPreActive = clrOrange;
input color InpH6ColorPreClosed = clrSilver;
input color InpH6ColorRed = clrRed;
input color InpH6ColorGreen = clrLime;
input color InpH6ColorPurple = clrPurple;
input color InpH6ColorTouchNoAway = clrYellow;
input color InpH6ColorUntouchedLevel = clrDeepSkyBlue;

input bool InpH6UpdateOnEveryTick = false;       // safer in visual tester; prevents tick-by-tick wipe/flicker
input bool InpH6UpdateOnNewBar = true;
input bool InpH6RunOnInit = true;

#define DAL_M0006_NODE_BUILD "1.16"

datetime g_m6_last_bar_time = 0;
int g_m6_new_bar_counter = 0;

string M6Symbol()
{
   if(InpSymbol == "") return _Symbol;
   return InpSymbol;
}

ENUM_TIMEFRAMES M6Timeframe()
{
   if(InpTimeframe == PERIOD_CURRENT) return (ENUM_TIMEFRAMES)_Period;
   return InpTimeframe;
}

void RunM0006NodeSurvivalMap(const int bars_override = -1, const string run_mode = "manual")
{
   DALM0006ReactionBoxConfig cfg;
   DAL_M0006DefaultReactionBoxConfig(cfg);

   cfg.symbol = M6Symbol();
   cfg.timeframe = M6Timeframe();
   cfg.requested_closed_bars = (bars_override > 0 ? bars_override : InpBars);
   cfg.L = MathMax(1, InpL);

   cfg.draw_chart = InpH6DrawNodeChart;
   cfg.include_live_bar = InpH6IncludeLiveBar;
   cfg.preserve_existing_on_empty_update = InpH6PreserveExistingOnEmptyUpdate;
   cfg.preserve_matured_boxes = InpH6PreserveMaturedBoxes;
   cfg.min_bars_for_update = MathMax(0, InpH6MinBarsForUpdate);
   cfg.max_boxes = InpH6ReactionMaxChartObjects;
   cfg.max_levels = InpH6LevelMaxChartObjects;
   cfg.draw_back = InpH6ReactionBoxBack;
   cfg.fill = InpH6ReactionBoxFill;
   cfg.line_width = MathMax(1, InpH6NodeLineWidth);
   cfg.draw_node_levels = (InpH6BoxesOnlyMode ? false : InpH6DrawNodeLevels);
   cfg.boxes_only_mode = InpH6BoxesOnlyMode;

   cfg.draw_boxes_only_after_horizon = InpH6DrawBoxesOnlyAfterHorizon;
   cfg.show_pre_stage = InpH6ShowPreHBoxes;
   cfg.show_red_stage = InpH6ShowRedHorizonBoxes;
   cfg.show_green_stage = InpH6ShowGreenHorizonBoxes;
   cfg.show_purple_stage = InpH6ShowPurpleHorizonBoxes;
   cfg.show_consumed_boxes = InpH6ShowConsumedBoxes;
   cfg.show_origin_touch_markers = (InpH6BoxesOnlyMode ? false : InpH6ShowOriginTouchMarkers);
   cfg.show_untouched_levels = (InpH6BoxesOnlyMode ? false : InpH6ShowUntouchedLevels);
   cfg.box_left_anchor_mode = MathMax(0, MathMin(1, InpH6BoxLeftAnchorMode));
   cfg.box_right_anchor_mode = MathMax(0, MathMin(1, InpH6BoxRightAnchorMode));

   cfg.horizon_red = MathMax(1, InpH6NodeHorizonRed);
   cfg.horizon_green = MathMax(cfg.horizon_red + 1, InpH6NodeHorizonGreen);
   cfg.horizon_purple = MathMax(cfg.horizon_green + 1, InpH6NodeHorizonPurple);

   cfg.touch_buffer_points = MathMax(0.0, InpH6NodeTouchBufferPoints);
   cfg.zone_end_retouch_buffer_points = MathMax(0.0, InpH6ReactionZoneEndBufferPoints);
   cfg.min_visual_box_points = MathMax(0.0, InpH6ReactionMinBoxHeightPoints);

   cfg.require_close_away_after_touch = InpH6RequireCloseAwayAfterTouch;
   cfg.max_away_scan_bars = MathMax(1, InpH6MaxAwayScanBars);

   cfg.color_pre_active = InpH6ColorPreActive;
   cfg.color_pre_closed = InpH6ColorPreClosed;
   cfg.color_red = InpH6ColorRed;
   cfg.color_green = InpH6ColorGreen;
   cfg.color_purple = InpH6ColorPurple;
   cfg.color_touch_no_away = InpH6ColorTouchNoAway;
   cfg.color_untouched_level = InpH6ColorUntouchedLevel;

   string sanity = "DAL_M0006_NODE_BUILD_SANITY *** build=" + string(DAL_M0006_NODE_BUILD)
      + "*officialReport=H0006_DIRECT_ALL_NODE_REACTION_BOX_VISUAL"
      + "*engine=direct_lrule_nodes_no_event_dependency"
      + "*symbol=" + cfg.symbol
      + "*tf=" + EnumToString(cfg.timeframe)
      + "*runMode=" + run_mode
      + "*bars=" + IntegerToString(cfg.requested_closed_bars)
      + "*fullBarsInput=" + IntegerToString(InpBars)
      + "*liveUpdateBarsInput=" + IntegerToString(InpH6LiveUpdateBars)
      + "*updateEveryNBars=" + IntegerToString(MathMax(1, InpH6UpdateEveryNBars))
      + "*L=" + IntegerToString(cfg.L)
      + "*drawChart=" + IntegerToString(cfg.draw_chart ? 1 : 0)
      + "*includeLiveBar=" + IntegerToString(cfg.include_live_bar ? 1 : 0)
      + "*preserveExistingOnEmpty=" + IntegerToString(cfg.preserve_existing_on_empty_update ? 1 : 0)
      + "*preserveMaturedBoxes=" + IntegerToString(cfg.preserve_matured_boxes ? 1 : 0)
      + "*clearVolatileObjectsOnInit=" + IntegerToString(InpH6ClearAllObjectsOnInit ? 1 : 0)
      + "*clearPersistentBoxesOnInit=" + IntegerToString(InpH6ClearPersistentBoxesOnInit ? 1 : 0)
      + "*boxPrefix=DAL_H6_PERSIST_BOX_"
      + "*volatilePrefix=DAL_H6_VOL_"
      + "*boxDeletePolicy=NEVER_DELETE_UNLESS_MANUAL_INPUT_TRUE"
      + "*boxUpdatePolicy=persistent_stable_name_color_only_update"
      + "*minBarsForUpdate=" + IntegerToString(cfg.min_bars_for_update)
      + "*updateEveryTick=" + IntegerToString(InpH6UpdateOnEveryTick ? 1 : 0)
      + "*updateOnNewBar=" + IntegerToString(InpH6UpdateOnNewBar ? 1 : 0)
      + "*boxesOnlyMode=" + IntegerToString(cfg.boxes_only_mode ? 1 : 0)
      + "*drawLevels=" + IntegerToString(cfg.draw_node_levels ? 1 : 0)
      + "*maxBoxObjects=" + IntegerToString(cfg.max_boxes)
      + "*maxLevelObjects=" + IntegerToString(cfg.max_levels)
      + "*drawBoxesOnlyAfterHorizon=" + IntegerToString(cfg.draw_boxes_only_after_horizon ? 1 : 0)
      + "*showPre=" + IntegerToString(cfg.show_pre_stage ? 1 : 0)
      + "*showRed=" + IntegerToString(cfg.show_red_stage ? 1 : 0)
      + "*showGreen=" + IntegerToString(cfg.show_green_stage ? 1 : 0)
      + "*showPurple=" + IntegerToString(cfg.show_purple_stage ? 1 : 0)
      + "*showConsumed=" + IntegerToString(cfg.show_consumed_boxes ? 1 : 0)
      + "*markerPolicy=" + (cfg.show_origin_touch_markers ? "ON" : "OFF")
      + "*showUntouchedLevels=" + IntegerToString(cfg.show_untouched_levels ? 1 : 0)
      + "*preTouchDrawPolicy=" + (cfg.show_untouched_levels ? "DEBUG_ON" : "OFF_OFFICIAL")
      + "*levelStartPolicy=AFTER_FIRST_TOUCH"
      + "*leftAnchorMode=" + IntegerToString(cfg.box_left_anchor_mode)
      + "*rightAnchorMode=" + IntegerToString(cfg.box_right_anchor_mode)
      + "*horizons=" + IntegerToString(cfg.horizon_red) + "/" + IntegerToString(cfg.horizon_green) + "/" + IntegerToString(cfg.horizon_purple)
      + "*scope=all_raw_nodes_no_regime_filter"
      + "*box=drawn_only_after_horizon_elapsed_after_touch_and_price_zone_start_to_zone_end"
      + "*colorRule=candles_after_touch_without_zone_end_retouch";
   Print(sanity);

   DAL_M0006RunAllNodeReactionBoxes(cfg);
}

int OnInit()
{
   g_m6_last_bar_time = iTime(M6Symbol(), M6Timeframe(), 0);
   g_m6_new_bar_counter = 0;

   if(InpH6ClearAllObjectsOnInit)
      DAL_M0006DeleteObjectsByPrefix("DAL_H6_VOL_");

   if(InpH6ClearPersistentBoxesOnInit)
      DAL_M0006DeleteObjectsByPrefix("DAL_H6_PERSIST_BOX_");

   if(InpH6RunOnInit)
      RunM0006NodeSurvivalMap(InpBars, "init_backfill");
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   // Keep H6 objects on chart for visual inspection.
}

void OnTick()
{
   if(InpH6UpdateOnEveryTick)
   {
      g_m6_last_bar_time = iTime(M6Symbol(), M6Timeframe(), 0);
      int live_bars_tick = (InpH6LiveUpdateBars > 0 ? InpH6LiveUpdateBars : InpBars);
      RunM0006NodeSurvivalMap(live_bars_tick, "live_tick_window");
      return;
   }

   if(!InpH6UpdateOnNewBar)
      return;

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
