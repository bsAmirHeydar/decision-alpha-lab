//+------------------------------------------------------------------+
//| CGM_Display.mqh                                                  |
//| Phase 10 — Compact display                                       |
//+------------------------------------------------------------------+
#property strict

#ifndef __CGM_DISPLAY_MQH__
#define __CGM_DISPLAY_MQH__

#include <IntermarketDivergenceExecution/CG/CGM_Types.mqh>

class CCGM_Display
{
public:
   string SummaryText(const SCGMSummary &s,const SCGMConfig &cfg)
   {
      string txt = "EXP0017 Phase 10 — Model Dataset\n";
      txt += "outcomes_loaded=" + IntegerToString(s.outcomes_loaded) + "\n";
      txt += "rank_rows_loaded=" + IntegerToString(s.rank_rows_loaded) + " shortlist_rows_loaded=" + IntegerToString(s.shortlist_rows_loaded) + "\n";
      txt += "rows_written=" + IntegerToString(s.rows_written) + " excluded=" + IntegerToString(s.rows_excluded) + "\n";
      txt += "wins=" + IntegerToString(s.win_rows) + " losses=" + IntegerToString(s.loss_rows) + " flats=" + IntegerToString(s.flat_rows) + " avg_primary_r=" + DoubleToString(s.avg_primary_r,4) + "\n";
      txt += "dataset=" + cfg.output_dataset_file;
      return txt;
   }

   void PrintSummary(const SCGMSummary &s,const SCGMConfig &cfg)
   {
      Print(SummaryText(s,cfg));
   }

   void CommentSummary(const SCGMSummary &s,const SCGMConfig &cfg)
   {
      Comment(SummaryText(s,cfg));
   }
};

#endif
