//+------------------------------------------------------------------+
//| Decision Alpha Lab — M0006 Reversal Explosive Optionality          |
//| Hypothesis 6: reversal known-time batches may be fatter-tail       |
//| optionality points, not necessarily higher win-rate points.        |
//+------------------------------------------------------------------+
#property strict
#property version   "1.00"
#property description "M0006 standalone atomic no-sample optionality and edge-map report"

#include <DecisionAlphaLab/M0001/DAL_M0001Config.mqh>

input string InpSymbol = "";                    // empty = chart symbol
input ENUM_TIMEFRAMES InpTimeframe = PERIOD_CURRENT;
input int InpBars = 0;                           // 0 = all available closed bars
input int InpWarmupHistoricalBars = 5000;

input int InpPermutationIterations = 100;
input bool InpStressH6Optionality = true;
input int InpH6StressMode = 1;                    // 0=off, 1=fast mean/hit null, 2=full mean+p90 null
input bool InpPrintH6EdgeMap = true;
input int InpH6EdgeMapLevel = 1;                  // 0=off, 1=core, 2=full
input int InpH6MinBucketN = 50;
input int InpH6EntryAnchorMode = 1;               // 0=known close, 1=next open
input bool InpH6ReportFastHorizon = true;
input bool InpH6ReportMainHorizon = true;
input bool InpH6ReportSlowHorizon = true;
input bool InpH6PrintComputeAudit = true;

input int InpH6HorizonBarsFast = 5;
input int InpH6HorizonBarsMain = 20;
input int InpH6HorizonBarsSlow = 50;
input int InpH6AtrPeriod = 14;
input double InpH6TailAtr1 = 2.0;
input double InpH6TailAtr2 = 4.0;
input double InpH6TailAtr3 = 8.0;

input int InpL = 5;
input double InpZoneRatio = 0.90;
input int InpExitGap = 6;
input ENUM_DALM0001ConsumeMode InpConsumeMode = DAL_M0001_CONSUME_BY_HUNT;
input int InpOutcomeCandleOffsetAfterExit = 0;
input bool InpWriteCsv = false;
input string InpCsvFileName = "M0006_Reversal_Explosive_Optionality.csv";

#include <DecisionAlphaLab/M0006/DAL_M0006OptionalityReport.mqh>

#define DAL_M0006_BUILD "1.01"

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

void RunM0006Report()
{
   DALM0004AtomicNoSampleConfig cfg;
   cfg.report_mode = DAL_M0004_ATOMIC_FAST_RAW_EVENT_BATCH;
   cfg.symbol = M6Symbol();
   cfg.timeframe = M6Timeframe();
   cfg.replay_closed_bars = (InpBars > 0 ? InpBars : Bars(M6Symbol(), M6Timeframe()) - 1);
   if(cfg.replay_closed_bars < 200) cfg.replay_closed_bars = 2500;
   cfg.warmup_closed_bars = InpWarmupHistoricalBars;
   cfg.L = InpL;
   cfg.zone_ratio = InpZoneRatio;
   cfg.exit_gap = InpExitGap;
   cfg.consume_mode = InpConsumeMode;
   cfg.outcome_candle_offset_after_exit = InpOutcomeCandleOffsetAfterExit;
   cfg.require_event_rtv_ready = false;
   cfg.skip_ambiguous_energy_batch = true;
   cfg.permutation_iterations = InpPermutationIterations;

   // H6 standalone mode: keep only optionality reports and edge-map diagnostics.
   cfg.h6_only_report = true;
   cfg.print_h6_optionality_report = true;
   cfg.print_h6_edge_map = InpPrintH6EdgeMap;
   cfg.h6_min_bucket_n = InpH6MinBucketN;
   cfg.h6_stress_mode = MathMax(0, MathMin(2, InpH6StressMode));
   cfg.h6_edge_map_level = MathMax(0, MathMin(2, InpH6EdgeMapLevel));
   cfg.h6_entry_anchor_mode = (InpH6EntryAnchorMode == 1 ? 1 : 0);
   cfg.h6_report_fast_horizon = InpH6ReportFastHorizon;
   cfg.h6_report_main_horizon = InpH6ReportMainHorizon;
   cfg.h6_report_slow_horizon = InpH6ReportSlowHorizon;
   cfg.h6_print_compute_audit = InpH6PrintComputeAudit;
   cfg.stress_h6_optionality = (InpStressH6Optionality && cfg.h6_stress_mode > 0);

   // Disable H4-only diagnostics in the standalone H6 expert.
   cfg.print_extended_report = false;
   cfg.print_deep_report = false;
   cfg.stress_transition_permutation = false;
   cfg.stress_run_shuffle = false;
   cfg.stress_block_concentration = false;
   cfg.stress_circular_shift = false;
   cfg.stress_local_block_shuffle = false;
   cfg.print_human_context_report = false;
   cfg.stress_context_shuffle = false;

   cfg.h6_horizon_fast = MathMax(1, InpH6HorizonBarsFast);
   cfg.h6_horizon_main = MathMax(cfg.h6_horizon_fast, InpH6HorizonBarsMain);
   cfg.h6_horizon_slow = MathMax(cfg.h6_horizon_main, InpH6HorizonBarsSlow);
   cfg.h6_atr_period = MathMax(2, InpH6AtrPeriod);
   cfg.h6_tail_atr_1 = (InpH6TailAtr1 > 0.0 ? InpH6TailAtr1 : 2.0);
   cfg.h6_tail_atr_2 = MathMax(cfg.h6_tail_atr_1, InpH6TailAtr2);
   cfg.h6_tail_atr_3 = MathMax(cfg.h6_tail_atr_2, InpH6TailAtr3);

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

   string sanity_line = "DAL_M0006_BUILD_SANITY *** symbol=" + M6Symbol()
      + "*tf=" + EnumToString(M6Timeframe())
      + "*build=" + DAL_M0006_BUILD
      + "*officialReport=H0006_STANDALONE_ATOMIC_OPTIONALITY"
      + "*sampleCalls=0*branchSamplesBuilt=0*m0002Calls=0"
      + "*contract=no_m0002_no_branch_samples_raw_m0001_events_only"
      + "*sequenceOrder=known_time_batch_sequence"
      + "*sameKnownTimeEventsAreSimultaneous=1"
      + "*hypothesis=reversal_explosive_optionality_not_win_rate"
      + "*replayClosedBars=" + IntegerToString(cfg.replay_closed_bars)
      + "*permutationIterations=" + IntegerToString(cfg.permutation_iterations)
      + "*horizons=" + IntegerToString(cfg.h6_horizon_fast) + "/" + IntegerToString(cfg.h6_horizon_main) + "/" + IntegerToString(cfg.h6_horizon_slow)
      + "*horizonFlags=" + IntegerToString(cfg.h6_report_fast_horizon ? 1 : 0) + "/" + IntegerToString(cfg.h6_report_main_horizon ? 1 : 0) + "/" + IntegerToString(cfg.h6_report_slow_horizon ? 1 : 0)
      + "*atrPeriod=" + IntegerToString(cfg.h6_atr_period)
      + "*tailAtr=" + DoubleToString(cfg.h6_tail_atr_1, 2) + "/" + DoubleToString(cfg.h6_tail_atr_2, 2) + "/" + DoubleToString(cfg.h6_tail_atr_3, 2)
      + "*entryAnchor=" + (cfg.h6_entry_anchor_mode == 1 ? "NEXT_OPEN" : "KNOWN_CLOSE")
      + "*edgeMap=" + IntegerToString(cfg.print_h6_edge_map ? 1 : 0)
      + "*edgeMapLevel=" + IntegerToString(cfg.h6_edge_map_level)
      + "*stressMode=" + IntegerToString(cfg.h6_stress_mode)
      + "*minBucketN=" + IntegerToString(cfg.h6_min_bucket_n)
      + "*L=" + IntegerToString(cfg.L)
      + "*zoneRatio=" + DoubleToString(cfg.zone_ratio, 4)
      + "*exitGap=" + IntegerToString(cfg.exit_gap)
      + "*consumeMode=" + DAL_M0001ConsumeModeToString(cfg.consume_mode);
   Print(sanity_line);

   DAL_M0006RunReversalExplosiveOptionality(cfg);
   DAL_M0006CloseReversalExplosiveOptionality();
}

int OnInit()
{
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   RunM0006Report();
}
