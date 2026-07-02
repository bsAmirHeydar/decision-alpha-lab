#ifndef __FP_FINAL_DECISION_STATE_RULES_MQH__
#define __FP_FINAL_DECISION_STATE_RULES_MQH__
#property strict

#include "FP_FinalDecisionStateTypes.mqh"
#include "FP_NoSendContextRules.mqh"

string FP_C02Bool(const bool v){ return (v ? "true" : "false"); }
string FP_C02Time(const datetime t){ if(t <= 0) return ""; return TimeToString(t, TIME_DATE|TIME_SECONDS); }
string FP_C02SafeCsv(string v){ StringReplace(v, "\"", "\"\""); return "\"" + v + "\""; }
string FP_C02TfLabel(const ENUM_TIMEFRAMES tf){ return EnumToString(tf); }

bool FP_C02NoSendIntegrityOk(const FP_Consolidation01NoSendContextRow &ctx)
{
   if(StringFind(ctx.no_send_contract, "NO_ORDER_SEND") < 0)
      return false;
   if(StringFind(ctx.no_send_contract, "NO_ORDER_CHECK") < 0)
      return false;
   if(StringFind(ctx.no_send_contract, "NO_CTRADE") < 0)
      return false;
   if(ctx.request_volume != 0.0)
      return false;
   return true;
}

void FP_C02ResolveBlocker(const FP_Consolidation01NoSendContextRow &ctx,
                          FP_Consolidation02FinalDecisionRow &row)
{
   if(!ctx.has_entry_bridge || !ctx.entry_bridge_ready)
   {
      row.blocker_layer = "LEVEL20_ENTRY_BRIDGE";
      row.blocker_status = ctx.entry_bridge_status;
      row.blocker_reason = (ctx.has_entry_bridge ? ctx.entry_bridge_status : "missing_cache");
      return;
   }

   if(!ctx.has_paper_intent || !ctx.paper_intent_allowed)
   {
      row.blocker_layer = "LEVEL21_PAPER_INTENT";
      row.blocker_status = ctx.paper_intent_status;
      row.blocker_reason = (ctx.has_paper_intent ? ctx.paper_intent_status : "missing_cache");
      return;
   }

   if(!ctx.has_safety_gate || !ctx.safety_gate_passed)
   {
      row.blocker_layer = "LEVEL24_SAFETY_GATE";
      row.blocker_status = ctx.safety_gate_status;
      row.blocker_reason = (ctx.has_safety_gate ? ctx.safety_gate_block_reason : "missing_cache");
      return;
   }

   if(!ctx.has_dry_run || !ctx.dry_run_request_built)
   {
      row.blocker_layer = "LEVEL25_BROKER_DRY_RUN";
      row.blocker_status = ctx.dry_run_status;
      row.blocker_reason = (ctx.has_dry_run ? ctx.dry_run_status : "missing_cache");
      return;
   }

   if(!ctx.has_validator || !ctx.validator_passed)
   {
      row.blocker_layer = "LEVEL26_BROKER_VALIDATOR";
      row.blocker_status = ctx.validator_status;
      row.blocker_reason = (ctx.has_validator ? ctx.validator_block_reason : "missing_cache");
      return;
   }

   if(!ctx.has_audit || !ctx.audit_passed)
   {
      row.blocker_layer = "LEVEL28_BROKER_REQUEST_AUDIT";
      row.blocker_status = ctx.audit_status;
      row.blocker_reason = (ctx.has_audit ? ctx.audit_block_reason : "missing_cache");
      return;
   }

   if(!ctx.has_adapter || !ctx.adapter_registered)
   {
      row.blocker_layer = "LEVEL29_PAPER_BROKER_ADAPTER";
      row.blocker_status = ctx.adapter_status;
      row.blocker_reason = (ctx.has_adapter ? ctx.adapter_block_reason : "missing_cache");
      return;
   }

   if(!ctx.has_lifecycle)
   {
      row.blocker_layer = "LEVEL30_PAPER_BROKER_LIFECYCLE";
      row.blocker_status = "missing_cache";
      row.blocker_reason = "missing_cache";
      return;
   }

   row.blocker_layer = "NONE";
   row.blocker_status = "none";
   row.blocker_reason = "none";
}

string FP_C02ResolveChainStage(const FP_Consolidation02FinalDecisionRow &row)
{
   if(row.blocker_layer == "LEVEL20_ENTRY_BRIDGE")
      return "CHAIN_BLOCKED_AT_ENTRY_BRIDGE";
   if(row.blocker_layer == "LEVEL21_PAPER_INTENT")
      return "CHAIN_BLOCKED_AT_PAPER_INTENT";
   if(row.blocker_layer == "LEVEL24_SAFETY_GATE")
      return "CHAIN_BLOCKED_AT_SAFETY_GATE";
   if(row.blocker_layer == "LEVEL25_BROKER_DRY_RUN")
      return "CHAIN_BLOCKED_AT_DRY_RUN";
   if(row.blocker_layer == "LEVEL26_BROKER_VALIDATOR")
      return "CHAIN_BLOCKED_AT_VALIDATOR";
   if(row.blocker_layer == "LEVEL28_BROKER_REQUEST_AUDIT")
      return "CHAIN_BLOCKED_AT_AUDIT";
   if(row.blocker_layer == "LEVEL29_PAPER_BROKER_ADAPTER")
      return "CHAIN_BLOCKED_AT_ADAPTER";
   if(row.blocker_layer == "LEVEL30_PAPER_BROKER_LIFECYCLE")
      return "CHAIN_BLOCKED_AT_LIFECYCLE";
   if(row.lifecycle_tracked)
      return "CHAIN_LIFECYCLE_TRACKED";
   return "CHAIN_READY_NO_SEND";
}

string FP_C02ResolveSetupState(const FP_Consolidation02FinalDecisionRow &row)
{
   if(row.blocker_layer != "NONE")
      return "SETUP_BLOCKED";
   if(row.lifecycle_tracked)
   {
      if(row.lifecycle_status == "PAPER_BROKER_LIFECYCLE_HIT_TARGET_BY_CLOSE")
         return "SETUP_PAPER_TARGET_HIT";
      if(row.lifecycle_status == "PAPER_BROKER_LIFECYCLE_HIT_STOP_BY_CLOSE")
         return "SETUP_PAPER_STOP_HIT";
      if(row.lifecycle_status == "PAPER_BROKER_LIFECYCLE_ACTIVE_OPEN_CLOSE_ONLY")
         return "SETUP_PAPER_ACTIVE_OPEN";
      if(row.lifecycle_status == "PAPER_BROKER_LIFECYCLE_ENTERED_BY_CLOSE")
         return "SETUP_PAPER_ENTERED";
      if(StringFind(row.lifecycle_status, "EXPIRED") >= 0)
         return "SETUP_PAPER_EXPIRED";
      return "SETUP_PAPER_TRACKED";
   }
   return "SETUP_READY_NO_SEND";
}

string FP_C02ResolveNextActionHint(const FP_Consolidation02FinalDecisionRow &row)
{
   if(row.blocker_layer == "NONE")
   {
      if(row.lifecycle_tracked)
         return "REVIEW_PAPER_LIFECYCLE_AND_R_LIKE";
      return "WAIT_FOR_PAPER_LIFECYCLE_OR_NEXT_BAR";
   }

   if(row.blocker_layer == "LEVEL20_ENTRY_BRIDGE")
      return "FIX_OR_WAIT_ENTRY_BRIDGE";
   if(row.blocker_layer == "LEVEL21_PAPER_INTENT")
      return "FIX_OR_WAIT_PAPER_INTENT";
   if(row.blocker_layer == "LEVEL24_SAFETY_GATE")
      return "FIX_SAFETY_GATE_CONSTRAINT";
   if(row.blocker_layer == "LEVEL25_BROKER_DRY_RUN")
      return "REVIEW_DRY_RUN_REQUEST_PREVIEW";
   if(row.blocker_layer == "LEVEL26_BROKER_VALIDATOR")
      return "FIX_VALIDATOR_BLOCK_REASON";
   if(row.blocker_layer == "LEVEL28_BROKER_REQUEST_AUDIT")
      return "FIX_NO_SEND_CHAIN_AUDIT";
   if(row.blocker_layer == "LEVEL29_PAPER_BROKER_ADAPTER")
      return "FIX_ADAPTER_REGISTRATION";
   if(row.blocker_layer == "LEVEL30_PAPER_BROKER_LIFECYCLE")
      return "WAIT_OR_FIX_LIFECYCLE_CACHE";

   return "NO_ACTION";
}

string FP_C02FirstBlockReason(const FP_Consolidation02FinalDecisionConfig &cfg,
                              const FP_Consolidation02FinalDecisionRow &row)
{
   if(cfg.require_no_send_integrity && !row.no_send_integrity_ok)
      return "BLOCK_FINAL_NO_SEND_INTEGRITY_BROKEN";
   if(cfg.require_context_ready_for_ready_state && !row.context_ready)
      return row.context_block_reason;
   if(cfg.require_lifecycle_tracked_for_ready_state && !row.lifecycle_tracked)
      return "BLOCK_FINAL_LIFECYCLE_NOT_TRACKED";
   if(row.blocker_layer != "NONE")
      return row.blocker_layer + ":" + row.blocker_reason;
   return "none";
}

void FP_C02BuildFinalDecisionRow(const string symbol,
                                 const ENUM_TIMEFRAMES period,
                                 const FP_Consolidation01NoSendContextRow &ctx,
                                 const FP_Consolidation02FinalDecisionConfig &cfg,
                                 FP_Consolidation02FinalDecisionRow &row)
{
   FP_ResetConsolidation02FinalDecisionRow(row);

   row.generated_at = TimeCurrent();
   row.symbol = symbol;
   row.period = period;
   row.period_label = FP_C02TfLabel(period);
   row.attempted = cfg.enabled;

   row.context_ready = ctx.context_ready;
   row.context_status = ctx.context_status;
   row.context_block_reason = ctx.context_block_reason;

   row.entry_bridge_ready = ctx.entry_bridge_ready;
   row.paper_intent_allowed = ctx.paper_intent_allowed;
   row.safety_gate_passed = ctx.safety_gate_passed;
   row.dry_run_request_built = ctx.dry_run_request_built;
   row.validator_passed = ctx.validator_passed;
   row.audit_passed = ctx.audit_passed;
   row.adapter_registered = ctx.adapter_registered;
   row.lifecycle_tracked = ctx.lifecycle_tracked;

   row.request_id = ctx.request_id;
   row.request_key = ctx.request_key;
   row.virtual_ticket = ctx.virtual_ticket;
   row.request_direction = ctx.request_direction;
   row.entry_price = ctx.request_price;
   row.stop_price = ctx.request_sl;
   row.target_price = ctx.request_tp;
   row.request_volume = ctx.request_volume;

   row.lifecycle_status = ctx.lifecycle_status;
   row.lifecycle_block_reason = ctx.lifecycle_block_reason;
   row.paper_order_state = ctx.paper_order_state;
   row.realized_r_like = ctx.realized_r_like;

   row.no_send_integrity_ok = FP_C02NoSendIntegrityOk(ctx);

   FP_C02ResolveBlocker(ctx, row);

   row.chain_stage = FP_C02ResolveChainStage(row);
   row.setup_state = FP_C02ResolveSetupState(row);
   row.next_action_hint = FP_C02ResolveNextActionHint(row);

   string block = FP_C02FirstBlockReason(cfg, row);
   row.decision_ready = (block == "none");

   if(row.decision_ready)
   {
      row.decision_state = "FINAL_DECISION_READY_NO_SEND";
      row.decision_block_reason = "none";
   }
   else
   {
      row.decision_state = "FINAL_DECISION_BLOCKED_NO_SEND";
      row.decision_block_reason = block;
   }

   row.decision_key = row.symbol;
   row.decision_key += "|TF=" + row.period_label;
   row.decision_key += "|STATE=" + row.decision_state;
   row.decision_key += "|SETUP=" + row.setup_state;
   row.decision_key += "|BLOCKER=" + row.blocker_layer;
   row.decision_key += "|REQ=" + row.request_id;
   row.decision_key += "|VT=" + row.virtual_ticket;
   row.decision_key += "|EXEC=NO";
}

#endif // __FP_FINAL_DECISION_STATE_RULES_MQH__
