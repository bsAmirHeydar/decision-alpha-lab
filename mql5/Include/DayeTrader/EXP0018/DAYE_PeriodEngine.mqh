
#ifndef __EXP0018_DAYE_PERIOD_ENGINE_MQH__
#define __EXP0018_DAYE_PERIOD_ENGINE_MQH__

#include <DayeTrader/EXP0018/DAYE_PeriodSelfTest.mqh>

class CDayePeriodAggregationEngine
{
private:
   DAYE_PeriodAggregationConfig m_config;
   DAYE_TimeConfig m_time_config;
   DAYE_PeriodDefinition m_registry[];
   DAYE_SymbolDescriptor m_symbol_a;
   DAYE_SymbolDescriptor m_symbol_b;
   DAYE_PeriodStoreSummary m_previous_summary;
   bool m_has_previous_summary;
   datetime m_last_probe_a;
   datetime m_last_probe_b;
   datetime m_last_full_refresh_utc;
   bool m_initialized;
   CDayePeriodStore m_store;
   CDayePeriodAuditWriter m_audit;

   void BuildSourceSummaryBase(DAYE_DataSyncSummary &summary,const datetime processing_time_utc)
   {
      ZeroMemory(summary);
      summary.schema_version = DAYE_DATA_SCHEMA_VERSION;
      summary.status = DAYE_DATA_STATUS_SYMBOL_UNAVAILABLE;
      summary.reason_code = "not_evaluated";
      summary.is_ready = false;
      summary.is_complete = false;
      summary.is_replay_safe = true;
      summary.run_key = "EXP0018|P03SOURCE|" + m_config.data_config.canonical_symbol_a + "|" + m_config.data_config.canonical_symbol_b;
      summary.broker_symbol_a = m_config.data_config.broker_symbol_a;
      summary.broker_symbol_b = m_config.data_config.broker_symbol_b;
      summary.canonical_symbol_a = m_config.data_config.canonical_symbol_a;
      summary.canonical_symbol_b = m_config.data_config.canonical_symbol_b;
      summary.timeframe = m_config.data_config.base_timeframe;
      summary.requested_bars_per_symbol = m_config.data_config.requested_bars_per_symbol;
      summary.processing_time_utc = processing_time_utc;
      summary.availability_time_utc = processing_time_utc;
   }

public:
   CDayePeriodAggregationEngine(void)
   {
      ZeroMemory(m_previous_summary);
      m_has_previous_summary = false;
      m_last_probe_a = 0;
      m_last_probe_b = 0;
      m_last_full_refresh_utc = 0;
      m_initialized = false;
   }

   bool Initialize(const DAYE_PeriodAggregationConfig &config,
                   const DAYE_TimeConfig &time_config,
                   const bool run_self_tests,
                   const bool write_audit_csv,
                   const string audit_filename)
   {
      string reason = "";
      if(!DAYE_ValidatePeriodAggregationConfig(config,reason))
      {
         Print("EXP0018 P03 initialization failed reason=",reason);
         return false;
      }
      if(!DAYE_ValidateTimeConfig(time_config,reason))
      {
         Print("EXP0018 P03 time config invalid reason=",reason);
         return false;
      }
      if(run_self_tests && !DAYE_RunEmbeddedPeriodAggregationSelfTests())
      {
         Print("EXP0018 P03 initialization blocked because embedded self-test failed.");
         return false;
      }

      m_config = config;
      m_time_config = time_config;
      DAYE_BuildCanonicalPeriodRegistry(m_registry);
      if(!DAYE_LoadSymbolDescriptor(config.data_config.broker_symbol_a,config.data_config.canonical_symbol_a,m_symbol_a))
      {
         Print("EXP0018 P03 symbol A descriptor failed reason=",m_symbol_a.reason_code);
         return false;
      }
      if(!DAYE_LoadSymbolDescriptor(config.data_config.broker_symbol_b,config.data_config.canonical_symbol_b,m_symbol_b))
      {
         Print("EXP0018 P03 symbol B descriptor failed reason=",m_symbol_b.reason_code);
         return false;
      }
      if(!m_audit.Open(audit_filename,write_audit_csv))
         return false;

      m_initialized = true;
      Print("EXP0018 P03 Period Aggregation and Completeness v2 initialized. Period OHLC is symbol-local; missing bars remain explicit; weekly remains disabled; no hunt, divergence, drawing, risk, or order authority exists.");
      return true;
   }

   bool ShouldRefresh(const datetime processing_time_utc)
   {
      datetime probe_a = 0;
      datetime probe_b = 0;
      bool ok_a = DAYE_ProbeLatestClosedBarTime(m_config.data_config.broker_symbol_a,m_config.data_config.base_timeframe,probe_a);
      bool ok_b = DAYE_ProbeLatestClosedBarTime(m_config.data_config.broker_symbol_b,m_config.data_config.base_timeframe,probe_b);
      if(!ok_a || !ok_b) return true;
      if(!m_has_previous_summary || !m_previous_summary.is_ready) return true;
      if(probe_a != m_last_probe_a || probe_b != m_last_probe_b) return true;
      if(m_last_full_refresh_utc <= 0 || (long)processing_time_utc - (long)m_last_full_refresh_utc >= m_config.force_full_refresh_seconds) return true;
      return false;
   }

   bool Process(const datetime current_broker_time,
                const bool print_summary,
                const bool print_latest_period,
                const bool print_events,
                const bool show_chart_comment,
                const bool write_summary_rows,
                const int audit_latest_period_count)
   {
      if(!m_initialized) return false;

      datetime processing_time_utc = TimeGMT();
      if(processing_time_utc <= 0)
      {
         int broker_offset = 0;
         bool replay_safe = true;
         string reason = "";
         if(!DAYE_BrokerToUtc(current_broker_time,m_time_config,processing_time_utc,broker_offset,replay_safe,reason))
            processing_time_utc = current_broker_time;
      }
      if(!ShouldRefresh(processing_time_utc)) return true;

      DAYE_DataSyncSummary source_summary;
      BuildSourceSummaryBase(source_summary,processing_time_utc);
      DAYE_SymbolDataHealth health_a;
      DAYE_SymbolDataHealth health_b;
      DAYE_SymbolBar bars_a[];
      DAYE_SymbolBar bars_b[];
      DAYE_SynchronizedBarPair pairs[];
      DAYE_SymbolPeriodSnapshot periods_a[];
      DAYE_SymbolPeriodSnapshot periods_b[];
      DAYE_PairedPeriodSnapshot paired_periods[];

      bool loaded_a = DAYE_LoadClosedBars(m_symbol_a,m_config.data_config,m_time_config,current_broker_time,bars_a,health_a);
      bool loaded_b = DAYE_LoadClosedBars(m_symbol_b,m_config.data_config,m_time_config,current_broker_time,bars_b,health_b);
      source_summary.copied_a = health_a.copied_bars;
      source_summary.copied_b = health_b.copied_bars;
      source_summary.invalid_a = health_a.invalid_bar_count;
      source_summary.invalid_b = health_b.invalid_bar_count;
      source_summary.duplicate_a = health_a.duplicate_timestamp_count;
      source_summary.duplicate_b = health_b.duplicate_timestamp_count;

      DAYE_PeriodStoreSummary period_summary;
      ZeroMemory(period_summary);
      period_summary.schema_version = DAYE_PERIOD_AGG_SCHEMA_VERSION;
      period_summary.status = DAYE_PERIOD_STATUS_SOURCE_UNAVAILABLE;
      period_summary.reason_code = "source_not_ready";
      period_summary.processing_time_utc = processing_time_utc;

      if(loaded_a && loaded_b)
      {
         source_summary.is_replay_safe = true;
         for(int i=0;i<ArraySize(bars_a);i++) if(!bars_a[i].is_replay_safe) source_summary.is_replay_safe=false;
         for(int i=0;i<ArraySize(bars_b);i++) if(!bars_b[i].is_replay_safe) source_summary.is_replay_safe=false;
         DAYE_AlignBarsByExactUtc(bars_a,bars_b,m_config.data_config,processing_time_utc,pairs,source_summary);
         if(ArraySize(pairs)>0) source_summary.availability_time_utc = pairs[ArraySize(pairs)-1].availability_time_utc;

         string reason_a = "";
         string reason_b = "";
         bool aggregate_a = DAYE_AggregateSymbolBars(bars_a,m_config,m_time_config,m_registry,processing_time_utc,processing_time_utc,periods_a,reason_a);
         bool aggregate_b = DAYE_AggregateSymbolBars(bars_b,m_config,m_time_config,m_registry,processing_time_utc,processing_time_utc,periods_b,reason_b);
         if(aggregate_a && aggregate_b)
         {
            DAYE_BuildPairedPeriodSnapshots(periods_a,periods_b,pairs,m_config,processing_time_utc,paired_periods);
            DAYE_BuildPeriodStoreSummary(source_summary,periods_a,periods_b,paired_periods,m_config,processing_time_utc,period_summary);
            m_store.Replace(paired_periods);
         }
         else
         {
            m_store.Clear();
            period_summary.status = DAYE_PERIOD_STATUS_TIME_WINDOW_FAILED;
            period_summary.reason_code = aggregate_a ? reason_b : reason_a;
            period_summary.is_ready = false;
         }
      }
      else
      {
         m_store.Clear();
         period_summary.status = DAYE_PERIOD_STATUS_SOURCE_UNAVAILABLE;
         period_summary.reason_code = loaded_a ? health_b.reason_code : health_a.reason_code;
         period_summary.is_ready = false;
      }

      DAYE_PeriodAggregateEvent events[];
      DAYE_DetectPeriodAggregateEvents(m_has_previous_summary,m_previous_summary,period_summary,events);
      for(int i=0;i<ArraySize(events);i++)
      {
         if(print_events) Print(DAYE_FormatPeriodAggregateEvent(events[i]));
         if(!m_audit.WriteEvent(events[i])) Print("EXP0018 P03 audit event write failed id=",events[i].event_id);
      }

      if(print_summary) Print(DAYE_FormatPeriodStoreSummary(period_summary));
      if(print_latest_period)
      {
         DAYE_PairedPeriodSnapshot latest;
         if(m_store.Latest(latest)) Print("  ",DAYE_FormatPairedPeriod(latest));
         DAYE_PairedPeriodSnapshot latest_complete;
         if(m_store.LatestComplete(latest_complete)) Print("  latest_complete ",DAYE_FormatPairedPeriod(latest_complete));
      }
      if(write_summary_rows && !m_audit.WriteSummary(period_summary))
         Print("EXP0018 P03 audit summary write failed.");

      int count_to_write = audit_latest_period_count;
      if(count_to_write < 0) count_to_write = 0;
      int start_index = m_store.Count() - count_to_write;
      if(start_index < 0) start_index = 0;
      for(int i=start_index;i<m_store.Count();i++)
      {
         DAYE_PairedPeriodSnapshot item;
         if(m_store.Get(i,item) && !m_audit.WritePeriod(item))
            Print("EXP0018 P03 audit period write failed id=",item.paired_period_id);
      }

      if(show_chart_comment)
         Comment(DAYE_FormatPeriodStoreSummary(period_summary) + "\nPeriod aggregation only — no hunts, signals, drawings, or trading.");
      else
         Comment("");

      datetime probe_a=0,probe_b=0;
      if(DAYE_ProbeLatestClosedBarTime(m_config.data_config.broker_symbol_a,m_config.data_config.base_timeframe,probe_a)) m_last_probe_a=probe_a;
      if(DAYE_ProbeLatestClosedBarTime(m_config.data_config.broker_symbol_b,m_config.data_config.base_timeframe,probe_b)) m_last_probe_b=probe_b;
      m_last_full_refresh_utc = processing_time_utc;
      m_previous_summary = period_summary;
      m_has_previous_summary = true;
      return true;
   }

   void Shutdown(void)
   {
      Comment("");
      m_audit.Close();
      m_store.Clear();
      ArrayResize(m_registry,0);
      ZeroMemory(m_previous_summary);
      m_has_previous_summary=false;
      m_last_probe_a=0;
      m_last_probe_b=0;
      m_last_full_refresh_utc=0;
      m_initialized=false;
   }
};

#endif
