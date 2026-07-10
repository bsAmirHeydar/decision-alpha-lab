#ifndef __EXP0018_DAYE_REPLAY_AUDIT_MQH__
#define __EXP0018_DAYE_REPLAY_AUDIT_MQH__

#include <DayeTrader/EXP0018/DAYE_ReplayReducer.mqh>

class CDayeReplayAuditWriter
{
private:
   int m_summary,m_events,m_frames,m_confirmations,m_references,m_uses;
   bool m_enabled;

   int OpenCsv(const string filename)
   { return FileOpen(filename,FILE_WRITE|FILE_CSV|FILE_COMMON|FILE_ANSI,','); }
public:
   CDayeReplayAuditWriter(void) { m_summary=m_events=m_frames=m_confirmations=m_references=m_uses=INVALID_HANDLE; m_enabled=false; }

   bool Open(const DAYE_ReplayConfig &config)
   {
      m_enabled=true;
      m_summary=OpenCsv(config.output_prefix+"_summary.csv");
      m_events=OpenCsv(config.output_prefix+"_events.csv");
      m_frames=OpenCsv(config.output_prefix+"_frames.csv");
      m_confirmations=OpenCsv(config.output_prefix+"_confirmations.csv");
      m_references=OpenCsv(config.output_prefix+"_references.csv");
      m_uses=OpenCsv(config.output_prefix+"_uses.csv");
      if(m_summary==INVALID_HANDLE || m_events==INVALID_HANDLE || m_frames==INVALID_HANDLE ||
         m_confirmations==INVALID_HANDLE || m_references==INVALID_HANDLE || m_uses==INVALID_HANDLE) return false;
      FileWrite(m_summary,"schema_version","run_id","status","reason","start_utc","end_utc","source_pairs","processed_cursors","results","confirmed","references","retired","accepted_uses","source_hash","confirmation_hash","lifecycle_hash","final_state_hash");
      FileWrite(m_events,"schema_version","event_id","event_type","subject_id","relationship_id","side","event_time_utc","availability_time_utc","processing_time_utc","reason","state_hash");
      FileWrite(m_frames,"schema_version","cursor_index","event_time_utc","availability_time_utc","period_count","ready_resolutions","ready_observations","one_sided","pending_candidates","results","references","accepted_uses","frame_hash");
      FileWrite(m_confirmations,"schema_version","result_id","outcome","reason","relationship_id","side","hunter","protected","current_period_id","reference_period_id","host_open_utc","host_close_utc","hunter_reference","endpoint","event_time_utc","availability_time_utc");
      FileWrite(m_references,"schema_version","reference_id","state","reason","side","protected","accepted_use_count","duplicate_use_count","rejected_use_count","activation_utc","retirement_utc","retirement_evidence_id");
      FileWrite(m_uses,"schema_version","use_id","status","reason","reference_id","result_id","relationship_id","side","hunter","protected","host_close_utc","reference_price","endpoint_price");
      return true;
   }

   void Close(void)
   {
      int handles[6]; handles[0]=m_summary; handles[1]=m_events; handles[2]=m_frames; handles[3]=m_confirmations; handles[4]=m_references; handles[5]=m_uses;
      for(int i=0;i<6;i++) if(handles[i]!=INVALID_HANDLE) FileClose(handles[i]);
      m_summary=m_events=m_frames=m_confirmations=m_references=m_uses=INVALID_HANDLE; m_enabled=false;
   }
   void Flush(void)
   {
      if(!m_enabled) return; if(m_summary!=INVALID_HANDLE) FileFlush(m_summary); if(m_events!=INVALID_HANDLE) FileFlush(m_events);
      if(m_frames!=INVALID_HANDLE) FileFlush(m_frames); if(m_confirmations!=INVALID_HANDLE) FileFlush(m_confirmations);
      if(m_references!=INVALID_HANDLE) FileFlush(m_references); if(m_uses!=INVALID_HANDLE) FileFlush(m_uses);
   }

   bool WriteEvent(const DAYE_ReplayEvent &e)
   {
      if(!m_enabled || m_events==INVALID_HANDLE) return false;
      FileWrite(m_events,e.schema_version,e.event_id,DAYE_ReplayEventTypeToString(e.event_type),e.subject_id,e.relationship_id,
                DAYE_HuntSideToString(e.side),TimeToString(e.event_time_utc,TIME_DATE|TIME_SECONDS),
                TimeToString(e.availability_time_utc,TIME_DATE|TIME_SECONDS),TimeToString(e.processing_time_utc,TIME_DATE|TIME_SECONDS),e.reason_code,e.state_hash);
      return true;
   }
   bool WriteFrame(const DAYE_ReplayFrame &f)
   {
      if(!m_enabled || m_frames==INVALID_HANDLE) return false;
      FileWrite(m_frames,f.schema_version,f.cursor_index,TimeToString(f.event_time_utc,TIME_DATE|TIME_SECONDS),TimeToString(f.availability_time_utc,TIME_DATE|TIME_SECONDS),
                f.period_count,f.ready_resolution_count,f.ready_observation_count,f.one_sided_count,f.pending_candidate_count,f.result_count,f.reference_count,f.accepted_use_count,f.frame_hash);
      return true;
   }
   bool WriteConfirmation(const DAYE_ConfirmationResult &r)
   {
      if(!m_enabled || m_confirmations==INVALID_HANDLE) return false;
      FileWrite(m_confirmations,r.schema_version,r.result_id,DAYE_ConfirmationOutcomeToString(r.outcome),r.reason_code,r.relationship_id,DAYE_HuntSideToString(r.side),
                r.hunter_canonical_symbol,r.protected_canonical_symbol,r.current_period_instance_id,r.reference_period_instance_id,
                TimeToString(r.host_bar_open_utc,TIME_DATE|TIME_SECONDS),TimeToString(r.host_bar_close_utc,TIME_DATE|TIME_SECONDS),
                DoubleToString(r.hunter_reference_price,8),DoubleToString(r.confirmation_endpoint_price,8),
                TimeToString(r.event_time_utc,TIME_DATE|TIME_SECONDS),TimeToString(r.availability_time_utc,TIME_DATE|TIME_SECONDS));
      return true;
   }
   bool WriteReference(const DAYE_ReferenceLifecycleRecord &r)
   {
      if(!m_enabled || m_references==INVALID_HANDLE) return false;
      FileWrite(m_references,r.schema_version,r.reference_id,DAYE_ReferenceLifecycleStateToString(r.state),r.reason_code,DAYE_HuntSideToString(r.side),
                r.protected_canonical_symbol,r.accepted_use_count,r.duplicate_use_count,r.rejected_use_count,
                TimeToString(r.activation_event_time_utc,TIME_DATE|TIME_SECONDS),TimeToString(r.retirement_event_time_utc,TIME_DATE|TIME_SECONDS),r.retirement_evidence_id);
      return true;
   }
   bool WriteUse(const DAYE_ReferenceUseRecord &u)
   {
      if(!m_enabled || m_uses==INVALID_HANDLE) return false;
      FileWrite(m_uses,u.schema_version,u.use_id,DAYE_ReferenceUseStatusToString(u.status),u.reason_code,u.reference_id,u.result_id,u.relationship_id,
                DAYE_HuntSideToString(u.side),u.hunter_canonical_symbol,u.protected_canonical_symbol,TimeToString(u.host_bar_close_utc,TIME_DATE|TIME_SECONDS),
                DoubleToString(u.hunter_reference_price,8),DoubleToString(u.confirmation_endpoint_price,8));
      return true;
   }
   bool WriteSummary(const DAYE_ReplaySummary &s)
   {
      if(!m_enabled || m_summary==INVALID_HANDLE) return false;
      FileWrite(m_summary,s.schema_version,s.run_id,DAYE_ReplayStatusToString(s.status),s.reason_code,
                TimeToString(s.start_utc,TIME_DATE|TIME_SECONDS),TimeToString(s.end_utc,TIME_DATE|TIME_SECONDS),s.source_pair_count,s.processed_cursor_count,
                s.confirmation_result_count,s.confirmed_count,s.reference_count,s.retired_reference_count,s.accepted_use_count,
                s.source_hash,s.confirmation_hash,s.lifecycle_hash,s.final_state_hash);
      return true;
   }
};

#endif
