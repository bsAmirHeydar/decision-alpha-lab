
#ifndef __EXP0018_DAYE_DATA_ENGINE_MQH__
#define __EXP0018_DAYE_DATA_ENGINE_MQH__

#include <DayeTrader/EXP0018/DAYE_DataAudit.mqh>
#include <DayeTrader/EXP0018/DAYE_DataSelfTest.mqh>

class CDayeMultiSymbolDataEngine
{
private:
   DAYE_DataSyncConfig m_config;
   DAYE_TimeConfig m_time_config;
   DAYE_SymbolDescriptor m_symbol_a;
   DAYE_SymbolDescriptor m_symbol_b;
   DAYE_DataSyncSummary m_previous_summary;
   bool m_has_previous_summary;
   datetime m_last_probe_a;
   datetime m_last_probe_b;
   datetime m_last_full_refresh_utc;
   bool m_initialized;
   CDayeDataAuditWriter m_audit;

   void BuildBaseSummary(DAYE_DataSyncSummary &summary,const datetime processing_time_utc)
   {
      ZeroMemory(summary);
      summary.schema_version = DAYE_DATA_SCHEMA_VERSION;
      summary.status = DAYE_DATA_STATUS_SYMBOL_UNAVAILABLE;
      summary.reason_code = "not_evaluated";
      summary.is_ready = false;
      summary.is_complete = false;
      summary.is_replay_safe = true;
      summary.run_key = "EXP0018|P02|" + m_config.canonical_symbol_a + "|" + m_config.canonical_symbol_b + "|" + EnumToString(m_config.base_timeframe);
      summary.broker_symbol_a = m_config.broker_symbol_a;
      summary.broker_symbol_b = m_config.broker_symbol_b;
      summary.canonical_symbol_a = m_config.canonical_symbol_a;
      summary.canonical_symbol_b = m_config.canonical_symbol_b;
      summary.timeframe = m_config.base_timeframe;
      summary.requested_bars_per_symbol = m_config.requested_bars_per_symbol;
      summary.processing_time_utc = processing_time_utc;
      summary.availability_time_utc = processing_time_utc;
   }

public:
   CDayeMultiSymbolDataEngine(void)
   {
      ZeroMemory(m_previous_summary);
      m_has_previous_summary = false;
      m_last_probe_a = 0;
      m_last_probe_b = 0;
      m_last_full_refresh_utc = 0;
      m_initialized = false;
   }

   bool Initialize(const DAYE_DataSyncConfig &config,
                   const DAYE_TimeConfig &time_config,
                   const bool run_self_tests,
                   const bool write_audit_csv,
                   const string audit_filename)
   {
      string reason = "";
      if(!DAYE_ValidateDataSyncConfig(config,reason))
      {
         Print("EXP0018 P02 initialization failed reason=",reason);
         return false;
      }
      if(!DAYE_ValidateTimeConfig(time_config,reason))
      {
         Print("EXP0018 P02 time config invalid reason=",reason);
         return false;
      }
      if(run_self_tests && !DAYE_RunEmbeddedDataSyncSelfTests())
      {
         Print("EXP0018 P02 initialization blocked because embedded self-test failed.");
         return false;
      }

      m_config = config;
      m_time_config = time_config;
      if(!DAYE_LoadSymbolDescriptor(config.broker_symbol_a,config.canonical_symbol_a,m_symbol_a))
      {
         Print("EXP0018 P02 symbol A descriptor failed reason=",m_symbol_a.reason_code);
         return false;
      }
      if(!DAYE_LoadSymbolDescriptor(config.broker_symbol_b,config.canonical_symbol_b,m_symbol_b))
      {
         Print("EXP0018 P02 symbol B descriptor failed reason=",m_symbol_b.reason_code);
         return false;
      }
      if(!m_audit.Open(audit_filename,write_audit_csv))
         return false;

      m_initialized = true;
      Print("EXP0018 P02 Multi-Symbol Data Synchronization v2 initialized. Alignment is exact UTC timestamp only. Missing bars are explicit. No forward-fill, hunt, signal, drawing, risk, or order authority exists.");
      return true;
   }

   bool ShouldRefresh(const datetime processing_time_utc)
   {
      datetime probe_a = 0;
      datetime probe_b = 0;
      bool ok_a = DAYE_ProbeLatestClosedBarTime(m_config.broker_symbol_a,m_config.base_timeframe,probe_a);
      bool ok_b = DAYE_ProbeLatestClosedBarTime(m_config.broker_symbol_b,m_config.base_timeframe,probe_b);
      if(!ok_a || !ok_b)
         return true;
      if(!m_has_previous_summary || !m_previous_summary.is_ready)
         return true;
      if(probe_a != m_last_probe_a || probe_b != m_last_probe_b)
         return true;
      if(m_last_full_refresh_utc <= 0 || (long)processing_time_utc - (long)m_last_full_refresh_utc >= m_config.force_full_refresh_seconds)
         return true;
      return false;
   }

   bool Process(const datetime current_broker_time,
                const bool print_summary,
                const bool print_health,
                const bool print_events,
                const bool show_chart_comment,
                const bool write_summary_rows,
                const bool write_latest_pair_row)
   {
      if(!m_initialized)
         return false;

      datetime processing_time_utc = TimeGMT();
      if(processing_time_utc <= 0)
      {
         int broker_offset = 0;
         bool replay_safe = true;
         string reason = "";
         if(!DAYE_BrokerToUtc(current_broker_time,m_time_config,processing_time_utc,broker_offset,replay_safe,reason))
            processing_time_utc = current_broker_time;
      }

      if(!ShouldRefresh(processing_time_utc))
         return true;

      DAYE_DataSyncSummary summary;
      BuildBaseSummary(summary,processing_time_utc);
      DAYE_SymbolDataHealth health_a;
      DAYE_SymbolDataHealth health_b;
      DAYE_SymbolBar bars_a[];
      DAYE_SymbolBar bars_b[];
      DAYE_SynchronizedBarPair pairs[];

      bool loaded_a = DAYE_LoadClosedBars(m_symbol_a,m_config,m_time_config,current_broker_time,bars_a,health_a);
      bool loaded_b = DAYE_LoadClosedBars(m_symbol_b,m_config,m_time_config,current_broker_time,bars_b,health_b);
      summary.copied_a = health_a.copied_bars;
      summary.copied_b = health_b.copied_bars;
      summary.invalid_a = health_a.invalid_bar_count;
      summary.invalid_b = health_b.invalid_bar_count;
      summary.duplicate_a = health_a.duplicate_timestamp_count;
      summary.duplicate_b = health_b.duplicate_timestamp_count;

      if(!loaded_a || !loaded_b)
      {
         if(!loaded_a)
         {
            summary.status = health_a.status;
            summary.reason_code = health_a.broker_symbol + ":" + health_a.reason_code;
         }
         else
         {
            summary.status = health_b.status;
            summary.reason_code = health_b.broker_symbol + ":" + health_b.reason_code;
         }
         summary.is_ready = false;
         summary.is_complete = false;
      }
      else
      {
         summary.is_replay_safe = true;
         for(int i=0;i<ArraySize(bars_a);i++)
            if(!bars_a[i].is_replay_safe) summary.is_replay_safe = false;
         for(int i=0;i<ArraySize(bars_b);i++)
            if(!bars_b[i].is_replay_safe) summary.is_replay_safe = false;
         DAYE_AlignBarsByExactUtc(bars_a,bars_b,m_config,processing_time_utc,pairs,summary);
         if(ArraySize(pairs) > 0)
            summary.availability_time_utc = pairs[ArraySize(pairs)-1].availability_time_utc;
      }

      DAYE_DataSyncEvent events[];
      DAYE_DetectDataSyncEvents(m_has_previous_summary,m_previous_summary,summary,events);
      for(int i=0;i<ArraySize(events);i++)
      {
         if(print_events)
            Print(DAYE_FormatDataSyncEvent(events[i]));
         if(!m_audit.WriteEvent(events[i]))
            Print("EXP0018 P02 audit event write failed id=",events[i].event_id);
      }

      if(print_summary)
         Print(DAYE_FormatDataSyncSummary(summary));
      if(print_health)
      {
         Print("  ",DAYE_FormatSymbolHealth(health_a));
         Print("  ",DAYE_FormatSymbolHealth(health_b));
      }
      if(write_summary_rows && !m_audit.WriteSummary(summary))
         Print("EXP0018 P02 audit summary write failed.");
      if(write_latest_pair_row && ArraySize(pairs) > 0 && !m_audit.WritePair(pairs[ArraySize(pairs)-1]))
         Print("EXP0018 P02 audit pair write failed.");

      if(show_chart_comment)
      {
         string text = DAYE_FormatDataSyncSummary(summary) + "\n" +
                       DAYE_FormatSymbolHealth(health_a) + "\n" +
                       DAYE_FormatSymbolHealth(health_b) + "\n" +
                       "Data synchronization only — no signals or trading.";
         Comment(text);
      }
      else
         Comment("");

      datetime probe_a = 0;
      datetime probe_b = 0;
      if(DAYE_ProbeLatestClosedBarTime(m_config.broker_symbol_a,m_config.base_timeframe,probe_a))
         m_last_probe_a = probe_a;
      if(DAYE_ProbeLatestClosedBarTime(m_config.broker_symbol_b,m_config.base_timeframe,probe_b))
         m_last_probe_b = probe_b;
      m_last_full_refresh_utc = processing_time_utc;
      m_previous_summary = summary;
      m_has_previous_summary = true;
      return true;
   }

   void Shutdown(void)
   {
      Comment("");
      m_audit.Close();
      ZeroMemory(m_previous_summary);
      m_has_previous_summary = false;
      m_last_probe_a = 0;
      m_last_probe_b = 0;
      m_last_full_refresh_utc = 0;
      m_initialized = false;
   }
};

#endif
