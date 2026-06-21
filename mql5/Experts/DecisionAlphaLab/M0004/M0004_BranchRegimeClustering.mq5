//+------------------------------------------------------------------+
//| Decision Alpha Lab — M0004 Branch Regime Clustering               |
//| Hypothesis 4: reversal/continuation branch labels form regimes.    |
//+------------------------------------------------------------------+
#property strict
#property version   "1.12"
#property description "M0004 fast atomic no-sample report with stress toggles and human-context diagnostics"

#include <DecisionAlphaLab/Market/DAL_Bars.mqh>
#include <DecisionAlphaLab/Market/DAL_LiveBarStream.mqh>
#include <DecisionAlphaLab/StructuralNodes/DAL_StructuralNodeEngine.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Config.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Engine.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001RtvNullComparison.mqh>
#include <DecisionAlphaLab/M0004/DAL_M0004Reports.mqh>
#include <DecisionAlphaLab/M0004/DAL_M0004AtomicNoSample.mqh>

input string InpSymbol = "";                   // empty = chart symbol
input ENUM_TIMEFRAMES InpTimeframe = PERIOD_CURRENT;
input int InpBars = 0;                          // 0 = no cap
input int InpWarmupHistoricalBars = 5000;       // pre-test closed bars used only to seed old nodes
input bool InpUseAtomicNoSampleMainReport = true;  // true = official H4 no-sample main report
input bool InpPrintLegacySampleReport = false;     // off by default: old M0002 sample sequence only for comparison
// 0 = FAST_RAW_EVENT_BATCH (official/fast), 1 = STRICT_PREFIX_REPLAY (small debug only).
// Kept as int on purpose: MetaEditor sometimes compiles the EA before the terminal Include tree is synced,
// and enum-typed inputs then fail with "declaration without type". The actual config still uses the enum internally.
input int InpAtomicReportMode = 0;
input int InpAtomicPermutationIterations = 100; // keep main report fast; set higher only for final publication

input bool InpAtomicStressTransitionPermutation = true;
input bool InpAtomicStressRunShuffle = true;
input bool InpAtomicStressBlockConcentration = true;
input bool InpAtomicStressCircularShift = true;
input bool InpAtomicStressLocalBlockShuffle = true;

input bool InpAtomicPrintExtendedReport = true; // fast extra lag/block/run diagnostics, still no samples
input bool InpAtomicPrintDeepReport = true; // information, run tails, batch intensity over atomic batches
input bool InpAtomicPrintH6OptionalityReport = false; // H6 moved to M0006; keep opt-in only
input bool InpAtomicPrintHumanContextReport = true; // rolling / EWMA human-eye context over known-time batches
input bool InpAtomicStressContextShuffle = false; // heavier context shuffle diagnostics
input bool InpAtomicStressH6Optionality = false; // H6 moved to M0006; keep opt-in only
input int InpH6HorizonBarsFast = 5;
input int InpH6HorizonBarsMain = 20;
input int InpH6HorizonBarsSlow = 50;
input int InpH6AtrPeriod = 14;
input double InpH6TailAtr1 = 2.0;
input double InpH6TailAtr2 = 4.0;
input double InpH6TailAtr3 = 8.0;
input int InpAtomicContextLookbackFast = 5;
input int InpAtomicContextLookbackMain = 10;
input int InpAtomicContextLookbackSlow = 20;
input double InpAtomicContextEwmaAlpha = 0.3500;
input double InpAtomicContextStrongThreshold = 0.6000;
input int InpAtomicCircularMinShiftBatches = 50;
input int InpAtomicLocalBlockShuffleSize = 50;
input int InpAtomicBlockSizeFast = 25;
input int InpAtomicBlockSizeMain = 50;
input int InpAtomicBlockSizeSlow = 200;
input bool InpAtomicWriteCsv = false;
input string InpAtomicCsvFileName = "M0004_Atomic_NoSample_Regime.csv";

input int InpL = 5;
input double InpZoneRatio = 0.90;
input int InpExitGap = 6;
input ENUM_DALM0001ConsumeMode InpConsumeMode = DAL_M0001_CONSUME_BY_HUNT;

// H0004 is label-regime research. It reuses the exact M0001 event lifecycle
// and the exact M0002 reversal/continuation classifier. The measured event RTV
// window remains locked to M0001; H0004 studies only the chronological sequence
// of branch labels after confirmed exit.
input int InpOutcomeCandleOffsetAfterExit = 0;  // 0 = candle that completes exit-gap; 1 = next closed candle

input int InpRandomSamplesPerEvent = 20;
input int InpBootstrapIterations = 300;
input int InpPermutationIterations = 500;
input int InpValidationSplits = 5;
input int InpBrokerUtcOffsetHours = 0;
input int InpRegimeLookbackBars = 100;
input bool InpPrintGroupSessionRegime = true;

input bool InpRunH4StressSuite = true;
input int InpHardRandomCandidates = 80;
input int InpPlaceboShiftBars = 50;
input int InpNonOverlapGapBars = 0;
input int InpBlockBootstrapIterations = 300;
input int InpBlockBootstrapBlockPairs = 25;
input int InpHorizonBars1 = 5;
input int InpHorizonBars2 = 10;
input int InpHorizonBars3 = 20;
input int InpHorizonBars4 = 50;

input int InpBranchStressIterations = 500;      // label-permutation / run-shuffle stress
input int InpBranchBlockSize = 50;              // contiguous branch-event blocks for concentration stress
input int InpBranchPlaceboLagEvents = 50;       // far-lag placebo correlation over branch labels
input int InpRegimeBlockSizeFast = 25;          // small contiguous event-block profile
input int InpRegimeBlockSizeSlow = 200;         // large contiguous event-block profile
input int InpCircularMinShiftEvents = 50;       // minimum shift for circular far-lag null
input int InpLocalBlockShuffleSize = 50;        // block-order shuffle null preserving within-block runs
input int InpContextLookbackFast = 5;           // short contextual branch-memory window
input int InpContextLookbackMain = 10;          // human-eye contextual branch-memory window
input int InpContextLookbackSlow = 20;          // slower contextual branch-memory window
input double InpContextEwmaAlpha = 0.35;        // recency weight for human-eye EWMA context
input double InpContextStrongThreshold = 0.60;  // dominant context threshold: >= continuation, <= reversal

#define DAL_M0004_USE_LIVE_BAR_STREAM true
#define DAL_M0004_START_FROM_NEXT_CLOSED_BAR true
#define DAL_M0004_CLOSED_BARS_ONLY true
#define DAL_M0004_TIMER_MS 0
#define DAL_M0004_MAX_EVENTS 0
#define DAL_M0004_MIN_RTV 0.0

#define DAL_M0004_BUILD "1.12"

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
   config.max_events = DAL_M0004_MAX_EVENTS;
   config.min_rtv = DAL_M0004_MIN_RTV;
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
   config.run_stress_suite = InpRunH4StressSuite;
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

void BuildM0004Config(DALM0004Config &config)
{
   config.stress_iterations = InpBranchStressIterations;
   config.block_size = InpBranchBlockSize;
   config.placebo_lag_events = InpBranchPlaceboLagEvents;
   config.regime_block_size_fast = InpRegimeBlockSizeFast;
   config.regime_block_size_slow = InpRegimeBlockSizeSlow;
   config.circular_min_shift_events = InpCircularMinShiftEvents;
   config.local_block_shuffle_size = InpLocalBlockShuffleSize;
   config.context_k_fast = InpContextLookbackFast;
   config.context_k_main = InpContextLookbackMain;
   config.context_k_slow = InpContextLookbackSlow;
   config.context_ewma_alpha = InpContextEwmaAlpha;
   config.context_strong_threshold = InpContextStrongThreshold;

   if(config.stress_iterations < 0) config.stress_iterations = 0;
   if(config.block_size < 5) config.block_size = 5;
   if(config.placebo_lag_events < 3) config.placebo_lag_events = 3;
   if(config.regime_block_size_fast < 5) config.regime_block_size_fast = 5;
   if(config.regime_block_size_slow < config.regime_block_size_fast) config.regime_block_size_slow = config.regime_block_size_fast;
   if(config.circular_min_shift_events < 3) config.circular_min_shift_events = 3;
   if(config.local_block_shuffle_size < 5) config.local_block_shuffle_size = 5;
   if(config.context_k_fast < 1) config.context_k_fast = 1;
   if(config.context_k_main < config.context_k_fast) config.context_k_main = config.context_k_fast;
   if(config.context_k_slow < config.context_k_main) config.context_k_slow = config.context_k_main;
   if(config.context_ewma_alpha <= 0.0) config.context_ewma_alpha = 0.35;
   if(config.context_ewma_alpha >= 1.0) config.context_ewma_alpha = 0.99;
   if(config.context_strong_threshold < 0.51) config.context_strong_threshold = 0.51;
   if(config.context_strong_threshold > 0.95) config.context_strong_threshold = 0.95;
}

void UpdateRuntimeComment(const int bars_count, const string source_mode)
{
   string start_text = g_analysis_start_time > 0 ? TimeToString(g_analysis_start_time, TIME_DATE | TIME_MINUTES) : "pending";

   Comment(
      "Decision Alpha Lab | M0004 Branch Regime Clustering\n",
      "source=", source_mode,
      "  symbol=", LabSymbol(),
      "  tf=", EnumToString(LabTimeframe()), "\n",
      "bars=", bars_count,
      "  warmup_bars=", InpWarmupHistoricalBars,
      "  analysis_start=", start_text, "\n",
      "measureMode=EVENT_RTV_LOCKED; sampleWindow=M0001 event RTV\n",
      "branch sequence = atomic no-sample known-time batches by default\n",
      "consumeMode=", DAL_M0001ConsumeModeToString(InpConsumeMode),
      "  touchCycle=", (InpConsumeMode == DAL_M0001_CONSUME_BY_HUNT ? "touch_exit_can_close_either_side_then_recompute_if_not_hunted" : "touch_exit_can_close_either_side_consumes_node"), "\n",
      "stressIters=", InpBranchStressIterations,
      "  blockSize=", InpBranchBlockSize,
      "  placeboLagEvents=", InpBranchPlaceboLagEvents,
      "  regimeBlocks=", InpRegimeBlockSizeFast, "/", InpBranchBlockSize, "/", InpRegimeBlockSizeSlow,
      "  circularMinShift=", InpCircularMinShiftEvents,
      "  localBlockShuffle=", InpLocalBlockShuffleSize, "\n",
      "contextK=", InpContextLookbackFast, "/", InpContextLookbackMain, "/", InpContextLookbackSlow,
      "  ewmaAlpha=", DoubleToString(InpContextEwmaAlpha, 2),
      "  contextThreshold=", DoubleToString(InpContextStrongThreshold, 2), "\n",
      "final branch-regime clustering report prints once on deinit"
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
   else if(DAL_M0004_START_FROM_NEXT_CLOSED_BAR)
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


void RunAtomicNoSampleM0004MainReport(const string source_mode)
{
   DALM0004AtomicNoSampleConfig cfg;
   cfg.report_mode = (InpAtomicReportMode == 1 ? DAL_M0004_ATOMIC_STRICT_PREFIX_REPLAY : DAL_M0004_ATOMIC_FAST_RAW_EVENT_BATCH);
   cfg.symbol = LabSymbol();
   cfg.timeframe = LabTimeframe();
   cfg.replay_closed_bars = (InpBars > 0 ? InpBars : g_live_bars_count);
   if(cfg.replay_closed_bars < 200) cfg.replay_closed_bars = 2500;
   cfg.warmup_closed_bars = InpWarmupHistoricalBars;
   cfg.L = InpL;
   cfg.zone_ratio = InpZoneRatio;
   cfg.exit_gap = InpExitGap;
   cfg.consume_mode = InpConsumeMode;
   cfg.outcome_candle_offset_after_exit = InpOutcomeCandleOffsetAfterExit;
   cfg.require_event_rtv_ready = false;
   cfg.skip_ambiguous_energy_batch = true;
   cfg.permutation_iterations = InpAtomicPermutationIterations;
   cfg.print_extended_report = InpAtomicPrintExtendedReport;
   cfg.print_deep_report = InpAtomicPrintDeepReport;
   cfg.print_h6_optionality_report = InpAtomicPrintH6OptionalityReport;
   cfg.print_h6_edge_map = false;
   cfg.h6_only_report = false;
   cfg.h6_min_bucket_n = 50;
   cfg.stress_transition_permutation = InpAtomicStressTransitionPermutation;
   cfg.stress_run_shuffle = InpAtomicStressRunShuffle;
   cfg.stress_block_concentration = InpAtomicStressBlockConcentration;
   cfg.stress_circular_shift = InpAtomicStressCircularShift;
   cfg.stress_local_block_shuffle = InpAtomicStressLocalBlockShuffle;
   cfg.stress_h6_optionality = InpAtomicStressH6Optionality;
   cfg.print_human_context_report = InpAtomicPrintHumanContextReport;
   cfg.stress_context_shuffle = InpAtomicStressContextShuffle;
   cfg.h6_horizon_fast = InpH6HorizonBarsFast;
   cfg.h6_horizon_main = InpH6HorizonBarsMain;
   cfg.h6_horizon_slow = InpH6HorizonBarsSlow;
   cfg.h6_atr_period = InpH6AtrPeriod;
   cfg.h6_tail_atr_1 = InpH6TailAtr1;
   cfg.h6_tail_atr_2 = InpH6TailAtr2;
   cfg.h6_tail_atr_3 = InpH6TailAtr3;
   cfg.context_k_fast = InpAtomicContextLookbackFast;
   cfg.context_k_main = InpAtomicContextLookbackMain;
   cfg.context_k_slow = InpAtomicContextLookbackSlow;
   cfg.context_ewma_alpha = InpAtomicContextEwmaAlpha;
   cfg.context_strong_threshold = InpAtomicContextStrongThreshold;
   cfg.circular_min_shift_batches = InpAtomicCircularMinShiftBatches;
   cfg.local_block_shuffle_size = InpAtomicLocalBlockShuffleSize;
   if(cfg.context_k_fast < 1) cfg.context_k_fast = 1;
   if(cfg.context_k_main < cfg.context_k_fast) cfg.context_k_main = cfg.context_k_fast;
   if(cfg.context_k_slow < cfg.context_k_main) cfg.context_k_slow = cfg.context_k_main;
   if(cfg.context_ewma_alpha <= 0.0) cfg.context_ewma_alpha = 0.35;
   if(cfg.context_ewma_alpha >= 1.0) cfg.context_ewma_alpha = 0.99;
   if(cfg.context_strong_threshold < 0.51) cfg.context_strong_threshold = 0.51;
   if(cfg.context_strong_threshold > 0.95) cfg.context_strong_threshold = 0.95;
   if(cfg.circular_min_shift_batches < 2) cfg.circular_min_shift_batches = 2;
   if(cfg.local_block_shuffle_size < 5) cfg.local_block_shuffle_size = 5;
   if(cfg.h6_horizon_fast < 1) cfg.h6_horizon_fast = 1;
   if(cfg.h6_horizon_main < cfg.h6_horizon_fast) cfg.h6_horizon_main = cfg.h6_horizon_fast;
   if(cfg.h6_horizon_slow < cfg.h6_horizon_main) cfg.h6_horizon_slow = cfg.h6_horizon_main;
   if(cfg.h6_atr_period < 2) cfg.h6_atr_period = 2;
   if(cfg.h6_tail_atr_1 <= 0.0) cfg.h6_tail_atr_1 = 2.0;
   if(cfg.h6_tail_atr_2 < cfg.h6_tail_atr_1) cfg.h6_tail_atr_2 = cfg.h6_tail_atr_1;
   if(cfg.h6_tail_atr_3 < cfg.h6_tail_atr_2) cfg.h6_tail_atr_3 = cfg.h6_tail_atr_2;
   cfg.block_size_fast = InpAtomicBlockSizeFast;
   cfg.block_size_main = InpAtomicBlockSizeMain;
   cfg.block_size_slow = InpAtomicBlockSizeSlow;
   cfg.print_only_summary = true;
   cfg.print_every_n_batches = 100;
   cfg.write_csv = InpAtomicWriteCsv;
   cfg.csv_file_name = InpAtomicCsvFileName;

   Print(
      "DAL_M0004_MAIN_ATOMIC_SANITY *** symbol=", LabSymbol(),
      "*tf=", EnumToString(LabTimeframe()),
      "*source=", source_mode,
      "*build=", DAL_M0004_BUILD,
      "*officialReport=ATOMIC_NO_SAMPLE",
      "*atomicMode=", (cfg.report_mode == DAL_M0004_ATOMIC_STRICT_PREFIX_REPLAY ? "STRICT_PREFIX_REPLAY" : "FAST_RAW_EVENT_BATCH"),
      "*sampleCalls=0*branchSamplesBuilt=0*m0002Calls=0",
      "*contract=no_m0002_no_branch_samples_raw_m0001_events_only",
      "*sequenceOrder=known_time_batch_sequence",
      "*sameKnownTimeEventsAreSimultaneous=1",
      "*mixedEnergyBatchPolicy=ambiguous_skip_from_transition",
      "*legacySampleReportEnabled=", (InpPrintLegacySampleReport ? 1 : 0),
      "*replayClosedBars=", cfg.replay_closed_bars,
      "*permutationIterations=", cfg.permutation_iterations,
      "*stressTransitionPermutation=", (cfg.stress_transition_permutation ? 1 : 0),
      "*stressRunShuffle=", (cfg.stress_run_shuffle ? 1 : 0),
      "*stressBlockConcentration=", (cfg.stress_block_concentration ? 1 : 0),
      "*stressCircularShift=", (cfg.stress_circular_shift ? 1 : 0),
      "*stressLocalBlockShuffle=", (cfg.stress_local_block_shuffle ? 1 : 0),
      "*extendedReport=", (cfg.print_extended_report ? 1 : 0),
      "*deepReport=", (cfg.print_deep_report ? 1 : 0),
      "*h6OptionalityReport=", (cfg.print_h6_optionality_report ? 1 : 0),
      "*stressH6Optionality=", (cfg.stress_h6_optionality ? 1 : 0),
      "*humanContextReport=", (cfg.print_human_context_report ? 1 : 0),
      "*h6Horizons=", cfg.h6_horizon_fast, "/", cfg.h6_horizon_main, "/", cfg.h6_horizon_slow,
      "*h6AtrPeriod=", cfg.h6_atr_period,
      "*h6TailAtr=", DoubleToString(cfg.h6_tail_atr_1, 2), "/", DoubleToString(cfg.h6_tail_atr_2, 2), "/", DoubleToString(cfg.h6_tail_atr_3, 2),
      "*contextK=", cfg.context_k_fast, "/", cfg.context_k_main, "/", cfg.context_k_slow,
      "*contextEwmaAlpha=", DoubleToString(cfg.context_ewma_alpha, 4),
      "*contextStrongThreshold=", DoubleToString(cfg.context_strong_threshold, 4),
      "*blockFast=", cfg.block_size_fast,
      "*blockMain=", cfg.block_size_main,
      "*blockSlow=", cfg.block_size_slow,
      "*warmupClosedBars=", cfg.warmup_closed_bars,
      "*L=", cfg.L,
      "*zoneRatio=", DoubleToString(cfg.zone_ratio, 4),
      "*exitGap=", cfg.exit_gap,
      "*consumeMode=", DAL_M0001ConsumeModeToString(cfg.consume_mode)
   );

   DAL_M0004RunAtomicNoSampleReport(cfg);
   DAL_M0004CloseAtomicNoSampleReport();
}

void PrintFinalReportsFromBars(
   const DALBar &bars[],
   const int bars_count,
   const string source_mode
)
{
   if(bars_count <= 0)
      return;

   if(InpUseAtomicNoSampleMainReport)
   {
      RunAtomicNoSampleM0004MainReport(source_mode);
      if(!InpPrintLegacySampleReport)
         return;
   }

   DALLRuleNode nodes[];
   DALM0001Event events[];
   int nodes_count = 0;
   int events_count = 0;
   ComputeM0002M0001LifecycleEvents(bars, bars_count, nodes, nodes_count, events, events_count);

   DALM0002Config h2_config;
   BuildM0002Config(h2_config);

   DALM0004Config h4_config;
   BuildM0004Config(h4_config);

   Print(
      "DAL_M0004_BUILD_SANITY *** symbol=", LabSymbol(),
      "*tf=", EnumToString(LabTimeframe()),
      "*source=", source_mode,
      "*build=", DAL_M0004_BUILD,
      "*measureMode=EVENT_RTV_LOCKED*stressSuite=H4_FULL",
      "*sampleWindow=m0001EventRtv",
      "*branchSequence=chronological_M0002_exit_labels",
      "*consumeMode=", DAL_M0001ConsumeModeToString(InpConsumeMode),
      "*touchCycle=", (InpConsumeMode == DAL_M0001_CONSUME_BY_HUNT ? "touch_exit_can_close_either_side_recompute_if_not_hunted" : "touch_exit_can_close_either_side_consumes_node"),
      "*branchStressIters=", InpBranchStressIterations,
      "*branchBlockSize=", InpBranchBlockSize,
      "*branchPlaceboLagEvents=", InpBranchPlaceboLagEvents,
      "*regimeBlockFast=", InpRegimeBlockSizeFast,
      "*regimeBlockSlow=", InpRegimeBlockSizeSlow,
      "*circularMinShiftEvents=", InpCircularMinShiftEvents,
      "*localBlockShuffleSize=", InpLocalBlockShuffleSize,
      "*contextKFast=", InpContextLookbackFast,
      "*contextKMain=", InpContextLookbackMain,
      "*contextKSlow=", InpContextLookbackSlow,
      "*contextEwmaAlpha=", DoubleToString(InpContextEwmaAlpha, 4),
      "*contextStrongThreshold=", DoubleToString(InpContextStrongThreshold, 4),
      "*L=", InpL,
      "*zoneRatio=", DoubleToString(InpZoneRatio, 4),
      "*exitGap=", InpExitGap,
      "*warmupBars=", InpWarmupHistoricalBars,
      "*eventUniverseGuard=exact_M0001_compute_events_then_M0002_branch_collect_then_chronological_sort",
      "*oldPostOutcomeFieldsForbidden=sampleBars_sampleStarts_afterOutcomeCandle",
      " *** if_this_line_is_missing_you_are_running_an_old_EX5_or_wrong_file"
   );

   Print(
      "DAL_M0004_BASE_STATE *** symbol=", LabSymbol(),
      "*tf=", EnumToString(LabTimeframe()),
      "*source=", source_mode,
      "*bars=", bars_count,
      "*nodes=", nodes_count,
      "*m0001Events=", events_count,
      "*analysisStart=", DAL_M0001AnalysisStartText(g_analysis_start_time),
      " *** logic=M0004_uses_exact_M0001_M0002_branch_labels_for_regime_clustering*build=", DAL_M0004_BUILD,
      "*measureMode=EVENT_RTV_LOCKED*stressSuite=H4_FULL*sampleWindow=m0001EventRtv*consumeMode=", DAL_M0001ConsumeModeToString(InpConsumeMode),
      "*touchCycle=", (InpConsumeMode == DAL_M0001_CONSUME_BY_HUNT ? "touch_exit_can_close_either_side_recompute_if_not_hunted" : "touch_exit_can_close_either_side_consumes_node"),
      "*branchStressIters=", InpBranchStressIterations,
      "*branchBlockSize=", InpBranchBlockSize,
      "*branchPlaceboLagEvents=", InpBranchPlaceboLagEvents,
      "*regimeBlockFast=", InpRegimeBlockSizeFast,
      "*regimeBlockSlow=", InpRegimeBlockSizeSlow,
      "*circularMinShiftEvents=", InpCircularMinShiftEvents,
      "*localBlockShuffleSize=", InpLocalBlockShuffleSize,
      "*contextKFast=", InpContextLookbackFast,
      "*contextKMain=", InpContextLookbackMain,
      "*contextKSlow=", InpContextLookbackSlow,
      "*contextEwmaAlpha=", DoubleToString(InpContextEwmaAlpha, 4),
      "*contextStrongThreshold=", DoubleToString(InpContextStrongThreshold, 4),
      "*inputFingerprint=L", InpL,
      "_zr", DoubleToString(InpZoneRatio, 4),
      "_eg", InpExitGap,
      "_warm", InpWarmupHistoricalBars
   );

   DAL_M0004PrintFinalReports(
      events,
      events_count,
      bars,
      bars_count,
      LabSymbol(),
      EnumToString(LabTimeframe()),
      source_mode,
      g_analysis_start_time,
      h2_config,
      h4_config
   );
}

void PrintFinalReports()
{
   if(DAL_M0004_USE_LIVE_BAR_STREAM)
   {
      PrintFinalReportsFromBars(g_live_bars, g_live_bars_count, "final_live_stream");
      return;
   }

   DALBar bars[];
   int bars_count = DAL_LoadBarsChronological(LabSymbol(), LabTimeframe(), InpBars, DAL_M0004_CLOSED_BARS_ONLY, bars);
   PrintFinalReportsFromBars(bars, bars_count, "final_copyrates");
}

int OnInit()
{
   InitializeCandleClock();

   if(DAL_M0004_USE_LIVE_BAR_STREAM)
   {
      InitializeLiveBarStream();
      UpdateRuntimeComment(g_live_bars_count, "branch_regime_warmup_ready");
   }
   else
   {
      UpdateRuntimeComment(0, "branch_regime_copyrates_ready");
   }

   if(DAL_M0004_TIMER_MS > 0)
      EventSetMillisecondTimer(DAL_M0004_TIMER_MS);

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

   if(DAL_M0004_USE_LIVE_BAR_STREAM)
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

   if(DAL_M0004_USE_LIVE_BAR_STREAM)
   {
      bool appended = UpdateLiveBarStream();
      if(appended)
         UpdateRuntimeComment(g_live_bars_count, "live_stream_timer_new_candle");
      return;
   }
}
