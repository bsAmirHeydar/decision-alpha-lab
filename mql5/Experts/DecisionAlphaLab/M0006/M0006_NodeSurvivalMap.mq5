//+------------------------------------------------------------------+
//| Decision Alpha Lab — M0006 All-Node Reaction Boxes                 |
//| Official H6 visual: draw every touched raw node as a reaction box.  |
//+------------------------------------------------------------------+
#property strict
#property version   "1.05"
#property description "Official H0006 direct all-node reaction box visual engine: no event dependency, no regime filter"

#include <DecisionAlphaLab/M0006/DAL_M0006AllNodeReactionBoxes.mqh>

input string InpSymbol = "";                    // empty = chart symbol
input ENUM_TIMEFRAMES InpTimeframe = PERIOD_CURRENT;
input int InpBars = 50000;                       // closed bars to scan; 0 = all available
input int InpL = 5;

input int InpH6NodeHorizonRed = 20;
input int InpH6NodeHorizonGreen = 50;
input int InpH6NodeHorizonPurple = 100;

input double InpH6NodeTouchBufferPoints = 0.0;
input double InpH6ReactionZoneEndBufferPoints = 0.0;
input double InpH6ReactionMinBoxHeightPoints = 0.0;

input bool InpH6DrawNodeChart = true;
input bool InpH6DrawReactionBoxes = true;
input int InpH6ReactionMaxChartObjects = 0;      // 0 = draw all boxes/markers
input bool InpH6ReactionBoxFill = true;
input bool InpH6ReactionBoxBack = true;
input int InpH6NodeLineWidth = 2;

input bool InpH6RequireCloseAwayAfterTouch = false;
input int InpH6MaxAwayScanBars = 3;

input color InpH6ColorPreActive = clrOrange;
input color InpH6ColorPreClosed = clrSilver;
input color InpH6ColorRed = clrRed;
input color InpH6ColorGreen = clrLime;
input color InpH6ColorPurple = clrPurple;
input color InpH6ColorTouchNoAway = clrYellow;

input bool InpH6UpdateOnNewBar = false;
input bool InpH6RunOnInit = true;

#define DAL_M0006_NODE_BUILD "1.05"

datetime g_m6_last_bar_time = 0;

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

void RunM0006NodeSurvivalMap()
{
   DALM0006ReactionBoxConfig cfg;
   DAL_M0006DefaultReactionBoxConfig(cfg);

   cfg.symbol = M6Symbol();
   cfg.timeframe = M6Timeframe();
   cfg.requested_closed_bars = InpBars;
   cfg.L = MathMax(1, InpL);

   cfg.draw_chart = InpH6DrawNodeChart && InpH6DrawReactionBoxes;
   cfg.max_boxes = InpH6ReactionMaxChartObjects;
   cfg.draw_back = InpH6ReactionBoxBack;
   cfg.fill = InpH6ReactionBoxFill;
   cfg.line_width = MathMax(1, InpH6NodeLineWidth);

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

   string sanity = "DAL_M0006_NODE_BUILD_SANITY *** build=" + string(DAL_M0006_NODE_BUILD)
      + "*officialReport=H0006_DIRECT_ALL_NODE_REACTION_BOX_VISUAL"
      + "*engine=direct_lrule_nodes_no_event_dependency"
      + "*symbol=" + cfg.symbol
      + "*tf=" + EnumToString(cfg.timeframe)
      + "*bars=" + IntegerToString(cfg.requested_closed_bars)
      + "*L=" + IntegerToString(cfg.L)
      + "*drawChart=" + IntegerToString(cfg.draw_chart ? 1 : 0)
      + "*maxObjects=" + IntegerToString(cfg.max_boxes)
      + "*horizons=" + IntegerToString(cfg.horizon_red) + "/" + IntegerToString(cfg.horizon_green) + "/" + IntegerToString(cfg.horizon_purple)
      + "*scope=all_raw_nodes_no_regime_filter"
      + "*box=time_node_origin_to_first_touch_price_node_to_touch_extreme"
      + "*colorRule=candles_after_touch_without_zone_end_retouch";
   Print(sanity);

   DAL_M0006RunAllNodeReactionBoxes(cfg);
}

int OnInit()
{
   g_m6_last_bar_time = iTime(M6Symbol(), M6Timeframe(), 0);
   if(InpH6RunOnInit)
      RunM0006NodeSurvivalMap();
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   // Keep H6 objects on chart for visual inspection.
}

void OnTick()
{
   if(!InpH6UpdateOnNewBar)
      return;

   datetime t = iTime(M6Symbol(), M6Timeframe(), 0);
   if(t <= 0 || t == g_m6_last_bar_time)
      return;

   g_m6_last_bar_time = t;
   RunM0006NodeSurvivalMap();
}
