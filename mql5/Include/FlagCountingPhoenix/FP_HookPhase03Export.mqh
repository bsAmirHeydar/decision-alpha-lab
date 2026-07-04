#ifndef __FP_HOOK_PHASE03_EXPORT_MQH__
#define __FP_HOOK_PHASE03_EXPORT_MQH__
#property strict

#include "FP_HookPhase03Visual.mqh"

string FP_HookP03SafeCsv(string s)
{
   StringReplace(s, "\"", "\"\"");
   return "\"" + s + "\"";
}

string FP_HookP03YAxisPath(const FP_HookPhase03Config &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_HOOK_P03_DEFAULT_FOLDER;
   return folder + "\\hook_phase03_y_axis.csv";
}

string FP_HookP03SummaryPath(const FP_HookPhase03Config &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_HOOK_P03_DEFAULT_FOLDER;
   return folder + "\\hook_phase03_summary.csv";
}

string FP_HookP03YAxisHeader()
{
   return "schema_version,version,sequence_id,direction,state,scale_l,origin_node_id,origin_time,origin_price,x_count,y_state,y_count,has_y01,y01_time,y01_price,has_y12,y12_time,y12_price,has_y23,y23_time,y23_price,has_y34,y34_time,y34_price";
}

string FP_HookP03YAxisRow(const FP_HookPhase03Record &r)
{
   string row = "";
   row += FP_HookP03SafeCsv(FP_HOOK_P03_SCHEMA_VERSION);
   row += "," + FP_HookP03SafeCsv(FP_HOOK_P03_VERSION);
   row += "," + IntegerToString(r.sequence.sequence_id);
   row += "," + FP_HookP03SafeCsv(FP_HookP02DirectionName(r.sequence.direction));
   row += "," + FP_HookP03SafeCsv(FP_HookP02StateName(r.sequence.state));
   row += "," + IntegerToString(r.sequence.scale_l);
   row += "," + IntegerToString(r.sequence.origin_node_id);
   row += "," + FP_HookP03SafeCsv(TimeToString(r.sequence.origin_time, TIME_DATE|TIME_SECONDS));
   row += "," + DoubleToString(r.sequence.origin_price, _Digits);
   row += "," + IntegerToString(r.sequence.x_count);
   row += "," + FP_HookP03SafeCsv(FP_HookP03YStateName(r.y_axis.y_state));
   row += "," + IntegerToString(r.y_axis.y_count);

   row += "," + FP_HookP03SafeCsv(FP_HookP03BoolName(r.y_axis.has_y01));
   row += "," + FP_HookP03SafeCsv(TimeToString(r.y_axis.y01_time, TIME_DATE|TIME_SECONDS));
   row += "," + DoubleToString(r.y_axis.y01_price, _Digits);

   row += "," + FP_HookP03SafeCsv(FP_HookP03BoolName(r.y_axis.has_y12));
   row += "," + FP_HookP03SafeCsv(TimeToString(r.y_axis.y12_time, TIME_DATE|TIME_SECONDS));
   row += "," + DoubleToString(r.y_axis.y12_price, _Digits);

   row += "," + FP_HookP03SafeCsv(FP_HookP03BoolName(r.y_axis.has_y23));
   row += "," + FP_HookP03SafeCsv(TimeToString(r.y_axis.y23_time, TIME_DATE|TIME_SECONDS));
   row += "," + DoubleToString(r.y_axis.y23_price, _Digits);

   row += "," + FP_HookP03SafeCsv(FP_HookP03BoolName(r.y_axis.has_y34));
   row += "," + FP_HookP03SafeCsv(TimeToString(r.y_axis.y34_time, TIME_DATE|TIME_SECONDS));
   row += "," + DoubleToString(r.y_axis.y34_price, _Digits);

   return row;
}

string FP_HookP03SummaryHeader()
{
   return "schema_version,version,symbol,period,display_family,bars_seen,bars_scanned,scales_seen,nodes_seen,phase02_sequences,records,positive,negative,y01,y12,y23,y34,y_complete,y_partial,y_missing,drawn,status,reason";
}

string FP_HookP03SummaryRow(const string symbol,
                            const ENUM_TIMEFRAMES period,
                            const FP_HookPhase03Config &cfg,
                            const FP_HookPhase03Report &r)
{
   string row = "";
   row += FP_HookP03SafeCsv(FP_HOOK_P03_SCHEMA_VERSION);
   row += "," + FP_HookP03SafeCsv(FP_HOOK_P03_VERSION);
   row += "," + FP_HookP03SafeCsv(symbol);
   row += "," + FP_HookP03SafeCsv(EnumToString(period));
   row += "," + FP_HookP03SafeCsv(FP_HookP01DisplayFamilyName(cfg.display_family));
   row += "," + IntegerToString(r.bars_seen);
   row += "," + IntegerToString(r.bars_scanned);
   row += "," + IntegerToString(r.scales_seen);
   row += "," + IntegerToString(r.nodes_seen);
   row += "," + IntegerToString(r.phase02_sequences_seen);
   row += "," + IntegerToString(r.records_total);
   row += "," + IntegerToString(r.records_positive);
   row += "," + IntegerToString(r.records_negative);
   row += "," + IntegerToString(r.y01_count);
   row += "," + IntegerToString(r.y12_count);
   row += "," + IntegerToString(r.y23_count);
   row += "," + IntegerToString(r.y34_count);
   row += "," + IntegerToString(r.y_complete_count);
   row += "," + IntegerToString(r.y_partial_count);
   row += "," + IntegerToString(r.y_missing_count);
   row += "," + IntegerToString(r.records_drawn);
   row += "," + FP_HookP03SafeCsv(r.status);
   row += "," + FP_HookP03SafeCsv(r.reason);
   return row;
}

bool FP_HookP03ExportYAxis(const FP_HookPhase03Config &cfg,
                           const FP_HookPhase03Record &records[],
                           FP_HookPhase03Report &report)
{
   if(!cfg.export_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_HOOK_P03_DEFAULT_FOLDER;
   FolderCreate(folder);

   int handle = FileOpen(FP_HookP03YAxisPath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "HOOK_P03_Y_AXIS_EXPORT_OPEN_FAILED";
      return false;
   }

   FileWriteString(handle, FP_HookP03YAxisHeader() + "\r\n");
   for(int i=0; i<ArraySize(records); i++)
      FileWriteString(handle, FP_HookP03YAxisRow(records[i]) + "\r\n");
   FileClose(handle);
   report.files_written++;
   return true;
}

bool FP_HookP03ExportSummary(const string symbol,
                             const ENUM_TIMEFRAMES period,
                             const FP_HookPhase03Config &cfg,
                             FP_HookPhase03Report &report)
{
   if(!cfg.export_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_HOOK_P03_DEFAULT_FOLDER;
   FolderCreate(folder);

   int handle = FileOpen(FP_HookP03SummaryPath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "HOOK_P03_SUMMARY_EXPORT_OPEN_FAILED";
      return false;
   }

   FileWriteString(handle, FP_HookP03SummaryHeader() + "\r\n");
   FileWriteString(handle, FP_HookP03SummaryRow(symbol, period, cfg, report) + "\r\n");
   FileClose(handle);
   report.files_written++;
   return true;
}

#endif // __FP_HOOK_PHASE03_EXPORT_MQH__
