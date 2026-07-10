#ifndef __FP_NDS_ENTRY_EXPORT_MQH__
#define __FP_NDS_ENTRY_EXPORT_MQH__
#property strict

#include "FP_NDSEntryRules.mqh"

string FP_NDSEntrySafeCsv(string value)
{
   StringReplace(value, "\"", "\"\"");
   return "\"" + value + "\"";
}

string FP_NDSEntryFolder(const FP_NDSEntryConfig &cfg)
{
   if(StringLen(cfg.folder) > 0)
      return cfg.folder;
   return FP_NDS_ENTRY_DEFAULT_FOLDER;
}

bool FP_NDSEntryWriteSingleRow(const string path,
                               const string header,
                               const string row,
                               FP_NDSEntryReport &report)
{
   int handle = FileOpen(path, FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      return false;
   }
   FileWriteString(handle, header + "\r\n");
   FileWriteString(handle, row + "\r\n");
   FileClose(handle);
   report.files_written++;
   return true;
}

string FP_NDSStructureHeader()
{
   return "generated_at,version,symbol,period,available,eligible,status,block_reason,sequence_id,scale_l,hook_direction,validity_family,post_f3_subfamily,valid_after_hook,valid_after_opposing_f3,valid_hook_family,sequence_valid,hook_failed,hook_closed,near_death_confirmed,resolve_confirmed,origin_bar_index,origin_time,origin_price,crown_node_id,crown_time,crown_price,terminal_node_id,terminal_time,terminal_price,death_boundary_price,completion_pct,parent_hook_sequence_id,opposing_f3_event_id,opposing_f3_terminal_bar_index,opposing_f3_terminal_time,opposing_f3_terminal_price,structure_key";
}

string FP_NDSStructureCsv(const FP_NDSEntryPipelineRow &p)
{
   FP_NDSStructureRow r = p.structure;
   string s = FP_NDSEntrySafeCsv(FP_NDSEntryTime(p.generated_at));
   s += "," + FP_NDSEntrySafeCsv(p.version);
   s += "," + FP_NDSEntrySafeCsv(p.symbol);
   s += "," + FP_NDSEntrySafeCsv(p.period_label);
   s += "," + FP_NDSEntrySafeCsv(FP_NDSEntryBool(r.available));
   s += "," + FP_NDSEntrySafeCsv(FP_NDSEntryBool(r.eligible));
   s += "," + FP_NDSEntrySafeCsv(r.status);
   s += "," + FP_NDSEntrySafeCsv(r.block_reason);
   s += "," + IntegerToString(r.sequence_id);
   s += "," + IntegerToString(r.scale_l);
   s += "," + FP_NDSEntrySafeCsv(r.hook_direction_label);
   s += "," + FP_NDSEntrySafeCsv(r.validity_family);
   s += "," + FP_NDSEntrySafeCsv(r.post_f3_subfamily);
   s += "," + FP_NDSEntrySafeCsv(FP_NDSEntryBool(r.valid_after_hook));
   s += "," + FP_NDSEntrySafeCsv(FP_NDSEntryBool(r.valid_after_opposing_f3));
   s += "," + FP_NDSEntrySafeCsv(FP_NDSEntryBool(r.valid_hook_family));
   s += "," + FP_NDSEntrySafeCsv(FP_NDSEntryBool(r.sequence_valid));
   s += "," + FP_NDSEntrySafeCsv(FP_NDSEntryBool(r.hook_failed));
   s += "," + FP_NDSEntrySafeCsv(FP_NDSEntryBool(r.hook_closed));
   s += "," + FP_NDSEntrySafeCsv(FP_NDSEntryBool(r.near_death_confirmed));
   s += "," + FP_NDSEntrySafeCsv(FP_NDSEntryBool(r.resolve_confirmed));
   s += "," + IntegerToString(r.origin_bar_index);
   s += "," + FP_NDSEntrySafeCsv(FP_NDSEntryTime(r.origin_time));
   s += "," + DoubleToString(r.origin_price, _Digits);
   s += "," + IntegerToString(r.crown_node_id);
   s += "," + FP_NDSEntrySafeCsv(FP_NDSEntryTime(r.crown_time));
   s += "," + DoubleToString(r.crown_price, _Digits);
   s += "," + IntegerToString(r.terminal_node_id);
   s += "," + FP_NDSEntrySafeCsv(FP_NDSEntryTime(r.terminal_time));
   s += "," + DoubleToString(r.terminal_price, _Digits);
   s += "," + DoubleToString(r.death_boundary_price, _Digits);
   s += "," + DoubleToString(r.completion_pct, 3);
   s += "," + IntegerToString(r.parent_hook_sequence_id);
   s += "," + IntegerToString(r.opposing_f3_event_id);
   s += "," + IntegerToString(r.opposing_f3_terminal_bar_index);
   s += "," + FP_NDSEntrySafeCsv(FP_NDSEntryTime(r.opposing_f3_terminal_time));
   s += "," + DoubleToString(r.opposing_f3_terminal_price, _Digits);
   s += "," + FP_NDSEntrySafeCsv(r.structure_key);
   return s;
}

string FP_NDSSetupHeader()
{
   return "generated_at,version,symbol,period,candidate_created,ready,status,block_reason,setup_id,setup_family,source_structure_key,source_zone_key,trade_direction,order_model,stop_model,target_model,created_bar_index,created_time,expiry_bars,expires_bar_index,setup_key,zone_available,zone_canonical,zone_status,zone_block_reason,zone_id,zone_source_mode,zone_lower,zone_upper,zone_width,zone_entry,zone_stop,zone_target,zone_key";
}

string FP_NDSSetupCsv(const FP_NDSEntryPipelineRow &p)
{
   FP_NDSSetupRow r = p.setup;
   FP_NDSZoneRow z = p.zone;
   string s = FP_NDSEntrySafeCsv(FP_NDSEntryTime(p.generated_at));
   s += "," + FP_NDSEntrySafeCsv(p.version);
   s += "," + FP_NDSEntrySafeCsv(p.symbol);
   s += "," + FP_NDSEntrySafeCsv(p.period_label);
   s += "," + FP_NDSEntrySafeCsv(FP_NDSEntryBool(r.candidate_created));
   s += "," + FP_NDSEntrySafeCsv(FP_NDSEntryBool(r.ready));
   s += "," + FP_NDSEntrySafeCsv(r.status);
   s += "," + FP_NDSEntrySafeCsv(r.block_reason);
   s += "," + FP_NDSEntrySafeCsv(r.setup_id);
   s += "," + FP_NDSEntrySafeCsv(r.setup_family);
   s += "," + FP_NDSEntrySafeCsv(r.source_structure_key);
   s += "," + FP_NDSEntrySafeCsv(r.source_zone_key);
   s += "," + FP_NDSEntrySafeCsv(r.trade_direction_label);
   s += "," + FP_NDSEntrySafeCsv(FP_NDSEntryOrderModelName(r.order_model));
   s += "," + FP_NDSEntrySafeCsv(FP_NDSStopModelName(r.stop_model));
   s += "," + FP_NDSEntrySafeCsv(FP_NDSTargetModelName(r.target_model));
   s += "," + IntegerToString(r.created_bar_index);
   s += "," + FP_NDSEntrySafeCsv(FP_NDSEntryTime(r.created_time));
   s += "," + IntegerToString(r.expiry_bars);
   s += "," + IntegerToString(r.expires_bar_index);
   s += "," + FP_NDSEntrySafeCsv(r.setup_key);
   s += "," + FP_NDSEntrySafeCsv(FP_NDSEntryBool(z.available));
   s += "," + FP_NDSEntrySafeCsv(FP_NDSEntryBool(z.canonical));
   s += "," + FP_NDSEntrySafeCsv(z.status);
   s += "," + FP_NDSEntrySafeCsv(z.block_reason);
   s += "," + FP_NDSEntrySafeCsv(z.zone_id);
   s += "," + FP_NDSEntrySafeCsv(z.source_mode);
   s += "," + DoubleToString(z.lower_price, _Digits);
   s += "," + DoubleToString(z.upper_price, _Digits);
   s += "," + DoubleToString(z.width, _Digits);
   s += "," + DoubleToString(z.planned_entry_price, _Digits);
   s += "," + DoubleToString(z.planned_stop_price, _Digits);
   s += "," + DoubleToString(z.planned_target_price, _Digits);
   s += "," + FP_NDSEntrySafeCsv(z.zone_key);
   return s;
}

string FP_NDSPlanHeader()
{
   return "generated_at,version,symbol,period,ready,status,block_reason,plan_id,source_setup_id,trade_direction,entry_price,stop_price,target_price,risk_distance,reward_distance,rr,min_rr_required,requested_risk_fraction,requested_volume,sizing_status,plan_key";
}

string FP_NDSPlanCsv(const FP_NDSEntryPipelineRow &p)
{
   FP_NDSTradePlanRow r = p.plan;
   string s = FP_NDSEntrySafeCsv(FP_NDSEntryTime(p.generated_at));
   s += "," + FP_NDSEntrySafeCsv(p.version);
   s += "," + FP_NDSEntrySafeCsv(p.symbol);
   s += "," + FP_NDSEntrySafeCsv(p.period_label);
   s += "," + FP_NDSEntrySafeCsv(FP_NDSEntryBool(r.ready));
   s += "," + FP_NDSEntrySafeCsv(r.status);
   s += "," + FP_NDSEntrySafeCsv(r.block_reason);
   s += "," + FP_NDSEntrySafeCsv(r.plan_id);
   s += "," + FP_NDSEntrySafeCsv(r.source_setup_id);
   s += "," + FP_NDSEntrySafeCsv(r.trade_direction_label);
   s += "," + DoubleToString(r.entry_price, _Digits);
   s += "," + DoubleToString(r.stop_price, _Digits);
   s += "," + DoubleToString(r.target_price, _Digits);
   s += "," + DoubleToString(r.risk_distance, _Digits);
   s += "," + DoubleToString(r.reward_distance, _Digits);
   s += "," + DoubleToString(r.rr, 4);
   s += "," + DoubleToString(r.min_rr_required, 4);
   s += "," + DoubleToString(r.requested_risk_fraction, 6);
   s += "," + DoubleToString(r.requested_volume, 4);
   s += "," + FP_NDSEntrySafeCsv(r.sizing_status);
   s += "," + FP_NDSEntrySafeCsv(r.plan_key);
   return s;
}

string FP_NDSCommandHeader()
{
   return "generated_at,version,symbol,period,built,send_allowed,status,block_reason,command_id,source_plan_id,command_action,order_type_preview,trade_direction,volume,price,sl,tp,expiry_bars,magic,comment,command_key,execution_status";
}

string FP_NDSCommandCsv(const FP_NDSEntryPipelineRow &p)
{
   FP_NDSCommandPreviewRow r = p.command;
   string s = FP_NDSEntrySafeCsv(FP_NDSEntryTime(p.generated_at));
   s += "," + FP_NDSEntrySafeCsv(p.version);
   s += "," + FP_NDSEntrySafeCsv(p.symbol);
   s += "," + FP_NDSEntrySafeCsv(p.period_label);
   s += "," + FP_NDSEntrySafeCsv(FP_NDSEntryBool(r.built));
   s += "," + FP_NDSEntrySafeCsv(FP_NDSEntryBool(r.send_allowed));
   s += "," + FP_NDSEntrySafeCsv(r.status);
   s += "," + FP_NDSEntrySafeCsv(r.block_reason);
   s += "," + FP_NDSEntrySafeCsv(r.command_id);
   s += "," + FP_NDSEntrySafeCsv(r.source_plan_id);
   s += "," + FP_NDSEntrySafeCsv(r.command_action);
   s += "," + FP_NDSEntrySafeCsv(r.order_type_preview);
   s += "," + FP_NDSEntrySafeCsv(r.trade_direction_label);
   s += "," + DoubleToString(r.volume, 4);
   s += "," + DoubleToString(r.price, _Digits);
   s += "," + DoubleToString(r.sl, _Digits);
   s += "," + DoubleToString(r.tp, _Digits);
   s += "," + IntegerToString(r.expiry_bars);
   s += "," + IntegerToString((int)r.magic);
   s += "," + FP_NDSEntrySafeCsv(r.comment);
   s += "," + FP_NDSEntrySafeCsv(r.command_key);
   s += "," + FP_NDSEntrySafeCsv(r.execution_status);
   return s;
}

string FP_NDSSummaryHeader()
{
   return "generated_at,version,schema_version,symbol,period,attempted,stage,status,block_reason,structure_available,structure_eligible,zone_available,zone_canonical,setup_candidate,setup_ready,plan_ready,command_built,send_allowed,no_send_contract,pipeline_key";
}

string FP_NDSSummaryCsv(const FP_NDSEntryPipelineRow &p)
{
   string s = FP_NDSEntrySafeCsv(FP_NDSEntryTime(p.generated_at));
   s += "," + FP_NDSEntrySafeCsv(p.version);
   s += "," + FP_NDSEntrySafeCsv(p.schema_version);
   s += "," + FP_NDSEntrySafeCsv(p.symbol);
   s += "," + FP_NDSEntrySafeCsv(p.period_label);
   s += "," + FP_NDSEntrySafeCsv(FP_NDSEntryBool(p.attempted));
   s += "," + FP_NDSEntrySafeCsv(p.stage_label);
   s += "," + FP_NDSEntrySafeCsv(p.status);
   s += "," + FP_NDSEntrySafeCsv(p.block_reason);
   s += "," + FP_NDSEntrySafeCsv(FP_NDSEntryBool(p.structure.available));
   s += "," + FP_NDSEntrySafeCsv(FP_NDSEntryBool(p.structure.eligible));
   s += "," + FP_NDSEntrySafeCsv(FP_NDSEntryBool(p.zone.available));
   s += "," + FP_NDSEntrySafeCsv(FP_NDSEntryBool(p.zone.canonical));
   s += "," + FP_NDSEntrySafeCsv(FP_NDSEntryBool(p.setup.candidate_created));
   s += "," + FP_NDSEntrySafeCsv(FP_NDSEntryBool(p.setup.ready));
   s += "," + FP_NDSEntrySafeCsv(FP_NDSEntryBool(p.plan.ready));
   s += "," + FP_NDSEntrySafeCsv(FP_NDSEntryBool(p.command.built));
   s += "," + FP_NDSEntrySafeCsv(FP_NDSEntryBool(p.command.send_allowed));
   s += "," + FP_NDSEntrySafeCsv(p.no_send_contract);
   s += "," + FP_NDSEntrySafeCsv(p.pipeline_key);
   return s;
}

bool FP_NDSExportEntryPipeline(const FP_NDSEntryConfig &cfg,
                               const FP_NDSEntryPipelineRow &row,
                               FP_NDSEntryReport &report)
{
   if(!cfg.export_csv)
      return true;

   string folder = FP_NDSEntryFolder(cfg);
   FolderCreate(folder);
   bool ok = true;

   if(FP_NDSEntryWriteSingleRow(folder + "\\nds_entry_structure_snapshot.csv", FP_NDSStructureHeader(), FP_NDSStructureCsv(row), report))
      report.structure_written = true;
   else ok = false;

   if(FP_NDSEntryWriteSingleRow(folder + "\\nds_entry_setup_candidate.csv", FP_NDSSetupHeader(), FP_NDSSetupCsv(row), report))
      report.setup_written = true;
   else ok = false;

   if(FP_NDSEntryWriteSingleRow(folder + "\\nds_entry_trade_plan.csv", FP_NDSPlanHeader(), FP_NDSPlanCsv(row), report))
      report.plan_written = true;
   else ok = false;

   if(FP_NDSEntryWriteSingleRow(folder + "\\nds_entry_command_preview.csv", FP_NDSCommandHeader(), FP_NDSCommandCsv(row), report))
      report.command_written = true;
   else ok = false;

   if(FP_NDSEntryWriteSingleRow(folder + "\\nds_entry_pipeline_summary.csv", FP_NDSSummaryHeader(), FP_NDSSummaryCsv(row), report))
      report.summary_written = true;
   else ok = false;

   return ok;
}

#endif // __FP_NDS_ENTRY_EXPORT_MQH__
