#ifndef __FP_FINAL_CSV_NORMALIZATION_RULES_MQH__
#define __FP_FINAL_CSV_NORMALIZATION_RULES_MQH__
#property strict

#include "FP_FinalCsvNormalizationTypes.mqh"
#include "FP_FinalDecisionStateRules.mqh"

string FP_C04Time(const datetime t){ if(t <= 0) return ""; return TimeToString(t, TIME_DATE|TIME_SECONDS); }
string FP_C04SafeCsv(string v){ StringReplace(v, "\"", "\"\""); return "\"" + v + "\""; }
string FP_C04TfLabel(const ENUM_TIMEFRAMES tf){ return EnumToString(tf); }
int FP_C04BoolI(const bool v){ return (v ? 1 : 0); }

double FP_C04AbsDouble(const double v)
{
   if(v < 0.0) return -v;
   return v;
}

int FP_C04DirectionSign(const string direction_label)
{
   if(direction_label == "DIRECTION_BULLISH")
      return 1;
   if(direction_label == "DIRECTION_BEARISH")
      return -1;
   return 0;
}

double FP_C04RiskDistance(const string direction_label,
                          const double entry_price,
                          const double stop_price)
{
   if(entry_price <= 0.0 || stop_price <= 0.0)
      return 0.0;
   return FP_C04AbsDouble(entry_price - stop_price);
}

double FP_C04RewardDistance(const string direction_label,
                            const double entry_price,
                            const double target_price)
{
   if(entry_price <= 0.0 || target_price <= 0.0)
      return 0.0;
   return FP_C04AbsDouble(target_price - entry_price);
}

string FP_C04FirstBlockReason(const FP_Consolidation04FinalCsvNormalizationConfig &cfg,
                              const FP_Consolidation04FinalCsvNormalizationRow &row)
{
   if(cfg.require_no_send_integrity && row.no_send_integrity_i <= 0)
      return "BLOCK_NORMALIZED_NO_SEND_INTEGRITY_BROKEN";
   return "none";
}

void FP_C04BuildFinalCsvNormalizationRow(const string symbol,
                                         const ENUM_TIMEFRAMES period,
                                         const FP_Consolidation02FinalDecisionRow &final_row,
                                         const FP_Consolidation04FinalCsvNormalizationConfig &cfg,
                                         FP_Consolidation04FinalCsvNormalizationRow &row)
{
   FP_ResetConsolidation04FinalCsvNormalizationRow(row);

   row.generated_at = TimeCurrent();
   row.symbol = symbol;
   row.period = period;
   row.period_label = FP_C04TfLabel(period);

   row.attempted_i = FP_C04BoolI(cfg.enabled);
   row.decision_ready_i = FP_C04BoolI(final_row.decision_ready);
   row.context_ready_i = FP_C04BoolI(final_row.context_ready);
   row.no_send_integrity_i = FP_C04BoolI(final_row.no_send_integrity_ok);

   row.entry_bridge_ready_i = FP_C04BoolI(final_row.entry_bridge_ready);
   row.paper_intent_allowed_i = FP_C04BoolI(final_row.paper_intent_allowed);
   row.safety_gate_passed_i = FP_C04BoolI(final_row.safety_gate_passed);
   row.dry_run_request_built_i = FP_C04BoolI(final_row.dry_run_request_built);
   row.validator_passed_i = FP_C04BoolI(final_row.validator_passed);
   row.audit_passed_i = FP_C04BoolI(final_row.audit_passed);
   row.adapter_registered_i = FP_C04BoolI(final_row.adapter_registered);
   row.lifecycle_tracked_i = FP_C04BoolI(final_row.lifecycle_tracked);

   row.decision_state = final_row.decision_state;
   row.decision_block_reason = final_row.decision_block_reason;
   row.setup_state = final_row.setup_state;
   row.chain_stage = final_row.chain_stage;
   row.next_action_hint = final_row.next_action_hint;
   row.blocker_layer = final_row.blocker_layer;
   row.blocker_reason = final_row.blocker_reason;

   row.request_id = final_row.request_id;
   row.request_key = final_row.request_key;
   row.virtual_ticket = final_row.virtual_ticket;

   row.direction_label = final_row.request_direction;
   row.direction_sign = FP_C04DirectionSign(final_row.request_direction);

   row.entry_price = final_row.entry_price;
   row.stop_price = final_row.stop_price;
   row.target_price = final_row.target_price;
   row.request_volume = final_row.request_volume;

   row.risk_distance = FP_C04RiskDistance(row.direction_label, row.entry_price, row.stop_price);
   row.reward_distance = FP_C04RewardDistance(row.direction_label, row.entry_price, row.target_price);
   if(row.risk_distance > 0.0)
      row.rr_like = row.reward_distance / row.risk_distance;

   row.lifecycle_status = final_row.lifecycle_status;
   row.paper_order_state = final_row.paper_order_state;
   row.realized_r_like = final_row.realized_r_like;

   string block = FP_C04FirstBlockReason(cfg, row);
   if(block == "none")
   {
      row.normalized_quality_status = "FINAL_CSV_NORMALIZED_READY";
      row.normalized_block_reason = "none";
   }
   else
   {
      row.normalized_quality_status = "FINAL_CSV_NORMALIZED_BLOCKED";
      row.normalized_block_reason = block;
   }
}

#endif // __FP_FINAL_CSV_NORMALIZATION_RULES_MQH__
