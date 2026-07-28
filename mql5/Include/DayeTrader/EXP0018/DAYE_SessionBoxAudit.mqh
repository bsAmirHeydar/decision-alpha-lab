#ifndef __EXP0018_DAYE_SESSION_BOX_AUDIT_MQH__
#define __EXP0018_DAYE_SESSION_BOX_AUDIT_MQH__

#include <DayeTrader/EXP0018/DAYE_SessionBoxDiagnostics.mqh>
#include <AlphaLab/UC04/AL_UC04CorePrimitives.mqh>

class CDayeSessionBoxAuditWriter
{
private:
   int m_handle;
   bool m_enabled;
public:
   CDayeSessionBoxAuditWriter(void) { m_handle=INVALID_HANDLE; m_enabled=false; }
   bool Open(const string filename,const bool enabled)
   {
      m_enabled=enabled;
      if(!enabled) return true;
      m_handle=FileOpen(filename,FILE_READ|FILE_WRITE|FILE_CSV|FILE_COMMON|FILE_ANSI,',');
      if(m_handle==INVALID_HANDLE) return false;
      if(FileSize(m_handle)==0)
         FileWrite(m_handle,"schema_version","record_type","event_id","event_type","projection_id","object_name","period_instance_id","trading_day_key","session_code","broker_symbol","canonical_symbol","chart_id","chart_timeframe","source_completeness","projection_status","start_utc","end_utc","start_broker","end_broker","high","low","event_time_utc","availability_time_utc","processing_time_utc","reason_code");
      FileSeek(m_handle,0,SEEK_END);
      return true;
   }
   void WriteProjection(const DAYE_SessionBoxProjection &p)
   {
      if(!m_enabled || m_handle==INVALID_HANDLE) return;
      FileWrite(m_handle,p.schema_version,"PROJECTION","","",p.projection_id,p.object_name,p.period_instance_id,p.trading_day_key,p.session_code,p.broker_symbol,p.canonical_symbol,IntegerToString(p.target_chart_id),EnumToString(p.target_chart_timeframe),DAYE_PeriodCompletenessToString(p.source_completeness),DAYE_SessionBoxProjectionStatusToString(p.status),TimeToString(p.geometry.start_time_utc,TIME_DATE|TIME_SECONDS),TimeToString(p.geometry.end_time_utc,TIME_DATE|TIME_SECONDS),TimeToString(p.geometry.start_time_broker,TIME_DATE|TIME_SECONDS),TimeToString(p.geometry.end_time_broker,TIME_DATE|TIME_SECONDS),DoubleToString(p.geometry.high_price,8),DoubleToString(p.geometry.low_price,8),TimeToString(p.event_time_utc,TIME_DATE|TIME_SECONDS),TimeToString(p.availability_time_utc,TIME_DATE|TIME_SECONDS),TimeToString(p.processing_time_utc,TIME_DATE|TIME_SECONDS),p.reason_code);
   }
   void WriteEvent(const DAYE_SessionBoxEvent &e)
   {
      if(!m_enabled || m_handle==INVALID_HANDLE) return;
      FileWrite(m_handle,e.schema_version,"EVENT",e.event_id,DAYE_SessionBoxEventTypeToString(e.event_type),e.projection_id,e.object_name,e.period_instance_id,"",e.session_code,e.broker_symbol,"",IntegerToString(e.target_chart_id),"","",DAYE_SessionBoxProjectionStatusToString(e.to_status),"","","","","","",TimeToString(e.event_time_utc,TIME_DATE|TIME_SECONDS),TimeToString(e.availability_time_utc,TIME_DATE|TIME_SECONDS),TimeToString(e.processing_time_utc,TIME_DATE|TIME_SECONDS),e.reason_code);
   }
   void WriteSummary(const DAYE_SessionBoxStoreSummary &s)
   {
      if(!m_enabled || m_handle==INVALID_HANDLE) return;
      FileWrite(m_handle,s.schema_version,"SUMMARY","","","","","","","","","","","","",DAYE_SessionBoxEngineStatusToString(s.status),"","","","","","",TimeToString(s.event_time_utc,TIME_DATE|TIME_SECONDS),TimeToString(s.availability_time_utc,TIME_DATE|TIME_SECONDS),TimeToString(s.processing_time_utc,TIME_DATE|TIME_SECONDS),s.reason_code);
   }
   void Flush(void) { if(m_enabled && m_handle!=INVALID_HANDLE) FileFlush(m_handle); }
   void Close(void) {
      AL_UC04CloseFileHandle(m_handle, m_enabled);
   }
};

#endif
