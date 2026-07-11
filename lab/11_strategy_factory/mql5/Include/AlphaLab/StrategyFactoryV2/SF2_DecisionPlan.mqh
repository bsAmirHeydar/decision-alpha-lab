#ifndef __ALPHA_LAB_SF2_DECISION_PLAN_MQH__
#define __ALPHA_LAB_SF2_DECISION_PLAN_MQH__

#include "SF2_PluginInterfaces.mqh"
#include "SF2_LatencyBudget.mqh"

struct SF2_DecisionThresholds
  {
   double minimum_probability;
   double minimum_expected_r;
   double maximum_uncertainty;
   double minimum_utility_margin;
  };

struct SF2_DecisionPlan
  {
   string                 strategy_id;
   string                 strategy_version;
   string                 plan_hash;
   int                    max_candidates;
   SF2_DecisionThresholds thresholds;
   SF2_LatencyBudget      latency_budget;
   bool                   paper_only;
   bool                   abstain_on_missing_feature;
  };

#endif
