#ifndef __EXP0018_DAYE_LIFECYCLE_AUDIT_MQH__
#define __EXP0018_DAYE_LIFECYCLE_AUDIT_MQH__

#include <DayeTrader/EXP0018/DAYE_LifecycleDiagnostics.mqh>
#include <AlphaLab/UC04/AL_UC04CorePrimitives.mqh>

class CDayeLifecycleAuditWriter
{
private:
   int m_handle;
   bool m_enabled;
public:
   CDayeLifecycleAuditWriter(void) { m_handle=INVALID_HANDLE; m_enabled=false; }
   bool Open(const bool enabled,const string filename)
   {
      m_enabled=enabled; if(!enabled) return true;
      m_handle=FileOpen(filename,FILE_WRITE|FILE_CSV|FILE_COMMON|FILE_SHARE_READ,',');
      if(m_handle==INVALID_HANDLE) return false;
      FileWrite(m_handle,"schema_version","record_type","event_time_utc","availability_time_utc","processing_time_utc",
                "reference_id","use_id","result_id","observation_id","relationship_id","side","reference_state",
                "use_status","hunter","protected","accepted_use_count","reason_code");
      return true;
   }
   void WriteSummary(const DAYE_LifecycleStoreSummary &s)
   {
      if(!m_enabled || m_handle==INVALID_HANDLE) return;
      FileWrite(m_handle,s.schema_version,"SUMMARY",s.event_time_utc,s.availability_time_utc,s.processing_time_utc,
                s.latest_reference_id,s.latest_use_id,"","","","","",DAYE_LifecycleStatusToString(s.status),"","",
                s.accepted_use_count,s.reason_code);
   }
   void WriteReference(const DAYE_ReferenceLifecycleRecord &r)
   {
      if(!m_enabled || m_handle==INVALID_HANDLE) return;
      FileWrite(m_handle,r.schema_version,"REFERENCE",r.retirement_event_time_utc>0?r.retirement_event_time_utc:r.activation_event_time_utc,
                r.retirement_availability_time_utc>0?r.retirement_availability_time_utc:r.activation_availability_time_utc,TimeGMT(),
                r.reference_id,"",r.latest_confirmation_result_id,r.latest_observation_id,"",DAYE_HuntSideToString(r.side),
                DAYE_ReferenceLifecycleStateToString(r.state),"",r.first_hunter_canonical_symbol,r.protected_canonical_symbol,
                r.accepted_use_count,r.reason_code);
   }
   void WriteUse(const DAYE_ReferenceUseRecord &u)
   {
      if(!m_enabled || m_handle==INVALID_HANDLE) return;
      FileWrite(m_handle,u.schema_version,"USE",u.event_time_utc,u.availability_time_utc,u.processing_time_utc,u.reference_id,u.use_id,
                u.result_id,u.observation_id,u.relationship_id,DAYE_HuntSideToString(u.side),"",DAYE_ReferenceUseStatusToString(u.status),
                u.hunter_canonical_symbol,u.protected_canonical_symbol,u.is_accepted?1:0,u.reason_code);
   }
   void WriteEvent(const DAYE_LifecycleEvent &e)
   {
      if(!m_enabled || m_handle==INVALID_HANDLE) return;
      FileWrite(m_handle,e.schema_version,"EVENT",e.event_time_utc,e.availability_time_utc,e.processing_time_utc,e.reference_id,e.use_id,
                e.result_id,e.observation_id,e.relationship_id,DAYE_HuntSideToString(e.side),DAYE_ReferenceLifecycleStateToString(e.to_state),
                DAYE_ReferenceUseStatusToString(e.use_status),"","",0,e.reason_code);
   }
   void Flush(void) { if(m_enabled && m_handle!=INVALID_HANDLE) FileFlush(m_handle); }
   void Close(void) {
      AL_UC04CloseFileHandle(m_handle, m_enabled);
   }
};

#endif
