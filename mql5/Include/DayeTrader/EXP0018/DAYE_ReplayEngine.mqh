#ifndef __EXP0018_DAYE_REPLAY_ENGINE_MQH__
#define __EXP0018_DAYE_REPLAY_ENGINE_MQH__

#include <DayeTrader/EXP0018/DAYE_ReplaySelfTest.mqh>

class CDayeHistoricalReplayEngine
{
private:
   DAYE_ReplayConfig m_config;
   DAYE_TimeConfig m_time_config;
   DAYE_ReplaySource m_source;
   DAYE_ReplaySummary m_summary;
   DAYE_PeriodDefinition m_period_registry[];
   DAYE_RelationshipDefinition m_relationship_registry[];
   DAYE_HuntObservation m_previous_observations[];
   CDayeConfirmationStore m_confirmation_store;
   CDayeLifecycleStore m_lifecycle_store;
   CDayeReplayAuditWriter m_audit;
   int m_cursor;
   bool m_initialized;
   bool m_finished;

   void Emit(const DAYE_ReplayEventType type,const string subject,const string relationship,const DAYE_HuntSide side,
             const datetime event_time,const datetime availability,const string reason)
   {
      DAYE_ReplayEvent e; ZeroMemory(e); e.schema_version=DAYE_REPLAY_SCHEMA_VERSION; e.event_type=type;
      e.subject_id=subject; e.relationship_id=relationship; e.side=side; e.event_time_utc=event_time;
      e.availability_time_utc=availability; e.processing_time_utc=TimeGMT(); if(e.processing_time_utc<=0) e.processing_time_utc=availability;
      e.reason_code=reason; e.state_hash=m_summary.final_state_hash;
      e.event_id=DAYE_BuildReplayEventId(m_summary.run_id,type,subject,event_time);
      if(m_config.write_event_rows) m_audit.WriteEvent(e);
   }

   void RecountLifecycle(void)
   {
      DAYE_ReferenceLifecycleRecord refs[]; m_lifecycle_store.ExportReferences(refs);
      DAYE_ReferenceUseRecord uses[]; m_lifecycle_store.ExportUses(uses);
      m_summary.reference_count=ArraySize(refs); m_summary.surviving_reference_count=0; m_summary.retired_reference_count=0;
      m_summary.accepted_use_count=0; m_summary.duplicate_use_count=0; m_summary.rejected_use_count=0;
      string lifecycle_hash="00000000";
      for(int i=0;i<ArraySize(refs);i++)
      {
         if(refs[i].is_retired) m_summary.retired_reference_count++; else m_summary.surviving_reference_count++;
         lifecycle_hash=DAYE_ReplayAppendHash(lifecycle_hash,DAYE_ReplayCanonicalReference(refs[i]));
      }
      for(int i=0;i<ArraySize(uses);i++)
      {
         if(uses[i].status==DAYE_USE_STATUS_ACCEPTED) m_summary.accepted_use_count++;
         else if(uses[i].status==DAYE_USE_STATUS_DUPLICATE_EXACT_OPPORTUNITY) m_summary.duplicate_use_count++;
         else m_summary.rejected_use_count++;
         lifecycle_hash=DAYE_ReplayAppendHash(lifecycle_hash,DAYE_ReplayCanonicalUse(uses[i]));
      }
      m_summary.lifecycle_hash=lifecycle_hash;
      m_summary.final_state_hash=DAYE_ReplayAppendHash(m_summary.confirmation_hash,m_summary.lifecycle_hash);
   }

   void ProcessObservationTransitions(const DAYE_HuntObservation &observations[],const datetime cursor_time)
   {
      DAYE_ConfirmationConfig confirmation_config=m_config.lifecycle_config.confirmation_config;
      ENUM_TIMEFRAMES host=DAYE_ResolveHostTimeframe(confirmation_config.host_timeframe);
      for(int i=0;i<ArraySize(observations);i++)
      {
         DAYE_HuntObservation obs=observations[i];
         if(obs.status!=DAYE_HUNT_STATUS_READY || !obs.is_publishable) continue;
         DAYE_HuntObservation previous; bool had_previous=DAYE_FindReplayObservation(m_previous_observations,obs.observation_id,previous);
         bool changed=!had_previous || previous.pair_state!=obs.pair_state || previous.availability_time_utc!=obs.availability_time_utc;
         int candidate_index=m_confirmation_store.FindCandidateIndexByObservationId(obs.observation_id);
         if(candidate_index>=0 && changed)
         {
            DAYE_ConfirmationCandidate candidate; if(m_confirmation_store.GetCandidate(candidate_index,candidate))
            {
               bool candidate_changed=false; DAYE_UpdateConfirmationCandidate(obs,candidate,candidate_changed);
               m_confirmation_store.SetCandidate(candidate_index,candidate);
               if(candidate_changed)
               {
                  m_summary.candidate_updated_count++;
                  Emit(DAYE_REPLAY_EVENT_CANDIDATE_UPDATED,candidate.candidate_id,candidate.relationship_id,candidate.side,
                       obs.event_time_utc,obs.availability_time_utc,"candidate_updated_from_as_of_observation");
               }
            }
         }
         bool transitioned_to_one_sided=obs.is_one_sided && (!had_previous || !previous.is_one_sided);
         if(transitioned_to_one_sided && candidate_index<0 && !m_confirmation_store.IsObservationFinalized(obs.observation_id))
         {
            datetime open_utc=0,close_utc=0; string reason="";
            if(DAYE_ResolveReplayHostWindow(obs.availability_time_utc,host,m_time_config,open_utc,close_utc,reason))
            {
               DAYE_HostBarPair target; ZeroMemory(target); target.schema_version=DAYE_CONFIRMATION_SCHEMA_VERSION;
               target.is_ready=true; target.is_replay_safe=true; target.timeframe=host; target.timeframe_seconds=PeriodSeconds(host);
               target.open_time_utc=open_utc; target.close_time_utc=close_utc;
               target.host_bar_id=DAYE_BuildHostBarId(host,open_utc,
                  confirmation_config.hunt_config.relationship_config.period_config.data_config.canonical_symbol_a,
                  confirmation_config.hunt_config.relationship_config.period_config.data_config.canonical_symbol_b);
               DAYE_ConfirmationCandidate candidate;
               if(DAYE_InitializeConfirmationCandidate(obs,target,candidate,reason) &&
                  m_confirmation_store.AppendCandidate(candidate,confirmation_config.maximum_pending_candidates))
               {
                  m_summary.one_sided_transition_count++; m_summary.candidate_opened_count++;
                  Emit(DAYE_REPLAY_EVENT_CANDIDATE_OPENED,candidate.candidate_id,candidate.relationship_id,candidate.side,
                       obs.event_time_utc,obs.availability_time_utc,"first_replay_one_sided_transition_opened_candidate");
               }
            }
         }
      }
      ArrayResize(m_previous_observations,ArraySize(observations));
      for(int i=0;i<ArraySize(observations);i++) m_previous_observations[i]=observations[i];
   }

   void FinalizeDueCandidates(const DAYE_HuntObservation &observations[],const int prefix_count,const datetime cursor_time)
   {
      DAYE_ConfirmationConfig confirmation_config=m_config.lifecycle_config.confirmation_config;
      for(int i=m_confirmation_store.CandidateCount()-1;i>=0;i--)
      {
         DAYE_ConfirmationCandidate candidate; if(!m_confirmation_store.GetCandidate(i,candidate)) continue;
         if(candidate.target_host_close_utc>cursor_time) continue;
         DAYE_HostBarPair host; string reason="";
         bool host_ok=DAYE_BuildReplayHostBarPair(m_source.pairs,candidate.target_host_open_utc,candidate.target_host_close_utc,
                                                  confirmation_config,m_time_config,host,reason);
         if(!host_ok)
         {
            ZeroMemory(host); host.schema_version=DAYE_CONFIRMATION_SCHEMA_VERSION; host.is_ready=false;
            host.open_time_utc=candidate.target_host_open_utc; host.close_time_utc=candidate.target_host_close_utc;
            host.host_bar_id=candidate.target_host_bar_id;
         }
         DAYE_ConfirmationResult result;
         bool close_missed=(candidate.target_host_close_utc<cursor_time);
         DAYE_FinalizeCandidateAtClose(candidate,host,cursor_time,close_missed,result);
         if(!host_ok && result.outcome==DAYE_CONFIRM_OUTCOME_UNKNOWN)
         { result.outcome=DAYE_CONFIRM_OUTCOME_UNAVAILABLE_AT_CLOSE; result.reason_code=reason; }
         m_confirmation_store.AppendResult(result,confirmation_config.maximum_results_to_publish);
         m_confirmation_store.RememberFinalizedObservation(candidate.observation_id,confirmation_config.maximum_finalized_ids_to_remember);
         m_confirmation_store.RemoveCandidateByObservationId(candidate.observation_id);
         m_summary.confirmation_result_count++;
         if(result.outcome==DAYE_CONFIRM_OUTCOME_CONFIRMED) m_summary.confirmed_count++;
         else if(result.outcome==DAYE_CONFIRM_OUTCOME_INVALIDATED_DOUBLE_HUNT) m_summary.double_hunt_invalidated_count++;
         else if(result.outcome==DAYE_CONFIRM_OUTCOME_NO_SIGNAL_AT_CLOSE) m_summary.no_signal_count++;
         else if(result.outcome==DAYE_CONFIRM_OUTCOME_INVALIDATED_ROLE_CHANGED) m_summary.role_changed_count++;
         else m_summary.unavailable_count++;
         m_summary.confirmation_hash=DAYE_ReplayAppendHash(m_summary.confirmation_hash,DAYE_ReplayCanonicalConfirmation(result));
         if(m_config.write_confirmation_rows) m_audit.WriteConfirmation(result);
         Emit(DAYE_REPLAY_EVENT_CONFIRMATION_FINALIZED,result.result_id,result.relationship_id,result.side,
              result.event_time_utc,result.availability_time_utc,result.reason_code);

         if(result.is_confirmed)
         {
            DAYE_ReferenceUseRecord use; bool activated=false,retired=false; string lifecycle_reason="";
            if(DAYE_ReplayApplyConfirmedResult(m_config.lifecycle_config,result,cursor_time,m_lifecycle_store,use,activated,retired,lifecycle_reason))
            {
               if(activated) Emit(DAYE_REPLAY_EVENT_REFERENCE_ACTIVATED,use.reference_id,result.relationship_id,result.side,
                                  result.event_time_utc,result.availability_time_utc,"first_confirmed_use_activated_reference");
               if(use.use_id!="")
               {
                  if(m_config.write_use_rows) m_audit.WriteUse(use);
                  Emit(use.is_accepted?DAYE_REPLAY_EVENT_USE_ACCEPTED:DAYE_REPLAY_EVENT_USE_REJECTED,use.use_id,
                       use.relationship_id,use.side,use.event_time_utc,use.availability_time_utc,use.reason_code);
               }
               if(retired) Emit(DAYE_REPLAY_EVENT_REFERENCE_RETIRED,use.reference_id,result.relationship_id,result.side,
                                result.event_time_utc,result.availability_time_utc,"reference_retired_during_result_admission");
            }
         }
      }

      DAYE_ReferenceLifecycleRecord retired[];
      DAYE_ReplayApplyObservationsToReferences(m_config.lifecycle_config,observations,m_lifecycle_store,cursor_time,retired);
      for(int i=0;i<ArraySize(retired);i++)
      {
         if(m_config.write_reference_rows) m_audit.WriteReference(retired[i]);
         Emit(DAYE_REPLAY_EVENT_REFERENCE_RETIRED,retired[i].reference_id,"",retired[i].side,
              retired[i].retirement_event_time_utc,retired[i].retirement_availability_time_utc,retired[i].reason_code);
      }
      RecountLifecycle();
   }

   bool ProcessOneCursor(const int cursor_index,string &reason)
   {
      reason=""; int prefix_count=cursor_index+1;
      DAYE_PairedPeriodSnapshot periods[]; DAYE_RelationshipResolution resolutions[]; DAYE_HuntObservation observations[];
      if(!DAYE_BuildReplayPipelineFrame(m_config,m_time_config,m_period_registry,m_relationship_registry,
                                        m_source.pairs,prefix_count,periods,resolutions,observations,reason)) return false;
      datetime cursor_time=m_source.pairs[cursor_index].availability_time_utc;
      m_summary.maximum_period_count=MathMax(m_summary.maximum_period_count,ArraySize(periods));
      m_summary.resolution_evaluation_count+=ArraySize(resolutions);
      m_summary.observation_evaluation_count+=ArraySize(observations);
      ProcessObservationTransitions(observations,cursor_time);
      FinalizeDueCandidates(observations,prefix_count,cursor_time);

      DAYE_ReplayFrame frame; ZeroMemory(frame); frame.schema_version=DAYE_REPLAY_SCHEMA_VERSION; frame.cursor_index=cursor_index;
      frame.event_time_utc=m_source.pairs[cursor_index].event_time_utc; frame.availability_time_utc=cursor_time;
      frame.period_count=ArraySize(periods);
      for(int i=0;i<ArraySize(resolutions);i++) if(resolutions[i].status==DAYE_REL_RESOLUTION_READY) frame.ready_resolution_count++;
      for(int i=0;i<ArraySize(observations);i++)
      {
         if(observations[i].status==DAYE_HUNT_STATUS_READY) frame.ready_observation_count++;
         if(observations[i].is_one_sided) frame.one_sided_count++;
      }
      frame.pending_candidate_count=m_confirmation_store.CandidateCount(); frame.result_count=m_confirmation_store.ResultCount();
      frame.reference_count=m_lifecycle_store.ReferenceCount();
      DAYE_ReferenceUseRecord uses[]; m_lifecycle_store.ExportUses(uses);
      for(int i=0;i<ArraySize(uses);i++) if(uses[i].is_accepted) frame.accepted_use_count++;
      frame.frame_hash=DAYE_ReplayHashText(IntegerToString(cursor_index)+"|"+IntegerToString(frame.period_count)+"|"+
                                           IntegerToString(frame.ready_observation_count)+"|"+m_summary.final_state_hash);
      if(m_config.write_frame_rows && m_config.frame_audit_stride>0 && (cursor_index%m_config.frame_audit_stride)==0) m_audit.WriteFrame(frame);
      m_summary.processed_cursor_count++;
      return true;
   }

   void Finish(void)
   {
      m_summary.status=DAYE_REPLAY_STATUS_COMPLETE; m_summary.reason_code="chronological_replay_complete";
      m_summary.is_ready=true; m_summary.is_complete=true; m_summary.processing_completed_utc=TimeGMT();
      if(m_summary.processing_completed_utc<=0) m_summary.processing_completed_utc=m_summary.end_utc;
      DAYE_ReferenceLifecycleRecord refs[]; m_lifecycle_store.ExportReferences(refs);
      DAYE_ReferenceUseRecord uses[]; m_lifecycle_store.ExportUses(uses);
      if(m_config.write_reference_rows) for(int i=0;i<ArraySize(refs);i++) m_audit.WriteReference(refs[i]);
      if(m_config.write_use_rows) for(int i=0;i<ArraySize(uses);i++) m_audit.WriteUse(uses[i]);
      m_audit.WriteSummary(m_summary); m_audit.Flush();
      Emit(DAYE_REPLAY_EVENT_RUN_COMPLETED,m_summary.run_id,"",DAYE_HUNT_SIDE_UNKNOWN,m_summary.end_utc,m_summary.end_utc,"chronological_replay_complete");
      m_audit.Flush(); m_finished=true;
   }

public:
   CDayeHistoricalReplayEngine(void) { m_cursor=0; m_initialized=false; m_finished=false; ZeroMemory(m_summary); }

   bool Initialize(const DAYE_ReplayConfig &config,const DAYE_TimeConfig &time_config,const bool run_self_tests)
   {
      m_config=config; m_time_config=time_config; string reason="";
      if(!DAYE_ValidateReplayConfig(config,time_config,reason))
      { m_summary.status=DAYE_REPLAY_STATUS_INVALID_CONFIG; m_summary.reason_code=reason; return false; }
      if(run_self_tests)
      {
         string report=""; if(!DAYE_RunReplaySelfTests(report)) { Print(report); return false; } Print(report);
      }
      DAYE_BuildCanonicalPeriodRegistry(m_period_registry);
      DAYE_BuildCanonicalRelationshipRegistry(m_relationship_registry);
      m_summary.schema_version=DAYE_REPLAY_SCHEMA_VERSION; m_summary.status=DAYE_REPLAY_STATUS_LOADING;
      m_summary.processing_started_utc=TimeGMT();
      if(!DAYE_LoadReplaySource(config,time_config,m_source))
      { m_summary.status=DAYE_REPLAY_STATUS_SOURCE_UNAVAILABLE; m_summary.reason_code=m_source.reason_code; return false; }
      m_summary.start_utc=m_source.start_utc; m_summary.end_utc=m_source.end_utc; m_summary.source_pair_count=m_source.aligned_count;
      m_summary.cursor_count=m_source.aligned_count; m_summary.source_unmatched_a=m_source.unmatched_a; m_summary.source_unmatched_b=m_source.unmatched_b;
      m_summary.is_replay_safe=m_source.is_replay_safe; m_summary.is_deterministic=true;
      m_summary.run_id=DAYE_BuildReplayRunId(config,m_source.start_utc,m_source.end_utc);
      m_summary.source_hash="00000000"; m_summary.confirmation_hash="00000000"; m_summary.lifecycle_hash="00000000"; m_summary.final_state_hash="00000000";
      for(int i=0;i<ArraySize(m_source.pairs);i++) m_summary.source_hash=DAYE_ReplayAppendHash(m_summary.source_hash,m_source.pairs[i].pair_id);
      if(!m_audit.Open(config)) { m_summary.status=DAYE_REPLAY_STATUS_IO_ERROR; m_summary.reason_code="replay_audit_open_failed"; return false; }
      m_cursor=0; m_summary.status=DAYE_REPLAY_STATUS_READY; m_summary.reason_code="replay_source_ready"; m_summary.is_ready=true;
      Emit(DAYE_REPLAY_EVENT_RUN_INITIALIZED,m_summary.run_id,"",DAYE_HUNT_SIDE_UNKNOWN,m_source.start_utc,m_source.start_utc,"historical_replay_initialized");
      Emit(DAYE_REPLAY_EVENT_SOURCE_LOADED,m_summary.run_id,"",DAYE_HUNT_SIDE_UNKNOWN,m_source.start_utc,m_source.end_utc,m_source.reason_code);
      m_initialized=true; return true;
   }

   bool ProcessChunk(const int requested_steps)
   {
      if(!m_initialized || m_finished) return false;
      m_summary.status=DAYE_REPLAY_STATUS_RUNNING; int steps=requested_steps; if(steps<1) steps=1;
      for(int s=0;s<steps && m_cursor<ArraySize(m_source.pairs);s++,m_cursor++)
      {
         string reason="";
         if(!ProcessOneCursor(m_cursor,reason))
         {
            m_summary.status=DAYE_REPLAY_STATUS_PIPELINE_FAILED; m_summary.reason_code=reason;
            Emit(DAYE_REPLAY_EVENT_RUN_FAILED,m_summary.run_id,"",DAYE_HUNT_SIDE_UNKNOWN,
                 m_source.pairs[m_cursor].event_time_utc,m_source.pairs[m_cursor].availability_time_utc,reason);
            m_audit.WriteSummary(m_summary); m_audit.Flush(); m_finished=true; return false;
         }
         if(m_config.progress_log_every_steps>0 && ((m_cursor+1)%m_config.progress_log_every_steps)==0)
            Print("EXP0018 P11 replay progress ",m_cursor+1,"/",ArraySize(m_source.pairs)," state_hash=",m_summary.final_state_hash);
      }
      if(m_cursor>=ArraySize(m_source.pairs)) Finish();
      return true;
   }

   bool IsFinished(void) { return m_finished; }
   bool GetSummary(DAYE_ReplaySummary &summary) { summary=m_summary; return m_initialized || m_finished; }
   int ExportResults(DAYE_ConfirmationResult &items[]) { return m_confirmation_store.ExportResults(items); }
   int ExportReferences(DAYE_ReferenceLifecycleRecord &items[]) { return m_lifecycle_store.ExportReferences(items); }
   int ExportUses(DAYE_ReferenceUseRecord &items[]) { return m_lifecycle_store.ExportUses(items); }
   void Shutdown(void) { m_audit.Close(); ArrayResize(m_source.pairs,0); ArrayResize(m_period_registry,0); ArrayResize(m_relationship_registry,0); ArrayResize(m_previous_observations,0); m_confirmation_store.Clear(); m_lifecycle_store.Clear(); m_initialized=false; }
};

#endif
