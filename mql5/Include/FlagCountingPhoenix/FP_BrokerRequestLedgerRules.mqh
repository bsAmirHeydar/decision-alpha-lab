#ifndef __FP_BROKER_REQUEST_LEDGER_RULES_MQH__
#define __FP_BROKER_REQUEST_LEDGER_RULES_MQH__
#property strict

#include "FP_BrokerRequestLedgerTypes.mqh"
#include "FP_BrokerValidatorRules.mqh"
#include "FP_BrokerDryRunRules.mqh"

string FP_L27Bool(const bool v){ return (v ? "true" : "false"); }
string FP_L27Time(const datetime t){ if(t <= 0) return ""; return TimeToString(t, TIME_DATE|TIME_SECONDS); }
string FP_L27SafeCsv(string v){ StringReplace(v, "\"", "\"\""); return "\"" + v + "\""; }
string FP_L27TfLabel(const ENUM_TIMEFRAMES tf){ return EnumToString(tf); }

string g_fp_l27_last_request_key = "";
int g_fp_l27_ledger_sequence = 0;

string FP_L27BuildLedgerId(const FP_Level25BrokerDryRunRow &dry_run,
                           const FP_Level26BrokerValidatorRow &validator)
{
   string id = "L27";
   id += "_" + dry_run.symbol;
   id += "_" + EnumToString(dry_run.period);
   id += "_" + dry_run.request_id;
   id += "_" + validator.validator_status;
   id += "_" + validator.validator_block_reason;
   return id;
}

void FP_L27BuildBrokerRequestLedgerRow(const string symbol,
                                       const ENUM_TIMEFRAMES period,
                                       const FP_Level24SafetyGateRow &safety,
                                       const FP_Level21PaperIntentRow &intent,
                                       const FP_Level25BrokerDryRunRow &dry_run,
                                       const FP_Level26BrokerValidatorRow &validator,
                                       const FP_Level27BrokerRequestLedgerConfig &cfg,
                                       FP_Level27BrokerRequestLedgerRow &row)
{
   FP_ResetLevel27BrokerRequestLedgerRow(row);

   row.generated_at = TimeCurrent();
   row.symbol = symbol;
   row.period = period;
   row.period_label = FP_L27TfLabel(period);
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

   row.safety_gate_status = safety.gate_status;
   row.safety_gate_passed = safety.gate_passed;
   row.safety_gate_block_reason = safety.gate_block_reason;

   row.intent_id = intent.intent_id;
   row.intent_allowed = intent.allowed;
   row.intent_status = intent.intent_status;

   row.request_order_type = dry_run.request_order_type;
   row.request_direction = dry_run.request_direction;
   row.request_volume = dry_run.request_volume;
   row.request_price = dry_run.request_price;
   row.request_sl = dry_run.request_sl;
   row.request_tp = dry_run.request_tp;
   row.request_magic = dry_run.request_magic;
   row.request_comment = dry_run.request_comment;

   row.price_normalized = validator.price_normalized;
   row.sl_normalized = validator.sl_normalized;
   row.tp_normalized = validator.tp_normalized;
   row.price_tick_aligned = validator.price_tick_aligned;
   row.sl_tick_aligned = validator.sl_tick_aligned;
   row.tp_tick_aligned = validator.tp_tick_aligned;
   row.stop_distance_ok = validator.stop_distance_ok;
   row.target_distance_ok = validator.target_distance_ok;
   row.zero_volume_ok = validator.zero_volume_ok;
   row.price_geometry_ok = validator.price_geometry_ok;

   row.ledger_id = FP_L27BuildLedgerId(dry_run, validator);

   string dedupe_key = dry_run.request_key;
   dedupe_key += "|VALIDATOR=" + validator.validator_status;
   dedupe_key += "|BLOCK=" + validator.validator_block_reason;

   if(cfg.skip_duplicate_request_key && dedupe_key == g_fp_l27_last_request_key)
   {
      row.duplicate_skipped = true;
      row.ledger_status = "BROKER_REQUEST_LEDGER_DUPLICATE_SKIPPED";
      row.ledger_reason = "duplicate_request_key";
      row.ledger_sequence = g_fp_l27_ledger_sequence;
   }
   else
   {
      g_fp_l27_last_request_key = dedupe_key;
      g_fp_l27_ledger_sequence++;
      row.duplicate_skipped = false;
      row.ledger_status = (validator.validator_passed ? "BROKER_REQUEST_LEDGER_ACCEPTED_NO_SEND" : "BROKER_REQUEST_LEDGER_RECORDED_BLOCKED_NO_SEND");
      row.ledger_reason = (validator.validator_passed ? "validator_passed_no_send" : validator.validator_block_reason);
      row.ledger_sequence = g_fp_l27_ledger_sequence;
   }

   row.ledger_key = row.symbol;
   row.ledger_key += "|TF=" + row.period_label;
   row.ledger_key += "|SEQ=" + IntegerToString(row.ledger_sequence);
   row.ledger_key += "|REQ=" + row.request_id;
   row.ledger_key += "|VALIDATOR=" + row.validator_status;
   row.ledger_key += "|DUP=" + FP_L27Bool(row.duplicate_skipped);
   row.ledger_key += "|NO_SEND=true";
   row.ledger_key += "|EXEC=NO";
}

#endif // __FP_BROKER_REQUEST_LEDGER_RULES_MQH__
