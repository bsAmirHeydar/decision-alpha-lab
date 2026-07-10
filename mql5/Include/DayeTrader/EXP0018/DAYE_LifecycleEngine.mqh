#ifndef __EXP0018_DAYE_LIFECYCLE_ENGINE_MQH__
#define __EXP0018_DAYE_LIFECYCLE_ENGINE_MQH__

#include <DayeTrader/EXP0018/DAYE_LifecycleSelfTest.mqh>

class CDayeLifecycleEngine
{
private:
   DAYE_LifecycleConfig m_config;
   DAYE_TimeConfig m_time_config;
   CDayeConfirmationEngine m_confirmation_engine;
   CDayeLifecycleStore m_store;
   CDayeLifecycleAuditWriter m_audit;
   DAYE_LifecycleStoreSummary m_previous_summary;
   DAYE_LifecycleStoreSummary m_current_summary;
   bool m_has_previous_summary;
   bool m_has_current_summary;
   bool m_initialized;
   bool m_checkpoint_restored;
   bool m_source_baselined;
   int m_restored_references;
   int m_restored_uses;
   int m_restored_processed;

   bool ValidateConfig(string &reason)
   {
      reason="";
      if(m_config.schema_version!=DAYE_LIFECYCLE_SCHEMA_VERSION) { reason="lifecycle_schema_version_invalid"; return false; }
      if(m_config.maximum_reference_records<1 || m_config.maximum_use_records<1 || m_config.maximum_processed_result_ids<1)
      { reason="lifecycle_store_limits_invalid"; return false; }
      if(!m_config.allow_repeat_across_new_opportunities_while_protected_survives)
      { reason="core_daye_policy_requires_repeat_across_new_opportunities_while_protected_survives"; return false; }
      if(!m_config.suppress_duplicate_exact_opportunity)
      { reason="core_daye_policy_requires_exact_opportunity_deduplication"; return false; }
      if(!m_config.retire_on_protected_touch)
      { reason="core_daye_policy_requires_protected_touch_retirement"; return false; }
      return true;
   }

   void BuildSummary(const DAYE_ConfirmationStoreSummary &source_summary,
                     const int source_result_count,
                     const int source_observation_count,
                     const datetime processing_time_utc,
                     DAYE_LifecycleStoreSummary &summary)
   {
      ZeroMemory(summary); summary.schema_version=DAYE_LIFECYCLE_SCHEMA_VERSION;
      summary.status=source_summary.is_ready?DAYE_LIFECYCLE_STATUS_READY:DAYE_LIFECYCLE_STATUS_SOURCE_NOT_READY;
      summary.reason_code=source_summary.is_ready?"lifecycle_engine_ready":"confirmation_source_not_ready";
      summary.is_ready=source_summary.is_ready; summary.is_replay_safe=source_summary.is_replay_safe;
      summary.checkpoint_restored=m_checkpoint_restored; summary.source_baselined=m_source_baselined;
      summary.processing_time_utc=processing_time_utc; summary.source_result_count=source_result_count;
      summary.source_observation_count=source_observation_count; summary.reference_count=m_store.ReferenceCount();
      summary.processed_result_id_count=m_store.ProcessedResultCount();

      DAYE_ReferenceLifecycleRecord refs[]; m_store.ExportReferences(refs);
      for(int i=0;i<ArraySize(refs);i++)
      {
         summary.latest_reference_id=refs[i].reference_id;
         if(refs[i].is_retired)
         {
            summary.retired_reference_count++; summary.latest_retired_reference_id=refs[i].reference_id;
            if(refs[i].state==DAYE_REF_STATE_RETIRED_PROTECTED_TOUCH) summary.retired_protected_touch_count++;
            if(refs[i].state==DAYE_REF_STATE_RETIRED_DOUBLE_HUNT) summary.retired_double_hunt_count++;
            if(refs[i].state==DAYE_REF_STATE_RETIRED_ROLE_SWITCH) summary.retired_role_switch_count++;
         }
         else summary.surviving_reference_count++;
         if(refs[i].retirement_event_time_utc>summary.event_time_utc) summary.event_time_utc=refs[i].retirement_event_time_utc;
         if(refs[i].latest_use_event_time_utc>summary.event_time_utc) summary.event_time_utc=refs[i].latest_use_event_time_utc;
         if(refs[i].retirement_availability_time_utc>summary.availability_time_utc) summary.availability_time_utc=refs[i].retirement_availability_time_utc;
         if(refs[i].latest_observation_availability_time_utc>summary.availability_time_utc) summary.availability_time_utc=refs[i].latest_observation_availability_time_utc;
      }
      DAYE_ReferenceUseRecord uses[]; m_store.ExportUses(uses);
      for(int i=0;i<ArraySize(uses);i++)
      {
         summary.latest_use_id=uses[i].use_id;
         if(uses[i].status==DAYE_USE_STATUS_ACCEPTED) summary.accepted_use_count++;
         else if(uses[i].status==DAYE_USE_STATUS_DUPLICATE_EXACT_OPPORTUNITY) summary.duplicate_use_count++;
         else summary.rejected_use_count++;
      }
      if(summary.reference_count==0 && source_summary.is_ready)
      {
         summary.status=DAYE_LIFECYCLE_STATUS_NO_CONFIRMED_RESULTS_YET;
         summary.reason_code="no_confirmed_results_have_activated_references";
      }
   }

   void ProcessConfirmedResult(const DAYE_ConfirmationResult &result,
                               const datetime processing_time_utc,
                               DAYE_LifecycleEvent &events[],
                               bool &state_changed)
   {
      if(m_store.IsResultProcessed(result.result_id)) return;
      m_store.RememberProcessedResult(result.result_id,m_config.maximum_processed_result_ids);
      state_changed=true;

      string validation_reason="";
      if(!DAYE_IsValidConfirmedResult(result,validation_reason)) return;

      string a=m_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.canonical_symbol_a;
      string b=m_config.confirmation_config.hunt_config.relationship_config.period_config.data_config.canonical_symbol_b;
      string reference_id=DAYE_BuildReferenceLifecycleId(result.reference_period_instance_id,result.side,a,b);
      string exact_key=DAYE_BuildExactOpportunityUseKey(result);
      int ref_index=m_store.FindReferenceIndex(reference_id);
      DAYE_ReferenceLifecycleRecord ref;
      bool new_reference=false;
      if(ref_index<0)
      {
         string init_reason="";
         if(!DAYE_InitializeReferenceRecord(m_config,result,ref,init_reason)) return;
         if(!m_store.AppendReference(ref,m_config.maximum_reference_records)) return;
         ref_index=m_store.FindReferenceIndex(reference_id); new_reference=true;
         DAYE_AppendLifecycleEvent(events,DAYE_LIFECYCLE_EVENT_REFERENCE_ACTIVATED,reference_id,"",result.result_id,result.observation_id,
                                   result.relationship_id,result.side,DAYE_REF_STATE_UNKNOWN,DAYE_REF_STATE_PROTECTED_SURVIVES,
                                   DAYE_USE_STATUS_UNKNOWN,result.event_time_utc,result.availability_time_utc,processing_time_utc,
                                   "first_confirmed_use_activated_reference");
      }
      if(!m_store.GetReference(ref_index,ref)) return;

      DAYE_ReferenceUseStatus use_status=DAYE_USE_STATUS_ACCEPTED;
      string use_reason="confirmed_use_accepted_while_protected_survives";
      DAYE_LifecycleEventType use_event=DAYE_LIFECYCLE_EVENT_CONFIRMED_USE_ACCEPTED;

      if(ref.is_retired || DAYE_IsReferenceRetiredState(ref.state))
      {
         use_status=DAYE_USE_STATUS_REJECTED_REFERENCE_RETIRED;
         use_reason="confirmed_result_arrived_after_reference_retirement";
         use_event=DAYE_LIFECYCLE_EVENT_RESULT_REJECTED_RETIRED;
         ref.rejected_use_count++;
      }
      else if(ref.protected_canonical_symbol!=result.protected_canonical_symbol)
      {
         DAYE_ReferenceLifecycleState before=ref.state;
         ref.state=DAYE_REF_STATE_RETIRED_ROLE_SWITCH; ref.is_retired=true; ref.is_immutable=true;
         ref.reason_code="role_switch_on_same_reference_retires_reference";
         ref.retirement_event_time_utc=result.event_time_utc; ref.retirement_availability_time_utc=result.availability_time_utc;
         ref.retirement_evidence_id=result.result_id; ref.rejected_use_count++;
         use_status=DAYE_USE_STATUS_REJECTED_ROLE_SWITCH; use_reason=ref.reason_code;
         use_event=DAYE_LIFECYCLE_EVENT_RESULT_REJECTED_ROLE_SWITCH;
         DAYE_AppendLifecycleEvent(events,DAYE_LIFECYCLE_EVENT_REFERENCE_RETIRED_ROLE_SWITCH,reference_id,"",result.result_id,result.observation_id,
                                   result.relationship_id,result.side,before,ref.state,use_status,result.event_time_utc,
                                   result.availability_time_utc,processing_time_utc,ref.reason_code);
      }
      else if(m_config.suppress_duplicate_exact_opportunity && m_store.HasExactOpportunityUse(exact_key))
      {
         use_status=DAYE_USE_STATUS_DUPLICATE_EXACT_OPPORTUNITY;
         use_reason="exact_opportunity_already_has_its_first_confirmed_use";
         use_event=DAYE_LIFECYCLE_EVENT_DUPLICATE_USE_SUPPRESSED;
         ref.duplicate_use_count++;
      }
      else
      {
         ref.accepted_use_count++; ref.latest_confirmation_result_id=result.result_id;
         ref.latest_use_event_time_utc=result.event_time_utc; ref.reason_code="protected_symbol_survives_after_confirmed_use";
      }

      DAYE_ReferenceUseRecord use;
      DAYE_BuildUseRecord(result,reference_id,use_status,use_reason,processing_time_utc,use);
      if(use.is_accepted || m_config.publish_rejected_uses) m_store.AppendUse(use,m_config.maximum_use_records);
      m_store.SetReference(ref_index,ref);
      DAYE_AppendLifecycleEvent(events,use_event,reference_id,use.use_id,result.result_id,result.observation_id,result.relationship_id,
                                result.side,ref.state,ref.state,use_status,result.event_time_utc,result.availability_time_utc,
                                processing_time_utc,use_reason);
      m_audit.WriteUse(use);
   }

public:
   CDayeLifecycleEngine(void)
   {
      ZeroMemory(m_previous_summary); ZeroMemory(m_current_summary);
      m_has_previous_summary=false; m_has_current_summary=false; m_initialized=false;
      m_checkpoint_restored=false; m_source_baselined=false;
      m_restored_references=0; m_restored_uses=0; m_restored_processed=0;
   }

   bool Initialize(const DAYE_LifecycleConfig &config,const DAYE_TimeConfig &time_config,
                   const bool run_self_tests,const bool write_audit,const string audit_filename)
   {
      m_config=config; m_time_config=time_config;
      string reason=""; if(!ValidateConfig(reason)) { Print("EXP0018 P07 invalid config: ",reason); return false; }
      if(run_self_tests)
      {
         string report=""; if(!DAYE_RunLifecycleSelfTests(report)) { Print("EXP0018 P07 self-test failed: ",report); return false; }
         Print(report);
      }
      if(!m_confirmation_engine.Initialize(m_config.confirmation_config,m_time_config,run_self_tests,false,"")) return false;
      if(!m_audit.Open(write_audit,audit_filename)) return false;
      string checkpoint_reason="";
      if(!DAYE_LoadLifecycleCheckpoint(m_config,m_store,m_restored_references,m_restored_uses,m_restored_processed,checkpoint_reason))
      { Print("EXP0018 P07 checkpoint restore failed: ",checkpoint_reason); return false; }
      m_checkpoint_restored=(m_restored_references>0 || m_restored_uses>0 || m_restored_processed>0);
      m_initialized=true; return true;
   }

   bool Process(const datetime current_broker_time,const bool print_summary,const bool print_latest_reference,
                const bool print_events,const bool show_chart_comment,const bool write_summary_rows,
                const int audit_latest_reference_count,const int audit_latest_use_count)
   {
      if(!m_initialized) return false;
      m_confirmation_engine.Process(current_broker_time,false,false,false,false,false,0,0);
      DAYE_ConfirmationStoreSummary confirmation_summary;
      if(!m_confirmation_engine.GetCurrentSummary(confirmation_summary)) return true;
      DAYE_ConfirmationResult results[]; m_confirmation_engine.ExportResults(results);
      DAYE_HuntObservation observations[]; m_confirmation_engine.ExportSourceObservations(observations);

      datetime processing_time_utc=TimeGMT(); if(processing_time_utc<=0) processing_time_utc=current_broker_time;
      DAYE_LifecycleEvent events[]; ArrayResize(events,0); bool state_changed=false;

      for(int i=0;i<ArraySize(results);i++) ProcessConfirmedResult(results[i],processing_time_utc,events,state_changed);

      if(!m_source_baselined)
      {
         m_source_baselined=true; state_changed=true;
         DAYE_AppendLifecycleEvent(events,DAYE_LIFECYCLE_EVENT_SOURCE_BASELINED,"","","","","",DAYE_HUNT_SIDE_UNKNOWN,
                                   DAYE_REF_STATE_UNKNOWN,DAYE_REF_STATE_UNKNOWN,DAYE_USE_STATUS_UNKNOWN,
                                   processing_time_utc,processing_time_utc,processing_time_utc,
                                   "current_hunt_observations_baselined_for_reference_survival_tracking");
      }

      for(int r=0;r<m_store.ReferenceCount();r++)
      {
         DAYE_ReferenceLifecycleRecord ref; if(!m_store.GetReference(r,ref)) continue;
         if(ref.is_retired) continue;
         for(int o=0;o<ArraySize(observations);o++)
         {
            DAYE_ReferenceLifecycleState before; DAYE_LifecycleEventType event_type; string reason="";
            if(!DAYE_ApplyObservationToReference(m_config,observations[o],ref,before,event_type,reason)) continue;
            m_store.SetReference(r,ref); state_changed=true;
            DAYE_AppendLifecycleEvent(events,event_type,ref.reference_id,"","",observations[o].observation_id,
                                      observations[o].relationship_id,ref.side,before,ref.state,DAYE_USE_STATUS_UNKNOWN,
                                      observations[o].event_time_utc,observations[o].availability_time_utc,
                                      processing_time_utc,reason);
            m_audit.WriteReference(ref);
            if(ref.is_retired) break;
         }
      }

      DAYE_LifecycleStoreSummary summary; BuildSummary(confirmation_summary,ArraySize(results),ArraySize(observations),processing_time_utc,summary);
      if(!m_has_previous_summary)
      {
         DAYE_AppendLifecycleEvent(events,DAYE_LIFECYCLE_EVENT_ENGINE_INITIALIZED,"","","","","",DAYE_HUNT_SIDE_UNKNOWN,
                                   DAYE_REF_STATE_UNKNOWN,DAYE_REF_STATE_UNKNOWN,DAYE_USE_STATUS_UNKNOWN,
                                   processing_time_utc,processing_time_utc,processing_time_utc,"lifecycle_engine_initialized");
         if(m_checkpoint_restored)
            DAYE_AppendLifecycleEvent(events,DAYE_LIFECYCLE_EVENT_CHECKPOINT_RESTORED,"","","","","",DAYE_HUNT_SIDE_UNKNOWN,
                                      DAYE_REF_STATE_UNKNOWN,DAYE_REF_STATE_UNKNOWN,DAYE_USE_STATUS_UNKNOWN,
                                      processing_time_utc,processing_time_utc,processing_time_utc,"lifecycle_checkpoint_restored");
      }
      else if(m_previous_summary.status!=summary.status)
      {
         DAYE_AppendLifecycleEvent(events,DAYE_LIFECYCLE_EVENT_STATUS_CHANGED,"","","","","",DAYE_HUNT_SIDE_UNKNOWN,
                                   DAYE_REF_STATE_UNKNOWN,DAYE_REF_STATE_UNKNOWN,DAYE_USE_STATUS_UNKNOWN,
                                   summary.event_time_utc,summary.availability_time_utc,processing_time_utc,summary.reason_code);
      }

      if(state_changed)
      {
         string checkpoint_reason="";
         if(!DAYE_SaveLifecycleCheckpoint(m_config,m_store,checkpoint_reason))
         { summary.status=DAYE_LIFECYCLE_STATUS_CHECKPOINT_ERROR; summary.reason_code=checkpoint_reason; summary.is_ready=false; }
         else if(m_config.persist_checkpoint)
            DAYE_AppendLifecycleEvent(events,DAYE_LIFECYCLE_EVENT_CHECKPOINT_SAVED,"","","","","",DAYE_HUNT_SIDE_UNKNOWN,
                                      DAYE_REF_STATE_UNKNOWN,DAYE_REF_STATE_UNKNOWN,DAYE_USE_STATUS_UNKNOWN,
                                      processing_time_utc,processing_time_utc,processing_time_utc,"lifecycle_checkpoint_saved");
      }

      for(int i=0;i<ArraySize(events);i++) { if(print_events) Print(DAYE_FormatLifecycleEvent(events[i])); m_audit.WriteEvent(events[i]); }
      if(print_summary) Print(DAYE_FormatLifecycleSummary(summary));
      if(print_latest_reference && m_store.ReferenceCount()>0)
      {
         DAYE_ReferenceLifecycleRecord latest; if(m_store.GetReference(m_store.ReferenceCount()-1,latest)) Print("  latest_reference ",DAYE_FormatLifecycleReference(latest));
      }
      if(write_summary_rows) m_audit.WriteSummary(summary);
      DAYE_ReferenceLifecycleRecord refs[]; m_store.ExportReferences(refs);
      int rs=ArraySize(refs)-audit_latest_reference_count; if(rs<0) rs=0;
      for(int i=rs;i<ArraySize(refs);i++) m_audit.WriteReference(refs[i]);
      DAYE_ReferenceUseRecord uses[]; m_store.ExportUses(uses);
      int us=ArraySize(uses)-audit_latest_use_count; if(us<0) us=0;
      for(int i=us;i<ArraySize(uses);i++) m_audit.WriteUse(uses[i]);
      m_audit.Flush();

      if(show_chart_comment) Comment(DAYE_FormatLifecycleSummary(summary)+"\nReference lifecycle only — no drawing, direction, risk, or trading.");
      else Comment("");
      m_previous_summary=summary; m_current_summary=summary; m_has_previous_summary=true; m_has_current_summary=true;
      return true;
   }

   bool GetCurrentSummary(DAYE_LifecycleStoreSummary &summary)
   { if(!m_has_current_summary) return false; summary=m_current_summary; return true; }
   int ExportReferences(DAYE_ReferenceLifecycleRecord &items[]) { return m_store.ExportReferences(items); }
   int ExportUses(DAYE_ReferenceUseRecord &items[]) { return m_store.ExportUses(items); }

   // P08 read-only period provenance. P07 still owns lifecycle only.
   int ExportSourcePeriods(DAYE_PairedPeriodSnapshot &items[])
   {
      return m_confirmation_engine.ExportSourcePeriods(items);
   }

   void Shutdown(void)
   {
      string reason=""; DAYE_SaveLifecycleCheckpoint(m_config,m_store,reason);
      Comment(""); m_audit.Close(); m_store.Clear(); m_confirmation_engine.Shutdown();
      ZeroMemory(m_previous_summary); ZeroMemory(m_current_summary);
      m_has_previous_summary=false; m_has_current_summary=false; m_initialized=false;
      m_checkpoint_restored=false; m_source_baselined=false;
   }
};

#endif
