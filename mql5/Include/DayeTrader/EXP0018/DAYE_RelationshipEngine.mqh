#ifndef __EXP0018_DAYE_RELATIONSHIP_ENGINE_MQH__
#define __EXP0018_DAYE_RELATIONSHIP_ENGINE_MQH__

#include <DayeTrader/EXP0018/DAYE_RelationshipSelfTest.mqh>

class CDayeRelationshipEngine
{
private:
   DAYE_RelationshipConfig m_config;
   DAYE_TimeConfig m_time_config;
   DAYE_RelationshipDefinition m_registry[];
   CDayePeriodAggregationEngine m_period_engine;
   CDayeRelationshipStore m_store;
   CDayeRelationshipAuditWriter m_audit;
   DAYE_RelationshipStoreSummary m_previous_summary;
   DAYE_RelationshipStoreSummary m_current_summary;
   bool m_has_previous_summary;
   bool m_has_current_summary;
   bool m_initialized;
   string m_last_source_fingerprint;

   string BuildSourceFingerprint(const DAYE_PeriodStoreSummary &summary)
   {
      return summary.run_key + "|" +
             IntegerToString(summary.paired_period_count) + "|" +
             summary.latest_paired_period_id + "|" +
             summary.latest_complete_paired_period_id + "|" +
             IntegerToString((long)summary.latest_period_start_utc) + "|" +
             IntegerToString((int)summary.status);
   }

public:
   CDayeRelationshipEngine(void)
   {
      ZeroMemory(m_previous_summary);
      ZeroMemory(m_current_summary);
      m_has_previous_summary = false;
      m_has_current_summary = false;
      m_initialized = false;
      m_last_source_fingerprint = "";
   }

   bool Initialize(const DAYE_RelationshipConfig &config,
                   const DAYE_TimeConfig &time_config,
                   const bool run_self_tests,
                   const bool write_audit_csv,
                   const string audit_filename)
   {
      string reason = "";
      if(!DAYE_ValidateRelationshipConfig(config,reason))
      {
         Print("EXP0018 P04 invalid relationship config reason=",reason);
         return false;
      }
      if(!DAYE_ValidatePeriodAggregationConfig(config.period_config,reason))
      {
         Print("EXP0018 P04 invalid P03 config reason=",reason);
         return false;
      }
      if(!DAYE_ValidateTimeConfig(time_config,reason))
      {
         Print("EXP0018 P04 invalid time config reason=",reason);
         return false;
      }
      if(run_self_tests && !DAYE_RunEmbeddedRelationshipSelfTests())
      {
         Print("EXP0018 P04 initialization blocked because embedded self-test failed.");
         return false;
      }

      m_config = config;
      m_time_config = time_config;
      DAYE_BuildCanonicalRelationshipRegistry(m_registry);
      if(!DAYE_ValidateCanonicalRelationshipRegistry(m_registry,reason))
      {
         Print("EXP0018 P04 registry validation failed reason=",reason);
         return false;
      }
      if(!m_period_engine.Initialize(config.period_config,time_config,run_self_tests,false,""))
      {
         Print("EXP0018 P04 could not initialize P03 dependency.");
         return false;
      }
      if(!m_audit.Open(audit_filename,write_audit_csv))
      {
         m_period_engine.Shutdown();
         return false;
      }
      if(write_audit_csv)
      {
         for(int i=0;i<ArraySize(m_registry);i++)
            m_audit.WriteRegistry(m_registry[i]);
         m_audit.Flush();
      }

      m_initialized = true;
      Print("EXP0018 P04 Declarative 22-Relationship Registry v2 initialized. Registry topology only; no hunt, direction, divergence, drawing, risk, or order authority exists.");
      return true;
   }

   bool Process(const datetime current_broker_time,
                const bool print_summary,
                const bool print_latest_ready,
                const bool print_events,
                const bool show_chart_comment,
                const bool write_summary_rows,
                const int audit_latest_resolution_count)
   {
      if(!m_initialized)
         return false;

      m_period_engine.Process(current_broker_time,false,false,false,false,false,0);

      DAYE_PeriodStoreSummary period_summary;
      if(!m_period_engine.GetCurrentSummary(period_summary))
         return true;

      string fingerprint = BuildSourceFingerprint(period_summary);
      if(fingerprint == m_last_source_fingerprint)
         return true;
      m_last_source_fingerprint = fingerprint;

      DAYE_PairedPeriodSnapshot periods[];
      m_period_engine.ExportPeriods(periods);
      datetime processing_time_utc = TimeGMT();
      if(processing_time_utc <= 0)
         processing_time_utc = current_broker_time;

      DAYE_RelationshipResolution resolutions[];
      DAYE_RelationshipStoreSummary summary;
      DAYE_ResolveRelationshipOpportunities(periods,m_registry,m_config,processing_time_utc,resolutions,summary);
      summary.is_replay_safe = summary.is_replay_safe && period_summary.is_replay_safe;
      m_store.Replace(resolutions);

      DAYE_RelationshipEvent events[];
      DAYE_DetectRelationshipEvents(m_has_previous_summary,m_previous_summary,summary,events);
      for(int i=0;i<ArraySize(events);i++)
      {
         if(print_events)
            Print(DAYE_FormatRelationshipEvent(events[i]));
         m_audit.WriteEvent(events[i]);
      }

      if(print_summary)
         Print(DAYE_FormatRelationshipSummary(summary));
      if(print_latest_ready)
      {
         DAYE_RelationshipResolution latest;
         if(m_store.LatestReady(latest))
            Print("  latest_ready ",DAYE_FormatRelationshipResolution(latest));
      }

      if(write_summary_rows)
         m_audit.WriteSummary(summary);
      int write_count = audit_latest_resolution_count;
      if(write_count < 0) write_count = 0;
      int start_index = m_store.Count() - write_count;
      if(start_index < 0) start_index = 0;
      for(int i=start_index;i<m_store.Count();i++)
      {
         DAYE_RelationshipResolution item;
         if(m_store.Get(i,item))
            m_audit.WriteResolution(item);
      }
      m_audit.Flush();

      if(show_chart_comment)
         Comment(DAYE_FormatRelationshipSummary(summary) + "\nRelationship topology only — no hunt, SMT, line, or trading.");
      else
         Comment("");

      m_previous_summary = summary;
      m_current_summary = summary;
      m_has_previous_summary = true;
      m_has_current_summary = true;
      return true;
   }

   bool GetCurrentSummary(DAYE_RelationshipStoreSummary &summary)
   {
      if(!m_has_current_summary)
         return false;
      summary = m_current_summary;
      return true;
   }

   int ExportRegistry(DAYE_RelationshipDefinition &items[])
   {
      ArrayResize(items,ArraySize(m_registry));
      for(int i=0;i<ArraySize(m_registry);i++)
         items[i] = m_registry[i];
      return ArraySize(items);
   }

   int ExportResolutions(DAYE_RelationshipResolution &items[])
   {
      return m_store.Export(items);
   }

   void Shutdown(void)
   {
      Comment("");
      m_audit.Close();
      m_store.Clear();
      m_period_engine.Shutdown();
      ArrayResize(m_registry,0);
      ZeroMemory(m_previous_summary);
      ZeroMemory(m_current_summary);
      m_has_previous_summary = false;
      m_has_current_summary = false;
      m_initialized = false;
      m_last_source_fingerprint = "";
   }
};

#endif
