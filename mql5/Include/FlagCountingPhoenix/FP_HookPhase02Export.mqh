#ifndef __FP_HOOK_PHASE02_EXPORT_MQH__
#define __FP_HOOK_PHASE02_EXPORT_MQH__
#property strict

#include "FP_HookPhase02Visual.mqh"

string FP_HookP02SafeCsv(string s)
{
   StringReplace(s, "\"", "\"\"");
   return "\"" + s + "\"";
}

string FP_HookP02SequencePath(const FP_HookPhase02Config &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_HOOK_P02_DEFAULT_FOLDER;
   return folder + "\\hook_phase02_sequences.csv";
}

string FP_HookP02SummaryPath(const FP_HookPhase02Config &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_HOOK_P02_DEFAULT_FOLDER;
   return folder + "\\hook_phase02_summary.csv";
}

string FP_HookP02SequenceHeader()
{
   return "schema_version,version,sequence_id,direction,state,scale_l,origin_node_id,origin_bar_index,origin_time,origin_price,x_count,x1_node_id,x1_bar_index,x1_time,x1_price,x2_node_id,x2_bar_index,x2_time,x2_price,x3_node_id,x3_bar_index,x3_time,x3_price,x4_node_id,x4_bar_index,x4_time,x4_price,cycle_crown_node_id,cycle_crown_time,cycle_crown_price,cycle_crown_valid,resolve_node_id,resolve_time,resolve_price,resolve_confirmed,retracement_ratio,near_death_confirmed,hook_failed,failure_node_id,failure_time,failure_price,render_eligible,visibility_reason,valid_after_hook,valid_after_opposing_f3,valid_hook_family,hook_validity_family,previous_hook_sequence_id,previous_hook_terminal_node_id,opposing_f3_event_id,death_boundary_price,capped,valid,source,reject_reason";
}

string FP_HookP02SequenceRow(const FP_HookPhase02Sequence &s)
{
   string row = "";
   row += FP_HookP02SafeCsv(FP_HOOK_P02_SCHEMA_VERSION);
   row += "," + FP_HookP02SafeCsv(FP_HOOK_P02_VERSION);
   row += "," + IntegerToString(s.sequence_id);
   row += "," + FP_HookP02SafeCsv(FP_HookP02DirectionName(s.direction));
   row += "," + FP_HookP02SafeCsv(FP_HookP02StateName(s.state));
   row += "," + IntegerToString(s.scale_l);
   row += "," + IntegerToString(s.origin_node_id);
   row += "," + IntegerToString(s.origin_bar_index);
   row += "," + FP_HookP02SafeCsv(TimeToString(s.origin_time, TIME_DATE|TIME_SECONDS));
   row += "," + DoubleToString(s.origin_price, _Digits);
   row += "," + IntegerToString(s.x_count);

   row += "," + IntegerToString(s.x1_node_id);
   row += "," + IntegerToString(s.x1_bar_index);
   row += "," + FP_HookP02SafeCsv(TimeToString(s.x1_time, TIME_DATE|TIME_SECONDS));
   row += "," + DoubleToString(s.x1_price, _Digits);

   row += "," + IntegerToString(s.x2_node_id);
   row += "," + IntegerToString(s.x2_bar_index);
   row += "," + FP_HookP02SafeCsv(TimeToString(s.x2_time, TIME_DATE|TIME_SECONDS));
   row += "," + DoubleToString(s.x2_price, _Digits);

   row += "," + IntegerToString(s.x3_node_id);
   row += "," + IntegerToString(s.x3_bar_index);
   row += "," + FP_HookP02SafeCsv(TimeToString(s.x3_time, TIME_DATE|TIME_SECONDS));
   row += "," + DoubleToString(s.x3_price, _Digits);

   row += "," + IntegerToString(s.x4_node_id);
   row += "," + IntegerToString(s.x4_bar_index);
   row += "," + FP_HookP02SafeCsv(TimeToString(s.x4_time, TIME_DATE|TIME_SECONDS));
   row += "," + DoubleToString(s.x4_price, _Digits);

   row += "," + IntegerToString(s.cycle_crown_node_id);
   row += "," + FP_HookP02SafeCsv(TimeToString(s.cycle_crown_time, TIME_DATE|TIME_SECONDS));
   row += "," + DoubleToString(s.cycle_crown_price, _Digits);
   row += "," + FP_HookP02SafeCsv(FP_HookP02BoolName(s.cycle_crown_valid));

   row += "," + IntegerToString(s.resolve_node_id);
   row += "," + FP_HookP02SafeCsv(TimeToString(s.resolve_time, TIME_DATE|TIME_SECONDS));
   row += "," + DoubleToString(s.resolve_price, _Digits);
   row += "," + FP_HookP02SafeCsv(FP_HookP02BoolName(s.resolve_confirmed));
   row += "," + DoubleToString(s.retracement_ratio, 6);
   row += "," + FP_HookP02SafeCsv(FP_HookP02BoolName(s.near_death_confirmed));
   row += "," + FP_HookP02SafeCsv(FP_HookP02BoolName(s.hook_failed));
   row += "," + IntegerToString(s.failure_node_id);
   row += "," + FP_HookP02SafeCsv(TimeToString(s.failure_time, TIME_DATE|TIME_SECONDS));
   row += "," + DoubleToString(s.failure_price, _Digits);
   row += "," + FP_HookP02SafeCsv(FP_HookP02BoolName(s.render_eligible));
   row += "," + FP_HookP02SafeCsv(s.visibility_reason);
   row += "," + FP_HookP02SafeCsv(FP_HookP02BoolName(s.valid_after_hook));
   row += "," + FP_HookP02SafeCsv(FP_HookP02BoolName(s.valid_after_opposing_f3));
   row += "," + FP_HookP02SafeCsv(FP_HookP02BoolName(s.valid_hook_family));
   row += "," + FP_HookP02SafeCsv(s.hook_validity_family);
   row += "," + IntegerToString(s.previous_hook_sequence_id);
   row += "," + IntegerToString(s.previous_hook_terminal_node_id);
   row += "," + IntegerToString(s.opposing_f3_event_id);

   row += "," + DoubleToString(s.death_boundary_price, _Digits);
   row += "," + FP_HookP02SafeCsv(FP_HookP02BoolName(s.capped));
   row += "," + FP_HookP02SafeCsv(FP_HookP02BoolName(s.valid));
   row += "," + FP_HookP02SafeCsv(s.source);
   row += "," + FP_HookP02SafeCsv(s.reject_reason);
   return row;
}

string FP_HookP02SummaryHeader()
{
   return "schema_version,version,symbol,period,display_family,origin_policy,seed_restart_guard,show_only_valid_hooks,valid_only_require_near_death,valid_f3_require_same_scale,bars_seen,bars_scanned,scales_seen,nodes_seen,sequences_total,positive,negative,ready,mature,capped,rejected,seed_reuse_rejects,valid_after_hook,valid_after_opposing_f3,valid_hook_family,invalid_family_filtered,origin_promotions,promoted_chains,drawn,status,reason";
}

string FP_HookP02SummaryRow(const string symbol,
                            const ENUM_TIMEFRAMES period,
                            const FP_HookPhase02Config &cfg,
                            const FP_HookPhase02Report &r)
{
   string row = "";
   row += FP_HookP02SafeCsv(FP_HOOK_P02_SCHEMA_VERSION);
   row += "," + FP_HookP02SafeCsv(FP_HOOK_P02_VERSION);
   row += "," + FP_HookP02SafeCsv(symbol);
   row += "," + FP_HookP02SafeCsv(EnumToString(period));
   row += "," + FP_HookP02SafeCsv(FP_HookP01DisplayFamilyName(cfg.display_family));
   row += "," + FP_HookP02SafeCsv(FP_HookP02OriginPolicyName(cfg.origin_policy));
   row += "," + FP_HookP02SafeCsv(FP_HookP02BoolName(cfg.seed_used_nodes_cannot_restart));
   row += "," + FP_HookP02SafeCsv(FP_HookP02BoolName(cfg.show_only_valid_hooks));
   row += "," + FP_HookP02SafeCsv(FP_HookP02BoolName(cfg.valid_only_require_near_death));
   row += "," + FP_HookP02SafeCsv(FP_HookP02BoolName(cfg.valid_f3_require_same_scale));
   row += "," + IntegerToString(r.bars_seen);
   row += "," + IntegerToString(r.bars_scanned);
   row += "," + IntegerToString(r.scales_seen);
   row += "," + IntegerToString(r.nodes_seen);
   row += "," + IntegerToString(r.sequences_total);
   row += "," + IntegerToString(r.sequences_positive);
   row += "," + IntegerToString(r.sequences_negative);
   row += "," + IntegerToString(r.sequences_ready);
   row += "," + IntegerToString(r.sequences_mature);
   row += "," + IntegerToString(r.sequences_capped);
   row += "," + IntegerToString(r.rejected_candidates);
   row += "," + IntegerToString(r.seed_reuse_rejects);
   row += "," + IntegerToString(r.valid_after_hook);
   row += "," + IntegerToString(r.valid_after_opposing_f3);
   row += "," + IntegerToString(r.valid_hook_family_total);
   row += "," + IntegerToString(r.invalid_family_filtered);
   row += "," + IntegerToString(r.origin_promotions);
   row += "," + IntegerToString(r.promoted_chains);
   row += "," + IntegerToString(r.sequences_drawn);
   row += "," + FP_HookP02SafeCsv(r.status);
   row += "," + FP_HookP02SafeCsv(r.reason);
   return row;
}

bool FP_HookP02ExportSequences(const FP_HookPhase02Config &cfg,
                               const FP_HookPhase02Sequence &sequences[],
                               FP_HookPhase02Report &report)
{
   if(!cfg.export_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_HOOK_P02_DEFAULT_FOLDER;
   FolderCreate(folder);

   int handle = FileOpen(FP_HookP02SequencePath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "HOOK_P02_SEQUENCE_EXPORT_OPEN_FAILED";
      return false;
   }

   FileWriteString(handle, FP_HookP02SequenceHeader() + "\r\n");
   for(int i=0; i<ArraySize(sequences); i++)
      FileWriteString(handle, FP_HookP02SequenceRow(sequences[i]) + "\r\n");
   FileClose(handle);
   report.files_written++;
   return true;
}

bool FP_HookP02ExportSummary(const string symbol,
                             const ENUM_TIMEFRAMES period,
                             const FP_HookPhase02Config &cfg,
                             FP_HookPhase02Report &report)
{
   if(!cfg.export_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_HOOK_P02_DEFAULT_FOLDER;
   FolderCreate(folder);

   int handle = FileOpen(FP_HookP02SummaryPath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "HOOK_P02_SUMMARY_EXPORT_OPEN_FAILED";
      return false;
   }

   FileWriteString(handle, FP_HookP02SummaryHeader() + "\r\n");
   FileWriteString(handle, FP_HookP02SummaryRow(symbol, period, cfg, report) + "\r\n");
   FileClose(handle);
   report.files_written++;
   return true;
}

#endif // __FP_HOOK_PHASE02_EXPORT_MQH__
