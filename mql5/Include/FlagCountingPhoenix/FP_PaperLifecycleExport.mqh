#ifndef __FP_PAPER_LIFECYCLE_EXPORT_MQH__
#define __FP_PAPER_LIFECYCLE_EXPORT_MQH__
#property strict

#include "FP_PaperLifecycleRules.mqh"

string FP_L22PaperLifecyclePath(const FP_Level22PaperLifecycleConfig &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL22_PAPER_LIFECYCLE_DEFAULT_FOLDER;
   return folder + "\\state_gate_level22_paper_lifecycle.csv";
}

string FP_L22PaperLifecycleHeader()
{
   string h = "";
   h += "generated_at,version,symbol,period,attempted,tracked,lifecycle_status,block_reason,lifecycle_id,lifecycle_key";
   h += ",intent_id,intent_status,intent_allowed,direction";
   h += ",entry_price,stop_price,target_price,risk_distance,reward_distance,rr_like";
   h += ",seed_time,entry_time,exit_time,seed_index,entry_index,exit_index,bars_elapsed,expiry_bars";
   h += ",entry_close,exit_close,best_close,worst_close,mfe_close_distance,mae_close_distance,realized_r_like";
   h += ",entry_condition,exit_condition,close_only_path_status,ambiguity_status,no_touch_contract,execution_status";
   return h;
}

string FP_L22PaperLifecycleRowCsv(const FP_Level22PaperLifecycleRow &r)
{
   string s = "";
   s += FP_L22SafeCsv(FP_L22Time(r.generated_at));
   s += "," + FP_L22SafeCsv(r.version);
   s += "," + FP_L22SafeCsv(r.symbol);
   s += "," + FP_L22SafeCsv(r.period_label);
   s += "," + FP_L22SafeCsv(FP_L22Bool(r.attempted));
   s += "," + FP_L22SafeCsv(FP_L22Bool(r.tracked));
   s += "," + FP_L22SafeCsv(r.lifecycle_status);
   s += "," + FP_L22SafeCsv(r.block_reason);
   s += "," + FP_L22SafeCsv(r.lifecycle_id);
   s += "," + FP_L22SafeCsv(r.lifecycle_key);

   s += "," + FP_L22SafeCsv(r.intent_id);
   s += "," + FP_L22SafeCsv(r.intent_status);
   s += "," + FP_L22SafeCsv(FP_L22Bool(r.intent_allowed));
   s += "," + FP_L22SafeCsv(r.direction_label);

   s += "," + DoubleToString(r.entry_price, _Digits);
   s += "," + DoubleToString(r.stop_price, _Digits);
   s += "," + DoubleToString(r.target_price, _Digits);
   s += "," + DoubleToString(r.risk_distance, _Digits);
   s += "," + DoubleToString(r.reward_distance, _Digits);
   s += "," + DoubleToString(r.rr_like, 4);

   s += "," + FP_L22SafeCsv(FP_L22Time(r.seed_time));
   s += "," + FP_L22SafeCsv(FP_L22Time(r.entry_time));
   s += "," + FP_L22SafeCsv(FP_L22Time(r.exit_time));
   s += "," + IntegerToString(r.seed_index);
   s += "," + IntegerToString(r.entry_index);
   s += "," + IntegerToString(r.exit_index);
   s += "," + IntegerToString(r.bars_elapsed);
   s += "," + IntegerToString(r.expiry_bars);

   s += "," + DoubleToString(r.entry_close, _Digits);
   s += "," + DoubleToString(r.exit_close, _Digits);
   s += "," + DoubleToString(r.best_close, _Digits);
   s += "," + DoubleToString(r.worst_close, _Digits);
   s += "," + DoubleToString(r.mfe_close_distance, _Digits);
   s += "," + DoubleToString(r.mae_close_distance, _Digits);
   s += "," + DoubleToString(r.realized_r_like, 4);

   s += "," + FP_L22SafeCsv(r.entry_condition);
   s += "," + FP_L22SafeCsv(r.exit_condition);
   s += "," + FP_L22SafeCsv(r.close_only_path_status);
   s += "," + FP_L22SafeCsv(r.ambiguity_status);
   s += "," + FP_L22SafeCsv(r.no_touch_contract);
   s += "," + FP_L22SafeCsv(r.execution_status);
   return s;
}

bool FP_L22ExportPaperLifecycle(const FP_Level22PaperLifecycleConfig &cfg,
                                const FP_Level22PaperLifecycleRow &row,
                                FP_Level22PaperLifecycleReport &report)
{
   if(!cfg.export_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL22_PAPER_LIFECYCLE_DEFAULT_FOLDER;
   FolderCreate(folder);

   int handle = FileOpen(FP_L22PaperLifecyclePath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "level22_paper_lifecycle_export_open_failed";
      return false;
   }

   FileWriteString(handle, FP_L22PaperLifecycleHeader() + "\r\n");
   FileWriteString(handle, FP_L22PaperLifecycleRowCsv(row) + "\r\n");
   FileClose(handle);

   report.files_written++;
   report.lifecycle_written = true;
   return true;
}

#endif // __FP_PAPER_LIFECYCLE_EXPORT_MQH__
