
#ifndef __EXP0018_DAYE_PERIOD_AUDIT_MQH__
#define __EXP0018_DAYE_PERIOD_AUDIT_MQH__

#include <DayeTrader/EXP0018/DAYE_PeriodDiagnostics.mqh>

class CDayePeriodAuditWriter
{
private:
   int m_handle;
   bool m_enabled;

public:
   CDayePeriodAuditWriter(void)
   {
      m_handle = INVALID_HANDLE;
      m_enabled = false;
   }

   bool Open(const string filename,const bool enabled)
   {
      m_enabled = enabled;
      if(!m_enabled) return true;
      ResetLastError();
      m_handle = FileOpen(filename,FILE_WRITE|FILE_CSV|FILE_ANSI|FILE_COMMON,',');
      if(m_handle == INVALID_HANDLE)
      {
         Print("EXP0018 P03 audit open failed file=",filename," error=",GetLastError());
         return false;
      }
      FileWrite(m_handle,
                "schema_version","record_type","event_id","event_type","status","reason_code",
                "event_time_utc","availability_time_utc","processing_time_utc",
                "paired_period_id","period_instance_id","period_family","period_code","trading_day_key",
                "start_utc","end_utc","completeness","publishable",
                "expected_aligned","aligned","unmatched_a","unmatched_b","aligned_coverage_percent",
                "symbol_a","a_completeness","a_observed","a_expected","a_open","a_high","a_low","a_close",
                "symbol_b","b_completeness","b_observed","b_expected","b_open","b_high","b_low","b_close",
                "previous_chronological","previous_same_code");
      FileFlush(m_handle);
      return true;
   }

   bool WriteSummary(const DAYE_PeriodStoreSummary &s)
   {
      if(!m_enabled) return true;
      if(m_handle == INVALID_HANDLE) return false;
      FileWrite(m_handle,
                s.schema_version,"SUMMARY","","",DAYE_PeriodAggregateStatusToString(s.status),s.reason_code,
                DAYE_PeriodFormatDateTime(s.source_last_event_time_utc),DAYE_PeriodFormatDateTime(s.availability_time_utc),DAYE_PeriodFormatDateTime(s.processing_time_utc),
                s.latest_paired_period_id,"","","","","","","","",
                "",s.source_aligned_pairs,s.source_unmatched_a,s.source_unmatched_b,"",
                "","",s.symbol_period_count_a,"","","","","",
                "","",s.symbol_period_count_b,"","","","","",
                "","");
      FileFlush(m_handle);
      return true;
   }

   bool WriteEvent(const DAYE_PeriodAggregateEvent &e)
   {
      if(!m_enabled) return true;
      if(m_handle == INVALID_HANDLE) return false;
      FileWrite(m_handle,
                e.schema_version,"EVENT",e.event_id,DAYE_PeriodAggregateEventTypeToString(e.event_type),DAYE_PeriodAggregateStatusToString(e.to_status),e.reason_code,
                DAYE_PeriodFormatDateTime(e.event_time_utc),DAYE_PeriodFormatDateTime(e.availability_time_utc),DAYE_PeriodFormatDateTime(e.processing_time_utc),
                "",e.period_instance_id,"","","","","","","",
                "","","","","",
                "","","","","","","","",
                "","","","","","","","",
                "","");
      FileFlush(m_handle);
      return true;
   }

   bool WritePeriod(const DAYE_PairedPeriodSnapshot &p)
   {
      if(!m_enabled) return true;
      if(m_handle == INVALID_HANDLE) return false;
      FileWrite(m_handle,
                p.schema_version,"PERIOD","","",DAYE_PeriodAggregateStatusToString(p.status),p.reason_code,
                DAYE_PeriodFormatDateTime(p.event_time_utc),DAYE_PeriodFormatDateTime(p.availability_time_utc),DAYE_PeriodFormatDateTime(p.processing_time_utc),
                p.paired_period_id,p.period_instance_id,DAYE_PeriodFamilyToString(p.period_family),p.period_code,p.trading_day_key,
                DAYE_PeriodFormatDateTime(p.window.start_utc),DAYE_PeriodFormatDateTime(p.window.end_utc),DAYE_PeriodCompletenessToString(p.completeness),p.is_publishable ? 1 : 0,
                p.expected_aligned_bar_count,p.aligned_bar_count,p.unmatched_a_count,p.unmatched_b_count,p.aligned_coverage_percent,
                p.symbol_a.canonical_symbol,DAYE_PeriodCompletenessToString(p.symbol_a.completeness),p.symbol_a.observed_bar_count,p.symbol_a.expected_bar_count,p.symbol_a.open,p.symbol_a.high,p.symbol_a.low,p.symbol_a.close,
                p.symbol_b.canonical_symbol,DAYE_PeriodCompletenessToString(p.symbol_b.completeness),p.symbol_b.observed_bar_count,p.symbol_b.expected_bar_count,p.symbol_b.open,p.symbol_b.high,p.symbol_b.low,p.symbol_b.close,
                p.previous_chronological_paired_period_id,p.previous_same_code_paired_period_id);
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
