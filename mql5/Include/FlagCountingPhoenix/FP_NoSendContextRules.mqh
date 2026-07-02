#ifndef __FP_NO_SEND_CONTEXT_RULES_MQH__
#define __FP_NO_SEND_CONTEXT_RULES_MQH__
#property strict

#include "FP_NoSendContextTypes.mqh"
#include "FP_BrokerDryRunEngine.mqh"
#include "FP_BrokerValidatorEngine.mqh"
#include "FP_BrokerRequestLedgerEngine.mqh"
#include "FP_BrokerRequestAuditEngine.mqh"
#include "FP_PaperBrokerAdapterEngine.mqh"
#include "FP_PaperBrokerLifecycleEngine.mqh"

string FP_C01Bool(const bool v){ return (v ? "true" : "false"); }
string FP_C01Time(const datetime t){ if(t <= 0) return ""; return TimeToString(t, TIME_DATE|TIME_SECONDS); }
string FP_C01SafeCsv(string v){ StringReplace(v, "\"", "\"\""); return "\"" + v + "\""; }
string FP_C01TfLabel(const ENUM_TIMEFRAMES tf){ return EnumToString(tf); }

string FP_C01FirstBlockReason(const FP_Consolidation01NoSendContextRow &row)
{
   if(!row.has_entry_bridge)
      return "BLOCK_CONTEXT_NO_ENTRY_BRIDGE_CACHE";
   if(!row.has_paper_intent)
      return "BLOCK_CONTEXT_NO_PAPER_INTENT_CACHE";
   if(!row.has_safety_gate)
      return "BLOCK_CONTEXT_NO_SAFETY_GATE_CACHE";
   if(!row.has_dry_run)
      return "BLOCK_CONTEXT_NO_DRY_RUN_CACHE";
   if(!row.has_validator)
      return "BLOCK_CONTEXT_NO_VALIDATOR_CACHE";
   if(!row.has_audit)
      return "BLOCK_CONTEXT_NO_AUDIT_CACHE";
   if(!row.has_adapter)
      return "BLOCK_CONTEXT_NO_ADAPTER_CACHE";
   if(!row.has_lifecycle)
      return "BLOCK_CONTEXT_NO_LIFECYCLE_CACHE";
   return "none";
}

void FP_C01BuildNoSendContextRow(const string symbol,
                                 const ENUM_TIMEFRAMES period,
                                 const FP_Consolidation01NoSendContextConfig &cfg,
                                 FP_Consolidation01NoSendContextRow &row)
{
   FP_ResetConsolidation01NoSendContextRow(row);

   row.generated_at = TimeCurrent();
   row.symbol = symbol;
   row.period = period;
   row.period_label = FP_C01TfLabel(period);
   row.attempted = cfg.enabled;

   row.has_entry_bridge = g_fp_c01_has_l20_entry_bridge_row;
   row.has_paper_intent = g_fp_c01_has_l21_paper_intent_row;
   row.has_safety_gate = g_fp_c01_has_l24_safety_gate_row;
   row.has_dry_run = g_fp_c01_has_l25_dry_run_row;
   row.has_validator = g_fp_c01_has_l26_validator_row;
   row.has_ledger = g_fp_c01_has_l27_ledger_row;
   row.has_audit = g_fp_c01_has_l28_audit_row;
   row.has_adapter = g_fp_c01_has_l29_adapter_row;
   row.has_lifecycle = g_fp_c01_has_l30_lifecycle_row;

   if(row.has_entry_bridge)
   {
      row.entry_bridge_ready = g_fp_c01_l20_entry_bridge_row.ready;
      row.entry_bridge_status = g_fp_c01_l20_entry_bridge_row.readiness_status;
   }

   if(row.has_paper_intent)
   {
      row.paper_intent_allowed = g_fp_c01_l21_paper_intent_row.allowed;
      row.paper_intent_status = g_fp_c01_l21_paper_intent_row.intent_status;
   }

   if(row.has_safety_gate)
   {
      row.safety_gate_passed = g_fp_c01_l24_safety_gate_row.gate_passed;
      row.safety_gate_status = g_fp_c01_l24_safety_gate_row.gate_status;
      row.safety_gate_block_reason = g_fp_c01_l24_safety_gate_row.gate_block_reason;
   }

   if(row.has_dry_run)
   {
      row.dry_run_request_built = g_fp_c01_l25_dry_run_row.request_built;
      row.dry_run_status = g_fp_c01_l25_dry_run_row.dry_run_status;
      row.request_id = g_fp_c01_l25_dry_run_row.request_id;
      row.request_key = g_fp_c01_l25_dry_run_row.request_key;
      row.request_direction = g_fp_c01_l25_dry_run_row.request_direction;
      row.request_price = g_fp_c01_l25_dry_run_row.request_price;
      row.request_sl = g_fp_c01_l25_dry_run_row.request_sl;
      row.request_tp = g_fp_c01_l25_dry_run_row.request_tp;
      row.request_volume = g_fp_c01_l25_dry_run_row.request_volume;
   }

   if(row.has_validator)
   {
      row.validator_passed = g_fp_c01_l26_validator_row.validator_passed;
      row.validator_status = g_fp_c01_l26_validator_row.validator_status;
      row.validator_block_reason = g_fp_c01_l26_validator_row.validator_block_reason;
   }

   if(row.has_audit)
   {
      row.audit_passed = g_fp_c01_l28_audit_row.audit_passed;
      row.audit_status = g_fp_c01_l28_audit_row.audit_status;
      row.audit_block_reason = g_fp_c01_l28_audit_row.audit_block_reason;
   }

   if(row.has_adapter)
   {
      row.adapter_registered = g_fp_c01_l29_adapter_row.adapter_registered;
      row.adapter_status = g_fp_c01_l29_adapter_row.adapter_status;
      row.adapter_block_reason = g_fp_c01_l29_adapter_row.adapter_block_reason;
      row.virtual_ticket = g_fp_c01_l29_adapter_row.virtual_ticket;
   }

   if(row.has_lifecycle)
   {
      row.lifecycle_tracked = g_fp_c01_l30_lifecycle_row.lifecycle_tracked;
      row.lifecycle_status = g_fp_c01_l30_lifecycle_row.lifecycle_status;
      row.lifecycle_block_reason = g_fp_c01_l30_lifecycle_row.lifecycle_block_reason;
      row.paper_order_state = g_fp_c01_l30_lifecycle_row.paper_order_state;
      row.realized_r_like = g_fp_c01_l30_lifecycle_row.realized_r_like;
   }

   string block = FP_C01FirstBlockReason(row);
   row.context_ready = (block == "none");

   if(row.context_ready)
   {
      row.context_status = "NO_SEND_CONTEXT_READY";
      row.context_block_reason = "none";
   }
   else
   {
      row.context_status = "NO_SEND_CONTEXT_INCOMPLETE";
      row.context_block_reason = block;
   }

   row.context_key = row.symbol;
   row.context_key += "|TF=" + row.period_label;
   row.context_key += "|READY=" + FP_C01Bool(row.context_ready);
   row.context_key += "|REQ=" + row.request_id;
   row.context_key += "|VT=" + row.virtual_ticket;
   row.context_key += "|LIFECYCLE=" + row.lifecycle_status;
   row.context_key += "|EXEC=NO";
}

#endif // __FP_NO_SEND_CONTEXT_RULES_MQH__
