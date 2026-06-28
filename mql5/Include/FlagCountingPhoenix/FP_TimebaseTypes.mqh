#ifndef __FP_TIMEBASE_TYPES_MQH__
#define __FP_TIMEBASE_TYPES_MQH__
#property strict

// ============================================================================
// FlagCounting Phoenix - Level 01 / Timebase Types
// ----------------------------------------------------------------------------
// Owns the input/output contracts for canonical candle loading. Keeping these
// structs isolated makes debugging easy and prevents higher engines from growing
// implicit timebase assumptions.
// ============================================================================

struct FP_TimebaseConfig
{
   string          symbol;
   ENUM_TIMEFRAMES period;
   int             requested_bars;
   int             min_closed_bars;
   bool            exclude_live_bar;
   bool            require_ascending_time;
   bool            strict_contract;
   bool            print_sanity;
   bool            print_samples;
};

struct FP_TimebaseReport
{
   bool      ok;
   string    status;
   string    reason;

   string    symbol;
   ENUM_TIMEFRAMES period;
   int       requested_bars;
   int       requested_copy_bars;
   int       min_closed_bars;

   bool      exclude_live_bar;
   bool      require_ascending_time;
   bool      strict_contract;
   bool      raw_array_as_series;
   bool      canonical_array_as_series;

   int       raw_bars;
   int       canonical_bars;
   int       dropped_live_bars;
   int       dropped_old_bars;

   bool      time_ascending;
   bool      strict_increasing_time;
   bool      duplicate_time_found;
   bool      ohlc_valid;

   int       first_index;
   int       last_index;
   int       invalid_time_index;
   int       duplicate_time_index;
   int       invalid_ohlc_index;

   datetime  first_time;
   datetime  last_time;
   datetime  newest_raw_time;
   datetime  excluded_live_time;
};

void FP_DefaultTimebaseConfig(FP_TimebaseConfig &cfg)
{
   cfg.symbol = _Symbol;
   cfg.period = _Period;
   cfg.requested_bars = 5000;
   cfg.min_closed_bars = 200;
   cfg.exclude_live_bar = true;
   cfg.require_ascending_time = true;
   cfg.strict_contract = true;
   cfg.print_sanity = true;
   cfg.print_samples = false;
}

void FP_ResetTimebaseReport(FP_TimebaseReport &r)
{
   r.ok = false;
   r.status = "reset";
   r.reason = "reset";

   r.symbol = "";
   r.period = PERIOD_CURRENT;
   r.requested_bars = 0;
   r.requested_copy_bars = 0;
   r.min_closed_bars = 0;

   r.exclude_live_bar = true;
   r.require_ascending_time = true;
   r.strict_contract = true;
   r.raw_array_as_series = false;
   r.canonical_array_as_series = false;

   r.raw_bars = 0;
   r.canonical_bars = 0;
   r.dropped_live_bars = 0;
   r.dropped_old_bars = 0;

   r.time_ascending = false;
   r.strict_increasing_time = false;
   r.duplicate_time_found = false;
   r.ohlc_valid = false;

   r.first_index = -1;
   r.last_index = -1;
   r.invalid_time_index = -1;
   r.duplicate_time_index = -1;
   r.invalid_ohlc_index = -1;

   r.first_time = 0;
   r.last_time = 0;
   r.newest_raw_time = 0;
   r.excluded_live_time = 0;
}

#endif // __FP_TIMEBASE_TYPES_MQH__
