#ifndef __FP_PAPER_BROKER_ADAPTER_RULES_MQH__
#define __FP_PAPER_BROKER_ADAPTER_RULES_MQH__
#property strict

#include "FP_PaperBrokerAdapterTypes.mqh"
#include "FP_BrokerRequestAuditRules.mqh"
#include "FP_BrokerValidatorRules.mqh"
#include "FP_BrokerDryRunRules.mqh"

string FP_L29Bool(const bool v){ return (v ? "true" : "false"); }
string FP_L29Time(const datetime t){ if(t <= 0) return ""; return TimeToString(t, TIME_DATE|TIME_SECONDS); }
string FP_L29SafeCsv(string v){ StringReplace(v, "\"", "\"\""); return "\"" + v + "\""; }
string FP_L29TfLabel(const ENUM_TIMEFRAMES tf){ return EnumToString(tf); }

string g_fp_l29_last_adapter_key = "";
int g_fp_l29_adapter_sequence = 0;

string FP_L29BuildAdapterId(const FP_Level25BrokerDryRunRow &dry_run,
                            const FP_Level26BrokerValidatorRow &validator,
                            const FP_Level28BrokerRequestAuditRow &audit)
{
   string id = "PBA";
   id += "_" + dry_run.symbol;
   id += "_" + EnumToString(dry_run.period);
   id += "_" + dry_run.request_id;
   id += "_" + validator.validator_status;
   id += "_" + audit.audit_status;
   return id;
}

string FP_L29BuildVirtualTicket(const string symbol,
                                const ENUM_TIMEFRAMES period,
                                const int seq,
                                const FP_Level25BrokerDryRunRow &dry_run)
{
   string t = "VT";
   t += "_" + symbol;
   t += "_" + EnumToString(period);
   t += "_" + IntegerToString(seq);
   t += "_" + dry_run.request_id;
   return t;
}

bool FP_L29NoSendContractOk(const FP_Level28BrokerRequestAuditRow &audit)
{
   if(StringFind(audit.no_send_contract, "NO_ORDER_SEND") < 0)
      return false;
   if(StringFind(audit.no_send_contract, "NO_ORDER_CHECK") < 0)
      return false;
   if(StringFind(audit.no_send_contract, "NO_CTRADE") < 0)
      return false;
   return true;
}

bool FP_L29AdapterChainCoherenceOk(const FP_Level25BrokerDryRunRow &dry_run,
                                   const FP_Level26BrokerValidatorRow &validator,
                                   const FP_Level28BrokerRequestAuditRow &audit)
{
   if(audit.audit_passed && !validator.validator_passed)
      return false;
   if(audit.audit_passed && !dry_run.request_built)
      return false;
   if(validator.validator_passed && !dry_run.request_built)
      return false;
   if(validator.request_id != dry_run.request_id)
      return false;
   if(audit.request_id != dry_run.request_id)
      return false;
   return true;
}

string FP_L29FirstBlockReason(const FP_Level29PaperBrokerAdapterConfig &cfg,
                              const FP_Level29PaperBrokerAdapterRow &row)
{
   if(!cfg.adapter_dry_run_only)
      return "BLOCK_ADAPTER_DRY_RUN_ONLY_FALSE";
   if(cfg.require_audit_passed && !row.audit_passed)
      return "BLOCK_ADAPTER_AUDIT_NOT_PASSED";
   if(cfg.require_validator_passed && !row.validator_passed)
      return "BLOCK_ADAPTER_VALIDATOR_NOT_PASSED";
   if(cfg.require_request_built && !row.request_built)
      return "BLOCK_ADAPTER_REQUEST_NOT_BUILT";
   if(cfg.require_dry_run_only && !row.dry_run_only_ok)
      return "BLOCK_ADAPTER_DRY_RUN_ONLY_BROKEN";
   if(cfg.require_zero_volume && !row.zero_volume_ok)
      return "BLOCK_ADAPTER_VOLUME_NOT_ZERO";
   if(!row.no_send_contract_ok)
      return "BLOCK_ADAPTER_NO_SEND_CONTRACT_BROKEN";
   if(!row.adapter_chain_coherence_ok)
      return "BLOCK_ADAPTER_CHAIN_INCOHERENT";
   return "none";
}

void FP_L29BuildPaperBrokerAdapterRow(const string symbol,
                                      const ENUM_TIMEFRAMES period,
                                      const FP_Level25BrokerDryRunRow &dry_run,
                                      const FP_Level26BrokerValidatorRow &validator,
                                      const FP_Level28BrokerRequestAuditRow &audit,
                                      const FP_Level29PaperBrokerAdapterConfig &cfg,
                                      FP_Level29PaperBrokerAdapterRow &row)
{
   FP_ResetLevel29PaperBrokerAdapterRow(row);

   row.generated_at = TimeCurrent();
   row.symbol = symbol;
   row.period = period;
   row.period_label = FP_L29TfLabel(period);
   row.attempted = cfg.enabled;

   row.request_id = dry_run.request_id;
   row.request_key = dry_run.request_key;
   row.request_built = dry_run.request_built;
   row.dry_run_only = dry_run.dry_run_only;
   row.dry_run_status = dry_run.dry_run_status;

   row.validator_passed = validator.validator_passed;
   row.validator_status = validator.validator_status;
   row.validator_block_reason = validator.validator_block_reason;

   row.audit_passed = audit.audit_passed;
   row.audit_status = audit.audit_status;
   row.audit_block_reason = audit.audit_block_reason;

   row.request_order_type = dry_run.request_order_type;
   row.request_direction = dry_run.request_direction;
   row.request_volume = dry_run.request_volume;
   row.request_price = dry_run.request_price;
   row.request_sl = dry_run.request_sl;
   row.request_tp = dry_run.request_tp;
   row.request_magic = dry_run.request_magic;
   row.request_comment = dry_run.request_comment;

   row.zero_volume_ok = (dry_run.request_volume == 0.0);
   row.dry_run_only_ok = dry_run.dry_run_only;
   row.no_send_contract_ok = FP_L29NoSendContractOk(audit);
   row.adapter_chain_coherence_ok = FP_L29AdapterChainCoherenceOk(dry_run, validator, audit);

   row.adapter_id = FP_L29BuildAdapterId(dry_run, validator, audit);

   string block = FP_L29FirstBlockReason(cfg, row);
   row.adapter_registered = (block == "none");

   string dedupe_key = row.request_key;
   dedupe_key += "|VALIDATOR=" + row.validator_status;
   dedupe_key += "|AUDIT=" + row.audit_status;
   dedupe_key += "|ADAPTER_BLOCK=" + block;

   if(cfg.skip_duplicate_adapter_key && dedupe_key == g_fp_l29_last_adapter_key)
   {
      row.duplicate_skipped = true;
      row.adapter_status = "PAPER_BROKER_ADAPTER_DUPLICATE_SKIPPED";
      row.adapter_block_reason = "duplicate_adapter_key";
      row.adapter_sequence = g_fp_l29_adapter_sequence;
      row.virtual_ticket = FP_L29BuildVirtualTicket(symbol, period, row.adapter_sequence, dry_run);
   }
   else
   {
      g_fp_l29_last_adapter_key = dedupe_key;
      g_fp_l29_adapter_sequence++;
      row.duplicate_skipped = false;
      row.adapter_sequence = g_fp_l29_adapter_sequence;
      row.virtual_ticket = FP_L29BuildVirtualTicket(symbol, period, row.adapter_sequence, dry_run);

      if(row.adapter_registered)
      {
         row.adapter_status = "PAPER_BROKER_ADAPTER_REGISTERED_NO_SEND";
         row.adapter_block_reason = "none";
         row.paper_order_state = "PAPER_ORDER_STATE_REGISTERED_PENDING_PREVIEW";
         row.paper_order_lifecycle_hint = "NEXT_LEVEL_30_PAPER_BROKER_LIFECYCLE";
         row.adapter_runtime_state = "ADAPTER_RUNTIME_REGISTERED_NO_SEND";
      }
      else
      {
         row.adapter_status = "PAPER_BROKER_ADAPTER_BLOCKED";
         row.adapter_block_reason = block;
         row.paper_order_state = "PAPER_ORDER_STATE_BLOCKED";
         row.paper_order_lifecycle_hint = "FIX_ADAPTER_BLOCK_BEFORE_LIFECYCLE";
         row.adapter_runtime_state = "ADAPTER_RUNTIME_BLOCKED_NO_SEND";
      }
   }

   row.adapter_key = row.symbol;
   row.adapter_key += "|TF=" + row.period_label;
   row.adapter_key += "|SEQ=" + IntegerToString(row.adapter_sequence);
   row.adapter_key += "|VT=" + row.virtual_ticket;
   row.adapter_key += "|REQ=" + row.request_id;
   row.adapter_key += "|REGISTERED=" + FP_L29Bool(row.adapter_registered);
   row.adapter_key += "|NO_SEND=true";
   row.adapter_key += "|EXEC=NO";
}

#endif // __FP_PAPER_BROKER_ADAPTER_RULES_MQH__
