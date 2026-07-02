#ifndef __FP_BROKER_DRY_RUN_RULES_MQH__
#define __FP_BROKER_DRY_RUN_RULES_MQH__
#property strict

#include "FP_BrokerDryRunTypes.mqh"
#include "FP_SafetyGateRules.mqh"
#include "FP_PaperIntentRules.mqh"

string FP_L25Bool(const bool v){ return (v ? "true" : "false"); }
string FP_L25Time(const datetime t){ if(t <= 0) return ""; return TimeToString(t, TIME_DATE|TIME_SECONDS); }
string FP_L25SafeCsv(string v){ StringReplace(v, "\"", "\"\""); return "\"" + v + "\""; }
string FP_L25TfLabel(const ENUM_TIMEFRAMES tf){ return EnumToString(tf); }

string FP_L25DirectionLabel(const int direction)
{
   if(direction == FP_DIR_BULLISH) return "DIRECTION_BULLISH";
   if(direction == FP_DIR_BEARISH) return "DIRECTION_BEARISH";
   return "DIRECTION_NONE";
}

string FP_L25OrderTypeFromDirection(const int direction)
{
   if(direction == FP_DIR_BULLISH)
      return "ORDER_TYPE_BUY_LIMIT_PREVIEW";
   if(direction == FP_DIR_BEARISH)
      return "ORDER_TYPE_SELL_LIMIT_PREVIEW";
   return "ORDER_TYPE_NONE";
}

string FP_L25PriceGeometryStatus(const FP_Level21PaperIntentRow &intent)
{
   if(intent.direction == FP_DIR_NONE)
      return "PRICE_GEOMETRY_BLOCKED_NO_DIRECTION";
   if(intent.entry_price <= 0.0)
      return "PRICE_GEOMETRY_BLOCKED_NO_ENTRY";
   if(intent.stop_price <= 0.0)
      return "PRICE_GEOMETRY_BLOCKED_NO_STOP";
   if(intent.target_price <= 0.0)
      return "PRICE_GEOMETRY_BLOCKED_NO_TARGET";

   if(intent.direction == FP_DIR_BULLISH)
   {
      if(intent.stop_price < intent.entry_price && intent.target_price > intent.entry_price)
         return "PRICE_GEOMETRY_OK_BULLISH";
      return "PRICE_GEOMETRY_BLOCKED_BULLISH";
   }

   if(intent.direction == FP_DIR_BEARISH)
   {
      if(intent.stop_price > intent.entry_price && intent.target_price < intent.entry_price)
         return "PRICE_GEOMETRY_OK_BEARISH";
      return "PRICE_GEOMETRY_BLOCKED_BEARISH";
   }

   return "PRICE_GEOMETRY_BLOCKED_UNKNOWN";
}

string FP_L25BuildRequestId(const FP_Level21PaperIntentRow &intent)
{
   string id = "DRYRUN";
   id += "_" + intent.symbol;
   id += "_" + intent.period_label;
   id += "_" + intent.intent_id;
   id += "_" + FP_L25DirectionLabel(intent.direction);
   id += "_" + DoubleToString(intent.entry_price, _Digits);
   id += "_" + DoubleToString(intent.stop_price, _Digits);
   id += "_" + DoubleToString(intent.target_price, _Digits);
   return id;
}

void FP_L25BuildBrokerDryRunRow(const string symbol,
                                const ENUM_TIMEFRAMES period,
                                const FP_Level24SafetyGateRow &safety,
                                const FP_Level21PaperIntentRow &intent,
                                const FP_Level25BrokerDryRunConfig &cfg,
                                FP_Level25BrokerDryRunRow &row)
{
   FP_ResetLevel25BrokerDryRunRow(row);

   row.generated_at = TimeCurrent();
   row.symbol = symbol;
   row.period = period;
   row.period_label = FP_L25TfLabel(period);
   row.attempted = cfg.enabled;
   row.dry_run_only = cfg.dry_run_only;

   row.safety_gate_status = safety.gate_status;
   row.safety_gate_passed = safety.gate_passed;
   row.safety_gate_block_reason = safety.gate_block_reason;

   row.intent_id = intent.intent_id;
   row.intent_allowed = intent.allowed;
   row.intent_status = intent.intent_status;

   row.request_action = "TRADE_ACTION_PENDING_PREVIEW_ONLY";
   row.request_order_type = FP_L25OrderTypeFromDirection(intent.direction);
   row.request_direction = FP_L25DirectionLabel(intent.direction);

   row.entry_price = intent.entry_price;
   row.stop_price = intent.stop_price;
   row.target_price = intent.target_price;
   row.risk_distance = intent.risk_distance;
   row.reward_distance = intent.reward_distance;
   row.rr_like = intent.rr_like;

   row.request_price = intent.entry_price;
   row.request_sl = intent.stop_price;
   row.request_tp = intent.target_price;

   // Intentionally zero. Level 25 must not size risk or volume.
   row.request_volume = 0.0;
   row.request_deviation_points = 0.0;

   row.request_magic = cfg.magic;
   row.request_comment = cfg.request_comment;

   row.price_geometry_status = FP_L25PriceGeometryStatus(intent);
   row.request_id = FP_L25BuildRequestId(intent);

   if(!cfg.dry_run_only)
   {
      row.request_built = false;
      row.dry_run_status = "BROKER_DRY_RUN_BLOCKED_DRY_RUN_ONLY_FALSE";
      row.block_reason = "dry_run_only_must_remain_true";
      row.request_validity_status = "REQUEST_INVALID_DRY_RUN_FLAG";
   }
   else if(cfg.require_safety_gate_passed && !safety.gate_passed)
   {
      row.request_built = false;
      row.dry_run_status = "BROKER_DRY_RUN_BLOCKED_SAFETY_GATE";
      row.block_reason = safety.gate_block_reason;
      row.request_validity_status = "REQUEST_BLOCKED_BY_SAFETY_GATE";
   }
   else if(cfg.require_intent_allowed && !intent.allowed)
   {
      row.request_built = false;
      row.dry_run_status = "BROKER_DRY_RUN_BLOCKED_INTENT_NOT_ALLOWED";
      row.block_reason = intent.intent_status + ":" + intent.block_reason;
      row.request_validity_status = "REQUEST_BLOCKED_BY_INTENT";
   }
   else if(intent.direction == FP_DIR_NONE)
   {
      row.request_built = false;
      row.dry_run_status = "BROKER_DRY_RUN_BLOCKED_NO_DIRECTION";
      row.block_reason = "direction_missing";
      row.request_validity_status = "REQUEST_INVALID_NO_DIRECTION";
   }
   else if(row.request_price <= 0.0 || row.request_sl <= 0.0 || row.request_tp <= 0.0)
   {
      row.request_built = false;
      row.dry_run_status = "BROKER_DRY_RUN_BLOCKED_MISSING_PRICES";
      row.block_reason = "entry_sl_or_tp_missing";
      row.request_validity_status = "REQUEST_INVALID_MISSING_PRICES";
   }
   else if(StringFind(row.price_geometry_status, "OK") < 0)
   {
      row.request_built = false;
      row.dry_run_status = "BROKER_DRY_RUN_BLOCKED_PRICE_GEOMETRY";
      row.block_reason = row.price_geometry_status;
      row.request_validity_status = "REQUEST_INVALID_PRICE_GEOMETRY";
   }
   else
   {
      row.request_built = true;
      row.dry_run_status = "BROKER_DRY_RUN_REQUEST_BUILT_CSV_ONLY";
      row.block_reason = "none";
      row.request_validity_status = "REQUEST_VALID_DRY_RUN_PREVIEW_ONLY";
   }

   row.request_key = row.symbol;
   row.request_key += "|TF=" + row.period_label;
   row.request_key += "|ID=" + row.request_id;
   row.request_key += "|TYPE=" + row.request_order_type;
   row.request_key += "|BUILT=" + FP_L25Bool(row.request_built);
   row.request_key += "|DRY_RUN_ONLY=" + FP_L25Bool(row.dry_run_only);
   row.request_key += "|VOL=" + DoubleToString(row.request_volume, 2);
   row.request_key += "|EXEC=NO";
}

#endif // __FP_BROKER_DRY_RUN_RULES_MQH__
