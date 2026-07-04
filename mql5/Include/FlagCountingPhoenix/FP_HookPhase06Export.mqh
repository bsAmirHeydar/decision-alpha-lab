#ifndef __FP_HOOK_PHASE06_EXPORT_MQH__
#define __FP_HOOK_PHASE06_EXPORT_MQH__
#property strict

#include "FP_HookPhase06Visual.mqh"

string FP_HookP06SafeCsv(string s)
{
   StringReplace(s, "\"", "\"\"");
   return "\"" + s + "\"";
}

string FP_HookP06QualityPath(const FP_HookPhase06Config &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_HOOK_P06_DEFAULT_FOLDER;
   return folder + "\\hook_phase06_xy_quality.csv";
}

string FP_HookP06SummaryPath(const FP_HookPhase06Config &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_HOOK_P06_DEFAULT_FOLDER;
   return folder + "\\hook_phase06_summary.csv";
}

string FP_HookP06QualityHeader()
{
   return "schema_version,version,sequence_id,direction,scale_l,origin_node_id,origin_time,origin_price,x_count,y_count,hook_type,lifecycle_state,y_state,xy_state,quality_bucket,quality_score,x_strength,y_strength,type_strength,lifecycle_strength,x_closed,y_closed,y_partial,dead,sufficient_x,sufficient_y,y_comparisons_total,y_comparisons_passed,y01_y12_passed,y12_y23_passed,y23_y34_passed,anchor_slot,anchor_time,anchor_price,reason";
}

string FP_HookP06QualityRow(const FP_HookPhase06Record &r)
{
   FP_HookPhase02Sequence seq = r.p05.p04.p03.sequence;
   FP_HookPhase06Score s = r.score;

   string row = "";
   row += FP_HookP06SafeCsv(FP_HOOK_P06_SCHEMA_VERSION);
   row += "," + FP_HookP06SafeCsv(FP_HOOK_P06_VERSION);
   row += "," + IntegerToString(seq.sequence_id);
   row += "," + FP_HookP06SafeCsv(FP_HookP02DirectionName(seq.direction));
   row += "," + IntegerToString(seq.scale_l);
   row += "," + IntegerToString(seq.origin_node_id);
   row += "," + FP_HookP06SafeCsv(TimeToString(seq.origin_time, TIME_DATE|TIME_SECONDS));
   row += "," + DoubleToString(seq.origin_price, _Digits);
   row += "," + IntegerToString(seq.x_count);
   row += "," + IntegerToString(r.p05.p04.p03.y_axis.y_count);
   row += "," + FP_HookP06SafeCsv(FP_HookP05TypeName(r.p05.classification.hook_type));
   row += "," + FP_HookP06SafeCsv(FP_HookP04LifecycleStateName(r.p05.p04.lifecycle.state));
   row += "," + FP_HookP06SafeCsv(FP_HookP06YStateName(s.y_state));
   row += "," + FP_HookP06SafeCsv(FP_HookP06XYStateName(s.xy_state));
   row += "," + FP_HookP06SafeCsv(FP_HookP06QualityBucketName(s.quality_bucket));
   row += "," + DoubleToString(s.quality_score, 4);
   row += "," + DoubleToString(s.x_strength, 4);
   row += "," + DoubleToString(s.y_strength, 4);
   row += "," + DoubleToString(s.type_strength, 4);
   row += "," + DoubleToString(s.lifecycle_strength, 4);
   row += "," + FP_HookP06SafeCsv(FP_HookP06BoolName(s.x_closed));
   row += "," + FP_HookP06SafeCsv(FP_HookP06BoolName(s.y_closed));
   row += "," + FP_HookP06SafeCsv(FP_HookP06BoolName(s.y_partial));
   row += "," + FP_HookP06SafeCsv(FP_HookP06BoolName(s.dead));
   row += "," + FP_HookP06SafeCsv(FP_HookP06BoolName(s.sufficient_x));
   row += "," + FP_HookP06SafeCsv(FP_HookP06BoolName(s.sufficient_y));
   row += "," + IntegerToString(s.y_comparisons_total);
   row += "," + IntegerToString(s.y_comparisons_passed);
   row += "," + FP_HookP06SafeCsv(FP_HookP06BoolName(s.y01_y12_passed));
   row += "," + FP_HookP06SafeCsv(FP_HookP06BoolName(s.y12_y23_passed));
   row += "," + FP_HookP06SafeCsv(FP_HookP06BoolName(s.y23_y34_passed));
   row += "," + FP_HookP06SafeCsv(s.anchor_slot);
   row += "," + FP_HookP06SafeCsv(TimeToString(s.anchor_time, TIME_DATE|TIME_SECONDS));
   row += "," + DoubleToString(s.anchor_price, _Digits);
   row += "," + FP_HookP06SafeCsv(s.reason);
   return row;
}

string FP_HookP06SummaryHeader()
{
   return "schema_version,version,symbol,period,display_family,bars_seen,bars_scanned,scales_seen,nodes_seen,phase02_sequences,phase03_records,phase04_records,phase05_records,records,positive,negative,xy_closed,x_only,y_only,open,dead,insufficient,y_closed,y_partial,y_not_closed,elite,high,medium,low,invalid,drawn,status,reason";
}

string FP_HookP06SummaryRow(const string symbol,
                            const ENUM_TIMEFRAMES period,
                            const FP_HookPhase06Config &cfg,
                            const FP_HookPhase06Report &r)
{
   string row = "";
   row += FP_HookP06SafeCsv(FP_HOOK_P06_SCHEMA_VERSION);
   row += "," + FP_HookP06SafeCsv(FP_HOOK_P06_VERSION);
   row += "," + FP_HookP06SafeCsv(symbol);
   row += "," + FP_HookP06SafeCsv(EnumToString(period));
   row += "," + FP_HookP06SafeCsv(FP_HookP01DisplayFamilyName(cfg.display_family));
   row += "," + IntegerToString(r.bars_seen);
   row += "," + IntegerToString(r.bars_scanned);
   row += "," + IntegerToString(r.scales_seen);
   row += "," + IntegerToString(r.nodes_seen);
   row += "," + IntegerToString(r.phase02_sequences_seen);
   row += "," + IntegerToString(r.phase03_records_seen);
   row += "," + IntegerToString(r.phase04_records_seen);
   row += "," + IntegerToString(r.phase05_records_seen);
   row += "," + IntegerToString(r.records_total);
   row += "," + IntegerToString(r.records_positive);
   row += "," + IntegerToString(r.records_negative);
   row += "," + IntegerToString(r.xy_closed_count);
   row += "," + IntegerToString(r.x_only_count);
   row += "," + IntegerToString(r.y_only_count);
   row += "," + IntegerToString(r.open_count);
   row += "," + IntegerToString(r.dead_count);
   row += "," + IntegerToString(r.insufficient_count);
   row += "," + IntegerToString(r.y_closed_count);
   row += "," + IntegerToString(r.y_partial_count);
   row += "," + IntegerToString(r.y_not_closed_count);
   row += "," + IntegerToString(r.elite_count);
   row += "," + IntegerToString(r.high_count);
   row += "," + IntegerToString(r.medium_count);
   row += "," + IntegerToString(r.low_count);
   row += "," + IntegerToString(r.invalid_count);
   row += "," + IntegerToString(r.records_drawn);
   row += "," + FP_HookP06SafeCsv(r.status);
   row += "," + FP_HookP06SafeCsv(r.reason);
   return row;
}

bool FP_HookP06ExportQuality(const FP_HookPhase06Config &cfg,
                             const FP_HookPhase06Record &records[],
                             FP_HookPhase06Report &report)
{
   if(!cfg.export_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_HOOK_P06_DEFAULT_FOLDER;
   FolderCreate(folder);

   int handle = FileOpen(FP_HookP06QualityPath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "HOOK_P06_QUALITY_EXPORT_OPEN_FAILED";
      return false;
   }

   FileWriteString(handle, FP_HookP06QualityHeader() + "\r\n");
   for(int i=0; i<ArraySize(records); i++)
      FileWriteString(handle, FP_HookP06QualityRow(records[i]) + "\r\n");
   FileClose(handle);
   report.files_written++;
   return true;
}

bool FP_HookP06ExportSummary(const string symbol,
                             const ENUM_TIMEFRAMES period,
                             const FP_HookPhase06Config &cfg,
                             FP_HookPhase06Report &report)
{
   if(!cfg.export_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_HOOK_P06_DEFAULT_FOLDER;
   FolderCreate(folder);

   int handle = FileOpen(FP_HookP06SummaryPath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "HOOK_P06_SUMMARY_EXPORT_OPEN_FAILED";
      return false;
   }

   FileWriteString(handle, FP_HookP06SummaryHeader() + "\r\n");
   FileWriteString(handle, FP_HookP06SummaryRow(symbol, period, cfg, report) + "\r\n");
   FileClose(handle);
   report.files_written++;
   return true;
}

#endif // __FP_HOOK_PHASE06_EXPORT_MQH__
