#ifndef __EXP0018_DAYE_TIME_AUDIT_MQH__
#define __EXP0018_DAYE_TIME_AUDIT_MQH__

#include <DayeTrader/EXP0018/DAYE_TimeEvents.mqh>

class CDayeTimeAuditWriter
{
private:
   int m_handle;
   string m_filename;
   bool m_enabled;

public:
   CDayeTimeAuditWriter(void)
   {
      m_handle = INVALID_HANDLE;
      m_filename = "";
      m_enabled = false;
   }

   bool Open(const string filename,const bool enabled)
   {
      m_enabled = enabled;
      m_filename = filename;
      if(!m_enabled)
         return true;

      ResetLastError();
      m_handle = FileOpen(m_filename,FILE_READ|FILE_WRITE|FILE_CSV|FILE_ANSI|FILE_COMMON,',');
      if(m_handle == INVALID_HANDLE)
      {
         Print("EXP0018 P01 audit open failed file=",m_filename," error=",GetLastError());
         return false;
      }
      if(FileSize(m_handle) == 0)
      {
         FileWrite(m_handle,
                   "schema_version","record_type","event_id","event_type","event_time_utc","availability_time_utc","processing_time_utc",
                   "broker_time","utc_time","new_york_time","ny_offset_minutes","ny_dst","ny_fold","trading_day_key","session","subcycle",
                   "from_period","to_period","reason_code");
         FileFlush(m_handle);
      }
      FileSeek(m_handle,0,SEEK_END);
      return true;
   }

   bool WriteSnapshot(const DAYE_TimeSnapshot &snapshot,const datetime processing_time_utc)
   {
      if(!m_enabled)
         return true;
      if(m_handle == INVALID_HANDLE)
         return false;
      FileWrite(m_handle,
                snapshot.schema_version,"SNAPSHOT","","",IntegerToString((long)snapshot.utc_time),IntegerToString((long)snapshot.utc_time),IntegerToString((long)processing_time_utc),
                IntegerToString((long)snapshot.broker_time),IntegerToString((long)snapshot.utc_time),IntegerToString((long)snapshot.new_york_time),
                snapshot.new_york_utc_offset_minutes,(snapshot.is_new_york_dst ? 1 : 0),snapshot.new_york_fold,snapshot.trading_day_key,
                DAYE_PeriodIdToString(snapshot.session_id),DAYE_PeriodIdToString(snapshot.subcycle_id),"","",snapshot.reason_code);
      FileFlush(m_handle);
      return true;
   }

   bool WriteEvent(const DAYE_TimeEvent &event)
   {
      if(!m_enabled)
         return true;
      if(m_handle == INVALID_HANDLE)
         return false;
      FileWrite(m_handle,
                event.schema_version,"EVENT",event.event_id,DAYE_TimeEventTypeToString(event.event_type),
                IntegerToString((long)event.event_time_utc),IntegerToString((long)event.availability_time_utc),IntegerToString((long)event.processing_time_utc),
                "","","","","","",event.trading_day_key,"","",
                DAYE_PeriodIdToString(event.from_period_id),DAYE_PeriodIdToString(event.to_period_id),event.reason_code);
      FileFlush(m_handle);
      return true;
   }

   void Close(void)
   {
      if(m_handle != INVALID_HANDLE)
      {
         FileClose(m_handle);
         m_handle = INVALID_HANDLE;
      }
      m_enabled = false;
   }
};

#endif
