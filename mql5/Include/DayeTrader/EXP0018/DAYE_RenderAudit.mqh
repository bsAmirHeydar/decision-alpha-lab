#ifndef __EXP0018_DAYE_RENDER_AUDIT_MQH__
#define __EXP0018_DAYE_RENDER_AUDIT_MQH__

#include <DayeTrader/EXP0018/DAYE_RenderDiagnostics.mqh>

class CDayeRenderAuditWriter
{
private:
   int m_handle;
   bool m_enabled;
public:
   CDayeRenderAuditWriter(void) { m_handle=INVALID_HANDLE; m_enabled=false; }
   bool Open(const string filename,const bool enabled)
   {
      m_enabled=enabled;
      if(!enabled) return true;
      m_handle=FileOpen(filename,FILE_READ|FILE_WRITE|FILE_CSV|FILE_COMMON|FILE_ANSI,',');
      if(m_handle==INVALID_HANDLE) return false;
      if(FileSize(m_handle)==0)
         FileWrite(m_handle,"schema_version","record_type","event_id","event_type","projection_id","use_id","reference_id","relationship_id","source_alias","side","hunter_symbol","protected_symbol","chart_id","chart_timeframe","line_object","text_object","status","reference_time_utc","confirmation_time_utc","reference_time_broker","confirmation_time_broker","reference_price","confirmation_price","event_time_utc","availability_time_utc","processing_time_utc","reason_code");
      FileSeek(m_handle,0,SEEK_END);
      return true;
   }
   void WriteProjection(const DAYE_RenderProjection &p)
   {
      if(!m_enabled || m_handle==INVALID_HANDLE) return;
      FileWrite(m_handle,p.schema_version,"PROJECTION","","",p.projection_id,p.use_id,p.reference_id,p.relationship_id,p.source_alias,
                DAYE_HuntSideToString(p.side),p.hunter_canonical_symbol,p.protected_canonical_symbol,IntegerToString(p.target_chart_id),
                EnumToString(p.target_chart_timeframe),p.line_object_name,p.text_object_name,DAYE_RenderProjectionStatusToString(p.status),
                TimeToString(p.geometry.reference_time_utc,TIME_DATE|TIME_SECONDS),TimeToString(p.geometry.confirmation_time_utc,TIME_DATE|TIME_SECONDS),
                TimeToString(p.geometry.reference_time_broker,TIME_DATE|TIME_SECONDS),TimeToString(p.geometry.confirmation_time_broker,TIME_DATE|TIME_SECONDS),
                DoubleToString(p.geometry.reference_price,8),DoubleToString(p.geometry.confirmation_price,8),
                TimeToString(p.event_time_utc,TIME_DATE|TIME_SECONDS),TimeToString(p.availability_time_utc,TIME_DATE|TIME_SECONDS),
                TimeToString(p.processing_time_utc,TIME_DATE|TIME_SECONDS),p.reason_code);
   }
   void WriteEvent(const DAYE_RenderEvent &e)
   {
      if(!m_enabled || m_handle==INVALID_HANDLE) return;
      FileWrite(m_handle,e.schema_version,"EVENT",e.event_id,DAYE_RenderEventTypeToString(e.event_type),e.projection_id,e.use_id,"","","","","","",
                IntegerToString(e.target_chart_id),"",e.object_name,"",DAYE_RenderProjectionStatusToString(e.to_status),"","","","","","",
                TimeToString(e.event_time_utc,TIME_DATE|TIME_SECONDS),TimeToString(e.availability_time_utc,TIME_DATE|TIME_SECONDS),
                TimeToString(e.processing_time_utc,TIME_DATE|TIME_SECONDS),e.reason_code);
   }
   void WriteSummary(const DAYE_RenderStoreSummary &s)
   {
      if(!m_enabled || m_handle==INVALID_HANDLE) return;
      FileWrite(m_handle,s.schema_version,"SUMMARY","","","","","","","","","","","","","","",DAYE_RenderEngineStatusToString(s.status),
                "","","","","","",TimeToString(s.event_time_utc,TIME_DATE|TIME_SECONDS),
                TimeToString(s.availability_time_utc,TIME_DATE|TIME_SECONDS),TimeToString(s.processing_time_utc,TIME_DATE|TIME_SECONDS),s.reason_code);
   }
   void Flush(void) { if(m_enabled && m_handle!=INVALID_HANDLE) FileFlush(m_handle); }
   void Close(void) { if(m_handle!=INVALID_HANDLE) FileClose(m_handle); m_handle=INVALID_HANDLE; m_enabled=false; }
};

#endif
