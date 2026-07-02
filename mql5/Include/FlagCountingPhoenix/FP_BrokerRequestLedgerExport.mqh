#ifndef __FP_BROKER_REQUEST_LEDGER_EXPORT_MQH__
#define __FP_BROKER_REQUEST_LEDGER_EXPORT_MQH__
#property strict

#include "FP_BrokerRequestLedgerRules.mqh"

string FP_L27BrokerRequestLedgerPath(const FP_Level27BrokerRequestLedgerConfig &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL27_BROKER_REQUEST_LEDGER_DEFAULT_FOLDER;
   return folder + "\\state_gate_level27_broker_request_ledger.csv";
}

string FP_L27BrokerRequestLatestPath(const FP_Level27BrokerRequestLedgerConfig &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL27_BROKER_REQUEST_LEDGER_DEFAULT_FOLDER;
   return folder + "\\latest_state_gate_level27_broker_request_ledger.csv";
}

string FP_L27BrokerRequestLedgerHeader()
{
   string h = "";
   h += "generated_at,version,symbol,period,attempted,ledger_written,latest_written,duplicate_skipped,ledger_status,ledger_reason,ledger_id,ledger_key";
   h += ",request_id,request_key,request_built,dry_run_only,dry_run_status,dry_run_block_reason";
   h += ",validator_passed,validator_status,validator_block_reason,validator_key";
   h += ",safety_gate_status,safety_gate_passed,safety_gate_block_reason";
   h += ",intent_id,intent_allowed,intent_status";
   h += ",request_order_type,request_direction,request_volume,request_price,request_sl,request_tp,request_magic,request_comment";
   h += ",price_normalized,sl_normalized,tp_normalized,price_tick_aligned,sl_tick_aligned,tp_tick_aligned,stop_distance_ok,target_distance_ok,zero_volume_ok,price_geometry_ok";
   h += ",ledger_sequence,no_send_contract,no_touch_contract,execution_status";
   return h;
}

string FP_L27BrokerRequestLedgerRowCsv(const FP_Level27BrokerRequestLedgerRow &r)
{
   string s = "";
   s += FP_L27SafeCsv(FP_L27Time(r.generated_at));
   s += "," + FP_L27SafeCsv(r.version);
   s += "," + FP_L27SafeCsv(r.symbol);
   s += "," + FP_L27SafeCsv(r.period_label);
   s += "," + FP_L27SafeCsv(FP_L27Bool(r.attempted));
   s += "," + FP_L27SafeCsv(FP_L27Bool(r.ledger_written));
   s += "," + FP_L27SafeCsv(FP_L27Bool(r.latest_written));
   s += "," + FP_L27SafeCsv(FP_L27Bool(r.duplicate_skipped));
   s += "," + FP_L27SafeCsv(r.ledger_status);
   s += "," + FP_L27SafeCsv(r.ledger_reason);
   s += "," + FP_L27SafeCsv(r.ledger_id);
   s += "," + FP_L27SafeCsv(r.ledger_key);

   s += "," + FP_L27SafeCsv(r.request_id);
   s += "," + FP_L27SafeCsv(r.request_key);
   s += "," + FP_L27SafeCsv(FP_L27Bool(r.request_built));
   s += "," + FP_L27SafeCsv(FP_L27Bool(r.dry_run_only));
   s += "," + FP_L27SafeCsv(r.dry_run_status);
   s += "," + FP_L27SafeCsv(r.dry_run_block_reason);

   s += "," + FP_L27SafeCsv(FP_L27Bool(r.validator_passed));
   s += "," + FP_L27SafeCsv(r.validator_status);
   s += "," + FP_L27SafeCsv(r.validator_block_reason);
   s += "," + FP_L27SafeCsv(r.validator_key);

   s += "," + FP_L27SafeCsv(r.safety_gate_status);
   s += "," + FP_L27SafeCsv(FP_L27Bool(r.safety_gate_passed));
   s += "," + FP_L27SafeCsv(r.safety_gate_block_reason);

   s += "," + FP_L27SafeCsv(r.intent_id);
   s += "," + FP_L27SafeCsv(FP_L27Bool(r.intent_allowed));
   s += "," + FP_L27SafeCsv(r.intent_status);

   s += "," + FP_L27SafeCsv(r.request_order_type);
   s += "," + FP_L27SafeCsv(r.request_direction);
   s += "," + DoubleToString(r.request_volume, 2);
   s += "," + DoubleToString(r.request_price, _Digits);
   s += "," + DoubleToString(r.request_sl, _Digits);
   s += "," + DoubleToString(r.request_tp, _Digits);
   s += "," + IntegerToString((int)r.request_magic);
   s += "," + FP_L27SafeCsv(r.request_comment);

   s += "," + FP_L27SafeCsv(FP_L27Bool(r.price_normalized));
   s += "," + FP_L27SafeCsv(FP_L27Bool(r.sl_normalized));
   s += "," + FP_L27SafeCsv(FP_L27Bool(r.tp_normalized));
   s += "," + FP_L27SafeCsv(FP_L27Bool(r.price_tick_aligned));
   s += "," + FP_L27SafeCsv(FP_L27Bool(r.sl_tick_aligned));
   s += "," + FP_L27SafeCsv(FP_L27Bool(r.tp_tick_aligned));
   s += "," + FP_L27SafeCsv(FP_L27Bool(r.stop_distance_ok));
   s += "," + FP_L27SafeCsv(FP_L27Bool(r.target_distance_ok));
   s += "," + FP_L27SafeCsv(FP_L27Bool(r.zero_volume_ok));
   s += "," + FP_L27SafeCsv(FP_L27Bool(r.price_geometry_ok));

   s += "," + IntegerToString(r.ledger_sequence);
   s += "," + FP_L27SafeCsv(r.no_send_contract);
   s += "," + FP_L27SafeCsv(r.no_touch_contract);
   s += "," + FP_L27SafeCsv(r.execution_status);
   return s;
}

bool FP_L27WriteLatestBrokerRequestLedger(const FP_Level27BrokerRequestLedgerConfig &cfg,
                                          const FP_Level27BrokerRequestLedgerRow &row,
                                          FP_Level27BrokerRequestLedgerReport &report)
{
   if(!cfg.export_csv)
      return true;

    if(!cfg.write_latest_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL27_BROKER_REQUEST_LEDGER_DEFAULT_FOLDER;
   FolderCreate(folder);

   int handle = FileOpen(FP_L27BrokerRequestLatestPath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "level27_broker_request_latest_open_failed";
      return false;
   }

   FileWriteString(handle, FP_L27BrokerRequestLedgerHeader() + "\r\n");
   FileWriteString(handle, FP_L27BrokerRequestLedgerRowCsv(row) + "\r\n");
   FileClose(handle);

   report.files_written++;
   report.latest_written = true;
   return true;
}

bool FP_L27AppendBrokerRequestLedger(const FP_Level27BrokerRequestLedgerConfig &cfg,
                                     const FP_Level27BrokerRequestLedgerRow &row,
                                     FP_Level27BrokerRequestLedgerReport &report)
{
   if(!cfg.export_csv)
      return true;

    if(!cfg.append_ledger_csv)
      return true;

   if(row.duplicate_skipped)
   {
      report.duplicate_skipped = true;
      return true;
   }

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL27_BROKER_REQUEST_LEDGER_DEFAULT_FOLDER;
   FolderCreate(folder);

   string path = FP_L27BrokerRequestLedgerPath(cfg);
   bool exists = FileIsExist(path);
   int handle = INVALID_HANDLE;

   if(!exists)
   {
      handle = FileOpen(path, FILE_WRITE|FILE_TXT|FILE_ANSI);
      if(handle == INVALID_HANDLE)
      {
         report.file_errors++;
         report.reason = "level27_broker_request_ledger_create_failed";
         return false;
      }
      FileWriteString(handle, FP_L27BrokerRequestLedgerHeader() + "\r\n");
   }
   else
   {
      handle = FileOpen(path, FILE_READ|FILE_WRITE|FILE_TXT|FILE_ANSI);
      if(handle == INVALID_HANDLE)
      {
         report.file_errors++;
         report.reason = "level27_broker_request_ledger_open_failed";
         return false;
      }
      FileSeek(handle, 0, SEEK_END);
   }

   FileWriteString(handle, FP_L27BrokerRequestLedgerRowCsv(row) + "\r\n");
   FileClose(handle);

   report.files_written++;
   report.ledger_written = true;
   return true;
}

#endif // __FP_BROKER_REQUEST_LEDGER_EXPORT_MQH__
