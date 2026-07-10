#ifndef __EXP0018_DAYE_ENGINE_MQH__
#define __EXP0018_DAYE_ENGINE_MQH__

#include <DayeTrader/EXP0018/DAYE_TimeAudit.mqh>
#include <DayeTrader/EXP0018/DAYE_TimeSelfTest.mqh>

class CDayeTimeKernelEngine
{
private:
   DAYE_TimeConfig m_config;
   DAYE_PeriodDefinition m_periods[];
   DAYE_TimeSnapshot m_previous_snapshot;
   bool m_has_previous_snapshot;
   datetime m_last_printed_utc_minute;
   bool m_initialized;
   CDayeTimeAuditWriter m_audit;

public:
   CDayeTimeKernelEngine(void)
   {
      ZeroMemory(m_previous_snapshot);
      m_has_previous_snapshot = false;
      m_last_printed_utc_minute = 0;
      m_initialized = false;
   }

   bool Initialize(const DAYE_TimeConfig &config,const bool print_registry,const bool run_self_tests,const bool write_audit_csv,const string audit_filename)
   {
      string reason = "";
      if(!DAYE_ValidateTimeConfig(config,reason))
      {
         Print("EXP0018 P01 initialization failed reason=",reason);
         return false;
      }
      if(run_self_tests && !DAYE_RunEmbeddedTimeSelfTests())
      {
         Print("EXP0018 P01 initialization blocked because embedded self-test failed.");
         return false;
      }

      m_config = config;
      DAYE_BuildCanonicalPeriodRegistry(m_periods);
      if(print_registry)
         DAYE_PrintPeriodRegistry(m_periods);
      if(!m_audit.Open(audit_filename,write_audit_csv))
         return false;

      m_initialized = true;
      Print("EXP0018 P01 New York Time Kernel v2 initialized. Weekly remains unavailable until ADR-DY-A03 is accepted. No signal, drawing, risk, or order authority exists.");
      return true;
   }

   bool Process(const datetime broker_time,const bool print_on_minute_change,const bool print_events,const bool show_chart_comment,const bool write_snapshot_rows)
   {
      if(!m_initialized)
         return false;

      DAYE_TimeSnapshot current;
      if(!DAYE_BuildTimeSnapshot(broker_time,m_config,m_periods,current))
      {
         Print("EXP0018 P01 snapshot failed status=",DAYE_StatusCodeToString(current.status)," reason=",current.reason_code," broker=",DAYE_FormatDateTime(broker_time));
         return false;
      }

      datetime processing_time_utc = TimeGMT();
      if(processing_time_utc <= 0)
         processing_time_utc = current.utc_time;

      DAYE_TimeEvent events[];
      DAYE_DetectTimeTransitions(m_has_previous_snapshot,m_previous_snapshot,current,processing_time_utc,events);
      for(int i=0;i<ArraySize(events);i++)
      {
         if(print_events)
            DAYE_PrintTimeEvent(events[i]);
         if(!m_audit.WriteEvent(events[i]))
            Print("EXP0018 P01 audit event write failed id=",events[i].event_id);
      }

      datetime utc_minute = current.utc_time - (current.utc_time % 60);
      bool should_print = (!print_on_minute_change || utc_minute != m_last_printed_utc_minute);
      string summary = DAYE_FormatSnapshot(current);
      if(should_print)
      {
         Print(summary);
         Print("  ",DAYE_FormatWindow(current.trading_day_window));
         Print("  ",DAYE_FormatWindow(current.session_window));
         if(!current.in_declared_session_gap)
            Print("  ",DAYE_FormatWindow(current.subcycle_window));
         m_last_printed_utc_minute = utc_minute;
         if(write_snapshot_rows && !m_audit.WriteSnapshot(current,processing_time_utc))
            Print("EXP0018 P01 audit snapshot write failed utc=",DAYE_FormatDateTime(current.utc_time));
      }

      if(show_chart_comment)
      {
         string detail = summary + "\n" + DAYE_FormatWindow(current.trading_day_window) + "\n" + DAYE_FormatWindow(current.session_window);
         if(!current.in_declared_session_gap)
            detail += "\n" + DAYE_FormatWindow(current.subcycle_window);
         detail += "\nTime kernel only — no signals or trading.";
         Comment(detail);
      }
      else
         Comment("");

      m_previous_snapshot = current;
      m_has_previous_snapshot = true;
      return true;
   }

   void Shutdown(void)
   {
      Comment("");
      m_audit.Close();
      ArrayResize(m_periods,0);
      ZeroMemory(m_previous_snapshot);
      m_has_previous_snapshot = false;
      m_initialized = false;
   }
};

#endif
