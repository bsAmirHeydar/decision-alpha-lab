#ifndef __EXP0018_DAYE_HUNT_ENGINE_MQH__
#define __EXP0018_DAYE_HUNT_ENGINE_MQH__

#include <DayeTrader/EXP0018/DAYE_HuntSelfTest.mqh>

class CDayeHuntEngine
{
private:
   DAYE_HuntConfig m_config;
   DAYE_TimeConfig m_time_config;
   CDayeRelationshipEngine m_relationship_engine;
   CDayeHuntStore m_store;
   CDayeHuntAuditWriter m_audit;
   DAYE_HuntStoreSummary m_previous_summary;
   DAYE_HuntStoreSummary m_current_summary;
   bool m_has_previous_summary;
   bool m_has_current_summary;
   bool m_initialized;
   string m_last_source_fingerprint;

   string BuildSourceFingerprint(const DAYE_RelationshipStoreSummary &summary)
   {
      return summary.run_key + "|" +
             IntegerToString(summary.ready_resolution_count) + "|" +
             summary.latest_ready_opportunity_id + "|" +
             IntegerToString((long)summary.event_time_utc) + "|" +
             IntegerToString((long)summary.availability_time_utc) + "|" +
             IntegerToString((int)summary.status);
   }

public:
   CDayeHuntEngine(void)
   {
      ZeroMemory(m_previous_summary);
      ZeroMemory(m_current_summary);
      m_has_previous_summary=false;
      m_has_current_summary=false;
      m_initialized=false;
      m_last_source_fingerprint="";
   }

   bool Initialize(const DAYE_HuntConfig &config,
                   const DAYE_TimeConfig &time_config,
                   const bool run_self_tests,
                   const bool write_audit_csv,
                   const string audit_filename)
   {
      string reason="";
      if(!DAYE_ValidateHuntConfig(config,reason))
      {
         Print("EXP0018 P05 invalid hunt config reason=",reason);
         return false;
      }
      if(!DAYE_ValidateRelationshipConfig(config.relationship_config,reason))
      {
         Print("EXP0018 P05 invalid P04 config reason=",reason);
         return false;
      }
      if(!DAYE_ValidateTimeConfig(time_config,reason))
      {
         Print("EXP0018 P05 invalid time config reason=",reason);
         return false;
      }
      if(run_self_tests && !DAYE_RunEmbeddedHuntSelfTests())
      {
         Print("EXP0018 P05 initialization blocked because embedded self-test failed.");
         return false;
      }

      m_config=config;
      m_time_config=time_config;
      if(!m_relationship_engine.Initialize(config.relationship_config,time_config,run_self_tests,false,""))
      {
         Print("EXP0018 P05 could not initialize P04 dependency.");
         return false;
      }
      if(!m_audit.Open(audit_filename,write_audit_csv))
      {
         m_relationship_engine.Shutdown();
         return false;
      }

      m_initialized=true;
      Print("EXP0018 P05 Touch-Only Hunt Observation v2 initialized. HIGH/LOW touch facts only; no BUY/SELL mapping, close confirmation, lifecycle retirement, drawing, risk, or order authority exists.");
      return true;
   }

   bool Process(const datetime current_broker_time,
                const bool print_summary,
                const bool print_latest_one_sided,
                const bool print_events,
                const bool show_chart_comment,
                const bool write_summary_rows,
                const int audit_latest_observation_count)
   {
      if(!m_initialized) return false;

      m_relationship_engine.Process(current_broker_time,false,false,false,false,false,0);
      DAYE_RelationshipStoreSummary relationship_summary;
      if(!m_relationship_engine.GetCurrentSummary(relationship_summary))
         return true;

      string fingerprint=BuildSourceFingerprint(relationship_summary);
      if(fingerprint == m_last_source_fingerprint)
         return true;
      m_last_source_fingerprint=fingerprint;

      DAYE_RelationshipResolution resolutions[];
      m_relationship_engine.ExportResolutions(resolutions);
      datetime processing_time_utc=TimeGMT();
      if(processing_time_utc <= 0) processing_time_utc=current_broker_time;

      DAYE_HuntObservation previous_items[];
      m_store.Export(previous_items);
      DAYE_HuntObservation current_items[];
      DAYE_HuntStoreSummary summary;
      DAYE_ClassifyHuntObservations(resolutions,m_config,processing_time_utc,current_items,summary);
      summary.is_replay_safe = summary.is_replay_safe && relationship_summary.is_replay_safe;

      DAYE_HuntEvent events[];
      DAYE_DetectHuntEvents(m_has_previous_summary,m_previous_summary,summary,previous_items,current_items,events);
      m_store.Replace(current_items);

      for(int i=0;i<ArraySize(events);i++)
      {
         if(print_events) Print(DAYE_FormatHuntEvent(events[i]));
         m_audit.WriteEvent(events[i]);
      }

      if(print_summary) Print(DAYE_FormatHuntSummary(summary));
      if(print_latest_one_sided)
      {
         DAYE_HuntObservation latest;
         if(m_store.LatestOneSided(latest))
            Print("  latest_one_sided ",DAYE_FormatHuntObservation(latest));
      }

      if(write_summary_rows) m_audit.WriteSummary(summary);
      int write_count=audit_latest_observation_count;
      if(write_count < 0) write_count=0;
      int start_index=m_store.Count()-write_count;
      if(start_index < 0) start_index=0;
      for(int i=start_index;i<m_store.Count();i++)
      {
         DAYE_HuntObservation item;
         if(m_store.Get(i,item)) m_audit.WriteObservation(item);
      }
      m_audit.Flush();

      if(show_chart_comment)
         Comment(DAYE_FormatHuntSummary(summary) + "\nTouch facts only — no direction, confirmation, line, or trading.");
      else
         Comment("");

      m_previous_summary=summary;
      m_current_summary=summary;
      m_has_previous_summary=true;
      m_has_current_summary=true;
      return true;
   }

   bool GetCurrentSummary(DAYE_HuntStoreSummary &summary)
   {
      if(!m_has_current_summary) return false;
      summary=m_current_summary;
      return true;
   }

   int ExportObservations(DAYE_HuntObservation &items[])
   {
      return m_store.Export(items);
   }

   void Shutdown(void)
   {
      Comment("");
      m_audit.Close();
      m_store.Clear();
      m_relationship_engine.Shutdown();
      ZeroMemory(m_previous_summary);
      ZeroMemory(m_current_summary);
      m_has_previous_summary=false;
      m_has_current_summary=false;
      m_initialized=false;
      m_last_source_fingerprint="";
   }
};

#endif
