#ifndef __EXP0018_DAYE_CONFIRMATION_AUDIT_MQH__
#define __EXP0018_DAYE_CONFIRMATION_AUDIT_MQH__

#include <DayeTrader/EXP0018/DAYE_ConfirmationDiagnostics.mqh>

class CDayeConfirmationAuditWriter
{
private:
   int m_handle;
   bool m_enabled;

   bool WriteHeader(void)
   {
      if(m_handle == INVALID_HANDLE) return false;
      FileWrite(m_handle,
                "schema_version","record_type","record_id","status","reason_code",
                "candidate_id","result_id","observation_id","opportunity_id","relationship_id","source_alias","side","major","chart_label",
                "initial_pair_state","close_pair_state","outcome","confirmed","immutable",
                "hunter_symbol","protected_symbol","current_period_instance_id","reference_period_instance_id",
                "hunter_reference_price","protected_reference_price",
                "host_bar_id","host_open_utc","host_close_utc","host_open","host_high","host_low","host_close","confirmation_endpoint",
                "candidate_first_seen_utc","event_time_utc","availability_time_utc","processing_time_utc",
                "source_observation_count","pending_candidate_count","result_count","confirmed_count","double_count","no_signal_count","unavailable_count","role_changed_count","missed_close_count",
                "event_type","from_pair_state","to_pair_state");
      FileFlush(m_handle);
      return true;
   }

public:
   CDayeConfirmationAuditWriter(void) { m_handle=INVALID_HANDLE; m_enabled=false; }

   bool Open(const string filename,const bool enabled)
   {
      m_enabled=enabled;
      if(!enabled) return true;
      m_handle=FileOpen(filename,FILE_READ|FILE_WRITE|FILE_CSV|FILE_COMMON|FILE_SHARE_READ|FILE_SHARE_WRITE,',');
      if(m_handle == INVALID_HANDLE)
      {
         Print("EXP0018 P06 audit open failed file=",filename," error=",GetLastError());
         return false;
      }
      if(FileSize(m_handle) == 0) return WriteHeader();
      FileSeek(m_handle,0,SEEK_END);
      return true;
   }

   bool WriteSummary(const DAYE_ConfirmationStoreSummary &summary)
   {
      if(!m_enabled) return true;
      FileWrite(m_handle,
                summary.schema_version,"SUMMARY",summary.run_key,DAYE_ConfirmationStatusToString(summary.status),summary.reason_code,
                summary.latest_candidate_id,summary.latest_result_id,"","", "","","",0,"",
                "","","",0,0,
                "","","","",0,0,
                "",summary.latest_closed_host_open_utc,summary.latest_closed_host_close_utc,0,0,0,0,0,
                0,summary.event_time_utc,summary.availability_time_utc,summary.processing_time_utc,
                summary.source_observation_count,summary.pending_candidate_count,summary.result_count,summary.confirmed_count,summary.invalidated_double_hunt_count,summary.no_signal_count,summary.unavailable_count,summary.role_changed_count,summary.missed_close_count,
                "","","");
      return true;
   }

   bool WriteCandidate(const DAYE_ConfirmationCandidate &item)
   {
      if(!m_enabled) return true;
      FileWrite(m_handle,
                item.schema_version,"CANDIDATE",item.candidate_id,DAYE_ConfirmationStatusToString(item.status),item.reason_code,
                item.candidate_id,"",item.observation_id,item.opportunity_id,item.relationship_id,item.source_alias,DAYE_HuntSideToString(item.side),item.is_major ? 1 : 0,item.chart_label,
                DAYE_HuntPairStateToString(item.initial_pair_state),DAYE_HuntPairStateToString(item.last_pair_state),"",0,0,
                item.hunter_canonical_symbol,item.protected_canonical_symbol,item.current_period_instance_id,item.reference_period_instance_id,item.hunter_reference_price,item.protected_reference_price,
                item.target_host_bar_id,item.target_host_open_utc,item.target_host_close_utc,0,0,0,0,0,
                item.first_seen_availability_time_utc,item.target_host_close_utc,item.last_seen_availability_time_utc,0,
                0,0,0,0,0,0,0,0,0,
                "","","");
      return true;
   }

   bool WriteResult(const DAYE_ConfirmationResult &item)
   {
      if(!m_enabled) return true;
      FileWrite(m_handle,
                item.schema_version,"RESULT",item.result_id,DAYE_ConfirmationStatusToString(item.status),item.reason_code,
                item.candidate_id,item.result_id,item.observation_id,item.opportunity_id,item.relationship_id,item.source_alias,DAYE_HuntSideToString(item.side),item.is_major ? 1 : 0,item.chart_label,
                DAYE_HuntPairStateToString(item.initial_pair_state),DAYE_HuntPairStateToString(item.close_pair_state),DAYE_ConfirmationOutcomeToString(item.outcome),item.is_confirmed ? 1 : 0,item.is_immutable ? 1 : 0,
                item.hunter_canonical_symbol,item.protected_canonical_symbol,item.current_period_instance_id,item.reference_period_instance_id,item.hunter_reference_price,item.protected_reference_price,
                item.host_bar_id,item.host_bar_open_utc,item.host_bar_close_utc,item.hunter_host_open,item.hunter_host_high,item.hunter_host_low,item.hunter_host_close,item.confirmation_endpoint_price,
                item.candidate_first_seen_utc,item.event_time_utc,item.availability_time_utc,item.processing_time_utc,
                0,0,0,0,0,0,0,0,0,
                "","","");
      return true;
   }

   bool WriteEvent(const DAYE_ConfirmationEvent &event)
   {
      if(!m_enabled) return true;
      FileWrite(m_handle,
                event.schema_version,"EVENT",event.event_id,"",event.reason_code,
                event.candidate_id,event.result_id,event.observation_id,"",event.relationship_id,"",DAYE_HuntSideToString(event.side),0,"",
                DAYE_HuntPairStateToString(event.from_pair_state),DAYE_HuntPairStateToString(event.to_pair_state),DAYE_ConfirmationOutcomeToString(event.outcome),0,0,
                "","","","",0,0,
                "",0,0,0,0,0,0,0,
                0,event.event_time_utc,event.availability_time_utc,event.processing_time_utc,
                0,0,0,0,0,0,0,0,0,
                DAYE_ConfirmationEventTypeToString(event.event_type),DAYE_HuntPairStateToString(event.from_pair_state),DAYE_HuntPairStateToString(event.to_pair_state));
      return true;
   }

   void Flush(void) { if(m_enabled && m_handle != INVALID_HANDLE) FileFlush(m_handle); }
   void Close(void)
   {
      if(m_handle != INVALID_HANDLE) FileClose(m_handle);
      m_handle=INVALID_HANDLE;
      m_enabled=false;
   }
};

#endif
