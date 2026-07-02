#ifndef __FP_BROKER_VALIDATOR_RULES_MQH__
#define __FP_BROKER_VALIDATOR_RULES_MQH__
#property strict

#include "FP_BrokerValidatorTypes.mqh"
#include "FP_BrokerDryRunRules.mqh"

string FP_L26Bool(const bool v){ return (v ? "true" : "false"); }
string FP_L26Time(const datetime t){ if(t <= 0) return ""; return TimeToString(t, TIME_DATE|TIME_SECONDS); }
string FP_L26SafeCsv(string v){ StringReplace(v, "\"", "\"\""); return "\"" + v + "\""; }
string FP_L26TfLabel(const ENUM_TIMEFRAMES tf){ return EnumToString(tf); }

double FP_L26AbsDouble(const double v)
{
   if(v < 0.0) return -v;
   return v;
}

bool FP_L26NearlyEqual(const double a,const double b,const double tolerance)
{
   return (FP_L26AbsDouble(a - b) <= tolerance);
}

double FP_L26NormalizeByDigits(const double value,const int digits)
{
   if(value <= 0.0) return 0.0;
   return NormalizeDouble(value, digits);
}

bool FP_L26PriceNormalized(const double price,const double normalized,const double point_value)
{
   double tolerance = point_value * 0.1;
   if(tolerance <= 0.0) tolerance = 0.00000001;
   return FP_L26NearlyEqual(price, normalized, tolerance);
}

bool FP_L26TickAligned(const double price,const double tick_size,const double point_value)
{
   if(price <= 0.0) return false;
   if(tick_size <= 0.0) return true;

   double steps = price / tick_size;
   double rounded_steps = MathRound(steps);
   double rebuilt = rounded_steps * tick_size;

   double tolerance = point_value * 0.25;
   if(tolerance <= 0.0) tolerance = tick_size * 0.1;
   if(tolerance <= 0.0) tolerance = 0.00000001;

   return FP_L26NearlyEqual(price, rebuilt, tolerance);
}

bool FP_L26DirectionalGeometryOk(const string direction,
                                 const double price,
                                 const double sl,
                                 const double tp)
{
   if(direction == "DIRECTION_BULLISH")
      return (sl < price && tp > price);
   if(direction == "DIRECTION_BEARISH")
      return (sl > price && tp < price);
   return false;
}

double FP_L26Distance(const double a,const double b)
{
   return FP_L26AbsDouble(a - b);
}

bool FP_L26DistanceOk(const double distance_price,const double min_distance_price)
{
   if(min_distance_price <= 0.0)
      return true;
   return (distance_price >= min_distance_price);
}

string FP_L26FirstBlockReason(const FP_Level26BrokerValidatorConfig &cfg,
                              const FP_Level26BrokerValidatorRow &row)
{
   if(cfg.require_dry_run_only && !row.dry_run_only)
      return "BLOCK_DRY_RUN_ONLY_FALSE";
   if(cfg.require_dry_run_built && !row.dry_run_request_built)
      return "BLOCK_DRY_RUN_REQUEST_NOT_BUILT";
   if(cfg.require_zero_volume && !row.zero_volume_ok)
      return "BLOCK_VOLUME_NOT_ZERO";
   if(!row.price_geometry_ok)
      return "BLOCK_PRICE_GEOMETRY";
   if(cfg.require_normalized_prices && !row.price_normalized)
      return "BLOCK_PRICE_NOT_NORMALIZED";
   if(cfg.require_normalized_prices && !row.sl_normalized)
      return "BLOCK_SL_NOT_NORMALIZED";
   if(cfg.require_normalized_prices && !row.tp_normalized)
      return "BLOCK_TP_NOT_NORMALIZED";
   if(cfg.require_tick_alignment && !row.price_tick_aligned)
      return "BLOCK_PRICE_NOT_TICK_ALIGNED";
   if(cfg.require_tick_alignment && !row.sl_tick_aligned)
      return "BLOCK_SL_NOT_TICK_ALIGNED";
   if(cfg.require_tick_alignment && !row.tp_tick_aligned)
      return "BLOCK_TP_NOT_TICK_ALIGNED";
   if(cfg.require_stop_distance && !row.stop_distance_ok)
      return "BLOCK_STOP_DISTANCE_TOO_SMALL";
   if(cfg.require_stop_distance && !row.target_distance_ok)
      return "BLOCK_TARGET_DISTANCE_TOO_SMALL";
   return "none";
}

void FP_L26BuildBrokerValidatorRow(const string symbol,
                                   const ENUM_TIMEFRAMES period,
                                   const FP_Level25BrokerDryRunRow &dry_run,
                                   const FP_Level26BrokerValidatorConfig &cfg,
                                   FP_Level26BrokerValidatorRow &row)
{
   FP_ResetLevel26BrokerValidatorRow(row);

   row.generated_at = TimeCurrent();
   row.symbol = symbol;
   row.period = period;
   row.period_label = FP_L26TfLabel(period);
   row.attempted = cfg.enabled;

   row.dry_run_status = dry_run.dry_run_status;
   row.dry_run_request_built = dry_run.request_built;
   row.dry_run_only = dry_run.dry_run_only;
   row.request_id = dry_run.request_id;
   row.request_order_type = dry_run.request_order_type;
   row.request_direction = dry_run.request_direction;

   row.request_volume = dry_run.request_volume;
   row.request_price = dry_run.request_price;
   row.request_sl = dry_run.request_sl;
   row.request_tp = dry_run.request_tp;

   row.symbol_digits = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
   row.symbol_point = SymbolInfoDouble(symbol, SYMBOL_POINT);
   row.symbol_tick_size = SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_SIZE);
   row.symbol_stops_level_points = (int)SymbolInfoInteger(symbol, SYMBOL_TRADE_STOPS_LEVEL);

   if(row.symbol_point <= 0.0)
      row.symbol_point = _Point;
   if(row.symbol_tick_size <= 0.0)
      row.symbol_tick_size = row.symbol_point;

   row.min_stop_distance_price = (double)row.symbol_stops_level_points * row.symbol_point;

   row.normalized_price = FP_L26NormalizeByDigits(row.request_price, row.symbol_digits);
   row.normalized_sl = FP_L26NormalizeByDigits(row.request_sl, row.symbol_digits);
   row.normalized_tp = FP_L26NormalizeByDigits(row.request_tp, row.symbol_digits);

   row.price_normalized = FP_L26PriceNormalized(row.request_price, row.normalized_price, row.symbol_point);
   row.sl_normalized = FP_L26PriceNormalized(row.request_sl, row.normalized_sl, row.symbol_point);
   row.tp_normalized = FP_L26PriceNormalized(row.request_tp, row.normalized_tp, row.symbol_point);

   row.price_tick_aligned = FP_L26TickAligned(row.request_price, row.symbol_tick_size, row.symbol_point);
   row.sl_tick_aligned = FP_L26TickAligned(row.request_sl, row.symbol_tick_size, row.symbol_point);
   row.tp_tick_aligned = FP_L26TickAligned(row.request_tp, row.symbol_tick_size, row.symbol_point);

   row.stop_distance_price = FP_L26Distance(row.request_price, row.request_sl);
   row.target_distance_price = FP_L26Distance(row.request_tp, row.request_price);

   if(row.symbol_point > 0.0)
   {
      row.stop_distance_points = row.stop_distance_price / row.symbol_point;
      row.target_distance_points = row.target_distance_price / row.symbol_point;
   }

   row.stop_distance_ok = FP_L26DistanceOk(row.stop_distance_price, row.min_stop_distance_price);
   row.target_distance_ok = FP_L26DistanceOk(row.target_distance_price, row.min_stop_distance_price);
   row.zero_volume_ok = (row.request_volume == 0.0);
   row.price_geometry_ok = FP_L26DirectionalGeometryOk(row.request_direction,
                                                       row.request_price,
                                                       row.request_sl,
                                                       row.request_tp);

   string block = FP_L26FirstBlockReason(cfg, row);
   row.validator_passed = (block == "none");

   if(row.validator_passed)
   {
      row.validator_status = "BROKER_VALIDATOR_PASSED_NO_SEND";
      row.validator_block_reason = "none";
   }
   else
   {
      row.validator_status = "BROKER_VALIDATOR_BLOCKED";
      row.validator_block_reason = block;
   }

   row.validator_key = row.symbol;
   row.validator_key += "|TF=" + row.period_label;
   row.validator_key += "|REQ=" + row.request_id;
   row.validator_key += "|PASSED=" + FP_L26Bool(row.validator_passed);
   row.validator_key += "|BLOCK=" + row.validator_block_reason;
   row.validator_key += "|NO_SEND=true";
   row.validator_key += "|EXEC=NO";
}

#endif // __FP_BROKER_VALIDATOR_RULES_MQH__
