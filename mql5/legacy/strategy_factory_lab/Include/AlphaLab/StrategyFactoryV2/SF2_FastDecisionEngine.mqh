#ifndef __ALPHA_LAB_SF2_FAST_DECISION_ENGINE_MQH__
#define __ALPHA_LAB_SF2_FAST_DECISION_ENGINE_MQH__

#include "SF2_DecisionPlan.mqh"
#include "SF2_Telemetry.mqh"

class SF2_FastDecisionEngine
  {
private:
   SF2_DecisionPlan    m_plan;
   SF2_TelemetryBuffer m_telemetry;

public:
   void              Configure(const SF2_DecisionPlan &plan)
     {
      m_plan=plan;
     }

   bool              SelectBest(const SF2_CandidateScore &scores[],
                                const SF2_TradeCandidate &candidates[],
                                int &best_index,
                                string &reason_code) const
     {
      best_index=-1;
      reason_code="no_candidates";
      double best_utility=-DBL_MAX;
      double second_utility=-DBL_MAX;
      for(int i=0;i<ArraySize(scores);i++)
        {
         if(scores[i].probability_positive<m_plan.thresholds.minimum_probability)
            continue;
         if(scores[i].expected_net_r<m_plan.thresholds.minimum_expected_r)
            continue;
         if(m_plan.thresholds.maximum_uncertainty>0.0 &&
            scores[i].uncertainty>m_plan.thresholds.maximum_uncertainty)
            continue;
         if(scores[i].utility>best_utility)
           {
            second_utility=best_utility;
            best_utility=scores[i].utility;
            best_index=i;
           }
         else if(scores[i].utility>second_utility)
            second_utility=scores[i].utility;
        }
      if(best_index<0)
        {
         reason_code="threshold_abstention";
         return(false);
        }
      if(second_utility>-DBL_MAX &&
         best_utility-second_utility<m_plan.thresholds.minimum_utility_margin)
        {
         best_index=-1;
         reason_code="insufficient_margin";
         return(false);
        }
      if(best_index>=ArraySize(candidates))
        {
         best_index=-1;
         reason_code="candidate_score_mismatch";
         return(false);
        }
      reason_code="approved";
      return(true);
     }

   bool              IsPaperOnly(void) const { return(m_plan.paper_only); }
   string            PlanHash(void) const { return(m_plan.plan_hash); }
  };

#endif
