#ifndef __FP_BROKER_DRY_RUN_TYPES_MQH__
#define __FP_BROKER_DRY_RUN_TYPES_MQH__
#property strict

#include "FP_SafetyGateTypes.mqh"
#include "FP_PaperIntentTypes.mqh"

#define FP_LEVEL25_BROKER_DRY_RUN_VERSION "25.00-broker-dry-run-only"
#define FP_LEVEL25_BROKER_DRY_RUN_DEFAULT_FOLDER "FlagCountingPhoenix"

// ============================================================================
// FlagCounting Phoenix - Level 25 Broker Dry Run Types
// ----------------------------------------------------------------------------
// Contract:
// - broker-like request preview only
// - CSV only
// - no CTrade
// - no OrderSend
// - no OrderCheck
// - no position
// - no volume / risk sizing
// - no renderer mutation
// - no chart-object mutation
// ============================================================================

struct FP_Level25BrokerDryRunConfig
{
   bool enabled;
   bool export_csv;
   bool print_summary;

   bool require_safety_gate_passed;
   bool require_intent_allowed;
   bool dry_run_only;

   long magic;
   string request_comment;
   string folder;
};

struct FP_Level25BrokerDryRunRow
{
   datetime generated_at;
   string version;
   string symbol;
   ENUM_TIMEFRAMES period;
   string period_label;

   bool attempted;
   bool request_built;
   bool dry_run_only;

   string dry_run_status;
   string block_reason;
   string request_id;
   string request_key;

   string safety_gate_status;
   bool safety_gate_passed;
   string safety_gate_block_reason;

   string intent_id;
   bool intent_allowed;
   string intent_status;

   string request_action;
   string request_order_type;
   string request_direction;

   double request_volume;
   double request_price;
   double request_sl;
   double request_tp;
   double request_deviation_points;

   long request_magic;
   string request_comment;

   double entry_price;
   double stop_price;
   double target_price;
   double risk_distance;
   double reward_distance;
   double rr_like;

   string price_geometry_status;
   string request_validity_status;

   string no_touch_contract;
   string execution_status;
};

struct FP_Level25BrokerDryRunReport
{
   bool attempted;
   bool ok;
   string status;
   string reason;
   int files_written;
   int file_errors;
   bool dry_run_written;
};

void FP_ResetLevel25BrokerDryRunConfig(FP_Level25BrokerDryRunConfig &cfg)
{
   cfg.enabled = true;
   cfg.export_csv = true;
   cfg.print_summary = false;

   cfg.require_safety_gate_passed = true;
   cfg.require_intent_allowed = true;
   cfg.dry_run_only = true;

   cfg.magic = 250025;
   cfg.request_comment = "DAL_L25_DRY_RUN_ONLY";
   cfg.folder = FP_LEVEL25_BROKER_DRY_RUN_DEFAULT_FOLDER;
}

void FP_ResetLevel25BrokerDryRunRow(FP_Level25BrokerDryRunRow &r)
{
   r.generated_at = 0;
   r.version = FP_LEVEL25_BROKER_DRY_RUN_VERSION;
   r.symbol = "";
   r.period = PERIOD_CURRENT;
   r.period_label = "";

   r.attempted = false;
   r.request_built = false;
   r.dry_run_only = true;

   r.dry_run_status = "BROKER_DRY_RUN_RESET";
   r.block_reason = "RESET";
   r.request_id = "";
   r.request_key = "";

   r.safety_gate_status = "";
   r.safety_gate_passed = false;
   r.safety_gate_block_reason = "";

   r.intent_id = "";
   r.intent_allowed = false;
   r.intent_status = "";

   r.request_action = "TRADE_ACTION_PENDING_PREVIEW_ONLY";
   r.request_order_type = "ORDER_TYPE_NONE";
   r.request_direction = "DIRECTION_NONE";

   r.request_volume = 0.0;
   r.request_price = 0.0;
   r.request_sl = 0.0;
   r.request_tp = 0.0;
   r.request_deviation_points = 0.0;

   r.request_magic = 0;
   r.request_comment = "";

   r.entry_price = 0.0;
   r.stop_price = 0.0;
   r.target_price = 0.0;
   r.risk_distance = 0.0;
   r.reward_distance = 0.0;
   r.rr_like = 0.0;

   r.price_geometry_status = "PRICE_GEOMETRY_NOT_EVALUATED";
   r.request_validity_status = "REQUEST_VALIDITY_NOT_EVALUATED";

   r.no_touch_contract = "BROKER_DRY_RUN_ONLY_NO_ORDER_SEND_NO_CTRADE_NO_RENDERER_MUTATION";
   r.execution_status = "REAL_EXECUTION_DISABLED_LEVEL25_BROKER_DRY_RUN_ONLY";
}

void FP_ResetLevel25BrokerDryRunReport(FP_Level25BrokerDryRunReport &r)
{
   r.attempted = false;
   r.ok = false;
   r.status = "not_attempted";
   r.reason = "not_attempted";
   r.files_written = 0;
   r.file_errors = 0;
   r.dry_run_written = false;
}

#endif // __FP_BROKER_DRY_RUN_TYPES_MQH__
