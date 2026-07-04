#ifndef __FP_HOOK_PHASE04_EXPORT_MQH__
#define __FP_HOOK_PHASE04_EXPORT_MQH__
#property strict

#include "FP_HookPhase04Visual.mqh"

string FP_HookP04SafeCsv(string s)
{
   StringReplace(s, "\"", "\"\"");
   return "\"" + s + "\"";
}

string FP_HookP04LifecyclePath(const FP_HookPhase04Config &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_HOOK_P04_DEFAULT_FOLDER;
   return folder + "\\hook_phase04_lifecycle.csv";
}

string FP_HookP04SummaryPath(const FP_HookPhase04Config &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_HOOK_P04_DEFAULT_FOLDER;
   return folder + "\\hook_phase04_summary.csv";
}

string FP_HookP04LifecycleHeader()
{
   return "schema_version,version,sequence_id,direction,state,scale_l,origin_node_id,origin_time,origin_price,x_count,y_count,lifecycle_state,state_reason,nd_detected,nd_time,nd_price,nd_threshold,death_detected,death_time,death_price,death_boundary,x_closure_candidate,x_closed,x_closure_time,x_closure_price,x_closure_threshold,y_ref_slot,y_ref_time,y_ref_price,has_required_x,has_required_y";
}

string FP_HookP04LifecycleRow(const FP_HookPhase04Record &r)
{
   FP_HookPhase02Sequence s = r.p03.sequence;
   FP_HookPhase04Lifecycle l = r.lifecycle;

   string row = "";
   row += FP_HookP04SafeCsv(FP_HOOK_P04_SCHEMA_VERSION);
   row += "," + FP_HookP04SafeCsv(FP_HOOK_P04_VERSION);
   row += "," + IntegerToString(s.sequence_id);
   row += "," + FP_HookP04SafeCsv(FP_HookP02DirectionName(s.direction));
   row += "," + FP_HookP04SafeCsv(FP_HookP02StateName(s.state));
   row += "," + IntegerToString(s.scale_l);
   row += "," + IntegerToString(s.origin_node_id);
   row += "," + FP_HookP04SafeCsv(TimeToString(s.origin_time, TIME_DATE|TIME_SECONDS));
   row += "," + DoubleToString(s.origin_price, _Digits);
   row += "," + IntegerToString(s.x_count);
   row += "," + IntegerToString(r.p03.y_axis.y_count);
   row += "," + FP_HookP04SafeCsv(FP_HookP04LifecycleStateName(l.state));
   row += "," + FP_HookP04SafeCsv(l.state_reason);

   row += "," + FP_HookP04SafeCsv(FP_HookP04BoolName(l.nd_detected));
   row += "," + FP_HookP04SafeCsv(TimeToString(l.nd_time, TIME_DATE|TIME_SECONDS));
   row += "," + DoubleToString(l.nd_price, _Digits);
   row += "," + DoubleToString(l.nd_threshold_price, _Digits);

   row += "," + FP_HookP04SafeCsv(FP_HookP04BoolName(l.origin_return_penetrated));
   row += "," + FP_HookP04SafeCsv(TimeToString(l.death_time, TIME_DATE|TIME_SECONDS));
   row += "," + DoubleToString(l.death_price, _Digits);
   row += "," + DoubleToString(l.death_boundary_price, _Digits);

   row += "," + FP_HookP04SafeCsv(FP_HookP04BoolName(l.x_closure_candidate));
   row += "," + FP_HookP04SafeCsv(FP_HookP04BoolName(l.x_closed));
   row += "," + FP_HookP04SafeCsv(TimeToString(l.x_closure_time, TIME_DATE|TIME_SECONDS));
   row += "," + DoubleToString(l.x_closure_price, _Digits);
   row += "," + DoubleToString(l.x_closure_threshold_price, _Digits);

   row += "," + FP_HookP04SafeCsv(l.x_closure_reference_y_slot);
   row += "," + FP_HookP04SafeCsv(TimeToString(l.x_closure_reference_y_time, TIME_DATE|TIME_SECONDS));
   row += "," + DoubleToString(l.x_closure_reference_y_price, _Digits);

   row += "," + FP_HookP04SafeCsv(FP_HookP04BoolName(l.has_required_x));
   row += "," + FP_HookP04SafeCsv(FP_HookP04BoolName(l.has_required_y));

   return row;
}

string FP_HookP04SummaryHeader()
{
   return "schema_version,version,symbol,period,display_family,bars_seen,bars_scanned,scales_seen,nodes_seen,phase02_sequences,phase03_records,records,positive,negative,nd,death,closure_candidates,x_closed,alive,insufficient,drawn,status,reason";
}

string FP_HookP04SummaryRow(const string symbol,
                            const ENUM_TIMEFRAMES period,
                            const FP_HookPhase04Config &cfg,
                            const FP_HookPhase04Report &r)
{
   string row = "";
   row += FP_HookP04SafeCsv(FP_HOOK_P04_SCHEMA_VERSION);
   row += "," + FP_HookP04SafeCsv(FP_HOOK_P04_VERSION);
   row += "," + FP_HookP04SafeCsv(symbol);
   row += "," + FP_HookP04SafeCsv(EnumToString(period));
   row += "," + FP_HookP04SafeCsv(FP_HookP01DisplayFamilyName(cfg.display_family));
   row += "," + IntegerToString(r.bars_seen);
   row += "," + IntegerToString(r.bars_scanned);
   row += "," + IntegerToString(r.scales_seen);
   row += "," + IntegerToString(r.nodes_seen);
   row += "," + IntegerToString(r.phase02_sequences_seen);
   row += "," + IntegerToString(r.phase03_records_seen);
   row += "," + IntegerToString(r.records_total);
   row += "," + IntegerToString(r.records_positive);
   row += "," + IntegerToString(r.records_negative);
   row += "," + IntegerToString(r.nd_count);
   row += "," + IntegerToString(r.death_count);
   row += "," + IntegerToString(r.x_closure_candidate_count);
   row += "," + IntegerToString(r.x_closed_count);
   row += "," + IntegerToString(r.alive_count);
   row += "," + IntegerToString(r.insufficient_count);
   row += "," + IntegerToString(r.records_drawn);
   row += "," + FP_HookP04SafeCsv(r.status);
   row += "," + FP_HookP04SafeCsv(r.reason);
   return row;
}

bool FP_HookP04ExportLifecycle(const FP_HookPhase04Config &cfg,
                               const FP_HookPhase04Record &records[],
                               FP_HookPhase04Report &report)
{
   if(!cfg.export_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_HOOK_P04_DEFAULT_FOLDER;
   FolderCreate(folder);

   int handle = FileOpen(FP_HookP04LifecyclePath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "HOOK_P04_LIFECYCLE_EXPORT_OPEN_FAILED";
      return false;
   }

   FileWriteString(handle, FP_HookP04LifecycleHeader() + "\r\n");
   for(int i=0; i<ArraySize(records); i++)
      FileWriteString(handle, FP_HookP04LifecycleRow(records[i]) + "\r\n");
   FileClose(handle);
   report.files_written++;
   return true;
}

bool FP_HookP04ExportSummary(const string symbol,
                             const ENUM_TIMEFRAMES period,
                             const FP_HookPhase04Config &cfg,
                             FP_HookPhase04Report &report)
{
   if(!cfg.export_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_HOOK_P04_DEFAULT_FOLDER;
   FolderCreate(folder);

   int handle = FileOpen(FP_HookP04SummaryPath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "HOOK_P04_SUMMARY_EXPORT_OPEN_FAILED";
      return false;
   }

   FileWriteString(handle, FP_HookP04SummaryHeader() + "\r\n");
   FileWriteString(handle, FP_HookP04SummaryRow(symbol, period, cfg, report) + "\r\n");
   FileClose(handle);
   report.files_written++;
   return true;
}

#endif // __FP_HOOK_PHASE04_EXPORT_MQH__
