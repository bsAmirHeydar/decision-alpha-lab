#ifndef __FP_BROKER_DRY_RUN_EXPORT_MQH__
#define __FP_BROKER_DRY_RUN_EXPORT_MQH__
#property strict

#include "FP_BrokerDryRunRules.mqh"

string FP_L25BrokerDryRunPath(const FP_Level25BrokerDryRunConfig &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL25_BROKER_DRY_RUN_DEFAULT_FOLDER;
   return folder + "\\state_gate_level25_broker_dry_run.csv";
}

string FP_L25BrokerDryRunHeader()
{
   string h = "";
   h += "generated_at,version,symbol,period,attempted,request_built,dry_run_only,dry_run_status,block_reason,request_id,request_key";
   h += ",safety_gate_status,safety_gate_passed,safety_gate_block_reason";
   h += ",intent_id,intent_allowed,intent_status";
   h += ",request_action,request_order_type,request_direction";
   h += ",request_volume,request_price,request_sl,request_tp,request_deviation_points,request_magic,request_comment";
   h += ",entry_price,stop_price,target_price,risk_distance,reward_distance,rr_like";
   h += ",price_geometry_status,request_validity_status,no_touch_contract,execution_status";
   return h;
}

string FP_L25BrokerDryRunRowCsv(const FP_Level25BrokerDryRunRow &r)
{
   string s = "";
   s += FP_L25SafeCsv(FP_L25Time(r.generated_at));
   s += "," + FP_L25SafeCsv(r.version);
   s += "," + FP_L25SafeCsv(r.symbol);
   s += "," + FP_L25SafeCsv(r.period_label);
   s += "," + FP_L25SafeCsv(FP_L25Bool(r.attempted));
   s += "," + FP_L25SafeCsv(FP_L25Bool(r.request_built));
   s += "," + FP_L25SafeCsv(FP_L25Bool(r.dry_run_only));
   s += "," + FP_L25SafeCsv(r.dry_run_status);
   s += "," + FP_L25SafeCsv(r.block_reason);
   s += "," + FP_L25SafeCsv(r.request_id);
   s += "," + FP_L25SafeCsv(r.request_key);

   s += "," + FP_L25SafeCsv(r.safety_gate_status);
   s += "," + FP_L25SafeCsv(FP_L25Bool(r.safety_gate_passed));
   s += "," + FP_L25SafeCsv(r.safety_gate_block_reason);

   s += "," + FP_L25SafeCsv(r.intent_id);
   s += "," + FP_L25SafeCsv(FP_L25Bool(r.intent_allowed));
   s += "," + FP_L25SafeCsv(r.intent_status);

   s += "," + FP_L25SafeCsv(r.request_action);
   s += "," + FP_L25SafeCsv(r.request_order_type);
   s += "," + FP_L25SafeCsv(r.request_direction);

   s += "," + DoubleToString(r.request_volume, 2);
   s += "," + DoubleToString(r.request_price, _Digits);
   s += "," + DoubleToString(r.request_sl, _Digits);
   s += "," + DoubleToString(r.request_tp, _Digits);
   s += "," + DoubleToString(r.request_deviation_points, 1);
   s += "," + IntegerToString((int)r.request_magic);
   s += "," + FP_L25SafeCsv(r.request_comment);

   s += "," + DoubleToString(r.entry_price, _Digits);
   s += "," + DoubleToString(r.stop_price, _Digits);
   s += "," + DoubleToString(r.target_price, _Digits);
   s += "," + DoubleToString(r.risk_distance, _Digits);
   s += "," + DoubleToString(r.reward_distance, _Digits);
   s += "," + DoubleToString(r.rr_like, 4);

   s += "," + FP_L25SafeCsv(r.price_geometry_status);
   s += "," + FP_L25SafeCsv(r.request_validity_status);
   s += "," + FP_L25SafeCsv(r.no_touch_contract);
   s += "," + FP_L25SafeCsv(r.execution_status);
   return s;
}

bool FP_L25ExportBrokerDryRun(const FP_Level25BrokerDryRunConfig &cfg,
                              const FP_Level25BrokerDryRunRow &row,
                              FP_Level25BrokerDryRunReport &report)
{
   if(!cfg.export_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL25_BROKER_DRY_RUN_DEFAULT_FOLDER;
   FolderCreate(folder);

   int handle = FileOpen(FP_L25BrokerDryRunPath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "level25_broker_dry_run_export_open_failed";
      return false;
   }

   FileWriteString(handle, FP_L25BrokerDryRunHeader() + "\r\n");
   FileWriteString(handle, FP_L25BrokerDryRunRowCsv(row) + "\r\n");
   FileClose(handle);

   report.files_written++;
   report.dry_run_written = true;
   return true;
}

#endif // __FP_BROKER_DRY_RUN_EXPORT_MQH__
