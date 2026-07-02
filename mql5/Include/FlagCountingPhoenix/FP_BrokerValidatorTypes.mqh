#ifndef __FP_BROKER_VALIDATOR_TYPES_MQH__
#define __FP_BROKER_VALIDATOR_TYPES_MQH__
#property strict

#include "FP_BrokerDryRunTypes.mqh"

#define FP_LEVEL26_BROKER_VALIDATOR_VERSION "26.00-broker-request-validator-no-send"
#define FP_LEVEL26_BROKER_VALIDATOR_DEFAULT_FOLDER "FlagCountingPhoenix"

// ============================================================================
// FlagCounting Phoenix - Level 26 Broker Request Validator Types
// ----------------------------------------------------------------------------
// Contract:
// - validate dry-run broker-like preview only
// - CSV only
// - no CTrade
// - no OrderSend
// - no OrderCheck
// - no position
// - no volume / risk sizing
// - no renderer mutation
// - no chart-object mutation
// ============================================================================

struct FP_Level26BrokerValidatorConfig
{
   bool enabled;
   bool export_csv;
   bool print_summary;

   bool require_dry_run_built;
   bool require_tick_alignment;
   bool require_stop_distance;
   bool require_normalized_prices;
   bool require_zero_volume;
   bool require_dry_run_only;

   string folder;
};

struct FP_Level26BrokerValidatorRow
{
   datetime generated_at;
   string version;
   string symbol;
   ENUM_TIMEFRAMES period;
   string period_label;

   bool attempted;
   bool validator_passed;
   string validator_status;
   string validator_block_reason;
   string validator_key;

   string dry_run_status;
   bool dry_run_request_built;
   bool dry_run_only;
   string request_id;
   string request_order_type;
   string request_direction;

   double request_volume;
   double request_price;
   double request_sl;
   double request_tp;

   int symbol_digits;
   double symbol_point;
   double symbol_tick_size;
   int symbol_stops_level_points;
   double min_stop_distance_price;

   double normalized_price;
   double normalized_sl;
   double normalized_tp;

   bool price_normalized;
   bool sl_normalized;
   bool tp_normalized;

   bool price_tick_aligned;
   bool sl_tick_aligned;
   bool tp_tick_aligned;

   double stop_distance_price;
   double target_distance_price;
   double stop_distance_points;
   double target_distance_points;

   bool stop_distance_ok;
   bool target_distance_ok;
   bool zero_volume_ok;
   bool price_geometry_ok;

   string no_send_contract;
   string no_touch_contract;
   string execution_status;
};

struct FP_Level26BrokerValidatorReport
{
   bool attempted;
   bool ok;
   string status;
   string reason;
   int files_written;
   int file_errors;
   bool validator_written;
};

void FP_ResetLevel26BrokerValidatorConfig(FP_Level26BrokerValidatorConfig &cfg)
{
   cfg.enabled = true;
   cfg.export_csv = true;
   cfg.print_summary = false;

   cfg.require_dry_run_built = true;
   cfg.require_tick_alignment = true;
   cfg.require_stop_distance = true;
   cfg.require_normalized_prices = true;
   cfg.require_zero_volume = true;
   cfg.require_dry_run_only = true;

   cfg.folder = FP_LEVEL26_BROKER_VALIDATOR_DEFAULT_FOLDER;
}

void FP_ResetLevel26BrokerValidatorRow(FP_Level26BrokerValidatorRow &r)
{
   r.generated_at = 0;
   r.version = FP_LEVEL26_BROKER_VALIDATOR_VERSION;
   r.symbol = "";
   r.period = PERIOD_CURRENT;
   r.period_label = "";

   r.attempted = false;
   r.validator_passed = false;
   r.validator_status = "BROKER_VALIDATOR_RESET";
   r.validator_block_reason = "RESET";
   r.validator_key = "";

   r.dry_run_status = "";
   r.dry_run_request_built = false;
   r.dry_run_only = true;
   r.request_id = "";
   r.request_order_type = "ORDER_TYPE_NONE";
   r.request_direction = "DIRECTION_NONE";

   r.request_volume = 0.0;
   r.request_price = 0.0;
   r.request_sl = 0.0;
   r.request_tp = 0.0;

   r.symbol_digits = 0;
   r.symbol_point = 0.0;
   r.symbol_tick_size = 0.0;
   r.symbol_stops_level_points = 0;
   r.min_stop_distance_price = 0.0;

   r.normalized_price = 0.0;
   r.normalized_sl = 0.0;
   r.normalized_tp = 0.0;

   r.price_normalized = false;
   r.sl_normalized = false;
   r.tp_normalized = false;

   r.price_tick_aligned = false;
   r.sl_tick_aligned = false;
   r.tp_tick_aligned = false;

   r.stop_distance_price = 0.0;
   r.target_distance_price = 0.0;
   r.stop_distance_points = 0.0;
   r.target_distance_points = 0.0;

   r.stop_distance_ok = false;
   r.target_distance_ok = false;
   r.zero_volume_ok = false;
   r.price_geometry_ok = false;

   r.no_send_contract = "NO_ORDER_SEND_NO_ORDER_CHECK_NO_CTRADE";
   r.no_touch_contract = "BROKER_VALIDATOR_ONLY_NO_ORDER_NO_BROKER_NO_RENDERER_MUTATION";
   r.execution_status = "REAL_EXECUTION_DISABLED_LEVEL26_BROKER_VALIDATOR_ONLY";
}

void FP_ResetLevel26BrokerValidatorReport(FP_Level26BrokerValidatorReport &r)
{
   r.attempted = false;
   r.ok = false;
   r.status = "not_attempted";
   r.reason = "not_attempted";
   r.files_written = 0;
   r.file_errors = 0;
   r.validator_written = false;
}

#endif // __FP_BROKER_VALIDATOR_TYPES_MQH__
