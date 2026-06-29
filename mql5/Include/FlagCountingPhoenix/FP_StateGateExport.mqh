#ifndef __FP_STATE_GATE_EXPORT_MQH__
#define __FP_STATE_GATE_EXPORT_MQH__
#property strict

#include "FP_StateGateRules.mqh"
#include "FP_ExportRows.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 19 State Gate Export
// ----------------------------------------------------------------------------
// Phase 5 writes closed-bar tracker fields plus Rally View, Hook View, and
// dashboard-debug CSV rows. Hook rows are read-only projections of existing
// Hook/ND branch output and do not change Hook/ND logic.
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
   FP_ExportCsvAppend(h, "latest_established_f_summary");
   FP_ExportCsvAppend(h, "probable_next_f_summary");
   FP_ExportCsvAppend(h, "hook_summary");
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
   FP_ExportCsvAppend(line, s.latest_established_f_summary);
   FP_ExportCsvAppend(line, s.probable_next_f_summary);
   FP_ExportCsvAppend(line, s.hook_summary);
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
   FP_ExportCsvAppend(h, "rally_preview_limit");
   FP_ExportCsvAppend(h, "hook_preview_limit");
   FP_ExportCsvAppend(h, "latest_established_f_summary");
   FP_ExportCsvAppend(h, "probable_next_f_summary");
   FP_ExportCsvAppend(h, "hook_summary");
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
   FP_ExportCsvAppend(line, IntegerToString(cfg.panel_rally_preview_rows_per_tf));
   FP_ExportCsvAppend(line, IntegerToString(cfg.panel_hook_preview_rows_per_tf));
   FP_ExportCsvAppend(line, s.latest_established_f_summary);
   FP_ExportCsvAppend(line, s.probable_next_f_summary);
   FP_ExportCsvAppend(line, s.hook_summary);
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

void FP_StateGateManifestKV(const int handle, const string key, const string value)
{
   string row = "";
   FP_ExportCsvAppend(row, key);
   FP_ExportCsvAppend(row, value);
   FP_StateGateExportWriteLine(handle, row);
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
   FP_StateGateManifestKV(handle, "panel_enabled", FP_ExportBool(cfg.panel_enabled));
   FP_StateGateManifestKV(handle, "panel_force_right_upper", FP_ExportBool(cfg.panel_force_right_upper));
   FP_StateGateManifestKV(handle, "panel_corner_effective", (cfg.panel_force_right_upper ? "CORNER_RIGHT_UPPER" : IntegerToString(cfg.panel_corner)));
   FP_StateGateManifestKV(handle, "panel_width", IntegerToString(cfg.panel_width));
   FP_StateGateManifestKV(handle, "panel_font_size", IntegerToString(cfg.panel_font_size));
   FP_StateGateManifestKV(handle, "panel_compact_mode", FP_ExportBool(cfg.panel_compact_mode));
   FP_StateGateManifestKV(handle, "panel_show_closed_bar", FP_ExportBool(cfg.panel_show_closed_bar));
   FP_StateGateManifestKV(handle, "panel_show_row_counts", FP_ExportBool(cfg.panel_show_row_counts));
   FP_StateGateManifestKV(handle, "panel_rally_preview_rows_per_tf", IntegerToString(cfg.panel_rally_preview_rows_per_tf));
   FP_StateGateManifestKV(handle, "panel_hook_preview_rows_per_tf", IntegerToString(cfg.panel_hook_preview_rows_per_tf));
   FP_StateGateManifestKV(handle, "projection_state", "phase5_rally_hook_panel_polished");

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
   string manifest_path = FP_StateGateExportPath("manifest", cfg);

   FP_StateGateExportSummaryCsv(summary_path, snapshot, report);
   FP_StateGateExportRallyCsv(rally_path, snapshot, report);
   FP_StateGateExportHookCsv(hooks_path, snapshot, report);
   FP_StateGateExportPanelCsv(panel_path, cfg, snapshot, report);
   FP_StateGateExportManifestCsv(manifest_path, cfg, snapshot, report);
}

#endif // __FP_STATE_GATE_EXPORT_MQH__
