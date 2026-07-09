//+------------------------------------------------------------------+
//| CGRK_Ranker.mqh                                                  |
//| Phase 09 — Ranking and scoring                                   |
//+------------------------------------------------------------------+
#property strict

#ifndef __CGRK_RANKER_MQH__
#define __CGRK_RANKER_MQH__

#include <IntermarketDivergenceExecution/CG/CGRK_Types.mqh>

class CCGRK_Ranker
{
private:
   double SafeWeightsSum(const SCGRKConfig &cfg)
   {
      double s = MathMax(0.0, cfg.weight_win_rate)
               + MathMax(0.0, cfg.weight_average_r)
               + MathMax(0.0, cfg.weight_normalized_outcome)
               + MathMax(0.0, cfg.weight_safety)
               + MathMax(0.0, cfg.weight_sample_confidence);
      if(s <= 0.0) return 1.0;
      return s;
   }

   string Grade(const double score)
   {
      if(score >= 80.0) return "A";
      if(score >= 70.0) return "B";
      if(score >= 60.0) return "C";
      if(score >= 50.0) return "D";
      return "F";
   }

public:
   void ScoreRows(SCGRKReportRow &rows[], const SCGRKConfig &cfg)
   {
      double wsum = SafeWeightsSum(cfg);
      int n = ArraySize(rows);

      for(int i=0; i<n; i++)
      {
         rows[i].eligible_for_ranking = (rows[i].valid && rows[i].sample_count >= cfg.minimum_sample_for_ranking);

         rows[i].sample_confidence_score = CGRK_Clamp(100.0 * ((double)rows[i].sample_count / (double)MathMax(1, cfg.minimum_sample_for_ranking)), 0.0, 100.0);
         rows[i].win_rate_score          = CGRK_Clamp(rows[i].win_rate_percent, 0.0, 100.0);
         rows[i].expectancy_score        = CGRK_Clamp(50.0 + rows[i].avg_r * 50.0, 0.0, 100.0);
         rows[i].normalized_score        = CGRK_Clamp(50.0 + rows[i].avg_normalized * 100.0, 0.0, 100.0);
         rows[i].safety_score            = CGRK_Clamp(100.0 - rows[i].stop_rate_percent - (double)rows[i].max_stop_streak * 4.0, 0.0, 100.0);

         rows[i].quality_score =
            (rows[i].win_rate_score          * MathMax(0.0, cfg.weight_win_rate) +
             rows[i].expectancy_score        * MathMax(0.0, cfg.weight_average_r) +
             rows[i].normalized_score        * MathMax(0.0, cfg.weight_normalized_outcome) +
             rows[i].safety_score            * MathMax(0.0, cfg.weight_safety) +
             rows[i].sample_confidence_score * MathMax(0.0, cfg.weight_sample_confidence)) / wsum;

         rows[i].opportunity_score = CGRK_Clamp(50.0 + rows[i].avg_mfe_r * 35.0, 0.0, 100.0);
         rows[i].stability_score   = CGRK_Clamp(100.0 - MathAbs(rows[i].avg_mae_r) * 25.0 - rows[i].max_stop_streak * 3.0, 0.0, 100.0);
         rows[i].grade             = rows[i].eligible_for_ranking ? Grade(rows[i].quality_score) : "UNRANKED";

         rows[i].red_flag_text = "";
         if(rows[i].sample_count < cfg.minimum_sample_for_ranking)
            rows[i].red_flag_text += "low_sample;";
         if(rows[i].win_rate_percent < cfg.minimum_win_rate_for_shortlist)
            rows[i].red_flag_text += "weak_win_rate;";
         if(rows[i].avg_r < cfg.minimum_average_r_for_shortlist)
            rows[i].red_flag_text += "negative_or_flat_avg_r;";
         if(rows[i].max_stop_streak > cfg.maximum_stop_streak_for_shortlist)
            rows[i].red_flag_text += "stop_streak_risk;";

         rows[i].eligible_for_shortlist =
            rows[i].eligible_for_ranking &&
            rows[i].sample_count >= cfg.minimum_sample_for_shortlist &&
            rows[i].quality_score >= cfg.minimum_quality_score_for_shortlist &&
            rows[i].win_rate_percent >= cfg.minimum_win_rate_for_shortlist &&
            rows[i].avg_r >= cfg.minimum_average_r_for_shortlist &&
            rows[i].max_stop_streak <= cfg.maximum_stop_streak_for_shortlist;

         if(rows[i].eligible_for_shortlist)
            rows[i].recommendation_text = "research_shortlist_candidate_not_execution_rule";
         else if(rows[i].eligible_for_ranking)
            rows[i].recommendation_text = "ranked_observation_not_execution_rule";
         else
            rows[i].recommendation_text = "insufficient_sample_not_ranked";
      }
   }

   void SortByQualityDescending(SCGRKReportRow &rows[])
   {
      int n = ArraySize(rows);
      for(int i=0; i<n-1; i++)
      {
         int best = i;
         for(int j=i+1; j<n; j++)
         {
            if(rows[j].quality_score > rows[best].quality_score)
               best = j;
         }
         if(best != i)
         {
            SCGRKReportRow tmp = rows[i];
            rows[i] = rows[best];
            rows[best] = tmp;
         }
      }
   }
};

#endif
