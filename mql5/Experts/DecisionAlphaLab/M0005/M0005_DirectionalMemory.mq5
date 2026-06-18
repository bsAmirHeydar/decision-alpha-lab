//+------------------------------------------------------------------+
//| Decision Alpha Lab — M0005 Directional Memory                     |
//| Hypothesis 5: structural regimes create path/direction memory.     |
//+------------------------------------------------------------------+
#property strict
#property version   "1.02"
#property description "M0005 tests structural directional memory with MFE/MAE until structural/path exit"

#include <DecisionAlphaLab/Market/DAL_Bars.mqh>
#include <DecisionAlphaLab/Market/DAL_LiveBarStream.mqh>
#include <DecisionAlphaLab/StructuralNodes/DAL_StructuralNodeEngine.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Config.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Engine.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001RtvNullComparison.mqh>
#include <DecisionAlphaLab/M0005/DAL_M0005Reports.mqh>

input string InpSymbol = "";
input ENUM_TIMEFRAMES InpTimeframe = PERIOD_CURRENT;
input int InpBars = 0;
input int InpWarmupHistoricalBars = 5000;

input int InpL = 5;
input double InpZoneRatio = 0.90;
input int InpExitGap = 6;
input ENUM_DALM0001ConsumeMode InpConsumeMode = DAL_M0001_CONSUME_BY_HUNT;
input int InpOutcomeCandleOffsetAfterExit = 0;

input ENUM_DALM0005RegimeSource InpH5RegimeSource = DAL_M0005_REGIME_LAST_ONLY;
input int InpH5ContextLookback = 10;
input double InpH5ContextEwmaAlpha = 0.35;
input double InpH5ContextStrongThreshold = 0.60;
input bool InpH5BreakUsesClose = true;
input ENUM_DALM0005ReversalStopMode InpH5ReversalStopMode = DAL_M0005_REV_STOP_ZONE_EDGE;
input bool InpH5ReversalStopUsesWick = true;
input bool InpH5ReversalSameBarStopFirst = true;
input double InpH5ReversalHuntLockZoneMultiple = 0.5;
input int InpH5MaxPathBars = 1000;
input int InpH5MaxPathEvents = 50;
input double InpH5ContinuationSuccessZoneMultiple = 1.0;
input double InpH5FollowZoneMultiple1 = 0.5;
input double InpH5FollowZoneMultiple2 = 1.0;
input double InpH5FollowZoneMultiple3 = 1.5;
input double InpH5FollowZoneMultiple4 = 2.0;
input int InpH5RandomSamplesPerPath = 20;
input int InpH5StressIterations = 500;
input int InpH5BlockSize = 50;

input int InpRandomSamplesPerEvent = 20;
input int InpBootstrapIterations = 300;
input int InpPermutationIterations = 500;
input int InpValidationSplits = 5;
input int InpBrokerUtcOffsetHours = 0;
input int InpRegimeLookbackBars = 100;
input bool InpPrintGroupSessionRegime = true;
input bool InpRunH5BaseStressSuite = true;
input int InpHardRandomCandidates = 80;
input int InpPlaceboShiftBars = 50;
input int InpNonOverlapGapBars = 0;
input int InpBlockBootstrapIterations = 300;
input int InpBlockBootstrapBlockPairs = 25;
input int InpHorizonBars1 = 5;
input int InpHorizonBars2 = 10;
input int InpHorizonBars3 = 20;
input int InpHorizonBars4 = 50;

#define DAL_M0005_USE_LIVE_BAR_STREAM true
#define DAL_M0005_START_FROM_NEXT_CLOSED_BAR true
#define DAL_M0005_CLOSED_BARS_ONLY true
#define DAL_M0005_TIMER_MS 0
#define DAL_M0005_MAX_EVENTS 0
#define DAL_M0005_MIN_RTV 0.0
#define DAL_M0005_BUILD "1.02"

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
   config.max_events = DAL_M0005_MAX_EVENTS;
   config.min_rtv = DAL_M0005_MIN_RTV;
}

void BuildM0002Config(DALM0002Config &config)
{
   DAL_M0002DefaultConfig(config);
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
   config.run_stress_suite = InpRunH5BaseStressSuite;
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

   if(config.outcome_candle_offset_after_exit < 0) config.outcome_candle_offset_after_exit = 0;
   if(config.random_samples_per_event < 1) config.random_samples_per_event = 1;
   if(config.bootstrap_iterations < 0) config.bootstrap_iterations = 0;
   if(config.permutation_iterations < 0) config.permutation_iterations = 0;
   if(config.validation_splits < 1) config.validation_splits = 1;
   if(config.regime_lookback_bars < 1) config.regime_lookback_bars = 1;
   if(config.hard_random_candidates < 1) config.hard_random_candidates = 1;
   if(config.placebo_shift_bars < 1) config.placebo_shift_bars = 1;
   if(config.nonoverlap_gap_bars < 0) config.nonoverlap_gap_bars = 0;
   if(config.block_bootstrap_iterations < 0) config.block_bootstrap_iterations = 0;
   if(config.block_bootstrap_block_pairs < 1) config.block_bootstrap_block_pairs = 1;
   if(config.horizon_bars_1 < 1) config.horizon_bars_1 = 1;
   if(config.horizon_bars_2 < 1) config.horizon_bars_2 = 1;
   if(config.horizon_bars_3 < 1) config.horizon_bars_3 = 1;
   if(config.horizon_bars_4 < 1) config.horizon_bars_4 = 1;
}

void BuildM0005Config(DALM0005Config &config)
{
   config.regime_source = InpH5RegimeSource;
   config.context_lookback = InpH5ContextLookback;
   config.context_ewma_alpha = InpH5ContextEwmaAlpha;
   config.context_strong_threshold = InpH5ContextStrongThreshold;
   config.break_uses_close = InpH5BreakUsesClose;
   config.reversal_stop_mode = InpH5ReversalStopMode;
   config.reversal_stop_uses_wick = InpH5ReversalStopUsesWick;
   config.reversal_same_bar_stop_first = InpH5ReversalSameBarStopFirst;
   config.reversal_hunt_lock_zone_multiple = InpH5ReversalHuntLockZoneMultiple;
   config.max_path_bars = InpH5MaxPathBars;
   config.max_path_events = InpH5MaxPathEvents;
   config.continuation_success_zone_multiple = InpH5ContinuationSuccessZoneMultiple;
   config.follow_zone_mult_1 = InpH5FollowZoneMultiple1;
   config.follow_zone_mult_2 = InpH5FollowZoneMultiple2;
   config.follow_zone_mult_3 = InpH5FollowZoneMultiple3;
   config.follow_zone_mult_4 = InpH5FollowZoneMultiple4;
   config.random_samples_per_path = InpH5RandomSamplesPerPath;
   config.stress_iterations = InpH5StressIterations;
   config.block_size = InpH5BlockSize;

   if(config.context_lookback < 1) config.context_lookback = 1;
   if(config.context_ewma_alpha <= 0.0) config.context_ewma_alpha = 0.35;
   if(config.context_ewma_alpha >= 1.0) config.context_ewma_alpha = 0.99;
   if(config.context_strong_threshold < 0.51) config.context_strong_threshold = 0.51;
   if(config.context_strong_threshold > 0.95) config.context_strong_threshold = 0.95;
   if(config.reversal_hunt_lock_zone_multiple <= 0.0) config.reversal_hunt_lock_zone_multiple = 0.5;
   if(config.reversal_hunt_lock_zone_multiple > 5.0) config.reversal_hunt_lock_zone_multiple = 5.0;
   if(config.max_path_bars < 0) config.max_path_bars = 0;
   if(config.max_path_events < 1) config.max_path_events = 1;
   if(config.continuation_success_zone_multiple <= 0.0) config.continuation_success_zone_multiple = 1.0;
   if(config.follow_zone_mult_1 <= 0.0) config.follow_zone_mult_1 = 0.5;
   if(config.follow_zone_mult_2 <= 0.0) config.follow_zone_mult_2 = 1.0;
   if(config.follow_zone_mult_3 <= 0.0) config.follow_zone_mult_3 = 1.5;
   if(config.follow_zone_mult_4 <= 0.0) config.follow_zone_mult_4 = 2.0;
   if(config.random_samples_per_path < 1) config.random_samples_per_path = 1;
   if(config.stress_iterations < 0) config.stress_iterations = 0;
   if(config.block_size < 5) config.block_size = 5;
}

void UpdateRuntimeComment(const int bars_count, const string source_mode)
{
   string start_text = g_analysis_start_time > 0 ? TimeToString(g_analysis_start_time, TIME_DATE | TIME_MINUTES) : "pending";

   Comment(
      "Decision Alpha Lab | M0005 Directional Memory\n",
      "source=", source_mode,
      "  symbol=", LabSymbol(),
      "  tf=", EnumToString(LabTimeframe()), "\n",
      "bars=", bars_count,
      "  warmup_bars=", InpWarmupHistoricalBars,
      "  analysis_start=", start_text, "\n",
      "regimeSource=", DAL_M0005RegimeSourceToString(InpH5RegimeSource),
      "  contextK=", InpH5ContextLookback,
      "  ewmaAlpha=", DoubleToString(InpH5ContextEwmaAlpha, 2),
      "  threshold=", DoubleToString(InpH5ContextStrongThreshold, 2), "\n",
      "reversal: next opposite structural zone target; default stop=zone edge, adaptive hunt stop optional\n",
      "continuation: zone break until regime change; realized/floating R and MFE/MAE stop at path exit"
   );
}

void ComputeM0001LifecycleEvents(
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
   else if(DAL_M0005_START_FROM_NEXT_CLOSED_BAR)
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

void PrintFinalReportsFromBars(const DALBar &bars[], const int bars_count, const string source_mode)
{
   if(bars_count <= 0)
      return;

   DALLRuleNode nodes[];
   DALM0001Event events[];
   int nodes_count = 0;
   int events_count = 0;
   ComputeM0001LifecycleEvents(bars, bars_count, nodes, nodes_count, events, events_count);

   DALM0002Config h2_config;
   BuildM0002Config(h2_config);

   DALM0005Config h5_config;
   BuildM0005Config(h5_config);

   Print(
      "DAL_M0005_BUILD_SANITY *** symbol=", LabSymbol(),
      "*tf=", EnumToString(LabTimeframe()),
      "*source=", source_mode,
      "*build=", DAL_M0005_BUILD,
      "*hypothesis=H0005_DIRECTIONAL_MEMORY",
      "*measureMode=EVENT_RTV_LOCKED",
      "*sampleWindow=m0001EventRtv",
      "*regimeSource=", DAL_M0005RegimeSourceToString(h5_config.regime_source),
      "*regimeSourceDefault=LAST_ONLY",
      "*reversalEntry=next_structural_zone_touch",
      "*reversalExit=opposite_zone_target_or_structural_stop",
      "*continuationEntry=last_zone_break_not_only_hunt",
      "*continuationExit=regime_change",
      "*reversalStopMode=", DAL_M0005ReversalStopModeToString(h5_config.reversal_stop_mode),
      "*reversalStopRule=input_controlled_default_zone_edge_no_future_hunt_lookahead",
      "*reversalStopUsesWick=", DAL_BoolToString(h5_config.reversal_stop_uses_wick),
      "*reversalSameBarStopFirst=", DAL_BoolToString(h5_config.reversal_same_bar_stop_first),
      "*reversalHuntLockZoneMultiple=", DoubleToString(h5_config.reversal_hunt_lock_zone_multiple, 4),
      "*mfeMaeStopGuard=stop_at_path_exit",
      "*rMetrics=realized_R_floating_R_winrate_profit_factor",
      "*randomDesign=matched_entry_same_duration_same_direction_same_actual_R_scale",
      "*contextK=", h5_config.context_lookback,
      "*contextEwmaAlpha=", DoubleToString(h5_config.context_ewma_alpha, 4),
      "*contextStrongThreshold=", DoubleToString(h5_config.context_strong_threshold, 4),
      "*continuationSuccessZoneMultiple=", DoubleToString(h5_config.continuation_success_zone_multiple, 4),
      "*breakUsesClose=", DAL_BoolToString(h5_config.break_uses_close),
      "*maxPathBars=", h5_config.max_path_bars,
      "*maxPathEvents=", h5_config.max_path_events,
      "*randomSamplesPerPath=", h5_config.random_samples_per_path,
      "*L=", InpL,
      "*zoneRatio=", DoubleToString(InpZoneRatio, 4),
      "*exitGap=", InpExitGap,
      "*eventUniverseGuard=exact_M0001_compute_events_then_M0002_branch_collect_then_M0005_path_test",
      " *** if_this_line_is_missing_you_are_running_an_old_EX5_or_wrong_file"
   );

   Print(
      "DAL_M0005_BASE_STATE *** symbol=", LabSymbol(),
      "*tf=", EnumToString(LabTimeframe()),
      "*source=", source_mode,
      "*bars=", bars_count,
      "*nodes=", nodes_count,
      "*m0001Events=", events_count,
      "*analysisStart=", DAL_M0001AnalysisStartText(g_analysis_start_time),
      " *** logic=M0005_structural_directional_memory_no_fixed_time_window*build=", DAL_M0005_BUILD,
      "*xAxis=structural_nodes_and_zones_for_reversal_destinations",
      "*yAxis=market_state_regime_for_continuation_exit",
      "*consumeMode=", DAL_M0001ConsumeModeToString(InpConsumeMode),
      "*touchCycle=", (InpConsumeMode == DAL_M0001_CONSUME_BY_HUNT ? "touch_exit_can_close_either_side_recompute_if_not_hunted" : "touch_exit_can_close_either_side_consumes_node")
   );

   DAL_M0005PrintFinalReports(
      events,
      events_count,
      bars,
      bars_count,
      LabSymbol(),
      EnumToString(LabTimeframe()),
      source_mode,
      g_analysis_start_time,
      h2_config,
      h5_config
   );
}

void PrintFinalReports()
{
   if(DAL_M0005_USE_LIVE_BAR_STREAM)
   {
      PrintFinalReportsFromBars(g_live_bars, g_live_bars_count, "final_live_stream");
      return;
   }

   DALBar bars[];
   int bars_count = DAL_LoadBarsChronological(LabSymbol(), LabTimeframe(), InpBars, DAL_M0005_CLOSED_BARS_ONLY, bars);
   PrintFinalReportsFromBars(bars, bars_count, "final_copyrates");
}

int OnInit()
{
   InitializeCandleClock();

   if(DAL_M0005_USE_LIVE_BAR_STREAM)
   {
      InitializeLiveBarStream();
      UpdateRuntimeComment(g_live_bars_count, "directional_memory_warmup_ready");
   }
   else
   {
      UpdateRuntimeComment(0, "directional_memory_copyrates_ready");
   }

   if(DAL_M0005_TIMER_MS > 0)
      EventSetMillisecondTimer(DAL_M0005_TIMER_MS);

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

   if(DAL_M0005_USE_LIVE_BAR_STREAM)
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

   if(DAL_M0005_USE_LIVE_BAR_STREAM)
   {
      bool appended = UpdateLiveBarStream();
      if(appended)
         UpdateRuntimeComment(g_live_bars_count, "live_stream_timer_new_candle");
      return;
   }
}
