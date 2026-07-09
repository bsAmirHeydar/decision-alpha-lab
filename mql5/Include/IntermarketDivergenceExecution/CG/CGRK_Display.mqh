//+------------------------------------------------------------------+
//| CGRK_Display.mqh                                                 |
//| Phase 09 — Compact dashboard comment                             |
//+------------------------------------------------------------------+
#property strict

#ifndef __CGRK_DISPLAY_MQH__
#define __CGRK_DISPLAY_MQH__

#include <IntermarketDivergenceExecution/CG/CGRK_Types.mqh>

class CCGRK_Display
{
public:
   void Show(const SCGRKReportRow &rows[], const int loaded_rows, const int ranked_rows, const int shortlist_rows, const SCGRKConfig &cfg)
   {
      if(!cfg.show_dashboard_comment)
      {
         Comment("");
         return;
      }

      string text = "EXP0017 Phase 09 — Statistical Ranking Dashboard\n";
      text += "Loaded rows: " + IntegerToString(loaded_rows) + "\n";
      text += "Ranked rows: " + IntegerToString(ranked_rows) + "\n";
      text += "Shortlist rows: " + IntegerToString(shortlist_rows) + "\n";
      text += "Min sample ranking: " + IntegerToString(cfg.minimum_sample_for_ranking) + "\n";
      text += "No execution / no filter / no strategy mutation\n\n";

      int shown = 0;
      for(int i=0; i<ArraySize(rows) && shown<10; i++)
      {
         if(!rows[i].eligible_for_ranking) continue;
         shown++;
         text += IntegerToString(shown) + ". " + rows[i].report_name + " | " + rows[i].bucket_key +
                 " | Q=" + DoubleToString(rows[i].quality_score,1) +
                 " | WR=" + DoubleToString(rows[i].win_rate_percent,1) +
                 " | R=" + DoubleToString(rows[i].avg_r,3) +
                 " | grade=" + rows[i].grade + "\n";
      }

      Comment(text);
   }
};

#endif
