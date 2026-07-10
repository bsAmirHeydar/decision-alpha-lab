#ifndef __EXP0018_DAYE_SESSION_BOX_ENGINE_MQH__
#define __EXP0018_DAYE_SESSION_BOX_ENGINE_MQH__

#include <DayeTrader/EXP0018/DAYE_SessionBoxSelfTest.mqh>

class CDayeSessionBoxEngine
{
private:
   DAYE_SessionBoxConfig m_config;
   DAYE_TimeConfig m_time_config;
   CDayePeriodAggregationEngine m_period_engine;
   CDayeSessionBoxStore m_store;
   CDayeSessionBoxAuditWriter m_audit;
   DAYE_SessionBoxStoreSummary m_current_summary;
   DAYE_SessionBoxStoreSummary m_previous_summary;
   bool m_has_current_summary;
   bool m_has_previous_summary;
   datetime m_last_projection_refresh_utc;
   string m_last_source_fingerprint;
   bool m_initialized;

   string BuildSourceFingerprint(const DAYE_PairedPeriodSnapshot &periods[])
   {
      string value=IntegerToString(ArraySize(periods));
      for(int i=MathMax(0,ArraySize(periods)-12);i<ArraySize(periods);i++)
      {
         if(periods[i].period_family!=DAYE_FAMILY_SESSION) continue;
         value+="|"+periods[i].period_instance_id+"|"+
                IntegerToString((long)periods[i].availability_time_utc)+"|"+
                DoubleToString(periods[i].symbol_a.high,8)+"|"+DoubleToString(periods[i].symbol_a.low,8)+"|"+
                DoubleToString(periods[i].symbol_b.high,8)+"|"+DoubleToString(periods[i].symbol_b.low,8)+"|"+
                IntegerToString((int)periods[i].symbol_a.completeness)+"|"+IntegerToString((int)periods[i].symbol_b.completeness);
      }
      return DAYE_SessionBoxHashText(value);
   }

   void AppendExpectedNameForChart(const long chart_id,const string object_name,long &chart_ids[],string &names[])
   {
      int n=ArraySize(names); ArrayResize(names,n+1); ArrayResize(chart_ids,n+1);
      names[n]=object_name; chart_ids[n]=chart_id;
   }

   void BuildProjection(const DAYE_SymbolPeriodSnapshot &snapshot,const long chart_id,
                        const DAYE_SessionBoxGeometry &geometry,const bool replay_safe,
                        DAYE_SessionBoxProjection &projection)
   {
      ZeroMemory(projection);
      projection.schema_version=DAYE_SESSION_BOX_SCHEMA_VERSION;
      projection.projection_id=DAYE_BuildSessionBoxProjectionId(snapshot.snapshot_id,chart_id);
      projection.symbol_snapshot_id=snapshot.snapshot_id;
      projection.period_instance_id=snapshot.period_instance_id;
      projection.trading_day_key=snapshot.trading_day_key;
      projection.session_code=snapshot.period_code;
      projection.broker_symbol=snapshot.broker_symbol;
      projection.canonical_symbol=snapshot.canonical_symbol;
      projection.target_chart_id=chart_id;
      projection.target_chart_timeframe=ChartPeriod(chart_id);
      projection.object_name=DAYE_BuildSessionBoxObjectName(snapshot.snapshot_id);
      projection.source_completeness=snapshot.completeness;
      projection.geometry=geometry;
      projection.is_open_session=(snapshot.completeness==DAYE_PERIOD_COMPLETENESS_OPEN);
      projection.is_replay_safe=replay_safe;
      projection.event_time_utc=snapshot.window.end_utc;
      projection.availability_time_utc=snapshot.availability_time_utc;
      projection.processing_time_utc=TimeGMT();
   }

   void CountProjectionStatus(const DAYE_SessionBoxProjection &p,DAYE_SessionBoxStoreSummary &summary)
   {
      if(p.status==DAYE_SESSION_BOX_STATUS_CREATED) summary.created_count++;
      else if(p.status==DAYE_SESSION_BOX_STATUS_UPDATED_OPEN) summary.updated_open_count++;
      else if(p.status==DAYE_SESSION_BOX_STATUS_VERIFIED_CLOSED) summary.verified_closed_count++;
      else if(p.status==DAYE_SESSION_BOX_STATUS_REPAIRED) summary.repaired_count++;
      else if(p.status==DAYE_SESSION_BOX_STATUS_WAITING_FOR_SYMBOL_CHART) summary.waiting_chart_count++;
      else if(p.status==DAYE_SESSION_BOX_STATUS_INVALID_GEOMETRY) summary.invalid_geometry_count++;
      else if(p.status==DAYE_SESSION_BOX_STATUS_OBJECT_CREATE_FAILED || p.status==DAYE_SESSION_BOX_STATUS_OBJECT_UPDATE_FAILED) summary.failed_object_count++;
      if(p.is_open_session && p.is_drawn) summary.open_box_count++;
      if(!p.is_open_session && p.is_drawn) summary.closed_box_count++;
   }

   void ProcessSymbolSnapshot(const DAYE_SymbolPeriodSnapshot &snapshot,const datetime lookback_start_utc,
                              const datetime processing_time_utc,
                              DAYE_SessionBoxStoreSummary &summary,
                              DAYE_SessionBoxEvent &events[],
                              long &expected_chart_ids[],string &expected_names[])
   {
      DAYE_SessionBoxProjectionStatus eligibility_status;
      string reason="";
      if(!DAYE_IsSessionSnapshotEligible(snapshot,m_config,lookback_start_utc,eligibility_status,reason))
      {
         summary.skipped_ineligible_count++;
         return;
      }
      summary.eligible_symbol_session_count++;
      DAYE_SessionBoxGeometry geometry;
      bool replay_safe=true;
      if(!DAYE_BuildSessionBoxGeometry(snapshot,m_time_config,geometry,replay_safe))
      {
         summary.invalid_geometry_count++;
         return;
      }

      long chart_ids[];
      int chart_count=DAYE_ResolveSessionBoxTargetCharts(snapshot.broker_symbol,m_config,chart_ids);
      if(chart_count<1)
      {
         DAYE_SessionBoxProjection projection;
         BuildProjection(snapshot,-1,geometry,replay_safe,projection);
         projection.status=DAYE_SESSION_BOX_STATUS_WAITING_FOR_SYMBOL_CHART;
         projection.reason_code="no_open_chart_for_exact_broker_symbol";
         projection.processing_time_utc=processing_time_utc;
         DAYE_SessionBoxProjection previous; DAYE_SessionBoxProjectionStatus old_status=DAYE_SESSION_BOX_STATUS_UNKNOWN;
         int old_index=m_store.Find(projection.projection_id);
         if(old_index>=0 && m_store.Get(old_index,previous)) old_status=previous.status;
         m_store.Upsert(projection,m_config.maximum_projection_records);
         DAYE_AppendSessionBoxEvent(events,projection,old_status,processing_time_utc);
         CountProjectionStatus(projection,summary);
         return;
      }

      for(int i=0;i<chart_count;i++)
      {
         DAYE_SessionBoxProjection projection;
         BuildProjection(snapshot,chart_ids[i],geometry,replay_safe,projection);
         projection.processing_time_utc=processing_time_utc;
         DAYE_SessionBoxProjection previous;
         DAYE_SessionBoxProjectionStatus old_status=DAYE_SESSION_BOX_STATUS_UNKNOWN;
         int old_index=m_store.Find(projection.projection_id);
         if(old_index>=0 && m_store.Get(old_index,previous))
         {
            old_status=previous.status;
            projection.create_count=previous.create_count;
            projection.update_count=previous.update_count;
            projection.verify_count=previous.verify_count;
            projection.repair_count=previous.repair_count;
         }
         bool manual_delete_repaired=false;
         projection.status=DAYE_ProjectSessionBoxToChart(snapshot,chart_ids[i],geometry,m_config,projection.reason_code,manual_delete_repaired);
         projection.is_drawn=(projection.status==DAYE_SESSION_BOX_STATUS_CREATED || projection.status==DAYE_SESSION_BOX_STATUS_UPDATED_OPEN || projection.status==DAYE_SESSION_BOX_STATUS_VERIFIED_CLOSED || projection.status==DAYE_SESSION_BOX_STATUS_REPAIRED);
         if(projection.status==DAYE_SESSION_BOX_STATUS_CREATED) projection.create_count++;
         if(projection.status==DAYE_SESSION_BOX_STATUS_UPDATED_OPEN) projection.update_count++;
         if(projection.status==DAYE_SESSION_BOX_STATUS_VERIFIED_CLOSED) projection.verify_count++;
         if(projection.status==DAYE_SESSION_BOX_STATUS_REPAIRED) projection.repair_count++;
         if(!m_store.Upsert(projection,m_config.maximum_projection_records))
         {
            projection.status=DAYE_SESSION_BOX_STATUS_STORE_CAPACITY_EXCEEDED;
            projection.reason_code="projection_store_capacity_exceeded";
            projection.is_drawn=false;
         }
         DAYE_AppendSessionBoxEvent(events,projection,old_status,processing_time_utc);
         CountProjectionStatus(projection,summary);
         AppendExpectedNameForChart(chart_ids[i],projection.object_name,expected_chart_ids,expected_names);
         summary.latest_projection_id=projection.projection_id;
         summary.latest_object_name=projection.object_name;
         summary.latest_period_instance_id=snapshot.period_instance_id;
         if(projection.availability_time_utc>summary.availability_time_utc) summary.availability_time_utc=projection.availability_time_utc;
         if(!projection.is_replay_safe) summary.is_replay_safe=false;
         m_audit.WriteProjection(projection);
      }
   }

   int CleanupOrphans(const long &expected_chart_ids[],const string &expected_names[])
   {
      if(!m_config.delete_owned_objects_outside_lookback) return 0;
      int deleted=0;
      long chart=ChartFirst();
      while(chart>=0)
      {
         string per_chart[]; ArrayResize(per_chart,0);
         for(int i=0;i<ArraySize(expected_names);i++)
         {
            if(expected_chart_ids[i]!=chart) continue;
            int n=ArraySize(per_chart); ArrayResize(per_chart,n+1); per_chart[n]=expected_names[i];
         }
         if(ChartSymbol(chart)==m_config.period_config.data_config.broker_symbol_a || ChartSymbol(chart)==m_config.period_config.data_config.broker_symbol_b)
            deleted+=DAYE_DeleteOrphanedSessionBoxes(chart,per_chart);
         chart=ChartNext(chart);
      }
      return deleted;
   }

public:
   CDayeSessionBoxEngine(void)
   {
      ZeroMemory(m_current_summary); ZeroMemory(m_previous_summary);
      m_has_current_summary=false; m_has_previous_summary=false;
      m_last_projection_refresh_utc=0; m_last_source_fingerprint=""; m_initialized=false;
   }

   bool Initialize(const DAYE_SessionBoxConfig &config,const DAYE_TimeConfig &time_config,
                   const bool run_self_tests,const bool write_audit,const string audit_filename)
   {
      string reason="";
      if(!DAYE_ValidateSessionBoxConfig(config,reason))
      {
         Print("EXP0018 P09 invalid config reason=",reason); return false;
      }
      if(!DAYE_ValidatePeriodAggregationConfig(config.period_config,reason))
      {
         Print("EXP0018 P09 period config invalid reason=",reason); return false;
      }
      if(!DAYE_ValidateTimeConfig(time_config,reason))
      {
         Print("EXP0018 P09 time config invalid reason=",reason); return false;
      }
      if(run_self_tests && !DAYE_RunEmbeddedSessionBoxSelfTests())
      {
         Print("EXP0018 P09 embedded self-tests failed."); return false;
      }
      m_config=config; m_time_config=time_config;
      if(!m_period_engine.Initialize(config.period_config,time_config,false,false,"")) return false;
      if(!m_audit.Open(audit_filename,write_audit)) return false;
      m_initialized=true;
      Print("EXP0018 P09 Session Box Rendering v2 initialized. A/L/N/P rectangles use symbol-local P03 ranges. No signal or execution authority exists.");
      return true;
   }

   bool Process(const datetime current_broker_time,const bool print_summary,const bool print_events,
                const bool show_chart_comment,const bool write_summary_rows)
   {
      if(!m_initialized) return false;
      datetime processing_time_utc=TimeGMT();
      if(processing_time_utc<=0) processing_time_utc=current_broker_time;
      m_period_engine.Process(current_broker_time,false,false,false,false,false,0);
      DAYE_PeriodStoreSummary source_summary;
      DAYE_PairedPeriodSnapshot periods[];
      bool source_ready=m_period_engine.GetCurrentSummary(source_summary);
      m_period_engine.ExportPeriods(periods);

      DAYE_SessionBoxStoreSummary summary;
      ZeroMemory(summary);
      summary.schema_version=DAYE_SESSION_BOX_SCHEMA_VERSION;
      summary.processing_time_utc=processing_time_utc;
      summary.is_replay_safe=true;
      summary.source_period_count=ArraySize(periods);
      if(!source_ready || !source_summary.is_ready)
      {
         summary.status=DAYE_SESSION_BOX_ENGINE_SOURCE_NOT_READY;
         summary.reason_code=source_ready?source_summary.reason_code:"p03_summary_unavailable";
         summary.is_ready=false;
         m_current_summary=summary; m_has_current_summary=true;
         if(print_summary) Print(DAYE_FormatSessionBoxSummary(summary));
         if(show_chart_comment) Comment(DAYE_FormatSessionBoxSummary(summary)); else Comment("");
         if(write_summary_rows) m_audit.WriteSummary(summary);
         return true;
      }

      string fingerprint=BuildSourceFingerprint(periods);
      bool verification_due=(m_last_projection_refresh_utc<=0 || (long)processing_time_utc-(long)m_last_projection_refresh_utc>=m_config.object_verification_interval_seconds);
      if(fingerprint==m_last_source_fingerprint && !verification_due) return true;

      datetime lookback_start_utc=processing_time_utc-(datetime)(m_config.lookback_weeks*7*86400);
      DAYE_SessionBoxEvent events[];
      long expected_chart_ids[];
      string expected_names[];
      for(int i=0;i<ArraySize(periods);i++)
      {
         if(periods[i].period_family!=DAYE_FAMILY_SESSION || !DAYE_IsCanonicalSessionCode(periods[i].period_code)) continue;
         summary.source_session_count++;
         ProcessSymbolSnapshot(periods[i].symbol_a,lookback_start_utc,processing_time_utc,summary,events,expected_chart_ids,expected_names);
         ProcessSymbolSnapshot(periods[i].symbol_b,lookback_start_utc,processing_time_utc,summary,events,expected_chart_ids,expected_names);
      }
      summary.deleted_orphan_count=CleanupOrphans(expected_chart_ids,expected_names);
      summary.projection_count=m_store.Count();
      summary.event_time_utc=processing_time_utc;
      summary.is_ready=(summary.eligible_symbol_session_count>0);
      if(summary.failed_object_count>0 || summary.invalid_geometry_count>0)
      {
         summary.status=DAYE_SESSION_BOX_ENGINE_DEGRADED;
         summary.reason_code="projection_completed_with_explicit_failures";
      }
      else if(summary.eligible_symbol_session_count<1)
      {
         summary.status=DAYE_SESSION_BOX_ENGINE_NO_ELIGIBLE_SESSIONS;
         summary.reason_code="no_session_snapshot_met_render_policy";
      }
      else if(summary.waiting_chart_count>=summary.eligible_symbol_session_count && summary.created_count+summary.updated_open_count+summary.verified_closed_count+summary.repaired_count==0)
      {
         summary.status=DAYE_SESSION_BOX_ENGINE_WAITING_FOR_CHART;
         summary.reason_code="eligible_sessions_exist_but_no_matching_symbol_chart_is_open";
      }
      else
      {
         summary.status=DAYE_SESSION_BOX_ENGINE_READY;
         summary.reason_code="session_boxes_projected_from_symbol_local_p03_ranges";
      }

      for(int i=0;i<ArraySize(events);i++)
      {
         if(print_events) Print(DAYE_FormatSessionBoxEvent(events[i]));
         m_audit.WriteEvent(events[i]);
      }
      if(print_summary) Print(DAYE_FormatSessionBoxSummary(summary));
      if(show_chart_comment) Comment(DAYE_FormatSessionBoxSummary(summary)+"\nSession boxes only — no signal or trading authority."); else Comment("");
      if(write_summary_rows) m_audit.WriteSummary(summary);
      m_audit.Flush();

      m_previous_summary=m_current_summary; m_has_previous_summary=m_has_current_summary;
      m_current_summary=summary; m_has_current_summary=true;
      m_last_source_fingerprint=fingerprint;
      m_last_projection_refresh_utc=processing_time_utc;
      return true;
   }

   bool GetCurrentSummary(DAYE_SessionBoxStoreSummary &summary)
   {
      if(!m_has_current_summary) return false;
      summary=m_current_summary; return true;
   }

   int ExportProjections(DAYE_SessionBoxProjection &items[])
   {
      return m_store.Export(items);
   }

   void Shutdown(void)
   {
      Comment("");
      if(m_config.delete_owned_objects_on_deinit) DAYE_DeleteOwnedSessionBoxesFromAllCharts();
      m_audit.Close(); m_period_engine.Shutdown(); m_store.Clear();
      ZeroMemory(m_current_summary); ZeroMemory(m_previous_summary);
      m_has_current_summary=false; m_has_previous_summary=false;
      m_last_projection_refresh_utc=0; m_last_source_fingerprint=""; m_initialized=false;
   }
};

#endif
