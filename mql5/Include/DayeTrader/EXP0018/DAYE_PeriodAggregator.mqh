#ifndef __EXP0018_DAYE_PERIOD_AGGREGATOR_MQH__
#define __EXP0018_DAYE_PERIOD_AGGREGATOR_MQH__

#include <DayeTrader/EXP0018/DAYE_PeriodIdentity.mqh>
#include <DayeTrader/EXP0018/DAYE_DataSynchronizer.mqh>

bool DAYE_ValidatePeriodAggregationConfig(const DAYE_PeriodAggregationConfig &config,string &reason_code)
{
   reason_code = "";
   string data_reason = "";
   if(!DAYE_ValidateDataSyncConfig(config.data_config,data_reason))
   {
      reason_code = "data_config:" + data_reason;
      return false;
   }

   int base_seconds = PeriodSeconds(config.data_config.base_timeframe);
   if(base_seconds <= 0 || base_seconds > 1800 || (1800 % base_seconds) != 0)
   {
      reason_code = "base_timeframe_must_evenly_divide_30_minutes";
      return false;
   }
   if(!config.include_daily_periods && !config.include_session_periods && !config.include_subcycle_periods)
   {
      reason_code = "at_least_one_period_family_must_be_enabled";
      return false;
   }
   if(config.include_weekly_periods)
   {
      reason_code = "weekly_period_blocked_until_ADR_DY_A03_is_accepted";
      return false;
   }
   if(config.minimum_publishable_coverage_percent < 0.0 || config.minimum_publishable_coverage_percent > 100.0)
   {
      reason_code = "minimum_publishable_coverage_percent_out_of_range";
      return false;
   }
   if(config.minimum_complete_paired_periods < 0)
   {
      reason_code = "minimum_complete_paired_periods_negative";
      return false;
   }
   if(config.maximum_periods_to_publish < 1)
   {
      reason_code = "maximum_periods_to_publish_below_one";
      return false;
   }
   if(config.force_full_refresh_seconds < 1)
   {
      reason_code = "force_full_refresh_seconds_below_one";
      return false;
   }
   return true;
}

int DAYE_FindSymbolPeriodByInstanceId(const DAYE_SymbolPeriodSnapshot &items[],const string period_instance_id)
{
   for(int i=ArraySize(items)-1;i>=0;i--)
      if(items[i].period_instance_id == period_instance_id)
         return i;
   return -1;
}

void DAYE_InitializeSymbolPeriodSnapshot(const DAYE_SymbolBar &bar,
                                         const DAYE_PeriodWindow &window,
                                         const string trading_day_key,
                                         const int base_seconds,
                                         const datetime processing_time_utc,
                                         DAYE_SymbolPeriodSnapshot &snapshot)
{
   ZeroMemory(snapshot);
   snapshot.schema_version = DAYE_PERIOD_AGG_SCHEMA_VERSION;
   snapshot.status = DAYE_PERIOD_STATUS_OK;
   snapshot.reason_code = "accumulating";
   snapshot.completeness = DAYE_PERIOD_COMPLETENESS_UNKNOWN;
   snapshot.is_publishable = false;
   snapshot.is_replay_safe = bar.is_replay_safe;
   snapshot.broker_symbol = bar.broker_symbol;
   snapshot.canonical_symbol = bar.canonical_symbol;
   snapshot.base_timeframe = bar.timeframe;
   snapshot.base_bar_seconds = base_seconds;
   snapshot.period_id = window.period_id;
   snapshot.period_family = window.family;
   snapshot.period_code = window.code;
   snapshot.period_instance_id = window.instance_id;
   snapshot.trading_day_key = trading_day_key;
   snapshot.window = window;
   snapshot.event_time_utc = window.start_utc;
   snapshot.processing_time_utc = processing_time_utc;
   snapshot.snapshot_id = "";
   snapshot.open = 0.0;
   snapshot.high = 0.0;
   snapshot.low = 0.0;
   snapshot.close = 0.0;
}

bool DAYE_AccumulateBarIntoPeriod(const DAYE_SymbolBar &bar,
                                  const DAYE_PeriodWindow &window,
                                  const string trading_day_key,
                                  const int base_seconds,
                                  const datetime processing_time_utc,
                                  DAYE_SymbolPeriodSnapshot &items[])
{
   if(!DAYE_PeriodWindowContainsBar(window,bar))
      return false;

   int index = DAYE_FindSymbolPeriodByInstanceId(items,window.instance_id);
   if(index < 0)
   {
      index = ArraySize(items);
      ArrayResize(items,index + 1);
      DAYE_InitializeSymbolPeriodSnapshot(bar,window,trading_day_key,base_seconds,processing_time_utc,items[index]);
   }

   DAYE_SymbolPeriodSnapshot snapshot = items[index];
   long offset = (long)bar.event_time_utc - (long)window.start_utc;
   if(offset < 0 || (base_seconds > 0 && (offset % base_seconds) != 0))
      snapshot.invalid_grid_bar_count++;

   string source_bar_id = DAYE_BuildSourceBarId(bar);
   if(snapshot.observed_bar_count == 0)
   {
      snapshot.open = bar.open;
      snapshot.high = bar.high;
      snapshot.low = bar.low;
      snapshot.high_first_time_utc = bar.event_time_utc;
      snapshot.high_last_time_utc = bar.event_time_utc;
      snapshot.low_first_time_utc = bar.event_time_utc;
      snapshot.low_last_time_utc = bar.event_time_utc;
      snapshot.high_first_source_bar_id = source_bar_id;
      snapshot.high_last_source_bar_id = source_bar_id;
      snapshot.low_first_source_bar_id = source_bar_id;
      snapshot.low_last_source_bar_id = source_bar_id;
      snapshot.first_source_bar_utc = bar.event_time_utc;
      snapshot.first_source_bar_id = source_bar_id;
   }
   else
   {
      if(bar.high > snapshot.high)
      {
         snapshot.high = bar.high;
         snapshot.high_first_time_utc = bar.event_time_utc;
         snapshot.high_last_time_utc = bar.event_time_utc;
         snapshot.high_first_source_bar_id = source_bar_id;
         snapshot.high_last_source_bar_id = source_bar_id;
      }
      else if(bar.high == snapshot.high)
      {
         snapshot.high_last_time_utc = bar.event_time_utc;
         snapshot.high_last_source_bar_id = source_bar_id;
      }

      if(bar.low < snapshot.low)
      {
         snapshot.low = bar.low;
         snapshot.low_first_time_utc = bar.event_time_utc;
         snapshot.low_last_time_utc = bar.event_time_utc;
         snapshot.low_first_source_bar_id = source_bar_id;
         snapshot.low_last_source_bar_id = source_bar_id;
      }
      else if(bar.low == snapshot.low)
      {
         snapshot.low_last_time_utc = bar.event_time_utc;
         snapshot.low_last_source_bar_id = source_bar_id;
      }
   }

   snapshot.close = bar.close;
   snapshot.observed_bar_count++;
   snapshot.tick_volume += bar.tick_volume;
   snapshot.real_volume += bar.real_volume;
   snapshot.spread_sum += bar.spread;
   snapshot.last_source_bar_utc = bar.event_time_utc;
   snapshot.last_source_close_utc = bar.close_time_utc;
   snapshot.last_source_bar_id = DAYE_BuildSourceBarId(bar);
   if(!bar.is_replay_safe) snapshot.is_replay_safe = false;
   snapshot.availability_time_utc = bar.close_time_utc;
   snapshot.snapshot_id = DAYE_BuildSymbolPeriodSnapshotId(snapshot);
   items[index] = snapshot;
   return true;
}

void DAYE_FinalizeSymbolPeriodSnapshot(DAYE_SymbolPeriodSnapshot &snapshot,
                                       const datetime now_utc,
                                       const DAYE_PeriodAggregationConfig &config)
{
   int expected = 0;
   long elapsed = (long)snapshot.window.end_utc - (long)snapshot.window.start_utc;
   if(snapshot.base_bar_seconds > 0 && elapsed > 0 && (elapsed % snapshot.base_bar_seconds) == 0)
      expected = (int)(elapsed / snapshot.base_bar_seconds);
   snapshot.expected_bar_count = expected;
   snapshot.period_is_open = (now_utc < snapshot.window.end_utc);
   snapshot.left_edge_truncated = (snapshot.observed_bar_count > 0 && snapshot.first_source_bar_utc > snapshot.window.start_utc);
   datetime expected_last = snapshot.window.end_utc - snapshot.base_bar_seconds;
   snapshot.right_edge_truncated = (!snapshot.period_is_open && snapshot.observed_bar_count > 0 && snapshot.last_source_bar_utc < expected_last);

   snapshot.missing_bar_count = expected - snapshot.observed_bar_count;
   if(snapshot.missing_bar_count < 0)
   {
      snapshot.unexpected_bar_count = -snapshot.missing_bar_count;
      snapshot.missing_bar_count = 0;
   }
   else
      snapshot.unexpected_bar_count = 0;

   snapshot.coverage_percent = 0.0;
   if(expected > 0)
      snapshot.coverage_percent = 100.0 * (double)snapshot.observed_bar_count / (double)expected;

   if(expected <= 0 || snapshot.invalid_grid_bar_count > 0 || snapshot.unexpected_bar_count > 0)
   {
      snapshot.status = DAYE_PERIOD_STATUS_INVALID_BAR_MEMBERSHIP;
      snapshot.reason_code = "invalid_expected_grid_or_membership";
      snapshot.completeness = DAYE_PERIOD_COMPLETENESS_INVALID;
      snapshot.is_publishable = false;
      return;
   }

   if(snapshot.observed_bar_count == 0)
   {
      snapshot.status = DAYE_PERIOD_STATUS_SOURCE_UNAVAILABLE;
      snapshot.reason_code = "no_source_bars_in_period";
      snapshot.completeness = DAYE_PERIOD_COMPLETENESS_EMPTY;
      snapshot.is_publishable = false;
      return;
   }

   if(snapshot.period_is_open)
   {
      snapshot.status = DAYE_PERIOD_STATUS_OK;
      snapshot.reason_code = "period_is_still_open";
      snapshot.completeness = DAYE_PERIOD_COMPLETENESS_OPEN;
      snapshot.is_publishable = config.include_open_periods && snapshot.coverage_percent >= config.minimum_publishable_coverage_percent;
      return;
   }

   bool exact_grid = (snapshot.observed_bar_count == expected &&
                      snapshot.first_source_bar_utc == snapshot.window.start_utc &&
                      snapshot.last_source_bar_utc == expected_last &&
                      !snapshot.left_edge_truncated &&
                      !snapshot.right_edge_truncated);
   if(exact_grid)
   {
      snapshot.status = DAYE_PERIOD_STATUS_OK;
      snapshot.reason_code = "complete_exact_base_bar_grid";
      snapshot.completeness = DAYE_PERIOD_COMPLETENESS_COMPLETE;
      snapshot.is_publishable = true;
      snapshot.availability_time_utc = snapshot.window.end_utc;
      return;
   }

   snapshot.status = DAYE_PERIOD_STATUS_PARTIAL_SOURCE_ALIGNMENT;
   snapshot.reason_code = "closed_period_has_missing_or_truncated_base_bars";
   snapshot.completeness = DAYE_PERIOD_COMPLETENESS_PARTIAL;
   snapshot.is_publishable = config.publish_partial_periods && snapshot.coverage_percent >= config.minimum_publishable_coverage_percent;
}

void DAYE_SwapSymbolPeriod(DAYE_SymbolPeriodSnapshot &a,DAYE_SymbolPeriodSnapshot &b)
{
   DAYE_SymbolPeriodSnapshot temp = a;
   a = b;
   b = temp;
}

bool DAYE_SymbolPeriodComesAfter(const DAYE_SymbolPeriodSnapshot &a,const DAYE_SymbolPeriodSnapshot &b)
{
   if(a.window.start_utc != b.window.start_utc)
      return a.window.start_utc > b.window.start_utc;
   int ar = DAYE_PeriodSortRank(a.period_family);
   int br = DAYE_PeriodSortRank(b.period_family);
   if(ar != br) return ar > br;
   return StringCompare(a.period_code,b.period_code) > 0;
}

void DAYE_SortSymbolPeriods(DAYE_SymbolPeriodSnapshot &items[])
{
   int n = ArraySize(items);
   for(int i=1;i<n;i++)
   {
      int j=i;
      while(j>0 && DAYE_SymbolPeriodComesAfter(items[j-1],items[j]))
      {
         DAYE_SwapSymbolPeriod(items[j-1],items[j]);
         j--;
      }
   }
}

void DAYE_AssignSymbolPeriodLinks(DAYE_SymbolPeriodSnapshot &items[])
{
   for(int i=0;i<ArraySize(items);i++)
   {
      items[i].previous_chronological_period_instance_id = "";
      items[i].previous_same_code_period_instance_id = "";
      int link_family = DAYE_PeriodLinkFamilyKey(items[i].period_family);
      for(int j=i-1;j>=0;j--)
      {
         if(items[i].previous_chronological_period_instance_id == "" &&
            DAYE_PeriodLinkFamilyKey(items[j].period_family) == link_family)
            items[i].previous_chronological_period_instance_id = items[j].period_instance_id;

         if(items[i].previous_same_code_period_instance_id == "" &&
            items[j].period_code == items[i].period_code)
            items[i].previous_same_code_period_instance_id = items[j].period_instance_id;

         if(items[i].previous_chronological_period_instance_id != "" &&
            items[i].previous_same_code_period_instance_id != "")
            break;
      }
   }
}

bool DAYE_AggregateSymbolBars(const DAYE_SymbolBar &bars[],
                              const DAYE_PeriodAggregationConfig &config,
                              const DAYE_TimeConfig &time_config,
                              const DAYE_PeriodDefinition &registry[],
                              const datetime now_utc,
                              const datetime processing_time_utc,
                              DAYE_SymbolPeriodSnapshot &items[],
                              string &reason_code)
{
   ArrayResize(items,0);
   reason_code = "";
   if(ArraySize(bars) < 1)
   {
      reason_code = "no_symbol_bars";
      return false;
   }

   int base_seconds = PeriodSeconds(config.data_config.base_timeframe);
   if(base_seconds <= 0)
   {
      reason_code = "invalid_base_timeframe_seconds";
      return false;
   }

   for(int i=0;i<ArraySize(bars);i++)
   {
      DAYE_TimeSnapshot time_snapshot;
      if(!DAYE_BuildTimeSnapshotFromUtc(bars[i].event_time_utc,time_config,registry,time_snapshot))
      {
         reason_code = "time_snapshot_failed:" + time_snapshot.reason_code;
         return false;
      }
      if(time_snapshot.in_declared_session_gap)
         continue;

      if(config.include_daily_periods)
         DAYE_AccumulateBarIntoPeriod(bars[i],time_snapshot.trading_day_window,time_snapshot.trading_day_key,base_seconds,processing_time_utc,items);
      if(config.include_session_periods)
         DAYE_AccumulateBarIntoPeriod(bars[i],time_snapshot.session_window,time_snapshot.trading_day_key,base_seconds,processing_time_utc,items);
      if(config.include_subcycle_periods)
         DAYE_AccumulateBarIntoPeriod(bars[i],time_snapshot.subcycle_window,time_snapshot.trading_day_key,base_seconds,processing_time_utc,items);
   }

   for(int i=0;i<ArraySize(items);i++)
      DAYE_FinalizeSymbolPeriodSnapshot(items[i],now_utc,config);
   DAYE_SortSymbolPeriods(items);
   DAYE_AssignSymbolPeriodLinks(items);
   return true;
}

int DAYE_CountAlignedPairsInWindow(const DAYE_SynchronizedBarPair &pairs[],const datetime start_utc,const datetime end_utc)
{
   int count = 0;
   for(int i=0;i<ArraySize(pairs);i++)
      if(pairs[i].event_time_utc >= start_utc && pairs[i].event_time_utc < end_utc)
         count++;
   return count;
}

void DAYE_BuildUnavailableSymbolPeriod(const DAYE_SymbolPeriodSnapshot &source,
                                       const string broker_symbol,
                                       const string canonical_symbol,
                                       DAYE_SymbolPeriodSnapshot &target)
{
   ZeroMemory(target);
   target.schema_version = DAYE_PERIOD_AGG_SCHEMA_VERSION;
   target.status = DAYE_PERIOD_STATUS_SOURCE_UNAVAILABLE;
   target.reason_code = "period_absent_for_symbol";
   target.completeness = DAYE_PERIOD_COMPLETENESS_UNAVAILABLE;
   target.is_publishable = false;
   target.is_replay_safe = source.is_replay_safe;
   target.broker_symbol = broker_symbol;
   target.canonical_symbol = canonical_symbol;
   target.base_timeframe = source.base_timeframe;
   target.base_bar_seconds = source.base_bar_seconds;
   target.period_id = source.period_id;
   target.period_family = source.period_family;
   target.period_code = source.period_code;
   target.period_instance_id = source.period_instance_id;
   target.trading_day_key = source.trading_day_key;
   target.window = source.window;
   target.event_time_utc = source.event_time_utc;
   target.processing_time_utc = source.processing_time_utc;
   target.snapshot_id = "EXP0018|P03|SYMBOL|" + source.period_instance_id + "|" + canonical_symbol;
}

int DAYE_FindMatchingPeriod(const DAYE_SymbolPeriodSnapshot &items[],const string instance_id)
{
   for(int i=0;i<ArraySize(items);i++)
      if(items[i].period_instance_id == instance_id)
         return i;
   return -1;
}

DAYE_PeriodCompleteness DAYE_DeterminePairedCompleteness(const DAYE_SymbolPeriodSnapshot &a,
                                                          const DAYE_SymbolPeriodSnapshot &b,
                                                          const int aligned_count,
                                                          const int expected_count)
{
   if(a.completeness == DAYE_PERIOD_COMPLETENESS_INVALID || b.completeness == DAYE_PERIOD_COMPLETENESS_INVALID)
      return DAYE_PERIOD_COMPLETENESS_INVALID;
   if(a.completeness == DAYE_PERIOD_COMPLETENESS_UNAVAILABLE || b.completeness == DAYE_PERIOD_COMPLETENESS_UNAVAILABLE)
      return DAYE_PERIOD_COMPLETENESS_UNAVAILABLE;
   if(a.completeness == DAYE_PERIOD_COMPLETENESS_OPEN || b.completeness == DAYE_PERIOD_COMPLETENESS_OPEN)
      return DAYE_PERIOD_COMPLETENESS_OPEN;
   if(a.completeness == DAYE_PERIOD_COMPLETENESS_COMPLETE &&
      b.completeness == DAYE_PERIOD_COMPLETENESS_COMPLETE &&
      expected_count > 0 && aligned_count == expected_count)
      return DAYE_PERIOD_COMPLETENESS_COMPLETE;
   return DAYE_PERIOD_COMPLETENESS_PARTIAL;
}

void DAYE_FinalizePairedPeriod(DAYE_PairedPeriodSnapshot &paired,const DAYE_PeriodAggregationConfig &config)
{
   paired.expected_aligned_bar_count = paired.symbol_a.expected_bar_count;
   if(paired.symbol_b.expected_bar_count > paired.expected_aligned_bar_count)
      paired.expected_aligned_bar_count = paired.symbol_b.expected_bar_count;
   paired.aligned_coverage_percent = 0.0;
   if(paired.expected_aligned_bar_count > 0)
      paired.aligned_coverage_percent = 100.0 * (double)paired.aligned_bar_count / (double)paired.expected_aligned_bar_count;
   paired.unmatched_a_count = paired.symbol_a.observed_bar_count - paired.aligned_bar_count;
   paired.unmatched_b_count = paired.symbol_b.observed_bar_count - paired.aligned_bar_count;
   if(paired.unmatched_a_count < 0) paired.unmatched_a_count = 0;
   if(paired.unmatched_b_count < 0) paired.unmatched_b_count = 0;

   paired.completeness = DAYE_DeterminePairedCompleteness(paired.symbol_a,paired.symbol_b,paired.aligned_bar_count,paired.expected_aligned_bar_count);
   paired.status = DAYE_PERIOD_STATUS_OK;
   paired.reason_code = DAYE_PeriodCompletenessToString(paired.completeness);
   paired.is_replay_safe = paired.symbol_a.is_replay_safe && paired.symbol_b.is_replay_safe;

   if(paired.completeness == DAYE_PERIOD_COMPLETENESS_INVALID)
      paired.status = DAYE_PERIOD_STATUS_INVALID_BAR_MEMBERSHIP;
   else if(paired.completeness == DAYE_PERIOD_COMPLETENESS_UNAVAILABLE)
      paired.status = DAYE_PERIOD_STATUS_SOURCE_UNAVAILABLE;
   else if(paired.completeness == DAYE_PERIOD_COMPLETENESS_PARTIAL)
      paired.status = DAYE_PERIOD_STATUS_PARTIAL_SOURCE_ALIGNMENT;

   paired.is_publishable = false;
   if(paired.completeness == DAYE_PERIOD_COMPLETENESS_COMPLETE)
      paired.is_publishable = true;
   else if(paired.completeness == DAYE_PERIOD_COMPLETENESS_OPEN)
      paired.is_publishable = config.include_open_periods && paired.aligned_coverage_percent >= config.minimum_publishable_coverage_percent;
   else if(paired.completeness == DAYE_PERIOD_COMPLETENESS_PARTIAL)
      paired.is_publishable = config.publish_partial_periods && paired.aligned_coverage_percent >= config.minimum_publishable_coverage_percent;

   if(config.require_both_symbols_complete && paired.completeness != DAYE_PERIOD_COMPLETENESS_COMPLETE)
      paired.is_publishable = false;
}

void DAYE_AppendPairedFromSource(const DAYE_SymbolPeriodSnapshot &source,
                                 const DAYE_SymbolPeriodSnapshot &other_items[],
                                 const bool source_is_a,
                                 const string broker_a,
                                 const string canonical_a,
                                 const string broker_b,
                                 const string canonical_b,
                                 const DAYE_SynchronizedBarPair &pairs[],
                                 const DAYE_PeriodAggregationConfig &config,
                                 const datetime processing_time_utc,
                                 DAYE_PairedPeriodSnapshot &out[])
{
   int existing = -1;
   for(int i=0;i<ArraySize(out);i++)
      if(out[i].period_instance_id == source.period_instance_id) { existing = i; break; }
   if(existing >= 0)
      return;

   int index = ArraySize(out);
   ArrayResize(out,index + 1);
   DAYE_PairedPeriodSnapshot paired;
   ZeroMemory(paired);
   paired.schema_version = DAYE_PERIOD_AGG_SCHEMA_VERSION;
   paired.period_instance_id = source.period_instance_id;
   paired.period_id = source.period_id;
   paired.period_family = source.period_family;
   paired.period_code = source.period_code;
   paired.trading_day_key = source.trading_day_key;
   paired.window = source.window;
   paired.event_time_utc = source.window.start_utc;
   paired.processing_time_utc = processing_time_utc;
   paired.paired_period_id = DAYE_BuildPairedPeriodId(source.period_instance_id,canonical_a,canonical_b);

   int other_index = DAYE_FindMatchingPeriod(other_items,source.period_instance_id);
   if(source_is_a)
   {
      paired.symbol_a = source;
      if(other_index >= 0) paired.symbol_b = other_items[other_index];
      else DAYE_BuildUnavailableSymbolPeriod(source,broker_b,canonical_b,paired.symbol_b);
   }
   else
   {
      paired.symbol_b = source;
      if(other_index >= 0) paired.symbol_a = other_items[other_index];
      else DAYE_BuildUnavailableSymbolPeriod(source,broker_a,canonical_a,paired.symbol_a);
   }

   paired.availability_time_utc = paired.symbol_a.availability_time_utc;
   if(paired.symbol_b.availability_time_utc > paired.availability_time_utc)
      paired.availability_time_utc = paired.symbol_b.availability_time_utc;
   paired.aligned_bar_count = DAYE_CountAlignedPairsInWindow(pairs,paired.window.start_utc,paired.window.end_utc);
   DAYE_FinalizePairedPeriod(paired,config);
   out[index] = paired;
}

void DAYE_SwapPairedPeriod(DAYE_PairedPeriodSnapshot &a,DAYE_PairedPeriodSnapshot &b)
{
   DAYE_PairedPeriodSnapshot temp = a;
   a = b;
   b = temp;
}

bool DAYE_PairedPeriodComesAfter(const DAYE_PairedPeriodSnapshot &a,const DAYE_PairedPeriodSnapshot &b)
{
   if(a.window.start_utc != b.window.start_utc)
      return a.window.start_utc > b.window.start_utc;
   int ar = DAYE_PeriodSortRank(a.period_family);
   int br = DAYE_PeriodSortRank(b.period_family);
   if(ar != br) return ar > br;
   return StringCompare(a.period_code,b.period_code) > 0;
}

void DAYE_SortPairedPeriods(DAYE_PairedPeriodSnapshot &items[])
{
   int n = ArraySize(items);
   for(int i=1;i<n;i++)
   {
      int j=i;
      while(j>0 && DAYE_PairedPeriodComesAfter(items[j-1],items[j]))
      {
         DAYE_SwapPairedPeriod(items[j-1],items[j]);
         j--;
      }
   }
}

void DAYE_AssignPairedPeriodLinks(DAYE_PairedPeriodSnapshot &items[])
{
   for(int i=0;i<ArraySize(items);i++)
   {
      items[i].previous_chronological_paired_period_id = "";
      items[i].previous_same_code_paired_period_id = "";
      int link_family = DAYE_PeriodLinkFamilyKey(items[i].period_family);
      for(int j=i-1;j>=0;j--)
      {
         if(items[i].previous_chronological_paired_period_id == "" &&
            DAYE_PeriodLinkFamilyKey(items[j].period_family) == link_family)
            items[i].previous_chronological_paired_period_id = items[j].paired_period_id;
         if(items[i].previous_same_code_paired_period_id == "" &&
            items[j].period_code == items[i].period_code)
            items[i].previous_same_code_paired_period_id = items[j].paired_period_id;
         if(items[i].previous_chronological_paired_period_id != "" &&
            items[i].previous_same_code_paired_period_id != "")
            break;
      }
   }
}

void DAYE_BuildPairedPeriodSnapshots(const DAYE_SymbolPeriodSnapshot &a_items[],
                                     const DAYE_SymbolPeriodSnapshot &b_items[],
                                     const DAYE_SynchronizedBarPair &pairs[],
                                     const DAYE_PeriodAggregationConfig &config,
                                     const datetime processing_time_utc,
                                     DAYE_PairedPeriodSnapshot &out[])
{
   ArrayResize(out,0);
   for(int i=0;i<ArraySize(a_items);i++)
      DAYE_AppendPairedFromSource(a_items[i],b_items,true,
                                  config.data_config.broker_symbol_a,config.data_config.canonical_symbol_a,
                                  config.data_config.broker_symbol_b,config.data_config.canonical_symbol_b,
                                  pairs,config,processing_time_utc,out);
   for(int i=0;i<ArraySize(b_items);i++)
      DAYE_AppendPairedFromSource(b_items[i],a_items,false,
                                  config.data_config.broker_symbol_a,config.data_config.canonical_symbol_a,
                                  config.data_config.broker_symbol_b,config.data_config.canonical_symbol_b,
                                  pairs,config,processing_time_utc,out);

   DAYE_SortPairedPeriods(out);
   DAYE_AssignPairedPeriodLinks(out);

   if(ArraySize(out) > config.maximum_periods_to_publish)
   {
      int keep = config.maximum_periods_to_publish;
      int start = ArraySize(out) - keep;
      DAYE_PairedPeriodSnapshot trimmed[];
      ArrayResize(trimmed,keep);
      for(int i=0;i<keep;i++) trimmed[i] = out[start+i];
      ArrayResize(out,keep);
      for(int i=0;i<keep;i++) out[i] = trimmed[i];
      DAYE_AssignPairedPeriodLinks(out);
   }
}

#endif
