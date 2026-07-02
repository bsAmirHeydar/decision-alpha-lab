#ifndef __FP_PAPER_BROKER_ADAPTER_EXPORT_MQH__
#define __FP_PAPER_BROKER_ADAPTER_EXPORT_MQH__
#property strict

#include "FP_PaperBrokerAdapterRules.mqh"

string FP_L29PaperBrokerAdapterPath(const FP_Level29PaperBrokerAdapterConfig &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL29_PAPER_BROKER_ADAPTER_DEFAULT_FOLDER;
   return folder + "\\state_gate_level29_paper_broker_adapter.csv";
}

string FP_L29PaperBrokerAdapterLatestPath(const FP_Level29PaperBrokerAdapterConfig &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL29_PAPER_BROKER_ADAPTER_DEFAULT_FOLDER;
   return folder + "\\latest_state_gate_level29_paper_broker_adapter.csv";
}

string FP_L29PaperBrokerAdapterHeader()
{
   string h = "";
   h += "generated_at,version,symbol,period,attempted,adapter_registered,adapter_written,latest_written,duplicate_skipped,adapter_status,adapter_block_reason,adapter_id,adapter_key";
   h += ",virtual_ticket,adapter_sequence,paper_order_state,paper_order_lifecycle_hint";
   h += ",request_id,request_key,request_built,dry_run_only,dry_run_status";
   h += ",validator_passed,validator_status,validator_block_reason";
   h += ",audit_passed,audit_status,audit_block_reason";
   h += ",request_order_type,request_direction,request_volume,request_price,request_sl,request_tp,request_magic,request_comment";
   h += ",zero_volume_ok,dry_run_only_ok,no_send_contract_ok,adapter_chain_coherence_ok,adapter_runtime_state";
   h += ",no_send_contract,no_touch_contract,execution_status";
   return h;
}

string FP_L29PaperBrokerAdapterRowCsv(const FP_Level29PaperBrokerAdapterRow &r)
{
   string s = "";
   s += FP_L29SafeCsv(FP_L29Time(r.generated_at));
   s += "," + FP_L29SafeCsv(r.version);
   s += "," + FP_L29SafeCsv(r.symbol);
   s += "," + FP_L29SafeCsv(r.period_label);
   s += "," + FP_L29SafeCsv(FP_L29Bool(r.attempted));
   s += "," + FP_L29SafeCsv(FP_L29Bool(r.adapter_registered));
   s += "," + FP_L29SafeCsv(FP_L29Bool(r.adapter_written));
   s += "," + FP_L29SafeCsv(FP_L29Bool(r.latest_written));
   s += "," + FP_L29SafeCsv(FP_L29Bool(r.duplicate_skipped));
   s += "," + FP_L29SafeCsv(r.adapter_status);
   s += "," + FP_L29SafeCsv(r.adapter_block_reason);
   s += "," + FP_L29SafeCsv(r.adapter_id);
   s += "," + FP_L29SafeCsv(r.adapter_key);

   s += "," + FP_L29SafeCsv(r.virtual_ticket);
   s += "," + IntegerToString(r.adapter_sequence);
   s += "," + FP_L29SafeCsv(r.paper_order_state);
   s += "," + FP_L29SafeCsv(r.paper_order_lifecycle_hint);

   s += "," + FP_L29SafeCsv(r.request_id);
   s += "," + FP_L29SafeCsv(r.request_key);
   s += "," + FP_L29SafeCsv(FP_L29Bool(r.request_built));
   s += "," + FP_L29SafeCsv(FP_L29Bool(r.dry_run_only));
   s += "," + FP_L29SafeCsv(r.dry_run_status);

   s += "," + FP_L29SafeCsv(FP_L29Bool(r.validator_passed));
   s += "," + FP_L29SafeCsv(r.validator_status);
   s += "," + FP_L29SafeCsv(r.validator_block_reason);

   s += "," + FP_L29SafeCsv(FP_L29Bool(r.audit_passed));
   s += "," + FP_L29SafeCsv(r.audit_status);
   s += "," + FP_L29SafeCsv(r.audit_block_reason);

   s += "," + FP_L29SafeCsv(r.request_order_type);
   s += "," + FP_L29SafeCsv(r.request_direction);
   s += "," + DoubleToString(r.request_volume, 2);
   s += "," + DoubleToString(r.request_price, _Digits);
   s += "," + DoubleToString(r.request_sl, _Digits);
   s += "," + DoubleToString(r.request_tp, _Digits);
   s += "," + IntegerToString((int)r.request_magic);
   s += "," + FP_L29SafeCsv(r.request_comment);

   s += "," + FP_L29SafeCsv(FP_L29Bool(r.zero_volume_ok));
   s += "," + FP_L29SafeCsv(FP_L29Bool(r.dry_run_only_ok));
   s += "," + FP_L29SafeCsv(FP_L29Bool(r.no_send_contract_ok));
   s += "," + FP_L29SafeCsv(FP_L29Bool(r.adapter_chain_coherence_ok));
   s += "," + FP_L29SafeCsv(r.adapter_runtime_state);

   s += "," + FP_L29SafeCsv(r.no_send_contract);
   s += "," + FP_L29SafeCsv(r.no_touch_contract);
   s += "," + FP_L29SafeCsv(r.execution_status);
   return s;
}

bool FP_L29WriteLatestPaperBrokerAdapter(const FP_Level29PaperBrokerAdapterConfig &cfg,
                                         const FP_Level29PaperBrokerAdapterRow &row,
                                         FP_Level29PaperBrokerAdapterReport &report)
{
   if(!cfg.export_csv)
      return true;

    if(!cfg.write_latest_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL29_PAPER_BROKER_ADAPTER_DEFAULT_FOLDER;
   FolderCreate(folder);

   int handle = FileOpen(FP_L29PaperBrokerAdapterLatestPath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "level29_paper_broker_adapter_latest_open_failed";
      return false;
   }

   FileWriteString(handle, FP_L29PaperBrokerAdapterHeader() + "\r\n");
   FileWriteString(handle, FP_L29PaperBrokerAdapterRowCsv(row) + "\r\n");
   FileClose(handle);

   report.files_written++;
   report.latest_written = true;
   return true;
}

bool FP_L29AppendPaperBrokerAdapter(const FP_Level29PaperBrokerAdapterConfig &cfg,
                                    const FP_Level29PaperBrokerAdapterRow &row,
                                    FP_Level29PaperBrokerAdapterReport &report)
{
   if(!cfg.export_csv)
      return true;

    if(!cfg.append_adapter_csv)
      return true;

   if(row.duplicate_skipped)
   {
      report.duplicate_skipped = true;
      return true;
   }

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL29_PAPER_BROKER_ADAPTER_DEFAULT_FOLDER;
   FolderCreate(folder);

   string path = FP_L29PaperBrokerAdapterPath(cfg);
   bool exists = FileIsExist(path);
   int handle = INVALID_HANDLE;

   if(!exists)
   {
      handle = FileOpen(path, FILE_WRITE|FILE_TXT|FILE_ANSI);
      if(handle == INVALID_HANDLE)
      {
         report.file_errors++;
         report.reason = "level29_paper_broker_adapter_create_failed";
         return false;
      }
      FileWriteString(handle, FP_L29PaperBrokerAdapterHeader() + "\r\n");
   }
   else
   {
      handle = FileOpen(path, FILE_READ|FILE_WRITE|FILE_TXT|FILE_ANSI);
      if(handle == INVALID_HANDLE)
      {
         report.file_errors++;
         report.reason = "level29_paper_broker_adapter_open_failed";
         return false;
      }
      FileSeek(handle, 0, SEEK_END);
   }

   FileWriteString(handle, FP_L29PaperBrokerAdapterRowCsv(row) + "\r\n");
   FileClose(handle);

   report.files_written++;
   report.adapter_written = true;
   return true;
}

#endif // __FP_PAPER_BROKER_ADAPTER_EXPORT_MQH__
