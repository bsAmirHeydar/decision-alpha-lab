//+------------------------------------------------------------------+
//| CGP13_Display.mqh                                                |
//| Phase 13 — Compact terminal summary                              |
//+------------------------------------------------------------------+
#property strict

#ifndef __CGP13_DISPLAY_MQH__
#define __CGP13_DISPLAY_MQH__

#include <IntermarketDivergenceExecution/CG/CGP13_Types.mqh>

class CCGP13_Display
{
public:
   string SummaryText(const SCGP13Summary &s)
   {
      return StringFormat("EXP0017 Phase13 bridge | status=%s | integrity=%s | files=%d/%d | required_missing=%d | python_allowed=%s",
         s.status,s.integrity_status,s.files_found,s.files_expected,s.required_missing,(s.python_run_allowed?"true":"false"));
   }

   void Publish(const SCGP13Summary &s,const bool show_comment,const bool print_summary)
   {
      string text=SummaryText(s);
      if(show_comment) Comment(text);
      else Comment("");
      if(print_summary) Print(text);
   }
};

#endif
