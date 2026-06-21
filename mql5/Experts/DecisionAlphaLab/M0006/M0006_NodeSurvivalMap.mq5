//+------------------------------------------------------------------+
//| Decision Alpha Lab — M0006 Node Survival Map                       |
//| Hypothesis 6: nodes that remain unbroken after 20/50/100 candles   |
//| may be sharper optionality / edge candidates on the chart.          |
//+------------------------------------------------------------------+
#property strict
#property version   "1.04"
#property description "M0006 all-node reaction boxes: every touched raw node draws a zone box colored by candles after touch until zone-end retouch"

#include <DecisionAlphaLab/M0001/DAL_M0001Config.mqh>

input string InpSymbol = "";                    // empty = chart symbol
input ENUM_TIMEFRAMES InpTimeframe = PERIOD_CURRENT;
input int InpBars = 0;                           // 0 = recent contiguous fast window unless all-bars is true
input bool InpH6UseAllAvailableBars = false;     // true = full history; slower on huge M1 histories
input int InpH6FastDefaultClosedBars = 120000;   // contiguous recent window; not random sampling
input int InpWarmupHistoricalBars = 5000;

input int InpH6NodeHorizonRed = 20;
input int InpH6NodeHorizonGreen = 50;
input int InpH6NodeHorizonPurple = 100;
input double InpH6NodeTouchBufferPoints = 0.0;   // 0 = exact node touch/break
input double InpH6NodeBreakBufferPoints = 0.0;   // >0 requires a stronger break beyond node
input bool InpH6DrawNodeChart = true;
input bool InpH6DrawNodeLines = false;          // old horizontal survivor lines; boxes are official H6 visual
input bool InpH6ReactionBoxReport = true;
input bool InpH6DrawReactionBoxes = true;
input double InpH6ReactionAwayBufferPoints = 0.0;       // after touch, price must move away from node to confirm reaction
input double InpH6ReactionZoneEndBufferPoints = 0.0;    // if later price reaches touch extreme again, box survival fails
input double InpH6ReactionMinBoxHeightPoints = 5.0;     // visual minimum height when touch is exact
input int InpH6ReactionMaxChartObjects = 0;    // 0 = draw all touched-node reaction boxes
input bool InpH6ReactionBoxFill = true;
input bool InpH6ReactionBoxBack = true;
input int InpH6NodeMaxChartObjects = 0;        // 0 = draw all survivor lines if enabled
input int InpH6NodeLineWidth = 2;
input color InpH6NodeColorRed = clrRed;
input color InpH6NodeColorGreen = clrLime;
input color InpH6NodeColorPurple = clrPurple;

input bool InpH6UpdateOnNewBar = false;          // true = rerun and redraw when a new bar appears
input bool InpH6RunOnInit = true;

input int InpL = 5;
input double InpZoneRatio = 0.90;
input int InpExitGap = 6;
input ENUM_DALM0001ConsumeMode InpConsumeMode = DAL_M0001_CONSUME_BY_HUNT;
input int InpOutcomeCandleOffsetAfterExit = 0;
input bool InpWriteCsv = false;
input string InpCsvFileName = "M0006_Node_Survival_Map.csv";

#include <DecisionAlphaLab/M0006/DAL_M0006NodeSurvivalMap.mqh>

#define DAL_M0006_NODE_BUILD "1.04"

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
   DALM0004AtomicNoSampleConfig cfg;
   cfg.report_mode = DAL_M0004_ATOMIC_FAST_RAW_EVENT_BATCH;
   cfg.symbol = M6Symbol();
   cfg.timeframe = M6Timeframe();

   int available_closed_bars = Bars(M6Symbol(), M6Timeframe()) - 1;
   if(available_closed_bars < 0) available_closed_bars = 0;
   int requested_closed_bars = InpBars;
   string window_mode = "RECENT_CONTIGUOUS_FAST_WINDOW";
   if(InpH6UseAllAvailableBars)
   {
      requested_closed_bars = available_closed_bars;
      window_mode = "ALL_AVAILABLE_BARS_SLOW";
   }
   else if(requested_closed_bars <= 0)
   {
      requested_closed_bars = MathMax(2500, InpH6FastDefaultClosedBars);
      window_mode = "DEFAULT_RECENT_CONTIGUOUS_FAST_WINDOW";
   }

   cfg.replay_closed_bars = MathMin(available_closed_bars, MathMax(2500, requested_closed_bars));
   if(cfg.replay_closed_bars < 200) cfg.replay_closed_bars = MathMin(available_closed_bars, 2500);
   cfg.warmup_closed_bars = MathMin(InpWarmupHistoricalBars, MathMax(0, cfg.replay_closed_bars - 200));
   cfg.L = InpL;
   cfg.zone_ratio = InpZoneRatio;
   cfg.exit_gap = InpExitGap;
   cfg.consume_mode = InpConsumeMode;
   cfg.outcome_candle_offset_after_exit = InpOutcomeCandleOffsetAfterExit;
   cfg.require_event_rtv_ready = false;
   cfg.skip_ambiguous_energy_batch = true;
   cfg.permutation_iterations = 0;

   cfg.h6_only_report = true;
   cfg.h6_node_survival_report = true;
   cfg.h6_node_draw_chart = InpH6DrawNodeChart;
   cfg.h6_node_draw_lines = InpH6DrawNodeLines;
   cfg.h6_reaction_box_report = InpH6ReactionBoxReport;
   cfg.h6_reaction_box_draw_chart = InpH6DrawReactionBoxes;
   cfg.h6_reaction_away_buffer_points = MathMax(0.0, InpH6ReactionAwayBufferPoints);
   cfg.h6_reaction_zone_end_buffer_points = MathMax(0.0, InpH6ReactionZoneEndBufferPoints);
   cfg.h6_reaction_min_box_height_points = MathMax(0.0, InpH6ReactionMinBoxHeightPoints);
   cfg.h6_reaction_max_chart_objects = MathMax(0, InpH6ReactionMaxChartObjects);
   cfg.h6_reaction_box_fill = InpH6ReactionBoxFill;
   cfg.h6_reaction_box_back = InpH6ReactionBoxBack;
   cfg.h6_node_horizon_1 = MathMax(1, InpH6NodeHorizonRed);
   cfg.h6_node_horizon_2 = MathMax(cfg.h6_node_horizon_1 + 1, InpH6NodeHorizonGreen);
   cfg.h6_node_horizon_3 = MathMax(cfg.h6_node_horizon_2 + 1, InpH6NodeHorizonPurple);
   cfg.h6_node_touch_buffer_points = MathMax(0.0, InpH6NodeTouchBufferPoints);
   cfg.h6_node_break_buffer_points = MathMax(0.0, InpH6NodeBreakBufferPoints);
   cfg.h6_node_max_chart_objects = MathMax(0, InpH6NodeMaxChartObjects);
   cfg.h6_node_line_width = MathMax(1, InpH6NodeLineWidth);
   cfg.h6_node_color_1 = InpH6NodeColorRed;
   cfg.h6_node_color_2 = InpH6NodeColorGreen;
   cfg.h6_node_color_3 = InpH6NodeColorPurple;

   // Disable the old optionality/tail report path for the official H6 node map.
   cfg.print_h6_optionality_report = false;
   cfg.print_h6_edge_map = false;
   cfg.stress_h6_optionality = false;
   cfg.h6_stress_mode = 0;
   cfg.h6_edge_map_level = 0;
   cfg.h6_entry_anchor_mode = 1;
   cfg.h6_report_fast_horizon = false;
   cfg.h6_report_main_horizon = false;
   cfg.h6_report_slow_horizon = false;
   cfg.h6_print_compute_audit = false;
   cfg.h6_candle_stream_mode = true;
   cfg.h6_require_full_horizon = true;
   cfg.h6_horizon_fast = cfg.h6_node_horizon_1;
   cfg.h6_horizon_main = cfg.h6_node_horizon_2;
   cfg.h6_horizon_slow = cfg.h6_node_horizon_3;
   cfg.h6_atr_period = 14;
   cfg.h6_tail_atr_1 = 2.0;
   cfg.h6_tail_atr_2 = 4.0;
   cfg.h6_tail_atr_3 = 8.0;

   // Disable H4-only diagnostics in standalone H6.
   cfg.print_extended_report = false;
   cfg.print_deep_report = false;
   cfg.stress_transition_permutation = false;
   cfg.stress_run_shuffle = false;
   cfg.stress_block_concentration = false;
   cfg.stress_circular_shift = false;
   cfg.stress_local_block_shuffle = false;
   cfg.print_human_context_report = false;
   cfg.stress_context_shuffle = false;

   cfg.context_k_fast = 5;
   cfg.context_k_main = 10;
   cfg.context_k_slow = 20;
   cfg.context_ewma_alpha = 0.35;
   cfg.context_strong_threshold = 0.60;
   cfg.circular_min_shift_batches = 50;
   cfg.local_block_shuffle_size = 50;
   cfg.block_size_fast = 25;
   cfg.block_size_main = 50;
   cfg.block_size_slow = 200;
   cfg.print_only_summary = true;
   cfg.print_every_n_batches = 100;
   cfg.write_csv = InpWriteCsv;
   cfg.csv_file_name = InpCsvFileName;

   string sanity_line = "DAL_M0006_NODE_BUILD_SANITY *** symbol=" + M6Symbol()
      + "*tf=" + EnumToString(M6Timeframe())
      + "*build=" + DAL_M0006_NODE_BUILD
      + "*officialReport=H0006_ALL_NODE_REACTION_BOX_MAP"
      + "*sampleCalls=0*branchSamplesBuilt=0*m0002Calls=0"
      + "*contract=raw_m0001_nodes_known_time_no_sample_no_same_candle_order"
      + "*availableClosedBars=" + IntegerToString(available_closed_bars)
      + "*replayClosedBars=" + IntegerToString(cfg.replay_closed_bars)
      + "*windowMode=" + window_mode
      + "*horizons=" + IntegerToString(cfg.h6_node_horizon_1) + "/" + IntegerToString(cfg.h6_node_horizon_2) + "/" + IntegerToString(cfg.h6_node_horizon_3)
      + "*colors=red/green/purple"
      + "*drawChart=" + IntegerToString(cfg.h6_node_draw_chart ? 1 : 0)
      + "*drawLines=" + IntegerToString(cfg.h6_node_draw_lines ? 1 : 0)
      + "*drawReactionBoxes=" + IntegerToString(cfg.h6_reaction_box_draw_chart ? 1 : 0)
      + "*maxChartObjects=" + IntegerToString(cfg.h6_node_max_chart_objects)
      + "*maxReactionBoxes=" + IntegerToString(cfg.h6_reaction_max_chart_objects)
      + "*meaning=draw_all_raw_node_reaction_boxes_and_color_by_candles_after_touch_without_zone_end_retouch"
      + "*L=" + IntegerToString(cfg.L)
      + "*zoneRatio=" + DoubleToString(cfg.zone_ratio, 4)
      + "*exitGap=" + IntegerToString(cfg.exit_gap)
      + "*consumeMode=" + DAL_M0001ConsumeModeToString(cfg.consume_mode);
   Print(sanity_line);

   DAL_M0006RunNodeSurvivalMap(cfg);
   DAL_M0006CloseNodeSurvivalMap();
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
   DAL_M0006CloseNodeSurvivalMap();
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
