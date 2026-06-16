//+------------------------------------------------------------------+
//| Decision Alpha Lab — M0001 Live Visual Lab                       |
//| Package-based live RTV audit inside MT5 / Strategy Tester.        |
//+------------------------------------------------------------------+
#property strict
#property version   "3.00"
#property description "M0001 live visual lab with debug packages and per-event audit layers"

#include <DecisionAlphaLab/M0001_Types.mqh>
#include <DecisionAlphaLab/M0001_Math.mqh>
#include <DecisionAlphaLab/M0001_LRuleNodes.mqh>
#include <DecisionAlphaLab/M0001_RTVEngine.mqh>
#include <DecisionAlphaLab/M0001_Drawer.mqh>

input string InpObjectPrefix        = "DAL_M0001_LIVE_";

input int    InpL                   = 5;
input double InpZoneRatio           = 0.90;
input int    InpExitGap             = 6;
input bool   InpConsumeOnTouch      = false;  // false = hunt mode; true = touch mode
input int    InpLookbackBars        = 1200;
input int    InpMaxBeforeLogs       = 500;

input bool   InpUseClosedBarsOnly   = true;
input bool   InpUpdateOnEveryTick   = false;
input int    InpTimerSeconds        = 1;
input bool   InpEngineIncludeOpenEvent = true;

// Package selector:
// 0 Custom
// 1 Structural Node Audit
// 2 Territory Construction Audit
// 3 Event Entry Exit Audit
// 4 Baseline vs Inside Sample Audit
// 5 RTV Formula Audit
// 6 Hunt Validation Audit
// 7 Live Open Event Audit
// 8 Candle Classification Audit
// 9 State Machine Audit
// 10 Focused Event Inspector
// 11 Multi Event Overview
// 12 Full Research Lab
input int    InpViewPreset          = 10;

// Focus selector:
// 0 None/latest
// 1 Selected Node/Revisit
// 2 Latest closed event
// 3 Latest open event
// 4 Latest hunted event
// 5 Strongest RTV event
input int    InpFocusMode           = 2;
input int    InpSelectedNodeId      = -1;
input int    InpSelectedRevisitId   = -1;

input bool   InpFilter_OnlyOpenEvents    = false;
input bool   InpFilter_OnlyClosedEvents  = false;
input bool   InpFilter_OnlyHuntedEvents  = false;
input bool   InpFilter_OnlyStrongRtv     = false;
input double InpFilter_MinRtv            = 0.0;
input double InpFilter_MaxRtv            = 0.0;
input double InpStrongRtvThreshold       = 1.25;

input int    InpMaxNodesToDraw      = 120;
input int    InpMaxEventsToDraw     = 80;
input int    InpMaxLabelsToDraw     = 80;
input bool   InpRenderLightMode     = true;
input bool   InpDeleteOnDeinit      = false;

// Custom package 1 — Structural Node Audit
input bool   InpPkg1_ShowNodes              = true;
input bool   InpPkg1_ShowNodeLabels         = true;
input bool   InpPkg1_ShowNodePriceLine      = true;
input bool   InpPkg1_ShowActiveFromLine     = true;
input bool   InpPkg1_ShowConfirmationWindow = true;

// Custom package 2 — Territory Construction Audit
input bool   InpPkg2_ShowExpansionExtreme   = true;
input bool   InpPkg2_ShowExpansionDistance  = true;
input bool   InpPkg2_ShowTerritoryBounds    = true;
input bool   InpPkg2_ShowTerritoryFill      = false;
input bool   InpPkg2_ShowZoneRatioLabel     = true;

// Custom package 3 — Event Entry Exit Audit
input bool   InpPkg3_ShowEventWindow        = true;
input bool   InpPkg3_ShowEntryMarker        = true;
input bool   InpPkg3_ShowExitMarker         = true;
input bool   InpPkg3_ShowOutsideCounter     = true;

// Custom package 4 — Baseline vs Inside Sample Audit
input bool   InpPkg4_ShowBeforeCandles        = true;
input bool   InpPkg4_ShowInsideCandles        = true;
input bool   InpPkg4_ShowOutsideActiveCandles = true;
input bool   InpPkg4_ShowSampleLegend         = true;

// Custom package 5 — RTV Formula Audit
input bool   InpPkg5_ShowRtvLabel       = true;
input bool   InpPkg5_ShowFormulaPanel   = true;
input bool   InpPkg5_ShowMeanInside     = true;
input bool   InpPkg5_ShowMeanBefore     = true;
input bool   InpPkg5_ShowMedians        = true;
input bool   InpPkg5_ShowCounts         = true;

// Custom package 6 — Hunt Validation Audit
input bool   InpPkg6_ShowHuntMarker     = true;
input bool   InpPkg6_ShowHuntLabel      = true;

// Custom package 7 — Live Open Event Audit
input bool   InpPkg7_ShowOpenEvent      = true;
input bool   InpPkg7_ShowLiveRtv        = true;
input bool   InpPkg7_ShowLiveCounts     = true;

// Custom package 8 — Candle Classification Audit
input bool   InpPkg8_ShowCandleTable          = true;
input bool   InpPkg8_ShowLogMoveValues        = true;
input bool   InpPkg8_ShowClassificationFlags  = true;
input int    InpPkg8_MaxCandlesInPanel        = 24;

// Custom package 9 — State Machine Audit
input bool   InpPkg9_ShowStateTimeline      = true;
input bool   InpPkg9_ShowStateLabels        = true;
input bool   InpPkg9_ShowTransitionMarkers  = true;
input bool   InpPkg9_ShowCurrentState       = true;

// Custom package 10 — Focused Event Inspector
input bool   InpPkg10_ShowInspectorCard     = true;
input bool   InpPkg10_ShowInspectorTable    = true;
input bool   InpPkg10_AutoFocusChart        = false;

// Custom package 11/12 — Overview / Research Lab
input bool   InpPkg11_ShowSummaryPanel      = true;


datetime g_last_bar_time = 0;
string   g_prefix;

//+------------------------------------------------------------------+
int OnInit()
{
   g_prefix = InpObjectPrefix + DAL_Sanitize(_Symbol) + "_" + DAL_Sanitize(EnumToString(_Period)) + "_";

   if(InpTimerSeconds > 0)
      EventSetTimer(InpTimerSeconds);

   RunLiveUpdate(true);
   return INIT_SUCCEEDED;
}

//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
   EventKillTimer();
   if(InpDeleteOnDeinit)
      DAL_DeleteObjects(g_prefix);
}

//+------------------------------------------------------------------+
void OnTimer()
{
   RunLiveUpdate(false);
}

//+------------------------------------------------------------------+
void OnTick()
{
   if(InpUpdateOnEveryTick)
      RunLiveUpdate(false);
   else
      RunOnNewBarOnly();
}

//+------------------------------------------------------------------+
void RunOnNewBarOnly()
{
   datetime last_closed_bar_time = iTime(_Symbol, _Period, 1);
   if(last_closed_bar_time == 0)
      return;

   if(last_closed_bar_time != g_last_bar_time)
      RunLiveUpdate(false);
}

//+------------------------------------------------------------------+
void BuildDrawOptions(DAL_DrawOptions &opt)
{
   opt.view_preset = InpViewPreset;
   opt.focus_mode = InpFocusMode;
   opt.selected_node_id = InpSelectedNodeId;
   opt.selected_revisit_id = InpSelectedRevisitId;

   opt.only_selected_event = false;
   opt.only_open_events = InpFilter_OnlyOpenEvents;
   opt.only_closed_events = InpFilter_OnlyClosedEvents;
   opt.only_hunted_events = InpFilter_OnlyHuntedEvents;
   opt.only_strong_rtv = InpFilter_OnlyStrongRtv;
   opt.min_rtv = InpFilter_MinRtv;
   opt.max_rtv = InpFilter_MaxRtv;
   opt.strong_rtv_threshold = InpStrongRtvThreshold;

   opt.show_nodes = InpPkg1_ShowNodes;
   opt.show_node_labels = InpPkg1_ShowNodeLabels;
   opt.show_node_price_line = InpPkg1_ShowNodePriceLine;
   opt.show_active_from_line = InpPkg1_ShowActiveFromLine;
   opt.show_confirmation_window = InpPkg1_ShowConfirmationWindow;

   opt.show_expansion_extreme = InpPkg2_ShowExpansionExtreme;
   opt.show_expansion_distance = InpPkg2_ShowExpansionDistance;
   opt.show_territory_bounds = InpPkg2_ShowTerritoryBounds;
   opt.show_territory_fill = InpPkg2_ShowTerritoryFill;
   opt.show_zone_ratio_label = InpPkg2_ShowZoneRatioLabel;

   opt.show_event_window = InpPkg3_ShowEventWindow;
   opt.show_entry_marker = InpPkg3_ShowEntryMarker;
   opt.show_exit_marker = InpPkg3_ShowExitMarker;
   opt.show_outside_counter = InpPkg3_ShowOutsideCounter;

   opt.show_before_candles = InpPkg4_ShowBeforeCandles;
   opt.show_inside_candles = InpPkg4_ShowInsideCandles;
   opt.show_outside_active_candles = InpPkg4_ShowOutsideActiveCandles;
   opt.show_sample_legend = InpPkg4_ShowSampleLegend;

   opt.show_rtv_label = InpPkg5_ShowRtvLabel;
   opt.show_formula_panel = InpPkg5_ShowFormulaPanel;
   opt.show_mean_inside = InpPkg5_ShowMeanInside;
   opt.show_mean_before = InpPkg5_ShowMeanBefore;
   opt.show_medians = InpPkg5_ShowMedians;
   opt.show_counts = InpPkg5_ShowCounts;

   opt.show_hunt_marker = InpPkg6_ShowHuntMarker;
   opt.show_hunt_label = InpPkg6_ShowHuntLabel;

   opt.show_open_event = InpPkg7_ShowOpenEvent;
   opt.show_live_rtv = InpPkg7_ShowLiveRtv;
   opt.show_live_counts = InpPkg7_ShowLiveCounts;

   opt.show_candle_table = InpPkg8_ShowCandleTable;
   opt.show_logmove_values = InpPkg8_ShowLogMoveValues;
   opt.show_classification_flags = InpPkg8_ShowClassificationFlags;
   opt.max_candles_in_panel = InpPkg8_MaxCandlesInPanel;

   opt.show_state_timeline = InpPkg9_ShowStateTimeline;
   opt.show_state_labels = InpPkg9_ShowStateLabels;
   opt.show_transition_markers = InpPkg9_ShowTransitionMarkers;
   opt.show_current_state = InpPkg9_ShowCurrentState;

   opt.show_inspector_card = InpPkg10_ShowInspectorCard;
   opt.show_inspector_table = InpPkg10_ShowInspectorTable;
   opt.auto_focus_chart = InpPkg10_AutoFocusChart;

   opt.show_summary_panel = InpPkg11_ShowSummaryPanel;
   opt.render_light_mode = InpRenderLightMode;
   opt.max_nodes_to_draw = InpMaxNodesToDraw;
   opt.max_events_to_draw = InpMaxEventsToDraw;
   opt.max_labels_to_draw = InpMaxLabelsToDraw;
}

//+------------------------------------------------------------------+
void RunLiveUpdate(const bool force)
{
   MqlRates rates[];
   ArraySetAsSeries(rates, false);

   int start_pos = InpUseClosedBarsOnly ? 1 : 0;
   int requested = MathMax(InpLookbackBars, InpL * 4 + InpExitGap + 50);
   int copied = CopyRates(_Symbol, _Period, start_pos, requested, rates);

   if(copied <= (InpL * 2 + InpExitGap + 5))
      return;

   ArraySetAsSeries(rates, false);

   datetime newest_time = rates[copied - 1].time;
   if(!force && !InpUpdateOnEveryTick && newest_time == g_last_bar_time)
      return;

   g_last_bar_time = newest_time;

   DAL_Node nodes[];
   int node_count = DAL_BuildLRuleNodes(rates, copied, InpL, nodes);

   DAL_Config cfg;
   cfg.L = InpL;
   cfg.zone_ratio = InpZoneRatio;
   cfg.exit_gap = InpExitGap;
   cfg.consume_on_touch = InpConsumeOnTouch;
   cfg.max_before_logs = InpMaxBeforeLogs;

   DAL_Event events[];
   int event_count = DAL_ComputeRTVEvents(rates, copied, nodes, cfg, InpEngineIncludeOpenEvent, events);

   DAL_DrawOptions opt;
   BuildDrawOptions(opt);

   DAL_DeleteObjects(g_prefix);
   int drawn = DAL_DrawRecentState(g_prefix, rates, copied, nodes, events, opt);

   ChartRedraw(0);
   Print("DAL M0001 LIVE | preset=", InpViewPreset,
         " bars=", copied,
         " nodes=", node_count,
         " events=", event_count,
         " drawn=", drawn,
         " last=", TimeToString(newest_time, TIME_DATE | TIME_MINUTES));
}
