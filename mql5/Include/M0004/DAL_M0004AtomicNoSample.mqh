#ifndef __DAL_M0004_ATOMIC_NO_SAMPLE_MQH__
#define __DAL_M0004_ATOMIC_NO_SAMPLE_MQH__

enum ENUM_DALM0004AtomicReportMode
{
   DAL_M0004_ATOMIC_FAST_RAW_EVENT_BATCH = 0,
   DAL_M0004_ATOMIC_STRICT_PREFIX_REPLAY = 1
};

#include <Market/DAL_Bars.mqh>
#include <StructuralNodes/DAL_StructuralNodeEngine.mqh>
#include <M0001/DAL_M0001Config.mqh>
#include <M0001/DAL_M0001Engine.mqh>

struct DALM0004AtomicNoSampleConfig
{
   ENUM_DALM0004AtomicReportMode report_mode;
   string symbol;
   ENUM_TIMEFRAMES timeframe;
   int replay_closed_bars;
   int warmup_closed_bars;
   int L;
   double zone_ratio;
   int exit_gap;
   ENUM_DALM0001ConsumeMode consume_mode;
   int outcome_candle_offset_after_exit;
   bool require_event_rtv_ready;
   bool skip_ambiguous_energy_batch;
   int permutation_iterations;
   bool print_extended_report;
   bool print_deep_report;
   bool print_h6_optionality_report;
   bool print_h6_edge_map;
   bool h6_only_report;
   int h6_min_bucket_n;
   bool stress_transition_permutation;
   bool stress_run_shuffle;
   bool stress_block_concentration;
   bool stress_circular_shift;
   bool stress_local_block_shuffle;
   bool stress_h6_optionality;
   int h6_stress_mode;              // 0=off, 1=fast mean/hit null, 2=full mean+p90 null
   int h6_edge_map_level;           // 0=off, 1=core buckets, 2=full buckets
   int h6_entry_anchor_mode;        // 0=known close, 1=next open (more execution-realistic)
   bool h6_report_fast_horizon;
   bool h6_report_main_horizon;
   bool h6_report_slow_horizon;
   bool h6_print_compute_audit;
   bool h6_candle_stream_mode;       // true = forward candle stream measurement; no future-read loops per bucket
   bool h6_require_full_horizon;     // true = skip observations without a complete future horizon
   bool h6_node_survival_report;     // true = H0006 node survival / no-break map instead of optionality stats
   bool h6_node_draw_chart;          // draw/update H6 objects on chart
   bool h6_node_draw_lines;          // draw old horizontal survivor levels (off by default in M0006)
   bool h6_reaction_box_report;      // report touch->reaction boxes that survive without zone-end retouch
   bool h6_reaction_box_draw_chart;  // draw touch reaction rectangles on chart
   double h6_reaction_away_buffer_points; // min move away from node after touch to confirm reversal
   double h6_reaction_zone_end_buffer_points; // near-zone-end retouch tolerance after reaction
   double h6_reaction_min_box_height_points; // minimum rectangle height for visibility
   int h6_reaction_max_chart_objects;
   bool h6_reaction_box_fill;
   bool h6_reaction_box_back;
   int h6_node_horizon_1;            // first survival maturity, default 20 candles
   int h6_node_horizon_2;            // second survival maturity, default 50 candles
   int h6_node_horizon_3;            // third survival maturity, default 100 candles
   double h6_node_touch_buffer_points; // optional near-node touch buffer in points
   double h6_node_break_buffer_points; // optional break buffer in points
   int h6_node_max_chart_objects;    // cap chart objects for speed/clarity
   int h6_node_line_width;
   color h6_node_color_1;
   color h6_node_color_2;
   color h6_node_color_3;
   bool print_human_context_report;
   bool stress_context_shuffle;
   int h6_horizon_fast;
   int h6_horizon_main;
   int h6_horizon_slow;
   int h6_atr_period;
   double h6_tail_atr_1;
   double h6_tail_atr_2;
   double h6_tail_atr_3;
   int context_k_fast;
   int context_k_main;
   int context_k_slow;
   double context_ewma_alpha;
   double context_strong_threshold;
   int circular_min_shift_batches;
   int local_block_shuffle_size;
   int block_size_fast;
   int block_size_main;
   int block_size_slow;
   bool print_only_summary;
   int print_every_n_batches;
   bool write_csv;
   string csv_file_name;
};

DALM0004AtomicNoSampleConfig g_dal_m0004_atomic_cfg;

#define InpAtomicReportMode g_dal_m0004_atomic_cfg.report_mode
#define InpSymbol g_dal_m0004_atomic_cfg.symbol
#define InpTimeframe g_dal_m0004_atomic_cfg.timeframe
#define InpReplayClosedBars g_dal_m0004_atomic_cfg.replay_closed_bars
#define InpWarmupClosedBars g_dal_m0004_atomic_cfg.warmup_closed_bars
#define InpL g_dal_m0004_atomic_cfg.L
#define InpZoneRatio g_dal_m0004_atomic_cfg.zone_ratio
#define InpExitGap g_dal_m0004_atomic_cfg.exit_gap
#define InpConsumeMode g_dal_m0004_atomic_cfg.consume_mode
#define InpOutcomeCandleOffsetAfterExit g_dal_m0004_atomic_cfg.outcome_candle_offset_after_exit
#define InpRequireEventRtvReady g_dal_m0004_atomic_cfg.require_event_rtv_ready
#define InpSkipAmbiguousEnergyBatch g_dal_m0004_atomic_cfg.skip_ambiguous_energy_batch
#define InpPermutationIterations g_dal_m0004_atomic_cfg.permutation_iterations
#define InpAtomicPrintExtendedReport g_dal_m0004_atomic_cfg.print_extended_report
#define InpAtomicPrintDeepReport g_dal_m0004_atomic_cfg.print_deep_report
#define InpAtomicPrintH6OptionalityReport g_dal_m0004_atomic_cfg.print_h6_optionality_report
#define InpAtomicPrintH6EdgeMap g_dal_m0004_atomic_cfg.print_h6_edge_map
#define InpAtomicH6OnlyReport g_dal_m0004_atomic_cfg.h6_only_report
#define InpH6MinBucketN g_dal_m0004_atomic_cfg.h6_min_bucket_n
#define InpAtomicStressTransitionPermutation g_dal_m0004_atomic_cfg.stress_transition_permutation
#define InpAtomicStressRunShuffle g_dal_m0004_atomic_cfg.stress_run_shuffle
#define InpAtomicStressBlockConcentration g_dal_m0004_atomic_cfg.stress_block_concentration
#define InpAtomicStressCircularShift g_dal_m0004_atomic_cfg.stress_circular_shift
#define InpAtomicStressLocalBlockShuffle g_dal_m0004_atomic_cfg.stress_local_block_shuffle
#define InpAtomicStressH6Optionality g_dal_m0004_atomic_cfg.stress_h6_optionality
#define InpH6StressMode g_dal_m0004_atomic_cfg.h6_stress_mode
#define InpH6EdgeMapLevel g_dal_m0004_atomic_cfg.h6_edge_map_level
#define InpH6EntryAnchorMode g_dal_m0004_atomic_cfg.h6_entry_anchor_mode
#define InpH6ReportFastHorizon g_dal_m0004_atomic_cfg.h6_report_fast_horizon
#define InpH6ReportMainHorizon g_dal_m0004_atomic_cfg.h6_report_main_horizon
#define InpH6ReportSlowHorizon g_dal_m0004_atomic_cfg.h6_report_slow_horizon
#define InpH6PrintComputeAudit g_dal_m0004_atomic_cfg.h6_print_compute_audit
#define InpH6CandleStreamMode g_dal_m0004_atomic_cfg.h6_candle_stream_mode
#define InpH6RequireFullHorizon g_dal_m0004_atomic_cfg.h6_require_full_horizon
#define InpH6NodeSurvivalReport g_dal_m0004_atomic_cfg.h6_node_survival_report
#define InpH6NodeDrawChart g_dal_m0004_atomic_cfg.h6_node_draw_chart
#define InpH6NodeDrawLines g_dal_m0004_atomic_cfg.h6_node_draw_lines
#define InpH6ReactionBoxReport g_dal_m0004_atomic_cfg.h6_reaction_box_report
#define InpH6ReactionBoxDrawChart g_dal_m0004_atomic_cfg.h6_reaction_box_draw_chart
#define InpH6ReactionAwayBufferPoints g_dal_m0004_atomic_cfg.h6_reaction_away_buffer_points
#define InpH6ReactionZoneEndBufferPoints g_dal_m0004_atomic_cfg.h6_reaction_zone_end_buffer_points
#define InpH6ReactionMinBoxHeightPoints g_dal_m0004_atomic_cfg.h6_reaction_min_box_height_points
#define InpH6ReactionMaxChartObjects g_dal_m0004_atomic_cfg.h6_reaction_max_chart_objects
#define InpH6ReactionBoxFill g_dal_m0004_atomic_cfg.h6_reaction_box_fill
#define InpH6ReactionBoxBack g_dal_m0004_atomic_cfg.h6_reaction_box_back
#define InpH6NodeHorizon1 g_dal_m0004_atomic_cfg.h6_node_horizon_1
#define InpH6NodeHorizon2 g_dal_m0004_atomic_cfg.h6_node_horizon_2
#define InpH6NodeHorizon3 g_dal_m0004_atomic_cfg.h6_node_horizon_3
#define InpH6NodeTouchBufferPoints g_dal_m0004_atomic_cfg.h6_node_touch_buffer_points
#define InpH6NodeBreakBufferPoints g_dal_m0004_atomic_cfg.h6_node_break_buffer_points
#define InpH6NodeMaxChartObjects g_dal_m0004_atomic_cfg.h6_node_max_chart_objects
#define InpH6NodeLineWidth g_dal_m0004_atomic_cfg.h6_node_line_width
#define InpH6NodeColor1 g_dal_m0004_atomic_cfg.h6_node_color_1
#define InpH6NodeColor2 g_dal_m0004_atomic_cfg.h6_node_color_2
#define InpH6NodeColor3 g_dal_m0004_atomic_cfg.h6_node_color_3
#define InpAtomicPrintHumanContextReport g_dal_m0004_atomic_cfg.print_human_context_report
#define InpAtomicStressContextShuffle g_dal_m0004_atomic_cfg.stress_context_shuffle
#define InpH6HorizonBarsFast g_dal_m0004_atomic_cfg.h6_horizon_fast
#define InpH6HorizonBarsMain g_dal_m0004_atomic_cfg.h6_horizon_main
#define InpH6HorizonBarsSlow g_dal_m0004_atomic_cfg.h6_horizon_slow
#define InpH6AtrPeriod g_dal_m0004_atomic_cfg.h6_atr_period
#define InpH6TailAtr1 g_dal_m0004_atomic_cfg.h6_tail_atr_1
#define InpH6TailAtr2 g_dal_m0004_atomic_cfg.h6_tail_atr_2
#define InpH6TailAtr3 g_dal_m0004_atomic_cfg.h6_tail_atr_3
#define InpAtomicContextKFast g_dal_m0004_atomic_cfg.context_k_fast
#define InpAtomicContextKMain g_dal_m0004_atomic_cfg.context_k_main
#define InpAtomicContextKSlow g_dal_m0004_atomic_cfg.context_k_slow
#define InpAtomicContextEwmaAlpha g_dal_m0004_atomic_cfg.context_ewma_alpha
#define InpAtomicContextStrongThreshold g_dal_m0004_atomic_cfg.context_strong_threshold
#define InpAtomicCircularMinShiftBatches g_dal_m0004_atomic_cfg.circular_min_shift_batches
#define InpAtomicLocalBlockShuffleSize g_dal_m0004_atomic_cfg.local_block_shuffle_size
#define InpAtomicBlockSizeFast g_dal_m0004_atomic_cfg.block_size_fast
#define InpAtomicBlockSizeMain g_dal_m0004_atomic_cfg.block_size_main
#define InpAtomicBlockSizeSlow g_dal_m0004_atomic_cfg.block_size_slow
#define InpPrintOnlySummary g_dal_m0004_atomic_cfg.print_only_summary
#define InpPrintEveryNBatches g_dal_m0004_atomic_cfg.print_every_n_batches
#define InpWriteCsv g_dal_m0004_atomic_cfg.write_csv
#define InpCsvFileName g_dal_m0004_atomic_cfg.csv_file_name

#define DAL_D0010_BUILD "M0004_MAIN_ATOMIC_1.08"
#define DAL_D0010_LABEL_REVERSAL 0
#define DAL_D0010_LABEL_CONTINUATION 1
#define DAL_D0010_LABEL_UNKNOWN -1


// M0001 structure.

// Atomic no-sample H4 contract.

// Output.

struct D0010Batch
{
   bool has_events;
   bool pure;
   int label;
   int known_index;
   datetime known_time;
   int event_count;
   int reversal_count;
   int continuation_count;
   int buy_direction_count;
   int sell_direction_count;
   bool ambiguous_direction;
   string reason;
};

struct D0010TransitionStats
{
   int n;
   int transitions;
   int reversal_count;
   int continuation_count;
   int rr;
   int rc;
   int cr;
   int cc;
   double reversal_pct;
   double continuation_pct;
   double same_pct;
   double switch_pct;
   double iid_same_pct;
   double same_lift_pct;
   double p_reversal_after_reversal;
   double p_continuation_after_reversal;
   double p_reversal_after_continuation;
   double p_continuation_after_continuation;
   double reversal_persistence_lift;
   double continuation_persistence_lift;
   double lag1_corr;
   double lag2_corr;
};

struct D0010RunStats
{
   int all_run_count;
   int all_max_run;
   double all_avg_run;
   int rev_runs;
   int rev_max_run;
   double rev_avg_run;
   int cont_runs;
   int cont_max_run;
   double cont_avg_run;
   double rev_iid_expected_avg_run;
   double cont_iid_expected_avg_run;
   double rev_avg_run_over_iid;
   double cont_avg_run_over_iid;
};

struct D0010Summary
{
   int steps;
   int decision_steps;
   int load_failures;
   int no_event_steps;
   int no_new_known_batch_steps;
   int raw_events_seen;
   int raw_events_known_now;
   int total_batches;
   int pure_batches;
   int ambiguous_batches;
   int same_time_batch_count;
   int same_time_event_count;
   int mixed_direction_batches;
   int reversal_batches;
   int continuation_batches;
};

int g_csv = INVALID_HANDLE;
D0010Summary g_sum;
int g_labels[];
datetime g_label_times[];
int g_label_batch_counts[];
int g_label_dirs[];
int g_label_known_indices[];

string D0010_Symbol()
{
   return (InpSymbol == "" ? _Symbol : InpSymbol);
}

ENUM_TIMEFRAMES D0010_Timeframe()
{
   return (InpTimeframe == PERIOD_CURRENT ? (ENUM_TIMEFRAMES)_Period : InpTimeframe);
}

string D0010_TimeText(const datetime t)
{
   if(t <= 0) return "0";
   return TimeToString(t, TIME_DATE | TIME_MINUTES | TIME_SECONDS);
}

string D0010_LabelText(const int label)
{
   if(label == DAL_D0010_LABEL_REVERSAL) return "REVERSAL";
   if(label == DAL_D0010_LABEL_CONTINUATION) return "CONTINUATION";
   return "UNKNOWN";
}

string D0010_DirText(const int d)
{
   if(d > 0) return "BUY";
   if(d < 0) return "SELL";
   return "NONE";
}

void D0010_ResetBatch(D0010Batch &b)
{
   b.has_events = false;
   b.pure = false;
   b.label = DAL_D0010_LABEL_UNKNOWN;
   b.known_index = -1;
   b.known_time = 0;
   b.event_count = 0;
   b.reversal_count = 0;
   b.continuation_count = 0;
   b.buy_direction_count = 0;
   b.sell_direction_count = 0;
   b.ambiguous_direction = false;
   b.reason = "not_built";
}

void D0010_ResetSummary(D0010Summary &s)
{
   s.steps = 0;
   s.decision_steps = 0;
   s.load_failures = 0;
   s.no_event_steps = 0;
   s.no_new_known_batch_steps = 0;
   s.raw_events_seen = 0;
   s.raw_events_known_now = 0;
   s.total_batches = 0;
   s.pure_batches = 0;
   s.ambiguous_batches = 0;
   s.same_time_batch_count = 0;
   s.same_time_event_count = 0;
   s.mixed_direction_batches = 0;
   s.reversal_batches = 0;
   s.continuation_batches = 0;
}

void D0010_BuildM0001Config(DALM0001Config &config)
{
   DAL_M0001DefaultConfig(config);
   config.L = InpL;
   config.zone_ratio = InpZoneRatio;
   config.exit_gap = InpExitGap;
   config.consume_mode = InpConsumeMode;
   config.consume_on_touch = (InpConsumeMode == DAL_M0001_CONSUME_BY_TOUCH);
   config.max_events = 0;
   config.min_rtv = 0.0;
}

void D0010_ReverseRates(MqlRates &rates[], const int count)
{
   int l = 0;
   int r = count - 1;
   while(l < r)
   {
      MqlRates tmp = rates[l];
      rates[l] = rates[r];
      rates[r] = tmp;
      l++;
      r--;
   }
}

bool D0010_RatesToBars(MqlRates &raw[], const int copied, DALBar &bars[])
{
   if(copied <= 0)
      return false;
   if(copied > 1 && raw[0].time > raw[copied - 1].time)
      D0010_ReverseRates(raw, copied);

   ArrayResize(bars, copied);
   for(int i = 0; i < copied; i++)
   {
      bars[i].time = raw[i].time;
      bars[i].open = raw[i].open;
      bars[i].high = raw[i].high;
      bars[i].low = raw[i].low;
      bars[i].close = raw[i].close;
      bars[i].tick_volume = raw[i].tick_volume;
      bars[i].spread = raw[i].spread;
   }
   return true;
}

bool D0010_LoadPrefixBars(const int oldest_closed_shift, const int cursor_closed_shift, DALBar &bars[], int &bars_count, string &reason)
{
   ArrayResize(bars, 0);
   bars_count = 0;
   reason = "not_loaded";

   if(oldest_closed_shift < cursor_closed_shift)
   {
      reason = "bad_shift_order";
      return false;
   }

   datetime start_time = iTime(D0010_Symbol(), D0010_Timeframe(), oldest_closed_shift);
   datetime stop_time = iTime(D0010_Symbol(), D0010_Timeframe(), cursor_closed_shift);
   if(start_time <= 0 || stop_time <= 0)
   {
      reason = "bad_itime";
      return false;
   }
   if(start_time > stop_time)
   {
      datetime t = start_time;
      start_time = stop_time;
      stop_time = t;
   }

   MqlRates raw[];
   int copied = CopyRates(D0010_Symbol(), D0010_Timeframe(), start_time, stop_time, raw);
   if(copied <= 0)
   {
      reason = "copy_prefix_failed*err=" + IntegerToString(GetLastError());
      return false;
   }
   if(!D0010_RatesToBars(raw, copied, bars))
   {
      reason = "rates_to_bars_failed";
      return false;
   }

   bars_count = copied;
   reason = "ok_prefix_only";
   return true;
}

int D0010_EventKnownIndex(const DALM0001Event &event)
{
   int base = event.exit_index;
   if(base < 0)
      base = event.touch_confirmed_index;
   if(base < 0)
      return -1;
   return base + MathMax(0, InpOutcomeCandleOffsetAfterExit);
}

bool D0010_EventEligibleForRegime(const DALM0001Event &event)
{
   if(!event.closed || !event.touch_confirmed)
      return false;
   if(InpRequireEventRtvReady && !event.rtv_ready)
      return false;
   return true;
}

bool D0010_ClassifyRawEvent(
   const DALM0001Event &event,
   const DALBar &bars[],
   const int bars_count,
   int &label,
   int &direction,
   int &known_index
)
{
   label = DAL_D0010_LABEL_UNKNOWN;
   direction = 0;
   known_index = D0010_EventKnownIndex(event);

   if(!D0010_EventEligibleForRegime(event))
      return false;
   if(known_index < 0 || known_index >= bars_count)
      return false;

   double known_close = bars[known_index].close;
   if(known_close == event.node_price)
      return false;

   bool low_node = (event.node_type == DAL_NODE_LOW);
   bool reversal = false;
   if(low_node)
      reversal = (known_close > event.node_price);
   else
      reversal = (known_close < event.node_price);

   label = reversal ? DAL_D0010_LABEL_REVERSAL : DAL_D0010_LABEL_CONTINUATION;
   if(label == DAL_D0010_LABEL_REVERSAL)
      direction = low_node ? +1 : -1;
   else
      direction = low_node ? -1 : +1;

   return true;
}

bool D0010_BuildCurrentKnownBatch(
   const DALM0001Event &events[],
   const int events_count,
   const DALBar &bars[],
   const int bars_count,
   const int decision_index,
   D0010Batch &batch
)
{
   D0010_ResetBatch(batch);
   if(events_count <= 0 || bars_count <= 0 || decision_index < 0 || decision_index >= bars_count)
      return false;

   int rev = 0;
   int cont = 0;
   int buy = 0;
   int sell = 0;
   int total = 0;

   for(int i = 0; i < events_count; i++)
   {
      int label = DAL_D0010_LABEL_UNKNOWN;
      int dir = 0;
      int known = -1;
      if(!D0010_ClassifyRawEvent(events[i], bars, bars_count, label, dir, known))
         continue;
      if(known != decision_index)
         continue;

      total++;
      if(label == DAL_D0010_LABEL_REVERSAL) rev++;
      if(label == DAL_D0010_LABEL_CONTINUATION) cont++;
      if(dir > 0) buy++;
      if(dir < 0) sell++;
   }

   if(total <= 0)
   {
      batch.reason = "no_new_raw_event_known_at_this_candle";
      return false;
   }

   batch.has_events = true;
   batch.known_index = decision_index;
   batch.known_time = bars[decision_index].time;
   batch.event_count = total;
   batch.reversal_count = rev;
   batch.continuation_count = cont;
   batch.buy_direction_count = buy;
   batch.sell_direction_count = sell;
   batch.ambiguous_direction = (buy > 0 && sell > 0);

   if(rev > 0 && cont > 0)
   {
      batch.pure = false;
      batch.label = DAL_D0010_LABEL_UNKNOWN;
      batch.reason = "same_known_time_mixed_reversal_continuation";
      return false;
   }

   if(rev > 0)
      batch.label = DAL_D0010_LABEL_REVERSAL;
   else if(cont > 0)
      batch.label = DAL_D0010_LABEL_CONTINUATION;
   else
      batch.label = DAL_D0010_LABEL_UNKNOWN;

   batch.pure = (batch.label == DAL_D0010_LABEL_REVERSAL || batch.label == DAL_D0010_LABEL_CONTINUATION);
   batch.reason = (batch.pure ? "ok_pure_known_time_batch" : "unknown_label");
   return batch.pure;
}

void D0010_AddPureBatchLabel(const D0010Batch &batch)
{
   int n = ArraySize(g_labels);
   if(n > 0 && g_label_times[n - 1] == batch.known_time)
      return;

   ArrayResize(g_labels, n + 1);
   ArrayResize(g_label_times, n + 1);
   ArrayResize(g_label_batch_counts, n + 1);
   ArrayResize(g_label_dirs, n + 1);
   ArrayResize(g_label_known_indices, n + 1);
   g_labels[n] = batch.label;
   g_label_times[n] = batch.known_time;
   g_label_batch_counts[n] = batch.event_count;
   if(batch.buy_direction_count > batch.sell_direction_count)
      g_label_dirs[n] = +1;
   else if(batch.sell_direction_count > batch.buy_direction_count)
      g_label_dirs[n] = -1;
   else
      g_label_dirs[n] = 0;
   g_label_known_indices[n] = batch.known_index;
}

string D0010_ModeText()
{
   if(InpAtomicReportMode == DAL_M0004_ATOMIC_STRICT_PREFIX_REPLAY) return "STRICT_PREFIX_REPLAY";
   return "FAST_RAW_EVENT_BATCH";
}

void D0010_OpenCsv()
{
   if(!InpWriteCsv)
      return;
   g_csv = FileOpen(InpCsvFileName, FILE_WRITE | FILE_CSV | FILE_ANSI);
   if(g_csv == INVALID_HANDLE)
   {
      Print("DAL_D0010_CSV_FAILED *** file=", InpCsvFileName, "*err=", GetLastError());
      return;
   }
   FileWrite(g_csv,
      "known_time",
      "known_index",
      "pure",
      "label",
      "event_count",
      "reversal_count",
      "continuation_count",
      "buy_direction_count",
      "sell_direction_count",
      "ambiguous_direction",
      "reason");
}

void D0010_WriteCsvBatch(const D0010Batch &batch)
{
   if(g_csv == INVALID_HANDLE || !batch.has_events)
      return;
   FileWrite(g_csv,
      D0010_TimeText(batch.known_time),
      batch.known_index,
      batch.pure ? 1 : 0,
      D0010_LabelText(batch.label),
      batch.event_count,
      batch.reversal_count,
      batch.continuation_count,
      batch.buy_direction_count,
      batch.sell_direction_count,
      batch.ambiguous_direction ? 1 : 0,
      batch.reason);
}

double D0010_SafePct(const double part, const double total)
{
   if(total <= 0.0)
      return 0.0;
   return 100.0 * part / total;
}

double D0010_SafeDiv(const double num, const double den)
{
   if(MathAbs(den) <= 0.000000000001)
      return 0.0;
   return num / den;
}

void D0010_ResetTransitionStats(D0010TransitionStats &s)
{
   s.n = 0;
   s.transitions = 0;
   s.reversal_count = 0;
   s.continuation_count = 0;
   s.rr = 0;
   s.rc = 0;
   s.cr = 0;
   s.cc = 0;
   s.reversal_pct = 0.0;
   s.continuation_pct = 0.0;
   s.same_pct = 0.0;
   s.switch_pct = 0.0;
   s.iid_same_pct = 0.0;
   s.same_lift_pct = 0.0;
   s.p_reversal_after_reversal = 0.0;
   s.p_continuation_after_reversal = 0.0;
   s.p_reversal_after_continuation = 0.0;
   s.p_continuation_after_continuation = 0.0;
   s.reversal_persistence_lift = 0.0;
   s.continuation_persistence_lift = 0.0;
   s.lag1_corr = 0.0;
   s.lag2_corr = 0.0;
}

void D0010_ComputeTransitionStats(const int &labels[], const int n, D0010TransitionStats &s)
{
   D0010_ResetTransitionStats(s);
   s.n = n;
   for(int i = 0; i < n; i++)
   {
      if(labels[i] == DAL_D0010_LABEL_REVERSAL) s.reversal_count++;
      if(labels[i] == DAL_D0010_LABEL_CONTINUATION) s.continuation_count++;
   }
   s.transitions = MathMax(0, n - 1);
   for(int j = 1; j < n; j++)
   {
      int prev = labels[j - 1];
      int cur = labels[j];
      if(prev == DAL_D0010_LABEL_REVERSAL && cur == DAL_D0010_LABEL_REVERSAL) s.rr++;
      if(prev == DAL_D0010_LABEL_REVERSAL && cur == DAL_D0010_LABEL_CONTINUATION) s.rc++;
      if(prev == DAL_D0010_LABEL_CONTINUATION && cur == DAL_D0010_LABEL_REVERSAL) s.cr++;
      if(prev == DAL_D0010_LABEL_CONTINUATION && cur == DAL_D0010_LABEL_CONTINUATION) s.cc++;
   }

   double n_d = (double)n;
   double tr_d = (double)s.transitions;
   s.reversal_pct = D0010_SafePct(s.reversal_count, n_d);
   s.continuation_pct = D0010_SafePct(s.continuation_count, n_d);
   s.same_pct = D0010_SafePct(s.rr + s.cc, tr_d);
   s.switch_pct = D0010_SafePct(s.rc + s.cr, tr_d);

   double p_rev = D0010_SafeDiv(s.reversal_count, n_d);
   double p_cont = D0010_SafeDiv(s.continuation_count, n_d);
   s.iid_same_pct = 100.0 * (p_rev * p_rev + p_cont * p_cont);
   s.same_lift_pct = s.same_pct - s.iid_same_pct;

   s.p_reversal_after_reversal = D0010_SafePct(s.rr, s.rr + s.rc);
   s.p_continuation_after_reversal = D0010_SafePct(s.rc, s.rr + s.rc);
   s.p_reversal_after_continuation = D0010_SafePct(s.cr, s.cr + s.cc);
   s.p_continuation_after_continuation = D0010_SafePct(s.cc, s.cr + s.cc);
   s.reversal_persistence_lift = s.p_reversal_after_reversal - s.reversal_pct;
   s.continuation_persistence_lift = s.p_continuation_after_continuation - s.continuation_pct;

   double den = MathSqrt((double)(s.rr + s.rc) * (double)(s.cr + s.cc) * (double)(s.rr + s.cr) * (double)(s.rc + s.cc));
   s.lag1_corr = D0010_SafeDiv((double)s.rr * (double)s.cc - (double)s.rc * (double)s.cr, den);

   if(n > 2)
   {
      int a00 = 0, a01 = 0, a10 = 0, a11 = 0;
      for(int k = 2; k < n; k++)
      {
         int prev2 = labels[k - 2];
         int cur2 = labels[k];
         if(prev2 == DAL_D0010_LABEL_REVERSAL && cur2 == DAL_D0010_LABEL_REVERSAL) a00++;
         if(prev2 == DAL_D0010_LABEL_REVERSAL && cur2 == DAL_D0010_LABEL_CONTINUATION) a01++;
         if(prev2 == DAL_D0010_LABEL_CONTINUATION && cur2 == DAL_D0010_LABEL_REVERSAL) a10++;
         if(prev2 == DAL_D0010_LABEL_CONTINUATION && cur2 == DAL_D0010_LABEL_CONTINUATION) a11++;
      }
      double den2 = MathSqrt((double)(a00 + a01) * (double)(a10 + a11) * (double)(a00 + a10) * (double)(a01 + a11));
      s.lag2_corr = D0010_SafeDiv((double)a00 * (double)a11 - (double)a01 * (double)a10, den2);
   }
}

void D0010_ComputeRuns(const int &labels[], const int n, const D0010TransitionStats &ts, D0010RunStats &r)
{
   r.all_run_count = 0;
   r.all_max_run = 0;
   r.all_avg_run = 0.0;
   r.rev_runs = 0;
   r.rev_max_run = 0;
   r.rev_avg_run = 0.0;
   r.cont_runs = 0;
   r.cont_max_run = 0;
   r.cont_avg_run = 0.0;
   r.rev_iid_expected_avg_run = 0.0;
   r.cont_iid_expected_avg_run = 0.0;
   r.rev_avg_run_over_iid = 0.0;
   r.cont_avg_run_over_iid = 0.0;

   if(n <= 0)
      return;

   int sum_all = 0;
   int sum_rev = 0;
   int sum_cont = 0;
   int cur_label = labels[0];
   int cur_len = 1;

   for(int i = 1; i <= n; i++)
   {
      if(i < n && labels[i] == cur_label)
      {
         cur_len++;
         continue;
      }

      r.all_run_count++;
      sum_all += cur_len;
      if(cur_len > r.all_max_run) r.all_max_run = cur_len;

      if(cur_label == DAL_D0010_LABEL_REVERSAL)
      {
         r.rev_runs++;
         sum_rev += cur_len;
         if(cur_len > r.rev_max_run) r.rev_max_run = cur_len;
      }
      else if(cur_label == DAL_D0010_LABEL_CONTINUATION)
      {
         r.cont_runs++;
         sum_cont += cur_len;
         if(cur_len > r.cont_max_run) r.cont_max_run = cur_len;
      }

      if(i < n)
      {
         cur_label = labels[i];
         cur_len = 1;
      }
   }

   r.all_avg_run = D0010_SafeDiv(sum_all, r.all_run_count);
   r.rev_avg_run = D0010_SafeDiv(sum_rev, r.rev_runs);
   r.cont_avg_run = D0010_SafeDiv(sum_cont, r.cont_runs);

   double p_rev = D0010_SafeDiv(ts.reversal_count, ts.n);
   double p_cont = D0010_SafeDiv(ts.continuation_count, ts.n);
   r.rev_iid_expected_avg_run = D0010_SafeDiv(1.0, MathMax(0.0000001, 1.0 - p_rev));
   r.cont_iid_expected_avg_run = D0010_SafeDiv(1.0, MathMax(0.0000001, 1.0 - p_cont));
   r.rev_avg_run_over_iid = D0010_SafeDiv(r.rev_avg_run, r.rev_iid_expected_avg_run);
   r.cont_avg_run_over_iid = D0010_SafeDiv(r.cont_avg_run, r.cont_iid_expected_avg_run);
}

double D0010_Rand01(const int iter, const int i, const int salt)
{
   double x = MathSin((iter + 1) * 12.9898 + (i + 1) * 78.233 + salt * 37.719) * 43758.5453123;
   double f = x - MathFloor(x);
   if(f < 0.0) f += 1.0;
   return f;
}

void D0010_ShuffleLabels(const int &src[], const int n, const int iter, int &dst[])
{
   ArrayResize(dst, n);
   for(int i = 0; i < n; i++) dst[i] = src[i];
   for(int j = n - 1; j > 0; j--)
   {
      int k = (int)MathFloor(D0010_Rand01(iter, j, 10) * (j + 1));
      if(k < 0) k = 0;
      if(k > j) k = j;
      int tmp = dst[j];
      dst[j] = dst[k];
      dst[k] = tmp;
   }
}

void D0010_PrintTransitionStats(const string tag, const D0010TransitionStats &s)
{
   Print(tag,
      " *** build=", DAL_D0010_BUILD,
      "*contract=atomic_no_sample_raw_m0001_known_time_batches",
      "*n=", s.n,
      "*transitions=", s.transitions,
      "*reversalN=", s.reversal_count,
      "*continuationN=", s.continuation_count,
      "*reversalPct=", DoubleToString(s.reversal_pct, 2),
      "*continuationPct=", DoubleToString(s.continuation_pct, 2),
      "*RR=", s.rr,
      "*RC=", s.rc,
      "*CR=", s.cr,
      "*CC=", s.cc,
      "*samePct=", DoubleToString(s.same_pct, 2),
      "*switchPct=", DoubleToString(s.switch_pct, 2),
      "*iidSamePct=", DoubleToString(s.iid_same_pct, 2),
      "*sameLiftPct=", DoubleToString(s.same_lift_pct, 2),
      "*pRevAfterRev=", DoubleToString(s.p_reversal_after_reversal, 2),
      "*pContAfterRev=", DoubleToString(s.p_continuation_after_reversal, 2),
      "*pRevAfterCont=", DoubleToString(s.p_reversal_after_continuation, 2),
      "*pContAfterCont=", DoubleToString(s.p_continuation_after_continuation, 2),
      "*revPersistenceLift=", DoubleToString(s.reversal_persistence_lift, 2),
      "*contPersistenceLift=", DoubleToString(s.continuation_persistence_lift, 2),
      "*lag1Corr=", DoubleToString(s.lag1_corr, 4),
      "*lag2Corr=", DoubleToString(s.lag2_corr, 4));
}

void D0010_PrintRunStats(const D0010RunStats &r)
{
   Print("DAL_D0010_ATOMIC_RUNS",
      " *** build=", DAL_D0010_BUILD,
      "*contract=atomic_no_sample_raw_m0001_known_time_batches",
      "*allRunCount=", r.all_run_count,
      "*allMaxRun=", r.all_max_run,
      "*allAvgRun=", DoubleToString(r.all_avg_run, 4),
      "*revRuns=", r.rev_runs,
      "*revMaxRun=", r.rev_max_run,
      "*revAvgRun=", DoubleToString(r.rev_avg_run, 4),
      "*revIidExpectedAvgRun=", DoubleToString(r.rev_iid_expected_avg_run, 4),
      "*revAvgRunOverIid=", DoubleToString(r.rev_avg_run_over_iid, 4),
      "*contRuns=", r.cont_runs,
      "*contMaxRun=", r.cont_max_run,
      "*contAvgRun=", DoubleToString(r.cont_avg_run, 4),
      "*contIidExpectedAvgRun=", DoubleToString(r.cont_iid_expected_avg_run, 4),
      "*contAvgRunOverIid=", DoubleToString(r.cont_avg_run_over_iid, 4));
}



double D0010_LabelValue(const int label)
{
   if(label == DAL_D0010_LABEL_CONTINUATION) return 1.0;
   return 0.0;
}

double D0010_LagCorr(const int &labels[], const int n, const int lag)
{
   if(n <= lag || lag <= 0)
      return 0.0;

   double sx = 0.0, sy = 0.0, sxx = 0.0, syy = 0.0, sxy = 0.0;
   int m = 0;
   for(int i = lag; i < n; i++)
   {
      double x = D0010_LabelValue(labels[i - lag]);
      double y = D0010_LabelValue(labels[i]);
      sx += x;
      sy += y;
      sxx += x * x;
      syy += y * y;
      sxy += x * y;
      m++;
   }
   double den = MathSqrt((m * sxx - sx * sx) * (m * syy - sy * sy));
   return D0010_SafeDiv(m * sxy - sx * sy, den);
}

void D0010_PrintLagDecay(const int &labels[], const int n)
{
   if(!InpAtomicPrintExtendedReport || n < 5)
      return;

   double lag1 = D0010_LagCorr(labels, n, 1);
   double lag2 = D0010_LagCorr(labels, n, 2);
   double lag3 = D0010_LagCorr(labels, n, 3);
   double lag5 = D0010_LagCorr(labels, n, 5);
   double lag10 = D0010_LagCorr(labels, n, 10);
   double lag20 = D0010_LagCorr(labels, n, 20);
   double lag50 = D0010_LagCorr(labels, n, 50);
   double lag100 = D0010_LagCorr(labels, n, 100);

   double pos_auc = 0.0;
   int max_lag = MathMin(50, n - 1);
   for(int lag = 1; lag <= max_lag; lag++)
   {
      double c = D0010_LagCorr(labels, n, lag);
      if(c > 0.0) pos_auc += c;
   }

   Print("DAL_D0010_ATOMIC_LAG_DECAY",
      " *** build=", DAL_D0010_BUILD,
      "*contract=atomic_no_sample_raw_m0001_known_time_batches",
      "*n=", n,
      "*lag1Corr=", DoubleToString(lag1, 4),
      "*lag2Corr=", DoubleToString(lag2, 4),
      "*lag3Corr=", DoubleToString(lag3, 4),
      "*lag5Corr=", DoubleToString(lag5, 4),
      "*lag10Corr=", DoubleToString(lag10, 4),
      "*lag20Corr=", DoubleToString(lag20, 4),
      "*lag50Corr=", DoubleToString(lag50, 4),
      "*lag100Corr=", DoubleToString(lag100, 4),
      "*positiveLagCorrAucTo50=", DoubleToString(pos_auc, 4),
      "*sequenceOrder=known_time_batch_sequence");
}

void D0010_PrintRunLengthTransition(const int &labels[], const int n)
{
   if(!InpAtomicPrintExtendedReport || n < 2)
      return;

   int bucketN[4];
   int bucketSame[4];
   int bucketRevN[4];
   int bucketRevSame[4];
   int bucketContN[4];
   int bucketContSame[4];
   ArrayInitialize(bucketN, 0);
   ArrayInitialize(bucketSame, 0);
   ArrayInitialize(bucketRevN, 0);
   ArrayInitialize(bucketRevSame, 0);
   ArrayInitialize(bucketContN, 0);
   ArrayInitialize(bucketContSame, 0);

   int current_run = 1;
   for(int i = 1; i < n; i++)
   {
      int prev = labels[i - 1];
      int cur = labels[i];
      int bucket = 3;
      if(current_run <= 1) bucket = 0;
      else if(current_run == 2) bucket = 1;
      else if(current_run == 3) bucket = 2;

      bool same = (prev == cur);
      bucketN[bucket]++;
      if(same) bucketSame[bucket]++;
      if(prev == DAL_D0010_LABEL_REVERSAL)
      {
         bucketRevN[bucket]++;
         if(same) bucketRevSame[bucket]++;
      }
      if(prev == DAL_D0010_LABEL_CONTINUATION)
      {
         bucketContN[bucket]++;
         if(same) bucketContSame[bucket]++;
      }

      if(same)
         current_run++;
      else
         current_run = 1;
   }

   Print("DAL_D0010_ATOMIC_RUN_LENGTH_TRANSITION",
      " *** build=", DAL_D0010_BUILD,
      "*contract=atomic_no_sample_raw_m0001_known_time_batches",
      "*n=", n,
      "*run1N=", bucketN[0],
      "*run1SamePct=", DoubleToString(D0010_SafePct(bucketSame[0], bucketN[0]), 2),
      "*run1RevSamePct=", DoubleToString(D0010_SafePct(bucketRevSame[0], bucketRevN[0]), 2),
      "*run1ContSamePct=", DoubleToString(D0010_SafePct(bucketContSame[0], bucketContN[0]), 2),
      "*run2N=", bucketN[1],
      "*run2SamePct=", DoubleToString(D0010_SafePct(bucketSame[1], bucketN[1]), 2),
      "*run2RevSamePct=", DoubleToString(D0010_SafePct(bucketRevSame[1], bucketRevN[1]), 2),
      "*run2ContSamePct=", DoubleToString(D0010_SafePct(bucketContSame[1], bucketContN[1]), 2),
      "*run3N=", bucketN[2],
      "*run3SamePct=", DoubleToString(D0010_SafePct(bucketSame[2], bucketN[2]), 2),
      "*run3RevSamePct=", DoubleToString(D0010_SafePct(bucketRevSame[2], bucketRevN[2]), 2),
      "*run3ContSamePct=", DoubleToString(D0010_SafePct(bucketContSame[2], bucketContN[2]), 2),
      "*run4plusN=", bucketN[3],
      "*run4plusSamePct=", DoubleToString(D0010_SafePct(bucketSame[3], bucketN[3]), 2),
      "*run4plusRevSamePct=", DoubleToString(D0010_SafePct(bucketRevSame[3], bucketRevN[3]), 2),
      "*run4plusContSamePct=", DoubleToString(D0010_SafePct(bucketContSame[3], bucketContN[3]), 2));
}

void D0010_PrintBlockProfile(const int &labels[], const int n, const int block_size, const string tag)
{
   if(!InpAtomicPrintExtendedReport || n < 3 || block_size <= 1)
      return;

   int blocks = (n + block_size - 1) / block_size;
   if(blocks <= 0)
      return;

   double cont_sum = 0.0, cont_sum2 = 0.0;
   double lift_sum = 0.0, lift_sum2 = 0.0;
   double lag_sum = 0.0, lag_sum2 = 0.0;
   double min_cont = 1000000.0, max_cont = -1000000.0;
   int positive_lift = 0;
   int positive_lag = 0;
   int hot_cont = 0;
   int cold_cont = 0;

   D0010TransitionStats global_ts;
   D0010_ComputeTransitionStats(labels, n, global_ts);

   for(int b = 0; b < blocks; b++)
   {
      int start = b * block_size;
      int end = MathMin(n, start + block_size);
      int m = end - start;
      if(m <= 1) continue;

      int local[];
      ArrayResize(local, m);
      for(int i = 0; i < m; i++) local[i] = labels[start + i];

      D0010TransitionStats st;
      D0010_ComputeTransitionStats(local, m, st);
      cont_sum += st.continuation_pct;
      cont_sum2 += st.continuation_pct * st.continuation_pct;
      lift_sum += st.same_lift_pct;
      lift_sum2 += st.same_lift_pct * st.same_lift_pct;
      lag_sum += st.lag1_corr;
      lag_sum2 += st.lag1_corr * st.lag1_corr;
      if(st.continuation_pct < min_cont) min_cont = st.continuation_pct;
      if(st.continuation_pct > max_cont) max_cont = st.continuation_pct;
      if(st.same_lift_pct > 0.0) positive_lift++;
      if(st.lag1_corr > 0.0) positive_lag++;
      if(st.continuation_pct >= global_ts.continuation_pct + 10.0) hot_cont++;
      if(st.continuation_pct <= global_ts.continuation_pct - 10.0) cold_cont++;
   }

   double mean_cont = D0010_SafeDiv(cont_sum, blocks);
   double sd_cont = MathSqrt(MathMax(0.0, D0010_SafeDiv(cont_sum2, blocks) - mean_cont * mean_cont));
   double mean_lift = D0010_SafeDiv(lift_sum, blocks);
   double sd_lift = MathSqrt(MathMax(0.0, D0010_SafeDiv(lift_sum2, blocks) - mean_lift * mean_lift));
   double mean_lag = D0010_SafeDiv(lag_sum, blocks);
   double sd_lag = MathSqrt(MathMax(0.0, D0010_SafeDiv(lag_sum2, blocks) - mean_lag * mean_lag));

   Print("DAL_D0010_ATOMIC_BLOCK_PROFILE_" + tag,
      " *** build=", DAL_D0010_BUILD,
      "*contract=atomic_no_sample_raw_m0001_known_time_batches",
      "*n=", n,
      "*blockSize=", block_size,
      "*blocks=", blocks,
      "*globalContPct=", DoubleToString(global_ts.continuation_pct, 2),
      "*meanContPct=", DoubleToString(mean_cont, 2),
      "*sdContPct=", DoubleToString(sd_cont, 4),
      "*minContPct=", DoubleToString(min_cont, 2),
      "*maxContPct=", DoubleToString(max_cont, 2),
      "*meanSameLift=", DoubleToString(mean_lift, 2),
      "*sdSameLift=", DoubleToString(sd_lift, 4),
      "*meanLag1=", DoubleToString(mean_lag, 4),
      "*sdLag1=", DoubleToString(sd_lag, 4),
      "*positiveLiftBlockPct=", DoubleToString(D0010_SafePct(positive_lift, blocks), 2),
      "*positiveLagBlockPct=", DoubleToString(D0010_SafePct(positive_lag, blocks), 2),
      "*hotContinuationBlockPct=", DoubleToString(D0010_SafePct(hot_cont, blocks), 2),
      "*coldContinuationBlockPct=", DoubleToString(D0010_SafePct(cold_cont, blocks), 2));
}


void D0010_PrintRunShuffleStress(const int &labels[], const int n, const D0010RunStats &obs)
{
   if(!InpAtomicStressRunShuffle || n < 5 || InpPermutationIterations <= 0)
      return;

   double max_sum = 0.0, max_sum2 = 0.0;
   double avg_sum = 0.0, avg_sum2 = 0.0;
   double rev_avg_sum = 0.0, rev_avg_sum2 = 0.0;
   double cont_avg_sum = 0.0, cont_avg_sum2 = 0.0;
   int max_ge = 0, avg_ge = 0, cont_ge = 0;

   int shuffled[];
   for(int iter = 0; iter < InpPermutationIterations; iter++)
   {
      D0010_ShuffleLabels(labels, n, iter + 101, shuffled);
      D0010TransitionStats ts;
      D0010RunStats rs;
      D0010_ComputeTransitionStats(shuffled, n, ts);
      D0010_ComputeRuns(shuffled, n, ts, rs);

      double mx = (double)rs.all_max_run;
      double av = rs.all_avg_run;
      double rv = rs.rev_avg_run;
      double cv = rs.cont_avg_run;
      max_sum += mx; max_sum2 += mx * mx;
      avg_sum += av; avg_sum2 += av * av;
      rev_avg_sum += rv; rev_avg_sum2 += rv * rv;
      cont_avg_sum += cv; cont_avg_sum2 += cv * cv;
      if(rs.all_max_run >= obs.all_max_run) max_ge++;
      if(rs.all_avg_run >= obs.all_avg_run) avg_ge++;
      if(rs.cont_avg_run >= obs.cont_avg_run) cont_ge++;
   }

   double it = (double)InpPermutationIterations;
   double max_mean = D0010_SafeDiv(max_sum, it);
   double avg_mean = D0010_SafeDiv(avg_sum, it);
   double rev_mean = D0010_SafeDiv(rev_avg_sum, it);
   double cont_mean = D0010_SafeDiv(cont_avg_sum, it);
   double max_sd = MathSqrt(MathMax(0.0, D0010_SafeDiv(max_sum2, it) - max_mean * max_mean));
   double avg_sd = MathSqrt(MathMax(0.0, D0010_SafeDiv(avg_sum2, it) - avg_mean * avg_mean));
   double cont_sd = MathSqrt(MathMax(0.0, D0010_SafeDiv(cont_avg_sum2, it) - cont_mean * cont_mean));

   Print("DAL_D0010_ATOMIC_RUN_SHUFFLE_STRESS",
      " *** build=", DAL_D0010_BUILD,
      "*contract=atomic_no_sample_raw_m0001_known_time_batches",
      "*n=", n,
      "*iters=", InpPermutationIterations,
      "*obsAllMaxRun=", obs.all_max_run,
      "*shuffleAllMaxRunMean=", DoubleToString(max_mean, 4),
      "*shuffleAllMaxRunSd=", DoubleToString(max_sd, 4),
      "*allMaxRunZ=", DoubleToString(D0010_SafeDiv((double)obs.all_max_run - max_mean, max_sd), 4),
      "*allMaxRunEmpP=", DoubleToString(D0010_SafeDiv(max_ge + 1, InpPermutationIterations + 1), 4),
      "*obsAllAvgRun=", DoubleToString(obs.all_avg_run, 4),
      "*shuffleAllAvgRunMean=", DoubleToString(avg_mean, 4),
      "*shuffleAllAvgRunSd=", DoubleToString(avg_sd, 4),
      "*allAvgRunZ=", DoubleToString(D0010_SafeDiv(obs.all_avg_run - avg_mean, avg_sd), 4),
      "*allAvgRunEmpP=", DoubleToString(D0010_SafeDiv(avg_ge + 1, InpPermutationIterations + 1), 4),
      "*obsRevAvgRun=", DoubleToString(obs.rev_avg_run, 4),
      "*shuffleRevAvgRunMean=", DoubleToString(rev_mean, 4),
      "*obsContAvgRun=", DoubleToString(obs.cont_avg_run, 4),
      "*shuffleContAvgRunMean=", DoubleToString(cont_mean, 4),
      "*shuffleContAvgRunSd=", DoubleToString(cont_sd, 4),
      "*contAvgRunEmpP=", DoubleToString(D0010_SafeDiv(cont_ge + 1, InpPermutationIterations + 1), 4));
}

double D0010_BlockContinuationPctSd(const int &labels[], const int n, const int block_size)
{
   if(n <= 0 || block_size <= 1) return 0.0;
   int blocks = (n + block_size - 1) / block_size;
   if(blocks <= 1) return 0.0;
   double sum = 0.0, sum2 = 0.0;
   for(int b = 0; b < blocks; b++)
   {
      int start = b * block_size;
      int end = MathMin(n, start + block_size);
      int cnt = 0, cont = 0;
      for(int i = start; i < end; i++)
      {
         cnt++;
         if(labels[i] == DAL_D0010_LABEL_CONTINUATION) cont++;
      }
      double pct = D0010_SafePct(cont, cnt);
      sum += pct; sum2 += pct * pct;
   }
   double mean = D0010_SafeDiv(sum, blocks);
   return MathSqrt(MathMax(0.0, D0010_SafeDiv(sum2, blocks) - mean * mean));
}

void D0010_PrintBlockConcentrationStress(const int &labels[], const int n)
{
   if(!InpAtomicStressBlockConcentration || n < 20 || InpPermutationIterations <= 0)
      return;
   int bs = MathMax(5, InpAtomicBlockSizeMain);
   double obs = D0010_BlockContinuationPctSd(labels, n, bs);
   double sum = 0.0, sum2 = 0.0;
   int ge = 0;
   int shuffled[];
   for(int iter = 0; iter < InpPermutationIterations; iter++)
   {
      D0010_ShuffleLabels(labels, n, iter + 303, shuffled);
      double sd = D0010_BlockContinuationPctSd(shuffled, n, bs);
      sum += sd; sum2 += sd * sd;
      if(sd >= obs) ge++;
   }
   double it = (double)InpPermutationIterations;
   double mean = D0010_SafeDiv(sum, it);
   double sd0 = MathSqrt(MathMax(0.0, D0010_SafeDiv(sum2, it) - mean * mean));
   Print("DAL_D0010_ATOMIC_BLOCK_CONCENTRATION_STRESS",
      " *** build=", DAL_D0010_BUILD,
      "*contract=atomic_no_sample_raw_m0001_known_time_batches",
      "*n=", n,
      "*blockSize=", bs,
      "*blocks=", ((n + bs - 1) / bs),
      "*iters=", InpPermutationIterations,
      "*obsContinuationPctSd=", DoubleToString(obs, 4),
      "*shuffleMeanPctSd=", DoubleToString(mean, 4),
      "*shuffleSdPctSd=", DoubleToString(sd0, 4),
      "*pctSdZ=", DoubleToString(D0010_SafeDiv(obs - mean, sd0), 4),
      "*pctSdEmpP=", DoubleToString(D0010_SafeDiv(ge + 1, InpPermutationIterations + 1), 4));
}

void D0010_PrintCircularShiftStress(const int &labels[], const int n, const D0010TransitionStats &obs)
{
   if(!InpAtomicStressCircularShift || n < 20 || InpPermutationIterations <= 0)
      return;
   int min_shift = MathMax(2, InpAtomicCircularMinShiftBatches);
   if(min_shift >= n) min_shift = MathMax(2, n / 4);
   double sum = 0.0, sum2 = 0.0;
   int ge = 0;
   for(int iter = 0; iter < InpPermutationIterations; iter++)
   {
      int range = MathMax(1, n - min_shift);
      int shift = min_shift + (int)MathFloor(D0010_Rand01(iter, 17, 909) * range);
      if(shift <= 0) shift = min_shift;
      if(shift >= n) shift = n - 1;
      double corr = 0.0;
      double sx = 0.0, sy = 0.0, sxx = 0.0, syy = 0.0, sxy = 0.0;
      for(int i = 0; i < n; i++)
      {
         double x = D0010_LabelValue(labels[i]);
         double y = D0010_LabelValue(labels[(i + shift) % n]);
         sx += x; sy += y; sxx += x * x; syy += y * y; sxy += x * y;
      }
      double den = MathSqrt((n * sxx - sx * sx) * (n * syy - sy * sy));
      corr = D0010_SafeDiv(n * sxy - sx * sy, den);
      sum += corr; sum2 += corr * corr;
      if(corr >= obs.lag1_corr) ge++;
   }
   double it = (double)InpPermutationIterations;
   double mean = D0010_SafeDiv(sum, it);
   double sd = MathSqrt(MathMax(0.0, D0010_SafeDiv(sum2, it) - mean * mean));
   Print("DAL_D0010_ATOMIC_CIRCULAR_SHIFT_STRESS",
      " *** build=", DAL_D0010_BUILD,
      "*contract=atomic_no_sample_raw_m0001_known_time_batches",
      "*n=", n,
      "*iters=", InpPermutationIterations,
      "*minShift=", min_shift,
      "*obsLag1Corr=", DoubleToString(obs.lag1_corr, 4),
      "*shiftMeanCorr=", DoubleToString(mean, 4),
      "*shiftSdCorr=", DoubleToString(sd, 4),
      "*lag1Z=", DoubleToString(D0010_SafeDiv(obs.lag1_corr - mean, sd), 4),
      "*lag1EmpP=", DoubleToString(D0010_SafeDiv(ge + 1, InpPermutationIterations + 1), 4));
}

void D0010_LocalBlockShuffle(const int &src[], const int n, const int block_size, const int iter, int &dst[])
{
   ArrayResize(dst, n);
   for(int i = 0; i < n; i++) dst[i] = src[i];
   int bs = MathMax(2, block_size);
   for(int start = 0; start < n; start += bs)
   {
      int end = MathMin(n, start + bs);
      for(int j = end - 1; j > start; j--)
      {
         int k = start + (int)MathFloor(D0010_Rand01(iter, j, 707) * (j - start + 1));
         if(k < start) k = start;
         if(k > j) k = j;
         int tmp = dst[j]; dst[j] = dst[k]; dst[k] = tmp;
      }
   }
}

void D0010_PrintLocalBlockShuffleStress(const int &labels[], const int n, const D0010TransitionStats &obs)
{
   if(!InpAtomicStressLocalBlockShuffle || n < 20 || InpPermutationIterations <= 0)
      return;
   int bs = MathMax(5, InpAtomicLocalBlockShuffleSize);
   double lift_sum = 0.0, lift_sum2 = 0.0;
   double lag_sum = 0.0, lag_sum2 = 0.0;
   int lift_ge = 0, lag_ge = 0;
   int shuffled[];
   for(int iter = 0; iter < InpPermutationIterations; iter++)
   {
      D0010_LocalBlockShuffle(labels, n, bs, iter + 808, shuffled);
      D0010TransitionStats ts;
      D0010_ComputeTransitionStats(shuffled, n, ts);
      lift_sum += ts.same_lift_pct; lift_sum2 += ts.same_lift_pct * ts.same_lift_pct;
      lag_sum += ts.lag1_corr; lag_sum2 += ts.lag1_corr * ts.lag1_corr;
      if(ts.same_lift_pct >= obs.same_lift_pct) lift_ge++;
      if(ts.lag1_corr >= obs.lag1_corr) lag_ge++;
   }
   double it = (double)InpPermutationIterations;
   double lift_mean = D0010_SafeDiv(lift_sum, it);
   double lag_mean = D0010_SafeDiv(lag_sum, it);
   double lift_sd = MathSqrt(MathMax(0.0, D0010_SafeDiv(lift_sum2, it) - lift_mean * lift_mean));
   double lag_sd = MathSqrt(MathMax(0.0, D0010_SafeDiv(lag_sum2, it) - lag_mean * lag_mean));
   Print("DAL_D0010_ATOMIC_LOCAL_BLOCK_SHUFFLE_STRESS",
      " *** build=", DAL_D0010_BUILD,
      "*contract=atomic_no_sample_raw_m0001_known_time_batches",
      "*n=", n,
      "*blockSize=", bs,
      "*iters=", InpPermutationIterations,
      "*obsSameLiftPct=", DoubleToString(obs.same_lift_pct, 2),
      "*blockNullMeanSameLiftPct=", DoubleToString(lift_mean, 2),
      "*blockNullSdSameLiftPct=", DoubleToString(lift_sd, 2),
      "*sameLiftZ=", DoubleToString(D0010_SafeDiv(obs.same_lift_pct - lift_mean, lift_sd), 4),
      "*sameLiftEmpP=", DoubleToString(D0010_SafeDiv(lift_ge + 1, InpPermutationIterations + 1), 4),
      "*obsLag1Corr=", DoubleToString(obs.lag1_corr, 4),
      "*blockNullMeanLag1Corr=", DoubleToString(lag_mean, 4),
      "*blockNullSdLag1Corr=", DoubleToString(lag_sd, 4),
      "*lag1Z=", DoubleToString(D0010_SafeDiv(obs.lag1_corr - lag_mean, lag_sd), 4),
      "*lag1EmpP=", DoubleToString(D0010_SafeDiv(lag_ge + 1, InpPermutationIterations + 1), 4));
}

int D0010_RollingContextSignal(const int &labels[], const int index, const int k, const double threshold, double &cont_pct, double &confidence_pct)
{
   cont_pct = 0.0;
   confidence_pct = 0.0;
   int kk = MathMax(1, k);
   int start = MathMax(0, index - kk);
   int cnt = 0, cont = 0;
   for(int i = start; i < index; i++)
   {
      cnt++;
      if(labels[i] == DAL_D0010_LABEL_CONTINUATION) cont++;
   }
   if(cnt <= 0) return DAL_D0010_LABEL_UNKNOWN;
   cont_pct = D0010_SafePct(cont, cnt);
   double p = D0010_SafeDiv(cont, cnt);
   confidence_pct = 100.0 * MathAbs(p - 0.5) * 2.0;
   if(p >= threshold) return DAL_D0010_LABEL_CONTINUATION;
   if(p <= 1.0 - threshold) return DAL_D0010_LABEL_REVERSAL;
   return DAL_D0010_LABEL_UNKNOWN;
}

int D0010_EwmaContextSignal(const int &labels[], const int index, const double alpha, const double threshold, double &cont_pct, double &confidence_pct)
{
   cont_pct = 0.0;
   confidence_pct = 0.0;
   if(index <= 0) return DAL_D0010_LABEL_UNKNOWN;
   double a = alpha;
   if(a <= 0.0) a = 0.35;
   if(a >= 1.0) a = 0.99;
   double ew = D0010_LabelValue(labels[0]);
   for(int i = 1; i < index; i++)
      ew = a * D0010_LabelValue(labels[i]) + (1.0 - a) * ew;
   cont_pct = 100.0 * ew;
   confidence_pct = 100.0 * MathAbs(ew - 0.5) * 2.0;
   if(ew >= threshold) return DAL_D0010_LABEL_CONTINUATION;
   if(ew <= 1.0 - threshold) return DAL_D0010_LABEL_REVERSAL;
   return DAL_D0010_LABEL_UNKNOWN;
}


double D0010_ContextFollowPct(const int &labels[], const int n, const int k, const bool ewma)
{
   if(n < 3) return 0.0;
   int dominant = 0, follow = 0;
   double threshold = InpAtomicContextStrongThreshold;
   if(threshold < 0.51) threshold = 0.51;
   if(threshold > 0.95) threshold = 0.95;
   for(int i = 1; i < n; i++)
   {
      double cont_pct = 0.0, conf_pct = 0.0;
      int sig = (ewma ? D0010_EwmaContextSignal(labels, i, InpAtomicContextEwmaAlpha, threshold, cont_pct, conf_pct)
                      : D0010_RollingContextSignal(labels, i, k, threshold, cont_pct, conf_pct));
      if(sig == DAL_D0010_LABEL_UNKNOWN)
         continue;
      dominant++;
      if(sig == labels[i]) follow++;
   }
   return D0010_SafePct(follow, dominant);
}

void D0010_PrintContextShuffleStress(const int &labels[], const int n)
{
   if(!InpAtomicStressContextShuffle || !InpAtomicPrintHumanContextReport || n < 10 || InpPermutationIterations <= 0)
      return;
   int k = MathMax(1, InpAtomicContextKMain);
   double obs_roll = D0010_ContextFollowPct(labels, n, k, false);
   double obs_ewma = D0010_ContextFollowPct(labels, n, k, true);
   double sum_r = 0.0, sum2_r = 0.0, sum_e = 0.0, sum2_e = 0.0;
   int ge_r = 0, ge_e = 0;
   int shuffled[];
   for(int iter = 0; iter < InpPermutationIterations; iter++)
   {
      D0010_ShuffleLabels(labels, n, iter + 404, shuffled);
      double r = D0010_ContextFollowPct(shuffled, n, k, false);
      double e = D0010_ContextFollowPct(shuffled, n, k, true);
      sum_r += r; sum2_r += r * r;
      sum_e += e; sum2_e += e * e;
      if(r >= obs_roll) ge_r++;
      if(e >= obs_ewma) ge_e++;
   }
   double it = (double)InpPermutationIterations;
   double mr = D0010_SafeDiv(sum_r, it);
   double me = D0010_SafeDiv(sum_e, it);
   double sr = MathSqrt(MathMax(0.0, D0010_SafeDiv(sum2_r, it) - mr * mr));
   double se = MathSqrt(MathMax(0.0, D0010_SafeDiv(sum2_e, it) - me * me));
   Print("DAL_D0010_ATOMIC_CONTEXT_SHUFFLE_STRESS",
      " *** build=", DAL_D0010_BUILD,
      "*contract=atomic_no_sample_raw_m0001_known_time_batches",
      "*null=label_shuffle_over_pure_known_time_batches",
      "*n=", n,
      "*iters=", InpPermutationIterations,
      "*k=", k,
      "*alpha=", DoubleToString(InpAtomicContextEwmaAlpha, 4),
      "*threshold=", DoubleToString(InpAtomicContextStrongThreshold, 4),
      "*obsRollingFollowPct=", DoubleToString(obs_roll, 2),
      "*nullRollingMeanFollowPct=", DoubleToString(mr, 2),
      "*nullRollingSdFollowPct=", DoubleToString(sr, 2),
      "*rollingFollowZ=", DoubleToString(D0010_SafeDiv(obs_roll - mr, sr), 4),
      "*rollingEmpP=", DoubleToString(D0010_SafeDiv(ge_r + 1, InpPermutationIterations + 1), 4),
      "*obsEwmaFollowPct=", DoubleToString(obs_ewma, 2),
      "*nullEwmaMeanFollowPct=", DoubleToString(me, 2),
      "*nullEwmaSdFollowPct=", DoubleToString(se, 2),
      "*ewmaFollowZ=", DoubleToString(D0010_SafeDiv(obs_ewma - me, se), 4),
      "*ewmaEmpP=", DoubleToString(D0010_SafeDiv(ge_e + 1, InpPermutationIterations + 1), 4));
}

void D0010_PrintHumanContextState(const int &labels[], const int n, const string method, const int k, const bool ewma)
{
   if(!InpAtomicPrintHumanContextReport || n < 3)
      return;
   int evaluated = 0, dominant = 0, neutral = 0, rev_ctx = 0, cont_ctx = 0;
   int follow = 0, sw = 0, rev_follow = 0, rev_total = 0, cont_follow = 0, cont_total = 0;
   double mean_cont = 0.0, mean_conf = 0.0;
   double threshold = InpAtomicContextStrongThreshold;
   if(threshold < 0.51) threshold = 0.51;
   if(threshold > 0.95) threshold = 0.95;
   for(int i = 1; i < n; i++)
   {
      double cont_pct = 0.0, conf_pct = 0.0;
      int sig = (ewma ? D0010_EwmaContextSignal(labels, i, InpAtomicContextEwmaAlpha, threshold, cont_pct, conf_pct)
                      : D0010_RollingContextSignal(labels, i, k, threshold, cont_pct, conf_pct));
      evaluated++;
      mean_cont += cont_pct;
      mean_conf += conf_pct;
      if(sig == DAL_D0010_LABEL_UNKNOWN)
      {
         neutral++;
         continue;
      }
      dominant++;
      if(sig == DAL_D0010_LABEL_REVERSAL) rev_ctx++;
      if(sig == DAL_D0010_LABEL_CONTINUATION) cont_ctx++;
      if(sig == labels[i])
      {
         follow++;
         if(sig == DAL_D0010_LABEL_REVERSAL) rev_follow++;
         if(sig == DAL_D0010_LABEL_CONTINUATION) cont_follow++;
      }
      else sw++;
      if(sig == DAL_D0010_LABEL_REVERSAL) rev_total++;
      if(sig == DAL_D0010_LABEL_CONTINUATION) cont_total++;
   }
   double global_cont_pct = D0010_SafePct(0,1);
   int cont_count = 0;
   for(int z = 0; z < n; z++) if(labels[z] == DAL_D0010_LABEL_CONTINUATION) cont_count++;
   global_cont_pct = D0010_SafePct(cont_count, n);
   double expected = 0.0;
   if(dominant > 0)
   {
      double sig_cont = D0010_SafeDiv(cont_ctx, dominant);
      double sig_rev = D0010_SafeDiv(rev_ctx, dominant);
      double base_cont = D0010_SafeDiv(cont_count, n);
      double base_rev = 1.0 - base_cont;
      expected = 100.0 * (sig_cont * base_cont + sig_rev * base_rev);
   }
   Print("DAL_D0010_ATOMIC_HUMAN_CONTEXT_STATE",
      " *** build=", DAL_D0010_BUILD,
      "*contract=atomic_no_sample_raw_m0001_known_time_batches",
      "*method=", method,
      "*k=", k,
      "*alpha=", DoubleToString(InpAtomicContextEwmaAlpha, 4),
      "*threshold=", DoubleToString(threshold, 4),
      "*n=", n,
      "*evaluated=", evaluated,
      "*dominantN=", dominant,
      "*neutralN=", neutral,
      "*revContextN=", rev_ctx,
      "*contContextN=", cont_ctx,
      "*globalContPct=", DoubleToString(global_cont_pct, 2),
      "*meanContextContPct=", DoubleToString(D0010_SafeDiv(mean_cont, evaluated), 2),
      "*meanConfidencePct=", DoubleToString(D0010_SafeDiv(mean_conf, evaluated), 2),
      "*dominantFollowPct=", DoubleToString(D0010_SafePct(follow, dominant), 2),
      "*dominantSwitchPct=", DoubleToString(D0010_SafePct(sw, dominant), 2),
      "*expectedFollowPct=", DoubleToString(expected, 2),
      "*dominantLiftPct=", DoubleToString(D0010_SafePct(follow, dominant) - expected, 2),
      "*revContextNextRevPct=", DoubleToString(D0010_SafePct(rev_follow, rev_total), 2),
      "*contContextNextContPct=", DoubleToString(D0010_SafePct(cont_follow, cont_total), 2));
}

void D0010_PrintLastOnlyQuality(const int &labels[], const int n)
{
   if(!InpAtomicPrintHumanContextReport || n < 2)
      return;
   int follow = 0, sw = 0, rev_sig = 0, cont_sig = 0, rev_follow = 0, cont_follow = 0;
   for(int i = 1; i < n; i++)
   {
      int sig = labels[i - 1];
      if(sig == DAL_D0010_LABEL_REVERSAL) rev_sig++;
      if(sig == DAL_D0010_LABEL_CONTINUATION) cont_sig++;
      if(sig == labels[i])
      {
         follow++;
         if(sig == DAL_D0010_LABEL_REVERSAL) rev_follow++;
         if(sig == DAL_D0010_LABEL_CONTINUATION) cont_follow++;
      }
      else sw++;
   }
   Print("DAL_D0010_ATOMIC_LAST_ONLY_QUALITY",
      " *** build=", DAL_D0010_BUILD,
      "*contract=atomic_no_sample_raw_m0001_known_time_batches",
      "*n=", n,
      "*signalN=", MathMax(0, n - 1),
      "*followN=", follow,
      "*switchN=", sw,
      "*followPct=", DoubleToString(D0010_SafePct(follow, n - 1), 2),
      "*switchPct=", DoubleToString(D0010_SafePct(sw, n - 1), 2),
      "*revSignalN=", rev_sig,
      "*contSignalN=", cont_sig,
      "*revNextRevPct=", DoubleToString(D0010_SafePct(rev_follow, rev_sig), 2),
      "*contNextContPct=", DoubleToString(D0010_SafePct(cont_follow, cont_sig), 2));
}


// -----------------------------------------------------------------------------
// Deep atomic diagnostics: information, run tails, batch intensity, and H6
// optionality/explosive-power metrics. These reports use only pure known-time
// batches; no M0002 samples and no same-candle internal ordering are introduced.
// -----------------------------------------------------------------------------

void D0010_SortDoubleArray(double &a[], const int n)
{
   if(n <= 1) return;
   // MQL5 built-in sort is much faster than the old insertion sort for H6 tail stats.
   ArraySort(a);
}

double D0010_QuantileFromSorted(const double &x[], const int n, const double q)
{
   if(n <= 0) return 0.0;
   double qq = q;
   if(qq < 0.0) qq = 0.0;
   if(qq > 1.0) qq = 1.0;
   double pos = qq * (n - 1);
   int lo = (int)MathFloor(pos);
   int hi = (int)MathCeil(pos);
   if(lo < 0) lo = 0;
   if(hi >= n) hi = n - 1;
   if(lo == hi) return x[lo];
   double w = pos - lo;
   return x[lo] * (1.0 - w) + x[hi] * w;
}

double D0010_QuantileOfValues(double &src[], const int n, const double q)
{
   if(n <= 0) return 0.0;
   double x[];
   ArrayResize(x, n);
   for(int i = 0; i < n; i++) x[i] = src[i];
   D0010_SortDoubleArray(x, n);
   return D0010_QuantileFromSorted(x, n, q);
}

double D0010_Log2(const double x)
{
   if(x <= 0.0) return 0.0;
   return MathLog(x) / MathLog(2.0);
}

void D0010_PrintInformationMetrics(const int &labels[], const int n, const D0010TransitionStats &ts)
{
   if(!InpAtomicPrintDeepReport || n < 3 || ts.transitions <= 0)
      return;

   double p_rev = D0010_SafeDiv(ts.reversal_count, n);
   double p_cont = D0010_SafeDiv(ts.continuation_count, n);
   double entropy = 0.0;
   if(p_rev > 0.0) entropy -= p_rev * D0010_Log2(p_rev);
   if(p_cont > 0.0) entropy -= p_cont * D0010_Log2(p_cont);

   double tr = (double)ts.transitions;
   int m[2][2];
   m[0][0] = ts.rr; m[0][1] = ts.rc; m[1][0] = ts.cr; m[1][1] = ts.cc;
   double row[2]; row[0] = (double)(ts.rr + ts.rc); row[1] = (double)(ts.cr + ts.cc);
   double col[2]; col[0] = (double)(ts.rr + ts.cr); col[1] = (double)(ts.rc + ts.cc);
   double mi_bits = 0.0;
   double chi2 = 0.0;
   for(int r = 0; r < 2; r++)
   {
      for(int c = 0; c < 2; c++)
      {
         double obs = (double)m[r][c];
         double expv = D0010_SafeDiv(row[r] * col[c], tr);
         if(obs > 0.0 && expv > 0.0)
            mi_bits += D0010_SafeDiv(obs, tr) * D0010_Log2(D0010_SafeDiv(obs * tr, row[r] * col[c]));
         if(expv > 0.0)
            chi2 += (obs - expv) * (obs - expv) / expv;
      }
   }

   double cond_entropy = MathMax(0.0, entropy - mi_bits);
   double predictability_gain_pct = D0010_SafePct(mi_bits, entropy);
   double odds_ratio = D0010_SafeDiv((double)ts.rr * (double)ts.cc, (double)ts.rc * (double)ts.cr);
   double yule_q = D0010_SafeDiv((double)ts.rr * (double)ts.cc - (double)ts.rc * (double)ts.cr,
                                 (double)ts.rr * (double)ts.cc + (double)ts.rc * (double)ts.cr);

   Print("DAL_D0010_ATOMIC_INFORMATION",
      " *** build=", DAL_D0010_BUILD,
      "*contract=atomic_no_sample_raw_m0001_known_time_batches",
      "*n=", n,
      "*labelEntropyBits=", DoubleToString(entropy, 6),
      "*conditionalEntropyBits=", DoubleToString(cond_entropy, 6),
      "*mutualInformationBits=", DoubleToString(mi_bits, 6),
      "*predictabilityGainPct=", DoubleToString(predictability_gain_pct, 2),
      "*markovChi2=", DoubleToString(chi2, 4),
      "*oddsRatio=", DoubleToString(odds_ratio, 4),
      "*yuleQ=", DoubleToString(yule_q, 4),
      "*pRev=", DoubleToString(ts.reversal_pct, 2),
      "*pCont=", DoubleToString(ts.continuation_pct, 2),
      "*interpretation=lag1_markov_information_over_known_time_batches");
}

void D0010_PrintRunDistributionMetrics(const int &labels[], const int n)
{
   if(!InpAtomicPrintDeepReport || n <= 0)
      return;

   double all_runs[], rev_runs[], cont_runs[];
   int all_n = 0, rev_n = 0, cont_n = 0;
   int cur_label = labels[0];
   int cur_len = 1;
   int rev_len5_batches = 0, cont_len5_batches = 0;
   int rev_len10_batches = 0, cont_len10_batches = 0;

   for(int i = 1; i <= n; i++)
   {
      if(i < n && labels[i] == cur_label)
      {
         cur_len++;
         continue;
      }

      ArrayResize(all_runs, all_n + 1);
      all_runs[all_n++] = (double)cur_len;
      if(cur_label == DAL_D0010_LABEL_REVERSAL)
      {
         ArrayResize(rev_runs, rev_n + 1);
         rev_runs[rev_n++] = (double)cur_len;
         if(cur_len >= 5) rev_len5_batches += cur_len;
         if(cur_len >= 10) rev_len10_batches += cur_len;
      }
      else if(cur_label == DAL_D0010_LABEL_CONTINUATION)
      {
         ArrayResize(cont_runs, cont_n + 1);
         cont_runs[cont_n++] = (double)cur_len;
         if(cur_len >= 5) cont_len5_batches += cur_len;
         if(cur_len >= 10) cont_len10_batches += cur_len;
      }

      if(i < n)
      {
         cur_label = labels[i];
         cur_len = 1;
      }
   }

   int rev_total = 0, cont_total = 0;
   for(int z = 0; z < n; z++)
   {
      if(labels[z] == DAL_D0010_LABEL_REVERSAL) rev_total++;
      if(labels[z] == DAL_D0010_LABEL_CONTINUATION) cont_total++;
   }

   Print("DAL_D0010_ATOMIC_RUN_DISTRIBUTION",
      " *** build=", DAL_D0010_BUILD,
      "*contract=atomic_no_sample_raw_m0001_known_time_batches",
      "*n=", n,
      "*allRuns=", all_n,
      "*allP50=", DoubleToString(D0010_QuantileOfValues(all_runs, all_n, 0.50), 2),
      "*allP75=", DoubleToString(D0010_QuantileOfValues(all_runs, all_n, 0.75), 2),
      "*allP90=", DoubleToString(D0010_QuantileOfValues(all_runs, all_n, 0.90), 2),
      "*allP95=", DoubleToString(D0010_QuantileOfValues(all_runs, all_n, 0.95), 2),
      "*revRuns=", rev_n,
      "*revP50=", DoubleToString(D0010_QuantileOfValues(rev_runs, rev_n, 0.50), 2),
      "*revP75=", DoubleToString(D0010_QuantileOfValues(rev_runs, rev_n, 0.75), 2),
      "*revP90=", DoubleToString(D0010_QuantileOfValues(rev_runs, rev_n, 0.90), 2),
      "*revP95=", DoubleToString(D0010_QuantileOfValues(rev_runs, rev_n, 0.95), 2),
      "*contRuns=", cont_n,
      "*contP50=", DoubleToString(D0010_QuantileOfValues(cont_runs, cont_n, 0.50), 2),
      "*contP75=", DoubleToString(D0010_QuantileOfValues(cont_runs, cont_n, 0.75), 2),
      "*contP90=", DoubleToString(D0010_QuantileOfValues(cont_runs, cont_n, 0.90), 2),
      "*contP95=", DoubleToString(D0010_QuantileOfValues(cont_runs, cont_n, 0.95), 2),
      "*revBatchesInsideRun5PlusPct=", DoubleToString(D0010_SafePct(rev_len5_batches, rev_total), 2),
      "*contBatchesInsideRun5PlusPct=", DoubleToString(D0010_SafePct(cont_len5_batches, cont_total), 2),
      "*revBatchesInsideRun10PlusPct=", DoubleToString(D0010_SafePct(rev_len10_batches, rev_total), 2),
      "*contBatchesInsideRun10PlusPct=", DoubleToString(D0010_SafePct(cont_len10_batches, cont_total), 2));
}

void D0010_PrintBatchIntensityMetrics(const int &labels[], const int &counts[], const int &dirs[], const int n)
{
   if(!InpAtomicPrintDeepReport || n <= 0)
      return;
   double rev_counts[], cont_counts[];
   int rev_n = 0, cont_n = 0, rev_multi = 0, cont_multi = 0, rev_big = 0, cont_big = 0;
   int rev_buy = 0, rev_sell = 0, cont_buy = 0, cont_sell = 0, rev_dir0 = 0, cont_dir0 = 0;
   double rev_sum = 0.0, cont_sum = 0.0;
   for(int i = 0; i < n; i++)
   {
      if(labels[i] == DAL_D0010_LABEL_REVERSAL)
      {
         ArrayResize(rev_counts, rev_n + 1); rev_counts[rev_n++] = (double)counts[i];
         rev_sum += counts[i];
         if(counts[i] > 1) rev_multi++;
         if(counts[i] >= 3) rev_big++;
         if(dirs[i] > 0) rev_buy++; else if(dirs[i] < 0) rev_sell++; else rev_dir0++;
      }
      else if(labels[i] == DAL_D0010_LABEL_CONTINUATION)
      {
         ArrayResize(cont_counts, cont_n + 1); cont_counts[cont_n++] = (double)counts[i];
         cont_sum += counts[i];
         if(counts[i] > 1) cont_multi++;
         if(counts[i] >= 3) cont_big++;
         if(dirs[i] > 0) cont_buy++; else if(dirs[i] < 0) cont_sell++; else cont_dir0++;
      }
   }
   Print("DAL_D0010_ATOMIC_BATCH_INTENSITY",
      " *** build=", DAL_D0010_BUILD,
      "*contract=atomic_no_sample_raw_m0001_known_time_batches",
      "*n=", n,
      "*revN=", rev_n,
      "*contN=", cont_n,
      "*revMeanEventsPerBatch=", DoubleToString(D0010_SafeDiv(rev_sum, rev_n), 4),
      "*contMeanEventsPerBatch=", DoubleToString(D0010_SafeDiv(cont_sum, cont_n), 4),
      "*revMultiEventBatchPct=", DoubleToString(D0010_SafePct(rev_multi, rev_n), 2),
      "*contMultiEventBatchPct=", DoubleToString(D0010_SafePct(cont_multi, cont_n), 2),
      "*revBigBatch3PlusPct=", DoubleToString(D0010_SafePct(rev_big, rev_n), 2),
      "*contBigBatch3PlusPct=", DoubleToString(D0010_SafePct(cont_big, cont_n), 2),
      "*revEventCountP90=", DoubleToString(D0010_QuantileOfValues(rev_counts, rev_n, 0.90), 2),
      "*contEventCountP90=", DoubleToString(D0010_QuantileOfValues(cont_counts, cont_n, 0.90), 2),
      "*revBuyDirPct=", DoubleToString(D0010_SafePct(rev_buy, rev_n), 2),
      "*revSellDirPct=", DoubleToString(D0010_SafePct(rev_sell, rev_n), 2),
      "*contBuyDirPct=", DoubleToString(D0010_SafePct(cont_buy, cont_n), 2),
      "*contSellDirPct=", DoubleToString(D0010_SafePct(cont_sell, cont_n), 2),
      "*revNoDominantDirPct=", DoubleToString(D0010_SafePct(rev_dir0, rev_n), 2),
      "*contNoDominantDirPct=", DoubleToString(D0010_SafePct(cont_dir0, cont_n), 2));
}

void D0010_PrintDeepReports(const int &labels[], const int &counts[], const int &dirs[], const int n, const D0010TransitionStats &ts)
{
   if(!InpAtomicPrintDeepReport)
      return;
   D0010_PrintInformationMetrics(labels, n, ts);
   D0010_PrintRunDistributionMetrics(labels, n);
   D0010_PrintBatchIntensityMetrics(labels, counts, dirs, n);
}

double D0010_ATRAt(const DALBar &bars[], const int bars_count, const int index, const int period)
{
   if(bars_count <= 1 || index <= 0)
      return 0.0;
   int p = MathMax(2, period);
   int start = MathMax(1, index - p + 1);
   double sum = 0.0;
   int n = 0;
   for(int i = start; i <= index && i < bars_count; i++)
   {
      double tr1 = bars[i].high - bars[i].low;
      double tr2 = MathAbs(bars[i].high - bars[i - 1].close);
      double tr3 = MathAbs(bars[i].low - bars[i - 1].close);
      double tr = MathMax(tr1, MathMax(tr2, tr3));
      sum += tr;
      n++;
   }
   return D0010_SafeDiv(sum, n);
}

struct D0010ValueStats
{
   int n;
   double mean;
   double median;
   double p75;
   double p90;
   double p95;
   double p99;
   double maxv;
   double hit1;
   double hit2;
   double hit3;
   double top10_share;
};

void D0010_ComputeValueStats(const double &values[], const int &labels[], const int n, const int wanted, const double t1, const double t2, const double t3, D0010ValueStats &st)
{
   st.n = 0; st.mean = 0.0; st.median = 0.0; st.p75 = 0.0; st.p90 = 0.0; st.p95 = 0.0; st.p99 = 0.0; st.maxv = 0.0; st.hit1 = 0.0; st.hit2 = 0.0; st.hit3 = 0.0; st.top10_share = 0.0;
   double x[];
   ArrayResize(x, n);
   int m = 0, h1 = 0, h2 = 0, h3 = 0;
   double sum = 0.0;
   for(int i = 0; i < n; i++)
   {
      if(labels[i] != wanted) continue;
      x[m] = values[i];
      sum += values[i];
      if(values[i] > st.maxv) st.maxv = values[i];
      if(values[i] >= t1) h1++;
      if(values[i] >= t2) h2++;
      if(values[i] >= t3) h3++;
      m++;
   }
   st.n = m;
   if(m <= 0) return;
   if(m < n) ArrayResize(x, m);
   st.mean = D0010_SafeDiv(sum, m);
   D0010_SortDoubleArray(x, m);
   st.median = D0010_QuantileFromSorted(x, m, 0.50);
   st.p75 = D0010_QuantileFromSorted(x, m, 0.75);
   st.p90 = D0010_QuantileFromSorted(x, m, 0.90);
   st.p95 = D0010_QuantileFromSorted(x, m, 0.95);
   st.p99 = D0010_QuantileFromSorted(x, m, 0.99);
   st.hit1 = D0010_SafePct(h1, m);
   st.hit2 = D0010_SafePct(h2, m);
   st.hit3 = D0010_SafePct(h3, m);
   int tail_start = (int)MathFloor(0.90 * m);
   if(tail_start < 0) tail_start = 0;
   if(tail_start >= m) tail_start = m - 1;
   double tail_sum = 0.0;
   for(int j = tail_start; j < m; j++) tail_sum += x[j];
   st.top10_share = D0010_SafePct(tail_sum, sum);
}


void D0010_H6FastMeanHitDiff(const double &values[], const int &labels[], const int n, const double hit_thr, double &mean_diff, double &hit_diff)
{
   double rsum = 0.0, csum = 0.0;
   int rn = 0, cn = 0, rh = 0, ch = 0;
   for(int i = 0; i < n; i++)
   {
      if(labels[i] == DAL_D0010_LABEL_REVERSAL)
      {
         rsum += values[i];
         rn++;
         if(values[i] >= hit_thr) rh++;
      }
      else if(labels[i] == DAL_D0010_LABEL_CONTINUATION)
      {
         csum += values[i];
         cn++;
         if(values[i] >= hit_thr) ch++;
      }
   }
   mean_diff = D0010_SafeDiv(rsum, rn) - D0010_SafeDiv(csum, cn);
   hit_diff = D0010_SafePct(rh, rn) - D0010_SafePct(ch, cn);
}

void D0010_H6OptionalityForHorizon(const DALBar &bars[], const int bars_count, const int horizon, const string tag)
{
   if(!InpAtomicPrintH6OptionalityReport)
      return;
   int n = ArraySize(g_labels);
   if(n <= 0 || bars_count <= 0 || horizon <= 0)
      return;

   Print("DAL_H0006_PROGRESS_", tag, " *** build=", DAL_D0010_BUILD,
      "*stage=start_horizon_measurement",
      "*engine=CANDLE_FORWARD_STREAM",
      "*horizonBars=", horizon,
      "*labels=", n,
      "*bars=", bars_count,
      "*statsSort=single_builtin_sort_per_series");

   double absv[], dirv[], advv[];
   int valid_labels[];
   int m = 0;
   for(int i = 0; i < n; i++)
   {
      int k = g_label_known_indices[i];
      if(k < 1 || k + 1 >= bars_count) continue;
      int end = MathMin(bars_count - 1, k + horizon);
      if(end <= k) continue;
      double atr = D0010_ATRAt(bars, bars_count, k, InpH6AtrPeriod);
      if(atr <= 0.0) continue;
      int start = k + 1;
      double entry = (InpH6EntryAnchorMode == 1 ? bars[start].open : bars[k].close);
      double hi = bars[start].high;
      double lo = bars[start].low;
      for(int j = start; j <= end; j++)
      {
         if(bars[j].high > hi) hi = bars[j].high;
         if(bars[j].low < lo) lo = bars[j].low;
      }
      double up = MathMax(0.0, hi - entry) / atr;
      double dn = MathMax(0.0, entry - lo) / atr;
      double absx = MathMax(up, dn);
      int d = g_label_dirs[i];
      double dirx = absx;
      double advx = MathMin(up, dn);
      if(d > 0)
      {
         dirx = up;
         advx = dn;
      }
      else if(d < 0)
      {
         dirx = dn;
         advx = up;
      }
      ArrayResize(absv, m + 1); ArrayResize(dirv, m + 1); ArrayResize(advv, m + 1); ArrayResize(valid_labels, m + 1);
      absv[m] = absx;
      dirv[m] = dirx;
      advv[m] = advx;
      valid_labels[m] = g_labels[i];
      m++;
   }

   if(InpH6PrintComputeAudit)
   {
      string audit_line = "DAL_H0006_COMPUTE_AUDIT_" + tag
         + " *** build=" + DAL_D0010_BUILD
         + "*contract=atomic_no_sample_known_time_batches_future_excursion_only_after_known_time"
         + "*horizonBars=" + IntegerToString(horizon)
         + "*validN=" + IntegerToString(m)
         + "*entryAnchor=" + (InpH6EntryAnchorMode == 1 ? "NEXT_OPEN" : "KNOWN_CLOSE")
         + "*futureWindow=start_after_known_batch"
         + "*measurement=one_pass_cached_for_optionality_and_edge_map";
      Print(audit_line);
   }

   D0010ValueStats rev_abs, cont_abs, rev_dir, cont_dir, rev_adv, cont_adv;
   D0010_ComputeValueStats(absv, valid_labels, m, DAL_D0010_LABEL_REVERSAL, InpH6TailAtr1, InpH6TailAtr2, InpH6TailAtr3, rev_abs);
   D0010_ComputeValueStats(absv, valid_labels, m, DAL_D0010_LABEL_CONTINUATION, InpH6TailAtr1, InpH6TailAtr2, InpH6TailAtr3, cont_abs);
   D0010_ComputeValueStats(dirv, valid_labels, m, DAL_D0010_LABEL_REVERSAL, InpH6TailAtr1, InpH6TailAtr2, InpH6TailAtr3, rev_dir);
   D0010_ComputeValueStats(dirv, valid_labels, m, DAL_D0010_LABEL_CONTINUATION, InpH6TailAtr1, InpH6TailAtr2, InpH6TailAtr3, cont_dir);
   D0010_ComputeValueStats(advv, valid_labels, m, DAL_D0010_LABEL_REVERSAL, InpH6TailAtr1, InpH6TailAtr2, InpH6TailAtr3, rev_adv);
   D0010_ComputeValueStats(advv, valid_labels, m, DAL_D0010_LABEL_CONTINUATION, InpH6TailAtr1, InpH6TailAtr2, InpH6TailAtr3, cont_adv);

   string verdict = "mixed_optional_tail";
   if(rev_abs.p95 > cont_abs.p95 && rev_abs.hit2 > cont_abs.hit2) verdict = "reversal_tail_dominates";
   else if(cont_abs.p95 > rev_abs.p95 && cont_abs.hit2 > rev_abs.hit2) verdict = "continuation_tail_dominates";

   string optionality_line = "DAL_H0006_OPTIONALITY_" + tag
      + " *** build=" + DAL_D0010_BUILD
      + "*hypothesis=H0006_REVERSAL_EXPLOSIVE_OPTIONALITY"
      + "*contract=atomic_no_sample_known_time_batches_future_excursion_only_after_known_time"
      + "*horizonBars=" + IntegerToString(horizon)
      + "*atrPeriod=" + IntegerToString((int)MathMax(2, InpH6AtrPeriod))
      + "*tailAtr1=" + DoubleToString(InpH6TailAtr1, 2)
      + "*tailAtr2=" + DoubleToString(InpH6TailAtr2, 2)
      + "*tailAtr3=" + DoubleToString(InpH6TailAtr3, 2)
      + "*validN=" + IntegerToString(m)
      + "*revN=" + IntegerToString(rev_abs.n)
      + "*contN=" + IntegerToString(cont_abs.n)
      + "*revAbsMeanATR=" + DoubleToString(rev_abs.mean, 4)
      + "*contAbsMeanATR=" + DoubleToString(cont_abs.mean, 4)
      + "*revMinusContAbsMeanATR=" + DoubleToString(rev_abs.mean - cont_abs.mean, 4)
      + "*revAbsP90ATR=" + DoubleToString(rev_abs.p90, 4)
      + "*contAbsP90ATR=" + DoubleToString(cont_abs.p90, 4)
      + "*revAbsP95ATR=" + DoubleToString(rev_abs.p95, 4)
      + "*contAbsP95ATR=" + DoubleToString(cont_abs.p95, 4)
      + "*revAbsP99ATR=" + DoubleToString(rev_abs.p99, 4)
      + "*contAbsP99ATR=" + DoubleToString(cont_abs.p99, 4)
      + "*revHitTail1Pct=" + DoubleToString(rev_abs.hit1, 2)
      + "*contHitTail1Pct=" + DoubleToString(cont_abs.hit1, 2)
      + "*revHitTail2Pct=" + DoubleToString(rev_abs.hit2, 2)
      + "*contHitTail2Pct=" + DoubleToString(cont_abs.hit2, 2)
      + "*revHitTail3Pct=" + DoubleToString(rev_abs.hit3, 2)
      + "*contHitTail3Pct=" + DoubleToString(cont_abs.hit3, 2)
      + "*revTop10SharePct=" + DoubleToString(rev_abs.top10_share, 2)
      + "*contTop10SharePct=" + DoubleToString(cont_abs.top10_share, 2)
      + "*revDirectionalMfeMeanATR=" + DoubleToString(rev_dir.mean, 4)
      + "*contDirectionalMfeMeanATR=" + DoubleToString(cont_dir.mean, 4)
      + "*revAdverseMeanATR=" + DoubleToString(rev_adv.mean, 4)
      + "*contAdverseMeanATR=" + DoubleToString(cont_adv.mean, 4)
      + "*optionalityRatioP95=" + DoubleToString(D0010_SafeDiv(rev_abs.p95, cont_abs.p95), 4)
      + "*verdict=" + verdict;
   Print(optionality_line);

   if(InpAtomicStressH6Optionality && InpPermutationIterations > 0 && InpH6StressMode > 0)
   {
      double obs_mean_diff = rev_abs.mean - cont_abs.mean;
      double obs_hit2_diff = rev_abs.hit2 - cont_abs.hit2;
      double obs_p90_diff = rev_abs.p90 - cont_abs.p90;
      double mean_sum = 0.0, mean_sum2 = 0.0, hit_sum = 0.0, hit_sum2 = 0.0, p90_sum = 0.0, p90_sum2 = 0.0;
      int mean_ge = 0, hit_ge = 0, p90_ge = 0;
      int shuf[];
      for(int iter = 0; iter < InpPermutationIterations; iter++)
      {
         D0010_ShuffleLabels(valid_labels, m, iter + 6001 + horizon, shuf);
         double md = 0.0, hd = 0.0, pd = 0.0;
         D0010_H6FastMeanHitDiff(absv, shuf, m, InpH6TailAtr2, md, hd);
         if(InpH6StressMode >= 2)
         {
            D0010ValueStats sr, sc;
            D0010_ComputeValueStats(absv, shuf, m, DAL_D0010_LABEL_REVERSAL, InpH6TailAtr1, InpH6TailAtr2, InpH6TailAtr3, sr);
            D0010_ComputeValueStats(absv, shuf, m, DAL_D0010_LABEL_CONTINUATION, InpH6TailAtr1, InpH6TailAtr2, InpH6TailAtr3, sc);
            pd = sr.p90 - sc.p90;
         }
         mean_sum += md; mean_sum2 += md * md;
         hit_sum += hd; hit_sum2 += hd * hd;
         p90_sum += pd; p90_sum2 += pd * pd;
         if(md >= obs_mean_diff) mean_ge++;
         if(hd >= obs_hit2_diff) hit_ge++;
         if(InpH6StressMode >= 2 && pd >= obs_p90_diff) p90_ge++;
      }
      double it = (double)InpPermutationIterations;
      double mean_null = D0010_SafeDiv(mean_sum, it);
      double hit_null = D0010_SafeDiv(hit_sum, it);
      double p90_null = D0010_SafeDiv(p90_sum, it);
      double mean_sd = MathSqrt(MathMax(0.0, D0010_SafeDiv(mean_sum2, it) - mean_null * mean_null));
      double hit_sd = MathSqrt(MathMax(0.0, D0010_SafeDiv(hit_sum2, it) - hit_null * hit_null));
      double p90_sd = MathSqrt(MathMax(0.0, D0010_SafeDiv(p90_sum2, it) - p90_null * p90_null));
      string optionality_stress_line = "DAL_H0006_OPTIONALITY_STRESS_" + tag
         + " *** build=" + DAL_D0010_BUILD
         + "*hypothesis=H0006_REVERSAL_EXPLOSIVE_OPTIONALITY"
         + "*null=label_shuffle_over_fixed_known_times_and_fixed_future_excursions"
         + "*stressMode=" + IntegerToString(InpH6StressMode)
         + "*horizonBars=" + IntegerToString(horizon)
         + "*iters=" + IntegerToString(InpPermutationIterations)
         + "*obsRevMinusContMeanAbsATR=" + DoubleToString(obs_mean_diff, 4)
         + "*nullMeanDiff=" + DoubleToString(mean_null, 4)
         + "*nullMeanDiffSd=" + DoubleToString(mean_sd, 4)
         + "*meanDiffZ=" + DoubleToString(D0010_SafeDiv(obs_mean_diff - mean_null, mean_sd), 4)
         + "*meanDiffEmpP=" + DoubleToString(D0010_SafeDiv(mean_ge + 1, InpPermutationIterations + 1), 4)
         + "*obsRevMinusContHitTail2Pct=" + DoubleToString(obs_hit2_diff, 2)
         + "*nullHitTail2Diff=" + DoubleToString(hit_null, 2)
         + "*nullHitTail2DiffSd=" + DoubleToString(hit_sd, 2)
         + "*hitTail2DiffZ=" + DoubleToString(D0010_SafeDiv(obs_hit2_diff - hit_null, hit_sd), 4)
         + "*hitTail2DiffEmpP=" + DoubleToString(D0010_SafeDiv(hit_ge + 1, InpPermutationIterations + 1), 4);
      if(InpH6StressMode >= 2)
      {
         optionality_stress_line += "*obsRevMinusContP90AbsATR=" + DoubleToString(obs_p90_diff, 4)
            + "*nullP90Diff=" + DoubleToString(p90_null, 4)
            + "*nullP90DiffSd=" + DoubleToString(p90_sd, 4)
            + "*p90DiffZ=" + DoubleToString(D0010_SafeDiv(obs_p90_diff - p90_null, p90_sd), 4)
            + "*p90DiffEmpP=" + DoubleToString(D0010_SafeDiv(p90_ge + 1, InpPermutationIterations + 1), 4);
      }
      Print(optionality_stress_line);
   }
}


void D0010_H6CandleStreamForHorizon(const DALBar &bars[], const int bars_count, const int horizon, const string tag)
{
   if(!InpAtomicPrintH6OptionalityReport)
      return;

   int n = ArraySize(g_labels);
   if(n <= 0 || bars_count <= 0 || horizon <= 0)
      return;

   Print("DAL_H0006_PROGRESS_", tag, " *** build=", DAL_D0010_BUILD,
      "*stage=start_horizon_measurement",
      "*engine=CANDLE_FORWARD_STREAM",
      "*horizonBars=", horizon,
      "*labels=", n,
      "*bars=", bars_count,
      "*statsSort=single_builtin_sort_per_series");

   double absv[], dirv[], advv[];
   int valid_labels[];
   ArrayResize(absv, n);
   ArrayResize(dirv, n);
   ArrayResize(advv, n);
   ArrayResize(valid_labels, n);

   int active_label[], active_dir[], active_end[];
   double active_entry[], active_atr[], active_hi[], active_lo[];
   ArrayResize(active_label, n);
   ArrayResize(active_dir, n);
   ArrayResize(active_end, n);
   ArrayResize(active_entry, n);
   ArrayResize(active_atr, n);
   ArrayResize(active_hi, n);
   ArrayResize(active_lo, n);

   int ptr = 0;
   int active_n = 0;
   int m = 0;
   int opened = 0;
   int closed = 0;
   int skipped_incomplete = 0;
   int skipped_bad_atr = 0;
   int max_active = 0;

   for(int b = 0; b < bars_count; b++)
   {
      while(ptr < n)
      {
         int k = g_label_known_indices[ptr];
         int start = k + 1;
         if(start > b)
            break;

         if(k < 1 || start >= bars_count)
         {
            skipped_incomplete++;
            ptr++;
            continue;
         }

         int end = k + horizon;
         if(end >= bars_count)
         {
            if(InpH6RequireFullHorizon)
            {
               skipped_incomplete++;
               ptr++;
               continue;
            }
            end = bars_count - 1;
         }
         if(end < start)
         {
            skipped_incomplete++;
            ptr++;
            continue;
         }

         double atr = D0010_ATRAt(bars, bars_count, k, InpH6AtrPeriod);
         if(atr <= 0.0)
         {
            skipped_bad_atr++;
            ptr++;
            continue;
         }

         int a = active_n;
         active_label[a] = g_labels[ptr];
         active_dir[a] = g_label_dirs[ptr];
         active_end[a] = end;
         active_entry[a] = (InpH6EntryAnchorMode == 1 ? bars[start].open : bars[k].close);
         active_atr[a] = atr;
         active_hi[a] = bars[start].high;
         active_lo[a] = bars[start].low;
         active_n++;
         opened++;
         ptr++;
      }

      int a = 0;
      while(a < active_n)
      {
         if(bars[b].high > active_hi[a]) active_hi[a] = bars[b].high;
         if(bars[b].low < active_lo[a]) active_lo[a] = bars[b].low;

         if(b >= active_end[a])
         {
            double up = MathMax(0.0, active_hi[a] - active_entry[a]) / active_atr[a];
            double dn = MathMax(0.0, active_entry[a] - active_lo[a]) / active_atr[a];
            double absx = MathMax(up, dn);
            int d = active_dir[a];
            double dirx = absx;
            double advx = MathMin(up, dn);
            if(d > 0)
            {
               dirx = up;
               advx = dn;
            }
            else if(d < 0)
            {
               dirx = dn;
               advx = up;
            }

            if(m < n)
            {
               absv[m] = absx;
               dirv[m] = dirx;
               advv[m] = advx;
               valid_labels[m] = active_label[a];
               m++;
               closed++;
            }

            active_n--;
            if(a < active_n)
            {
               active_label[a] = active_label[active_n];
               active_dir[a] = active_dir[active_n];
               active_end[a] = active_end[active_n];
               active_entry[a] = active_entry[active_n];
               active_atr[a] = active_atr[active_n];
               active_hi[a] = active_hi[active_n];
               active_lo[a] = active_lo[active_n];
            }
            continue;
         }
         a++;
      }
      if(active_n > max_active)
         max_active = active_n;
   }

   if(InpH6PrintComputeAudit)
   {
      string audit_line = "DAL_H0006_COMPUTE_AUDIT_" + tag
         + " *** build=" + DAL_D0010_BUILD
         + "*contract=atomic_no_sample_known_time_batches_forward_candle_stream"
         + "*horizonBars=" + IntegerToString(horizon)
         + "*validN=" + IntegerToString(m)
         + "*opened=" + IntegerToString(opened)
         + "*closed=" + IntegerToString(closed)
         + "*leftOpen=" + IntegerToString(active_n)
         + "*skippedIncomplete=" + IntegerToString(skipped_incomplete)
         + "*skippedBadAtr=" + IntegerToString(skipped_bad_atr)
         + "*maxActive=" + IntegerToString(max_active)
         + "*entryAnchor=" + (InpH6EntryAnchorMode == 1 ? "NEXT_OPEN" : "KNOWN_CLOSE")
         + "*fullHorizonOnly=" + IntegerToString(InpH6RequireFullHorizon ? 1 : 0)
         + "*futureWindow=bar_by_bar_after_known_batch"
         + "*measurement=candle_forward_stream_no_prefix_rebuild_no_sample";
      Print(audit_line);
   }

   D0010ValueStats rev_abs, cont_abs, rev_dir, cont_dir, rev_adv, cont_adv;
   D0010_ComputeValueStats(absv, valid_labels, m, DAL_D0010_LABEL_REVERSAL, InpH6TailAtr1, InpH6TailAtr2, InpH6TailAtr3, rev_abs);
   D0010_ComputeValueStats(absv, valid_labels, m, DAL_D0010_LABEL_CONTINUATION, InpH6TailAtr1, InpH6TailAtr2, InpH6TailAtr3, cont_abs);
   D0010_ComputeValueStats(dirv, valid_labels, m, DAL_D0010_LABEL_REVERSAL, InpH6TailAtr1, InpH6TailAtr2, InpH6TailAtr3, rev_dir);
   D0010_ComputeValueStats(dirv, valid_labels, m, DAL_D0010_LABEL_CONTINUATION, InpH6TailAtr1, InpH6TailAtr2, InpH6TailAtr3, cont_dir);
   D0010_ComputeValueStats(advv, valid_labels, m, DAL_D0010_LABEL_REVERSAL, InpH6TailAtr1, InpH6TailAtr2, InpH6TailAtr3, rev_adv);
   D0010_ComputeValueStats(advv, valid_labels, m, DAL_D0010_LABEL_CONTINUATION, InpH6TailAtr1, InpH6TailAtr2, InpH6TailAtr3, cont_adv);

   string verdict = "mixed_optional_tail";
   if(rev_abs.p95 > cont_abs.p95 && rev_abs.hit2 > cont_abs.hit2) verdict = "reversal_tail_dominates";
   else if(cont_abs.p95 > rev_abs.p95 && cont_abs.hit2 > rev_abs.hit2) verdict = "continuation_tail_dominates";

   string optionality_line = "DAL_H0006_OPTIONALITY_" + tag
      + " *** build=" + DAL_D0010_BUILD
      + "*hypothesis=H0006_REVERSAL_EXPLOSIVE_OPTIONALITY"
      + "*engine=CANDLE_FORWARD_STREAM"
      + "*contract=atomic_no_sample_known_time_batches_future_excursion_only_after_known_time"
      + "*horizonBars=" + IntegerToString(horizon)
      + "*atrPeriod=" + IntegerToString((int)MathMax(2, InpH6AtrPeriod))
      + "*tailAtr1=" + DoubleToString(InpH6TailAtr1, 2)
      + "*tailAtr2=" + DoubleToString(InpH6TailAtr2, 2)
      + "*tailAtr3=" + DoubleToString(InpH6TailAtr3, 2)
      + "*validN=" + IntegerToString(m)
      + "*revN=" + IntegerToString(rev_abs.n)
      + "*contN=" + IntegerToString(cont_abs.n)
      + "*revAbsMeanATR=" + DoubleToString(rev_abs.mean, 4)
      + "*contAbsMeanATR=" + DoubleToString(cont_abs.mean, 4)
      + "*revMinusContAbsMeanATR=" + DoubleToString(rev_abs.mean - cont_abs.mean, 4)
      + "*revAbsP90ATR=" + DoubleToString(rev_abs.p90, 4)
      + "*contAbsP90ATR=" + DoubleToString(cont_abs.p90, 4)
      + "*revAbsP95ATR=" + DoubleToString(rev_abs.p95, 4)
      + "*contAbsP95ATR=" + DoubleToString(cont_abs.p95, 4)
      + "*revAbsP99ATR=" + DoubleToString(rev_abs.p99, 4)
      + "*contAbsP99ATR=" + DoubleToString(cont_abs.p99, 4)
      + "*revHitTail1Pct=" + DoubleToString(rev_abs.hit1, 2)
      + "*contHitTail1Pct=" + DoubleToString(cont_abs.hit1, 2)
      + "*revHitTail2Pct=" + DoubleToString(rev_abs.hit2, 2)
      + "*contHitTail2Pct=" + DoubleToString(cont_abs.hit2, 2)
      + "*revHitTail3Pct=" + DoubleToString(rev_abs.hit3, 2)
      + "*contHitTail3Pct=" + DoubleToString(cont_abs.hit3, 2)
      + "*revTop10SharePct=" + DoubleToString(rev_abs.top10_share, 2)
      + "*contTop10SharePct=" + DoubleToString(cont_abs.top10_share, 2)
      + "*revDirectionalMfeMeanATR=" + DoubleToString(rev_dir.mean, 4)
      + "*contDirectionalMfeMeanATR=" + DoubleToString(cont_dir.mean, 4)
      + "*revAdverseMeanATR=" + DoubleToString(rev_adv.mean, 4)
      + "*contAdverseMeanATR=" + DoubleToString(cont_adv.mean, 4)
      + "*optionalityRatioP95=" + DoubleToString(D0010_SafeDiv(rev_abs.p95, cont_abs.p95), 4)
      + "*verdict=" + verdict;
   Print(optionality_line);

   if(InpAtomicStressH6Optionality && InpPermutationIterations > 0 && InpH6StressMode > 0)
   {
      double obs_mean_diff = rev_abs.mean - cont_abs.mean;
      double obs_hit2_diff = rev_abs.hit2 - cont_abs.hit2;
      double obs_p90_diff = rev_abs.p90 - cont_abs.p90;
      double mean_sum = 0.0, mean_sum2 = 0.0, hit_sum = 0.0, hit_sum2 = 0.0, p90_sum = 0.0, p90_sum2 = 0.0;
      int mean_ge = 0, hit_ge = 0, p90_ge = 0;
      int shuf[];
      for(int iter = 0; iter < InpPermutationIterations; iter++)
      {
         D0010_ShuffleLabels(valid_labels, m, iter + 7001 + horizon, shuf);
         double md = 0.0, hd = 0.0, pd = 0.0;
         D0010_H6FastMeanHitDiff(absv, shuf, m, InpH6TailAtr2, md, hd);
         if(InpH6StressMode >= 2)
         {
            D0010ValueStats sr, sc;
            D0010_ComputeValueStats(absv, shuf, m, DAL_D0010_LABEL_REVERSAL, InpH6TailAtr1, InpH6TailAtr2, InpH6TailAtr3, sr);
            D0010_ComputeValueStats(absv, shuf, m, DAL_D0010_LABEL_CONTINUATION, InpH6TailAtr1, InpH6TailAtr2, InpH6TailAtr3, sc);
            pd = sr.p90 - sc.p90;
         }
         mean_sum += md; mean_sum2 += md * md;
         hit_sum += hd; hit_sum2 += hd * hd;
         p90_sum += pd; p90_sum2 += pd * pd;
         if(md >= obs_mean_diff) mean_ge++;
         if(hd >= obs_hit2_diff) hit_ge++;
         if(InpH6StressMode >= 2 && pd >= obs_p90_diff) p90_ge++;
      }
      double it = (double)InpPermutationIterations;
      double mean_null = D0010_SafeDiv(mean_sum, it);
      double hit_null = D0010_SafeDiv(hit_sum, it);
      double p90_null = D0010_SafeDiv(p90_sum, it);
      double mean_sd = MathSqrt(MathMax(0.0, D0010_SafeDiv(mean_sum2, it) - mean_null * mean_null));
      double hit_sd = MathSqrt(MathMax(0.0, D0010_SafeDiv(hit_sum2, it) - hit_null * hit_null));
      double p90_sd = MathSqrt(MathMax(0.0, D0010_SafeDiv(p90_sum2, it) - p90_null * p90_null));
      string optionality_stress_line = "DAL_H0006_OPTIONALITY_STRESS_" + tag
         + " *** build=" + DAL_D0010_BUILD
         + "*hypothesis=H0006_REVERSAL_EXPLOSIVE_OPTIONALITY"
         + "*engine=CANDLE_FORWARD_STREAM"
         + "*null=label_shuffle_over_fixed_known_times_and_fixed_future_excursions"
         + "*stressMode=" + IntegerToString(InpH6StressMode)
         + "*horizonBars=" + IntegerToString(horizon)
         + "*iters=" + IntegerToString(InpPermutationIterations)
         + "*obsRevMinusContMeanAbsATR=" + DoubleToString(obs_mean_diff, 4)
         + "*nullMeanDiff=" + DoubleToString(mean_null, 4)
         + "*nullMeanDiffSd=" + DoubleToString(mean_sd, 4)
         + "*meanDiffZ=" + DoubleToString(D0010_SafeDiv(obs_mean_diff - mean_null, mean_sd), 4)
         + "*meanDiffEmpP=" + DoubleToString(D0010_SafeDiv(mean_ge + 1, InpPermutationIterations + 1), 4)
         + "*obsRevMinusContHitTail2Pct=" + DoubleToString(obs_hit2_diff, 2)
         + "*nullHitTail2Diff=" + DoubleToString(hit_null, 2)
         + "*nullHitTail2DiffSd=" + DoubleToString(hit_sd, 2)
         + "*hitTail2DiffZ=" + DoubleToString(D0010_SafeDiv(obs_hit2_diff - hit_null, hit_sd), 4)
         + "*hitTail2DiffEmpP=" + DoubleToString(D0010_SafeDiv(hit_ge + 1, InpPermutationIterations + 1), 4);
      if(InpH6StressMode >= 2)
      {
         optionality_stress_line += "*obsRevMinusContP90AbsATR=" + DoubleToString(obs_p90_diff, 4)
            + "*nullP90Diff=" + DoubleToString(p90_null, 4)
            + "*nullP90DiffSd=" + DoubleToString(p90_sd, 4)
            + "*p90DiffZ=" + DoubleToString(D0010_SafeDiv(obs_p90_diff - p90_null, p90_sd), 4)
            + "*p90DiffEmpP=" + DoubleToString(D0010_SafeDiv(p90_ge + 1, InpPermutationIterations + 1), 4);
      }
      Print(optionality_stress_line);
   }
}


void D0010_ComputePlainValueStats(const double &values[], const int n, const double t1, const double t2, const double t3, D0010ValueStats &st)
{
   st.n = 0; st.mean = 0.0; st.median = 0.0; st.p75 = 0.0; st.p90 = 0.0; st.p95 = 0.0; st.p99 = 0.0; st.maxv = 0.0; st.hit1 = 0.0; st.hit2 = 0.0; st.hit3 = 0.0; st.top10_share = 0.0;
   if(n <= 0) return;
   double x[];
   ArrayResize(x, n);
   int h1 = 0, h2 = 0, h3 = 0;
   double sum = 0.0;
   for(int i = 0; i < n; i++)
   {
      x[i] = values[i];
      sum += values[i];
      if(values[i] > st.maxv) st.maxv = values[i];
      if(values[i] >= t1) h1++;
      if(values[i] >= t2) h2++;
      if(values[i] >= t3) h3++;
   }
   st.n = n;
   st.mean = D0010_SafeDiv(sum, n);
   D0010_SortDoubleArray(x, n);
   st.median = D0010_QuantileFromSorted(x, n, 0.50);
   st.p75 = D0010_QuantileFromSorted(x, n, 0.75);
   st.p90 = D0010_QuantileFromSorted(x, n, 0.90);
   st.p95 = D0010_QuantileFromSorted(x, n, 0.95);
   st.p99 = D0010_QuantileFromSorted(x, n, 0.99);
   st.hit1 = D0010_SafePct(h1, n);
   st.hit2 = D0010_SafePct(h2, n);
   st.hit3 = D0010_SafePct(h3, n);
   int tail_start = (int)MathFloor(0.90 * n);
   if(tail_start < 0) tail_start = 0;
   if(tail_start >= n) tail_start = n - 1;
   double tail_sum = 0.0;
   for(int j = tail_start; j < n; j++) tail_sum += x[j];
   st.top10_share = D0010_SafePct(tail_sum, sum);
}

void D0010_H6PrintEdgeBucket(const string tag, const string bucket, const int total_valid, D0010ValueStats &allst, D0010ValueStats &st)
{
   if(st.n <= 0) return;
   double p95_lift = st.p95 - allst.p95;
   double p99_lift = st.p99 - allst.p99;
   double hit2_lift = st.hit2 - allst.hit2;
   double edge_score = st.p95 * D0010_SafeDiv(st.hit2, 100.0);
   string materiality = "neutral";
   if(st.n < MathMax(10, InpH6MinBucketN)) materiality = "too_sparse";
   else if(p95_lift > 0.25 && hit2_lift > 2.0) materiality = "edge_candidate";
   else if(p95_lift > 0.75 && hit2_lift > 5.0) materiality = "strong_edge_candidate";
   else if(p95_lift < -0.25 && hit2_lift < -2.0) materiality = "negative_or_unimportant";

   string edge_bucket_line = "DAL_H0006_EDGE_BUCKET_" + tag
      + " *** build=" + DAL_D0010_BUILD
      + "*hypothesis=H0006_REVERSAL_EXPLOSIVE_OPTIONALITY"
      + "*contract=atomic_no_sample_known_time_batches_future_excursion_only_after_known_time"
      + "*bucket=" + bucket
      + "*n=" + IntegerToString(st.n)
      + "*pctOfValid=" + DoubleToString(D0010_SafePct(st.n, total_valid), 2)
      + "*absMeanATR=" + DoubleToString(st.mean, 4)
      + "*absP75ATR=" + DoubleToString(st.p75, 4)
      + "*absP90ATR=" + DoubleToString(st.p90, 4)
      + "*absP95ATR=" + DoubleToString(st.p95, 4)
      + "*absP99ATR=" + DoubleToString(st.p99, 4)
      + "*hitTail1Pct=" + DoubleToString(st.hit1, 2)
      + "*hitTail2Pct=" + DoubleToString(st.hit2, 2)
      + "*hitTail3Pct=" + DoubleToString(st.hit3, 2)
      + "*top10SharePct=" + DoubleToString(st.top10_share, 2)
      + "*p95LiftVsAllATR=" + DoubleToString(p95_lift, 4)
      + "*p99LiftVsAllATR=" + DoubleToString(p99_lift, 4)
      + "*hitTail2LiftVsAllPct=" + DoubleToString(hit2_lift, 2)
      + "*edgeScore=" + DoubleToString(edge_score, 4)
      + "*materiality=" + materiality;
   Print(edge_bucket_line);
}

void D0010_H6AppendIf(bool cond, const double value, double &arr[], int &n)
{
   if(!cond) return;
   ArrayResize(arr, n + 1);
   arr[n++] = value;
}

void D0010_H6EdgeMapForHorizon(const DALBar &bars[], const int bars_count, const int horizon, const string tag)
{
   if(!InpAtomicPrintH6EdgeMap)
      return;
   int n = ArraySize(g_labels);
   if(n <= 0 || bars_count <= 0 || horizon <= 0)
      return;

   double allv[], rev_all[], cont_all[], rev_single[], rev_multi[], rev_big[], cont_single[], cont_multi[], cont_big[];
   double rev_buy[], rev_sell[], cont_buy[], cont_sell[], rev_run_start[], rev_run_cont[], cont_run_start[], cont_run_cont[];
   int alln=0, rn=0, cn=0, rsn=0, rmn=0, rbn=0, csn=0, cmn=0, cbn=0;
   int rbuy=0, rsell=0, cbuy=0, csell=0, rstart=0, rcont=0, cstart=0, ccont=0;

   for(int i = 0; i < n; i++)
   {
      int k = g_label_known_indices[i];
      if(k < 1 || k + 1 >= bars_count) continue;
      int end = MathMin(bars_count - 1, k + horizon);
      if(end <= k) continue;
      double atr = D0010_ATRAt(bars, bars_count, k, InpH6AtrPeriod);
      if(atr <= 0.0) continue;
      int start = k + 1;
      double entry = (InpH6EntryAnchorMode == 1 ? bars[start].open : bars[k].close);
      double hi = bars[start].high;
      double lo = bars[start].low;
      for(int j = start; j <= end; j++)
      {
         if(bars[j].high > hi) hi = bars[j].high;
         if(bars[j].low < lo) lo = bars[j].low;
      }
      double absx = MathMax(MathMax(0.0, hi - entry), MathMax(0.0, entry - lo)) / atr;
      bool is_rev = (g_labels[i] == DAL_D0010_LABEL_REVERSAL);
      bool is_cont = (g_labels[i] == DAL_D0010_LABEL_CONTINUATION);
      bool same_prev = (i > 0 && g_labels[i - 1] == g_labels[i]);
      int bc = g_label_batch_counts[i];
      int d = g_label_dirs[i];

      D0010_H6AppendIf(true, absx, allv, alln);
      D0010_H6AppendIf(is_rev, absx, rev_all, rn);
      D0010_H6AppendIf(is_cont, absx, cont_all, cn);
      D0010_H6AppendIf(is_rev && bc <= 1, absx, rev_single, rsn);
      D0010_H6AppendIf(is_rev && bc > 1, absx, rev_multi, rmn);
      D0010_H6AppendIf(is_rev && bc >= 3, absx, rev_big, rbn);
      D0010_H6AppendIf(is_cont && bc <= 1, absx, cont_single, csn);
      D0010_H6AppendIf(is_cont && bc > 1, absx, cont_multi, cmn);
      D0010_H6AppendIf(is_cont && bc >= 3, absx, cont_big, cbn);
      D0010_H6AppendIf(is_rev && d > 0, absx, rev_buy, rbuy);
      D0010_H6AppendIf(is_rev && d < 0, absx, rev_sell, rsell);
      D0010_H6AppendIf(is_cont && d > 0, absx, cont_buy, cbuy);
      D0010_H6AppendIf(is_cont && d < 0, absx, cont_sell, csell);
      D0010_H6AppendIf(is_rev && !same_prev, absx, rev_run_start, rstart);
      D0010_H6AppendIf(is_rev && same_prev, absx, rev_run_cont, rcont);
      D0010_H6AppendIf(is_cont && !same_prev, absx, cont_run_start, cstart);
      D0010_H6AppendIf(is_cont && same_prev, absx, cont_run_cont, ccont);
   }

   D0010ValueStats allst, st;
   D0010_ComputePlainValueStats(allv, alln, InpH6TailAtr1, InpH6TailAtr2, InpH6TailAtr3, allst);
   if(alln <= 0) return;

   string edge_audit_line = "DAL_H0006_EDGE_MAP_AUDIT_" + tag
      + " *** build=" + DAL_D0010_BUILD
      + "*hypothesis=H0006_REVERSAL_EXPLOSIVE_OPTIONALITY"
      + "*horizonBars=" + IntegerToString(horizon)
      + "*validN=" + IntegerToString(alln)
      + "*minBucketN=" + IntegerToString((int)MathMax(10, InpH6MinBucketN))
      + "*tailAtr=" + DoubleToString(InpH6TailAtr1, 2) + "/" + DoubleToString(InpH6TailAtr2, 2) + "/" + DoubleToString(InpH6TailAtr3, 2)
      + "*bucketDimensions=label_intensity_direction_run_position"
      + "*question=which_known_time_conditions_are_edgier_optional_tail_locations";
   Print(edge_audit_line);

   D0010_ComputePlainValueStats(rev_all, rn, InpH6TailAtr1, InpH6TailAtr2, InpH6TailAtr3, st); D0010_H6PrintEdgeBucket(tag, "REV_ALL", alln, allst, st);
   D0010_ComputePlainValueStats(cont_all, cn, InpH6TailAtr1, InpH6TailAtr2, InpH6TailAtr3, st); D0010_H6PrintEdgeBucket(tag, "CONT_ALL", alln, allst, st);
   if(InpH6EdgeMapLevel >= 1)
   {
      D0010_ComputePlainValueStats(rev_multi, rmn, InpH6TailAtr1, InpH6TailAtr2, InpH6TailAtr3, st); D0010_H6PrintEdgeBucket(tag, "REV_MULTI_EVENT", alln, allst, st);
      D0010_ComputePlainValueStats(rev_big, rbn, InpH6TailAtr1, InpH6TailAtr2, InpH6TailAtr3, st); D0010_H6PrintEdgeBucket(tag, "REV_BIG_3PLUS_EVENT", alln, allst, st);
      D0010_ComputePlainValueStats(cont_multi, cmn, InpH6TailAtr1, InpH6TailAtr2, InpH6TailAtr3, st); D0010_H6PrintEdgeBucket(tag, "CONT_MULTI_EVENT", alln, allst, st);
      D0010_ComputePlainValueStats(cont_big, cbn, InpH6TailAtr1, InpH6TailAtr2, InpH6TailAtr3, st); D0010_H6PrintEdgeBucket(tag, "CONT_BIG_3PLUS_EVENT", alln, allst, st);
      D0010_ComputePlainValueStats(rev_run_start, rstart, InpH6TailAtr1, InpH6TailAtr2, InpH6TailAtr3, st); D0010_H6PrintEdgeBucket(tag, "REV_RUN_START", alln, allst, st);
      D0010_ComputePlainValueStats(rev_run_cont, rcont, InpH6TailAtr1, InpH6TailAtr2, InpH6TailAtr3, st); D0010_H6PrintEdgeBucket(tag, "REV_RUN_CONTINUATION", alln, allst, st);
      D0010_ComputePlainValueStats(cont_run_start, cstart, InpH6TailAtr1, InpH6TailAtr2, InpH6TailAtr3, st); D0010_H6PrintEdgeBucket(tag, "CONT_RUN_START", alln, allst, st);
      D0010_ComputePlainValueStats(cont_run_cont, ccont, InpH6TailAtr1, InpH6TailAtr2, InpH6TailAtr3, st); D0010_H6PrintEdgeBucket(tag, "CONT_RUN_CONTINUATION", alln, allst, st);
   }
   if(InpH6EdgeMapLevel >= 2)
   {
      D0010_ComputePlainValueStats(rev_single, rsn, InpH6TailAtr1, InpH6TailAtr2, InpH6TailAtr3, st); D0010_H6PrintEdgeBucket(tag, "REV_SINGLE_EVENT", alln, allst, st);
      D0010_ComputePlainValueStats(cont_single, csn, InpH6TailAtr1, InpH6TailAtr2, InpH6TailAtr3, st); D0010_H6PrintEdgeBucket(tag, "CONT_SINGLE_EVENT", alln, allst, st);
      D0010_ComputePlainValueStats(rev_buy, rbuy, InpH6TailAtr1, InpH6TailAtr2, InpH6TailAtr3, st); D0010_H6PrintEdgeBucket(tag, "REV_BUY_DOMINANT", alln, allst, st);
      D0010_ComputePlainValueStats(rev_sell, rsell, InpH6TailAtr1, InpH6TailAtr2, InpH6TailAtr3, st); D0010_H6PrintEdgeBucket(tag, "REV_SELL_DOMINANT", alln, allst, st);
      D0010_ComputePlainValueStats(cont_buy, cbuy, InpH6TailAtr1, InpH6TailAtr2, InpH6TailAtr3, st); D0010_H6PrintEdgeBucket(tag, "CONT_BUY_DOMINANT", alln, allst, st);
      D0010_ComputePlainValueStats(cont_sell, csell, InpH6TailAtr1, InpH6TailAtr2, InpH6TailAtr3, st); D0010_H6PrintEdgeBucket(tag, "CONT_SELL_DOMINANT", alln, allst, st);
   }
}


// H0006 node survival map: node becomes a colored edge candidate if price does
// not break the node after 20/50/100 closed candles from its known-time batch.
struct D0010NodeSurvivalStats
{
   int known_nodes;
   int high_nodes;
   int low_nodes;
   int matured1;
   int matured2;
   int matured3;
   int survived1;
   int survived2;
   int survived3;
   int broken1;
   int broken2;
   int broken3;
   int touched1;
   int touched2;
   int touched3;
   int detached1;
   int detached2;
   int detached3;
   int active_stage1;
   int active_stage2;
   int active_stage3;
   int chart_drawn;
   int reaction_touch_nodes;
   int reaction_confirmed_nodes;
   int reaction_matured1;
   int reaction_matured2;
   int reaction_matured3;
   int reaction_survived1;
   int reaction_survived2;
   int reaction_survived3;
   int reaction_retouch1;
   int reaction_retouch2;
   int reaction_retouch3;
   int reaction_active_stage1;
   int reaction_active_stage2;
   int reaction_active_stage3;
   int reaction_boxes_drawn;
};

void D0010_ResetNodeSurvivalStats(D0010NodeSurvivalStats &st)
{
   st.known_nodes = 0;
   st.high_nodes = 0;
   st.low_nodes = 0;
   st.matured1 = 0;
   st.matured2 = 0;
   st.matured3 = 0;
   st.survived1 = 0;
   st.survived2 = 0;
   st.survived3 = 0;
   st.broken1 = 0;
   st.broken2 = 0;
   st.broken3 = 0;
   st.touched1 = 0;
   st.touched2 = 0;
   st.touched3 = 0;
   st.detached1 = 0;
   st.detached2 = 0;
   st.detached3 = 0;
   st.active_stage1 = 0;
   st.active_stage2 = 0;
   st.active_stage3 = 0;
   st.chart_drawn = 0;
   st.reaction_touch_nodes = 0;
   st.reaction_confirmed_nodes = 0;
   st.reaction_matured1 = 0;
   st.reaction_matured2 = 0;
   st.reaction_matured3 = 0;
   st.reaction_survived1 = 0;
   st.reaction_survived2 = 0;
   st.reaction_survived3 = 0;
   st.reaction_retouch1 = 0;
   st.reaction_retouch2 = 0;
   st.reaction_retouch3 = 0;
   st.reaction_active_stage1 = 0;
   st.reaction_active_stage2 = 0;
   st.reaction_active_stage3 = 0;
   st.reaction_boxes_drawn = 0;
}

bool D0010_H6NodeBrokenAtBar(const DALBar &bar, const double node_price, const bool high_node, const double break_buffer)
{
   if(high_node)
      return (bar.high >= node_price + break_buffer);
   return (bar.low <= node_price - break_buffer);
}

bool D0010_H6NodeTouchedAtBar(const DALBar &bar, const double node_price, const bool high_node, const double touch_buffer)
{
   if(high_node)
      return (bar.high >= node_price - touch_buffer);
   return (bar.low <= node_price + touch_buffer);
}

void D0010_H6FindNodeTouchBreak(
   const DALBar &bars[],
   const int bars_count,
   const int known,
   const double node_price,
   const bool high_node,
   const int scan_to,
   const double touch_buffer,
   const double break_buffer,
   int &touch_index,
   int &break_index
)
{
   touch_index = -1;
   break_index = -1;
   int start = known + 1;
   int end = MathMin(bars_count - 1, scan_to);
   for(int j = start; j <= end; j++)
   {
      if(touch_index < 0 && D0010_H6NodeTouchedAtBar(bars[j], node_price, high_node, touch_buffer))
         touch_index = j;
      if(D0010_H6NodeBrokenAtBar(bars[j], node_price, high_node, break_buffer))
      {
         break_index = j;
         if(touch_index < 0) touch_index = j;
         return;
      }
   }
}

void D0010_H6DeleteNodeObjects(const string prefix)
{
   if(!InpH6NodeDrawChart)
      return;
   int total = ObjectsTotal(0);
   for(int i = total - 1; i >= 0; i--)
   {
      string name = ObjectName(0, i);
      if(StringFind(name, prefix) == 0)
         ObjectDelete(0, name);
   }
}

bool D0010_H6DrawNodeLine(
   const string name,
   const datetime t1,
   const datetime t2,
   const double price,
   const color c,
   const int width,
   const string tooltip
)
{
   if(!InpH6NodeDrawChart)
      return false;
   ObjectDelete(0, name);
   if(!ObjectCreate(0, name, OBJ_TREND, 0, t1, price, t2, price))
      return false;
   ObjectSetInteger(0, name, OBJPROP_COLOR, c);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, MathMax(1, width));
   ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_SOLID);
   ObjectSetInteger(0, name, OBJPROP_RAY_RIGHT, true);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_BACK, false);
   ObjectSetString(0, name, OBJPROP_TOOLTIP, tooltip);
   return true;
}


double D0010_H6ReactionTouchPriceAtBar(const DALBar &bar, const bool high_node)
{
   if(high_node)
      return bar.high;
   return bar.low;
}

bool D0010_H6ReactionAwayConfirmedAtBar(
   const DALBar &bar,
   const double node_price,
   const bool high_node,
   const double away_buffer
)
{
   if(high_node)
      return (bar.low <= node_price - away_buffer);
   return (bar.high >= node_price + away_buffer);
}

bool D0010_H6ReactionZoneEndRetouchedAtBar(
   const DALBar &bar,
   const double zone_end_price,
   const bool high_node,
   const double retouch_buffer
)
{
   if(high_node)
      return (bar.high >= zone_end_price - retouch_buffer);
   return (bar.low <= zone_end_price + retouch_buffer);
}

void D0010_H6FindReactionBox(
   const DALBar &bars[],
   const int bars_count,
   const int known,
   const double node_price,
   const bool high_node,
   const int scan_to,
   const double touch_buffer,
   const double away_buffer,
   const double retouch_buffer,
   int &touch_index,
   int &confirm_index,
   int &retouch_index,
   double &zone_end_price
)
{
   touch_index = -1;
   confirm_index = -1;
   retouch_index = -1;
   zone_end_price = node_price;

   int start = known + 1;
   int end = MathMin(bars_count - 1, scan_to);
   for(int j = start; j <= end; j++)
   {
      if(touch_index < 0)
      {
         if(D0010_H6NodeTouchedAtBar(bars[j], node_price, high_node, touch_buffer))
         {
            touch_index = j;
            zone_end_price = D0010_H6ReactionTouchPriceAtBar(bars[j], high_node);
         }
         continue;
      }

      // Conservative OHLC rule: if a later bar both retouches the far edge
      // and moves away, we count the zone-end retouch first to avoid hidden
      // same-candle sequence assumptions.
      if(D0010_H6ReactionZoneEndRetouchedAtBar(bars[j], zone_end_price, high_node, retouch_buffer))
      {
         retouch_index = j;
         return;
      }

      if(confirm_index < 0 && D0010_H6ReactionAwayConfirmedAtBar(bars[j], node_price, high_node, away_buffer))
         confirm_index = j;
   }
}

bool D0010_H6DrawReactionBox(
   const string name,
   const datetime t1,
   const datetime t2,
   const double node_price,
   const double zone_end_price,
   const bool high_node,
   const color c,
   const int width,
   const string tooltip
)
{
   if(!InpH6NodeDrawChart || !InpH6ReactionBoxDrawChart)
      return false;

   double point = SymbolInfoDouble(D0010_Symbol(), SYMBOL_POINT);
   if(point <= 0.0) point = _Point;
   double min_h = MathMax(0.0, InpH6ReactionMinBoxHeightPoints) * point;
   double p1 = node_price;
   double p2 = zone_end_price;
   if(MathAbs(p2 - p1) < min_h)
   {
      if(high_node)
         p2 = p1 + min_h;
      else
         p2 = p1 - min_h;
   }

   double top = MathMax(p1, p2);
   double bottom = MathMin(p1, p2);
   datetime right_time = t2;
   if(right_time <= t1)
      right_time = t1 + PeriodSeconds(D0010_Timeframe());

   ObjectDelete(0, name);
   if(!ObjectCreate(0, name, OBJ_RECTANGLE, 0, t1, top, right_time, bottom))
      return false;
   ObjectSetInteger(0, name, OBJPROP_COLOR, c);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, MathMax(1, width));
   ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_SOLID);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_BACK, InpH6ReactionBoxBack ? 1 : 0);
   ObjectSetInteger(0, name, OBJPROP_FILL, InpH6ReactionBoxFill ? 1 : 0);
   ObjectSetString(0, name, OBJPROP_TOOLTIP, tooltip);
   return true;
}

int D0010_H6NodeStage(const int age, const int h1, const int h2, const int h3)
{
   if(age >= h3) return 3;
   if(age >= h2) return 2;
   if(age >= h1) return 1;
   return 0;
}

color D0010_H6NodeStageColor(const int stage)
{
   if(stage >= 3) return InpH6NodeColor3;
   if(stage == 2) return InpH6NodeColor2;
   return InpH6NodeColor1;
}

int D0010_H6ReactionAchievedStage(
   const int confirm_index,
   const int retouch_index,
   const int last,
   const int h1,
   const int h2,
   const int h3,
   int &age_until_end,
   bool &active_box
)
{
   age_until_end = 0;
   active_box = true;
   if(confirm_index < 0)
      return 0;

   int effective_last = last;
   if(retouch_index > 0)
   {
      active_box = false;
      effective_last = retouch_index - 1;
   }
   if(effective_last < confirm_index)
      effective_last = confirm_index;

   age_until_end = effective_last - confirm_index;
   return D0010_H6NodeStage(age_until_end, h1, h2, h3);
}

int D0010_H6TouchLifecycleStage(
   const int touch_index,
   const int retouch_index,
   const int last,
   const int h1,
   const int h2,
   const int h3,
   int &age_until_end,
   bool &active_box
)
{
   age_until_end = 0;
   active_box = true;
   if(touch_index < 0)
      return 0;

   int effective_last = last;
   if(retouch_index > 0)
   {
      active_box = false;
      effective_last = retouch_index - 1;
   }
   if(effective_last < touch_index)
      effective_last = touch_index;

   age_until_end = effective_last - touch_index;
   return D0010_H6NodeStage(age_until_end, h1, h2, h3);
}

color D0010_H6ReactionStageColor(const int stage, const bool active_box)
{
   if(stage >= 3) return InpH6NodeColor3;
   if(stage == 2) return InpH6NodeColor2;
   if(stage == 1) return InpH6NodeColor1;
   if(active_box) return clrOrange;
   return clrSilver;
}

void D0010_H6NodeSurvivalReport(
   const DALM0001Event &events[],
   const int events_count,
   const DALBar &bars[],
   const int bars_count,
   const int nodes_count
)
{
   if(!InpH6NodeSurvivalReport)
      return;

   D0010NodeSurvivalStats st;
   D0010_ResetNodeSurvivalStats(st);

   int h1 = MathMax(1, InpH6NodeHorizon1);
   int h2 = MathMax(h1 + 1, InpH6NodeHorizon2);
   int h3 = MathMax(h2 + 1, InpH6NodeHorizon3);
   int warmup = MathMax(InpWarmupClosedBars, InpL * 2 + InpExitGap + 50);
   int last = bars_count - 1;
   double point = SymbolInfoDouble(D0010_Symbol(), SYMBOL_POINT);
   if(point <= 0.0) point = _Point;
   double touch_buffer = MathMax(0.0, InpH6NodeTouchBufferPoints) * point;
   double break_buffer = MathMax(0.0, InpH6NodeBreakBufferPoints) * point;
   double reaction_away_buffer = MathMax(0.0, InpH6ReactionAwayBufferPoints) * point;
   double reaction_retouch_buffer = MathMax(0.0, InpH6ReactionZoneEndBufferPoints) * point;

   for(int i = 0; i < events_count; i++)
   {
      int label = DAL_D0010_LABEL_UNKNOWN;
      int dir = 0;
      int known = -1;
      if(!D0010_ClassifyRawEvent(events[i], bars, bars_count, label, dir, known))
         continue;
      if(known < warmup || known + 1 >= bars_count)
         continue;

      bool high_node = (events[i].node_type == DAL_NODE_HIGH);
      bool low_node = (events[i].node_type == DAL_NODE_LOW);
      if(!high_node && !low_node)
         continue;

      st.known_nodes++;
      if(high_node) st.high_nodes++;
      if(low_node) st.low_nodes++;

      int touch_index = -1;
      int break_index = -1;
      D0010_H6FindNodeTouchBreak(bars, bars_count, known, events[i].node_price, high_node, known + h3, touch_buffer, break_buffer, touch_index, break_index);

      if(known + h1 <= last)
      {
         st.matured1++;
         if(touch_index > 0 && touch_index <= known + h1) st.touched1++;
         if(break_index > 0 && break_index <= known + h1) st.broken1++;
         else st.survived1++;
         if((touch_index < 0 || touch_index > known + h1) && (break_index < 0 || break_index > known + h1)) st.detached1++;
      }
      if(known + h2 <= last)
      {
         st.matured2++;
         if(touch_index > 0 && touch_index <= known + h2) st.touched2++;
         if(break_index > 0 && break_index <= known + h2) st.broken2++;
         else st.survived2++;
         if((touch_index < 0 || touch_index > known + h2) && (break_index < 0 || break_index > known + h2)) st.detached2++;
      }
      if(known + h3 <= last)
      {
         st.matured3++;
         if(touch_index > 0 && touch_index <= known + h3) st.touched3++;
         if(break_index > 0 && break_index <= known + h3) st.broken3++;
         else st.survived3++;
         if((touch_index < 0 || touch_index > known + h3) && (break_index < 0 || break_index > known + h3)) st.detached3++;
      }


      if(InpH6ReactionBoxReport || InpH6ReactionBoxDrawChart)
      {
         int rx_touch = -1;
         int rx_confirm = -1;
         int rx_retouch = -1;
         double rx_zone_end = events[i].node_price;
         D0010_H6FindReactionBox(bars, bars_count, known, events[i].node_price, high_node, known + h3, touch_buffer, reaction_away_buffer, reaction_retouch_buffer, rx_touch, rx_confirm, rx_retouch, rx_zone_end);
         if(rx_touch > 0)
            st.reaction_touch_nodes++;
         if(rx_touch > 0)
         {
            st.reaction_confirmed_nodes++;
            if(rx_touch + h1 <= last)
            {
               st.reaction_matured1++;
               if(rx_retouch > 0 && rx_retouch <= rx_touch + h1) st.reaction_retouch1++;
               else st.reaction_survived1++;
            }
            if(rx_touch + h2 <= last)
            {
               st.reaction_matured2++;
               if(rx_retouch > 0 && rx_retouch <= rx_touch + h2) st.reaction_retouch2++;
               else st.reaction_survived2++;
            }
            if(rx_touch + h3 <= last)
            {
               st.reaction_matured3++;
               if(rx_retouch > 0 && rx_retouch <= rx_touch + h3) st.reaction_retouch3++;
               else st.reaction_survived3++;
            }
         }
      }
   }

   string header = "DAL_H0006_NODE_SURVIVAL_AUDIT *** build=" + DAL_D0010_BUILD
      + "*hypothesis=H0006_NODE_SURVIVAL_MAP"
      + "*contract=raw_m0001_nodes_known_time_no_sample_no_same_candle_order"
      + "*bars=" + IntegerToString(bars_count)
      + "*nodes=" + IntegerToString(nodes_count)
      + "*rawEvents=" + IntegerToString(events_count)
      + "*knownNodes=" + IntegerToString(st.known_nodes)
      + "*highNodes=" + IntegerToString(st.high_nodes)
      + "*lowNodes=" + IntegerToString(st.low_nodes)
      + "*horizons=" + IntegerToString(h1) + "/" + IntegerToString(h2) + "/" + IntegerToString(h3)
      + "*colors=red/green/purple"
      + "*meaning=if_node_not_broken_after_horizon_it_becomes_colored_edge_candidate"
      + "*touchBufferPoints=" + DoubleToString(InpH6NodeTouchBufferPoints, 2)
      + "*breakBufferPoints=" + DoubleToString(InpH6NodeBreakBufferPoints, 2)
      + "*reactionBoxReport=" + IntegerToString(InpH6ReactionBoxReport ? 1 : 0)
      + "*reactionBoxDraw=" + IntegerToString(InpH6ReactionBoxDrawChart ? 1 : 0)
      + "*reactionAwayBufferPoints=" + DoubleToString(InpH6ReactionAwayBufferPoints, 2)
      + "*zoneEndRetouchBufferPoints=" + DoubleToString(InpH6ReactionZoneEndBufferPoints, 2)
      + "*reactionRule=touch_node_then_confirm_away_then_survive_without_zone_end_retouch";
   Print(header);

   string h1_line = "DAL_H0006_NODE_SURVIVAL_H" + IntegerToString(h1) + " *** build=" + DAL_D0010_BUILD
      + "*color=RED"
      + "*matured=" + IntegerToString(st.matured1)
      + "*survived=" + IntegerToString(st.survived1)
      + "*broken=" + IntegerToString(st.broken1)
      + "*touched=" + IntegerToString(st.touched1)
      + "*detachedNoTouchNoBreak=" + IntegerToString(st.detached1)
      + "*survivalPct=" + DoubleToString(D0010_SafePct(st.survived1, st.matured1), 2)
      + "*breakPct=" + DoubleToString(D0010_SafePct(st.broken1, st.matured1), 2)
      + "*detachedPct=" + DoubleToString(D0010_SafePct(st.detached1, st.matured1), 2);
   Print(h1_line);

   string h2_line = "DAL_H0006_NODE_SURVIVAL_H" + IntegerToString(h2) + " *** build=" + DAL_D0010_BUILD
      + "*color=GREEN"
      + "*matured=" + IntegerToString(st.matured2)
      + "*survived=" + IntegerToString(st.survived2)
      + "*broken=" + IntegerToString(st.broken2)
      + "*touched=" + IntegerToString(st.touched2)
      + "*detachedNoTouchNoBreak=" + IntegerToString(st.detached2)
      + "*survivalPct=" + DoubleToString(D0010_SafePct(st.survived2, st.matured2), 2)
      + "*breakPct=" + DoubleToString(D0010_SafePct(st.broken2, st.matured2), 2)
      + "*detachedPct=" + DoubleToString(D0010_SafePct(st.detached2, st.matured2), 2)
      + "*conditionalSurvivalFromH" + IntegerToString(h1) + "Pct=" + DoubleToString(D0010_SafePct(st.survived2, MathMax(1, st.survived1)), 2);
   Print(h2_line);

   string h3_line = "DAL_H0006_NODE_SURVIVAL_H" + IntegerToString(h3) + " *** build=" + DAL_D0010_BUILD
      + "*color=PURPLE"
      + "*matured=" + IntegerToString(st.matured3)
      + "*survived=" + IntegerToString(st.survived3)
      + "*broken=" + IntegerToString(st.broken3)
      + "*touched=" + IntegerToString(st.touched3)
      + "*detachedNoTouchNoBreak=" + IntegerToString(st.detached3)
      + "*survivalPct=" + DoubleToString(D0010_SafePct(st.survived3, st.matured3), 2)
      + "*breakPct=" + DoubleToString(D0010_SafePct(st.broken3, st.matured3), 2)
      + "*detachedPct=" + DoubleToString(D0010_SafePct(st.detached3, st.matured3), 2)
      + "*conditionalSurvivalFromH" + IntegerToString(h2) + "Pct=" + DoubleToString(D0010_SafePct(st.survived3, MathMax(1, st.survived2)), 2);
   Print(h3_line);

   if(InpH6ReactionBoxReport)
   {
      string rx_audit = "DAL_H0006_REACTION_BOX_AUDIT *** build=" + DAL_D0010_BUILD
         + "*hypothesis=H0006_NODE_REACTION_BOX"
         + "*contract=raw_m0001_known_time_touch_reaction_no_same_candle_sequence"
         + "*knownNodes=" + IntegerToString(st.known_nodes)
         + "*touchNodes=" + IntegerToString(st.reaction_touch_nodes)
         + "*confirmedReactionNodes=" + IntegerToString(st.reaction_confirmed_nodes)
         + "*touchToReactionRule=first_touch_of_any_raw_node_then_measure_survival_from_touch"
         + "*invalidator=zone_end_retouch_after_touch"
         + "*box=time_from_node_origin_to_first_touch_price_from_node_level_to_touch_extreme"
         + "*colorRule=touch_age_without_zone_end_retouch"
         + "*colors=red/green/purple_by_reaction_survival_" + IntegerToString(h1) + "/" + IntegerToString(h2) + "/" + IntegerToString(h3);
      Print(rx_audit);

      string rx_h1 = "DAL_H0006_REACTION_BOX_H" + IntegerToString(h1) + " *** build=" + DAL_D0010_BUILD
         + "*color=RED"
         + "*matured=" + IntegerToString(st.reaction_matured1)
         + "*survivedNoZoneEndRetouch=" + IntegerToString(st.reaction_survived1)
         + "*zoneEndRetouched=" + IntegerToString(st.reaction_retouch1)
         + "*survivalPct=" + DoubleToString(D0010_SafePct(st.reaction_survived1, st.reaction_matured1), 2)
         + "*retouchPct=" + DoubleToString(D0010_SafePct(st.reaction_retouch1, st.reaction_matured1), 2);
      Print(rx_h1);

      string rx_h2 = "DAL_H0006_REACTION_BOX_H" + IntegerToString(h2) + " *** build=" + DAL_D0010_BUILD
         + "*color=GREEN"
         + "*matured=" + IntegerToString(st.reaction_matured2)
         + "*survivedNoZoneEndRetouch=" + IntegerToString(st.reaction_survived2)
         + "*zoneEndRetouched=" + IntegerToString(st.reaction_retouch2)
         + "*survivalPct=" + DoubleToString(D0010_SafePct(st.reaction_survived2, st.reaction_matured2), 2)
         + "*retouchPct=" + DoubleToString(D0010_SafePct(st.reaction_retouch2, st.reaction_matured2), 2)
         + "*conditionalSurvivalFromH" + IntegerToString(h1) + "Pct=" + DoubleToString(D0010_SafePct(st.reaction_survived2, MathMax(1, st.reaction_survived1)), 2);
      Print(rx_h2);

      string rx_h3 = "DAL_H0006_REACTION_BOX_H" + IntegerToString(h3) + " *** build=" + DAL_D0010_BUILD
         + "*color=PURPLE"
         + "*matured=" + IntegerToString(st.reaction_matured3)
         + "*survivedNoZoneEndRetouch=" + IntegerToString(st.reaction_survived3)
         + "*zoneEndRetouched=" + IntegerToString(st.reaction_retouch3)
         + "*survivalPct=" + DoubleToString(D0010_SafePct(st.reaction_survived3, st.reaction_matured3), 2)
         + "*retouchPct=" + DoubleToString(D0010_SafePct(st.reaction_retouch3, st.reaction_matured3), 2)
         + "*conditionalSurvivalFromH" + IntegerToString(h2) + "Pct=" + DoubleToString(D0010_SafePct(st.reaction_survived3, MathMax(1, st.reaction_survived2)), 2);
      Print(rx_h3);
   }

   string prefix = "DAL_H6_NODE_";
   D0010_H6DeleteNodeObjects(prefix);

   if(InpH6NodeDrawChart)
   {
      int max_objects = (InpH6NodeMaxChartObjects <= 0 ? 2147483647 : InpH6NodeMaxChartObjects);
      int max_reaction_objects = (InpH6ReactionMaxChartObjects <= 0 ? 2147483647 : InpH6ReactionMaxChartObjects);
      int drawn = 0;
      for(int i = events_count - 1; i >= 0 && (drawn < max_objects || st.reaction_boxes_drawn < max_reaction_objects); i--)
      {
         int label = DAL_D0010_LABEL_UNKNOWN;
         int dir = 0;
         int known = -1;
         if(!D0010_ClassifyRawEvent(events[i], bars, bars_count, label, dir, known))
            continue;
         if(known < warmup || known + 1 > last)
            continue;
         bool high_node = (events[i].node_type == DAL_NODE_HIGH);
         bool low_node = (events[i].node_type == DAL_NODE_LOW);
         if(!high_node && !low_node)
            continue;

         int tix = -1;
         int bix = -1;
         D0010_H6FindNodeTouchBreak(bars, bars_count, known, events[i].node_price, high_node, last, touch_buffer, break_buffer, tix, bix);
         if(bix <= 0)
         {
            int age = last - known;
            int stage = D0010_H6NodeStage(age, h1, h2, h3);
            if(stage > 0 && InpH6NodeDrawLines && drawn < max_objects)
            {
               if(stage == 1) st.active_stage1++;
               if(stage == 2) st.active_stage2++;
               if(stage == 3) st.active_stage3++;
               color c = D0010_H6NodeStageColor(stage);
               string side = high_node ? "HIGH" : "LOW";
               string stage_text = (stage == 1 ? "H" + IntegerToString(h1) : (stage == 2 ? "H" + IntegerToString(h2) : "H" + IntegerToString(h3)));
               string name = prefix + "LINE_" + stage_text + "_" + IntegerToString(i) + "_" + side;
               string tip = "H6 node survivor line " + stage_text + " " + side + " age=" + IntegerToString(age) + " price=" + DoubleToString(events[i].node_price, _Digits);
               if(D0010_H6DrawNodeLine(name, bars[known].time, bars[last].time, events[i].node_price, c, InpH6NodeLineWidth, tip))
               {
                  drawn++;
                  st.chart_drawn++;
               }
            }
         }

         if(InpH6ReactionBoxDrawChart && st.reaction_boxes_drawn < max_reaction_objects)
         {
            int rx_touch = -1;
            int rx_confirm = -1;
            int rx_retouch = -1;
            double rx_zone_end = events[i].node_price;
            D0010_H6FindReactionBox(bars, bars_count, known, events[i].node_price, high_node, last, touch_buffer, reaction_away_buffer, reaction_retouch_buffer, rx_touch, rx_confirm, rx_retouch, rx_zone_end);
            if(rx_touch > 0)
            {
               int rx_age = 0;
               bool rx_active_box = true;
               int rx_stage = D0010_H6TouchLifecycleStage(rx_touch, rx_retouch, last, h1, h2, h3, rx_age, rx_active_box);

               if(rx_active_box)
               {
                  if(rx_stage == 1) st.reaction_active_stage1++;
                  if(rx_stage == 2) st.reaction_active_stage2++;
                  if(rx_stage == 3) st.reaction_active_stage3++;
               }

               color rc = D0010_H6ReactionStageColor(rx_stage, rx_active_box);
               string side2 = high_node ? "HIGH" : "LOW";
               string rx_stage_text = "PRE_H" + IntegerToString(h1);
               if(rx_stage == 1) rx_stage_text = "H" + IntegerToString(h1);
               else if(rx_stage == 2) rx_stage_text = "H" + IntegerToString(h2);
               else if(rx_stage >= 3) rx_stage_text = "H" + IntegerToString(h3);
               string rx_state_text = rx_active_box ? "ACTIVE" : "CLOSED";
               string rx_name = prefix + "BOX_" + rx_stage_text + "_" + rx_state_text + "_" + IntegerToString(i) + "_" + side2;
               string rx_tip = "H6 reaction box " + rx_stage_text + " " + side2
                  + " originTime=" + TimeToString(bars[known].time)
                  + " touchTime=" + TimeToString(bars[rx_touch].time)
                  + " confirmTime=" + (rx_confirm > 0 ? TimeToString(bars[rx_confirm].time) : "NONE")
                  + " retouchTime=" + (rx_retouch > 0 ? TimeToString(bars[rx_retouch].time) : "NONE")
                  + " active=" + IntegerToString(rx_active_box ? 1 : 0)
                  + " candlesAfterTouchWithoutZoneEndRetouch=" + IntegerToString(rx_age)
                  + " node=" + DoubleToString(events[i].node_price, _Digits)
                  + " touchExtreme=" + DoubleToString(rx_zone_end, _Digits)
                  + " direction=" + (high_node ? "sell_reaction" : "buy_reaction")
                  + " rule=all_touched_nodes_no_regime_filter";
               if(D0010_H6DrawReactionBox(rx_name, bars[known].time, bars[rx_touch].time, events[i].node_price, rx_zone_end, high_node, rc, InpH6NodeLineWidth, rx_tip))
               {
                  st.reaction_boxes_drawn++;
                  st.chart_drawn++;
               }
            }
         }
      }
      ChartRedraw(0);
   }

   string chart_line = "DAL_H0006_NODE_CHART_UPDATE *** build=" + DAL_D0010_BUILD
      + "*drawChart=" + IntegerToString(InpH6NodeDrawChart ? 1 : 0)
      + "*objectsDrawn=" + IntegerToString(st.chart_drawn)
      + "*maxObjects=" + IntegerToString(InpH6NodeMaxChartObjects <= 0 ? -1 : InpH6NodeMaxChartObjects)
      + "*activeRedH" + IntegerToString(h1) + "=" + IntegerToString(st.active_stage1)
      + "*activeGreenH" + IntegerToString(h2) + "=" + IntegerToString(st.active_stage2)
      + "*activePurpleH" + IntegerToString(h3) + "=" + IntegerToString(st.active_stage3)
      + "*reactionBoxesDrawn=" + IntegerToString(st.reaction_boxes_drawn)
      + "*maxReactionBoxes=" + IntegerToString(InpH6ReactionMaxChartObjects <= 0 ? -1 : InpH6ReactionMaxChartObjects)
      + "*reactionActiveRedH" + IntegerToString(h1) + "=" + IntegerToString(st.reaction_active_stage1)
      + "*reactionActiveGreenH" + IntegerToString(h2) + "=" + IntegerToString(st.reaction_active_stage2)
      + "*reactionActivePurpleH" + IntegerToString(h3) + "=" + IntegerToString(st.reaction_active_stage3)
      + "*drawLines=" + IntegerToString(InpH6NodeDrawLines ? 1 : 0)
      + "*drawReactionBoxes=" + IntegerToString(InpH6ReactionBoxDrawChart ? 1 : 0)
      + "*reactionColorRule=age_from_touch_until_zone_end_retouch"
      + "*reactionScope=all_raw_nodes_no_regime_filter"
      + "*objectPrefix=DAL_H6_NODE_"
      + "*updatePolicy=delete_and_redraw_all_reaction_boxes_active_and_closed_plus_optional_lines";
   Print(chart_line);
}

void D0010_PrintH6OptionalityReports(const DALBar &bars[], const int bars_count)
{
   if(!InpAtomicPrintH6OptionalityReport)
      return;
   int hf = MathMax(1, InpH6HorizonBarsFast);
   int hm = MathMax(1, InpH6HorizonBarsMain);
   int hs = MathMax(1, InpH6HorizonBarsSlow);

   if(InpH6CandleStreamMode)
   {
      if(InpH6ReportFastHorizon)
         D0010_H6CandleStreamForHorizon(bars, bars_count, hf, "FAST");
      if(InpH6ReportMainHorizon)
         D0010_H6CandleStreamForHorizon(bars, bars_count, hm, "MAIN");
      if(InpH6ReportSlowHorizon)
         D0010_H6CandleStreamForHorizon(bars, bars_count, hs, "SLOW");
      return;
   }

   if(InpH6ReportFastHorizon)
   {
      D0010_H6OptionalityForHorizon(bars, bars_count, hf, "FAST");
      if(InpAtomicPrintH6EdgeMap && InpH6EdgeMapLevel > 0) D0010_H6EdgeMapForHorizon(bars, bars_count, hf, "FAST");
   }
   if(InpH6ReportMainHorizon)
   {
      D0010_H6OptionalityForHorizon(bars, bars_count, hm, "MAIN");
      if(InpAtomicPrintH6EdgeMap && InpH6EdgeMapLevel > 0) D0010_H6EdgeMapForHorizon(bars, bars_count, hm, "MAIN");
   }
   if(InpH6ReportSlowHorizon)
   {
      D0010_H6OptionalityForHorizon(bars, bars_count, hs, "SLOW");
      if(InpAtomicPrintH6EdgeMap && InpH6EdgeMapLevel > 0) D0010_H6EdgeMapForHorizon(bars, bars_count, hs, "SLOW");
   }
}

void D0010_PrintHumanContextReports(const int &labels[], const int n)
{
   if(!InpAtomicPrintHumanContextReport)
      return;
   D0010_PrintLastOnlyQuality(labels, n);
   D0010_PrintHumanContextState(labels, n, "rolling_fast", MathMax(1, InpAtomicContextKFast), false);
   D0010_PrintHumanContextState(labels, n, "rolling_main", MathMax(1, InpAtomicContextKMain), false);
   D0010_PrintHumanContextState(labels, n, "rolling_slow", MathMax(1, InpAtomicContextKSlow), false);
   D0010_PrintHumanContextState(labels, n, "ewma_human_eye", MathMax(1, InpAtomicContextKMain), true);
   D0010_PrintContextShuffleStress(labels, n);
}

void D0010_PrintExtendedReports(const int &labels[], const int n)
{
   if(!InpAtomicPrintExtendedReport)
      return;
   D0010_PrintLagDecay(labels, n);
   D0010_PrintRunLengthTransition(labels, n);
   D0010_PrintBlockProfile(labels, n, MathMax(5, InpAtomicBlockSizeFast), "FAST");
   D0010_PrintBlockProfile(labels, n, MathMax(10, InpAtomicBlockSizeMain), "MAIN");
   D0010_PrintBlockProfile(labels, n, MathMax(20, InpAtomicBlockSizeSlow), "SLOW");
}

void D0010_PrintPermutationStress(const int &labels[], const int n, const D0010TransitionStats &obs)
{
   int iters = MathMax(0, InpPermutationIterations);
   if(n < 3 || iters <= 0)
   {
      Print("DAL_D0010_ATOMIC_PERM_STRESS *** build=", DAL_D0010_BUILD, "*n=", n, "*iters=0*reason=disabled_or_too_small");
      return;
   }

   double sum_lift = 0.0;
   double sum_lift2 = 0.0;
   double sum_corr = 0.0;
   double sum_corr2 = 0.0;
   int ge_lift = 0;
   int ge_corr = 0;

   for(int iter = 0; iter < iters; iter++)
   {
      int shuffled[];
      D0010_ShuffleLabels(labels, n, iter, shuffled);
      D0010TransitionStats st;
      D0010_ComputeTransitionStats(shuffled, n, st);
      sum_lift += st.same_lift_pct;
      sum_lift2 += st.same_lift_pct * st.same_lift_pct;
      sum_corr += st.lag1_corr;
      sum_corr2 += st.lag1_corr * st.lag1_corr;
      if(st.same_lift_pct >= obs.same_lift_pct) ge_lift++;
      if(st.lag1_corr >= obs.lag1_corr) ge_corr++;
   }

   double mean_lift = sum_lift / iters;
   double var_lift = MathMax(0.0, sum_lift2 / iters - mean_lift * mean_lift);
   double sd_lift = MathSqrt(var_lift);
   double mean_corr = sum_corr / iters;
   double var_corr = MathMax(0.0, sum_corr2 / iters - mean_corr * mean_corr);
   double sd_corr = MathSqrt(var_corr);
   double z_lift = D0010_SafeDiv(obs.same_lift_pct - mean_lift, sd_lift);
   double z_corr = D0010_SafeDiv(obs.lag1_corr - mean_corr, sd_corr);
   double p_lift = D0010_SafeDiv(ge_lift + 1, iters + 1);
   double p_corr = D0010_SafeDiv(ge_corr + 1, iters + 1);

   Print("DAL_D0010_ATOMIC_PERM_STRESS",
      " *** build=", DAL_D0010_BUILD,
      "*contract=atomic_no_sample_raw_m0001_known_time_batches",
      "*null=label_permutation_over_pure_known_time_batches",
      "*n=", n,
      "*iters=", iters,
      "*obsSameLiftPct=", DoubleToString(obs.same_lift_pct, 2),
      "*permMeanSameLiftPct=", DoubleToString(mean_lift, 2),
      "*permSdSameLiftPct=", DoubleToString(sd_lift, 2),
      "*sameLiftZ=", DoubleToString(z_lift, 4),
      "*sameLiftEmpP=", DoubleToString(p_lift, 4),
      "*obsLag1Corr=", DoubleToString(obs.lag1_corr, 4),
      "*permMeanLag1Corr=", DoubleToString(mean_corr, 4),
      "*permSdLag1Corr=", DoubleToString(sd_corr, 4),
      "*lag1Z=", DoubleToString(z_corr, 4),
      "*lag1EmpP=", DoubleToString(p_corr, 4));
}

void D0010_PrintBatch(const int step, const D0010Batch &batch)
{
   Print("DAL_D0010_BATCH",
      " *** build=", DAL_D0010_BUILD,
      "*step=", step,
      "*knownTime=", D0010_TimeText(batch.known_time),
      "*knownIndex=", batch.known_index,
      "*pure=", batch.pure ? 1 : 0,
      "*label=", D0010_LabelText(batch.label),
      "*events=", batch.event_count,
      "*rev=", batch.reversal_count,
      "*cont=", batch.continuation_count,
      "*buyDir=", batch.buy_direction_count,
      "*sellDir=", batch.sell_direction_count,
      "*ambiguousDirection=", batch.ambiguous_direction ? 1 : 0,
      "*reason=", batch.reason);
}


void D0010_SortKnownTriples(int &knowns[], int &labels[], int &dirs[], const int n)
{
   for(int i = 1; i < n; i++)
   {
      int k = knowns[i];
      int l = labels[i];
      int d = dirs[i];
      int j = i - 1;
      while(j >= 0 && (knowns[j] > k || (knowns[j] == k && labels[j] > l)))
      {
         knowns[j + 1] = knowns[j];
         labels[j + 1] = labels[j];
         dirs[j + 1] = dirs[j];
         j--;
      }
      knowns[j + 1] = k;
      labels[j + 1] = l;
      dirs[j + 1] = d;
   }
}

bool D0010_LoadFinalReplayBars(DALBar &bars[], int &bars_count, string &reason)
{
   ArrayResize(bars, 0);
   bars_count = 0;
   reason = "not_loaded";

   int total = Bars(D0010_Symbol(), D0010_Timeframe());
   if(total <= 0)
   {
      reason = "no_bars";
      return false;
   }

   int replay = MathMax(200, InpReplayClosedBars);
   int oldest_shift = MathMin(total - 1, replay);
   int latest_closed_shift = 1;
   if(oldest_shift <= latest_closed_shift + 10)
   {
      reason = "not_enough_closed_bars";
      return false;
   }

   return D0010_LoadPrefixBars(oldest_shift, latest_closed_shift, bars, bars_count, reason);
}

void D0010_ConsumeBatchFromCounts(
   const int known_index,
   const datetime known_time,
   const int event_count,
   const int rev,
   const int cont,
   const int buy,
   const int sell
)
{
   D0010Batch batch;
   D0010_ResetBatch(batch);
   batch.has_events = (event_count > 0);
   batch.known_index = known_index;
   batch.known_time = known_time;
   batch.event_count = event_count;
   batch.reversal_count = rev;
   batch.continuation_count = cont;
   batch.buy_direction_count = buy;
   batch.sell_direction_count = sell;
   batch.ambiguous_direction = (buy > 0 && sell > 0);

   if(event_count <= 0)
      return;

   if(rev > 0 && cont > 0)
   {
      batch.pure = false;
      batch.label = DAL_D0010_LABEL_UNKNOWN;
      batch.reason = "same_known_time_mixed_reversal_continuation";
   }
   else if(rev > 0)
   {
      batch.pure = true;
      batch.label = DAL_D0010_LABEL_REVERSAL;
      batch.reason = "ok_pure_known_time_batch";
   }
   else if(cont > 0)
   {
      batch.pure = true;
      batch.label = DAL_D0010_LABEL_CONTINUATION;
      batch.reason = "ok_pure_known_time_batch";
   }
   else
   {
      batch.pure = false;
      batch.label = DAL_D0010_LABEL_UNKNOWN;
      batch.reason = "unknown_label";
   }

   g_sum.total_batches++;
   g_sum.raw_events_known_now += batch.event_count;
   if(batch.event_count > 1)
   {
      g_sum.same_time_batch_count++;
      g_sum.same_time_event_count += batch.event_count;
   }
   if(batch.ambiguous_direction) g_sum.mixed_direction_batches++;

   if(!batch.pure)
   {
      g_sum.ambiguous_batches++;
      D0010_WriteCsvBatch(batch);
      return;
   }

   g_sum.pure_batches++;
   if(batch.label == DAL_D0010_LABEL_REVERSAL) g_sum.reversal_batches++;
   if(batch.label == DAL_D0010_LABEL_CONTINUATION) g_sum.continuation_batches++;
   D0010_AddPureBatchLabel(batch);
   D0010_WriteCsvBatch(batch);
}

bool D0010_RunFastRawEventBatch()
{
   D0010_ResetSummary(g_sum);
   ArrayResize(g_labels, 0);
   ArrayResize(g_label_times, 0);
   ArrayResize(g_label_batch_counts, 0);
   ArrayResize(g_label_dirs, 0);
   ArrayResize(g_label_known_indices, 0);
   D0010_OpenCsv();

   DALBar bars[];
   int bars_count = 0;
   string reason = "";
   if(!D0010_LoadFinalReplayBars(bars, bars_count, reason))
   {
      Print("DAL_D0010_FAILED *** build=", DAL_D0010_BUILD, "*mode=FAST_RAW_EVENT_BATCH*reason=", reason);
      return false;
   }

   int warmup = MathMax(InpWarmupClosedBars, InpL * 2 + InpExitGap + 50);
   if(bars_count <= warmup + 10)
   {
      Print("DAL_D0010_FAILED *** build=", DAL_D0010_BUILD, "*mode=FAST_RAW_EVENT_BATCH*reason=not_enough_loaded_bars*bars=", bars_count, "*warmup=", warmup);
      return false;
   }

   Print("DAL_D0010_START *** build=", DAL_D0010_BUILD,
      "*symbol=", D0010_Symbol(),
      "*tf=", EnumToString(D0010_Timeframe()),
      "*mode=FAST_RAW_EVENT_BATCH",
      "*contract=no_m0002_no_branch_samples_raw_m0001_events_only",
      "*compute=M0001_once_then_known_time_batch",
      "*sequenceOrder=known_time_batch_sequence",
      "*sameKnownTimeEventsAreSimultaneous=1",
      "*mixedEnergyBatchPolicy=ambiguous_skip_from_transition",
      "*bars=", bars_count,
      "*warmup=", warmup);

   DALM0001Config m1;
   D0010_BuildM0001Config(m1);
   DALLRuleNode nodes[];
   int nodes_count = DAL_DetectConfirmedStructuralNodes(bars, bars_count, m1.L, nodes);
   DALM0001Event events[];
   int events_count = DAL_M0001ComputeEvents(bars, bars_count, nodes, nodes_count, m1, events);

   g_sum.steps = 1;
   g_sum.decision_steps = bars_count - warmup;
   g_sum.raw_events_seen = events_count;

   if(events_count <= 0)
   {
      g_sum.no_event_steps = 1;
      Print("DAL_D0010_AUDIT *** build=", DAL_D0010_BUILD, "*mode=FAST_RAW_EVENT_BATCH*sampleCalls=0*branchSamplesBuilt=0*m0002Calls=0*rawEventsSeen=0*reason=no_events");
      return true;
   }

   int knowns[];
   int labels[];
   int dirs[];
   int n = 0;
   for(int i = 0; i < events_count; i++)
   {
      int label = DAL_D0010_LABEL_UNKNOWN;
      int dir = 0;
      int known = -1;
      if(!D0010_ClassifyRawEvent(events[i], bars, bars_count, label, dir, known))
         continue;
      if(known < warmup || known >= bars_count)
         continue;
      ArrayResize(knowns, n + 1);
      ArrayResize(labels, n + 1);
      ArrayResize(dirs, n + 1);
      knowns[n] = known;
      labels[n] = label;
      dirs[n] = dir;
      n++;
   }

   if(n <= 0)
   {
      g_sum.no_new_known_batch_steps = 1;
      Print("DAL_D0010_AUDIT *** build=", DAL_D0010_BUILD, "*mode=FAST_RAW_EVENT_BATCH*sampleCalls=0*branchSamplesBuilt=0*m0002Calls=0*rawEventsSeen=", events_count, "*knownEvents=0*reason=no_known_events_after_warmup");
      return true;
   }

   D0010_SortKnownTriples(knowns, labels, dirs, n);

   int pos = 0;
   while(pos < n)
   {
      int known = knowns[pos];
      int rev = 0;
      int cont = 0;
      int buy = 0;
      int sell = 0;
      int total = 0;

      while(pos < n && knowns[pos] == known)
      {
         if(labels[pos] == DAL_D0010_LABEL_REVERSAL) rev++;
         if(labels[pos] == DAL_D0010_LABEL_CONTINUATION) cont++;
         if(dirs[pos] > 0) buy++;
         if(dirs[pos] < 0) sell++;
         total++;
         pos++;
      }

      D0010_ConsumeBatchFromCounts(known, bars[known].time, total, rev, cont, buy, sell);
   }

   if(g_csv != INVALID_HANDLE)
      FileFlush(g_csv);

   int label_n = ArraySize(g_labels);
   D0010TransitionStats ts;
   D0010_ComputeTransitionStats(g_labels, label_n, ts);
   D0010RunStats rs;
   D0010_ComputeRuns(g_labels, label_n, ts, rs);

   if(InpAtomicH6OnlyReport && InpH6NodeSurvivalReport)
   {
      string h6_node_audit_line = "DAL_M0006_AUDIT *** build=" + DAL_D0010_BUILD
         + "*officialReport=H0006_NODE_SURVIVAL_MAP"
         + "*mode=FAST_RAW_EVENT_BATCH"
         + "*sampleCalls=0"
         + "*branchSamplesBuilt=0"
         + "*m0002Calls=0"
         + "*m0001ComputePasses=1"
         + "*prefixRebuilds=0"
         + "*contract=no_m0002_no_branch_samples_raw_m0001_events_only"
         + "*sequenceOrder=known_time_batch_sequence"
         + "*sameKnownTimeEventsAreSimultaneous=1"
         + "*bars=" + IntegerToString(bars_count)
         + "*nodes=" + IntegerToString(nodes_count)
         + "*rawEventsSeen=" + IntegerToString(g_sum.raw_events_seen)
         + "*rawEventsKnownNow=" + IntegerToString(g_sum.raw_events_known_now)
         + "*totalBatches=" + IntegerToString(g_sum.total_batches)
         + "*pureBatches=" + IntegerToString(g_sum.pure_batches)
         + "*ambiguousBatches=" + IntegerToString(g_sum.ambiguous_batches)
         + "*horizons=" + IntegerToString(InpH6NodeHorizon1) + "/" + IntegerToString(InpH6NodeHorizon2) + "/" + IntegerToString(InpH6NodeHorizon3)
         + "*chartDraw=" + IntegerToString(InpH6NodeDrawChart ? 1 : 0)
         + "*meaning=node_survives_if_not_broken_after_horizon";
      Print(h6_node_audit_line);
      D0010_H6NodeSurvivalReport(events, events_count, bars, bars_count, nodes_count);
      return true;
   }

   if(InpAtomicH6OnlyReport)
   {
      string h6_audit_line = "DAL_M0006_AUDIT *** build=" + DAL_D0010_BUILD
         + "*officialReport=H0006_ATOMIC_NO_SAMPLE_OPTIONALITY"
         + "*mode=FAST_RAW_EVENT_BATCH"
         + "*sampleCalls=0"
         + "*branchSamplesBuilt=0"
         + "*m0002Calls=0"
         + "*m0001ComputePasses=1"
         + "*prefixRebuilds=0"
         + "*contract=no_m0002_no_branch_samples_raw_m0001_events_only"
         + "*sequenceOrder=known_time_batch_sequence"
         + "*sameKnownTimeEventsAreSimultaneous=1"
         + "*mixedEnergyBatchPolicy=ambiguous_skip_from_transition"
         + "*bars=" + IntegerToString(bars_count)
         + "*nodes=" + IntegerToString(nodes_count)
         + "*rawEventsSeen=" + IntegerToString(g_sum.raw_events_seen)
         + "*rawEventsKnownNow=" + IntegerToString(g_sum.raw_events_known_now)
         + "*totalBatches=" + IntegerToString(g_sum.total_batches)
         + "*pureBatches=" + IntegerToString(g_sum.pure_batches)
         + "*ambiguousBatches=" + IntegerToString(g_sum.ambiguous_batches)
         + "*reversalBatches=" + IntegerToString(g_sum.reversal_batches)
         + "*continuationBatches=" + IntegerToString(g_sum.continuation_batches)
         + "*horizons=" + IntegerToString(InpH6HorizonBarsFast) + "/" + IntegerToString(InpH6HorizonBarsMain) + "/" + IntegerToString(InpH6HorizonBarsSlow)
         + "*atrPeriod=" + IntegerToString(InpH6AtrPeriod)
         + "*h6Engine=" + (InpH6CandleStreamMode ? "CANDLE_FORWARD_STREAM" : "BATCH_FORWARD_SCAN")
         + "*fullHorizonOnly=" + IntegerToString(InpH6RequireFullHorizon ? 1 : 0)
         + "*edgeMap=" + IntegerToString(InpAtomicPrintH6EdgeMap ? 1 : 0);
      Print(h6_audit_line);
      D0010_PrintH6OptionalityReports(bars, bars_count);
      return true;
   }

   Print("DAL_D0010_AUDIT *** build=", DAL_D0010_BUILD,
      "*mode=FAST_RAW_EVENT_BATCH",
      "*sampleCalls=0",
      "*branchSamplesBuilt=0",
      "*m0002Calls=0",
      "*m0001ComputePasses=1",
      "*prefixRebuilds=0",
      "*contract=no_m0002_no_branch_samples_raw_m0001_events_only",
      "*sequenceOrder=known_time_batch_sequence",
      "*sameKnownTimeEventsAreSimultaneous=1",
      "*mixedEnergyBatchPolicy=ambiguous_skip_from_transition",
      "*bars=", bars_count,
      "*nodes=", nodes_count,
      "*rawEventsSeen=", g_sum.raw_events_seen,
      "*rawEventsKnownNow=", g_sum.raw_events_known_now,
      "*eventsCompressedByBatching=", MathMax(0, g_sum.raw_events_known_now - g_sum.total_batches),
      "*internalTransitionsPrevented=", MathMax(0, g_sum.raw_events_known_now - g_sum.total_batches),
      "*totalBatches=", g_sum.total_batches,
      "*pureBatches=", g_sum.pure_batches,
      "*ambiguousBatches=", g_sum.ambiguous_batches,
      "*ambiguousBatchPct=", DoubleToString(D0010_SafePct(g_sum.ambiguous_batches, g_sum.total_batches), 2),
      "*sameTimeBatchCount=", g_sum.same_time_batch_count,
      "*sameTimeBatchPct=", DoubleToString(D0010_SafePct(g_sum.same_time_batch_count, g_sum.total_batches), 2),
      "*sameTimeEventCount=", g_sum.same_time_event_count,
      "*mixedDirectionBatches=", g_sum.mixed_direction_batches,
      "*reversalBatches=", g_sum.reversal_batches,
      "*continuationBatches=", g_sum.continuation_batches);

   D0010_PrintTransitionStats("DAL_D0010_ATOMIC_TRANSITION", ts);
   D0010_PrintRunStats(rs);
   D0010_PrintPermutationStress(g_labels, label_n, ts);
   D0010_PrintRunShuffleStress(g_labels, label_n, rs);
   D0010_PrintBlockConcentrationStress(g_labels, label_n);
   D0010_PrintCircularShiftStress(g_labels, label_n, ts);
   D0010_PrintLocalBlockShuffleStress(g_labels, label_n, ts);
   D0010_PrintExtendedReports(g_labels, label_n);
   D0010_PrintDeepReports(g_labels, g_label_batch_counts, g_label_dirs, label_n, ts);
   D0010_PrintHumanContextReports(g_labels, label_n);
   D0010_PrintH6OptionalityReports(bars, bars_count);
   return true;
}

bool D0010_Run()
{
   D0010_ResetSummary(g_sum);
   ArrayResize(g_labels, 0);
   ArrayResize(g_label_times, 0);
   ArrayResize(g_label_batch_counts, 0);
   ArrayResize(g_label_dirs, 0);
   ArrayResize(g_label_known_indices, 0);
   D0010_OpenCsv();

   int total = Bars(D0010_Symbol(), D0010_Timeframe());
   if(total <= 0)
   {
      Print("DAL_D0010_FAILED *** build=", DAL_D0010_BUILD, "*reason=no_bars");
      return false;
   }

   int replay = MathMax(200, InpReplayClosedBars);
   int oldest_shift = MathMin(total - 1, replay);
   int warmup = MathMax(InpWarmupClosedBars, InpL * 2 + InpExitGap + 50);
   if(oldest_shift <= warmup + 3)
   {
      Print("DAL_D0010_FAILED *** build=", DAL_D0010_BUILD, "*reason=not_enough_bars*oldestShift=", oldest_shift, "*warmup=", warmup);
      return false;
   }

   Print("DAL_D0010_START *** build=", DAL_D0010_BUILD,
      "*symbol=", D0010_Symbol(),
      "*tf=", EnumToString(D0010_Timeframe()),
      "*mode=atomic_no_sample_live_regime_replay",
      "*contract=no_m0002_no_branch_samples_raw_m0001_events_only",
      "*sequenceOrder=known_time_batch_sequence",
      "*sameKnownTimeEventsAreSimultaneous=1",
      "*mixedEnergyBatchPolicy=ambiguous_skip_from_transition");

   for(int cursor_shift = oldest_shift - warmup; cursor_shift >= 2; cursor_shift--)
   {
      g_sum.steps++;
      DALBar bars[];
      int bars_count = 0;
      string load_reason = "";
      if(!D0010_LoadPrefixBars(oldest_shift, cursor_shift, bars, bars_count, load_reason))
      {
         g_sum.load_failures++;
         continue;
      }
      if(bars_count <= InpL * 2 + InpExitGap + 20)
         continue;

      g_sum.decision_steps++;
      int decision_index = bars_count - 1;

      DALM0001Config m1;
      D0010_BuildM0001Config(m1);
      DALLRuleNode nodes[];
      int nodes_count = DAL_DetectConfirmedStructuralNodes(bars, bars_count, m1.L, nodes);
      DALM0001Event events[];
      int events_count = DAL_M0001ComputeEvents(bars, bars_count, nodes, nodes_count, m1, events);
      g_sum.raw_events_seen += events_count;
      if(events_count <= 0)
      {
         g_sum.no_event_steps++;
         continue;
      }

      D0010Batch batch;
      bool pure = D0010_BuildCurrentKnownBatch(events, events_count, bars, bars_count, decision_index, batch);
      if(!batch.has_events)
      {
         g_sum.no_new_known_batch_steps++;
         continue;
      }

      g_sum.total_batches++;
      g_sum.raw_events_known_now += batch.event_count;
      if(batch.event_count > 1)
      {
         g_sum.same_time_batch_count++;
         g_sum.same_time_event_count += batch.event_count;
      }
      if(batch.ambiguous_direction) g_sum.mixed_direction_batches++;
      if(!pure)
      {
         g_sum.ambiguous_batches++;
         D0010_WriteCsvBatch(batch);
         if(!InpSkipAmbiguousEnergyBatch && batch.label != DAL_D0010_LABEL_UNKNOWN)
            D0010_AddPureBatchLabel(batch);
         if(!InpPrintOnlySummary && (g_sum.total_batches % MathMax(1, InpPrintEveryNBatches) == 0 || batch.event_count > 1))
            D0010_PrintBatch(g_sum.steps, batch);
         continue;
      }

      g_sum.pure_batches++;
      if(batch.label == DAL_D0010_LABEL_REVERSAL) g_sum.reversal_batches++;
      if(batch.label == DAL_D0010_LABEL_CONTINUATION) g_sum.continuation_batches++;
      D0010_AddPureBatchLabel(batch);
      D0010_WriteCsvBatch(batch);

      if(!InpPrintOnlySummary && (g_sum.pure_batches % MathMax(1, InpPrintEveryNBatches) == 0 || batch.event_count > 1))
         D0010_PrintBatch(g_sum.steps, batch);
   }

   if(g_csv != INVALID_HANDLE)
      FileFlush(g_csv);

   int n = ArraySize(g_labels);
   D0010TransitionStats ts;
   D0010_ComputeTransitionStats(g_labels, n, ts);
   D0010RunStats rs;
   D0010_ComputeRuns(g_labels, n, ts, rs);

   Print("DAL_D0010_AUDIT *** build=", DAL_D0010_BUILD,
      "*sampleCalls=0",
      "*branchSamplesBuilt=0",
      "*m0002Calls=0",
      "*contract=no_m0002_no_branch_samples_raw_m0001_events_only",
      "*sequenceOrder=known_time_batch_sequence",
      "*sameKnownTimeEventsAreSimultaneous=1",
      "*mixedEnergyBatchPolicy=ambiguous_skip_from_transition",
      "*steps=", g_sum.steps,
      "*decisionSteps=", g_sum.decision_steps,
      "*loadFailures=", g_sum.load_failures,
      "*rawEventsSeen=", g_sum.raw_events_seen,
      "*rawEventsKnownNow=", g_sum.raw_events_known_now,
      "*eventsCompressedByBatching=", MathMax(0, g_sum.raw_events_known_now - g_sum.total_batches),
      "*internalTransitionsPrevented=", MathMax(0, g_sum.raw_events_known_now - g_sum.total_batches),
      "*totalBatches=", g_sum.total_batches,
      "*pureBatches=", g_sum.pure_batches,
      "*ambiguousBatches=", g_sum.ambiguous_batches,
      "*ambiguousBatchPct=", DoubleToString(D0010_SafePct(g_sum.ambiguous_batches, g_sum.total_batches), 2),
      "*sameTimeBatchCount=", g_sum.same_time_batch_count,
      "*sameTimeBatchPct=", DoubleToString(D0010_SafePct(g_sum.same_time_batch_count, g_sum.total_batches), 2),
      "*sameTimeEventCount=", g_sum.same_time_event_count,
      "*mixedDirectionBatches=", g_sum.mixed_direction_batches,
      "*reversalBatches=", g_sum.reversal_batches,
      "*continuationBatches=", g_sum.continuation_batches,
      "*noEventSteps=", g_sum.no_event_steps,
      "*noNewKnownBatchSteps=", g_sum.no_new_known_batch_steps);

   D0010_PrintTransitionStats("DAL_D0010_ATOMIC_TRANSITION", ts);
   D0010_PrintRunStats(rs);
   D0010_PrintPermutationStress(g_labels, n, ts);
   D0010_PrintRunShuffleStress(g_labels, n, rs);
   D0010_PrintBlockConcentrationStress(g_labels, n);
   D0010_PrintCircularShiftStress(g_labels, n, ts);
   D0010_PrintLocalBlockShuffleStress(g_labels, n, ts);
   D0010_PrintExtendedReports(g_labels, n);
   D0010_PrintDeepReports(g_labels, g_label_batch_counts, g_label_dirs, n, ts);
   D0010_PrintHumanContextReports(g_labels, n);
   DALBar final_bars[];
   int final_bars_count = 0;
   string final_reason = "";
   if(D0010_LoadFinalReplayBars(final_bars, final_bars_count, final_reason))
      D0010_PrintH6OptionalityReports(final_bars, final_bars_count);
   return true;
}

bool DAL_M0004RunAtomicNoSampleReport(const DALM0004AtomicNoSampleConfig &config)
{
   g_dal_m0004_atomic_cfg = config;
   if(g_dal_m0004_atomic_cfg.report_mode == DAL_M0004_ATOMIC_STRICT_PREFIX_REPLAY)
      return D0010_Run();
   return D0010_RunFastRawEventBatch();
}

void DAL_M0004CloseAtomicNoSampleReport()
{
   if(g_csv != INVALID_HANDLE)
   {
      FileClose(g_csv);
      g_csv = INVALID_HANDLE;
   }
}

#undef InpAtomicReportMode
#undef InpSymbol
#undef InpTimeframe
#undef InpReplayClosedBars
#undef InpWarmupClosedBars
#undef InpL
#undef InpZoneRatio
#undef InpExitGap
#undef InpConsumeMode
#undef InpOutcomeCandleOffsetAfterExit
#undef InpRequireEventRtvReady
#undef InpSkipAmbiguousEnergyBatch
#undef InpPermutationIterations
#undef InpAtomicPrintExtendedReport
#undef InpAtomicPrintDeepReport
#undef InpAtomicPrintH6OptionalityReport
#undef InpAtomicPrintH6EdgeMap
#undef InpAtomicH6OnlyReport
#undef InpH6MinBucketN
#undef InpAtomicStressTransitionPermutation
#undef InpAtomicStressRunShuffle
#undef InpAtomicStressBlockConcentration
#undef InpAtomicStressCircularShift
#undef InpAtomicStressLocalBlockShuffle
#undef InpAtomicStressH6Optionality
#undef InpH6StressMode
#undef InpH6EdgeMapLevel
#undef InpH6EntryAnchorMode
#undef InpH6ReportFastHorizon
#undef InpH6ReportMainHorizon
#undef InpH6ReportSlowHorizon
#undef InpH6PrintComputeAudit
#undef InpH6CandleStreamMode
#undef InpH6RequireFullHorizon
#undef InpH6NodeSurvivalReport
#undef InpH6NodeDrawChart
#undef InpH6NodeDrawLines
#undef InpH6ReactionBoxReport
#undef InpH6ReactionBoxDrawChart
#undef InpH6ReactionAwayBufferPoints
#undef InpH6ReactionZoneEndBufferPoints
#undef InpH6ReactionMinBoxHeightPoints
#undef InpH6ReactionMaxChartObjects
#undef InpH6ReactionBoxFill
#undef InpH6ReactionBoxBack
#undef InpH6NodeHorizon1
#undef InpH6NodeHorizon2
#undef InpH6NodeHorizon3
#undef InpH6NodeTouchBufferPoints
#undef InpH6NodeBreakBufferPoints
#undef InpH6NodeMaxChartObjects
#undef InpH6NodeLineWidth
#undef InpH6NodeColor1
#undef InpH6NodeColor2
#undef InpH6NodeColor3
#undef InpAtomicPrintHumanContextReport
#undef InpAtomicStressContextShuffle
#undef InpH6HorizonBarsFast
#undef InpH6HorizonBarsMain
#undef InpH6HorizonBarsSlow
#undef InpH6AtrPeriod
#undef InpH6TailAtr1
#undef InpH6TailAtr2
#undef InpH6TailAtr3
#undef InpAtomicContextKFast
#undef InpAtomicContextKMain
#undef InpAtomicContextKSlow
#undef InpAtomicContextEwmaAlpha
#undef InpAtomicContextStrongThreshold
#undef InpAtomicCircularMinShiftBatches
#undef InpAtomicLocalBlockShuffleSize
#undef InpAtomicBlockSizeFast
#undef InpAtomicBlockSizeMain
#undef InpAtomicBlockSizeSlow
#undef InpPrintOnlySummary
#undef InpPrintEveryNBatches
#undef InpWriteCsv
#undef InpCsvFileName

#endif
