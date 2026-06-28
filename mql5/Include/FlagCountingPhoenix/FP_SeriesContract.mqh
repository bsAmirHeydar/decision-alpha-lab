#ifndef __FP_SERIES_CONTRACT_MQH__
#define __FP_SERIES_CONTRACT_MQH__
#property strict

#include "FP_BarSnapshot.mqh"
#include "FP_TimebaseTypes.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 01 / Series Contract
// ----------------------------------------------------------------------------
// Canonical bar convention:
//   - ArraySetAsSeries(rates, false)
//   - index 0 is the oldest canonical bar
//   - newer bars have higher indices
//   - the current forming live bar is excluded by default
//
// This module validates that convention before any structural engine runs.
// ============================================================================

bool FP_RatesHaveAscendingTime(const MqlRates &rates[], const int total, int &bad_index)
{
   bad_index = -1;
   if(total <= 1) return true;
   for(int i=1; i<total; i++)
   {
      if(rates[i].time < rates[i - 1].time)
      {
         bad_index = i;
         return false;
      }
   }
   return true;
}

bool FP_RatesHaveStrictIncreasingTime(const MqlRates &rates[], const int total, int &bad_index, int &duplicate_index)
{
   bad_index = -1;
   duplicate_index = -1;
   if(total <= 1) return true;
   for(int i=1; i<total; i++)
   {
      if(rates[i].time < rates[i - 1].time)
      {
         bad_index = i;
         return false;
      }
      if(rates[i].time == rates[i - 1].time)
      {
         duplicate_index = i;
         return false;
      }
   }
   return true;
}

bool FP_RatesHaveValidOhlc(const MqlRates &rates[], const int total, const double eps, int &bad_index, string &bad_reason)
{
   bad_index = -1;
   bad_reason = "ok";
   for(int i=0; i<total; i++)
   {
      string reason = "ok";
      if(!FP_BarOhlcIsValid(rates[i].open, rates[i].high, rates[i].low, rates[i].close, eps, reason))
      {
         bad_index = i;
         bad_reason = reason;
         return false;
      }
   }
   return true;
}

bool FP_ValidateCanonicalRates(const MqlRates &rates[],
                               const int total,
                               const FP_TimebaseConfig &cfg,
                               FP_TimebaseReport &r)
{
   r.canonical_bars = total;
   r.canonical_array_as_series = ArrayGetAsSeries(rates);

   if(total > 0)
   {
      r.first_index = 0;
      r.last_index = total - 1;
      r.first_time = rates[0].time;
      r.last_time = rates[total - 1].time;
   }

   if(total < cfg.min_closed_bars)
   {
      r.ok = false;
      r.status = "not_enough_closed_bars";
      r.reason = "canonical_bars_below_minimum";
      return false;
   }

   int time_bad = -1;
   r.time_ascending = FP_RatesHaveAscendingTime(rates, total, time_bad);
   r.invalid_time_index = time_bad;

   int strict_bad = -1;
   int duplicate_bad = -1;
   r.strict_increasing_time = FP_RatesHaveStrictIncreasingTime(rates, total, strict_bad, duplicate_bad);
   r.duplicate_time_index = duplicate_bad;
   r.duplicate_time_found = (duplicate_bad >= 0);
   if(!r.strict_increasing_time && strict_bad >= 0)
      r.invalid_time_index = strict_bad;

   string ohlc_reason = "ok";
   int ohlc_bad = -1;
   r.ohlc_valid = FP_RatesHaveValidOhlc(rates, total, 0.0, ohlc_bad, ohlc_reason);
   r.invalid_ohlc_index = ohlc_bad;

   if(cfg.require_ascending_time && !r.time_ascending)
   {
      r.ok = false;
      r.status = "time_not_ascending";
      r.reason = "canonical_time_order_broken";
      return false;
   }

   if(cfg.require_ascending_time && !r.strict_increasing_time)
   {
      r.ok = false;
      r.status = (r.duplicate_time_found ? "duplicate_bar_time" : "time_not_strictly_increasing");
      r.reason = (r.duplicate_time_found ? "duplicate_bar_time" : "strict_time_order_broken");
      return false;
   }

   if(!r.ohlc_valid)
   {
      r.ok = false;
      r.status = "invalid_ohlc";
      r.reason = ohlc_reason;
      return false;
   }

   if(r.canonical_array_as_series)
   {
      r.ok = false;
      r.status = "canonical_array_is_series";
      r.reason = "expected_ArraySetAsSeries_false";
      return false;
   }

   r.ok = true;
   r.status = "ok";
   r.reason = "canonical_timebase_ready";
   return true;
}

#endif // __FP_SERIES_CONTRACT_MQH__
