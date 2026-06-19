//+------------------------------------------------------------------+
//| Decision Alpha Lab — M0003 Continuation Inertia Memory |
//| Hypothesis 3: continuation inertia, memory, and clustered volatility after node-zone exit.   |
//+------------------------------------------------------------------+
#property strict
#property version   "1.04"
#property description "M0003 tests continuation inertia, memory, and cluster-stress using exact M0001/M0002 branch modules"

#include <DecisionAlphaLab/Market/DAL_Bars.mqh>
#include <DecisionAlphaLab/Market/DAL_LiveBarStream.mqh>
#include <DecisionAlphaLab/StructuralNodes/DAL_StructuralNodeEngine.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Config.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Engine.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001RtvNullComparison.mqh>
#include <DecisionAlphaLab/M0003/DAL_M0003Reports.mqh>

input string InpSymbol = "";                   // empty = chart symbol
input ENUM_TIMEFRAMES InpTimeframe = PERIOD_CURRENT;
input int InpBars = 0;                          // 0 = no cap
input int InpWarmupHistoricalBars = 5000;       // pre-test closed bars used only to seed old nodes

input int InpL = 5;
input double InpZoneRatio = 0.90;
input int InpExitGap = 6;
input ENUM_DALM0001ConsumeMode InpConsumeMode = DAL_M0001_CONSUME_BY_HUNT;

// H0003 reuses the M0001 event RTV window and the M0002 branch classifier.
// The old post-outcome fixed-window diagnostic caused misleading branch rawMean/rawMed values
// and is intentionally not exposed in this production research EA.
input int InpOutcomeCandleOffsetAfterExit = 0;  // 0 = candle that completes exit-gap; 1 = next closed candle

input int InpRandomSamplesPerEvent = 20;
input int InpBootstrapIterations = 300;
input int InpPermutationIterations = 500;
input int InpValidationSplits = 5;
input int InpBrokerUtcOffsetHours = 0;
input int InpRegimeLookbackBars = 100;
input bool InpPrintGroupSessionRegime = true;

input bool InpRunH3StressSuite = true;
input int InpHardRandomCandidates = 80;
input int InpPlaceboShiftBars = 50;
input int InpNonOverlapGapBars = 0;
input int InpBlockBootstrapIterations = 300;
input int InpBlockBootstrapBlockPairs = 25;
input int InpHorizonBars1 = 5;
input int InpHorizonBars2 = 10;
input int InpHorizonBars3 = 20;
input int InpHorizonBars4 = 50;

input int InpClusterStressIterations = 200;  // deterministic iid-shuffle stress for lag and high-run clustering
input int InpClusterBlockSize = 25;          // contiguous branch-event block size for cluster robustness
input double InpHighRunPercentile = 0.75;    // high-volatility run threshold inside each branch

#define DAL_M0002_USE_LIVE_BAR_STREAM true
#define DAL_M0002_START_FROM_NEXT_CLOSED_BAR true
#define DAL_M0002_CLOSED_BARS_ONLY true
#define DAL_M0002_TIMER_MS 0
#define DAL_M0002_MAX_EVENTS 0
#define DAL_M0002_MIN_RTV 0.0

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

void BuildM0001Config(DALM0001Config &config)
{
   DAL_M0001DefaultConfig(config);
   config.L = InpL;
   config.zone_ratio = InpZoneRatio;
   config.exit_gap = InpExitGap;
   config.consume_mode = InpConsumeMode;
   config.consume_on_touch = false;
   if(config.consume_on_touch)
      config.consume_mode = DAL_M0001_CONSUME_BY_TOUCH;
   config.max_events = DAL_M0002_MAX_EVENTS;
   config.min_rtv = DAL_M0002_MIN_RTV;
}

void BuildM0002Config(DALM0002Config &config)
{
   DAL_M0002DefaultConfig(config);
   // Hard lock H0003 to EVENT_RTV. Branching is only a label over the completed M0001 exit event;
   // it must not change the measured volatility window.
   config.measure_mode = DAL_M0002_MEASURE_EVENT_RTV;
   config.outcome_candle_offset_after_exit = InpOutcomeCandleOffsetAfterExit;
   config.post_outcome_sample_bars = 0;
   config.use_event_length_for_sample = false;
   config.random_samples_per_event = InpRandomSamplesPerEvent;
   config.bootstrap_iterations = InpBootstrapIterations;
   config.permutation_iterations = InpPermutationIterations;
   config.validation_splits = InpValidationSplits;
   config.broker_utc_offset_hours = InpBrokerUtcOffsetHours;
   config.regime_lookback_bars = InpRegimeLookbackBars;
   config.print_group_session_regime = InpPrintGroupSessionRegime;
   config.run_stress_suite = InpRunH3StressSuite;
   config.hard_random_candidates = InpHardRandomCandidates;
   config.placebo_shift_bars = InpPlaceboShiftBars;
   config.nonoverlap_gap_bars = InpNonOverlapGapBars;
   config.block_bootstrap_iterations = InpBlockBootstrapIterations;
   config.block_bootstrap_block_pairs = InpBlockBootstrapBlockPairs;
   config.horizon_bars_1 = InpHorizonBars1;
   config.horizon_bars_2 = InpHorizonBars2;
   config.horizon_bars_3 = InpHorizonBars3;
   config.horizon_bars_4 = InpHorizonBars4;
   config.consume_mode = InpConsumeMode;
   config.consume_on_touch = (InpConsumeMode == DAL_M0001_CONSUME_BY_TOUCH);

   if(config.outcome_candle_offset_after_exit < 0)
      config.outcome_candle_offset_after_exit = 0;
   if(config.random_samples_per_event < 1)
      config.random_samples_per_event = 1;
   if(config.bootstrap_iterations < 0)
      config.bootstrap_iterations = 0;
   if(config.permutation_iterations < 0)
      config.permutation_iterations = 0;
   if(config.validation_splits < 1)
      config.validation_splits = 1;
   if(config.regime_lookback_bars < 1)
      config.regime_lookback_bars = 1;
   if(config.hard_random_candidates < 1)
      config.hard_random_candidates = 1;
   if(config.placebo_shift_bars < 1)
      config.placebo_shift_bars = 1;
   if(config.nonoverlap_gap_bars < 0)
      config.nonoverlap_gap_bars = 0;
   if(config.block_bootstrap_iterations < 0)
      config.block_bootstrap_iterations = 0;
   if(config.block_bootstrap_block_pairs < 1)
      config.block_bootstrap_block_pairs = 1;
   if(config.horizon_bars_1 < 1) config.horizon_bars_1 = 1;
   if(config.horizon_bars_2 < 1) config.horizon_bars_2 = 1;
   if(config.horizon_bars_3 < 1) config.horizon_bars_3 = 1;
   if(config.horizon_bars_4 < 1) config.horizon_bars_4 = 1;
}


void BuildM0003Config(DALM0003Config &config)
{
   config.cluster_stress_iterations = InpClusterStressIterations;
   config.cluster_block_size = InpClusterBlockSize;
   config.high_run_percentile = InpHighRunPercentile;

   if(config.cluster_stress_iterations < 0)
      config.cluster_stress_iterations = 0;
   if(config.cluster_block_size < 2)
      config.cluster_block_size = 2;
   if(config.high_run_percentile <= 0.50)
      config.high_run_percentile = 0.75;
   if(config.high_run_percentile >= 0.99)
      config.high_run_percentile = 0.99;
}

void UpdateRuntimeComment(const int bars_count, const string source_mode)
{
   string start_text = g_analysis_start_time > 0 ? TimeToString(g_analysis_start_time, TIME_DATE | TIME_MINUTES) : "pending";

   Comment(
      "Decision Alpha Lab | M0003 Continuation Inertia Memory\n",
      "source=", source_mode,
      "  symbol=", LabSymbol(),
      "  tf=", EnumToString(LabTimeframe()), "\n",
      "bars=", bars_count,
      "  warmup_bars=", InpWarmupHistoricalBars,
      "  analysis_start=", start_text, "\n",
      "measureMode=EVENT_RTV_LOCKED",
      "  outcomeCandleOffsetAfterExit=", InpOutcomeCandleOffsetAfterExit, "\n",
      "sampleWindow=M0001 event RTV; branch label does not change measured window\n",
      "consumeMode=", DAL_M0001ConsumeModeToString(InpConsumeMode),
      "  touchCycle=", (InpConsumeMode == DAL_M0001_CONSUME_BY_HUNT ? "touch_exit_can_close_either_side_then_recompute_if_not_hunted" : "touch_exit_can_close_either_side_consumes_node"), "\n",
      "branch=LOW above node => reversal, below => continuation; HIGH inverse",
      "  randomEngine=", DAL_M0001RandomEngineSignature(),
      "  randomK=", InpRandomSamplesPerEvent,
      "  utcOffset=", InpBrokerUtcOffsetHours, "\n",
      "clusterStressIters=", InpClusterStressIterations,
      "  clusterBlockSize=", InpClusterBlockSize,
      "  highRunPct=", DoubleToString(InpHighRunPercentile, 2), "\n",
      "final split inertia/memory/cluster stress report prints once on deinit"
   );
}

void ComputeM0002M0001LifecycleEvents(
   const DALBar &bars[],
   const int bars_count,
   DALLRuleNode &nodes[],
   int &nodes_count,
   DALM0001Event &events[],
   int &events_count
)
{
   ArrayResize(nodes, 0);
   ArrayResize(events, 0);
   nodes_count = 0;
   events_count = 0;

   if(bars_count <= 0)
      return;

   DALM0001Config config;
   BuildM0001Config(config);

   nodes_count = DAL_DetectConfirmedStructuralNodes(bars, bars_count, config.L, nodes);

   // H0003 must use the exact H0001/M0001 event lifecycle through M0002 branch samples.
   // The consume criterion is the same input as M0001:
   // - CONSUME_BY_HUNT: a confirmed touch/revisit does NOT consume the node;
   //   the node remains alive and the next territory cycle is recomputed after the exit candle.
   // - CONSUME_BY_TOUCH: the confirmed touch consumes the node and no further cycle is built.
   // Reversal/continuation is only a branch label assigned to each valid M0001
   // touch-confirmed completed-exit event at its exit candle.
   events_count = DAL_M0001ComputeEvents(bars, bars_count, nodes, nodes_count, config, events);
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
      DAL_WarmupClosedBarsByShift(LabSymbol(), LabTimeframe(), warmup_bars, 0, g_live_bars, g_live_bars_count);
      if(g_live_bars_count > 0)
         g_last_closed_stream_bar_time = g_live_bars[g_live_bars_count - 1].time;
   }
   else if(DAL_M0002_START_FROM_NEXT_CLOSED_BAR)
   {
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

void PrintFinalReportsFromBars(
   const DALBar &bars[],
   const int bars_count,
   const string source_mode
)
{
   if(bars_count <= 0)
      return;

   DALLRuleNode nodes[];
   DALM0001Event events[];
   int nodes_count = 0;
   int events_count = 0;
   ComputeM0002M0001LifecycleEvents(bars, bars_count, nodes, nodes_count, events, events_count);

   DALM0002Config h2_config;
   BuildM0002Config(h2_config);

   DALM0003Config h3_config;
   BuildM0003Config(h3_config);

   Print(
      "DAL_M0003_BUILD_SANITY *** symbol=", LabSymbol(),
      "*tf=", EnumToString(LabTimeframe()),
      "*source=", source_mode,
      "*build=1.04",
      "*measureMode=EVENT_RTV_LOCKED*stressSuite=H3_FULL",
      "*sampleWindow=m0001EventRtv",
      "*consumeMode=", DAL_M0001ConsumeModeToString(InpConsumeMode),
      "*touchCycle=", (InpConsumeMode == DAL_M0001_CONSUME_BY_HUNT ? "touch_exit_can_close_either_side_recompute_if_not_hunted" : "touch_exit_can_close_either_side_consumes_node"),
      "*clusterStressIters=", InpClusterStressIterations,
      "*clusterBlockSize=", InpClusterBlockSize,
      "*highRunPercentile=", DoubleToString(InpHighRunPercentile, 2),
      "*L=", InpL,
      "*zoneRatio=", DoubleToString(InpZoneRatio, 4),
      "*exitGap=", InpExitGap,
      "*warmupBars=", InpWarmupHistoricalBars,
      "*randomK=", InpRandomSamplesPerEvent,
      "*eventUniverseGuard=exact_M0001_compute_events_then_M0002_branch_collect",
      "*oldPostOutcomeFieldsForbidden=sampleBars_sampleStarts_afterOutcomeCandle",
      " *** if_this_line_is_missing_you_are_running_an_old_EX5_or_wrong_file"
   );

   Print(
      "DAL_M0003_BASE_STATE *** symbol=", LabSymbol(),
      "*tf=", EnumToString(LabTimeframe()),
      "*source=", source_mode,
      "*bars=", bars_count,
      "*nodes=", nodes_count,
      "*m0001Events=", events_count,
      "*analysisStart=", DAL_M0001AnalysisStartText(g_analysis_start_time),
      " *** logic=M0003_uses_exact_M0001_M0002_branch_samples_for_inertia_memory_cluster*build=1.04*measureMode=EVENT_RTV_LOCKED*stressSuite=H3_FULL*sampleWindow=m0001EventRtv*consumeMode=", DAL_M0001ConsumeModeToString(InpConsumeMode),
      "*touchCycle=", (InpConsumeMode == DAL_M0001_CONSUME_BY_HUNT ? "touch_exit_can_close_either_side_recompute_if_not_hunted" : "touch_exit_can_close_either_side_consumes_node"),
      "*clusterStressIters=", InpClusterStressIterations,
      "*clusterBlockSize=", InpClusterBlockSize,
      "*highRunPercentile=", DoubleToString(InpHighRunPercentile, 2),
      "*inputFingerprint=L", InpL,
      "_zr", DoubleToString(InpZoneRatio, 4),
      "_eg", InpExitGap,
      "_warm", InpWarmupHistoricalBars,
      "_k", InpRandomSamplesPerEvent
   );

   DAL_M0003PrintFinalReports(
      events,
      events_count,
      bars,
      bars_count,
      LabSymbol(),
      EnumToString(LabTimeframe()),
      source_mode,
      g_analysis_start_time,
      h2_config,
      h3_config
   );
}

void PrintFinalReports()
{
   if(DAL_M0002_USE_LIVE_BAR_STREAM)
   {
      PrintFinalReportsFromBars(g_live_bars, g_live_bars_count, "final_live_stream");
      return;
   }

   DALBar bars[];
   int bars_count = DAL_LoadBarsChronological(LabSymbol(), LabTimeframe(), InpBars, DAL_M0002_CLOSED_BARS_ONLY, bars);
   PrintFinalReportsFromBars(bars, bars_count, "final_copyrates");
}

int OnInit()
{
   InitializeCandleClock();

   if(DAL_M0002_USE_LIVE_BAR_STREAM)
   {
      InitializeLiveBarStream();
      UpdateRuntimeComment(g_live_bars_count, "fast_final_only_warmup_ready");
   }
   else
   {
      UpdateRuntimeComment(0, "fast_final_only_copyrates_ready");
   }

   if(DAL_M0002_TIMER_MS > 0)
      EventSetMillisecondTimer(DAL_M0002_TIMER_MS);

   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   PrintFinalReports();
   EventKillTimer();
}

void OnTick()
{
   if(!HasNewClosedCandle())
      return;

   if(DAL_M0002_USE_LIVE_BAR_STREAM)
   {
      bool appended = UpdateLiveBarStream();
      if(appended)
         UpdateRuntimeComment(g_live_bars_count, "live_stream_new_candle");
      return;
   }
}

void OnTimer()
{
   if(!HasNewClosedCandle())
      return;

   if(DAL_M0002_USE_LIVE_BAR_STREAM)
   {
      bool appended = UpdateLiveBarStream();
      if(appended)
         UpdateRuntimeComment(g_live_bars_count, "live_stream_timer_new_candle");
      return;
   }
}
