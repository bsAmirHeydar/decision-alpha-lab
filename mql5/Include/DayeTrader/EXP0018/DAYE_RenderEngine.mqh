#ifndef __EXP0018_DAYE_RENDER_ENGINE_MQH__
#define __EXP0018_DAYE_RENDER_ENGINE_MQH__

#include <DayeTrader/EXP0018/DAYE_RenderSelfTest.mqh>

class CDayeRenderEngine
{
private:
   DAYE_RenderConfig m_config;
   DAYE_TimeConfig m_time_config;
   CDayeLifecycleEngine m_lifecycle_engine;
   CDayeRenderStore m_store;
   CDayeRenderAuditWriter m_audit;
   DAYE_RenderStoreSummary m_previous_summary;
   DAYE_RenderStoreSummary m_current_summary;
   bool m_has_previous_summary;
   bool m_has_current_summary;
   bool m_initialized;

   bool ValidateConfig(string &reason)
   {
      reason="";
      if(m_config.schema_version!=DAYE_RENDER_SCHEMA_VERSION) { reason="render_schema_version_invalid"; return false; }
      if(m_config.line_width<1 || m_config.line_width>5) { reason="line_width_out_of_range"; return false; }
      if(m_config.label_font_size<6 || m_config.label_font_size>40) { reason="label_font_size_out_of_range"; return false; }
      if(m_config.maximum_projection_records<1 || m_config.maximum_target_charts_per_use<1)
      { reason="render_store_limits_invalid"; return false; }
      if(m_config.open_missing_hunter_chart && m_config.target_policy==DAYE_RENDER_TARGET_CURRENT_CHART_IF_HUNTER)
      { reason="current_chart_only_policy_cannot_open_missing_hunter_chart"; return false; }
      if(!m_config.preserve_orphaned_owned_objects)
      { reason="core_historical_persistence_requires_preserve_orphaned_owned_objects"; return false; }
      return true;
   }

   void BuildProjectionBase(const DAYE_ReferenceUseRecord &use,const long chart_id,
                            const DAYE_RenderGeometry &geometry,const datetime processing_time_utc,
                            DAYE_RenderProjection &projection)
   {
      ZeroMemory(projection);
      projection.schema_version=DAYE_RENDER_SCHEMA_VERSION;
      projection.projection_id=DAYE_BuildRenderProjectionId(use.use_id,chart_id);
      projection.use_id=use.use_id; projection.reference_id=use.reference_id;
      projection.relationship_id=use.relationship_id; projection.source_alias=use.source_alias;
      projection.chart_label=use.chart_label; projection.side=use.side;
      projection.is_major=use.is_major; projection.is_historical_immutable=use.is_historical_immutable;
      projection.is_replay_safe=use.is_replay_safe;
      projection.hunter_broker_symbol=use.hunter_broker_symbol;
      projection.hunter_canonical_symbol=use.hunter_canonical_symbol;
      projection.protected_canonical_symbol=use.protected_canonical_symbol;
      projection.target_chart_id=chart_id;
      projection.target_chart_timeframe=(chart_id>0)?ChartPeriod(chart_id):PERIOD_CURRENT;
      projection.line_object_name=DAYE_BuildRenderLineName(use.use_id);
      projection.text_object_name=DAYE_BuildRenderTextName(use.use_id);
      projection.geometry=geometry;
      projection.event_time_utc=use.event_time_utc;
      projection.availability_time_utc=use.availability_time_utc;
      projection.processing_time_utc=processing_time_utc;
   }

   void Summarize(const DAYE_LifecycleStoreSummary &source_summary,
                  const DAYE_ReferenceUseRecord &uses[],const DAYE_PairedPeriodSnapshot &periods[],
                  const datetime processing_time_utc,DAYE_RenderStoreSummary &summary)
   {
      ZeroMemory(summary); summary.schema_version=DAYE_RENDER_SCHEMA_VERSION;
      summary.processing_time_utc=processing_time_utc;
      summary.source_use_count=ArraySize(uses); summary.source_period_count=ArraySize(periods);
      summary.is_replay_safe=source_summary.is_replay_safe;
      for(int i=0;i<ArraySize(uses);i++)
      {
         if(uses[i].is_accepted) summary.accepted_source_use_count++;
         if(uses[i].event_time_utc>summary.event_time_utc) summary.event_time_utc=uses[i].event_time_utc;
         if(uses[i].availability_time_utc>summary.availability_time_utc) summary.availability_time_utc=uses[i].availability_time_utc;
         if(uses[i].is_accepted) summary.latest_use_id=uses[i].use_id;
         summary.open_hunter_chart_count+=DAYE_CountOpenHunterCharts(uses[i].hunter_broker_symbol);
      }
      DAYE_RenderProjection items[]; m_store.Export(items); summary.projection_count=ArraySize(items);
      for(int i=0;i<ArraySize(items);i++)
      {
         summary.latest_projection_id=items[i].projection_id; summary.latest_object_name=items[i].line_object_name;
         if(items[i].status==DAYE_RENDER_STATUS_CREATED) summary.created_count++;
         if(items[i].status==DAYE_RENDER_STATUS_VERIFIED) summary.verified_count++;
         if(items[i].status==DAYE_RENDER_STATUS_REPAIRED) summary.repaired_count++;
         if(items[i].status==DAYE_RENDER_STATUS_WAITING_FOR_HUNTER_CHART) summary.waiting_chart_count++;
         if(items[i].status==DAYE_RENDER_STATUS_SOURCE_PERIOD_NOT_FOUND) summary.source_period_missing_count++;
         if(items[i].status==DAYE_RENDER_STATUS_SOURCE_EXTREME_UNAVAILABLE) summary.source_extreme_missing_count++;
         if(items[i].status==DAYE_RENDER_STATUS_OBJECT_CREATE_FAILED || items[i].status==DAYE_RENDER_STATUS_OBJECT_UPDATE_FAILED) summary.failed_object_count++;
         if(items[i].is_major && items[i].is_drawn) summary.major_label_count++;
         if(!items[i].is_major && items[i].is_drawn) summary.minor_unlabeled_count++;
      }

      if(!source_summary.is_ready)
      { summary.status=DAYE_RENDER_ENGINE_SOURCE_NOT_READY; summary.reason_code="lifecycle_source_not_ready"; summary.is_ready=false; }
      else if(summary.accepted_source_use_count==0)
      { summary.status=DAYE_RENDER_ENGINE_NO_ACCEPTED_USES; summary.reason_code="no_accepted_lifecycle_uses_to_draw"; summary.is_ready=true; }
      else if(summary.waiting_chart_count>0 && summary.created_count+summary.verified_count+summary.repaired_count==0)
      { summary.status=DAYE_RENDER_ENGINE_WAITING_FOR_CHART; summary.reason_code="accepted_uses_waiting_for_open_hunter_chart"; summary.is_ready=true; }
      else if(summary.source_period_missing_count>0 || summary.source_extreme_missing_count>0 || summary.failed_object_count>0)
      { summary.status=DAYE_RENDER_ENGINE_DEGRADED; summary.reason_code="one_or_more_visual_projections_degraded"; summary.is_ready=true; }
      else
      { summary.status=DAYE_RENDER_ENGINE_READY; summary.reason_code="accepted_lifecycle_uses_projected_idempotently"; summary.is_ready=true; }
   }

public:
   CDayeRenderEngine(void)
   {
      ZeroMemory(m_previous_summary); ZeroMemory(m_current_summary);
      m_has_previous_summary=false; m_has_current_summary=false; m_initialized=false;
   }

   bool Initialize(const DAYE_RenderConfig &config,const DAYE_TimeConfig &time_config,
                   const bool run_self_tests,const bool write_audit,const string audit_filename)
   {
      m_config=config; m_time_config=time_config;
      string reason="";
      if(!ValidateConfig(reason)) { Print("EXP0018 P08 invalid render config reason=",reason); return false; }
      if(run_self_tests && !DAYE_RunEmbeddedRenderSelfTests())
      { Print("EXP0018 P08 embedded self-tests failed."); return false; }
      if(!m_lifecycle_engine.Initialize(config.lifecycle_config,time_config,run_self_tests,false,""))
      { Print("EXP0018 P08 could not initialize P07 lifecycle dependency."); return false; }
      if(!m_audit.Open(audit_filename,write_audit))
      { m_lifecycle_engine.Shutdown(); return false; }
      m_initialized=true;
      Print("EXP0018 P08 Divergence Drawing v2 initialized. Drawing projection only; no detection, direction, risk, or execution authority.");
      return true;
   }

   bool Process(const datetime current_broker_time,const bool print_summary,const bool print_latest,
                const bool print_events,const bool show_chart_comment,const bool write_summary_rows,
                const int audit_latest_projection_count)
   {
      if(!m_initialized) return false;
      m_lifecycle_engine.Process(current_broker_time,false,false,false,false,false,0,0);
      DAYE_LifecycleStoreSummary source_summary;
      if(!m_lifecycle_engine.GetCurrentSummary(source_summary)) return true;

      DAYE_ReferenceUseRecord uses[]; m_lifecycle_engine.ExportUses(uses);
      DAYE_PairedPeriodSnapshot periods[]; m_lifecycle_engine.ExportSourcePeriods(periods);
      datetime processing_time_utc=TimeGMT(); if(processing_time_utc<=0) processing_time_utc=current_broker_time;
      DAYE_RenderEvent events[];

      ENUM_TIMEFRAMES host_tf=m_config.lifecycle_config.confirmation_config.host_timeframe;
      if(host_tf==PERIOD_CURRENT) host_tf=(ENUM_TIMEFRAMES)_Period;

      for(int i=0;i<ArraySize(uses);i++)
      {
         if(!uses[i].is_accepted || uses[i].status!=DAYE_USE_STATUS_ACCEPTED) continue;
         DAYE_RenderGeometry geometry;
         bool geometry_ok=DAYE_BuildRenderGeometry(uses[i],periods,m_config,m_time_config,geometry);
         if(!geometry_ok)
         {
            DAYE_RenderProjection degraded; BuildProjectionBase(uses[i],0,geometry,processing_time_utc,degraded);
            DAYE_RenderProjectionStatus old_status=DAYE_RENDER_STATUS_UNKNOWN;
            int old_index=m_store.Find(degraded.projection_id); DAYE_RenderProjection old;
            if(old_index>=0 && m_store.Get(old_index,old)) old_status=old.status;
            if(geometry.reason_code=="reference_period_not_present_in_current_source_lookback")
               degraded.status=DAYE_RENDER_STATUS_SOURCE_PERIOD_NOT_FOUND;
            else if(StringFind(geometry.reason_code,"extreme")>=0)
               degraded.status=DAYE_RENDER_STATUS_SOURCE_EXTREME_UNAVAILABLE;
            else degraded.status=DAYE_RENDER_STATUS_INVALID_GEOMETRY;
            degraded.reason_code=geometry.reason_code;
            m_store.Upsert(degraded,m_config.maximum_projection_records);
            DAYE_RenderEventType degraded_event=DAYE_RenderEventTypeForStatus(degraded.status,false);
            if(degraded_event!=DAYE_RENDER_EVENT_NONE && old_status!=degraded.status)
               DAYE_AppendRenderEvent(events,degraded_event,degraded,old_status,processing_time_utc,degraded.reason_code);
            m_audit.WriteProjection(degraded);
            continue;
         }

         long chart_ids[];
         int chart_count=DAYE_ResolveHunterTargetCharts(uses[i],m_config,host_tf,chart_ids);
         if(chart_count==0)
         {
            DAYE_RenderProjection pending; BuildProjectionBase(uses[i],0,geometry,processing_time_utc,pending);
            DAYE_RenderProjectionStatus old_status=DAYE_RENDER_STATUS_UNKNOWN;
            int old_index=m_store.Find(pending.projection_id); DAYE_RenderProjection old;
            if(old_index>=0 && m_store.Get(old_index,old)) old_status=old.status;
            pending.status=DAYE_RENDER_STATUS_WAITING_FOR_HUNTER_CHART;
            pending.reason_code="no_open_chart_matches_hunter_symbol_and_target_policy";
            m_store.Upsert(pending,m_config.maximum_projection_records);
            if(old_status!=pending.status)
               DAYE_AppendRenderEvent(events,DAYE_RENDER_EVENT_WAITING_FOR_HUNTER_CHART,pending,old_status,processing_time_utc,pending.reason_code);
            continue;
         }

         m_store.Remove(DAYE_BuildRenderProjectionId(uses[i].use_id,0));
         for(int c=0;c<chart_count;c++)
         {
            DAYE_RenderProjection projection; BuildProjectionBase(uses[i],chart_ids[c],geometry,processing_time_utc,projection);
            DAYE_RenderProjectionStatus old_status=DAYE_RENDER_STATUS_UNKNOWN;
            int old_index=m_store.Find(projection.projection_id); DAYE_RenderProjection old;
            if(old_index>=0 && m_store.Get(old_index,old))
            {
               old_status=old.status;
               projection.create_count=old.create_count;
               projection.verify_count=old.verify_count;
               projection.repair_count=old.repair_count;
            }

            bool manual_delete_repaired=false;
            string object_reason="";
            bool previously_recorded_as_drawn=(old_index>=0 && old.is_drawn);
            projection.status=DAYE_ProjectAcceptedUseToChart(uses[i],chart_ids[c],geometry,m_config,previously_recorded_as_drawn,object_reason,manual_delete_repaired);
            projection.reason_code=object_reason;
            projection.is_drawn=(projection.status==DAYE_RENDER_STATUS_CREATED || projection.status==DAYE_RENDER_STATUS_VERIFIED || projection.status==DAYE_RENDER_STATUS_REPAIRED);
            if(projection.status==DAYE_RENDER_STATUS_CREATED) projection.create_count++;
            if(projection.status==DAYE_RENDER_STATUS_VERIFIED) projection.verify_count++;
            if(projection.status==DAYE_RENDER_STATUS_REPAIRED) projection.repair_count++;
            if(!m_store.Upsert(projection,m_config.maximum_projection_records))
            { projection.status=DAYE_RENDER_STATUS_STORE_CAPACITY_EXCEEDED; projection.reason_code="projection_store_capacity_exceeded"; }
            DAYE_RenderEventType event_type=DAYE_RenderEventTypeForStatus(projection.status,manual_delete_repaired);
            if(event_type!=DAYE_RENDER_EVENT_NONE && (old_status!=projection.status || projection.status==DAYE_RENDER_STATUS_REPAIRED || manual_delete_repaired))
               DAYE_AppendRenderEvent(events,event_type,projection,old_status,processing_time_utc,projection.reason_code);
            m_audit.WriteProjection(projection);
         }
      }

      DAYE_RenderStoreSummary summary; Summarize(source_summary,uses,periods,processing_time_utc,summary);
      if(!m_has_previous_summary)
      {
         DAYE_RenderProjection engine_projection; ZeroMemory(engine_projection);
         engine_projection.projection_id="EXP0018|P08|ENGINE";
         engine_projection.event_time_utc=processing_time_utc; engine_projection.availability_time_utc=processing_time_utc;
         DAYE_AppendRenderEvent(events,DAYE_RENDER_EVENT_ENGINE_INITIALIZED,engine_projection,DAYE_RENDER_STATUS_UNKNOWN,processing_time_utc,"render_engine_initialized");
      }
      for(int i=0;i<ArraySize(events);i++) { if(print_events) Print(DAYE_FormatRenderEvent(events[i])); m_audit.WriteEvent(events[i]); }
      if(print_summary) Print(DAYE_FormatRenderSummary(summary));
      if(print_latest && m_store.Count()>0)
      {
         DAYE_RenderProjection latest; if(m_store.Get(m_store.Count()-1,latest)) Print("  latest_projection ",DAYE_FormatRenderProjection(latest));
      }
      if(write_summary_rows) m_audit.WriteSummary(summary);
      if(audit_latest_projection_count>0)
      {
         DAYE_RenderProjection projections[]; m_store.Export(projections);
         int start=ArraySize(projections)-audit_latest_projection_count; if(start<0) start=0;
         for(int i=start;i<ArraySize(projections);i++) m_audit.WriteProjection(projections[i]);
      }
      m_audit.Flush();

      if(show_chart_comment) Comment(DAYE_FormatRenderSummary(summary)+"\nDrawing projection only — no trade direction, risk, or execution.");
      else Comment("");
      m_previous_summary=summary; m_current_summary=summary; m_has_previous_summary=true; m_has_current_summary=true;
      return true;
   }

   bool GetCurrentSummary(DAYE_RenderStoreSummary &summary)
   { if(!m_has_current_summary) return false; summary=m_current_summary; return true; }
   int ExportProjections(DAYE_RenderProjection &items[]) { return m_store.Export(items); }

   // P10 read-only source surfaces. These methods do not transfer mutation
   // authority to the visual layer; they expose immutable snapshots already
   // produced by P03 and accepted-use history already produced by P07.
   int ExportSourcePeriods(DAYE_PairedPeriodSnapshot &items[])
   { return m_lifecycle_engine.ExportSourcePeriods(items); }

   int ExportAcceptedUses(DAYE_ReferenceUseRecord &items[])
   { return m_lifecycle_engine.ExportUses(items); }

   void Shutdown(void)
   {
      if(m_config.delete_owned_objects_on_deinit) DAYE_DeleteOwnedObjectsFromAllCharts();
      Comment(""); m_audit.Close(); m_store.Clear(); m_lifecycle_engine.Shutdown();
      ZeroMemory(m_previous_summary); ZeroMemory(m_current_summary);
      m_has_previous_summary=false; m_has_current_summary=false; m_initialized=false;
   }
};

#endif
