#ifndef __FP_BROKER_REQUEST_AUDIT_RULES_MQH__
#define __FP_BROKER_REQUEST_AUDIT_RULES_MQH__
#property strict

#include "FP_BrokerRequestAuditTypes.mqh"
#include "FP_BrokerRequestLedgerRules.mqh"
#include "FP_BrokerValidatorRules.mqh"
#include "FP_BrokerDryRunRules.mqh"

string FP_L28Bool(const bool v){ return (v ? "true" : "false"); }
string FP_L28Time(const datetime t){ if(t <= 0) return ""; return TimeToString(t, TIME_DATE|TIME_SECONDS); }
string FP_L28SafeCsv(string v){ StringReplace(v, "\"", "\"\""); return "\"" + v + "\""; }
string FP_L28TfLabel(const ENUM_TIMEFRAMES tf){ return EnumToString(tf); }

string g_fp_l28_last_audit_key = "";
int g_fp_l28_audit_sequence = 0;

string FP_L28BuildAuditId(const FP_Level25BrokerDryRunRow &dry_run,
                          const FP_Level26BrokerValidatorRow &validator)
{
   string id = "AUDIT";
   id += "_" + dry_run.symbol;
   id += "_" + EnumToString(dry_run.period);
   id += "_" + dry_run.request_id;
   id += "_" + validator.validator_status;
   id += "_" + validator.validator_block_reason;
   return id;
}

bool FP_L28NoSendContractOk(const FP_Level26BrokerValidatorRow &validator)
{
   if(StringFind(validator.no_send_contract, "NO_ORDER_SEND") < 0)
      return false;
   if(StringFind(validator.no_send_contract, "NO_ORDER_CHECK") < 0)
      return false;
   if(StringFind(validator.no_send_contract, "NO_CTRADE") < 0)
      return false;
   return true;
}

bool FP_L28RequestValidatorCoherenceOk(const FP_Level25BrokerDryRunRow &dry_run,
                                       const FP_Level26BrokerValidatorRow &validator)
{
   if(validator.validator_passed && !dry_run.request_built)
      return false;
   if(validator.validator_passed && !dry_run.dry_run_only)
      return false;
   if(validator.validator_passed && dry_run.request_volume != 0.0)
      return false;
   if(validator.request_id != dry_run.request_id)
      return false;
   return true;
}

bool FP_L28SafetyIntentCoherenceOk(const FP_Level24SafetyGateRow &safety,
                                   const FP_Level21PaperIntentRow &intent,
                                   const FP_Level25BrokerDryRunRow &dry_run)
{
   if(dry_run.request_built && !safety.gate_passed)
      return false;
   if(dry_run.request_built && !intent.allowed)
      return false;
   return true;
}

string FP_L28FirstBlockReason(const FP_Level28BrokerRequestAuditConfig &cfg,
                              const FP_Level28BrokerRequestAuditRow &row)
{
   if(cfg.require_dry_run_only && !row.dry_run_only_ok)
      return "BLOCK_AUDIT_DRY_RUN_ONLY_FALSE";
   if(cfg.require_zero_volume && !row.zero_volume_ok)
      return "BLOCK_AUDIT_VOLUME_NOT_ZERO";
   if(cfg.require_no_send_contract && !row.no_send_contract_ok)
      return "BLOCK_AUDIT_NO_SEND_CONTRACT_BROKEN";
   if(cfg.require_request_validator_coherence && !row.request_validator_coherence_ok)
      return "BLOCK_AUDIT_REQUEST_VALIDATOR_INCOHERENT";
   if(cfg.require_safety_intent_coherence && !row.safety_intent_coherence_ok)
      return "BLOCK_AUDIT_SAFETY_INTENT_INCOHERENT";
   return "none";
}

void FP_L28BuildBrokerRequestAuditRow(const string symbol,
                                      const ENUM_TIMEFRAMES period,
                                      const FP_Level24SafetyGateRow &safety,
                                      const FP_Level21PaperIntentRow &intent,
                                      const FP_Level25BrokerDryRunRow &dry_run,
                                      const FP_Level26BrokerValidatorRow &validator,
                                      const FP_Level28BrokerRequestAuditConfig &cfg,
                                      FP_Level28BrokerRequestAuditRow &row)
{
   FP_ResetLevel28BrokerRequestAuditRow(row);

   row.generated_at = TimeCurrent();
   row.symbol = symbol;
   row.period = period;
   row.period_label = FP_L28TfLabel(period);
   row.attempted = cfg.enabled;

   row.request_id = dry_run.request_id;
   row.request_key = dry_run.request_key;
   row.request_built = dry_run.request_built;
   row.dry_run_only = dry_run.dry_run_only;
   row.dry_run_status = dry_run.dry_run_status;
   row.dry_run_block_reason = dry_run.block_reason;

   row.validator_passed = validator.validator_passed;
   row.validator_status = validator.validator_status;
   row.validator_block_reason = validator.validator_block_reason;
   row.validator_key = validator.validator_key;

   row.safety_gate_passed = safety.gate_passed;
   row.safety_gate_status = safety.gate_status;
   row.safety_gate_block_reason = safety.gate_block_reason;

   row.intent_allowed = intent.allowed;
   row.intent_id = intent.intent_id;
   row.intent_status = intent.intent_status;

   row.request_order_type = dry_run.request_order_type;
   row.request_direction = dry_run.request_direction;
   row.request_volume = dry_run.request_volume;
   row.request_price = dry_run.request_price;
   row.request_sl = dry_run.request_sl;
   row.request_tp = dry_run.request_tp;

   row.dry_run_only_ok = dry_run.dry_run_only;
   row.zero_volume_ok = (dry_run.request_volume == 0.0);
   row.no_send_contract_ok = FP_L28NoSendContractOk(validator);
   row.request_validator_coherence_ok = FP_L28RequestValidatorCoherenceOk(dry_run, validator);
   row.safety_intent_coherence_ok = FP_L28SafetyIntentCoherenceOk(safety, intent, dry_run);

   row.ledger_sequence_current = g_fp_l27_ledger_sequence;
   row.ledger_last_request_key = g_fp_l27_last_request_key;
   row.ledger_runtime_seen = (g_fp_l27_ledger_sequence > 0 || StringLen(g_fp_l27_last_request_key) > 0);

   row.validator_readiness = (validator.validator_passed ? "VALIDATOR_READY_NO_SEND" : "VALIDATOR_BLOCKED_NO_SEND");
   if(dry_run.request_built && validator.validator_passed)
      row.request_chain_state = "REQUEST_CHAIN_BUILT_AND_VALIDATED_NO_SEND";
   else if(dry_run.request_built && !validator.validator_passed)
      row.request_chain_state = "REQUEST_CHAIN_BUILT_BUT_VALIDATOR_BLOCKED";
   else if(!dry_run.request_built)
      row.request_chain_state = "REQUEST_CHAIN_NOT_BUILT";
   else
      row.request_chain_state = "REQUEST_CHAIN_UNKNOWN";

   row.audit_id = FP_L28BuildAuditId(dry_run, validator);

   string block = FP_L28FirstBlockReason(cfg, row);
   row.audit_passed = (block == "none");

   string dedupe_key = row.request_key;
   dedupe_key += "|VALIDATOR=" + row.validator_status;
   dedupe_key += "|AUDIT_BLOCK=" + block;
   dedupe_key += "|CHAIN=" + row.request_chain_state;

   if(cfg.skip_duplicate_audit_key && dedupe_key == g_fp_l28_last_audit_key)
   {
      row.duplicate_skipped = true;
      row.audit_status = "BROKER_REQUEST_AUDIT_DUPLICATE_SKIPPED";
      row.audit_block_reason = "duplicate_audit_key";
   }
   else
   {
      g_fp_l28_last_audit_key = dedupe_key;
      g_fp_l28_audit_sequence++;
      row.duplicate_skipped = false;

      if(row.audit_passed)
      {
         row.audit_status = "BROKER_REQUEST_AUDIT_PASSED_NO_SEND";
         row.audit_block_reason = "none";
      }
      else
      {
         row.audit_status = "BROKER_REQUEST_AUDIT_BLOCKED";
         row.audit_block_reason = block;
      }
   }

   row.audit_key = row.symbol;
   row.audit_key += "|TF=" + row.period_label;
   row.audit_key += "|SEQ=" + IntegerToString(g_fp_l28_audit_sequence);
   row.audit_key += "|REQ=" + row.request_id;
   row.audit_key += "|PASSED=" + FP_L28Bool(row.audit_passed);
   row.audit_key += "|BLOCK=" + row.audit_block_reason;
   row.audit_key += "|NO_SEND=true";
   row.audit_key += "|EXEC=NO";
}

#endif // __FP_BROKER_REQUEST_AUDIT_RULES_MQH__
