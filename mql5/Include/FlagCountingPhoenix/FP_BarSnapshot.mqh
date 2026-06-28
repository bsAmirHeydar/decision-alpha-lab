#ifndef __FP_BAR_SNAPSHOT_MQH__
#define __FP_BAR_SNAPSHOT_MQH__
#property strict

// ============================================================================
// FlagCounting Phoenix - Level 01 / Bar Snapshot
// ----------------------------------------------------------------------------
// This module is intentionally tiny. It owns the normalized per-bar diagnostic
// view used by the timebase contract. Structural engines still consume
// MqlRates[] directly, but this snapshot gives Level 01 a stable audit shape.
//
// Important: open/close/volume are used here only for data sanity diagnostics.
// They are not structural inputs for nodes, flags, hooks, or sequence logic.
// ============================================================================

struct FP_BarSnapshot
{
   int       index;
   datetime  time;
   double    open;
   double    high;
   double    low;
   double    close;
   long      tick_volume;
   int       spread;
   long      real_volume;
   bool      valid;
   string    reason;
};

void FP_ResetBarSnapshot(FP_BarSnapshot &b)
{
   b.index = -1;
   b.time = 0;
   b.open = 0.0;
   b.high = 0.0;
   b.low = 0.0;
   b.close = 0.0;
   b.tick_volume = 0;
   b.spread = 0;
   b.real_volume = 0;
   b.valid = false;
   b.reason = "reset";
}

bool FP_BarOhlcIsValid(const double open,
                       const double high,
                       const double low,
                       const double close,
                       const double eps,
                       string &reason)
{
   reason = "ok";
   if(high + eps < low)
   {
      reason = "high_below_low";
      return false;
   }
   if(open > high + eps || open < low - eps)
   {
      reason = "open_outside_high_low";
      return false;
   }
   if(close > high + eps || close < low - eps)
   {
      reason = "close_outside_high_low";
      return false;
   }
   return true;
}

bool FP_BarSnapshotFromRate(const MqlRates &rate,
                            const int index,
                            const double eps,
                            FP_BarSnapshot &b)
{
   FP_ResetBarSnapshot(b);
   b.index = index;
   b.time = rate.time;
   b.open = rate.open;
   b.high = rate.high;
   b.low = rate.low;
   b.close = rate.close;
   b.tick_volume = rate.tick_volume;
   b.spread = rate.spread;
   b.real_volume = rate.real_volume;

   string reason = "ok";
   b.valid = FP_BarOhlcIsValid(rate.open, rate.high, rate.low, rate.close, eps, reason);
   b.reason = reason;
   return b.valid;
}

string FP_BarSnapshotAudit(const FP_BarSnapshot &b, const int digits)
{
   return "idx=" + IntegerToString(b.index) +
          " time=" + TimeToString(b.time, TIME_DATE|TIME_SECONDS) +
          " O=" + DoubleToString(b.open, digits) +
          " H=" + DoubleToString(b.high, digits) +
          " L=" + DoubleToString(b.low, digits) +
          " C=" + DoubleToString(b.close, digits) +
          " valid=" + (b.valid ? "true" : "false") +
          " reason=" + b.reason;
}

#endif // __FP_BAR_SNAPSHOT_MQH__
