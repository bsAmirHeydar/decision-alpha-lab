//+------------------------------------------------------------------+
//| CGWF_Display.mqh                                                 |
//| Phase 11 — Compact display                                       |
//+------------------------------------------------------------------+
#property strict

#ifndef __CGWF_DISPLAY_MQH__
#define __CGWF_DISPLAY_MQH__

#include <IntermarketDivergenceExecution/CG/CGWF_Types.mqh>

class CCGWF_Display
{
public:
   void Show(const SCGWFSummary &s, const SCGWFConfig &cfg)
   {
      if(!cfg.show_chart_comment) return;
      string text = "EXP0017 Phase 11 — Walk-Forward Model Experiment\n";
      text += "Status: " + s.status + "\n";
      text += "Rows loaded: " + IntegerToString(s.rows_loaded) + "\n";
      text += "Rows accepted: " + IntegerToString(s.rows_after_filter) + "\n";
      text += "Folds: " + IntegerToString(s.folds_usable) + "/" + IntegerToString(s.folds_built) + " usable\n";
      text += "Predictions: " + IntegerToString(s.predictions_written) + "\n";
      text += "OOS avg R: " + DoubleToString(s.oos_avg_r,4) + "\n";
      text += "OOS win rate: " + DoubleToString(s.oos_win_rate,2) + "%\n";
      text += "Bucket key: " + CGWF_KeyModeToString(cfg.primary_bucket_key_mode) + "\n";
      text += "No trading / no mutation / research only";
      Comment(text);
   }

   void PrintSummary(const SCGWFSummary &s, const SCGWFConfig &cfg)
   {
      if(!cfg.print_summary) return;
      Print("EXP0017 Phase11 complete: status=",s.status,
            " rows_loaded=",s.rows_loaded,
            " rows_after_filter=",s.rows_after_filter,
            " folds_usable=",s.folds_usable,
            " predictions=",s.predictions_written,
            " oos_avg_r=",DoubleToString(s.oos_avg_r,6),
            " oos_win_rate=",DoubleToString(s.oos_win_rate,2));
   }
};

#endif
