#ifndef __FP_STATE_GATE_EXPORT_MQH__
#define __FP_STATE_GATE_EXPORT_MQH__
#property strict

#include "FP_StateGateRules.mqh"
#include "FP_ExportRows.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 19 State Gate Export
// ----------------------------------------------------------------------------
// Phase 9 writes closed-bar tracker fields plus Rally View, Hook View,
// panel/debug rows, State Contract CSV, and a diagnostics CSV for compile and
// dashboard visibility hardening. Hook and Rally rows remain read-only projections.
// ============================================================================

bool FP_StateGateExportOpenWrite(const string path, int &handle)
{
   handle = FileOpen(path, FILE_WRITE|FILE_TXT|FILE_ANSI);
   return (handle != INVALID_HANDLE);
}

bool FP_StateGateExportWriteLine(const int handle, const string line)
{
   if(handle == INVALID_HANDLE) return false;
   FileWriteString(handle, line + "\r\n");
   return true;
}

string FP_StateGateExportFileName(const string suffix, const FP_StateGateConfig &cfg)
{
   if(cfg.export_overwrite_latest)
      return "latest_state_gate_" + suffix + ".csv";
   string stamp = TimeToString(TimeCurrent(), TIME_DATE|TIME_SECONDS);
   return FP_ExportSafeName("state_gate_" + stamp + "_" + suffix) + ".csv";
}

string FP_StateGateExportPath(const string suffix, const FP_StateGateConfig &cfg)
{
   return FP_ExportJoinPath(cfg.export_folder, FP_StateGateExportFileName(suffix, cfg));
}

string FP_StateGateSummaryHeader()
{
   string h = "";
   FP_ExportCsvAppend(h, "symbol");
   FP_ExportCsvAppend(h, "chart_timeframe");
   FP_ExportCsvAppend(h, "slot");
   FP_ExportCsvAppend(h, "timeframe");
   FP_ExportCsvAppend(h, "closed_bar_time");
   FP_ExportCsvAppend(h, "previous_closed_bar_time");
   FP_ExportCsvAppend(h, "closed_bar_close");
   FP_ExportCsvAppend(h, "bars_available");
   FP_ExportCsvAppend(h, "closed_bar_available");
   FP_ExportCsvAppend(h, "dirty");
   FP_ExportCsvAppend(h, "update_count");
   FP_ExportCsvAppend(h, "tracker_status");
   FP_ExportCsvAppend(h, "status");
   FP_ExportCsvAppend(h, "reason");
   FP_ExportCsvAppend(h, "rally_rows");
   FP_ExportCsvAppend(h, "hook_rows");
   FP_ExportCsvAppend(h, "extreme_candidate_rows");
   FP_ExportCsvAppend(h, "mtf_alignment_rows");
   FP_ExportCsvAppend(h, "latest_established_f_summary");
   FP_ExportCsvAppend(h, "probable_next_f_summary");
   FP_ExportCsvAppend(h, "hook_summary");
   FP_ExportCsvAppend(h, "state_key");
   FP_ExportCsvAppend(h, "primary_rally_key");
   FP_ExportCsvAppend(h, "primary_hook_key");
   FP_ExportCsvAppend(h, "anatomy_status");
   FP_ExportCsvAppend(h, "storage_status");
   FP_ExportCsvAppend(h, "entry_bridge_status");
   FP_ExportCsvAppend(h, "contract_status");
   FP_ExportCsvAppend(h, "entry_bridge_readiness");
   FP_ExportCsvAppend(h, "entry_bridge_key");
   FP_ExportCsvAppend(h, "candidate_extreme_status");
   FP_ExportCsvAppend(h, "candidate_extreme_key");
   FP_ExportCsvAppend(h, "candidate_extreme_source");
   FP_ExportCsvAppend(h, "candidate_direction");
   FP_ExportCsvAppend(h, "candidate_scale_context");
   FP_ExportCsvAppend(h, "x_invalidation_status");
   FP_ExportCsvAppend(h, "x_destination_status");
   FP_ExportCsvAppend(h, "optionality_status");
   FP_ExportCsvAppend(h, "extreme_map_status");
   FP_ExportCsvAppend(h, "extreme_map_key");
   FP_ExportCsvAppend(h, "primary_extreme_source");
   FP_ExportCsvAppend(h, "primary_extreme_direction");
   FP_ExportCsvAppend(h, "primary_extreme_side");
   FP_ExportCsvAppend(h, "primary_extreme_role");
   FP_ExportCsvAppend(h, "primary_extreme_price_status");
   FP_ExportCsvAppend(h, "primary_extreme_price");
   FP_ExportCsvAppend(h, "primary_extreme_node_id");
   FP_ExportCsvAppend(h, "primary_extreme_scale_L");
   FP_ExportCsvAppend(h, "extreme_map_notes");
   FP_ExportCsvAppend(h, "mtf_alignment_status");
   FP_ExportCsvAppend(h, "mtf_alignment_key");
   FP_ExportCsvAppend(h, "mtf_parent_timeframe");
   FP_ExportCsvAppend(h, "mtf_parent_extreme_key");
   FP_ExportCsvAppend(h, "mtf_parent_direction");
   FP_ExportCsvAppend(h, "mtf_parent_side");
   FP_ExportCsvAppend(h, "mtf_direction_relation");
   FP_ExportCsvAppend(h, "mtf_side_relation");
   FP_ExportCsvAppend(h, "mtf_context_role");
   FP_ExportCsvAppend(h, "geometry_readiness");
   FP_ExportCsvAppend(h, "candidate_entry_price_status");
   FP_ExportCsvAppend(h, "candidate_destination_price_status");
   FP_ExportCsvAppend(h, "destination_distance");
   FP_ExportCsvAppend(h, "potential_R_status");
   FP_ExportCsvAppend(h, "mtf_alignment_notes");
   FP_ExportCsvAppend(h, "candidate_entry_price_status");
   FP_ExportCsvAppend(h, "candidate_entry_price");
   FP_ExportCsvAppend(h, "candidate_invalidation_price_status");
   FP_ExportCsvAppend(h, "candidate_invalidation_price");
   FP_ExportCsvAppend(h, "candidate_destination_price_status");
   FP_ExportCsvAppend(h, "candidate_destination_price");
   FP_ExportCsvAppend(h, "risk_distance_status");
   FP_ExportCsvAppend(h, "risk_distance");
   FP_ExportCsvAppend(h, "destination_distance_status");
   FP_ExportCsvAppend(h, "destination_distance");
   FP_ExportCsvAppend(h, "potential_R_status");
   FP_ExportCsvAppend(h, "potential_R");
   FP_ExportCsvAppend(h, "geometry_readiness");
   FP_ExportCsvAppend(h, "geometry_key");
   FP_ExportCsvAppend(h, "geometry_notes");
   return h;
}



string FP_StateGateSummaryRow(const FP_StateGateSnapshot &snapshot, const int slot)
{
   FP_StateGateTimeframeState s = snapshot.tf_states[slot];
   string line = "";
   FP_ExportCsvAppend(line, snapshot.symbol);
   FP_ExportCsvAppend(line, EnumToString(snapshot.chart_timeframe));
   FP_ExportCsvAppend(line, IntegerToString(slot));
   FP_ExportCsvAppend(line, s.timeframe_label);
   FP_ExportCsvAppend(line, FP_ExportTime(s.last_closed_bar_time));
   FP_ExportCsvAppend(line, FP_ExportTime(s.previous_closed_bar_time));
   FP_ExportCsvAppend(line, FP_ExportDouble(s.last_closed_bar_close));
   FP_ExportCsvAppend(line, IntegerToString(s.bars_available));
   FP_ExportCsvAppend(line, FP_ExportBool(s.closed_bar_available));
   FP_ExportCsvAppend(line, FP_ExportBool(s.dirty));
   FP_ExportCsvAppend(line, IntegerToString(s.update_count));
   FP_ExportCsvAppend(line, s.tracker_status);
   FP_ExportCsvAppend(line, s.status);
   FP_ExportCsvAppend(line, s.reason);
   FP_ExportCsvAppend(line, IntegerToString(s.rally_row_count));
   FP_ExportCsvAppend(line, IntegerToString(s.hook_row_count));
   FP_ExportCsvAppend(line, IntegerToString(s.extreme_candidate_row_count));
   FP_ExportCsvAppend(line, IntegerToString(s.mtf_alignment_row_count));
   FP_ExportCsvAppend(line, s.latest_established_f_summary);
   FP_ExportCsvAppend(line, s.probable_next_f_summary);
   FP_ExportCsvAppend(line, s.hook_summary);
   FP_ExportCsvAppend(line, s.state_key);
   FP_ExportCsvAppend(line, s.primary_rally_key);
   FP_ExportCsvAppend(line, s.primary_hook_key);
   FP_ExportCsvAppend(line, s.anatomy_status);
   FP_ExportCsvAppend(line, s.storage_status);
   FP_ExportCsvAppend(line, s.entry_bridge_status);
   FP_ExportCsvAppend(line, s.contract_status);
   FP_ExportCsvAppend(line, s.entry_bridge_readiness);
   FP_ExportCsvAppend(line, s.entry_bridge_key);
   FP_ExportCsvAppend(line, s.candidate_extreme_status);
   FP_ExportCsvAppend(line, s.candidate_extreme_key);
   FP_ExportCsvAppend(line, s.candidate_extreme_source);
   FP_ExportCsvAppend(line, s.candidate_direction);
   FP_ExportCsvAppend(line, s.candidate_scale_context);
   FP_ExportCsvAppend(line, s.x_invalidation_status);
   FP_ExportCsvAppend(line, s.x_destination_status);
   FP_ExportCsvAppend(line, s.optionality_status);
   FP_ExportCsvAppend(line, s.extreme_map_status);
   FP_ExportCsvAppend(line, s.extreme_map_key);
   FP_ExportCsvAppend(line, s.primary_extreme_source);
   FP_ExportCsvAppend(line, s.primary_extreme_direction);
   FP_ExportCsvAppend(line, s.primary_extreme_side);
   FP_ExportCsvAppend(line, s.primary_extreme_role);
   FP_ExportCsvAppend(line, s.primary_extreme_price_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(s.primary_extreme_price));
   FP_ExportCsvAppend(line, IntegerToString(s.primary_extreme_node_id));
   FP_ExportCsvAppend(line, IntegerToString(s.primary_extreme_scale_L));
   FP_ExportCsvAppend(line, s.extreme_map_notes);
   FP_ExportCsvAppend(line, s.mtf_alignment_status);
   FP_ExportCsvAppend(line, s.mtf_alignment_key);
   FP_ExportCsvAppend(line, s.mtf_parent_timeframe);
   FP_ExportCsvAppend(line, s.mtf_parent_extreme_key);
   FP_ExportCsvAppend(line, s.mtf_parent_direction);
   FP_ExportCsvAppend(line, s.mtf_parent_side);
   FP_ExportCsvAppend(line, s.mtf_direction_relation);
   FP_ExportCsvAppend(line, s.mtf_side_relation);
   FP_ExportCsvAppend(line, s.mtf_context_role);
   FP_ExportCsvAppend(line, s.geometry_readiness);
   FP_ExportCsvAppend(line, s.candidate_entry_price_status);
   FP_ExportCsvAppend(line, s.candidate_destination_price_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(s.destination_distance));
   FP_ExportCsvAppend(line, s.potential_R_status);
   FP_ExportCsvAppend(line, s.mtf_alignment_notes);
   FP_ExportCsvAppend(line, s.candidate_entry_price_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(s.candidate_entry_price));
   FP_ExportCsvAppend(line, s.candidate_invalidation_price_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(s.candidate_invalidation_price));
   FP_ExportCsvAppend(line, s.candidate_destination_price_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(s.candidate_destination_price));
   FP_ExportCsvAppend(line, s.risk_distance_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(s.risk_distance));
   FP_ExportCsvAppend(line, s.destination_distance_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(s.destination_distance));
   FP_ExportCsvAppend(line, s.potential_R_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(s.potential_R));
   FP_ExportCsvAppend(line, s.geometry_readiness);
   FP_ExportCsvAppend(line, s.geometry_key);
   FP_ExportCsvAppend(line, s.geometry_notes);
   return line;
}



bool FP_StateGateExportSummaryCsv(const string path,
                                  const FP_StateGateSnapshot &snapshot,
                                  FP_StateGateReport &report)
{
   int handle = INVALID_HANDLE;
   if(!FP_StateGateExportOpenWrite(path, handle))
   {
      report.file_errors++;
      report.reason = report.reason + ";state_gate_summary_open_failed";
      return false;
   }
   FP_StateGateExportWriteLine(handle, FP_StateGateSummaryHeader());
   for(int i=0; i<snapshot.timeframe_count; i++)
      FP_StateGateExportWriteLine(handle, FP_StateGateSummaryRow(snapshot, i));
   FileClose(handle);
   report.files_written++;
   return true;
}

string FP_StateGateRallyHeader()
{
   string h = "";
   FP_ExportCsvAppend(h, "symbol");
   FP_ExportCsvAppend(h, "slot");
   FP_ExportCsvAppend(h, "timeframe");
   FP_ExportCsvAppend(h, "closed_bar_time");
   FP_ExportCsvAppend(h, "closed_bar_close");
   FP_ExportCsvAppend(h, "status");
   FP_ExportCsvAppend(h, "source_event_id");
   FP_ExportCsvAppend(h, "sequence_id");
   FP_ExportCsvAppend(h, "parent_event_id");
   FP_ExportCsvAppend(h, "scale_L");
   FP_ExportCsvAppend(h, "direction");
   FP_ExportCsvAppend(h, "f_level");
   FP_ExportCsvAppend(h, "latest_established_f");
   FP_ExportCsvAppend(h, "probable_next_f");
   FP_ExportCsvAppend(h, "body_state");
   FP_ExportCsvAppend(h, "flag_stage");
   FP_ExportCsvAppend(h, "post_flag_stage");
   FP_ExportCsvAppend(h, "source_id");
   FP_ExportCsvAppend(h, "label");
   return h;
}

string FP_StateGateRallyCsvRow(const string symbol, const FP_StateGateRallyRow &r)
{
   string line = "";
   FP_ExportCsvAppend(line, symbol);
   FP_ExportCsvAppend(line, IntegerToString(r.slot_index));
   FP_ExportCsvAppend(line, r.timeframe_label);
   FP_ExportCsvAppend(line, FP_ExportTime(r.last_closed_bar_time));
   FP_ExportCsvAppend(line, FP_ExportDouble(r.last_closed_bar_close));
   FP_ExportCsvAppend(line, IntegerToString(r.status));
   FP_ExportCsvAppend(line, IntegerToString(r.source_event_id));
   FP_ExportCsvAppend(line, IntegerToString(r.sequence_id));
   FP_ExportCsvAppend(line, IntegerToString(r.parent_event_id));
   FP_ExportCsvAppend(line, IntegerToString(r.scale_L));
   FP_ExportCsvAppend(line, IntegerToString(r.direction));
   FP_ExportCsvAppend(line, IntegerToString(r.f_level));
   FP_ExportCsvAppend(line, r.latest_established_f);
   FP_ExportCsvAppend(line, r.probable_next_f);
   FP_ExportCsvAppend(line, r.body_state);
   FP_ExportCsvAppend(line, r.flag_stage);
   FP_ExportCsvAppend(line, r.post_flag_stage);
   FP_ExportCsvAppend(line, r.source_id);
   FP_ExportCsvAppend(line, r.label);
   return line;
}

bool FP_StateGateExportRallyCsv(const string path,
                                const FP_StateGateSnapshot &snapshot,
                                FP_StateGateReport &report)
{
   int handle = INVALID_HANDLE;
   if(!FP_StateGateExportOpenWrite(path, handle))
   {
      report.file_errors++;
      report.reason = report.reason + ";state_gate_rally_open_failed";
      return false;
   }
   FP_StateGateExportWriteLine(handle, FP_StateGateRallyHeader());
   for(int r=0; r<snapshot.rally_row_count; r++)
      FP_StateGateExportWriteLine(handle, FP_StateGateRallyCsvRow(snapshot.symbol, snapshot.rally_rows[r]));
   FileClose(handle);
   report.files_written++;
   return true;
}

string FP_StateGateHookHeader()
{
   string h = "";
   FP_ExportCsvAppend(h, "symbol");
   FP_ExportCsvAppend(h, "slot");
   FP_ExportCsvAppend(h, "timeframe");
   FP_ExportCsvAppend(h, "closed_bar_time");
   FP_ExportCsvAppend(h, "closed_bar_close");
   FP_ExportCsvAppend(h, "status");
   FP_ExportCsvAppend(h, "source_hook_id");
   FP_ExportCsvAppend(h, "sequence_id");
   FP_ExportCsvAppend(h, "scale_L");
   FP_ExportCsvAppend(h, "direction");
   FP_ExportCsvAppend(h, "polarity");
   FP_ExportCsvAppend(h, "current_node_number");
   FP_ExportCsvAppend(h, "latest_high_node_id");
   FP_ExportCsvAppend(h, "latest_high_node_price");
   FP_ExportCsvAppend(h, "latest_low_node_id");
   FP_ExportCsvAppend(h, "latest_low_node_price");
   FP_ExportCsvAppend(h, "position_label");
   FP_ExportCsvAppend(h, "source_id");
   FP_ExportCsvAppend(h, "label");
   return h;
}

string FP_StateGateHookCsvRow(const string symbol, const FP_StateGateHookRow &hrow)
{
   string line = "";
   FP_ExportCsvAppend(line, symbol);
   FP_ExportCsvAppend(line, IntegerToString(hrow.slot_index));
   FP_ExportCsvAppend(line, hrow.timeframe_label);
   FP_ExportCsvAppend(line, FP_ExportTime(hrow.last_closed_bar_time));
   FP_ExportCsvAppend(line, FP_ExportDouble(hrow.last_closed_bar_close));
   FP_ExportCsvAppend(line, IntegerToString(hrow.status));
   FP_ExportCsvAppend(line, IntegerToString(hrow.source_hook_id));
   FP_ExportCsvAppend(line, IntegerToString(hrow.sequence_id));
   FP_ExportCsvAppend(line, IntegerToString(hrow.scale_L));
   FP_ExportCsvAppend(line, IntegerToString(hrow.direction));
   FP_ExportCsvAppend(line, hrow.polarity);
   FP_ExportCsvAppend(line, IntegerToString(hrow.current_node_number));
   FP_ExportCsvAppend(line, IntegerToString(hrow.latest_high_node_id));
   FP_ExportCsvAppend(line, FP_ExportDouble(hrow.latest_high_node_price));
   FP_ExportCsvAppend(line, IntegerToString(hrow.latest_low_node_id));
   FP_ExportCsvAppend(line, FP_ExportDouble(hrow.latest_low_node_price));
   FP_ExportCsvAppend(line, hrow.position_label);
   FP_ExportCsvAppend(line, hrow.source_id);
   FP_ExportCsvAppend(line, hrow.label);
   return line;
}

bool FP_StateGateExportHookCsv(const string path,
                               const FP_StateGateSnapshot &snapshot,
                               FP_StateGateReport &report)
{
   int handle = INVALID_HANDLE;
   if(!FP_StateGateExportOpenWrite(path, handle))
   {
      report.file_errors++;
      report.reason = report.reason + ";state_gate_hooks_open_failed";
      return false;
   }
   FP_StateGateExportWriteLine(handle, FP_StateGateHookHeader());
   for(int h=0; h<snapshot.hook_row_count; h++)
      FP_StateGateExportWriteLine(handle, FP_StateGateHookCsvRow(snapshot.symbol, snapshot.hook_rows[h]));
   FileClose(handle);
   report.files_written++;
   return true;
}


string FP_StateGatePanelHeader()
{
   string h = "";
   FP_ExportCsvAppend(h, "symbol");
   FP_ExportCsvAppend(h, "slot");
   FP_ExportCsvAppend(h, "timeframe");
   FP_ExportCsvAppend(h, "dirty");
   FP_ExportCsvAppend(h, "closed_bar_time");
   FP_ExportCsvAppend(h, "closed_bar_close");
   FP_ExportCsvAppend(h, "rally_rows_total");
   FP_ExportCsvAppend(h, "hook_rows_total");
   FP_ExportCsvAppend(h, "extreme_candidate_rows_total");
   FP_ExportCsvAppend(h, "mtf_alignment_rows_total");
   FP_ExportCsvAppend(h, "rally_preview_limit");
   FP_ExportCsvAppend(h, "hook_preview_limit");
   FP_ExportCsvAppend(h, "latest_established_f_summary");
   FP_ExportCsvAppend(h, "probable_next_f_summary");
   FP_ExportCsvAppend(h, "hook_summary");
   FP_ExportCsvAppend(h, "state_key");
   FP_ExportCsvAppend(h, "contract_status");
   FP_ExportCsvAppend(h, "entry_bridge_status");
   FP_ExportCsvAppend(h, "entry_bridge_readiness");
   FP_ExportCsvAppend(h, "candidate_extreme_status");
   FP_ExportCsvAppend(h, "candidate_extreme_key");
   FP_ExportCsvAppend(h, "extreme_map_status");
   FP_ExportCsvAppend(h, "extreme_map_key");
   FP_ExportCsvAppend(h, "primary_extreme_source");
   FP_ExportCsvAppend(h, "primary_extreme_side");
   FP_ExportCsvAppend(h, "primary_extreme_price_status");
   FP_ExportCsvAppend(h, "mtf_alignment_status");
   FP_ExportCsvAppend(h, "mtf_parent_timeframe");
   FP_ExportCsvAppend(h, "mtf_direction_relation");
   FP_ExportCsvAppend(h, "mtf_side_relation");
   FP_ExportCsvAppend(h, "mtf_context_role");
   FP_ExportCsvAppend(h, "tracker_status");
   FP_ExportCsvAppend(h, "reason");
   return h;
}



string FP_StateGatePanelCsvRow(const FP_StateGateConfig &cfg,
                               const FP_StateGateSnapshot &snapshot,
                               const int slot)
{
   FP_StateGateTimeframeState s = snapshot.tf_states[slot];
   string line = "";
   FP_ExportCsvAppend(line, snapshot.symbol);
   FP_ExportCsvAppend(line, IntegerToString(slot));
   FP_ExportCsvAppend(line, s.timeframe_label);
   FP_ExportCsvAppend(line, FP_ExportBool(s.dirty));
   FP_ExportCsvAppend(line, FP_ExportTime(s.last_closed_bar_time));
   FP_ExportCsvAppend(line, FP_ExportDouble(s.last_closed_bar_close));
   FP_ExportCsvAppend(line, IntegerToString(s.rally_row_count));
   FP_ExportCsvAppend(line, IntegerToString(s.hook_row_count));
   FP_ExportCsvAppend(line, IntegerToString(s.extreme_candidate_row_count));
   FP_ExportCsvAppend(line, IntegerToString(s.mtf_alignment_row_count));
   FP_ExportCsvAppend(line, IntegerToString(cfg.panel_rally_preview_rows_per_tf));
   FP_ExportCsvAppend(line, IntegerToString(cfg.panel_hook_preview_rows_per_tf));
   FP_ExportCsvAppend(line, s.latest_established_f_summary);
   FP_ExportCsvAppend(line, s.probable_next_f_summary);
   FP_ExportCsvAppend(line, s.hook_summary);
   FP_ExportCsvAppend(line, s.state_key);
   FP_ExportCsvAppend(line, s.contract_status);
   FP_ExportCsvAppend(line, s.entry_bridge_status);
   FP_ExportCsvAppend(line, s.entry_bridge_readiness);
   FP_ExportCsvAppend(line, s.candidate_extreme_status);
   FP_ExportCsvAppend(line, s.candidate_extreme_key);
   FP_ExportCsvAppend(line, s.extreme_map_status);
   FP_ExportCsvAppend(line, s.extreme_map_key);
   FP_ExportCsvAppend(line, s.primary_extreme_source);
   FP_ExportCsvAppend(line, s.primary_extreme_side);
   FP_ExportCsvAppend(line, s.primary_extreme_price_status);
   FP_ExportCsvAppend(line, s.mtf_alignment_status);
   FP_ExportCsvAppend(line, s.mtf_parent_timeframe);
   FP_ExportCsvAppend(line, s.mtf_direction_relation);
   FP_ExportCsvAppend(line, s.mtf_side_relation);
   FP_ExportCsvAppend(line, s.mtf_context_role);
   FP_ExportCsvAppend(line, s.tracker_status);
   FP_ExportCsvAppend(line, s.reason);
   return line;
}



bool FP_StateGateExportPanelCsv(const string path,
                                const FP_StateGateConfig &cfg,
                                const FP_StateGateSnapshot &snapshot,
                                FP_StateGateReport &report)
{
   int handle = INVALID_HANDLE;
   if(!FP_StateGateExportOpenWrite(path, handle))
   {
      report.file_errors++;
      report.reason = report.reason + ";state_gate_panel_open_failed";
      return false;
   }
   FP_StateGateExportWriteLine(handle, FP_StateGatePanelHeader());
   for(int i=0; i<snapshot.timeframe_count; i++)
      FP_StateGateExportWriteLine(handle, FP_StateGatePanelCsvRow(cfg, snapshot, i));
   FileClose(handle);
   report.files_written++;
   return true;
}



// ---------------------------------------------------------------------------
// Phase 10 - Panel Lines Contract
// ---------------------------------------------------------------------------
// This CSV mirrors the logical dashboard line model in an expanded state so
// every visible idea on the panel can be traced even if the chart objects are
// clipped, hidden by old input sets, or collapsed by the operator.
// It is a debug/export contract only. It never modifies the State Gate snapshot.

string FP_StateGatePanelLineHeader()
{
   string h = "";
   FP_ExportCsvAppend(h, "symbol");
   FP_ExportCsvAppend(h, "update_serial");
   FP_ExportCsvAppend(h, "line_index");
   FP_ExportCsvAppend(h, "slot");
   FP_ExportCsvAppend(h, "timeframe");
   FP_ExportCsvAppend(h, "section");
   FP_ExportCsvAppend(h, "line_type");
   FP_ExportCsvAppend(h, "preview_index");
   FP_ExportCsvAppend(h, "source_kind");
   FP_ExportCsvAppend(h, "source_id");
   FP_ExportCsvAppend(h, "effective_corner");
   FP_ExportCsvAppend(h, "panel_x");
   FP_ExportCsvAppend(h, "panel_y");
   FP_ExportCsvAppend(h, "text");
   FP_ExportCsvAppend(h, "closed_bar_time");
   FP_ExportCsvAppend(h, "state_key");
   FP_ExportCsvAppend(h, "contract_status");
   FP_ExportCsvAppend(h, "entry_bridge_status");
   return h;
}

string FP_StateGatePanelLineRow(const FP_StateGateConfig &cfg,
                                const FP_StateGateSnapshot &snapshot,
                                const int line_index,
                                const int slot,
                                const string section,
                                const string line_type,
                                const int preview_index,
                                const string source_kind,
                                const string source_id,
                                const string text,
                                const datetime closed_bar_time,
                                const string state_key,
                                const string contract_status,
                                const string entry_bridge_status)
{
   string line = "";
   FP_ExportCsvAppend(line, snapshot.symbol);
   FP_ExportCsvAppend(line, IntegerToString(snapshot.update_serial));
   FP_ExportCsvAppend(line, IntegerToString(line_index));
   FP_ExportCsvAppend(line, IntegerToString(slot));
   if(slot >= 0 && slot < snapshot.timeframe_count)
      FP_ExportCsvAppend(line, snapshot.tf_states[slot].timeframe_label);
   else
      FP_ExportCsvAppend(line, "GLOBAL");
   FP_ExportCsvAppend(line, section);
   FP_ExportCsvAppend(line, line_type);
   FP_ExportCsvAppend(line, IntegerToString(preview_index));
   FP_ExportCsvAppend(line, source_kind);
   FP_ExportCsvAppend(line, source_id);
   FP_ExportCsvAppend(line, FP_StateGateEffectiveCornerName(cfg));
   FP_ExportCsvAppend(line, IntegerToString(cfg.panel_x));
   FP_ExportCsvAppend(line, IntegerToString(cfg.panel_y));
   FP_ExportCsvAppend(line, text);
   FP_ExportCsvAppend(line, FP_ExportTime(closed_bar_time));
   FP_ExportCsvAppend(line, state_key);
   FP_ExportCsvAppend(line, contract_status);
   FP_ExportCsvAppend(line, entry_bridge_status);
   return line;
}

string FP_StateGatePanelLineTrackerText(const FP_StateGateConfig &cfg,
                                        const FP_StateGateTimeframeState &s)
{
   string text = s.timeframe_label + " | " + FP_StateGateDirtyLabel(s);
   if(cfg.panel_show_closed_bar)
   {
      text += " | closed=" + FP_StateGateClosedBarTimeLabel(s.last_closed_bar_time);
      text += " | close=" + FP_StateGateCloseLabel(s.last_closed_bar_close);
   }
   text += " | updates=" + IntegerToString(s.update_count);
   if(!s.closed_bar_available)
      text += " | " + s.reason;
   return text;
}

string FP_StateGatePanelLineRallyText(const FP_StateGateConfig &cfg,
                                      const int preview_index,
                                      const FP_StateGateRallyRow &r)
{
   string text = "R" + IntegerToString(preview_index+1) + " | " + r.timeframe_label + " | " + FP_DirectionName(r.direction);
   if(r.latest_established_f != FP_STATE_GATE_RALLY_ESTABLISHED_NONE)
      text += " | " + r.latest_established_f;
   else if(r.probable_next_f != FP_STATE_GATE_RALLY_PROBABLE_NONE)
      text += " | " + r.probable_next_f;
   else if(r.flag_stage != "")
      text += " | " + r.flag_stage;
   else if(r.post_flag_stage != "")
      text += " | " + r.post_flag_stage;
   if(cfg.show_scale_l)
      text += " | L" + IntegerToString(r.scale_L);
   if(cfg.show_ids)
      text += " | E#" + IntegerToString(r.source_event_id);
   return text;
}

string FP_StateGatePanelLineHookText(const FP_StateGateConfig &cfg,
                                     const int preview_index,
                                     const FP_StateGateHookRow &h)
{
   string text = "H" + IntegerToString(preview_index+1) + " | " + h.timeframe_label;
   if(h.polarity != "")
      text += " | " + h.polarity;
   else
      text += " | " + FP_DirectionName(h.direction);
   text += " | N" + IntegerToString(h.current_node_number);
   if(cfg.show_scale_l)
      text += " | L" + IntegerToString(h.scale_L);
   if(h.latest_high_node_id >= 0)
      text += " | H#" + IntegerToString(h.latest_high_node_id);
   if(h.latest_low_node_id >= 0)
      text += " | L#" + IntegerToString(h.latest_low_node_id);
   if(cfg.show_ids)
      text += " | Hk#" + IntegerToString(h.source_hook_id);
   return text;
}

bool FP_StateGateExportPanelLinesCsv(const string path,
                                     const FP_StateGateConfig &cfg,
                                     const FP_StateGateSnapshot &snapshot,
                                     FP_StateGateReport &report)
{
   int handle = INVALID_HANDLE;
   if(!FP_StateGateExportOpenWrite(path, handle))
   {
      report.file_errors++;
      report.reason = report.reason + ";state_gate_panel_lines_open_failed";
      return false;
   }

   FP_StateGateExportWriteLine(handle, FP_StateGatePanelLineHeader());

   int line_index = 0;
   string header_text = "State Gate | " + snapshot.symbol + " | dirty=" + IntegerToString(snapshot.dirty_timeframes) + "/" + IntegerToString(snapshot.timeframe_count);
   header_text += " | rally=" + IntegerToString(snapshot.rally_row_count) + " | hook=" + IntegerToString(snapshot.hook_row_count);
   FP_StateGateExportWriteLine(handle, FP_StateGatePanelLineRow(cfg, snapshot, line_index++, -1, "GLOBAL", "HEADER", -1, "SNAPSHOT", "global", header_text, snapshot.generated_at, "", "", ""));

   string diag_text = "diag | " + FP_StateGateEffectiveCornerName(cfg) + "|x=" + IntegerToString(cfg.panel_x) + "|y=" + IntegerToString(cfg.panel_y);
   diag_text += "|w=" + IntegerToString(cfg.panel_width) + "|font=" + IntegerToString(cfg.panel_font_size);
   diag_text += "|serial=" + IntegerToString(snapshot.update_serial);
   FP_StateGateExportWriteLine(handle, FP_StateGatePanelLineRow(cfg, snapshot, line_index++, -1, "GLOBAL", "DIAGNOSTICS", -1, "SNAPSHOT", "diagnostics", diag_text, snapshot.generated_at, "", "", ""));

   for(int slot=0; slot<snapshot.timeframe_count; slot++)
   {
      FP_StateGateTimeframeState s = snapshot.tf_states[slot];

      string slot_header = "[" + s.timeframe_label + "] " + FP_StateGateDirtyLabel(s);
      slot_header += " | R=" + IntegerToString(s.rally_row_count);
      slot_header += " H=" + IntegerToString(s.hook_row_count);
      if(s.latest_established_f_summary != "")
         slot_header += " | " + s.latest_established_f_summary;
      FP_StateGateExportWriteLine(handle, FP_StateGatePanelLineRow(cfg, snapshot, line_index++, slot, "TF", "SLOT_HEADER", -1, "TF_STATE", s.timeframe_label, slot_header, s.last_closed_bar_time, s.state_key, s.contract_status, s.entry_bridge_status));

      FP_StateGateExportWriteLine(handle, FP_StateGatePanelLineRow(cfg, snapshot, line_index++, slot, "TRACKER", "TRACKER", -1, "TF_STATE", s.timeframe_label, FP_StateGatePanelLineTrackerText(cfg, s), s.last_closed_bar_time, s.state_key, s.contract_status, s.entry_bridge_status));

      if(cfg.panel_show_row_counts)
      {
         string counts = "counts | rally=" + IntegerToString(s.rally_row_count) + " | hook=" + IntegerToString(s.hook_row_count) + " | status=" + s.tracker_status;
         FP_StateGateExportWriteLine(handle, FP_StateGatePanelLineRow(cfg, snapshot, line_index++, slot, "COUNTS", "ROW_COUNTS", -1, "TF_STATE", s.timeframe_label, counts, s.last_closed_bar_time, s.state_key, s.contract_status, s.entry_bridge_status));
      }

      if(cfg.panel_show_contract_key)
      {
         string contract = "contract | " + s.contract_status + " | " + s.entry_bridge_status + " | key=" + s.state_key;
         FP_StateGateExportWriteLine(handle, FP_StateGatePanelLineRow(cfg, snapshot, line_index++, slot, "CONTRACT", "STATE_KEY", -1, "TF_STATE", s.timeframe_label, contract, s.last_closed_bar_time, s.state_key, s.contract_status, s.entry_bridge_status));
      }

      string xmap = "xmap | rows=" + IntegerToString(s.extreme_candidate_row_count) + " | " + s.extreme_map_status + " | primary=" + s.primary_extreme_source + "|" + s.primary_extreme_side + "|" + s.primary_extreme_price_status;
      FP_StateGateExportWriteLine(handle, FP_StateGatePanelLineRow(cfg, snapshot, line_index++, slot, "EXTREME_MAP", "EXTREME_MAP", -1, "EXTREME_CANDIDATE", s.extreme_map_key, xmap, s.last_closed_bar_time, s.state_key, s.contract_status, s.entry_bridge_status));

      string mtf = "mtf | rows=" + IntegerToString(s.mtf_alignment_row_count) + " | " + s.mtf_alignment_status + " | parent=" + s.mtf_parent_timeframe + " | " + s.mtf_direction_relation + " | " + s.mtf_side_relation + " | " + s.mtf_context_role;
      FP_StateGateExportWriteLine(handle, FP_StateGatePanelLineRow(cfg, snapshot, line_index++, slot, "MTF_ALIGNMENT", "MTF_ALIGNMENT", -1, "MTF_ALIGNMENT", s.mtf_alignment_key, mtf, s.last_closed_bar_time, s.state_key, s.contract_status, s.entry_bridge_status));

      string geom = "geometry | " + s.geometry_readiness + " | entry=" + s.candidate_entry_price_status + " | invalidation=" + s.candidate_invalidation_price_status + " | destination=" + s.candidate_destination_price_status + " | potentialR=" + s.potential_R_status;
      FP_StateGateExportWriteLine(handle, FP_StateGatePanelLineRow(cfg, snapshot, line_index++, slot, "ENTRY_GEOMETRY", "ENTRY_GEOMETRY", -1, "ENTRY_GEOMETRY", s.geometry_key, geom, s.last_closed_bar_time, s.state_key, s.contract_status, s.entry_bridge_status));

      string idea = "idea | rows=" + IntegerToString(s.entry_idea_row_count) + " | " + s.entry_idea_status + " | " + s.primary_entry_idea_family + " | " + s.entry_idea_readiness + " | " + s.primary_entry_idea_mtf_context;
      FP_StateGateExportWriteLine(handle, FP_StateGatePanelLineRow(cfg, snapshot, line_index++, slot, "ENTRY_IDEA", "ENTRY_IDEA", -1, "ENTRY_IDEA", s.entry_idea_key, idea, s.last_closed_bar_time, s.state_key, s.contract_status, s.entry_bridge_status));

      string decision = "decision | rows=" + IntegerToString(s.entry_decision_row_count) + " | " + s.entry_decision_status + " | " + s.entry_decision_direction + " | " + s.entry_decision_type + " | allowed=" + FP_ExportBool(s.entry_decision_allowed) + " | " + s.entry_decision_execution_status;
      FP_StateGateExportWriteLine(handle, FP_StateGatePanelLineRow(cfg, snapshot, line_index++, slot, "ENTRY_DECISION", "ENTRY_DECISION", -1, "ENTRY_DECISION", s.entry_decision_key, decision, s.last_closed_bar_time, s.state_key, s.contract_status, s.entry_bridge_status));

      string paper = "paper | rows=" + IntegerToString(s.paper_ledger_row_count) + " | " + s.paper_ledger_record_status + " | " + s.paper_ledger_direction + " | " + s.paper_ledger_lifecycle_status + " | " + s.paper_ledger_execution_status;
      FP_StateGateExportWriteLine(handle, FP_StateGatePanelLineRow(cfg, snapshot, line_index++, slot, "PAPER_LEDGER", "PAPER_LEDGER", -1, "PAPER_LEDGER", s.paper_ledger_key, paper, s.last_closed_bar_time, s.state_key, s.contract_status, s.entry_bridge_status));

      string lifecycle = "lifecycle | rows=" + IntegerToString(s.paper_lifecycle_row_count) + " | " + s.paper_lifecycle_path_state + " | " + s.paper_lifecycle_outcome + " | " + s.paper_lifecycle_execution_status;
      FP_StateGateExportWriteLine(handle, FP_StateGatePanelLineRow(cfg, snapshot, line_index++, slot, "PAPER_LIFECYCLE", "PAPER_LIFECYCLE", -1, "PAPER_LIFECYCLE", s.paper_lifecycle_key, lifecycle, s.last_closed_bar_time, s.state_key, s.contract_status, s.entry_bridge_status));

      string result = "result | rows=" + IntegerToString(s.paper_result_row_count) + " | " + s.paper_result_status + " | " + s.paper_result_bucket + " | delta=" + FP_ExportDouble(s.paper_result_price_delta) + " | " + s.paper_result_r_status;
      FP_StateGateExportWriteLine(handle, FP_StateGatePanelLineRow(cfg, snapshot, line_index++, slot, "PAPER_RESULT", "PAPER_RESULT", -1, "PAPER_RESULT", s.paper_result_key, result, s.last_closed_bar_time, s.state_key, s.contract_status, s.entry_bridge_status));

      string rally_header = "Rally | total=" + IntegerToString(s.rally_row_count) + " | latest=" + s.latest_established_f_summary + " | probable=" + s.probable_next_f_summary;
      FP_StateGateExportWriteLine(handle, FP_StateGatePanelLineRow(cfg, snapshot, line_index++, slot, "RALLY", "SECTION_HEADER", -1, "TF_STATE", s.timeframe_label, rally_header, s.last_closed_bar_time, s.state_key, s.contract_status, s.entry_bridge_status));

      int rlimit = FP_StateGateClampInt(cfg.panel_rally_preview_rows_per_tf, 0, 8);
      int rally_seen = 0;
      int rally_total = 0;
      for(int r=0; r<snapshot.rally_row_count; r++)
      {
         if(snapshot.rally_rows[r].slot_index != slot)
            continue;
         rally_total++;
         if(rally_seen >= rlimit)
            continue;
         FP_StateGateRallyRow rr = snapshot.rally_rows[r];
         string rid = "event=" + IntegerToString(rr.source_event_id) + "|seq=" + IntegerToString(rr.sequence_id);
         FP_StateGateExportWriteLine(handle, FP_StateGatePanelLineRow(cfg, snapshot, line_index++, slot, "RALLY", "PREVIEW_ROW", rally_seen, "RALLY_ROW", rid, FP_StateGatePanelLineRallyText(cfg, rally_seen, rr), rr.last_closed_bar_time, s.state_key, s.contract_status, s.entry_bridge_status));
         rally_seen++;
      }
      if(rally_total > rlimit && rlimit > 0)
      {
         string more = "R+ | " + IntegerToString(rally_total - rlimit) + " more Rally rows in latest_state_gate_rally.csv";
         FP_StateGateExportWriteLine(handle, FP_StateGatePanelLineRow(cfg, snapshot, line_index++, slot, "RALLY", "MORE_ROWS", -1, "RALLY_ROW", "more", more, s.last_closed_bar_time, s.state_key, s.contract_status, s.entry_bridge_status));
      }

      string hook_header = "Hook | total=" + IntegerToString(s.hook_row_count) + " | summary=" + s.hook_summary;
      FP_StateGateExportWriteLine(handle, FP_StateGatePanelLineRow(cfg, snapshot, line_index++, slot, "HOOK", "SECTION_HEADER", -1, "TF_STATE", s.timeframe_label, hook_header, s.last_closed_bar_time, s.state_key, s.contract_status, s.entry_bridge_status));

      int hlimit = FP_StateGateClampInt(cfg.panel_hook_preview_rows_per_tf, 0, 12);
      int hook_seen = 0;
      int hook_total = 0;
      for(int hi=0; hi<snapshot.hook_row_count; hi++)
      {
         if(snapshot.hook_rows[hi].slot_index != slot)
            continue;
         hook_total++;
         if(hook_seen >= hlimit)
            continue;
         FP_StateGateHookRow hh = snapshot.hook_rows[hi];
         string hid = "hook=" + IntegerToString(hh.source_hook_id) + "|seq=" + IntegerToString(hh.sequence_id);
         FP_StateGateExportWriteLine(handle, FP_StateGatePanelLineRow(cfg, snapshot, line_index++, slot, "HOOK", "PREVIEW_ROW", hook_seen, "HOOK_ROW", hid, FP_StateGatePanelLineHookText(cfg, hook_seen, hh), hh.last_closed_bar_time, s.state_key, s.contract_status, s.entry_bridge_status));
         hook_seen++;
      }
      if(hook_total > hlimit && hlimit > 0)
      {
         string more_h = "H+ | " + IntegerToString(hook_total - hlimit) + " more Hook rows in latest_state_gate_hooks.csv";
         FP_StateGateExportWriteLine(handle, FP_StateGatePanelLineRow(cfg, snapshot, line_index++, slot, "HOOK", "MORE_ROWS", -1, "HOOK_ROW", "more", more_h, s.last_closed_bar_time, s.state_key, s.contract_status, s.entry_bridge_status));
      }
   }

   FileClose(handle);
   report.files_written++;
   return true;
}


string FP_StateGateContractHeader()
{
   string h = "";
   FP_ExportCsvAppend(h, "symbol");
   FP_ExportCsvAppend(h, "chart_timeframe");
   FP_ExportCsvAppend(h, "slot");
   FP_ExportCsvAppend(h, "timeframe");
   FP_ExportCsvAppend(h, "closed_bar_time");
   FP_ExportCsvAppend(h, "closed_bar_close");
   FP_ExportCsvAppend(h, "dirty");
   FP_ExportCsvAppend(h, "update_count");
   FP_ExportCsvAppend(h, "state_key");
   FP_ExportCsvAppend(h, "contract_status");
   FP_ExportCsvAppend(h, "anatomy_status");
   FP_ExportCsvAppend(h, "storage_status");
   FP_ExportCsvAppend(h, "entry_bridge_status");
   FP_ExportCsvAppend(h, "entry_bridge_readiness");
   FP_ExportCsvAppend(h, "entry_bridge_key");
   FP_ExportCsvAppend(h, "candidate_extreme_status");
   FP_ExportCsvAppend(h, "candidate_extreme_key");
   FP_ExportCsvAppend(h, "candidate_extreme_source");
   FP_ExportCsvAppend(h, "candidate_direction");
   FP_ExportCsvAppend(h, "candidate_scale_context");
   FP_ExportCsvAppend(h, "x_invalidation_status");
   FP_ExportCsvAppend(h, "x_invalidation_key");
   FP_ExportCsvAppend(h, "x_destination_status");
   FP_ExportCsvAppend(h, "x_destination_key");
   FP_ExportCsvAppend(h, "optionality_status");
   FP_ExportCsvAppend(h, "optionality_key");
   FP_ExportCsvAppend(h, "extreme_candidate_rows");
   FP_ExportCsvAppend(h, "extreme_map_status");
   FP_ExportCsvAppend(h, "extreme_map_key");
   FP_ExportCsvAppend(h, "primary_extreme_source");
   FP_ExportCsvAppend(h, "primary_extreme_direction");
   FP_ExportCsvAppend(h, "primary_extreme_side");
   FP_ExportCsvAppend(h, "primary_extreme_role");
   FP_ExportCsvAppend(h, "primary_extreme_price_status");
   FP_ExportCsvAppend(h, "primary_extreme_price");
   FP_ExportCsvAppend(h, "primary_extreme_node_id");
   FP_ExportCsvAppend(h, "primary_extreme_scale_L");
   FP_ExportCsvAppend(h, "extreme_map_notes");
   FP_ExportCsvAppend(h, "mtf_alignment_rows");
   FP_ExportCsvAppend(h, "mtf_alignment_status");
   FP_ExportCsvAppend(h, "mtf_alignment_key");
   FP_ExportCsvAppend(h, "mtf_parent_timeframe");
   FP_ExportCsvAppend(h, "mtf_parent_extreme_key");
   FP_ExportCsvAppend(h, "mtf_parent_direction");
   FP_ExportCsvAppend(h, "mtf_parent_side");
   FP_ExportCsvAppend(h, "mtf_direction_relation");
   FP_ExportCsvAppend(h, "mtf_side_relation");
   FP_ExportCsvAppend(h, "mtf_context_role");
   FP_ExportCsvAppend(h, "mtf_alignment_notes");
   FP_ExportCsvAppend(h, "candidate_entry_price_status");
   FP_ExportCsvAppend(h, "candidate_entry_price");
   FP_ExportCsvAppend(h, "candidate_invalidation_price_status");
   FP_ExportCsvAppend(h, "candidate_invalidation_price");
   FP_ExportCsvAppend(h, "candidate_destination_price_status");
   FP_ExportCsvAppend(h, "candidate_destination_price");
   FP_ExportCsvAppend(h, "risk_distance_status");
   FP_ExportCsvAppend(h, "risk_distance");
   FP_ExportCsvAppend(h, "destination_distance_status");
   FP_ExportCsvAppend(h, "destination_distance");
   FP_ExportCsvAppend(h, "potential_R_status");
   FP_ExportCsvAppend(h, "potential_R");
   FP_ExportCsvAppend(h, "geometry_readiness");
   FP_ExportCsvAppend(h, "geometry_key");
   FP_ExportCsvAppend(h, "geometry_notes");
   FP_ExportCsvAppend(h, "primary_rally_key");
   FP_ExportCsvAppend(h, "primary_hook_key");
   FP_ExportCsvAppend(h, "latest_established_f_summary");
   FP_ExportCsvAppend(h, "probable_next_f_summary");
   FP_ExportCsvAppend(h, "hook_summary");
   FP_ExportCsvAppend(h, "rally_rows");
   FP_ExportCsvAppend(h, "hook_rows");
   FP_ExportCsvAppend(h, "tracker_status");
   FP_ExportCsvAppend(h, "reason");
   return h;
}



string FP_StateGateContractRow(const FP_StateGateSnapshot &snapshot, const int slot)
{
   FP_StateGateTimeframeState s = snapshot.tf_states[slot];
   string line = "";
   FP_ExportCsvAppend(line, snapshot.symbol);
   FP_ExportCsvAppend(line, EnumToString(snapshot.chart_timeframe));
   FP_ExportCsvAppend(line, IntegerToString(slot));
   FP_ExportCsvAppend(line, s.timeframe_label);
   FP_ExportCsvAppend(line, FP_ExportTime(s.last_closed_bar_time));
   FP_ExportCsvAppend(line, FP_ExportDouble(s.last_closed_bar_close));
   FP_ExportCsvAppend(line, FP_ExportBool(s.dirty));
   FP_ExportCsvAppend(line, IntegerToString(s.update_count));
   FP_ExportCsvAppend(line, s.state_key);
   FP_ExportCsvAppend(line, s.contract_status);
   FP_ExportCsvAppend(line, s.anatomy_status);
   FP_ExportCsvAppend(line, s.storage_status);
   FP_ExportCsvAppend(line, s.entry_bridge_status);
   FP_ExportCsvAppend(line, s.entry_bridge_readiness);
   FP_ExportCsvAppend(line, s.entry_bridge_key);
   FP_ExportCsvAppend(line, s.candidate_extreme_status);
   FP_ExportCsvAppend(line, s.candidate_extreme_key);
   FP_ExportCsvAppend(line, s.candidate_extreme_source);
   FP_ExportCsvAppend(line, s.candidate_direction);
   FP_ExportCsvAppend(line, s.candidate_scale_context);
   FP_ExportCsvAppend(line, s.x_invalidation_status);
   FP_ExportCsvAppend(line, s.x_invalidation_key);
   FP_ExportCsvAppend(line, s.x_destination_status);
   FP_ExportCsvAppend(line, s.x_destination_key);
   FP_ExportCsvAppend(line, s.optionality_status);
   FP_ExportCsvAppend(line, s.optionality_key);
   FP_ExportCsvAppend(line, IntegerToString(s.extreme_candidate_row_count));
   FP_ExportCsvAppend(line, s.extreme_map_status);
   FP_ExportCsvAppend(line, s.extreme_map_key);
   FP_ExportCsvAppend(line, s.primary_extreme_source);
   FP_ExportCsvAppend(line, s.primary_extreme_direction);
   FP_ExportCsvAppend(line, s.primary_extreme_side);
   FP_ExportCsvAppend(line, s.primary_extreme_role);
   FP_ExportCsvAppend(line, s.primary_extreme_price_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(s.primary_extreme_price));
   FP_ExportCsvAppend(line, IntegerToString(s.primary_extreme_node_id));
   FP_ExportCsvAppend(line, IntegerToString(s.primary_extreme_scale_L));
   FP_ExportCsvAppend(line, s.extreme_map_notes);
   FP_ExportCsvAppend(line, IntegerToString(s.mtf_alignment_row_count));
   FP_ExportCsvAppend(line, s.mtf_alignment_status);
   FP_ExportCsvAppend(line, s.mtf_alignment_key);
   FP_ExportCsvAppend(line, s.mtf_parent_timeframe);
   FP_ExportCsvAppend(line, s.mtf_parent_extreme_key);
   FP_ExportCsvAppend(line, s.mtf_parent_direction);
   FP_ExportCsvAppend(line, s.mtf_parent_side);
   FP_ExportCsvAppend(line, s.mtf_direction_relation);
   FP_ExportCsvAppend(line, s.mtf_side_relation);
   FP_ExportCsvAppend(line, s.mtf_context_role);
   FP_ExportCsvAppend(line, s.mtf_alignment_notes);
   FP_ExportCsvAppend(line, s.candidate_entry_price_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(s.candidate_entry_price));
   FP_ExportCsvAppend(line, s.candidate_invalidation_price_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(s.candidate_invalidation_price));
   FP_ExportCsvAppend(line, s.candidate_destination_price_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(s.candidate_destination_price));
   FP_ExportCsvAppend(line, s.risk_distance_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(s.risk_distance));
   FP_ExportCsvAppend(line, s.destination_distance_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(s.destination_distance));
   FP_ExportCsvAppend(line, s.potential_R_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(s.potential_R));
   FP_ExportCsvAppend(line, s.geometry_readiness);
   FP_ExportCsvAppend(line, s.geometry_key);
   FP_ExportCsvAppend(line, s.geometry_notes);
   FP_ExportCsvAppend(line, s.primary_rally_key);
   FP_ExportCsvAppend(line, s.primary_hook_key);
   FP_ExportCsvAppend(line, s.latest_established_f_summary);
   FP_ExportCsvAppend(line, s.probable_next_f_summary);
   FP_ExportCsvAppend(line, s.hook_summary);
   FP_ExportCsvAppend(line, IntegerToString(s.rally_row_count));
   FP_ExportCsvAppend(line, IntegerToString(s.hook_row_count));
   FP_ExportCsvAppend(line, s.tracker_status);
   FP_ExportCsvAppend(line, s.reason);
   return line;
}



bool FP_StateGateExportContractCsv(const string path,
                                   const FP_StateGateSnapshot &snapshot,
                                   FP_StateGateReport &report)
{
   int handle = INVALID_HANDLE;
   if(!FP_StateGateExportOpenWrite(path, handle))
   {
      report.file_errors++;
      report.reason = report.reason + ";state_gate_contract_open_failed";
      return false;
   }
   FP_StateGateExportWriteLine(handle, FP_StateGateContractHeader());
   for(int i=0; i<snapshot.timeframe_count; i++)
      FP_StateGateExportWriteLine(handle, FP_StateGateContractRow(snapshot, i));
   FileClose(handle);
   report.files_written++;
   report.contract_rows = snapshot.timeframe_count;
   return true;
}




string FP_StateGateMtfAlignmentHeader()
{
   string h = "";
   FP_ExportCsvAppend(h, "symbol");
   FP_ExportCsvAppend(h, "chart_timeframe");
   FP_ExportCsvAppend(h, "child_slot");
   FP_ExportCsvAppend(h, "parent_slot");
   FP_ExportCsvAppend(h, "child_timeframe");
   FP_ExportCsvAppend(h, "parent_timeframe");
   FP_ExportCsvAppend(h, "child_closed_bar_time");
   FP_ExportCsvAppend(h, "parent_closed_bar_time");
   FP_ExportCsvAppend(h, "status");
   FP_ExportCsvAppend(h, "readiness");
   FP_ExportCsvAppend(h, "child_extreme_key");
   FP_ExportCsvAppend(h, "parent_extreme_key");
   FP_ExportCsvAppend(h, "child_source");
   FP_ExportCsvAppend(h, "parent_source");
   FP_ExportCsvAppend(h, "child_direction");
   FP_ExportCsvAppend(h, "parent_direction");
   FP_ExportCsvAppend(h, "child_side");
   FP_ExportCsvAppend(h, "parent_side");
   FP_ExportCsvAppend(h, "direction_relation");
   FP_ExportCsvAppend(h, "side_relation");
   FP_ExportCsvAppend(h, "context_role");
   FP_ExportCsvAppend(h, "child_node_id");
   FP_ExportCsvAppend(h, "parent_node_id");
   FP_ExportCsvAppend(h, "child_price");
   FP_ExportCsvAppend(h, "parent_price");
   FP_ExportCsvAppend(h, "child_price_status");
   FP_ExportCsvAppend(h, "parent_price_status");
   FP_ExportCsvAppend(h, "alignment_key");
   FP_ExportCsvAppend(h, "label");
   return h;
}

string FP_StateGateMtfAlignmentRowCsv(const FP_StateGateSnapshot &snapshot,
                                      const int index)
{
   FP_StateGateMtfAlignmentRow m = snapshot.mtf_alignment_rows[index];
   string line = "";
   FP_ExportCsvAppend(line, snapshot.symbol);
   FP_ExportCsvAppend(line, EnumToString(snapshot.chart_timeframe));
   FP_ExportCsvAppend(line, IntegerToString(m.child_slot));
   FP_ExportCsvAppend(line, IntegerToString(m.parent_slot));
   FP_ExportCsvAppend(line, m.child_timeframe_label);
   FP_ExportCsvAppend(line, m.parent_timeframe_label);
   FP_ExportCsvAppend(line, FP_ExportTime(m.child_closed_bar_time));
   FP_ExportCsvAppend(line, FP_ExportTime(m.parent_closed_bar_time));
   FP_ExportCsvAppend(line, IntegerToString(m.status));
   FP_ExportCsvAppend(line, m.readiness);
   FP_ExportCsvAppend(line, m.child_extreme_key);
   FP_ExportCsvAppend(line, m.parent_extreme_key);
   FP_ExportCsvAppend(line, m.child_source);
   FP_ExportCsvAppend(line, m.parent_source);
   FP_ExportCsvAppend(line, m.child_direction);
   FP_ExportCsvAppend(line, m.parent_direction);
   FP_ExportCsvAppend(line, m.child_side);
   FP_ExportCsvAppend(line, m.parent_side);
   FP_ExportCsvAppend(line, m.direction_relation);
   FP_ExportCsvAppend(line, m.side_relation);
   FP_ExportCsvAppend(line, m.context_role);
   FP_ExportCsvAppend(line, IntegerToString(m.child_node_id));
   FP_ExportCsvAppend(line, IntegerToString(m.parent_node_id));
   FP_ExportCsvAppend(line, FP_ExportDouble(m.child_price));
   FP_ExportCsvAppend(line, FP_ExportDouble(m.parent_price));
   FP_ExportCsvAppend(line, m.child_price_status);
   FP_ExportCsvAppend(line, m.parent_price_status);
   FP_ExportCsvAppend(line, m.alignment_key);
   FP_ExportCsvAppend(line, m.label);
   return line;
}

bool FP_StateGateExportMtfAlignmentCsv(const string path,
                                       const FP_StateGateSnapshot &snapshot,
                                       FP_StateGateReport &report)
{
   int handle = INVALID_HANDLE;
   if(!FP_StateGateExportOpenWrite(path, handle))
   {
      report.file_errors++;
      report.reason = report.reason + ";state_gate_mtf_alignment_open_failed";
      return false;
   }
   FP_StateGateExportWriteLine(handle, FP_StateGateMtfAlignmentHeader());
   for(int i=0; i<snapshot.mtf_alignment_row_count; i++)
      FP_StateGateExportWriteLine(handle, FP_StateGateMtfAlignmentRowCsv(snapshot, i));
   FileClose(handle);
   report.files_written++;
   return true;
}


string FP_StateGateExtremeCandidateHeader()
{
   string h = "";
   FP_ExportCsvAppend(h, "symbol");
   FP_ExportCsvAppend(h, "chart_timeframe");
   FP_ExportCsvAppend(h, "slot");
   FP_ExportCsvAppend(h, "timeframe");
   FP_ExportCsvAppend(h, "closed_bar_time");
   FP_ExportCsvAppend(h, "closed_bar_close");
   FP_ExportCsvAppend(h, "rank");
   FP_ExportCsvAppend(h, "status");
   FP_ExportCsvAppend(h, "readiness");
   FP_ExportCsvAppend(h, "source_kind");
   FP_ExportCsvAppend(h, "source_id");
   FP_ExportCsvAppend(h, "source_row_index");
   FP_ExportCsvAppend(h, "direction");
   FP_ExportCsvAppend(h, "side");
   FP_ExportCsvAppend(h, "role");
   FP_ExportCsvAppend(h, "scale_L");
   FP_ExportCsvAppend(h, "node_id");
   FP_ExportCsvAppend(h, "price");
   FP_ExportCsvAppend(h, "price_status");
   FP_ExportCsvAppend(h, "source_key");
   FP_ExportCsvAppend(h, "label");
   FP_ExportCsvAppend(h, "state_key");
   FP_ExportCsvAppend(h, "extreme_map_status");
   FP_ExportCsvAppend(h, "extreme_map_key");
   FP_ExportCsvAppend(h, "entry_bridge_status");
   FP_ExportCsvAppend(h, "entry_bridge_readiness");
   FP_ExportCsvAppend(h, "entry_bridge_key");
   return h;
}

string FP_StateGateExtremeCandidateRowCsv(const FP_StateGateSnapshot &snapshot,
                                          const int index)
{
   FP_StateGateExtremeCandidateRow x = snapshot.extreme_candidate_rows[index];
   string line = "";
   FP_ExportCsvAppend(line, snapshot.symbol);
   FP_ExportCsvAppend(line, EnumToString(snapshot.chart_timeframe));
   FP_ExportCsvAppend(line, IntegerToString(x.slot_index));
   FP_ExportCsvAppend(line, x.timeframe_label);
   FP_ExportCsvAppend(line, FP_ExportTime(x.last_closed_bar_time));
   FP_ExportCsvAppend(line, FP_ExportDouble(x.last_closed_bar_close));
   FP_ExportCsvAppend(line, IntegerToString(x.rank));
   FP_ExportCsvAppend(line, IntegerToString(x.status));
   FP_ExportCsvAppend(line, x.readiness);
   FP_ExportCsvAppend(line, x.source_kind);
   FP_ExportCsvAppend(line, x.source_id);
   FP_ExportCsvAppend(line, IntegerToString(x.source_row_index));
   FP_ExportCsvAppend(line, x.direction_label);
   FP_ExportCsvAppend(line, x.side);
   FP_ExportCsvAppend(line, x.role);
   FP_ExportCsvAppend(line, IntegerToString(x.scale_L));
   FP_ExportCsvAppend(line, IntegerToString(x.node_id));
   FP_ExportCsvAppend(line, FP_ExportDouble(x.price));
   FP_ExportCsvAppend(line, x.price_status);
   FP_ExportCsvAppend(line, x.source_key);
   FP_ExportCsvAppend(line, x.label);

   if(x.slot_index >= 0 && x.slot_index < snapshot.timeframe_count)
   {
      FP_StateGateTimeframeState s = snapshot.tf_states[x.slot_index];
      FP_ExportCsvAppend(line, s.state_key);
      FP_ExportCsvAppend(line, s.extreme_map_status);
      FP_ExportCsvAppend(line, s.extreme_map_key);
      FP_ExportCsvAppend(line, s.entry_bridge_status);
      FP_ExportCsvAppend(line, s.entry_bridge_readiness);
      FP_ExportCsvAppend(line, s.entry_bridge_key);
   }
   else
   {
      FP_ExportCsvAppend(line, "");
      FP_ExportCsvAppend(line, "");
      FP_ExportCsvAppend(line, "");
      FP_ExportCsvAppend(line, "");
      FP_ExportCsvAppend(line, "");
      FP_ExportCsvAppend(line, "");
   }

   return line;
}

bool FP_StateGateExportExtremeCandidatesCsv(const string path,
                                            const FP_StateGateSnapshot &snapshot,
                                            FP_StateGateReport &report)
{
   int handle = INVALID_HANDLE;
   if(!FP_StateGateExportOpenWrite(path, handle))
   {
      report.file_errors++;
      report.reason = report.reason + ";state_gate_extreme_candidates_open_failed";
      return false;
   }
   FP_StateGateExportWriteLine(handle, FP_StateGateExtremeCandidateHeader());
   for(int i=0; i<snapshot.extreme_candidate_row_count; i++)
      FP_StateGateExportWriteLine(handle, FP_StateGateExtremeCandidateRowCsv(snapshot, i));
   FileClose(handle);
   report.files_written++;
   return true;
}


string FP_StateGateEntryBridgeHeader()
{
   string h = "";
   FP_ExportCsvAppend(h, "symbol");
   FP_ExportCsvAppend(h, "chart_timeframe");
   FP_ExportCsvAppend(h, "slot");
   FP_ExportCsvAppend(h, "timeframe");
   FP_ExportCsvAppend(h, "closed_bar_time");
   FP_ExportCsvAppend(h, "closed_bar_close");
   FP_ExportCsvAppend(h, "entry_bridge_status");
   FP_ExportCsvAppend(h, "entry_bridge_readiness");
   FP_ExportCsvAppend(h, "entry_bridge_key");
   FP_ExportCsvAppend(h, "candidate_extreme_status");
   FP_ExportCsvAppend(h, "candidate_extreme_key");
   FP_ExportCsvAppend(h, "candidate_extreme_source");
   FP_ExportCsvAppend(h, "candidate_direction");
   FP_ExportCsvAppend(h, "candidate_scale_context");
   FP_ExportCsvAppend(h, "x_invalidation_status");
   FP_ExportCsvAppend(h, "x_invalidation_key");
   FP_ExportCsvAppend(h, "x_destination_status");
   FP_ExportCsvAppend(h, "x_destination_key");
   FP_ExportCsvAppend(h, "optionality_status");
   FP_ExportCsvAppend(h, "optionality_key");
   FP_ExportCsvAppend(h, "extreme_candidate_rows");
   FP_ExportCsvAppend(h, "extreme_map_status");
   FP_ExportCsvAppend(h, "extreme_map_key");
   FP_ExportCsvAppend(h, "primary_extreme_source");
   FP_ExportCsvAppend(h, "primary_extreme_direction");
   FP_ExportCsvAppend(h, "primary_extreme_side");
   FP_ExportCsvAppend(h, "primary_extreme_role");
   FP_ExportCsvAppend(h, "primary_extreme_price_status");
   FP_ExportCsvAppend(h, "primary_extreme_price");
   FP_ExportCsvAppend(h, "primary_extreme_node_id");
   FP_ExportCsvAppend(h, "primary_extreme_scale_L");
   FP_ExportCsvAppend(h, "mtf_alignment_rows");
   FP_ExportCsvAppend(h, "mtf_alignment_status");
   FP_ExportCsvAppend(h, "mtf_alignment_key");
   FP_ExportCsvAppend(h, "mtf_parent_timeframe");
   FP_ExportCsvAppend(h, "mtf_direction_relation");
   FP_ExportCsvAppend(h, "mtf_side_relation");
   FP_ExportCsvAppend(h, "mtf_context_role");
   FP_ExportCsvAppend(h, "candidate_entry_price_status");
   FP_ExportCsvAppend(h, "candidate_entry_price");
   FP_ExportCsvAppend(h, "candidate_invalidation_price_status");
   FP_ExportCsvAppend(h, "candidate_invalidation_price");
   FP_ExportCsvAppend(h, "candidate_destination_price_status");
   FP_ExportCsvAppend(h, "candidate_destination_price");
   FP_ExportCsvAppend(h, "risk_distance_status");
   FP_ExportCsvAppend(h, "risk_distance");
   FP_ExportCsvAppend(h, "destination_distance_status");
   FP_ExportCsvAppend(h, "destination_distance");
   FP_ExportCsvAppend(h, "potential_R_status");
   FP_ExportCsvAppend(h, "potential_R");
   FP_ExportCsvAppend(h, "geometry_readiness");
   FP_ExportCsvAppend(h, "geometry_key");
   FP_ExportCsvAppend(h, "geometry_notes");
   FP_ExportCsvAppend(h, "primary_rally_key");
   FP_ExportCsvAppend(h, "primary_hook_key");
   FP_ExportCsvAppend(h, "state_key");
   FP_ExportCsvAppend(h, "contract_status");
   return h;
}



string FP_StateGateEntryBridgeRow(const FP_StateGateSnapshot &snapshot, const int slot)
{
   FP_StateGateTimeframeState s = snapshot.tf_states[slot];
   string line = "";
   FP_ExportCsvAppend(line, snapshot.symbol);
   FP_ExportCsvAppend(line, EnumToString(snapshot.chart_timeframe));
   FP_ExportCsvAppend(line, IntegerToString(slot));
   FP_ExportCsvAppend(line, s.timeframe_label);
   FP_ExportCsvAppend(line, FP_ExportTime(s.last_closed_bar_time));
   FP_ExportCsvAppend(line, FP_ExportDouble(s.last_closed_bar_close));
   FP_ExportCsvAppend(line, s.entry_bridge_status);
   FP_ExportCsvAppend(line, s.entry_bridge_readiness);
   FP_ExportCsvAppend(line, s.entry_bridge_key);
   FP_ExportCsvAppend(line, s.candidate_extreme_status);
   FP_ExportCsvAppend(line, s.candidate_extreme_key);
   FP_ExportCsvAppend(line, s.candidate_extreme_source);
   FP_ExportCsvAppend(line, s.candidate_direction);
   FP_ExportCsvAppend(line, s.candidate_scale_context);
   FP_ExportCsvAppend(line, s.x_invalidation_status);
   FP_ExportCsvAppend(line, s.x_invalidation_key);
   FP_ExportCsvAppend(line, s.x_destination_status);
   FP_ExportCsvAppend(line, s.x_destination_key);
   FP_ExportCsvAppend(line, s.optionality_status);
   FP_ExportCsvAppend(line, s.optionality_key);
   FP_ExportCsvAppend(line, IntegerToString(s.extreme_candidate_row_count));
   FP_ExportCsvAppend(line, s.extreme_map_status);
   FP_ExportCsvAppend(line, s.extreme_map_key);
   FP_ExportCsvAppend(line, s.primary_extreme_source);
   FP_ExportCsvAppend(line, s.primary_extreme_direction);
   FP_ExportCsvAppend(line, s.primary_extreme_side);
   FP_ExportCsvAppend(line, s.primary_extreme_role);
   FP_ExportCsvAppend(line, s.primary_extreme_price_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(s.primary_extreme_price));
   FP_ExportCsvAppend(line, IntegerToString(s.primary_extreme_node_id));
   FP_ExportCsvAppend(line, IntegerToString(s.primary_extreme_scale_L));
   FP_ExportCsvAppend(line, IntegerToString(s.mtf_alignment_row_count));
   FP_ExportCsvAppend(line, s.mtf_alignment_status);
   FP_ExportCsvAppend(line, s.mtf_alignment_key);
   FP_ExportCsvAppend(line, s.mtf_parent_timeframe);
   FP_ExportCsvAppend(line, s.mtf_direction_relation);
   FP_ExportCsvAppend(line, s.mtf_side_relation);
   FP_ExportCsvAppend(line, s.mtf_context_role);
   FP_ExportCsvAppend(line, s.candidate_entry_price_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(s.candidate_entry_price));
   FP_ExportCsvAppend(line, s.candidate_invalidation_price_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(s.candidate_invalidation_price));
   FP_ExportCsvAppend(line, s.candidate_destination_price_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(s.candidate_destination_price));
   FP_ExportCsvAppend(line, s.risk_distance_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(s.risk_distance));
   FP_ExportCsvAppend(line, s.destination_distance_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(s.destination_distance));
   FP_ExportCsvAppend(line, s.potential_R_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(s.potential_R));
   FP_ExportCsvAppend(line, s.geometry_readiness);
   FP_ExportCsvAppend(line, s.geometry_key);
   FP_ExportCsvAppend(line, s.geometry_notes);
   FP_ExportCsvAppend(line, s.primary_rally_key);
   FP_ExportCsvAppend(line, s.primary_hook_key);
   FP_ExportCsvAppend(line, s.state_key);
   FP_ExportCsvAppend(line, s.contract_status);
   return line;
}



bool FP_StateGateExportEntryBridgeCsv(const string path,
                                      const FP_StateGateSnapshot &snapshot,
                                      FP_StateGateReport &report)
{
   int handle = INVALID_HANDLE;
   if(!FP_StateGateExportOpenWrite(path, handle))
   {
      report.file_errors++;
      report.reason = report.reason + ";state_gate_entry_bridge_open_failed";
      return false;
   }
   FP_StateGateExportWriteLine(handle, FP_StateGateEntryBridgeHeader());
   for(int i=0; i<snapshot.timeframe_count; i++)
      FP_StateGateExportWriteLine(handle, FP_StateGateEntryBridgeRow(snapshot, i));
   FileClose(handle);
   report.files_written++;
   return true;
}



string FP_StateGateEntryGeometryHeader()
{
   string h = "";
   FP_ExportCsvAppend(h, "symbol");
   FP_ExportCsvAppend(h, "chart_timeframe");
   FP_ExportCsvAppend(h, "slot");
   FP_ExportCsvAppend(h, "timeframe");
   FP_ExportCsvAppend(h, "closed_bar_time");
   FP_ExportCsvAppend(h, "closed_bar_close");
   FP_ExportCsvAppend(h, "geometry_readiness");
   FP_ExportCsvAppend(h, "geometry_key");
   FP_ExportCsvAppend(h, "candidate_entry_price_status");
   FP_ExportCsvAppend(h, "candidate_entry_price");
   FP_ExportCsvAppend(h, "candidate_invalidation_price_status");
   FP_ExportCsvAppend(h, "candidate_invalidation_price");
   FP_ExportCsvAppend(h, "candidate_destination_price_status");
   FP_ExportCsvAppend(h, "candidate_destination_price");
   FP_ExportCsvAppend(h, "risk_distance_status");
   FP_ExportCsvAppend(h, "risk_distance");
   FP_ExportCsvAppend(h, "destination_distance_status");
   FP_ExportCsvAppend(h, "destination_distance");
   FP_ExportCsvAppend(h, "potential_R_status");
   FP_ExportCsvAppend(h, "potential_R");
   FP_ExportCsvAppend(h, "primary_extreme_source");
   FP_ExportCsvAppend(h, "primary_extreme_side");
   FP_ExportCsvAppend(h, "primary_extreme_price_status");
   FP_ExportCsvAppend(h, "primary_extreme_price");
   FP_ExportCsvAppend(h, "primary_extreme_node_id");
   FP_ExportCsvAppend(h, "primary_extreme_scale_L");
   FP_ExportCsvAppend(h, "extreme_map_status");
   FP_ExportCsvAppend(h, "extreme_map_key");
   FP_ExportCsvAppend(h, "mtf_alignment_status");
   FP_ExportCsvAppend(h, "mtf_alignment_key");
   FP_ExportCsvAppend(h, "mtf_context_role");
   FP_ExportCsvAppend(h, "entry_bridge_status");
   FP_ExportCsvAppend(h, "entry_bridge_readiness");
   FP_ExportCsvAppend(h, "entry_bridge_key");
   FP_ExportCsvAppend(h, "x_invalidation_status");
   FP_ExportCsvAppend(h, "x_invalidation_key");
   FP_ExportCsvAppend(h, "x_destination_status");
   FP_ExportCsvAppend(h, "x_destination_key");
   FP_ExportCsvAppend(h, "optionality_status");
   FP_ExportCsvAppend(h, "optionality_key");
   FP_ExportCsvAppend(h, "geometry_notes");
   return h;
}

string FP_StateGateEntryGeometryRow(const FP_StateGateSnapshot &snapshot, const int slot)
{
   FP_StateGateTimeframeState s = snapshot.tf_states[slot];
   string line = "";
   FP_ExportCsvAppend(line, snapshot.symbol);
   FP_ExportCsvAppend(line, EnumToString(snapshot.chart_timeframe));
   FP_ExportCsvAppend(line, IntegerToString(slot));
   FP_ExportCsvAppend(line, s.timeframe_label);
   FP_ExportCsvAppend(line, FP_ExportTime(s.last_closed_bar_time));
   FP_ExportCsvAppend(line, FP_ExportDouble(s.last_closed_bar_close));
   FP_ExportCsvAppend(line, s.geometry_readiness);
   FP_ExportCsvAppend(line, s.geometry_key);
   FP_ExportCsvAppend(line, s.candidate_entry_price_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(s.candidate_entry_price));
   FP_ExportCsvAppend(line, s.candidate_invalidation_price_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(s.candidate_invalidation_price));
   FP_ExportCsvAppend(line, s.candidate_destination_price_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(s.candidate_destination_price));
   FP_ExportCsvAppend(line, s.risk_distance_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(s.risk_distance));
   FP_ExportCsvAppend(line, s.destination_distance_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(s.destination_distance));
   FP_ExportCsvAppend(line, s.potential_R_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(s.potential_R));
   FP_ExportCsvAppend(line, s.primary_extreme_source);
   FP_ExportCsvAppend(line, s.primary_extreme_side);
   FP_ExportCsvAppend(line, s.primary_extreme_price_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(s.primary_extreme_price));
   FP_ExportCsvAppend(line, IntegerToString(s.primary_extreme_node_id));
   FP_ExportCsvAppend(line, IntegerToString(s.primary_extreme_scale_L));
   FP_ExportCsvAppend(line, s.extreme_map_status);
   FP_ExportCsvAppend(line, s.extreme_map_key);
   FP_ExportCsvAppend(line, s.mtf_alignment_status);
   FP_ExportCsvAppend(line, s.mtf_alignment_key);
   FP_ExportCsvAppend(line, s.mtf_context_role);
   FP_ExportCsvAppend(line, s.entry_bridge_status);
   FP_ExportCsvAppend(line, s.entry_bridge_readiness);
   FP_ExportCsvAppend(line, s.entry_bridge_key);
   FP_ExportCsvAppend(line, s.x_invalidation_status);
   FP_ExportCsvAppend(line, s.x_invalidation_key);
   FP_ExportCsvAppend(line, s.x_destination_status);
   FP_ExportCsvAppend(line, s.x_destination_key);
   FP_ExportCsvAppend(line, s.optionality_status);
   FP_ExportCsvAppend(line, s.optionality_key);
   FP_ExportCsvAppend(line, s.geometry_notes);
   return line;
}

bool FP_StateGateExportEntryGeometryCsv(const string path,
                                        const FP_StateGateSnapshot &snapshot,
                                        FP_StateGateReport &report)
{
   int handle = INVALID_HANDLE;
   if(!FP_StateGateExportOpenWrite(path, handle))
   {
      report.file_errors++;
      report.reason = report.reason + ";state_gate_entry_geometry_open_failed";
      return false;
   }
   FP_StateGateExportWriteLine(handle, FP_StateGateEntryGeometryHeader());
   for(int i=0; i<snapshot.timeframe_count; i++)
      FP_StateGateExportWriteLine(handle, FP_StateGateEntryGeometryRow(snapshot, i));
   FileClose(handle);
   report.files_written++;
   return true;
}



string FP_StateGateEntryIdeaHeader()
{
   string h = "";
   FP_ExportCsvAppend(h, "symbol");
   FP_ExportCsvAppend(h, "chart_timeframe");
   FP_ExportCsvAppend(h, "slot");
   FP_ExportCsvAppend(h, "timeframe");
   FP_ExportCsvAppend(h, "closed_bar_time");
   FP_ExportCsvAppend(h, "closed_bar_close");
   FP_ExportCsvAppend(h, "status");
   FP_ExportCsvAppend(h, "readiness");
   FP_ExportCsvAppend(h, "idea_family");
   FP_ExportCsvAppend(h, "idea_type");
   FP_ExportCsvAppend(h, "idea_direction");
   FP_ExportCsvAppend(h, "idea_source");
   FP_ExportCsvAppend(h, "idea_role");
   FP_ExportCsvAppend(h, "geometry_status");
   FP_ExportCsvAppend(h, "mtf_context_role");
   FP_ExportCsvAppend(h, "extreme_side");
   FP_ExportCsvAppend(h, "entry_price");
   FP_ExportCsvAppend(h, "invalidation_anchor_price");
   FP_ExportCsvAppend(h, "destination_anchor_price");
   FP_ExportCsvAppend(h, "destination_distance");
   FP_ExportCsvAppend(h, "risk_status");
   FP_ExportCsvAppend(h, "potential_R_status");
   FP_ExportCsvAppend(h, "potential_R");
   FP_ExportCsvAppend(h, "idea_key");
   FP_ExportCsvAppend(h, "label");
   FP_ExportCsvAppend(h, "state_key");
   FP_ExportCsvAppend(h, "geometry_key");
   FP_ExportCsvAppend(h, "mtf_alignment_key");
   return h;
}

string FP_StateGateEntryIdeaRowCsv(const FP_StateGateSnapshot &snapshot,
                                   const int index)
{
   FP_StateGateEntryIdeaRow e = snapshot.entry_idea_rows[index];
   string line = "";
   FP_ExportCsvAppend(line, snapshot.symbol);
   FP_ExportCsvAppend(line, EnumToString(snapshot.chart_timeframe));
   FP_ExportCsvAppend(line, IntegerToString(e.slot_index));
   FP_ExportCsvAppend(line, e.timeframe_label);
   FP_ExportCsvAppend(line, FP_ExportTime(e.last_closed_bar_time));
   FP_ExportCsvAppend(line, FP_ExportDouble(e.last_closed_bar_close));
   FP_ExportCsvAppend(line, IntegerToString(e.status));
   FP_ExportCsvAppend(line, e.readiness);
   FP_ExportCsvAppend(line, e.idea_family);
   FP_ExportCsvAppend(line, e.idea_type);
   FP_ExportCsvAppend(line, e.idea_direction);
   FP_ExportCsvAppend(line, e.idea_source);
   FP_ExportCsvAppend(line, e.idea_role);
   FP_ExportCsvAppend(line, e.geometry_status);
   FP_ExportCsvAppend(line, e.mtf_context_role);
   FP_ExportCsvAppend(line, e.extreme_side);
   FP_ExportCsvAppend(line, FP_ExportDouble(e.entry_price));
   FP_ExportCsvAppend(line, FP_ExportDouble(e.invalidation_anchor_price));
   FP_ExportCsvAppend(line, FP_ExportDouble(e.destination_anchor_price));
   FP_ExportCsvAppend(line, FP_ExportDouble(e.destination_distance));
   FP_ExportCsvAppend(line, e.risk_status);
   FP_ExportCsvAppend(line, e.potential_R_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(e.potential_R));
   FP_ExportCsvAppend(line, e.idea_key);
   FP_ExportCsvAppend(line, e.label);

   if(e.slot_index >= 0 && e.slot_index < snapshot.timeframe_count)
   {
      FP_StateGateTimeframeState s = snapshot.tf_states[e.slot_index];
      FP_ExportCsvAppend(line, s.state_key);
      FP_ExportCsvAppend(line, s.geometry_key);
      FP_ExportCsvAppend(line, s.mtf_alignment_key);
   }
   else
   {
      FP_ExportCsvAppend(line, "");
      FP_ExportCsvAppend(line, "");
      FP_ExportCsvAppend(line, "");
   }

   return line;
}

bool FP_StateGateExportEntryIdeasCsv(const string path,
                                     const FP_StateGateSnapshot &snapshot,
                                     FP_StateGateReport &report)
{
   int handle = INVALID_HANDLE;
   if(!FP_StateGateExportOpenWrite(path, handle))
   {
      report.file_errors++;
      report.reason = report.reason + ";state_gate_entry_ideas_open_failed";
      return false;
   }
   FP_StateGateExportWriteLine(handle, FP_StateGateEntryIdeaHeader());
   for(int i=0; i<snapshot.entry_idea_row_count; i++)
      FP_StateGateExportWriteLine(handle, FP_StateGateEntryIdeaRowCsv(snapshot, i));
   FileClose(handle);
   report.files_written++;
   return true;
}



string FP_StateGateEntryDecisionHeader()
{
   string h = "";
   FP_ExportCsvAppend(h, "symbol");
   FP_ExportCsvAppend(h, "chart_timeframe");
   FP_ExportCsvAppend(h, "slot");
   FP_ExportCsvAppend(h, "timeframe");
   FP_ExportCsvAppend(h, "closed_bar_time");
   FP_ExportCsvAppend(h, "closed_bar_close");
   FP_ExportCsvAppend(h, "status");
   FP_ExportCsvAppend(h, "readiness");
   FP_ExportCsvAppend(h, "decision_status");
   FP_ExportCsvAppend(h, "decision_direction");
   FP_ExportCsvAppend(h, "decision_type");
   FP_ExportCsvAppend(h, "decision_mode");
   FP_ExportCsvAppend(h, "decision_allowed");
   FP_ExportCsvAppend(h, "decision_price_status");
   FP_ExportCsvAppend(h, "decision_price");
   FP_ExportCsvAppend(h, "invalidation_status");
   FP_ExportCsvAppend(h, "invalidation_price");
   FP_ExportCsvAppend(h, "destination_status");
   FP_ExportCsvAppend(h, "destination_price");
   FP_ExportCsvAppend(h, "risk_status");
   FP_ExportCsvAppend(h, "potential_R_status");
   FP_ExportCsvAppend(h, "source_idea_key");
   FP_ExportCsvAppend(h, "source_geometry_key");
   FP_ExportCsvAppend(h, "source_mtf_key");
   FP_ExportCsvAppend(h, "block_reason");
   FP_ExportCsvAppend(h, "execution_status");
   FP_ExportCsvAppend(h, "decision_key");
   FP_ExportCsvAppend(h, "label");
   return h;
}

string FP_StateGateEntryDecisionRowCsv(const FP_StateGateSnapshot &snapshot,
                                       const int index)
{
   FP_StateGateEntryDecisionRow d = snapshot.entry_decision_rows[index];
   string line = "";
   FP_ExportCsvAppend(line, snapshot.symbol);
   FP_ExportCsvAppend(line, EnumToString(snapshot.chart_timeframe));
   FP_ExportCsvAppend(line, IntegerToString(d.slot_index));
   FP_ExportCsvAppend(line, d.timeframe_label);
   FP_ExportCsvAppend(line, FP_ExportTime(d.last_closed_bar_time));
   FP_ExportCsvAppend(line, FP_ExportDouble(d.last_closed_bar_close));
   FP_ExportCsvAppend(line, IntegerToString(d.status));
   FP_ExportCsvAppend(line, d.readiness);
   FP_ExportCsvAppend(line, d.decision_status);
   FP_ExportCsvAppend(line, d.decision_direction);
   FP_ExportCsvAppend(line, d.decision_type);
   FP_ExportCsvAppend(line, d.decision_mode);
   FP_ExportCsvAppend(line, FP_ExportBool(d.decision_allowed));
   FP_ExportCsvAppend(line, d.decision_price_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(d.decision_price));
   FP_ExportCsvAppend(line, d.invalidation_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(d.invalidation_price));
   FP_ExportCsvAppend(line, d.destination_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(d.destination_price));
   FP_ExportCsvAppend(line, d.risk_status);
   FP_ExportCsvAppend(line, d.potential_R_status);
   FP_ExportCsvAppend(line, d.source_idea_key);
   FP_ExportCsvAppend(line, d.source_geometry_key);
   FP_ExportCsvAppend(line, d.source_mtf_key);
   FP_ExportCsvAppend(line, d.block_reason);
   FP_ExportCsvAppend(line, d.execution_status);
   FP_ExportCsvAppend(line, d.decision_key);
   FP_ExportCsvAppend(line, d.label);
   return line;
}

bool FP_StateGateExportEntryDecisionsCsv(const string path,
                                         const FP_StateGateSnapshot &snapshot,
                                         FP_StateGateReport &report)
{
   int handle = INVALID_HANDLE;
   if(!FP_StateGateExportOpenWrite(path, handle))
   {
      report.file_errors++;
      report.reason = report.reason + ";state_gate_entry_decisions_open_failed";
      return false;
   }
   FP_StateGateExportWriteLine(handle, FP_StateGateEntryDecisionHeader());
   for(int i=0; i<snapshot.entry_decision_row_count; i++)
      FP_StateGateExportWriteLine(handle, FP_StateGateEntryDecisionRowCsv(snapshot, i));
   FileClose(handle);
   report.files_written++;
   return true;
}



string FP_StateGatePaperLedgerHeader()
{
   string h = "";
   FP_ExportCsvAppend(h, "symbol");
   FP_ExportCsvAppend(h, "chart_timeframe");
   FP_ExportCsvAppend(h, "slot");
   FP_ExportCsvAppend(h, "timeframe");
   FP_ExportCsvAppend(h, "recorded_at");
   FP_ExportCsvAppend(h, "closed_bar_time");
   FP_ExportCsvAppend(h, "closed_bar_close");
   FP_ExportCsvAppend(h, "status");
   FP_ExportCsvAppend(h, "record_status");
   FP_ExportCsvAppend(h, "ledger_mode");
   FP_ExportCsvAppend(h, "lifecycle_status");
   FP_ExportCsvAppend(h, "decision_status");
   FP_ExportCsvAppend(h, "decision_readiness");
   FP_ExportCsvAppend(h, "decision_direction");
   FP_ExportCsvAppend(h, "decision_type");
   FP_ExportCsvAppend(h, "decision_allowed");
   FP_ExportCsvAppend(h, "entry_price");
   FP_ExportCsvAppend(h, "invalidation_price");
   FP_ExportCsvAppend(h, "destination_price");
   FP_ExportCsvAppend(h, "risk_status");
   FP_ExportCsvAppend(h, "potential_R_status");
   FP_ExportCsvAppend(h, "source_decision_key");
   FP_ExportCsvAppend(h, "source_idea_key");
   FP_ExportCsvAppend(h, "source_geometry_key");
   FP_ExportCsvAppend(h, "source_mtf_key");
   FP_ExportCsvAppend(h, "execution_status");
   FP_ExportCsvAppend(h, "block_reason");
   FP_ExportCsvAppend(h, "ledger_key");
   FP_ExportCsvAppend(h, "event_id");
   FP_ExportCsvAppend(h, "label");
   return h;
}

string FP_StateGatePaperLedgerRowCsv(const FP_StateGateSnapshot &snapshot,
                                     const int index)
{
   FP_StateGatePaperLedgerRow p = snapshot.paper_ledger_rows[index];
   string line = "";
   FP_ExportCsvAppend(line, snapshot.symbol);
   FP_ExportCsvAppend(line, EnumToString(snapshot.chart_timeframe));
   FP_ExportCsvAppend(line, IntegerToString(p.slot_index));
   FP_ExportCsvAppend(line, p.timeframe_label);
   FP_ExportCsvAppend(line, FP_ExportTime(p.recorded_at));
   FP_ExportCsvAppend(line, FP_ExportTime(p.last_closed_bar_time));
   FP_ExportCsvAppend(line, FP_ExportDouble(p.last_closed_bar_close));
   FP_ExportCsvAppend(line, IntegerToString(p.status));
   FP_ExportCsvAppend(line, p.record_status);
   FP_ExportCsvAppend(line, p.ledger_mode);
   FP_ExportCsvAppend(line, p.lifecycle_status);
   FP_ExportCsvAppend(line, p.decision_status);
   FP_ExportCsvAppend(line, p.decision_readiness);
   FP_ExportCsvAppend(line, p.decision_direction);
   FP_ExportCsvAppend(line, p.decision_type);
   FP_ExportCsvAppend(line, FP_ExportBool(p.decision_allowed));
   FP_ExportCsvAppend(line, FP_ExportDouble(p.entry_price));
   FP_ExportCsvAppend(line, FP_ExportDouble(p.invalidation_price));
   FP_ExportCsvAppend(line, FP_ExportDouble(p.destination_price));
   FP_ExportCsvAppend(line, p.risk_status);
   FP_ExportCsvAppend(line, p.potential_R_status);
   FP_ExportCsvAppend(line, p.source_decision_key);
   FP_ExportCsvAppend(line, p.source_idea_key);
   FP_ExportCsvAppend(line, p.source_geometry_key);
   FP_ExportCsvAppend(line, p.source_mtf_key);
   FP_ExportCsvAppend(line, p.execution_status);
   FP_ExportCsvAppend(line, p.block_reason);
   FP_ExportCsvAppend(line, p.ledger_key);
   FP_ExportCsvAppend(line, p.event_id);
   FP_ExportCsvAppend(line, p.label);
   return line;
}

bool FP_StateGateExportPaperLedgerCsv(const string path,
                                      const FP_StateGateSnapshot &snapshot,
                                      FP_StateGateReport &report)
{
   int handle = INVALID_HANDLE;
   if(!FP_StateGateExportOpenWrite(path, handle))
   {
      report.file_errors++;
      report.reason = report.reason + ";state_gate_paper_ledger_open_failed";
      return false;
   }
   FP_StateGateExportWriteLine(handle, FP_StateGatePaperLedgerHeader());
   for(int i=0; i<snapshot.paper_ledger_row_count; i++)
      FP_StateGateExportWriteLine(handle, FP_StateGatePaperLedgerRowCsv(snapshot, i));
   FileClose(handle);
   report.files_written++;
   return true;
}



string FP_StateGatePaperLifecycleHeader()
{
   string h = "";
   FP_ExportCsvAppend(h, "symbol");
   FP_ExportCsvAppend(h, "chart_timeframe");
   FP_ExportCsvAppend(h, "slot");
   FP_ExportCsvAppend(h, "timeframe");
   FP_ExportCsvAppend(h, "evaluated_at");
   FP_ExportCsvAppend(h, "closed_bar_time");
   FP_ExportCsvAppend(h, "closed_bar_close");
   FP_ExportCsvAppend(h, "status");
   FP_ExportCsvAppend(h, "lifecycle_status");
   FP_ExportCsvAppend(h, "path_state");
   FP_ExportCsvAppend(h, "entry_touch_status");
   FP_ExportCsvAppend(h, "invalidation_touch_status");
   FP_ExportCsvAppend(h, "destination_touch_status");
   FP_ExportCsvAppend(h, "outcome");
   FP_ExportCsvAppend(h, "direction");
   FP_ExportCsvAppend(h, "decision_type");
   FP_ExportCsvAppend(h, "entry_price");
   FP_ExportCsvAppend(h, "invalidation_price");
   FP_ExportCsvAppend(h, "destination_price");
   FP_ExportCsvAppend(h, "entry_touched");
   FP_ExportCsvAppend(h, "invalidation_touched");
   FP_ExportCsvAppend(h, "destination_touched");
   FP_ExportCsvAppend(h, "source_ledger_key");
   FP_ExportCsvAppend(h, "source_decision_key");
   FP_ExportCsvAppend(h, "event_id");
   FP_ExportCsvAppend(h, "lifecycle_key");
   FP_ExportCsvAppend(h, "execution_status");
   FP_ExportCsvAppend(h, "label");
   return h;
}

string FP_StateGatePaperLifecycleRowCsv(const FP_StateGateSnapshot &snapshot,
                                        const int index)
{
   FP_StateGatePaperLifecycleRow p = snapshot.paper_lifecycle_rows[index];
   string line = "";
   FP_ExportCsvAppend(line, snapshot.symbol);
   FP_ExportCsvAppend(line, EnumToString(snapshot.chart_timeframe));
   FP_ExportCsvAppend(line, IntegerToString(p.slot_index));
   FP_ExportCsvAppend(line, p.timeframe_label);
   FP_ExportCsvAppend(line, FP_ExportTime(p.evaluated_at));
   FP_ExportCsvAppend(line, FP_ExportTime(p.last_closed_bar_time));
   FP_ExportCsvAppend(line, FP_ExportDouble(p.last_closed_bar_close));
   FP_ExportCsvAppend(line, IntegerToString(p.status));
   FP_ExportCsvAppend(line, p.lifecycle_status);
   FP_ExportCsvAppend(line, p.path_state);
   FP_ExportCsvAppend(line, p.entry_touch_status);
   FP_ExportCsvAppend(line, p.invalidation_touch_status);
   FP_ExportCsvAppend(line, p.destination_touch_status);
   FP_ExportCsvAppend(line, p.outcome);
   FP_ExportCsvAppend(line, p.direction);
   FP_ExportCsvAppend(line, p.decision_type);
   FP_ExportCsvAppend(line, FP_ExportDouble(p.entry_price));
   FP_ExportCsvAppend(line, FP_ExportDouble(p.invalidation_price));
   FP_ExportCsvAppend(line, FP_ExportDouble(p.destination_price));
   FP_ExportCsvAppend(line, FP_ExportBool(p.entry_touched));
   FP_ExportCsvAppend(line, FP_ExportBool(p.invalidation_touched));
   FP_ExportCsvAppend(line, FP_ExportBool(p.destination_touched));
   FP_ExportCsvAppend(line, p.source_ledger_key);
   FP_ExportCsvAppend(line, p.source_decision_key);
   FP_ExportCsvAppend(line, p.event_id);
   FP_ExportCsvAppend(line, p.lifecycle_key);
   FP_ExportCsvAppend(line, p.execution_status);
   FP_ExportCsvAppend(line, p.label);
   return line;
}

bool FP_StateGateExportPaperLifecycleCsv(const string path,
                                         const FP_StateGateSnapshot &snapshot,
                                         FP_StateGateReport &report)
{
   int handle = INVALID_HANDLE;
   if(!FP_StateGateExportOpenWrite(path, handle))
   {
      report.file_errors++;
      report.reason = report.reason + ";state_gate_paper_lifecycle_open_failed";
      return false;
   }
   FP_StateGateExportWriteLine(handle, FP_StateGatePaperLifecycleHeader());
   for(int i=0; i<snapshot.paper_lifecycle_row_count; i++)
      FP_StateGateExportWriteLine(handle, FP_StateGatePaperLifecycleRowCsv(snapshot, i));
   FileClose(handle);
   report.files_written++;
   return true;
}



string FP_StateGatePaperResultHeader()
{
   string h = "";
   FP_ExportCsvAppend(h, "symbol");
   FP_ExportCsvAppend(h, "chart_timeframe");
   FP_ExportCsvAppend(h, "slot");
   FP_ExportCsvAppend(h, "timeframe");
   FP_ExportCsvAppend(h, "summarized_at");
   FP_ExportCsvAppend(h, "closed_bar_time");
   FP_ExportCsvAppend(h, "closed_bar_close");
   FP_ExportCsvAppend(h, "status");
   FP_ExportCsvAppend(h, "result_status");
   FP_ExportCsvAppend(h, "outcome");
   FP_ExportCsvAppend(h, "result_bucket");
   FP_ExportCsvAppend(h, "direction");
   FP_ExportCsvAppend(h, "decision_type");
   FP_ExportCsvAppend(h, "entry_price");
   FP_ExportCsvAppend(h, "exit_anchor_price");
   FP_ExportCsvAppend(h, "destination_price");
   FP_ExportCsvAppend(h, "invalidation_price");
   FP_ExportCsvAppend(h, "price_delta");
   FP_ExportCsvAppend(h, "abs_distance");
   FP_ExportCsvAppend(h, "r_status");
   FP_ExportCsvAppend(h, "r_multiple");
   FP_ExportCsvAppend(h, "source_lifecycle_key");
   FP_ExportCsvAppend(h, "source_ledger_key");
   FP_ExportCsvAppend(h, "source_decision_key");
   FP_ExportCsvAppend(h, "event_id");
   FP_ExportCsvAppend(h, "result_key");
   FP_ExportCsvAppend(h, "execution_status");
   FP_ExportCsvAppend(h, "label");
   return h;
}

string FP_StateGatePaperResultRowCsv(const FP_StateGateSnapshot &snapshot,
                                     const int index)
{
   FP_StateGatePaperResultRow r = snapshot.paper_result_rows[index];
   string line = "";
   FP_ExportCsvAppend(line, snapshot.symbol);
   FP_ExportCsvAppend(line, EnumToString(snapshot.chart_timeframe));
   FP_ExportCsvAppend(line, IntegerToString(r.slot_index));
   FP_ExportCsvAppend(line, r.timeframe_label);
   FP_ExportCsvAppend(line, FP_ExportTime(r.summarized_at));
   FP_ExportCsvAppend(line, FP_ExportTime(r.last_closed_bar_time));
   FP_ExportCsvAppend(line, FP_ExportDouble(r.last_closed_bar_close));
   FP_ExportCsvAppend(line, IntegerToString(r.status));
   FP_ExportCsvAppend(line, r.result_status);
   FP_ExportCsvAppend(line, r.outcome);
   FP_ExportCsvAppend(line, r.result_bucket);
   FP_ExportCsvAppend(line, r.direction);
   FP_ExportCsvAppend(line, r.decision_type);
   FP_ExportCsvAppend(line, FP_ExportDouble(r.entry_price));
   FP_ExportCsvAppend(line, FP_ExportDouble(r.exit_anchor_price));
   FP_ExportCsvAppend(line, FP_ExportDouble(r.destination_price));
   FP_ExportCsvAppend(line, FP_ExportDouble(r.invalidation_price));
   FP_ExportCsvAppend(line, FP_ExportDouble(r.price_delta));
   FP_ExportCsvAppend(line, FP_ExportDouble(r.abs_distance));
   FP_ExportCsvAppend(line, r.r_status);
   FP_ExportCsvAppend(line, FP_ExportDouble(r.r_multiple));
   FP_ExportCsvAppend(line, r.source_lifecycle_key);
   FP_ExportCsvAppend(line, r.source_ledger_key);
   FP_ExportCsvAppend(line, r.source_decision_key);
   FP_ExportCsvAppend(line, r.event_id);
   FP_ExportCsvAppend(line, r.result_key);
   FP_ExportCsvAppend(line, r.execution_status);
   FP_ExportCsvAppend(line, r.label);
   return line;
}

bool FP_StateGateExportPaperResultsCsv(const string path,
                                       const FP_StateGateSnapshot &snapshot,
                                       FP_StateGateReport &report)
{
   int handle = INVALID_HANDLE;
   if(!FP_StateGateExportOpenWrite(path, handle))
   {
      report.file_errors++;
      report.reason = report.reason + ";state_gate_paper_results_open_failed";
      return false;
   }
   FP_StateGateExportWriteLine(handle, FP_StateGatePaperResultHeader());
   for(int i=0; i<snapshot.paper_result_row_count; i++)
      FP_StateGateExportWriteLine(handle, FP_StateGatePaperResultRowCsv(snapshot, i));
   FileClose(handle);
   report.files_written++;
   return true;
}


void FP_StateGateManifestKV(const int handle, const string key, const string value)
{
   string row = "";
   FP_ExportCsvAppend(row, key);
   FP_ExportCsvAppend(row, value);
   FP_StateGateExportWriteLine(handle, row);
}


string FP_StateGateDiagnosticsHeader()
{
   string h = "";
   FP_ExportCsvAppend(h, "kind");
   FP_ExportCsvAppend(h, "symbol");
   FP_ExportCsvAppend(h, "chart_timeframe");
   FP_ExportCsvAppend(h, "slot");
   FP_ExportCsvAppend(h, "timeframe");
   FP_ExportCsvAppend(h, "state_gate_version");
   FP_ExportCsvAppend(h, "effective_corner");
   FP_ExportCsvAppend(h, "force_left_upper");
   FP_ExportCsvAppend(h, "force_right_upper");
   FP_ExportCsvAppend(h, "panel_corner_input");
   FP_ExportCsvAppend(h, "panel_x");
   FP_ExportCsvAppend(h, "panel_y");
   FP_ExportCsvAppend(h, "panel_width");
   FP_ExportCsvAppend(h, "panel_font_size");
   FP_ExportCsvAppend(h, "panel_enabled");
   FP_ExportCsvAppend(h, "panel_show_diagnostics");
   FP_ExportCsvAppend(h, "closed_bar_available");
   FP_ExportCsvAppend(h, "dirty");
   FP_ExportCsvAppend(h, "tracker_status");
   FP_ExportCsvAppend(h, "rally_rows");
   FP_ExportCsvAppend(h, "hook_rows");
   FP_ExportCsvAppend(h, "state_key");
   FP_ExportCsvAppend(h, "reason");
   return h;
}

string FP_StateGateDiagnosticsGlobalRow(const FP_StateGateConfig &cfg,
                                        const FP_StateGateSnapshot &snapshot)
{
   string line = "";
   FP_ExportCsvAppend(line, "global");
   FP_ExportCsvAppend(line, snapshot.symbol);
   FP_ExportCsvAppend(line, EnumToString(snapshot.chart_timeframe));
   FP_ExportCsvAppend(line, "-1");
   FP_ExportCsvAppend(line, "ALL");
   FP_ExportCsvAppend(line, FP_STATE_GATE_VERSION);
   FP_ExportCsvAppend(line, FP_StateGateEffectiveCornerName(cfg));
   FP_ExportCsvAppend(line, FP_ExportBool(cfg.panel_force_left_upper));
   FP_ExportCsvAppend(line, FP_ExportBool(cfg.panel_force_right_upper));
   FP_ExportCsvAppend(line, FP_StateGateBaseCornerName(cfg.panel_corner));
   FP_ExportCsvAppend(line, IntegerToString(cfg.panel_x));
   FP_ExportCsvAppend(line, IntegerToString(cfg.panel_y));
   FP_ExportCsvAppend(line, IntegerToString(cfg.panel_width));
   FP_ExportCsvAppend(line, IntegerToString(cfg.panel_font_size));
   FP_ExportCsvAppend(line, FP_ExportBool(cfg.panel_enabled));
   FP_ExportCsvAppend(line, FP_ExportBool(cfg.panel_show_diagnostics));
   FP_ExportCsvAppend(line, "");
   FP_ExportCsvAppend(line, FP_ExportBool(snapshot.any_dirty));
   FP_ExportCsvAppend(line, snapshot.status);
   FP_ExportCsvAppend(line, IntegerToString(snapshot.rally_row_count));
   FP_ExportCsvAppend(line, IntegerToString(snapshot.hook_row_count));
   FP_ExportCsvAppend(line, "");
   FP_ExportCsvAppend(line, snapshot.reason);
   return line;
}

string FP_StateGateDiagnosticsSlotRow(const FP_StateGateConfig &cfg,
                                      const FP_StateGateSnapshot &snapshot,
                                      const int slot)
{
   FP_StateGateTimeframeState s = snapshot.tf_states[slot];
   string line = "";
   FP_ExportCsvAppend(line, "slot");
   FP_ExportCsvAppend(line, snapshot.symbol);
   FP_ExportCsvAppend(line, EnumToString(snapshot.chart_timeframe));
   FP_ExportCsvAppend(line, IntegerToString(slot));
   FP_ExportCsvAppend(line, s.timeframe_label);
   FP_ExportCsvAppend(line, FP_STATE_GATE_VERSION);
   FP_ExportCsvAppend(line, FP_StateGateEffectiveCornerName(cfg));
   FP_ExportCsvAppend(line, FP_ExportBool(cfg.panel_force_left_upper));
   FP_ExportCsvAppend(line, FP_ExportBool(cfg.panel_force_right_upper));
   FP_ExportCsvAppend(line, FP_StateGateBaseCornerName(cfg.panel_corner));
   FP_ExportCsvAppend(line, IntegerToString(cfg.panel_x));
   FP_ExportCsvAppend(line, IntegerToString(cfg.panel_y));
   FP_ExportCsvAppend(line, IntegerToString(cfg.panel_width));
   FP_ExportCsvAppend(line, IntegerToString(cfg.panel_font_size));
   FP_ExportCsvAppend(line, FP_ExportBool(cfg.panel_enabled));
   FP_ExportCsvAppend(line, FP_ExportBool(cfg.panel_show_diagnostics));
   FP_ExportCsvAppend(line, FP_ExportBool(s.closed_bar_available));
   FP_ExportCsvAppend(line, FP_ExportBool(s.dirty));
   FP_ExportCsvAppend(line, s.tracker_status);
   FP_ExportCsvAppend(line, IntegerToString(s.rally_row_count));
   FP_ExportCsvAppend(line, IntegerToString(s.hook_row_count));
   FP_ExportCsvAppend(line, s.state_key);
   FP_ExportCsvAppend(line, s.reason);
   return line;
}

bool FP_StateGateExportDiagnosticsCsv(const string path,
                                      const FP_StateGateConfig &cfg,
                                      const FP_StateGateSnapshot &snapshot,
                                      FP_StateGateReport &report)
{
   int handle = INVALID_HANDLE;
   if(!FP_StateGateExportOpenWrite(path, handle))
   {
      report.file_errors++;
      report.reason = report.reason + ";state_gate_diagnostics_open_failed";
      return false;
   }
   FP_StateGateExportWriteLine(handle, FP_StateGateDiagnosticsHeader());
   FP_StateGateExportWriteLine(handle, FP_StateGateDiagnosticsGlobalRow(cfg, snapshot));
   for(int i=0; i<snapshot.timeframe_count; i++)
      FP_StateGateExportWriteLine(handle, FP_StateGateDiagnosticsSlotRow(cfg, snapshot, i));
   FileClose(handle);
   report.files_written++;
   return true;
}


bool FP_StateGateExportManifestCsv(const string path,
                                   const FP_StateGateConfig &cfg,
                                   const FP_StateGateSnapshot &snapshot,
                                   FP_StateGateReport &report)
{
   int handle = INVALID_HANDLE;
   if(!FP_StateGateExportOpenWrite(path, handle))
   {
      report.file_errors++;
      report.reason = report.reason + ";state_gate_manifest_open_failed";
      return false;
   }
   string header = "";
   FP_ExportCsvAppend(header, "key");
   FP_ExportCsvAppend(header, "value");
   FP_StateGateExportWriteLine(handle, header);

   FP_StateGateManifestKV(handle, "state_gate_version", FP_STATE_GATE_VERSION);
   FP_StateGateManifestKV(handle, "export_time", TimeToString(TimeCurrent(), TIME_DATE|TIME_SECONDS));
   FP_StateGateManifestKV(handle, "symbol", snapshot.symbol);
   FP_StateGateManifestKV(handle, "chart_timeframe", EnumToString(snapshot.chart_timeframe));
   FP_StateGateManifestKV(handle, "closed_bar_mode", "shift_1_closed_candle_only");
   FP_StateGateManifestKV(handle, "tf1", FP_StateGateTimeframeName(cfg.tf1));
   FP_StateGateManifestKV(handle, "tf2", FP_StateGateTimeframeName(cfg.tf2));
   FP_StateGateManifestKV(handle, "tf3", FP_StateGateTimeframeName(cfg.tf3));
   FP_StateGateManifestKV(handle, "dirty_timeframes", IntegerToString(snapshot.dirty_timeframes));
   FP_StateGateManifestKV(handle, "available_timeframes", IntegerToString(snapshot.available_timeframes));
   FP_StateGateManifestKV(handle, "unchanged_timeframes", IntegerToString(snapshot.unchanged_timeframes));
   FP_StateGateManifestKV(handle, "unavailable_timeframes", IntegerToString(snapshot.unavailable_timeframes));
   FP_StateGateManifestKV(handle, "rally_rows", IntegerToString(snapshot.rally_row_count));
   FP_StateGateManifestKV(handle, "hook_rows", IntegerToString(snapshot.hook_row_count));
   FP_StateGateManifestKV(handle, "extreme_candidate_rows", IntegerToString(snapshot.extreme_candidate_row_count));
   FP_StateGateManifestKV(handle, "mtf_alignment_rows", IntegerToString(snapshot.mtf_alignment_row_count));
   FP_StateGateManifestKV(handle, "geometry_rows", IntegerToString(snapshot.timeframe_count));
   FP_StateGateManifestKV(handle, "panel_enabled", FP_ExportBool(cfg.panel_enabled));
   FP_StateGateManifestKV(handle, "panel_force_left_upper", FP_ExportBool(cfg.panel_force_left_upper));
   FP_StateGateManifestKV(handle, "panel_force_right_upper", FP_ExportBool(cfg.panel_force_right_upper));
   FP_StateGateManifestKV(handle, "panel_corner_input", FP_StateGateBaseCornerName(cfg.panel_corner));
   FP_StateGateManifestKV(handle, "panel_corner_effective", FP_StateGateEffectiveCornerName(cfg));
   FP_StateGateManifestKV(handle, "panel_x", IntegerToString(cfg.panel_x));
   FP_StateGateManifestKV(handle, "panel_y", IntegerToString(cfg.panel_y));
   FP_StateGateManifestKV(handle, "panel_width", IntegerToString(cfg.panel_width));
   FP_StateGateManifestKV(handle, "panel_font_size", IntegerToString(cfg.panel_font_size));
   FP_StateGateManifestKV(handle, "panel_compact_mode", FP_ExportBool(cfg.panel_compact_mode));
   FP_StateGateManifestKV(handle, "panel_show_closed_bar", FP_ExportBool(cfg.panel_show_closed_bar));
   FP_StateGateManifestKV(handle, "panel_show_row_counts", FP_ExportBool(cfg.panel_show_row_counts));
   FP_StateGateManifestKV(handle, "panel_rally_preview_rows_per_tf", IntegerToString(cfg.panel_rally_preview_rows_per_tf));
   FP_StateGateManifestKV(handle, "panel_hook_preview_rows_per_tf", IntegerToString(cfg.panel_hook_preview_rows_per_tf));
   FP_StateGateManifestKV(handle, "max_extreme_candidates_per_tf", IntegerToString(cfg.max_extreme_candidates_per_tf));
   FP_StateGateManifestKV(handle, "panel_show_contract_key", FP_ExportBool(cfg.panel_show_contract_key));
   FP_StateGateManifestKV(handle, "panel_show_diagnostics", FP_ExportBool(cfg.panel_show_diagnostics));
   FP_StateGateManifestKV(handle, "export_contract_csv", FP_ExportBool(cfg.export_contract_csv));
   FP_StateGateManifestKV(handle, "export_diagnostics_csv", FP_ExportBool(cfg.export_diagnostics_csv));
   FP_StateGateManifestKV(handle, "export_panel_lines_csv", FP_ExportBool(cfg.export_panel_lines_csv));
   FP_StateGateManifestKV(handle, "export_entry_bridge_csv", FP_ExportBool(cfg.export_entry_bridge_csv));
   FP_StateGateManifestKV(handle, "export_extreme_candidates_csv", FP_ExportBool(cfg.export_extreme_candidates_csv));
   FP_StateGateManifestKV(handle, "export_mtf_alignment_csv", FP_ExportBool(cfg.export_mtf_alignment_csv));
   FP_StateGateManifestKV(handle, "export_entry_geometry_csv", FP_ExportBool(cfg.export_entry_geometry_csv));
   FP_StateGateManifestKV(handle, "export_entry_ideas_csv", FP_ExportBool(cfg.export_entry_ideas_csv));
   FP_StateGateManifestKV(handle, "export_entry_decisions_csv", FP_ExportBool(cfg.export_entry_decisions_csv));
   FP_StateGateManifestKV(handle, "export_paper_ledger_csv", FP_ExportBool(cfg.export_paper_ledger_csv));
   FP_StateGateManifestKV(handle, "export_paper_lifecycle_csv", FP_ExportBool(cfg.export_paper_lifecycle_csv));
   FP_StateGateManifestKV(handle, "export_paper_results_csv", FP_ExportBool(cfg.export_paper_results_csv));
   FP_StateGateManifestKV(handle, "entry_idea_rows", IntegerToString(snapshot.entry_idea_row_count));
   FP_StateGateManifestKV(handle, "entry_decision_rows", IntegerToString(snapshot.entry_decision_row_count));
   FP_StateGateManifestKV(handle, "paper_ledger_rows", IntegerToString(snapshot.paper_ledger_row_count));
   FP_StateGateManifestKV(handle, "paper_lifecycle_rows", IntegerToString(snapshot.paper_lifecycle_row_count));
   FP_StateGateManifestKV(handle, "paper_result_rows", IntegerToString(snapshot.paper_result_row_count));
   FP_StateGateManifestKV(handle, "contract_rows", IntegerToString(snapshot.timeframe_count));
   FP_StateGateManifestKV(handle, "projection_state", "phase19_paper_result_metrics");

   FileClose(handle);
   report.files_written++;
   return true;
}

void FP_StateGateExportLatestCsv(const FP_StateGateConfig &cfg,
                                 const FP_StateGateSnapshot &snapshot,
                                 FP_StateGateReport &report)
{
   if(!cfg.export_csv) return;
   report.export_attempted = true;
   if(!snapshot.initialized)
   {
      report.reason = report.reason + ";state_gate_snapshot_not_initialized";
      return;
   }

   FP_ExportEnsureFolder(cfg.export_folder);
   string summary_path = FP_StateGateExportPath("summary", cfg);
   string rally_path = FP_StateGateExportPath("rally", cfg);
   string hooks_path = FP_StateGateExportPath("hooks", cfg);
   string panel_path = FP_StateGateExportPath("panel", cfg);
   string contract_path = FP_StateGateExportPath("contract", cfg);
   string diagnostics_path = FP_StateGateExportPath("diagnostics", cfg);
   string panel_lines_path = FP_StateGateExportPath("panel_lines", cfg);
   string entry_bridge_path = FP_StateGateExportPath("entry_bridge", cfg);
   string extreme_candidates_path = FP_StateGateExportPath("extreme_candidates", cfg);
   string mtf_alignment_path = FP_StateGateExportPath("mtf_alignment", cfg);
   string entry_geometry_path = FP_StateGateExportPath("entry_geometry", cfg);
   string entry_ideas_path = FP_StateGateExportPath("entry_ideas", cfg);
   string entry_decisions_path = FP_StateGateExportPath("entry_decisions", cfg);
   string paper_ledger_path = FP_StateGateExportPath("paper_ledger", cfg);
   string paper_lifecycle_path = FP_StateGateExportPath("paper_lifecycle", cfg);
   string paper_results_path = FP_StateGateExportPath("paper_results", cfg);
   string manifest_path = FP_StateGateExportPath("manifest", cfg);

   FP_StateGateExportSummaryCsv(summary_path, snapshot, report);
   FP_StateGateExportRallyCsv(rally_path, snapshot, report);
   FP_StateGateExportHookCsv(hooks_path, snapshot, report);
   FP_StateGateExportPanelCsv(panel_path, cfg, snapshot, report);
   if(cfg.export_contract_csv)
      FP_StateGateExportContractCsv(contract_path, snapshot, report);
   if(cfg.export_diagnostics_csv)
      FP_StateGateExportDiagnosticsCsv(diagnostics_path, cfg, snapshot, report);
   if(cfg.export_panel_lines_csv)
      FP_StateGateExportPanelLinesCsv(panel_lines_path, cfg, snapshot, report);
   if(cfg.export_entry_bridge_csv)
      FP_StateGateExportEntryBridgeCsv(entry_bridge_path, snapshot, report);
   if(cfg.export_extreme_candidates_csv)
      FP_StateGateExportExtremeCandidatesCsv(extreme_candidates_path, snapshot, report);
   if(cfg.export_mtf_alignment_csv)
      FP_StateGateExportMtfAlignmentCsv(mtf_alignment_path, snapshot, report);
   if(cfg.export_entry_geometry_csv)
      FP_StateGateExportEntryGeometryCsv(entry_geometry_path, snapshot, report);
   if(cfg.export_entry_ideas_csv)
      FP_StateGateExportEntryIdeasCsv(entry_ideas_path, snapshot, report);
   if(cfg.export_entry_decisions_csv)
      FP_StateGateExportEntryDecisionsCsv(entry_decisions_path, snapshot, report);
   if(cfg.export_paper_ledger_csv)
      FP_StateGateExportPaperLedgerCsv(paper_ledger_path, snapshot, report);
   if(cfg.export_paper_lifecycle_csv)
      FP_StateGateExportPaperLifecycleCsv(paper_lifecycle_path, snapshot, report);
   if(cfg.export_paper_results_csv)
      FP_StateGateExportPaperResultsCsv(paper_results_path, snapshot, report);
   FP_StateGateExportManifestCsv(manifest_path, cfg, snapshot, report);
}

#endif // __FP_STATE_GATE_EXPORT_MQH__
