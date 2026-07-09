//+------------------------------------------------------------------+
//| CGS_Display.mqh                                                  |
//| EXP0017 Phase 08 — Compact Display                              |
//+------------------------------------------------------------------+
#ifndef __EXP0017_CGS_DISPLAY_MQH__
#define __EXP0017_CGS_DISPLAY_MQH__

#include <IntermarketDivergenceExecution/CG/CGS_Types.mqh>

class CCGS_Display
{
private:
   string m_last_text;

public:
   void SetText(const string text)
   {
      m_last_text = text;
   }

   void ShowIfEnabled(const bool enabled)
   {
      if(enabled)
         Comment(m_last_text);
   }

   string BuildSummary(const SCGSReportConfig &cfg,const int sample_count,const int report_count,const datetime run_time)
   {
      string t = "EXP0017 Phase 08 — Statistical Report Engine\n";
      t += "Outcome CSV: " + cfg.outcome_file + "\n";
      t += "Report prefix: " + cfg.report_prefix + "\n";
      t += "Primary window: " + CGS_WindowName(cfg.primary_window) + "\n";
      t += "Samples read: " + IntegerToString(sample_count) + "\n";
      t += "Reports written: " + IntegerToString(report_count) + "\n";
      t += "Last run: " + TimeToString(run_time, TIME_DATE|TIME_SECONDS) + "\n";
      t += "Boundary: reports only; no trading; no strategy mutation.";
      return t;
   }
};

#endif
