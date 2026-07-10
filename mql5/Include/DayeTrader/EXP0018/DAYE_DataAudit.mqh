
#ifndef __EXP0018_DAYE_DATA_AUDIT_MQH__
#define __EXP0018_DAYE_DATA_AUDIT_MQH__

#include <DayeTrader/EXP0018/DAYE_DataDiagnostics.mqh>

class CDayeDataAuditWriter
{
private:
   int m_handle;
   bool m_enabled;

public:
   CDayeDataAuditWriter(void)
   {
      m_handle = INVALID_HANDLE;
      m_enabled = false;
   }

   bool Open(const string filename,const bool enabled)
   {
      m_enabled = enabled;
      if(!m_enabled)
         return true;
      ResetLastError();
      m_handle = FileOpen(filename,FILE_WRITE|FILE_CSV|FILE_ANSI|FILE_COMMON,',');
      if(m_handle == INVALID_HANDLE)
      {
         Print("EXP0018 P02 audit open failed file=",filename," error=",GetLastError());
         return false;
      }
      FileWrite(m_handle,
                "schema_version","record_type","event_id","event_type",
                "event_time_utc","availability_time_utc","processing_time_utc",
                "status","reason_code","pair_id","timeframe",
                "symbol_a","symbol_b","event_bar_utc","aligned_count",
                "unmatched_a","unmatched_b","a_open","a_high","a_low","a_close",
                "b_open","b_high","b_low","b_close");
      FileFlush(m_handle);
      return true;
   }

   bool WriteSummary(const DAYE_DataSyncSummary &summary)
   {
      if(!m_enabled)
         return true;
      if(m_handle == INVALID_HANDLE)
         return false;
      FileWrite(m_handle,
                summary.schema_version,"SUMMARY","","",
                "",DAYE_DataFormatDateTime(summary.availability_time_utc),DAYE_DataFormatDateTime(summary.processing_time_utc),
                DAYE_DataStatusCodeToString(summary.status),summary.reason_code,"",EnumToString(summary.timeframe),
                summary.broker_symbol_a,summary.broker_symbol_b,DAYE_DataFormatDateTime(summary.last_common_event_time_utc),summary.aligned_count,
                summary.unmatched_a,summary.unmatched_b,"","","","","","","","");
      FileFlush(m_handle);
      return true;
   }

   bool WriteEvent(const DAYE_DataSyncEvent &event)
   {
      if(!m_enabled)
         return true;
      if(m_handle == INVALID_HANDLE)
         return false;
      FileWrite(m_handle,
                event.schema_version,"EVENT",event.event_id,DAYE_DataEventTypeToString(event.event_type),
                DAYE_DataFormatDateTime(event.event_time_utc),DAYE_DataFormatDateTime(event.availability_time_utc),DAYE_DataFormatDateTime(event.processing_time_utc),
                DAYE_DataStatusCodeToString(event.to_status),event.reason_code,"","",
                "","",DAYE_DataFormatDateTime(event.latest_common_event_time_utc),"","","",
                "","","","","","","","");
      FileFlush(m_handle);
      return true;
   }

   bool WritePair(const DAYE_SynchronizedBarPair &pair)
   {
      if(!m_enabled)
         return true;
      if(m_handle == INVALID_HANDLE)
         return false;
      FileWrite(m_handle,
                pair.schema_version,"PAIR","","",
                DAYE_DataFormatDateTime(pair.event_time_utc),DAYE_DataFormatDateTime(pair.availability_time_utc),DAYE_DataFormatDateTime(pair.processing_time_utc),
                DAYE_DataStatusCodeToString(pair.status),pair.reason_code,pair.pair_id,EnumToString(pair.timeframe),
                pair.symbol_a.broker_symbol,pair.symbol_b.broker_symbol,DAYE_DataFormatDateTime(pair.event_time_utc),"","","",
                pair.symbol_a.open,pair.symbol_a.high,pair.symbol_a.low,pair.symbol_a.close,
                pair.symbol_b.open,pair.symbol_b.high,pair.symbol_b.low,pair.symbol_b.close);
      FileFlush(m_handle);
      return true;
   }

   void Close(void)
   {
      if(m_handle != INVALID_HANDLE)
      {
         FileFlush(m_handle);
         FileClose(m_handle);
      }
      m_handle = INVALID_HANDLE;
      m_enabled = false;
   }
};

#endif
