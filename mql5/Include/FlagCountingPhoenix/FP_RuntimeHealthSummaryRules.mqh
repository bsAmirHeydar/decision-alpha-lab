#ifndef __FP_RUNTIME_HEALTH_SUMMARY_RULES_MQH__
#define __FP_RUNTIME_HEALTH_SUMMARY_RULES_MQH__
#property strict

#include "FP_RuntimeHealthSummaryTypes.mqh"
#include "FP_FinalCsvNormalizationRules.mqh"

string FP_C05Bool(const bool v){ return (v ? "true" : "false"); }
string FP_C05Time(const datetime t){ if(t <= 0) return ""; return TimeToString(t, TIME_DATE|TIME_SECONDS); }
string FP_C05SafeCsv(string v){ StringReplace(v, "\"", "\"\""); return "\"" + v + "\""; }
string FP_C05TfLabel(const ENUM_TIMEFRAMES tf){ return EnumToString(tf); }

bool FP_C05ExpectedOutputsEnabled(const FP_Consolidation05RuntimeHealthRow &row)
{
   return (row.context_export_enabled && row.final_decision_export_enabled && row.normalized_export_enabled);
}

string FP_C05FirstBlockReason(const FP_Consolidation05RuntimeHealthConfig &cfg,
                              const FP_Consolidation05RuntimeHealthRow &row)
{
   if(cfg.require_no_send_integrity && !row.no_send_integrity_ok)
      return "BLOCK_RUNTIME_NO_SEND_INTEGRITY_BROKEN";

   if(cfg.require_context_ready && !row.context_ready)
      return "BLOCK_RUNTIME_CONTEXT_NOT_READY";

   if(cfg.require_final_decision_export && !row.final_decision_export_enabled)
      return "BLOCK_RUNTIME_FINAL_DECISION_EXPORT_DISABLED";

   if(cfg.require_normalized_export && !row.normalized_export_enabled)
      return "BLOCK_RUNTIME_NORMALIZED_EXPORT_DISABLED";

   if(row.final_decision_state == "FINAL_DECISION_BLOCKED_NO_SEND")
      return "WARN_RUNTIME_FINAL_DECISION_BLOCKED:" + row.final_decision_block_reason;

   if(row.normalized_quality_status == "FINAL_CSV_NORMALIZED_BLOCKED")
      return "WARN_RUNTIME_NORMALIZED_BLOCKED:" + row.normalized_block_reason;

   return "none";
}

void FP_C05BuildRuntimeHealthRow(const string symbol,
                                 const ENUM_TIMEFRAMES period,
                                 const FP_Consolidation01NoSendContextConfig &context_cfg,
                                 const FP_Consolidation02FinalDecisionConfig &final_cfg,
                                 const FP_Consolidation04FinalCsvNormalizationConfig &normalization_cfg,
                                 const FP_Consolidation01NoSendContextRow &ctx,
                                 const FP_Consolidation02FinalDecisionRow &final_row,
                                 const FP_Consolidation04FinalCsvNormalizationRow &normalized_row,
                                 const FP_Consolidation05RuntimeHealthConfig &cfg,
                                 FP_Consolidation05RuntimeHealthRow &row)
{
   FP_ResetConsolidation05RuntimeHealthRow(row);

   row.generated_at = TimeCurrent();
   row.symbol = symbol;
   row.period = period;
   row.period_label = FP_C05TfLabel(period);
   row.attempted = cfg.enabled;

   row.context_enabled = context_cfg.enabled;
   row.context_export_enabled = (context_cfg.enabled && context_cfg.export_csv && context_cfg.write_latest_csv);
   row.context_ready = ctx.context_ready;
   row.context_status = ctx.context_status;
   row.context_block_reason = ctx.context_block_reason;

   row.final_decision_enabled = final_cfg.enabled;
   row.final_decision_export_enabled = (final_cfg.enabled && final_cfg.export_csv && final_cfg.write_latest_csv);
   row.final_decision_ready = final_row.decision_ready;
   row.final_decision_state = final_row.decision_state;
   row.final_decision_block_reason = final_row.decision_block_reason;

   row.normalized_enabled = normalization_cfg.enabled;
   row.normalized_export_enabled = (normalization_cfg.enabled && normalization_cfg.export_csv && normalization_cfg.write_latest_csv);
   row.normalized_ready = (normalized_row.normalized_quality_status == "FINAL_CSV_NORMALIZED_READY");
   row.normalized_quality_status = normalized_row.normalized_quality_status;
   row.normalized_block_reason = normalized_row.normalized_block_reason;

   row.no_send_integrity_ok = final_row.no_send_integrity_ok;

   row.expected_outputs_enabled_count = 0;
   if(row.context_export_enabled) row.expected_outputs_enabled_count++;
   if(row.final_decision_export_enabled) row.expected_outputs_enabled_count++;
   if(row.normalized_export_enabled) row.expected_outputs_enabled_count++;
   row.expected_outputs_required_count = 3;
   row.expected_outputs_enabled = FP_C05ExpectedOutputsEnabled(row);

   row.setup_state = final_row.setup_state;
   row.chain_stage = final_row.chain_stage;
   row.blocker_layer = final_row.blocker_layer;
   row.blocker_reason = final_row.blocker_reason;
   row.request_id = final_row.request_id;
   row.virtual_ticket = final_row.virtual_ticket;
   row.request_direction = final_row.request_direction;
   row.entry_price = final_row.entry_price;
   row.stop_price = final_row.stop_price;
   row.target_price = final_row.target_price;
   row.request_volume = final_row.request_volume;
   row.realized_r_like = final_row.realized_r_like;

   string block = FP_C05FirstBlockReason(cfg, row);

   if(block == "none")
   {
      row.health_ok = true;
      row.health_status = "RUNTIME_HEALTH_OK_NO_SEND";
      row.health_block_reason = "none";
   }
   else if(StringFind(block, "WARN_") == 0)
   {
      row.health_ok = true;
      row.health_status = "RUNTIME_HEALTH_WARN_NO_SEND";
      row.health_block_reason = block;
   }
   else
   {
      row.health_ok = false;
      row.health_status = "RUNTIME_HEALTH_BLOCKED_NO_SEND";
      row.health_block_reason = block;
   }

   row.health_key = row.symbol;
   row.health_key += "|TF=" + row.period_label;
   row.health_key += "|HEALTH=" + row.health_status;
   row.health_key += "|SETUP=" + row.setup_state;
   row.health_key += "|CHAIN=" + row.chain_stage;
   row.health_key += "|BLOCKER=" + row.blocker_layer;
   row.health_key += "|REQ=" + row.request_id;
   row.health_key += "|VT=" + row.virtual_ticket;
   row.health_key += "|EXEC=NO";
}

#endif // __FP_RUNTIME_HEALTH_SUMMARY_RULES_MQH__
