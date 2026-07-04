#ifndef __FP_HOOK_PHASE05_EXPORT_MQH__
#define __FP_HOOK_PHASE05_EXPORT_MQH__
#property strict

#include "FP_HookPhase05Visual.mqh"

string FP_HookP05SafeCsv(string s)
{
   StringReplace(s, "\"", "\"\"");
   return "\"" + s + "\"";
}

string FP_HookP05TypePath(const FP_HookPhase05Config &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_HOOK_P05_DEFAULT_FOLDER;
   return folder + "\\hook_phase05_type_abc.csv";
}

string FP_HookP05SummaryPath(const FP_HookPhase05Config &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_HOOK_P05_DEFAULT_FOLDER;
   return folder + "\\hook_phase05_summary.csv";
}

string FP_HookP05TypeHeader()
{
   return "schema_version,version,sequence_id,direction,scale_l,origin_node_id,origin_time,origin_price,x_count,y_count,lifecycle_state,hook_type,type_state,confidence,type_rank,has_y01,y01_time,y01_price,has_y12,y12_time,y12_price,has_y23,y23_time,y23_price,has_y34,y34_time,y34_price,third_y_slot,third_y_time,third_y_price,used_y34_as_third,condition_first,condition_second,reason";
}

string FP_HookP05TypeRow(const FP_HookPhase05Record &r)
{
   FP_HookPhase02Sequence s = r.p04.p03.sequence;
   FP_HookPhase05Classification c = r.classification;

   string row = "";
   row += FP_HookP05SafeCsv(FP_HOOK_P05_SCHEMA_VERSION);
   row += "," + FP_HookP05SafeCsv(FP_HOOK_P05_VERSION);
   row += "," + IntegerToString(s.sequence_id);
   row += "," + FP_HookP05SafeCsv(FP_HookP02DirectionName(s.direction));
   row += "," + IntegerToString(s.scale_l);
   row += "," + IntegerToString(s.origin_node_id);
   row += "," + FP_HookP05SafeCsv(TimeToString(s.origin_time, TIME_DATE|TIME_SECONDS));
   row += "," + DoubleToString(s.origin_price, _Digits);
   row += "," + IntegerToString(s.x_count);
   row += "," + IntegerToString(r.p04.p03.y_axis.y_count);
   row += "," + FP_HookP05SafeCsv(FP_HookP04LifecycleStateName(r.p04.lifecycle.state));
   row += "," + FP_HookP05SafeCsv(FP_HookP05TypeName(c.hook_type));
   row += "," + FP_HookP05SafeCsv(FP_HookP05StateName(c.state));
   row += "," + DoubleToString(c.confidence_score, 4);
   row += "," + DoubleToString(c.type_rank_score, 4);

   row += "," + FP_HookP05SafeCsv(FP_HookP05BoolName(c.has_y01));
   row += "," + FP_HookP05SafeCsv(TimeToString(c.y01_time, TIME_DATE|TIME_SECONDS));
   row += "," + DoubleToString(c.y01_price, _Digits);

   row += "," + FP_HookP05SafeCsv(FP_HookP05BoolName(c.has_y12));
   row += "," + FP_HookP05SafeCsv(TimeToString(c.y12_time, TIME_DATE|TIME_SECONDS));
   row += "," + DoubleToString(c.y12_price, _Digits);

   row += "," + FP_HookP05SafeCsv(FP_HookP05BoolName(c.has_y23));
   row += "," + FP_HookP05SafeCsv(TimeToString(c.y23_time, TIME_DATE|TIME_SECONDS));
   row += "," + DoubleToString(c.y23_price, _Digits);

   row += "," + FP_HookP05SafeCsv(FP_HookP05BoolName(c.has_y34));
   row += "," + FP_HookP05SafeCsv(TimeToString(c.y34_time, TIME_DATE|TIME_SECONDS));
   row += "," + DoubleToString(c.y34_price, _Digits);

   row += "," + FP_HookP05SafeCsv(c.third_y_slot);
   row += "," + FP_HookP05SafeCsv(TimeToString(c.third_y_time, TIME_DATE|TIME_SECONDS));
   row += "," + DoubleToString(c.third_y_price, _Digits);

   row += "," + FP_HookP05SafeCsv(FP_HookP05BoolName(c.used_y34_as_third));
   row += "," + FP_HookP05SafeCsv(FP_HookP05BoolName(c.condition_first));
   row += "," + FP_HookP05SafeCsv(FP_HookP05BoolName(c.condition_second));
   row += "," + FP_HookP05SafeCsv(c.reason);
   return row;
}

string FP_HookP05SummaryHeader()
{
   return "schema_version,version,symbol,period,display_family,bars_seen,bars_scanned,scales_seen,nodes_seen,phase02_sequences,phase03_records,phase04_records,records,positive,negative,type_a,type_b,type_c,insufficient,y34_fallback,drawn,status,reason";
}

string FP_HookP05SummaryRow(const string symbol,
                            const ENUM_TIMEFRAMES period,
                            const FP_HookPhase05Config &cfg,
                            const FP_HookPhase05Report &r)
{
   string row = "";
   row += FP_HookP05SafeCsv(FP_HOOK_P05_SCHEMA_VERSION);
   row += "," + FP_HookP05SafeCsv(FP_HOOK_P05_VERSION);
   row += "," + FP_HookP05SafeCsv(symbol);
   row += "," + FP_HookP05SafeCsv(EnumToString(period));
   row += "," + FP_HookP05SafeCsv(FP_HookP01DisplayFamilyName(cfg.display_family));
   row += "," + IntegerToString(r.bars_seen);
   row += "," + IntegerToString(r.bars_scanned);
   row += "," + IntegerToString(r.scales_seen);
   row += "," + IntegerToString(r.nodes_seen);
   row += "," + IntegerToString(r.phase02_sequences_seen);
   row += "," + IntegerToString(r.phase03_records_seen);
   row += "," + IntegerToString(r.phase04_records_seen);
   row += "," + IntegerToString(r.records_total);
   row += "," + IntegerToString(r.records_positive);
   row += "," + IntegerToString(r.records_negative);
   row += "," + IntegerToString(r.type_a_count);
   row += "," + IntegerToString(r.type_b_count);
   row += "," + IntegerToString(r.type_c_count);
   row += "," + IntegerToString(r.insufficient_count);
   row += "," + IntegerToString(r.y34_fallback_count);
   row += "," + IntegerToString(r.records_drawn);
   row += "," + FP_HookP05SafeCsv(r.status);
   row += "," + FP_HookP05SafeCsv(r.reason);
   return row;
}

bool FP_HookP05ExportTypes(const FP_HookPhase05Config &cfg,
                           const FP_HookPhase05Record &records[],
                           FP_HookPhase05Report &report)
{
   if(!cfg.export_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_HOOK_P05_DEFAULT_FOLDER;
   FolderCreate(folder);

   int handle = FileOpen(FP_HookP05TypePath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "HOOK_P05_TYPE_EXPORT_OPEN_FAILED";
      return false;
   }

   FileWriteString(handle, FP_HookP05TypeHeader() + "\r\n");
   for(int i=0; i<ArraySize(records); i++)
      FileWriteString(handle, FP_HookP05TypeRow(records[i]) + "\r\n");
   FileClose(handle);
   report.files_written++;
   return true;
}

bool FP_HookP05ExportSummary(const string symbol,
                             const ENUM_TIMEFRAMES period,
                             const FP_HookPhase05Config &cfg,
                             FP_HookPhase05Report &report)
{
   if(!cfg.export_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_HOOK_P05_DEFAULT_FOLDER;
   FolderCreate(folder);

   int handle = FileOpen(FP_HookP05SummaryPath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "HOOK_P05_SUMMARY_EXPORT_OPEN_FAILED";
      return false;
   }

   FileWriteString(handle, FP_HookP05SummaryHeader() + "\r\n");
   FileWriteString(handle, FP_HookP05SummaryRow(symbol, period, cfg, report) + "\r\n");
   FileClose(handle);
   report.files_written++;
   return true;
}

#endif // __FP_HOOK_PHASE05_EXPORT_MQH__
