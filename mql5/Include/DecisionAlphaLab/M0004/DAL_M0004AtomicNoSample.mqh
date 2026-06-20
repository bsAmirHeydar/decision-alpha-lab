#ifndef __DAL_M0004_ATOMIC_NO_SAMPLE_MQH__
#define __DAL_M0004_ATOMIC_NO_SAMPLE_MQH__

#include <DecisionAlphaLab/Market/DAL_Bars.mqh>
#include <DecisionAlphaLab/StructuralNodes/DAL_StructuralNodeEngine.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Config.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Engine.mqh>

struct DALM0004AtomicNoSampleConfig
{
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
   bool print_only_summary;
   int print_every_n_batches;
   bool write_csv;
   string csv_file_name;
};

DALM0004AtomicNoSampleConfig g_dal_m0004_atomic_cfg;

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
#define InpPrintOnlySummary g_dal_m0004_atomic_cfg.print_only_summary
#define InpPrintEveryNBatches g_dal_m0004_atomic_cfg.print_every_n_batches
#define InpWriteCsv g_dal_m0004_atomic_cfg.write_csv
#define InpCsvFileName g_dal_m0004_atomic_cfg.csv_file_name

#define DAL_D0010_BUILD "M0004_MAIN_ATOMIC_1.00"
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
   g_labels[n] = batch.label;
   g_label_times[n] = batch.known_time;
   g_label_batch_counts[n] = batch.event_count;
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

bool D0010_Run()
{
   D0010_ResetSummary(g_sum);
   ArrayResize(g_labels, 0);
   ArrayResize(g_label_times, 0);
   ArrayResize(g_label_batch_counts, 0);
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
   return true;
}

bool DAL_M0004RunAtomicNoSampleReport(const DALM0004AtomicNoSampleConfig &config)
{
   g_dal_m0004_atomic_cfg = config;
   return D0010_Run();
}

void DAL_M0004CloseAtomicNoSampleReport()
{
   if(g_csv != INVALID_HANDLE)
   {
      FileClose(g_csv);
      g_csv = INVALID_HANDLE;
   }
}

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
#undef InpPrintOnlySummary
#undef InpPrintEveryNBatches
#undef InpWriteCsv
#undef InpCsvFileName

#endif
