#ifndef __FP_TIMEBASE_MQH__
#define __FP_TIMEBASE_MQH__
#property strict

#include "FP_SeriesContract.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 01 / Candle Stream and Timebase
// ----------------------------------------------------------------------------
// This is the single gateway from terminal history into Phoenix structural
// engines. Higher layers must receive canonical bars from here, not call
// CopyRates privately.
// ============================================================================

int FP_TimebaseMaxInt(const int a, const int b)
{
   return (a > b ? a : b);
}

int FP_TimebaseRequestedCopyBars(const FP_TimebaseConfig &cfg)
{
   int requested = cfg.requested_bars;
   if(requested < 1) requested = 1;

   int min_needed = cfg.min_closed_bars;
   if(min_needed < 1) min_needed = 1;

   int live_pad = (cfg.exclude_live_bar ? 1 : 0);
   return FP_TimebaseMaxInt(requested + live_pad, min_needed + live_pad);
}

int FP_LoadCanonicalRates(const FP_TimebaseConfig &cfg,
                          MqlRates &canonical_rates[],
                          FP_TimebaseReport &report)
{
   FP_ResetTimebaseReport(report);
   ArrayResize(canonical_rates, 0);
   ArraySetAsSeries(canonical_rates, false);

   report.symbol = cfg.symbol;
   report.period = cfg.period;
   report.requested_bars = cfg.requested_bars;
   report.min_closed_bars = cfg.min_closed_bars;
   report.exclude_live_bar = cfg.exclude_live_bar;
   report.require_ascending_time = cfg.require_ascending_time;
   report.strict_contract = cfg.strict_contract;

   int copy_bars = FP_TimebaseRequestedCopyBars(cfg);
   report.requested_copy_bars = copy_bars;

   MqlRates raw_rates[];
   ArraySetAsSeries(raw_rates, false);
   int copied = CopyRates(cfg.symbol, cfg.period, 0, copy_bars, raw_rates);
   ArraySetAsSeries(raw_rates, false);

   report.raw_array_as_series = ArrayGetAsSeries(raw_rates);
   report.raw_bars = copied;

   if(copied <= 0)
   {
      report.ok = false;
      report.status = "copy_rates_failed";
      report.reason = "CopyRates_returned_no_bars";
      return 0;
   }

   report.newest_raw_time = raw_rates[copied - 1].time;

   int available = copied;
   if(cfg.exclude_live_bar)
   {
      if(available <= 1)
      {
         report.ok = false;
         report.status = "no_closed_bar_after_live_drop";
         report.reason = "raw_history_contains_only_live_bar";
         return 0;
      }
      report.excluded_live_time = raw_rates[available - 1].time;
      report.dropped_live_bars = 1;
      available--;
   }

   int keep = available;
   if(cfg.requested_bars > 0 && keep > cfg.requested_bars)
      keep = cfg.requested_bars;

   int start = available - keep;
   report.dropped_old_bars = FP_TimebaseMaxInt(0, start);

   ArrayResize(canonical_rates, keep);
   for(int i=0; i<keep; i++)
      canonical_rates[i] = raw_rates[start + i];
   ArraySetAsSeries(canonical_rates, false);

   FP_ValidateCanonicalRates(canonical_rates, keep, cfg, report);
   return keep;
}

string FP_TimebaseBool(const bool v)
{
   return (v ? "true" : "false");
}

string FP_TimebaseTime(const datetime t)
{
   if(t <= 0) return "none";
   return TimeToString(t, TIME_DATE|TIME_SECONDS);
}

void FP_PrintTimebaseReport(const string tag, const FP_TimebaseReport &r)
{
   Print(tag,
         " status=", r.status,
         " ok=", FP_TimebaseBool(r.ok),
         " reason=", r.reason,
         " symbol=", r.symbol,
         " tf=", EnumToString(r.period),
         " requested=", r.requested_bars,
         " copy_requested=", r.requested_copy_bars,
         " raw=", r.raw_bars,
         " canonical=", r.canonical_bars,
         " min_closed=", r.min_closed_bars,
         " closed_only=", FP_TimebaseBool(r.exclude_live_bar),
         " dropped_live=", r.dropped_live_bars,
         " dropped_old=", r.dropped_old_bars,
         " raw_series=", FP_TimebaseBool(r.raw_array_as_series),
         " canonical_series=", FP_TimebaseBool(r.canonical_array_as_series),
         " ascending=", FP_TimebaseBool(r.time_ascending),
         " strict_time=", FP_TimebaseBool(r.strict_increasing_time),
         " duplicate_time=", FP_TimebaseBool(r.duplicate_time_found),
         " ohlc=", FP_TimebaseBool(r.ohlc_valid),
         " first_idx=", r.first_index,
         " last_idx=", r.last_index,
         " first_time=", FP_TimebaseTime(r.first_time),
         " last_time=", FP_TimebaseTime(r.last_time),
         " newest_raw=", FP_TimebaseTime(r.newest_raw_time),
         " excluded_live=", FP_TimebaseTime(r.excluded_live_time),
         " bad_time_idx=", r.invalid_time_index,
         " duplicate_idx=", r.duplicate_time_index,
         " bad_ohlc_idx=", r.invalid_ohlc_index);
}

void FP_PrintTimebaseSamples(const string tag, const MqlRates &rates[], const int total)
{
   if(total <= 0)
   {
      Print(tag, " no_samples total=0");
      return;
   }

   FP_BarSnapshot first;
   FP_BarSnapshot last;
   FP_BarSnapshotFromRate(rates[0], 0, 0.0, first);
   FP_BarSnapshotFromRate(rates[total - 1], total - 1, 0.0, last);

   Print(tag, " sample_first ", FP_BarSnapshotAudit(first, _Digits));
   Print(tag, " sample_last ", FP_BarSnapshotAudit(last, _Digits));
}

#endif // __FP_TIMEBASE_MQH__
