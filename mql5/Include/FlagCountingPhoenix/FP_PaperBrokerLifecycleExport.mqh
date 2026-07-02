#ifndef __FP_PAPER_BROKER_LIFECYCLE_EXPORT_MQH__
#define __FP_PAPER_BROKER_LIFECYCLE_EXPORT_MQH__
#property strict

#include "FP_PaperBrokerLifecycleRules.mqh"

string FP_L30PaperBrokerLifecyclePath(const FP_Level30PaperBrokerLifecycleConfig &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL30_PAPER_BROKER_LIFECYCLE_DEFAULT_FOLDER;
   return folder + "\\state_gate_level30_paper_broker_lifecycle.csv";
}

string FP_L30PaperBrokerLifecycleLatestPath(const FP_Level30PaperBrokerLifecycleConfig &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL30_PAPER_BROKER_LIFECYCLE_DEFAULT_FOLDER;
   return folder + "\\latest_state_gate_level30_paper_broker_lifecycle.csv";
}

string FP_L30PaperBrokerLifecycleHeader()
{
   string h = "";
   h += "generated_at,version,symbol,period,attempted,lifecycle_tracked,lifecycle_written,latest_written,duplicate_skipped,lifecycle_status,lifecycle_block_reason,lifecycle_id,lifecycle_key";
   h += ",virtual_ticket,lifecycle_sequence,adapter_status,adapter_registered,adapter_block_reason";
   h += ",request_id,request_key,request_order_type,request_direction,request_volume,request_price,request_sl,request_tp";
   h += ",seed_time,entry_time,exit_time,seed_index,entry_index,exit_index,expiry_bars,bars_to_entry,bars_in_trade,bars_elapsed_total";
   h += ",entry_close,exit_close,best_close,worst_close,mfe_close_distance,mae_close_distance,risk_distance,reward_distance,realized_r_like";
   h += ",entry_condition,exit_condition,paper_order_state,paper_order_event,close_only_contract,no_send_contract,no_touch_contract,execution_status";
   return h;
}

string FP_L30PaperBrokerLifecycleRowCsv(const FP_Level30PaperBrokerLifecycleRow &r)
{
   string s = "";
   s += FP_L30SafeCsv(FP_L30Time(r.generated_at));
   s += "," + FP_L30SafeCsv(r.version);
   s += "," + FP_L30SafeCsv(r.symbol);
   s += "," + FP_L30SafeCsv(r.period_label);
   s += "," + FP_L30SafeCsv(FP_L30Bool(r.attempted));
   s += "," + FP_L30SafeCsv(FP_L30Bool(r.lifecycle_tracked));
   s += "," + FP_L30SafeCsv(FP_L30Bool(r.lifecycle_written));
   s += "," + FP_L30SafeCsv(FP_L30Bool(r.latest_written));
   s += "," + FP_L30SafeCsv(FP_L30Bool(r.duplicate_skipped));
   s += "," + FP_L30SafeCsv(r.lifecycle_status);
   s += "," + FP_L30SafeCsv(r.lifecycle_block_reason);
   s += "," + FP_L30SafeCsv(r.lifecycle_id);
   s += "," + FP_L30SafeCsv(r.lifecycle_key);

   s += "," + FP_L30SafeCsv(r.virtual_ticket);
   s += "," + IntegerToString(r.lifecycle_sequence);
   s += "," + FP_L30SafeCsv(r.adapter_status);
   s += "," + FP_L30SafeCsv(FP_L30Bool(r.adapter_registered));
   s += "," + FP_L30SafeCsv(r.adapter_block_reason);

   s += "," + FP_L30SafeCsv(r.request_id);
   s += "," + FP_L30SafeCsv(r.request_key);
   s += "," + FP_L30SafeCsv(r.request_order_type);
   s += "," + FP_L30SafeCsv(r.request_direction);
   s += "," + DoubleToString(r.request_volume, 2);
   s += "," + DoubleToString(r.request_price, _Digits);
   s += "," + DoubleToString(r.request_sl, _Digits);
   s += "," + DoubleToString(r.request_tp, _Digits);

   s += "," + FP_L30SafeCsv(FP_L30Time(r.seed_time));
   s += "," + FP_L30SafeCsv(FP_L30Time(r.entry_time));
   s += "," + FP_L30SafeCsv(FP_L30Time(r.exit_time));
   s += "," + IntegerToString(r.seed_index);
   s += "," + IntegerToString(r.entry_index);
   s += "," + IntegerToString(r.exit_index);
   s += "," + IntegerToString(r.expiry_bars);
   s += "," + IntegerToString(r.bars_to_entry);
   s += "," + IntegerToString(r.bars_in_trade);
   s += "," + IntegerToString(r.bars_elapsed_total);

   s += "," + DoubleToString(r.entry_close, _Digits);
   s += "," + DoubleToString(r.exit_close, _Digits);
   s += "," + DoubleToString(r.best_close, _Digits);
   s += "," + DoubleToString(r.worst_close, _Digits);
   s += "," + DoubleToString(r.mfe_close_distance, _Digits);
   s += "," + DoubleToString(r.mae_close_distance, _Digits);
   s += "," + DoubleToString(r.risk_distance, _Digits);
   s += "," + DoubleToString(r.reward_distance, _Digits);
   s += "," + DoubleToString(r.realized_r_like, 4);

   s += "," + FP_L30SafeCsv(r.entry_condition);
   s += "," + FP_L30SafeCsv(r.exit_condition);
   s += "," + FP_L30SafeCsv(r.paper_order_state);
   s += "," + FP_L30SafeCsv(r.paper_order_event);
   s += "," + FP_L30SafeCsv(r.close_only_contract);
   s += "," + FP_L30SafeCsv(r.no_send_contract);
   s += "," + FP_L30SafeCsv(r.no_touch_contract);
   s += "," + FP_L30SafeCsv(r.execution_status);
   return s;
}

bool FP_L30WriteLatestPaperBrokerLifecycle(const FP_Level30PaperBrokerLifecycleConfig &cfg,
                                           const FP_Level30PaperBrokerLifecycleRow &row,
                                           FP_Level30PaperBrokerLifecycleReport &report)
{
   if(!cfg.write_latest_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL30_PAPER_BROKER_LIFECYCLE_DEFAULT_FOLDER;
   FolderCreate(folder);

   int handle = FileOpen(FP_L30PaperBrokerLifecycleLatestPath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "level30_paper_broker_lifecycle_latest_open_failed";
      return false;
   }

   FileWriteString(handle, FP_L30PaperBrokerLifecycleHeader() + "\r\n");
   FileWriteString(handle, FP_L30PaperBrokerLifecycleRowCsv(row) + "\r\n");
   FileClose(handle);

   report.files_written++;
   report.latest_written = true;
   return true;
}

bool FP_L30AppendPaperBrokerLifecycle(const FP_Level30PaperBrokerLifecycleConfig &cfg,
                                      const FP_Level30PaperBrokerLifecycleRow &row,
                                      FP_Level30PaperBrokerLifecycleReport &report)
{
   if(!cfg.append_lifecycle_csv)
      return true;

   if(row.duplicate_skipped)
   {
      report.duplicate_skipped = true;
      return true;
   }

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL30_PAPER_BROKER_LIFECYCLE_DEFAULT_FOLDER;
   FolderCreate(folder);

   string path = FP_L30PaperBrokerLifecyclePath(cfg);
   bool exists = FileIsExist(path);
   int handle = INVALID_HANDLE;

   if(!exists)
   {
      handle = FileOpen(path, FILE_WRITE|FILE_TXT|FILE_ANSI);
      if(handle == INVALID_HANDLE)
      {
         report.file_errors++;
         report.reason = "level30_paper_broker_lifecycle_create_failed";
         return false;
      }
      FileWriteString(handle, FP_L30PaperBrokerLifecycleHeader() + "\r\n");
   }
   else
   {
      handle = FileOpen(path, FILE_READ|FILE_WRITE|FILE_TXT|FILE_ANSI);
      if(handle == INVALID_HANDLE)
      {
         report.file_errors++;
         report.reason = "level30_paper_broker_lifecycle_open_failed";
         return false;
      }
      FileSeek(handle, 0, SEEK_END);
   }

   FileWriteString(handle, FP_L30PaperBrokerLifecycleRowCsv(row) + "\r\n");
   FileClose(handle);

   report.files_written++;
   report.lifecycle_written = true;
   return true;
}

#endif // __FP_PAPER_BROKER_LIFECYCLE_EXPORT_MQH__
