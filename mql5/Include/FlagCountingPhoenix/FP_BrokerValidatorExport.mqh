#ifndef __FP_BROKER_VALIDATOR_EXPORT_MQH__
#define __FP_BROKER_VALIDATOR_EXPORT_MQH__
#property strict

#include "FP_BrokerValidatorRules.mqh"

string FP_L26BrokerValidatorPath(const FP_Level26BrokerValidatorConfig &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL26_BROKER_VALIDATOR_DEFAULT_FOLDER;
   return folder + "\\state_gate_level26_broker_validator.csv";
}

string FP_L26BrokerValidatorHeader()
{
   string h = "";
   h += "generated_at,version,symbol,period,attempted,validator_passed,validator_status,validator_block_reason,validator_key";
   h += ",dry_run_status,dry_run_request_built,dry_run_only,request_id,request_order_type,request_direction";
   h += ",request_volume,request_price,request_sl,request_tp";
   h += ",symbol_digits,symbol_point,symbol_tick_size,symbol_stops_level_points,min_stop_distance_price";
   h += ",normalized_price,normalized_sl,normalized_tp";
   h += ",price_normalized,sl_normalized,tp_normalized";
   h += ",price_tick_aligned,sl_tick_aligned,tp_tick_aligned";
   h += ",stop_distance_price,target_distance_price,stop_distance_points,target_distance_points";
   h += ",stop_distance_ok,target_distance_ok,zero_volume_ok,price_geometry_ok";
   h += ",no_send_contract,no_touch_contract,execution_status";
   return h;
}

string FP_L26BrokerValidatorRowCsv(const FP_Level26BrokerValidatorRow &r)
{
   string s = "";
   s += FP_L26SafeCsv(FP_L26Time(r.generated_at));
   s += "," + FP_L26SafeCsv(r.version);
   s += "," + FP_L26SafeCsv(r.symbol);
   s += "," + FP_L26SafeCsv(r.period_label);
   s += "," + FP_L26SafeCsv(FP_L26Bool(r.attempted));
   s += "," + FP_L26SafeCsv(FP_L26Bool(r.validator_passed));
   s += "," + FP_L26SafeCsv(r.validator_status);
   s += "," + FP_L26SafeCsv(r.validator_block_reason);
   s += "," + FP_L26SafeCsv(r.validator_key);

   s += "," + FP_L26SafeCsv(r.dry_run_status);
   s += "," + FP_L26SafeCsv(FP_L26Bool(r.dry_run_request_built));
   s += "," + FP_L26SafeCsv(FP_L26Bool(r.dry_run_only));
   s += "," + FP_L26SafeCsv(r.request_id);
   s += "," + FP_L26SafeCsv(r.request_order_type);
   s += "," + FP_L26SafeCsv(r.request_direction);

   s += "," + DoubleToString(r.request_volume, 2);
   s += "," + DoubleToString(r.request_price, r.symbol_digits);
   s += "," + DoubleToString(r.request_sl, r.symbol_digits);
   s += "," + DoubleToString(r.request_tp, r.symbol_digits);

   s += "," + IntegerToString(r.symbol_digits);
   s += "," + DoubleToString(r.symbol_point, r.symbol_digits);
   s += "," + DoubleToString(r.symbol_tick_size, r.symbol_digits);
   s += "," + IntegerToString(r.symbol_stops_level_points);
   s += "," + DoubleToString(r.min_stop_distance_price, r.symbol_digits);

   s += "," + DoubleToString(r.normalized_price, r.symbol_digits);
   s += "," + DoubleToString(r.normalized_sl, r.symbol_digits);
   s += "," + DoubleToString(r.normalized_tp, r.symbol_digits);

   s += "," + FP_L26SafeCsv(FP_L26Bool(r.price_normalized));
   s += "," + FP_L26SafeCsv(FP_L26Bool(r.sl_normalized));
   s += "," + FP_L26SafeCsv(FP_L26Bool(r.tp_normalized));

   s += "," + FP_L26SafeCsv(FP_L26Bool(r.price_tick_aligned));
   s += "," + FP_L26SafeCsv(FP_L26Bool(r.sl_tick_aligned));
   s += "," + FP_L26SafeCsv(FP_L26Bool(r.tp_tick_aligned));

   s += "," + DoubleToString(r.stop_distance_price, r.symbol_digits);
   s += "," + DoubleToString(r.target_distance_price, r.symbol_digits);
   s += "," + DoubleToString(r.stop_distance_points, 2);
   s += "," + DoubleToString(r.target_distance_points, 2);

   s += "," + FP_L26SafeCsv(FP_L26Bool(r.stop_distance_ok));
   s += "," + FP_L26SafeCsv(FP_L26Bool(r.target_distance_ok));
   s += "," + FP_L26SafeCsv(FP_L26Bool(r.zero_volume_ok));
   s += "," + FP_L26SafeCsv(FP_L26Bool(r.price_geometry_ok));

   s += "," + FP_L26SafeCsv(r.no_send_contract);
   s += "," + FP_L26SafeCsv(r.no_touch_contract);
   s += "," + FP_L26SafeCsv(r.execution_status);
   return s;
}

bool FP_L26ExportBrokerValidator(const FP_Level26BrokerValidatorConfig &cfg,
                                 const FP_Level26BrokerValidatorRow &row,
                                 FP_Level26BrokerValidatorReport &report)
{
   if(!cfg.export_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL26_BROKER_VALIDATOR_DEFAULT_FOLDER;
   FolderCreate(folder);

   int handle = FileOpen(FP_L26BrokerValidatorPath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "level26_broker_validator_export_open_failed";
      return false;
   }

   FileWriteString(handle, FP_L26BrokerValidatorHeader() + "\r\n");
   FileWriteString(handle, FP_L26BrokerValidatorRowCsv(row) + "\r\n");
   FileClose(handle);

   report.files_written++;
   report.validator_written = true;
   return true;
}

#endif // __FP_BROKER_VALIDATOR_EXPORT_MQH__
