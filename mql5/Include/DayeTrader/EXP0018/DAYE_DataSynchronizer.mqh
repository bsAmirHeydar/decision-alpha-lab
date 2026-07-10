
#ifndef __EXP0018_DAYE_DATA_SYNCHRONIZER_MQH__
#define __EXP0018_DAYE_DATA_SYNCHRONIZER_MQH__

#include <DayeTrader/EXP0018/DAYE_DataQuality.mqh>

bool DAYE_IsSeriesSynchronized(const string symbol,const ENUM_TIMEFRAMES timeframe,bool &synchronized,string &reason_code)
{
   synchronized = false;
   reason_code = "";
   long value = 0;
   ResetLastError();
   if(!SeriesInfoInteger(symbol,timeframe,SERIES_SYNCHRONIZED,value))
   {
      reason_code = "series_info_failed_" + IntegerToString(GetLastError());
      return false;
   }
   synchronized = (value != 0);
   return true;
}

bool DAYE_LoadClosedBars(const DAYE_SymbolDescriptor &descriptor,
                         const DAYE_DataSyncConfig &config,
                         const DAYE_TimeConfig &time_config,
                         const datetime current_broker_time,
                         DAYE_SymbolBar &bars[],
                         DAYE_SymbolDataHealth &health)
{
   ArrayResize(bars,0);
   DAYE_InitSymbolHealth(descriptor,config,health);

   bool synchronized = false;
   string reason = "";
   if(!DAYE_IsSeriesSynchronized(descriptor.broker_symbol,config.base_timeframe,synchronized,reason))
   {
      health.status = DAYE_DATA_STATUS_HISTORY_NOT_SYNCHRONIZED;
      health.reason_code = reason;
      return false;
   }
   health.series_synchronized = synchronized;
   if(config.require_series_synchronized && !synchronized)
   {
      health.status = DAYE_DATA_STATUS_HISTORY_NOT_SYNCHRONIZED;
      health.reason_code = "series_not_synchronized";
      return false;
   }

   ResetLastError();
   int available = Bars(descriptor.broker_symbol,config.base_timeframe);
   health.bars_available = available;
   if(available < config.minimum_common_bars)
   {
      health.status = DAYE_DATA_STATUS_INSUFFICIENT_BARS;
      health.reason_code = "bars_available_below_minimum";
      return false;
   }

   MqlRates raw[];
   ArraySetAsSeries(raw,false);
   int start_position = config.use_closed_bars_only ? 1 : 0;
   ResetLastError();
   int copied = CopyRates(descriptor.broker_symbol,
                          config.base_timeframe,
                          start_position,
                          config.requested_bars_per_symbol,
                          raw);
   health.copied_bars = copied;
   if(copied <= 0)
   {
      health.status = DAYE_DATA_STATUS_COPY_RATES_FAILED;
      health.reason_code = "copy_rates_failed_" + IntegerToString(GetLastError());
      return false;
   }

   ArraySetAsSeries(raw,false);
   ArrayResize(bars,copied);
   int accepted = 0;
   for(int i=0;i<copied;i++)
   {
      DAYE_SymbolBar built;
      if(!DAYE_BuildSymbolBar(raw[i],descriptor,config.base_timeframe,time_config,current_broker_time,built))
      {
         health.invalid_bar_count++;
         if(config.fail_on_any_invalid_bar)
         {
            health.status = built.status;
            health.reason_code = built.reason_code;
            ArrayResize(bars,0);
            return false;
         }
         continue;
      }
      if(config.use_closed_bars_only && built.completeness != DAYE_BAR_COMPLETENESS_CLOSED)
         continue;
      bars[accepted] = built;
      accepted++;
   }
   ArrayResize(bars,accepted);
   health.accepted_bars = accepted;

   if(accepted < config.minimum_common_bars)
   {
      health.status = DAYE_DATA_STATUS_INSUFFICIENT_BARS;
      health.reason_code = "accepted_bars_below_minimum";
      return false;
   }
   if(!DAYE_ValidateChronologicalBars(bars,health))
      return false;

   health.first_event_time_utc = bars[0].event_time_utc;
   health.last_event_time_utc = bars[accepted-1].event_time_utc;

   datetime now_utc = 0;
   int broker_offset = 0;
   bool replay_safe = true;
   if(DAYE_BrokerToUtc(current_broker_time,time_config,now_utc,broker_offset,replay_safe,reason))
   {
      long age = (long)now_utc - (long)bars[accepted-1].close_time_utc;
      if(age < 0)
         age = 0;
      health.latest_closed_bar_age_seconds = (int)age;
      if(config.enforce_freshness && health.latest_closed_bar_age_seconds > config.maximum_latest_bar_age_seconds)
      {
         health.status = DAYE_DATA_STATUS_STALE_DATA;
         health.reason_code = "latest_closed_bar_is_stale";
         return false;
      }
   }

   health.status = DAYE_DATA_STATUS_OK;
   health.reason_code = "ok";
   return true;
}

string DAYE_BuildSynchronizedPairId(const DAYE_DataSyncConfig &config,const datetime event_time_utc)
{
   return "EXP0018|P02|" + EnumToString(config.base_timeframe) + "|" +
          IntegerToString((long)event_time_utc) + "|" +
          config.canonical_symbol_a + "|" + config.canonical_symbol_b;
}

bool DAYE_AlignBarsByExactUtc(DAYE_SymbolBar &bars_a[],
                              DAYE_SymbolBar &bars_b[],
                              const DAYE_DataSyncConfig &config,
                              const datetime processing_time_utc,
                              DAYE_SynchronizedBarPair &pairs[],
                              DAYE_DataSyncSummary &summary)
{
   ArrayResize(pairs,0);
   summary.aligned_count = 0;
   summary.unmatched_a = 0;
   summary.unmatched_b = 0;
   summary.first_common_event_time_utc = 0;
   summary.last_common_event_time_utc = 0;

   int i = 0;
   int j = 0;
   while(i < ArraySize(bars_a) && j < ArraySize(bars_b))
   {
      datetime ta = bars_a[i].event_time_utc;
      datetime tb = bars_b[j].event_time_utc;
      if(ta == tb)
      {
         int index = ArraySize(pairs);
         ArrayResize(pairs,index + 1);
         DAYE_SynchronizedBarPair pair;
         ZeroMemory(pair);
         pair.schema_version = DAYE_DATA_SCHEMA_VERSION;
         pair.status = DAYE_DATA_STATUS_OK;
         pair.reason_code = "exact_utc_match";
         pair.pair_id = DAYE_BuildSynchronizedPairId(config,ta);
         pair.timeframe = config.base_timeframe;
         pair.event_time_utc = ta;
         pair.event_time_ny = bars_a[i].event_time_ny;
         pair.availability_time_utc = bars_a[i].close_time_utc;
         if(bars_b[j].close_time_utc > pair.availability_time_utc)
            pair.availability_time_utc = bars_b[j].close_time_utc;
         pair.processing_time_utc = processing_time_utc;
         pair.symbol_a = bars_a[i];
         pair.symbol_b = bars_b[j];
         pairs[index] = pair;

         if(summary.first_common_event_time_utc == 0)
            summary.first_common_event_time_utc = ta;
         summary.last_common_event_time_utc = ta;
         i++;
         j++;
      }
      else if(ta < tb)
      {
         summary.unmatched_a++;
         i++;
      }
      else
      {
         summary.unmatched_b++;
         j++;
      }
   }
   summary.unmatched_a += ArraySize(bars_a) - i;
   summary.unmatched_b += ArraySize(bars_b) - j;

   summary.aligned_count = ArraySize(pairs);
   if(summary.aligned_count < 1)
   {
      summary.status = DAYE_DATA_STATUS_NO_COMMON_TIMESTAMPS;
      summary.reason_code = "no_exact_common_event_time_utc";
      summary.is_ready = false;
      summary.is_complete = false;
      return false;
   }

   bool complete = (summary.unmatched_a == 0 && summary.unmatched_b == 0);
   summary.is_complete = complete;
   if(!complete)
   {
      summary.status = DAYE_DATA_STATUS_PARTIAL_ALIGNMENT;
      summary.reason_code = "explicit_unmatched_timestamps";
      if(config.require_complete_alignment)
      {
         summary.is_ready = false;
         return false;
      }
   }
   else
   {
      summary.status = DAYE_DATA_STATUS_OK;
      summary.reason_code = "exact_timestamp_alignment_complete";
   }

   if(summary.aligned_count < config.minimum_common_bars)
   {
      summary.status = DAYE_DATA_STATUS_INSUFFICIENT_BARS;
      summary.reason_code = "common_bars_below_minimum";
      summary.is_ready = false;
      return false;
   }

   if(ArraySize(pairs) > config.maximum_pairs_to_publish)
   {
      int keep = config.maximum_pairs_to_publish;
      int source_start = ArraySize(pairs) - keep;
      DAYE_SynchronizedBarPair trimmed[];
      ArrayResize(trimmed,keep);
      for(int k=0;k<keep;k++)
         trimmed[k] = pairs[source_start + k];
      ArrayResize(pairs,keep);
      for(int k=0;k<keep;k++)
         pairs[k] = trimmed[k];
   }

   summary.is_ready = true;
   return true;
}

bool DAYE_ProbeLatestClosedBarTime(const string symbol,const ENUM_TIMEFRAMES timeframe,datetime &bar_time)
{
   bar_time = 0;
   datetime values[];
   ArraySetAsSeries(values,false);
   ResetLastError();
   int copied = CopyTime(symbol,timeframe,1,1,values);
   if(copied != 1)
      return false;
   bar_time = values[0];
   return (bar_time > 0);
}

#endif
