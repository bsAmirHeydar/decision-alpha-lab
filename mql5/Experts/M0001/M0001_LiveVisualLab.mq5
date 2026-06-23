//+------------------------------------------------------------------+
//| Decision Alpha Lab — M0001 MQL-Native Live Visual Lab            |
//| Python-free runtime. MQL5 is the source of truth.                |
//+------------------------------------------------------------------+
#property strict
#property version   "1.61"
#property description "M0001 native MQL5 structural node and RTV visual lab"

#include <Market/DAL_Bars.mqh>
#include <Market/DAL_LiveBarStream.mqh>
#include <StructuralNodes/DAL_StructuralNodeEngine.mqh>
#include <M0001/DAL_M0001Config.mqh>
#include <M0001/DAL_M0001Engine.mqh>
#include <M0001/DAL_M0001AuditState.mqh>
#include <M0001/DAL_M0001Visual.mqh>
#include <M0001/DAL_M0001RtvNullComparison.mqh>

input string InpSymbol = "";                 // empty = chart symbol
input ENUM_TIMEFRAMES InpTimeframe = PERIOD_CURRENT;
input int InpBars = 0;                       // 0 = no cap
input int InpWarmupHistoricalBars = 5000;     // pre-test closed bars used only to seed old nodes

input int InpL = 5;
input double InpZoneRatio = 0.90;
input int InpExitGap = 6;
input ENUM_DALM0001ConsumeMode InpConsumeMode = DAL_M0001_CONSUME_BY_HUNT;

input bool InpShowNodes = true;
input bool InpShowZones = true;
input bool InpShowRevisits = true;
input bool InpShowEvents = false;        // optional frozen event boxes; off for a clean chart
input bool InpShowRTV = false;
input bool InpShowState = true;
input bool InpShowExtremes = false;
input bool InpShowSummary = true;
input bool InpRuntimeVisuals = false;        // true = redraw on each closed candle; false = final-only fast mode
input bool InpDrawFinalVisuals = true;         // draw the final audited chart state once at the end
input bool InpKeepVisualsOnDeinit = true;      // keep final chart objects after the test finishes

input bool InpPrintHistogram = false;          // optional; off keeps final Journal lines compact
input int InpRandomSamplesPerEvent = 20;       // K matched random windows per node event
input int InpBootstrapIterations = 300;        // bootstrap CI for paired deltas; 0 = off
input int InpPermutationIterations = 500;      // sign-flip permutation p-value; 0 = off
input int InpValidationSplits = 5;             // chronological split-stability report
input bool InpRunStressSuite = true;            // hard nulls, placebo, outlier, non-overlap, block bootstrap, horizons
input int InpBrokerUtcOffsetHours = 0;          // broker server time = UTC + offset; used for UTC session reports
input int InpRegimeLookbackBars = 100;          // pre-entry realized-volatility regime lookback
input int InpHardRandomCandidates = 80;         // candidates per event for hard matched random null
input int InpPlaceboShiftBars = 50;             // +/- shifted-entry placebo distance
input int InpNonOverlapGapBars = 0;             // minimum gap after event end for non-overlap stress
input int InpBlockBootstrapIterations = 300;    // block-bootstrap CI for dependent market events
input int InpBlockBootstrapBlockPairs = 25;     // contiguous pair-block length for block bootstrap
input int InpHorizonBars1 = 5;                  // fixed-horizon stress #1
input int InpHorizonBars2 = 10;                 // fixed-horizon stress #2
input int InpHorizonBars3 = 20;                 // fixed-horizon stress #3
input int InpHorizonBars4 = 50;                 // fixed-horizon stress #4
input bool InpRunParameterRobustness = false;  // optional slow grid around current L/zone/gap

// Internal defaults kept out of the Inputs panel.
#define DAL_M0001_OBJECT_PREFIX "DAL_MQL_M0001_"
#define DAL_M0001_USE_LIVE_BAR_STREAM true
#define DAL_M0001_START_FROM_NEXT_CLOSED_BAR true
#define DAL_M0001_CLOSED_BARS_ONLY true
#define DAL_M0001_TIMER_MS 0

#define DAL_M0001_DRAW_ONLY_VISIBLE_WINDOW true
#define DAL_M0001_VISIBLE_WINDOW_PADDING_BARS 80
#define DAL_M0001_REDRAW_ON_CHART_CHANGE true
#define DAL_M0001_PURGE_TRACE_LINES true
#define DAL_M0001_PURGE_MAIN_WINDOW_INDICATORS true

#define DAL_M0001_SHOW_NODE_PRICES true
#define DAL_M0001_SHOW_ACTIVE_FROM false
#define DAL_M0001_SHOW_EVENTS false
#define DAL_M0001_SHOW_RTV_LABELS false
#define DAL_M0001_SHOW_NODE_VISIBILITY_DEBUG false
#define DAL_M0001_SHOW_CONSUMED_HISTORY true

#define DAL_M0001_MAX_EVENTS 0
#define DAL_M0001_MIN_RTV 0.0
#define DAL_M0001_PRINT_RUN_STATUS false
#define DAL_M0001_MAX_NODES_TO_DRAW 0
#define DAL_M0001_MAX_EVENTS_TO_DRAW 0
#define DAL_M0001_MAX_AUDIT_STATES_TO_DRAW 0

#define DAL_M0001_NODE_ARROW_WIDTH 2
#define DAL_M0001_HIGH_NODE_PRICE_TEXT_GAP_POINTS 120.0
#define DAL_M0001_LOW_NODE_PRICE_TEXT_GAP_POINTS 120.0
#define DAL_M0001_NODE_PRICE_TEXT_FONT_SIZE 9

datetime g_last_open_bar_time = 0;
datetime g_last_closed_stream_bar_time = 0;
datetime g_analysis_start_time = 0;
bool g_live_stream_initialized = false;
DALBar g_live_bars[];
int g_live_bars_count = 0;


string LabSymbol()
{
   if(InpSymbol == "")
      return _Symbol;
   return InpSymbol;
}

ENUM_TIMEFRAMES LabTimeframe()
{
   if(InpTimeframe == PERIOD_CURRENT)
      return (ENUM_TIMEFRAMES)_Period;
   return InpTimeframe;
}

void InitializeCandleClock()
{
   g_last_open_bar_time = iTime(LabSymbol(), LabTimeframe(), 0);
}

bool HasNewClosedCandle()
{
   datetime current_open_bar_time = iTime(LabSymbol(), LabTimeframe(), 0);
   if(current_open_bar_time <= 0)
      return false;

   if(g_last_open_bar_time <= 0)
   {
      g_last_open_bar_time = current_open_bar_time;
      return false;
   }

   if(current_open_bar_time == g_last_open_bar_time)
      return false;

   g_last_open_bar_time = current_open_bar_time;
   return true;
}

void BuildConfig(DALM0001Config &config)
{
   DAL_M0001DefaultConfig(config);
   config.L = InpL;
   config.zone_ratio = InpZoneRatio;
   config.exit_gap = InpExitGap;
   config.consume_mode = InpConsumeMode;
   config.consume_on_touch = false;

   if(config.consume_on_touch)
      config.consume_mode = DAL_M0001_CONSUME_BY_TOUCH;

   config.max_events = DAL_M0001_MAX_EVENTS;
   config.min_rtv = DAL_M0001_MIN_RTV;
}

bool ResolveChartVisibleTimeWindow(
   datetime &window_from,
   datetime &window_to
)
{
   if(!DAL_M0001_DRAW_ONLY_VISIBLE_WINDOW)
      return false;

   long first_visible = 0;
   long visible_bars = 0;

   if(!ChartGetInteger(0, CHART_FIRST_VISIBLE_BAR, 0, first_visible))
      return false;

   if(!ChartGetInteger(0, CHART_VISIBLE_BARS, 0, visible_bars))
      return false;

   if(first_visible < 0 || visible_bars <= 0)
      return false;

   int padding = DAL_M0001_VISIBLE_WINDOW_PADDING_BARS;
   if(padding < 0)
      padding = 0;

   int left_shift = (int)first_visible + padding;
   int right_shift = (int)first_visible - (int)visible_bars + 1 - padding;

   if(right_shift < 0)
      right_shift = 0;

   datetime left_time = iTime(LabSymbol(), LabTimeframe(), left_shift);
   datetime right_time = iTime(LabSymbol(), LabTimeframe(), right_shift);

   if(left_time <= 0 || right_time <= 0)
      return false;

   if(left_time <= right_time)
   {
      window_from = left_time;
      window_to = right_time;
   }
   else
   {
      window_from = right_time;
      window_to = left_time;
   }

   return (window_from > 0 && window_to > 0 && window_to >= window_from);
}

void BuildVisualConfig(DALM0001VisualConfig &visual)
{
   DAL_M0001DefaultVisualConfig(visual);
   visual.prefix = DAL_M0001_OBJECT_PREFIX;
   visual.show_nodes = InpShowNodes;
   visual.show_node_prices = DAL_M0001_SHOW_NODE_PRICES;
   // Hard-disabled: full-chart node price lines create visual noise.
   // Use DAL_M0001_SHOW_NODE_PRICES for local text labels above/below node markers.
   visual.show_node_price_lines = false;
   visual.show_active_from = DAL_M0001_SHOW_ACTIVE_FROM;
   visual.show_events = InpShowEvents;
   visual.show_rtv_labels = InpShowRTV;
   visual.show_revisit_labels = InpShowRevisits;
   visual.show_node_state_labels = InpShowState;
   visual.show_hunts = InpShowState;
   visual.show_node_visibility_debug = DAL_M0001_SHOW_NODE_VISIBILITY_DEBUG;
   visual.show_expansion_extreme_lines = InpShowExtremes;
   visual.show_consumed_extreme_history = DAL_M0001_SHOW_CONSUMED_HISTORY;
   visual.show_live_hunt_zones = InpShowZones;
   visual.show_invalidated_hunt_zones = false;
   visual.show_consumed_hunt_zone_history = DAL_M0001_SHOW_CONSUMED_HISTORY;
   visual.show_consumed_node_markers = InpShowState;
   visual.max_nodes = DAL_M0001_MAX_NODES_TO_DRAW;
   visual.max_events = DAL_M0001_MAX_EVENTS_TO_DRAW;
   visual.max_audit_states = DAL_M0001_MAX_AUDIT_STATES_TO_DRAW;
   // Hard-disabled: chevron mode creates diagonal high/low trace lines.
   visual.node_marker_style = 0;
   visual.node_arrow_width = DAL_M0001_NODE_ARROW_WIDTH;
   visual.chevron_points = 70.0;
   visual.chevron_bars = 0.28;
   visual.chevron_width = 2;
   visual.high_node_price_text_gap_points = DAL_M0001_HIGH_NODE_PRICE_TEXT_GAP_POINTS;
   visual.low_node_price_text_gap_points = DAL_M0001_LOW_NODE_PRICE_TEXT_GAP_POINTS;
   visual.node_price_text_font_size = DAL_M0001_NODE_PRICE_TEXT_FONT_SIZE;

   datetime visible_from = 0;
   datetime visible_to = 0;
   visual.use_time_window = ResolveChartVisibleTimeWindow(visible_from, visible_to);
   visual.time_window_from = visible_from;
   visual.time_window_to = visible_to;
}



void BuildRtvReportConfig(DALM0001RtvReportConfig &report)
{
   DAL_M0001DefaultRtvReportConfig(report);
   report.print_histogram = InpPrintHistogram;
   report.random_samples_per_event = InpRandomSamplesPerEvent;
   report.bootstrap_iterations = InpBootstrapIterations;
   report.permutation_iterations = InpPermutationIterations;
   report.validation_splits = InpValidationSplits;
   report.run_stress_suite = InpRunStressSuite;
   report.broker_utc_offset_hours = InpBrokerUtcOffsetHours;
   report.regime_lookback_bars = InpRegimeLookbackBars;
   report.hard_random_candidates = InpHardRandomCandidates;
   report.placebo_shift_bars = InpPlaceboShiftBars;
   report.nonoverlap_gap_bars = InpNonOverlapGapBars;
   report.block_bootstrap_iterations = InpBlockBootstrapIterations;
   report.block_bootstrap_block_pairs = InpBlockBootstrapBlockPairs;
   report.horizon_bars_1 = InpHorizonBars1;
   report.horizon_bars_2 = InpHorizonBars2;
   report.horizon_bars_3 = InpHorizonBars3;
   report.horizon_bars_4 = InpHorizonBars4;

   if(report.random_samples_per_event < 1)
      report.random_samples_per_event = 1;
   if(report.bootstrap_iterations < 0)
      report.bootstrap_iterations = 0;
   if(report.permutation_iterations < 0)
      report.permutation_iterations = 0;
   if(report.validation_splits < 1)
      report.validation_splits = 1;
   if(report.regime_lookback_bars < 1)
      report.regime_lookback_bars = 1;
   if(report.hard_random_candidates < 1)
      report.hard_random_candidates = 1;
   if(report.placebo_shift_bars < 1)
      report.placebo_shift_bars = 1;
   if(report.nonoverlap_gap_bars < 0)
      report.nonoverlap_gap_bars = 0;
   if(report.block_bootstrap_iterations < 0)
      report.block_bootstrap_iterations = 0;
   if(report.block_bootstrap_block_pairs < 1)
      report.block_bootstrap_block_pairs = 1;
}


void DAL_M0001UpdateRuntimeComment(
   const int bars_count,
   const int nodes_count,
   const int events_count,
   const int audit_states_count,
   const string source_mode
)
{
   string start_text = g_analysis_start_time > 0 ? TimeToString(g_analysis_start_time, TIME_DATE | TIME_MINUTES) : "pending";

   Comment(
      "Decision Alpha Lab | M0001 Runtime\n",
      "source=", source_mode,
      "  symbol=", LabSymbol(),
      "  tf=", EnumToString(LabTimeframe()), "\n",
      "bars=", bars_count,
      "  nodes=", nodes_count,
      "  events=", events_count,
      "  audit_states=", audit_states_count, "\n",
      "warmup_bars=", InpWarmupHistoricalBars,
      "  analysis_start=", start_text, "\n",
      "runtime_visuals=", (InpRuntimeVisuals ? "on" : "off"),
      "  final_visuals=", (InpDrawFinalVisuals ? "on" : "off"),
      "  keep_visuals=", (InpKeepVisualsOnDeinit ? "on" : "off"), "\n",
      "randomK=", InpRandomSamplesPerEvent,
      "  bootstrap=", InpBootstrapIterations,
      "  permutation=", InpPermutationIterations,
      "  splits=", InpValidationSplits, "\n",
      "stress=", (InpRunStressSuite ? "on" : "off"),
      "  utcOffset=", InpBrokerUtcOffsetHours,
      "  regimeLookback=", InpRegimeLookbackBars,
      "  hardCandidates=", InpHardRandomCandidates, "\n",
      "compact final validation report prints once on deinit"
   );
}


void DAL_M0001DrawComputedState(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const DALM0001Event &events[],
   const int events_count,
   const DALM0001NodeAuditState &audit_states[],
   const int audit_states_count,
   const DALM0001Config &config,
   const string source_mode
)
{
   DALM0001VisualConfig visual;
   BuildVisualConfig(visual);

   if(DAL_M0001_PURGE_TRACE_LINES)
      DAL_DeleteTraceLineObjects();

   DAL_DeleteM0001VisualArtifacts(DAL_M0001_OBJECT_PREFIX);
   DAL_M0001DrawNodes(nodes, nodes_count, visual, LabTimeframe());
   DAL_M0001DrawAuditStates(audit_states, audit_states_count, visual, config);
   DAL_M0001DrawEvents(events, events_count, visual, config);

   if(InpShowSummary)
      DAL_M0001DrawSummary(DAL_M0001_OBJECT_PREFIX, bars_count, nodes_count, events_count, audit_states_count, config, visual, nodes);

   ChartRedraw(0);
}

void DAL_M0001ComputeState(
   const DALBar &bars[],
   const int bars_count,
   const DALM0001Config &config,
   DALLRuleNode &nodes[],
   int &nodes_count,
   DALM0001Event &events[],
   int &events_count,
   DALM0001NodeAuditState &audit_states[],
   int &audit_states_count
)
{
   ArrayResize(nodes, 0);
   ArrayResize(events, 0);
   ArrayResize(audit_states, 0);

   nodes_count = 0;
   events_count = 0;
   audit_states_count = 0;

   if(bars_count <= 0)
      return;

   nodes_count = DAL_DetectConfirmedStructuralNodes(bars, bars_count, config.L, nodes);
   events_count = DAL_M0001ComputeEvents(bars, bars_count, nodes, nodes_count, config, events);
   audit_states_count = DAL_M0001ComputeNodeAuditStates(bars, bars_count, nodes, nodes_count, config, audit_states);
}

void RunM0001FromBars(
   const DALBar &bars[],
   const int bars_count,
   const string source_mode
)
{
   if(bars_count <= 0)
      return;

   DALM0001Config config;
   BuildConfig(config);

   DALLRuleNode nodes[];
   DALM0001Event events[];
   DALM0001NodeAuditState audit_states[];
   int nodes_count = 0;
   int events_count = 0;
   int audit_states_count = 0;

   DAL_M0001ComputeState(
      bars,
      bars_count,
      config,
      nodes,
      nodes_count,
      events,
      events_count,
      audit_states,
      audit_states_count
   );

   DAL_M0001UpdateRuntimeComment(bars_count, nodes_count, events_count, audit_states_count, source_mode);
   DAL_M0001DrawComputedState(bars, bars_count, nodes, nodes_count, events, events_count, audit_states, audit_states_count, config, source_mode);

   if(DAL_M0001_PRINT_RUN_STATUS)
   {
      Print(
         "DAL M0001 MQL-NATIVE | source=", source_mode,
         " bars=", bars_count,
         " nodes=", nodes_count,
         " events=", events_count,
         " L=", config.L,
         " zone=", DoubleToString(config.zone_ratio, 2),
         " gap=", config.exit_gap,
         " consume=", DAL_M0001ConsumeModeToString(config.consume_mode)
      );
   }
}

void InitializeLiveBarStream()
{
   if(g_live_stream_initialized)
      return;

   ArrayResize(g_live_bars, 0);
   g_live_bars_count = 0;
   g_last_closed_stream_bar_time = 0;

   int warmup_bars = InpWarmupHistoricalBars;
   if(warmup_bars < 0)
      warmup_bars = 0;

   if(warmup_bars > 0)
   {
      DAL_WarmupClosedBarsByShift(
         LabSymbol(),
         LabTimeframe(),
         warmup_bars,
         0,
         g_live_bars,
         g_live_bars_count
      );

      if(g_live_bars_count > 0)
         g_last_closed_stream_bar_time = g_live_bars[g_live_bars_count - 1].time;
   }
   else if(DAL_M0001_START_FROM_NEXT_CLOSED_BAR)
   {
      // Critical live-safe behavior:
      // Do not copy/process history at attach time. Start only when the next bar closes.
      g_last_closed_stream_bar_time = DAL_LastClosedBarTime(LabSymbol(), LabTimeframe());
   }

   g_live_stream_initialized = true;
}

bool UpdateLiveBarStream()
{
   InitializeLiveBarStream();

   int before_count = g_live_bars_count;

   bool appended = DAL_AppendLatestClosedBarIfNew(
      LabSymbol(),
      LabTimeframe(),
      InpBars,
      g_live_bars,
      g_live_bars_count,
      g_last_closed_stream_bar_time
   );

   if(appended && g_analysis_start_time <= 0 && g_live_bars_count > before_count)
      g_analysis_start_time = g_live_bars[g_live_bars_count - 1].time;

   return appended;
}



void DAL_M0001PrintParameterRobustnessGrid(
   const DALBar &bars[],
   const int bars_count,
   const string source_mode,
   const DALM0001RtvReportConfig &report_config
)
{
   if(bars_count <= 0)
      return;

   int l_values[5];
   l_values[0] = InpL - 2;
   l_values[1] = InpL - 1;
   l_values[2] = InpL;
   l_values[3] = InpL + 1;
   l_values[4] = InpL + 2;

   double zone_values[3];
   zone_values[0] = InpZoneRatio - 0.05;
   zone_values[1] = InpZoneRatio;
   zone_values[2] = InpZoneRatio + 0.05;

   int gap_values[3];
   gap_values[0] = InpExitGap - 1;
   gap_values[1] = InpExitGap;
   gap_values[2] = InpExitGap + 1;

   double dlog_values[];
   ArrayResize(dlog_values, 0);

   int combos = 0;
   int valid = 0;
   int positive_mean = 0;
   int positive_median = 0;
   int win_over_50 = 0;
   int min_n = 0;
   double min_dlog = 0.0;
   double max_dlog = 0.0;
   double total_dlog = 0.0;
   double total_win = 0.0;

   for(int li = 0; li < 5; li++)
   {
      int L = l_values[li];
      if(L < 1)
         continue;

      for(int zi = 0; zi < 3; zi++)
      {
         double zone = zone_values[zi];
         if(zone <= 0.0 || zone >= 0.999)
            continue;

         for(int gi = 0; gi < 3; gi++)
         {
            int gap = gap_values[gi];
            if(gap < 1)
               continue;

            combos++;

            DALM0001Config cfg;
            BuildConfig(cfg);
            cfg.L = L;
            cfg.zone_ratio = zone;
            cfg.exit_gap = gap;

            DALLRuleNode nodes[];
            DALM0001Event events[];
            DALM0001NodeAuditState audit_states[];
            int nodes_count = 0;
            int events_count = 0;
            int audit_states_count = 0;

            DAL_M0001ComputeState(bars, bars_count, cfg, nodes, nodes_count, events, events_count, audit_states, audit_states_count);

            DALM0001PairedLogRtv pairs[];
            double node_logs[];
            double random_logs[];
            DALM0001IntegrityAudit audit;
            int random_k = report_config.random_samples_per_event;
            if(random_k > 5)
               random_k = 5; // parameter grid is an optional robustness sweep; keep it bounded.
            if(random_k < 1)
               random_k = 1;

            int pair_count = DAL_M0001CollectPairedLogRtvs(events, events_count, bars, bars_count, g_analysis_start_time, random_k, report_config.broker_utc_offset_hours, report_config.regime_lookback_bars, pairs, node_logs, random_logs, audit);
            if(pair_count <= 10)
               continue;

            DALM0001LogRtvStats node_stats;
            DALM0001LogRtvStats random_stats;
            DALM0001LogRtvComparison cmp;
            DAL_M0001ComputeLogRtvStats(node_logs, node_stats);
            DAL_M0001ComputeLogRtvStats(random_logs, random_stats);
            DAL_M0001ComputeLogRtvComparison(node_logs, random_logs, node_stats, random_stats, cmp);

            valid++;
            if(min_n == 0 || pair_count < min_n)
               min_n = pair_count;

            if(valid == 1 || cmp.delta_log_mean < min_dlog)
               min_dlog = cmp.delta_log_mean;
            if(valid == 1 || cmp.delta_log_mean > max_dlog)
               max_dlog = cmp.delta_log_mean;

            if(cmp.delta_log_mean > 0.0)
               positive_mean++;
            if(cmp.delta_log_median > 0.0)
               positive_median++;
            if(cmp.paired_win_pct > 50.0)
               win_over_50++;

            total_dlog += cmp.delta_log_mean;
            total_win += cmp.paired_win_pct;

            int size = ArraySize(dlog_values);
            ArrayResize(dlog_values, size + 1);
            dlog_values[size] = cmp.delta_log_mean;
         }
      }
   }

   double median_dlog = 0.0;
   if(ArraySize(dlog_values) > 0)
   {
      ArraySort(dlog_values);
      median_dlog = DAL_M0001NullPercentileSorted(dlog_values, 0.50);
   }

   double mean_dlog = valid > 0 ? total_dlog / valid : 0.0;
   double mean_win = valid > 0 ? total_win / valid : 0.0;
   double robust_param_pct = valid > 0 ? 100.0 * positive_mean / valid : 0.0;
   double positive_median_pct = valid > 0 ? 100.0 * positive_median / valid : 0.0;
   double win_over_50_pct = valid > 0 ? 100.0 * win_over_50 / valid : 0.0;

   Print(
      "DAL_M0001_FINAL_PARAM_ROBUST *** symbol=", LabSymbol(),
      "*tf=", EnumToString(LabTimeframe()),
      "*source=", source_mode,
      "*analysisStart=", DAL_M0001AnalysisStartText(g_analysis_start_time),
      " *** PARAM_GRID",
      "*combos=", combos,
      "*valid=", valid,
      "*minN=", min_n,
      "*robustParamPct=", DAL_M0001FmtPct(robust_param_pct),
      "*positiveMedianPct=", DAL_M0001FmtPct(positive_median_pct),
      "*winOver50Pct=", DAL_M0001FmtPct(win_over_50_pct),
      "*meanDLog=", DAL_M0001Fmt4(mean_dlog),
      "*medianDLog=", DAL_M0001Fmt4(median_dlog),
      "*minDLog=", DAL_M0001Fmt4(min_dlog),
      "*maxDLog=", DAL_M0001Fmt4(max_dlog),
      "*meanWinPct=", DAL_M0001FmtPct(mean_win),
      "*grid=Lpm2_zonepm0.05_gappm1",
      "*gridRandomK=", DAL_M0001IntMin(report_config.random_samples_per_event, 5)
   );
}

void DAL_M0001PrintFinalReportsFromBars(
   const DALBar &bars[],
   const int bars_count,
   const string source_mode
)
{
   if(bars_count <= 0)
      return;

   DALM0001Config config;
   BuildConfig(config);

   DALLRuleNode nodes[];
   DALM0001Event events[];
   DALM0001NodeAuditState audit_states[];
   int nodes_count = 0;
   int events_count = 0;
   int audit_states_count = 0;

   // Final-only mode computes the full research state exactly once here.
   // The same computed arrays feed both the final statistics and the restored
   // chart drawings, so final visuals cannot drift from the final report.
   DAL_M0001ComputeState(
      bars,
      bars_count,
      config,
      nodes,
      nodes_count,
      events,
      events_count,
      audit_states,
      audit_states_count
   );

   DAL_M0001UpdateRuntimeComment(bars_count, nodes_count, events_count, audit_states_count, source_mode);

   DALM0001RtvReportConfig report_config;
   BuildRtvReportConfig(report_config);

   DAL_M0001PrintFinalNodeRandomReports(
      events,
      events_count,
      bars,
      bars_count,
      LabSymbol(),
      EnumToString(LabTimeframe()),
      source_mode,
      g_analysis_start_time,
      report_config
   );

   if(InpRunParameterRobustness)
      DAL_M0001PrintParameterRobustnessGrid(bars, bars_count, source_mode, report_config);

   if(InpDrawFinalVisuals)
      DAL_M0001DrawComputedState(bars, bars_count, nodes, nodes_count, events, events_count, audit_states, audit_states_count, config, "final_visual_state");
}

void DAL_M0001PrintFinalReports()
{
   if(DAL_M0001_USE_LIVE_BAR_STREAM)
   {
      DAL_M0001PrintFinalReportsFromBars(g_live_bars, g_live_bars_count, "final_live_stream");
      return;
   }

   DALBar bars[];
   int bars_count = DAL_LoadBarsChronological(LabSymbol(), LabTimeframe(), InpBars, DAL_M0001_CLOSED_BARS_ONLY, bars);
   DAL_M0001PrintFinalReportsFromBars(bars, bars_count, "final_copyrates");
}

void RunM0001()
{
   if(DAL_M0001_USE_LIVE_BAR_STREAM)
   {
      InitializeLiveBarStream();
      RunM0001FromBars(g_live_bars, g_live_bars_count, "live_stream");
      return;
   }

   DALBar bars[];
   int bars_count = DAL_LoadBarsChronological(LabSymbol(), LabTimeframe(), InpBars, DAL_M0001_CLOSED_BARS_ONLY, bars);
   RunM0001FromBars(bars, bars_count, "fallback_copyrates");
}

int OnInit()
{
   if(DAL_M0001_PURGE_MAIN_WINDOW_INDICATORS)
      DAL_DeleteMainWindowIndicators();

   InitializeCandleClock();

   if(DAL_M0001_USE_LIVE_BAR_STREAM)
   {
      InitializeLiveBarStream();

      if(InpRuntimeVisuals)
         RunM0001FromBars(g_live_bars, g_live_bars_count, "live_stream_warmup_ready");
      else
         DAL_M0001UpdateRuntimeComment(g_live_bars_count, 0, 0, 0, "fast_final_only_warmup_ready");
   }
   else
   {
      if(InpRuntimeVisuals)
         RunM0001();
      else
         DAL_M0001UpdateRuntimeComment(0, 0, 0, 0, "fast_final_only_copyrates_ready");
   }

   if(DAL_M0001_TIMER_MS > 0)
      EventSetMillisecondTimer(DAL_M0001_TIMER_MS);

   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   DAL_M0001PrintFinalReports();

   EventKillTimer();

   if(!InpKeepVisualsOnDeinit)
   {
      DAL_DeleteM0001VisualArtifacts(DAL_M0001_OBJECT_PREFIX);
      Comment("");
   }
}

void OnTick()
{
   // Candle-gated runtime: MQL5 delivers OnTick(), but this EA does no
   // research work and no CopyRates append until a new candle has opened
   // and the previous candle is closed. This keeps the lab candle-based,
   // not tick-based.
   if(!HasNewClosedCandle())
      return;

   if(DAL_M0001_USE_LIVE_BAR_STREAM)
   {
      bool appended = UpdateLiveBarStream();
      if(appended && InpRuntimeVisuals)
         RunM0001FromBars(g_live_bars, g_live_bars_count, "live_stream_new_candle");
      return;
   }

   if(InpRuntimeVisuals)
      RunM0001();
}

void OnChartEvent(
   const int id,
   const long &lparam,
   const double &dparam,
   const string &sparam
)
{
   if(!InpRuntimeVisuals)
      return;

   if(!DAL_M0001_REDRAW_ON_CHART_CHANGE)
      return;

   if(id == CHARTEVENT_CHART_CHANGE)
      RunM0001();
}

void OnTimer()
{
   // Timer is disabled by default. If it is enabled later, keep it under
   // the same candle gate so it cannot re-run research logic intra-candle.
   if(!HasNewClosedCandle())
      return;

   if(DAL_M0001_USE_LIVE_BAR_STREAM)
   {
      bool appended = UpdateLiveBarStream();
      if(appended && InpRuntimeVisuals)
         RunM0001FromBars(g_live_bars, g_live_bars_count, "live_stream_timer_new_candle");
      return;
   }

   if(InpRuntimeVisuals)
      RunM0001();
}
