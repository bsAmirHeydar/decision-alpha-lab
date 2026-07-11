#ifndef __SF12_VALIDATION_GATE_MQH__
#define __SF12_VALIDATION_GATE_MQH__
#include "SF12_FoldObservation.mqh"
struct SF12_PromotionThresholds
{
   int minimum_oos_folds;long minimum_oos_samples;double minimum_positive_fold_share;double minimum_worst_fold_mean_r;
   double minimum_oos_to_is_ratio;double maximum_pbo;double minimum_deflated_probability;double maximum_reality_check_p;
   double minimum_surface_support;double minimum_best_trade_removed_mean_r;double minimum_stress_floor_mean_r;
};
struct SF12_ExternalDiagnostics
{
   double probability_of_backtest_overfitting;double deflated_probability;double reality_check_p;double surface_support;
   double stress_floor_mean_r;string diagnostics_hash;
};
struct SF12_GateResult
{
   string gate_id;ENUM_SF12_GATE_STATUS status;double observed_value;double threshold_value;string comparison;string reason_code;string evidence_hash;
};
struct SF12_PromotionDecision
{
   string schema;string decision_id;string plan_hash;string selected_trial_id;ENUM_SF12_PROMOTION_STATUS status;
   SF12_GateResult gates[];string rejection_reasons;string evidence_hashes;string decision_hash;
};
SF12_GateResult SF12_MakeGate(const string id,const bool passed,const double observed,const double threshold,const string comparison,const string failure_reason)
{
   SF12_GateResult g;g.gate_id=id;g.status=passed?SF12_GATE_PASS:SF12_GATE_FAIL;g.observed_value=observed;g.threshold_value=threshold;g.comparison=comparison;
   g.reason_code=passed?"PASS":failure_reason;g.evidence_hash=SF01_StableId("gateev",id+"|"+SF01_CanonicalDouble(observed)+"|"+comparison+"|"+SF01_CanonicalDouble(threshold));return g;
}
#endif
