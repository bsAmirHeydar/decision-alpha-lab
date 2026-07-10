
#ifndef __EXP0018_DAYE_PERIOD_STORE_MQH__
#define __EXP0018_DAYE_PERIOD_STORE_MQH__

#include <DayeTrader/EXP0018/DAYE_PeriodAggregator.mqh>

class CDayePeriodStore
{
private:
   DAYE_PairedPeriodSnapshot m_items[];

public:
   CDayePeriodStore(void)
   {
      ArrayResize(m_items,0);
   }

   void Clear(void)
   {
      ArrayResize(m_items,0);
   }

   void Replace(const DAYE_PairedPeriodSnapshot &items[])
   {
      ArrayResize(m_items,ArraySize(items));
      for(int i=0;i<ArraySize(items);i++)
         m_items[i] = items[i];
   }

   int Count(void)
   {
      return ArraySize(m_items);
   }

   bool Get(const int index,DAYE_PairedPeriodSnapshot &item)
   {
      if(index < 0 || index >= ArraySize(m_items))
         return false;
      item = m_items[index];
      return true;
   }

   bool FindByPairedId(const string paired_id,DAYE_PairedPeriodSnapshot &item)
   {
      for(int i=0;i<ArraySize(m_items);i++)
      {
         if(m_items[i].paired_period_id == paired_id)
         {
            item = m_items[i];
            return true;
         }
      }
      return false;
   }

   bool FindByPeriodInstanceId(const string period_instance_id,DAYE_PairedPeriodSnapshot &item)
   {
      for(int i=0;i<ArraySize(m_items);i++)
      {
         if(m_items[i].period_instance_id == period_instance_id)
         {
            item = m_items[i];
            return true;
         }
      }
      return false;
   }

   bool Latest(DAYE_PairedPeriodSnapshot &item)
   {
      if(ArraySize(m_items) < 1)
         return false;
      item = m_items[ArraySize(m_items)-1];
      return true;
   }

   bool LatestComplete(DAYE_PairedPeriodSnapshot &item)
   {
      for(int i=ArraySize(m_items)-1;i>=0;i--)
      {
         if(m_items[i].completeness == DAYE_PERIOD_COMPLETENESS_COMPLETE)
         {
            item = m_items[i];
            return true;
         }
      }
      return false;
   }
};

void DAYE_BuildPeriodStoreSummary(const DAYE_DataSyncSummary &source_summary,
                                  const DAYE_SymbolPeriodSnapshot &a_items[],
                                  const DAYE_SymbolPeriodSnapshot &b_items[],
                                  const DAYE_PairedPeriodSnapshot &paired_items[],
                                  const DAYE_PeriodAggregationConfig &config,
                                  const datetime processing_time_utc,
                                  DAYE_PeriodStoreSummary &summary)
{
   ZeroMemory(summary);
   summary.schema_version = DAYE_PERIOD_AGG_SCHEMA_VERSION;
   summary.status = DAYE_PERIOD_STATUS_SOURCE_UNAVAILABLE;
   summary.reason_code = "not_evaluated";
   summary.is_ready = false;
   summary.is_complete = true;
   summary.is_replay_safe = source_summary.is_replay_safe;
   summary.run_key = "EXP0018|P03|" + config.data_config.canonical_symbol_a + "|" + config.data_config.canonical_symbol_b + "|" + EnumToString(config.data_config.base_timeframe);
   summary.processing_time_utc = processing_time_utc;
   summary.source_first_event_time_utc = source_summary.first_common_event_time_utc;
   summary.source_last_event_time_utc = source_summary.last_common_event_time_utc;
   summary.source_bars_a = source_summary.copied_a;
   summary.source_bars_b = source_summary.copied_b;
   summary.source_aligned_pairs = source_summary.aligned_count;
   summary.source_unmatched_a = source_summary.unmatched_a;
   summary.source_unmatched_b = source_summary.unmatched_b;
   summary.symbol_period_count_a = ArraySize(a_items);
   summary.symbol_period_count_b = ArraySize(b_items);
   summary.paired_period_count = ArraySize(paired_items);

   for(int i=0;i<ArraySize(paired_items);i++)
   {
      DAYE_PairedPeriodSnapshot item = paired_items[i];
      if(item.period_family == DAYE_FAMILY_DAILY) summary.daily_period_count++;
      else if(item.period_family == DAYE_FAMILY_SESSION) summary.session_period_count++;
      else if(item.period_family == DAYE_FAMILY_SUBCYCLE_90M || item.period_family == DAYE_FAMILY_SUBCYCLE_TAIL) summary.subcycle_period_count++;

      if(item.completeness == DAYE_PERIOD_COMPLETENESS_COMPLETE)
      {
         summary.complete_paired_period_count++;
         summary.latest_complete_paired_period_id = item.paired_period_id;
         summary.latest_complete_period_end_utc = item.window.end_utc;
      }
      else if(item.completeness == DAYE_PERIOD_COMPLETENESS_PARTIAL)
      {
         summary.partial_paired_period_count++;
         summary.is_complete = false;
      }
      else if(item.completeness == DAYE_PERIOD_COMPLETENESS_OPEN)
         summary.open_paired_period_count++;
      else if(item.completeness == DAYE_PERIOD_COMPLETENESS_UNAVAILABLE || item.completeness == DAYE_PERIOD_COMPLETENESS_INVALID)
      {
         summary.unavailable_paired_period_count++;
         summary.is_complete = false;
      }
      if(!item.is_replay_safe) summary.is_replay_safe = false;
      summary.latest_paired_period_id = item.paired_period_id;
      summary.latest_period_start_utc = item.window.start_utc;
      if(item.availability_time_utc > summary.availability_time_utc)
         summary.availability_time_utc = item.availability_time_utc;
   }

   if(ArraySize(paired_items) < 1)
   {
      summary.status = DAYE_PERIOD_STATUS_SOURCE_UNAVAILABLE;
      summary.reason_code = "no_paired_period_snapshots";
      return;
   }
   if(summary.complete_paired_period_count < config.minimum_complete_paired_periods)
   {
      summary.status = DAYE_PERIOD_STATUS_INSUFFICIENT_COMPLETE_PERIODS;
      summary.reason_code = "complete_paired_periods_below_minimum";
      return;
   }
   if(source_summary.status == DAYE_DATA_STATUS_PARTIAL_ALIGNMENT || summary.partial_paired_period_count > 0 || summary.unavailable_paired_period_count > 0)
   {
      summary.status = DAYE_PERIOD_STATUS_PARTIAL_SOURCE_ALIGNMENT;
      summary.reason_code = "period_store_ready_with_explicit_partial_history";
      summary.is_ready = true;
      return;
   }
   summary.status = DAYE_PERIOD_STATUS_OK;
   summary.reason_code = "period_store_ready";
   summary.is_ready = true;
}

#endif
