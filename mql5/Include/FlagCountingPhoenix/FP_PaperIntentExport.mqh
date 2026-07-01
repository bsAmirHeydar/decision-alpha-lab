#ifndef __FP_PAPER_INTENT_EXPORT_MQH__
#define __FP_PAPER_INTENT_EXPORT_MQH__
#property strict

#include "FP_PaperIntentRules.mqh"

string FP_L21PaperIntentPath(const FP_Level21PaperIntentConfig &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL21_PAPER_INTENT_DEFAULT_FOLDER;
   return folder + "\\state_gate_level21_paper_intents.csv";
}

string FP_L21PaperIntentHeader()
{
   string h = "";
   h += "generated_at,version,symbol,period,attempted,allowed,intent_status,block_reason,intent_id,intent_key";
   h += ",source_bridge_key,source_kind,source_id,source_level,source_L,direction";
   h += ",entry_price,stop_price,target_price,risk_distance,reward_distance,rr_like";
   h += ",entry_anchor_time,stop_anchor_time,target_anchor_time";
   h += ",entry_anchor_id,stop_anchor_id,target_anchor_id";
   h += ",entry_anchor_kind,stop_anchor_kind,target_anchor_kind";
   h += ",geometry_status,lifecycle_seed_status,expiry_bars,no_touch_contract,execution_status";
   return h;
}

string FP_L21PaperIntentRowCsv(const FP_Level21PaperIntentRow &r)
{
   string s = "";
   s += FP_L21SafeCsv(FP_L21Time(r.generated_at));
   s += "," + FP_L21SafeCsv(r.version);
   s += "," + FP_L21SafeCsv(r.symbol);
   s += "," + FP_L21SafeCsv(r.period_label);
   s += "," + FP_L21SafeCsv(FP_L21Bool(r.attempted));
   s += "," + FP_L21SafeCsv(FP_L21Bool(r.allowed));
   s += "," + FP_L21SafeCsv(r.intent_status);
   s += "," + FP_L21SafeCsv(r.block_reason);
   s += "," + FP_L21SafeCsv(r.intent_id);
   s += "," + FP_L21SafeCsv(r.intent_key);

   s += "," + FP_L21SafeCsv(r.source_bridge_key);
   s += "," + FP_L21SafeCsv(r.source_kind);
   s += "," + FP_L21SafeCsv(r.source_id);
   s += "," + IntegerToString(r.source_level);
   s += "," + IntegerToString(r.source_L);
   s += "," + FP_L21SafeCsv(r.direction_label);

   s += "," + DoubleToString(r.entry_price, _Digits);
   s += "," + DoubleToString(r.stop_price, _Digits);
   s += "," + DoubleToString(r.target_price, _Digits);
   s += "," + DoubleToString(r.risk_distance, _Digits);
   s += "," + DoubleToString(r.reward_distance, _Digits);
   s += "," + DoubleToString(r.rr_like, 4);

   s += "," + FP_L21SafeCsv(FP_L21Time(r.entry_anchor_time));
   s += "," + FP_L21SafeCsv(FP_L21Time(r.stop_anchor_time));
   s += "," + FP_L21SafeCsv(FP_L21Time(r.target_anchor_time));

   s += "," + FP_L21SafeCsv(r.entry_anchor_id);
   s += "," + FP_L21SafeCsv(r.stop_anchor_id);
   s += "," + FP_L21SafeCsv(r.target_anchor_id);

   s += "," + FP_L21SafeCsv(r.entry_anchor_kind);
   s += "," + FP_L21SafeCsv(r.stop_anchor_kind);
   s += "," + FP_L21SafeCsv(r.target_anchor_kind);

   s += "," + FP_L21SafeCsv(r.geometry_status);
   s += "," + FP_L21SafeCsv(r.lifecycle_seed_status);
   s += "," + IntegerToString(r.expiry_bars);
   s += "," + FP_L21SafeCsv(r.no_touch_contract);
   s += "," + FP_L21SafeCsv(r.execution_status);
   return s;
}

bool FP_L21ExportPaperIntent(const FP_Level21PaperIntentConfig &cfg,
                             const FP_Level21PaperIntentRow &row,
                             FP_Level21PaperIntentReport &report)
{
   if(!cfg.export_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL21_PAPER_INTENT_DEFAULT_FOLDER;
   FolderCreate(folder);

   int handle = FileOpen(FP_L21PaperIntentPath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "level21_paper_intent_export_open_failed";
      return false;
   }

   FileWriteString(handle, FP_L21PaperIntentHeader() + "\r\n");
   FileWriteString(handle, FP_L21PaperIntentRowCsv(row) + "\r\n");
   FileClose(handle);

   report.files_written++;
   report.intent_written = true;
   return true;
}

#endif // __FP_PAPER_INTENT_EXPORT_MQH__
