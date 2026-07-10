#ifndef __EXP0018_DAYE_CONFIRMATION_ENGINE_MQH__
#define __EXP0018_DAYE_CONFIRMATION_ENGINE_MQH__

#include <DayeTrader/EXP0018/DAYE_ConfirmationSelfTest.mqh>

class CDayeConfirmationEngine
{
private:
   DAYE_ConfirmationConfig m_config;
   DAYE_TimeConfig m_time_config;
   CDayeHuntEngine m_hunt_engine;
   CDayeConfirmationStore m_store;
   CDayeConfirmationAuditWriter m_audit;
   DAYE_ConfirmationStoreSummary m_previous_summary;
   DAYE_ConfirmationStoreSummary m_current_summary;
   bool m_has_previous_summary;
   bool m_has_current_summary;
   bool m_initialized;
   bool m_source_baselined;
   bool m_checkpoint_restored;
   int m_restored_candidate_count;
   datetime m_last_closed_host_open_utc;

   void BuildSummary(const DAYE_HuntStoreSummary &source_summary,
                     const DAYE_HostClockSnapshot &clock,
                     const datetime processing_time_utc,
                     DAYE_ConfirmationStoreSummary &summary)
   {
      ZeroMemory(summary);
      summary.schema_version=DAYE_CONFIRMATION_SCHEMA_VERSION;
      summary.status=DAYE_CONFIRM_STATUS_READY;
      summary.reason_code="confirmation_engine_ready";
      summary.is_ready=source_summary.is_ready && clock.is_ready;
      summary.is_replay_safe=source_summary.is_replay_safe && clock.is_replay_safe;
      summary.source_baselined=m_source_baselined;
      summary.checkpoint_restored=m_checkpoint_restored;
      summary.host_timeframe=clock.timeframe;
      summary.host_timeframe_seconds=clock.timeframe_seconds;
      summary.processing_time_utc=processing_time_utc;
      summary.source_observation_count=source_summary.observation_count;
      summary.pending_candidate_count=m_store.CandidateCount();
      summary.result_count=m_store.ResultCount();
      summary.remembered_finalized_count=m_store.FinalizedIdCount();
      summary.restored_candidate_count=m_restored_candidate_count;
      summary.latest_closed_host_open_utc=clock.latest_closed_bar.open_time_utc;
      summary.latest_closed_host_close_utc=clock.latest_closed_bar.close_time_utc;
      summary.event_time_utc=clock.latest_closed_bar.close_time_utc;
      summary.availability_time_utc=source_summary.availability_time_utc;
      if(summary.availability_time_utc < clock.latest_closed_bar.close_time_utc)
         summary.availability_time_utc=clock.latest_closed_bar.close_time_utc;

      DAYE_ConfirmationCandidate candidates[];
      m_store.ExportCandidates(candidates);
      if(ArraySize(candidates)>0) summary.latest_candidate_id=candidates[ArraySize(candidates)-1].candidate_id;

      DAYE_ConfirmationResult results[];
      m_store.ExportResults(results);
      for(int i=0;i<ArraySize(results);i++)
      {
         summary.latest_result_id=results[i].result_id;
         if(results[i].outcome == DAYE_CONFIRM_OUTCOME_CONFIRMED)
         {
            summary.confirmed_count++;
            summary.latest_confirmed_result_id=results[i].result_id;
         }
         else if(results[i].outcome == DAYE_CONFIRM_OUTCOME_INVALIDATED_DOUBLE_HUNT) summary.invalidated_double_hunt_count++;
         else if(results[i].outcome == DAYE_CONFIRM_OUTCOME_NO_SIGNAL_AT_CLOSE) summary.no_signal_count++;
         else if(results[i].outcome == DAYE_CONFIRM_OUTCOME_INVALIDATED_ROLE_CHANGED) summary.role_changed_count++;
         else if(results[i].outcome == DAYE_CONFIRM_OUTCOME_MISSED_CLOSE_REPLAY_REQUIRED) summary.missed_close_count++;
         else summary.unavailable_count++;
      }

      if(!source_summary.is_ready)
      {
         summary.status=DAYE_CONFIRM_STATUS_SOURCE_NOT_READY;
         summary.reason_code="p05_source_not_ready";
         summary.is_ready=false;
      }
      else if(!clock.is_ready)
      {
         summary.status=DAYE_CONFIRM_STATUS_HOST_CLOCK_NOT_READY;
         summary.reason_code=clock.reason_code;
         summary.is_ready=false;
      }
      else if(!m_source_baselined && m_store.CandidateCount()==0)
      {
         summary.status=DAYE_CONFIRM_STATUS_NO_LIVE_TRANSITIONS_YET;
         summary.reason_code="source_snapshot_not_yet_baselined";
      }
      summary.run_key="EXP0018|P06|CONFIRM_V2|" + IntegerToString((int)clock.timeframe) + "|" +
                      IntegerToString((long)summary.latest_closed_host_open_utc) + "|" + summary.latest_result_id;
   }

   bool BecameOneSided(const DAYE_HuntObservation &current)
   {
      DAYE_ConfirmationSourceMemory prior;
      if(!m_store.FindSourceMemory(current.observation_id,prior))
         return current.is_one_sided;
      return current.is_one_sided && (!prior.is_one_sided || prior.pair_state != current.pair_state);
   }

   void WriteEvents(const DAYE_ConfirmationEvent &events[],const bool print_events)
   {
      for(int i=0;i<ArraySize(events);i++)
      {
         if(print_events) Print(DAYE_FormatConfirmationEvent(events[i]));
         m_audit.WriteEvent(events[i]);
      }
   }

public:
   CDayeConfirmationEngine(void)
   {
      ZeroMemory(m_previous_summary);
      ZeroMemory(m_current_summary);
      m_has_previous_summary=false;
      m_has_current_summary=false;
      m_initialized=false;
      m_source_baselined=false;
      m_checkpoint_restored=false;
      m_restored_candidate_count=0;
      m_last_closed_host_open_utc=0;
   }

   bool Initialize(const DAYE_ConfirmationConfig &config,
                   const DAYE_TimeConfig &time_config,
                   const bool run_self_tests,
                   const bool write_audit_csv,
                   const string audit_filename)
   {
      string reason="";
      if(!DAYE_ValidateConfirmationConfig(config,reason))
      {
         Print("EXP0018 P06 invalid confirmation config reason=",reason);
         return false;
      }
      if(!DAYE_ValidateHuntConfig(config.hunt_config,reason) || !DAYE_ValidateTimeConfig(time_config,reason))
      {
         Print("EXP0018 P06 invalid dependency config reason=",reason);
         return false;
      }
      if(run_self_tests && !DAYE_RunEmbeddedConfirmationSelfTests())
      {
         Print("EXP0018 P06 initialization blocked because embedded self-test failed.");
         return false;
      }

      m_config=config;
      m_time_config=time_config;
      if(!m_hunt_engine.Initialize(config.hunt_config,time_config,run_self_tests,false,""))
      {
         Print("EXP0018 P06 could not initialize P05 dependency.");
         return false;
      }
      if(!m_audit.Open(audit_filename,write_audit_csv))
      {
         m_hunt_engine.Shutdown();
         return false;
      }

      int restored_finalized=0;
      if(!DAYE_LoadConfirmationCheckpoint(config,m_last_closed_host_open_utc,m_store,m_restored_candidate_count,restored_finalized,reason))
      {
         Print("EXP0018 P06 checkpoint restore failed reason=",reason);
         m_audit.Close();
         m_hunt_engine.Shutdown();
         return false;
      }
      m_checkpoint_restored=(m_restored_candidate_count>0 || restored_finalized>0 || m_last_closed_host_open_utc>0);
      m_initialized=true;
      Print("EXP0018 P06 Host-Timeframe Close Confirmation v2 initialized. It confirms HIGH/LOW side facts only; no direction mapping, lifecycle retirement, drawing, risk, or order authority exists.");
      return true;
   }

   bool Process(const datetime current_broker_time,
                const bool print_summary,
                const bool print_latest_result,
                const bool print_events,
                const bool show_chart_comment,
                const bool write_summary_rows,
                const int audit_latest_candidate_count,
                const int audit_latest_result_count)
   {
      if(!m_initialized) return false;

      m_hunt_engine.Process(current_broker_time,false,false,false,false,false,0);
      DAYE_HuntStoreSummary hunt_summary;
      if(!m_hunt_engine.GetCurrentSummary(hunt_summary)) return true;
      DAYE_HuntObservation observations[];
      m_hunt_engine.ExportObservations(observations);

      datetime processing_time_utc=0;
      int broker_offset=0;
      bool replay_safe=true;
      string time_reason="";
      if(!DAYE_BrokerToUtc(current_broker_time,m_time_config,processing_time_utc,broker_offset,replay_safe,time_reason))
      {
         processing_time_utc=TimeGMT();
         if(processing_time_utc<=0) processing_time_utc=current_broker_time;
      }

      DAYE_HostClockSnapshot clock;
      DAYE_ReadHostClock(m_config,m_time_config,processing_time_utc,clock);
      DAYE_ConfirmationEvent events[];
      ArrayResize(events,0);
      bool state_changed=false;

      bool had_clock_baseline=(m_last_closed_host_open_utc>0);
      bool closed_advanced=false;
      bool missed_host_close=false;
      datetime previous_closed_close_utc=0;
      if(clock.is_ready)
      {
         if(!had_clock_baseline)
         {
            m_last_closed_host_open_utc=clock.latest_closed_bar.open_time_utc;
            state_changed=true;
         }
         else if(clock.latest_closed_bar.open_time_utc > m_last_closed_host_open_utc)
         {
            closed_advanced=true;
            previous_closed_close_utc=m_last_closed_host_open_utc + (datetime)clock.timeframe_seconds;
            if(clock.latest_closed_bar.open_time_utc > previous_closed_close_utc)
               missed_host_close=true;
            DAYE_AppendConfirmationEvent(events,DAYE_CONFIRM_EVENT_HOST_BAR_CLOSED,"","","","",DAYE_HUNT_SIDE_UNKNOWN,DAYE_HUNT_PAIR_UNKNOWN,DAYE_HUNT_PAIR_UNKNOWN,DAYE_CONFIRM_OUTCOME_UNKNOWN,clock.latest_closed_bar.close_time_utc,clock.latest_closed_bar.close_time_utc,processing_time_utc,missed_host_close ? "host_bar_advanced_with_gap" : "exact_next_host_bar_closed");
         }
      }

      if(!m_source_baselined)
      {
         m_store.ReplaceSourceMemory(observations);
         m_source_baselined=true;
         state_changed=true;
         DAYE_AppendConfirmationEvent(events,DAYE_CONFIRM_EVENT_SOURCE_BASELINED,"","","","",DAYE_HUNT_SIDE_UNKNOWN,DAYE_HUNT_PAIR_UNKNOWN,DAYE_HUNT_PAIR_UNKNOWN,DAYE_CONFIRM_OUTCOME_UNKNOWN,processing_time_utc,processing_time_utc,processing_time_utc,"existing_source_states_baselined_without_retroactive_candidate_creation");
      }
      else
      {
         for(int i=0;i<ArraySize(observations);i++)
         {
            int candidate_index=m_store.FindCandidateIndexByObservationId(observations[i].observation_id);
            if(candidate_index>=0)
            {
               DAYE_ConfirmationCandidate candidate;
               if(m_store.GetCandidate(candidate_index,candidate))
               {
                  DAYE_HuntPairState before=candidate.last_pair_state;
                  bool changed=false;
                  DAYE_UpdateConfirmationCandidate(observations[i],candidate,changed);
                  if(changed)
                  {
                     m_store.SetCandidate(candidate_index,candidate);
                     state_changed=true;
                     DAYE_AppendConfirmationEvent(events,DAYE_CONFIRM_EVENT_CANDIDATE_UPDATED,candidate.candidate_id,"",candidate.observation_id,candidate.relationship_id,candidate.side,before,candidate.last_pair_state,DAYE_CONFIRM_OUTCOME_UNKNOWN,observations[i].event_time_utc,observations[i].availability_time_utc,processing_time_utc,"candidate_source_state_updated_before_target_close");
                  }
               }
               continue;
            }

            if(m_store.IsObservationFinalized(observations[i].observation_id)) continue;
            if(!BecameOneSided(observations[i])) continue;

            DAYE_HostBarPair target;
            string target_reason="";
            if(!DAYE_ResolveCandidateTarget(observations[i],clock,closed_advanced,previous_closed_close_utc,target,target_reason))
               continue;

            DAYE_ConfirmationCandidate candidate;
            string candidate_reason="";
            if(!DAYE_InitializeConfirmationCandidate(observations[i],target,candidate,candidate_reason))
               continue;
            if(m_store.AppendCandidate(candidate,m_config.maximum_pending_candidates))
            {
               state_changed=true;
               DAYE_AppendConfirmationEvent(events,DAYE_CONFIRM_EVENT_CANDIDATE_OPENED,candidate.candidate_id,"",candidate.observation_id,candidate.relationship_id,candidate.side,DAYE_HUNT_PAIR_UNKNOWN,candidate.initial_pair_state,DAYE_CONFIRM_OUTCOME_UNKNOWN,candidate.first_seen_event_time_utc,candidate.first_seen_availability_time_utc,processing_time_utc,target_reason);
            }
         }
      }

      // Restored candidates and live candidates both receive the current source snapshot, but never data after target close.
      for(int i=0;i<m_store.CandidateCount();i++)
      {
         DAYE_ConfirmationCandidate candidate;
         if(!m_store.GetCandidate(i,candidate)) continue;
         DAYE_HuntObservation observation;
         if(!DAYE_FindHuntObservationById(observations,candidate.observation_id,observation)) continue;
         DAYE_HuntPairState before=candidate.last_pair_state;
         bool changed=false;
         DAYE_UpdateConfirmationCandidate(observation,candidate,changed);
         if(changed)
         {
            m_store.SetCandidate(i,candidate);
            state_changed=true;
            DAYE_AppendConfirmationEvent(events,DAYE_CONFIRM_EVENT_CANDIDATE_UPDATED,candidate.candidate_id,"",candidate.observation_id,candidate.relationship_id,candidate.side,before,candidate.last_pair_state,DAYE_CONFIRM_OUTCOME_UNKNOWN,observation.event_time_utc,observation.availability_time_utc,processing_time_utc,"pending_candidate_refreshed_at_or_before_target_close");
         }
      }

      if(closed_advanced && clock.latest_closed_bar.is_ready)
      {
         for(int i=m_store.CandidateCount()-1;i>=0;i--)
         {
            DAYE_ConfirmationCandidate candidate;
            if(!m_store.GetCandidate(i,candidate)) continue;
            if(candidate.target_host_close_utc > clock.latest_closed_bar.close_time_utc) continue;

            bool candidate_missed=missed_host_close || candidate.target_host_close_utc < clock.latest_closed_bar.close_time_utc;
            DAYE_ConfirmationResult result;
            DAYE_FinalizeCandidateAtClose(candidate,clock.latest_closed_bar,processing_time_utc,candidate_missed,result);
            bool publish=m_config.publish_nonconfirmed_results || result.is_confirmed;
            if(publish) m_store.AppendResult(result,m_config.maximum_results_to_publish);
            m_store.RememberFinalizedObservation(candidate.observation_id,m_config.maximum_finalized_ids_to_remember);
            m_store.RemoveCandidateByObservationId(candidate.observation_id);
            state_changed=true;

            DAYE_ConfirmationEventType event_type=DAYE_EventTypeForOutcome(result.outcome);
            DAYE_AppendConfirmationEvent(events,event_type,candidate.candidate_id,result.result_id,candidate.observation_id,candidate.relationship_id,candidate.side,candidate.initial_pair_state,candidate.last_pair_state,result.outcome,result.event_time_utc,result.availability_time_utc,result.processing_time_utc,result.reason_code);
            m_audit.WriteResult(result);
         }
      }

      m_store.ReplaceSourceMemory(observations);
      if(clock.is_ready && clock.latest_closed_bar.open_time_utc >= m_last_closed_host_open_utc)
      {
         if(clock.latest_closed_bar.open_time_utc != m_last_closed_host_open_utc) state_changed=true;
         m_last_closed_host_open_utc=clock.latest_closed_bar.open_time_utc;
      }

      DAYE_ConfirmationStoreSummary summary;
      BuildSummary(hunt_summary,clock,processing_time_utc,summary);
      if(!m_has_previous_summary)
      {
         DAYE_AppendConfirmationEvent(events,DAYE_CONFIRM_EVENT_ENGINE_INITIALIZED,"","","","",DAYE_HUNT_SIDE_UNKNOWN,DAYE_HUNT_PAIR_UNKNOWN,DAYE_HUNT_PAIR_UNKNOWN,DAYE_CONFIRM_OUTCOME_UNKNOWN,processing_time_utc,processing_time_utc,processing_time_utc,"confirmation_engine_initialized");
         if(m_checkpoint_restored)
            DAYE_AppendConfirmationEvent(events,DAYE_CONFIRM_EVENT_CHECKPOINT_RESTORED,"","","","",DAYE_HUNT_SIDE_UNKNOWN,DAYE_HUNT_PAIR_UNKNOWN,DAYE_HUNT_PAIR_UNKNOWN,DAYE_CONFIRM_OUTCOME_UNKNOWN,processing_time_utc,processing_time_utc,processing_time_utc,"pending_candidates_or_finalized_ids_restored");
      }
      else if(m_previous_summary.status != summary.status)
      {
         DAYE_AppendConfirmationEvent(events,DAYE_CONFIRM_EVENT_STATUS_CHANGED,"","","","",DAYE_HUNT_SIDE_UNKNOWN,DAYE_HUNT_PAIR_UNKNOWN,DAYE_HUNT_PAIR_UNKNOWN,DAYE_CONFIRM_OUTCOME_UNKNOWN,summary.event_time_utc,summary.availability_time_utc,summary.processing_time_utc,summary.reason_code);
      }

      if(state_changed)
      {
         string checkpoint_reason="";
         if(!DAYE_SaveConfirmationCheckpoint(m_config,m_last_closed_host_open_utc,m_store,checkpoint_reason))
         {
            summary.status=DAYE_CONFIRM_STATUS_CHECKPOINT_ERROR;
            summary.reason_code=checkpoint_reason;
            summary.is_ready=false;
         }
         else if(m_config.persist_checkpoint)
         {
            DAYE_AppendConfirmationEvent(events,DAYE_CONFIRM_EVENT_CHECKPOINT_SAVED,"","","","",DAYE_HUNT_SIDE_UNKNOWN,DAYE_HUNT_PAIR_UNKNOWN,DAYE_HUNT_PAIR_UNKNOWN,DAYE_CONFIRM_OUTCOME_UNKNOWN,processing_time_utc,processing_time_utc,processing_time_utc,"confirmation_checkpoint_saved");
         }
      }

      WriteEvents(events,print_events);
      if(print_summary) Print(DAYE_FormatConfirmationSummary(summary));
      if(print_latest_result && m_store.ResultCount()>0)
      {
         DAYE_ConfirmationResult latest;
         if(m_store.GetResult(m_store.ResultCount()-1,latest)) Print("  latest_result ",DAYE_FormatConfirmationResult(latest));
      }

      if(write_summary_rows) m_audit.WriteSummary(summary);
      int candidate_start=m_store.CandidateCount()-audit_latest_candidate_count;
      if(candidate_start<0) candidate_start=0;
      for(int i=candidate_start;i<m_store.CandidateCount();i++)
      {
         DAYE_ConfirmationCandidate candidate;
         if(m_store.GetCandidate(i,candidate)) m_audit.WriteCandidate(candidate);
      }
      int result_start=m_store.ResultCount()-audit_latest_result_count;
      if(result_start<0) result_start=0;
      for(int i=result_start;i<m_store.ResultCount();i++)
      {
         DAYE_ConfirmationResult result;
         if(m_store.GetResult(i,result)) m_audit.WriteResult(result);
      }
      m_audit.Flush();

      if(show_chart_comment)
         Comment(DAYE_FormatConfirmationSummary(summary) + "\nClose outcomes only — no lifecycle, drawing, direction, risk, or trading.");
      else Comment("");

      m_previous_summary=summary;
      m_current_summary=summary;
      m_has_previous_summary=true;
      m_has_current_summary=true;
      return true;
   }

   bool GetCurrentSummary(DAYE_ConfirmationStoreSummary &summary)
   {
      if(!m_has_current_summary) return false;
      summary=m_current_summary;
      return true;
   }

   int ExportCandidates(DAYE_ConfirmationCandidate &items[]) { return m_store.ExportCandidates(items); }
   int ExportResults(DAYE_ConfirmationResult &items[]) { return m_store.ExportResults(items); }

   // P07 read-only evidence surface. This does not grant lifecycle authority to P06.
   int ExportSourceObservations(DAYE_HuntObservation &items[]) { return m_hunt_engine.ExportObservations(items); }

   bool GetSourceHuntSummary(DAYE_HuntStoreSummary &summary)
   {
      return m_hunt_engine.GetCurrentSummary(summary);
   }

   // P08 read-only period provenance. Confirmation authority remains unchanged.
   int ExportSourcePeriods(DAYE_PairedPeriodSnapshot &items[])
   {
      return m_hunt_engine.ExportSourcePeriods(items);
   }

   void Shutdown(void)
   {
      string reason="";
      DAYE_SaveConfirmationCheckpoint(m_config,m_last_closed_host_open_utc,m_store,reason);
      Comment("");
      m_audit.Close();
      m_store.Clear();
      m_hunt_engine.Shutdown();
      ZeroMemory(m_previous_summary);
      ZeroMemory(m_current_summary);
      m_has_previous_summary=false;
      m_has_current_summary=false;
      m_initialized=false;
      m_source_baselined=false;
      m_checkpoint_restored=false;
      m_restored_candidate_count=0;
      m_last_closed_host_open_utc=0;
   }
};

#endif
