#ifndef __FP_STATE_GATE_EXPORT_MQH__
#define __FP_STATE_GATE_EXPORT_MQH__
#property strict

#include "FP_StateGatePanel.mqh"

string FP_L19ExportPath(const FP_Level19StateGateConfig &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL19_STATE_GATE_DEFAULT_FOLDER;
   return folder + "\\latest_state_gate_level19.csv";
}

string FP_L19ClosedBarLedgerPath(const FP_Level19StateGateConfig &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL19_STATE_GATE_DEFAULT_FOLDER;
   return folder + "\\state_gate_level19_closed_bar_ledger.csv";
}

string FP_L19StateDeltaPath(const FP_Level19StateGateConfig &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL19_STATE_GATE_DEFAULT_FOLDER;
   return folder + "\\state_gate_level19_state_delta.csv";
}

string FP_L19TransitionEventPath(const FP_Level19StateGateConfig &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL19_STATE_GATE_DEFAULT_FOLDER;
   return folder + "\\state_gate_level19_transition_events.csv";
}

string FP_L19TransitionSummaryPath(const FP_Level19StateGateConfig &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL19_STATE_GATE_DEFAULT_FOLDER;
   return folder + "\\state_gate_level19_transition_summary.csv";
}

string FP_L19TransitionStabilityPath(const FP_Level19StateGateConfig &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL19_STATE_GATE_DEFAULT_FOLDER;
   return folder + "\\state_gate_level19_transition_stability.csv";
}

string FP_L19RegimeLabelPath(const FP_Level19StateGateConfig &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL19_STATE_GATE_DEFAULT_FOLDER;
   return folder + "\\state_gate_level19_regime_labels.csv";
}

string FP_L19CompletionPath(const FP_Level19StateGateConfig &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL19_STATE_GATE_DEFAULT_FOLDER;
   return folder + "\\state_gate_level19_completion.csv";
}

string FP_L19Header()
{
   return "generated_at,version,symbol,period,bars,scale_count,timebase_ok,timebase_status,timebase_reason,first_bar_time,last_bar_time,raw_nodes_total,nodes_total,confirmed_nodes_total,pending_nodes_total,hooks_total,visible_hooks_seen,events_total,visible_events_total,hidden_events_total,f1_total,f2_total,f3_total,nd_total,export_attempted,export_ok,export_files_written,export_file_errors,render_attempted,render_ok,render_objects_created,render_object_errors,render_objects_deleted,render_reason,validation_attempted,validation_ok,validation_failed,validation_warned,latest_visible_event_id,latest_visible_event_level,latest_visible_event_L,latest_visible_event_direction,latest_visible_event_status,latest_visible_hook_id,latest_visible_hook_L,latest_visible_hook_direction,latest_visible_hook_status,latest_visible_hook_is_nd,latest_visible_hook_node_count,state_status,state_key,no_touch_contract";
}

string FP_L19Row(const FP_Level19StateGateSnapshot &s)
{
   string r = "";
   r += FP_L19SafeCsv(FP_L19Time(s.generated_at));
   r += "," + FP_L19SafeCsv(s.version);
   r += "," + FP_L19SafeCsv(s.symbol);
   r += "," + FP_L19SafeCsv(s.period_label);
   r += "," + IntegerToString(s.bars);
   r += "," + IntegerToString(s.scale_count);
   r += "," + FP_L19SafeCsv(FP_L19Bool(s.timebase_ok));
   r += "," + FP_L19SafeCsv(s.timebase_status);
   r += "," + FP_L19SafeCsv(s.timebase_reason);
   r += "," + FP_L19SafeCsv(FP_L19Time(s.first_bar_time));
   r += "," + FP_L19SafeCsv(FP_L19Time(s.last_bar_time));
   r += "," + IntegerToString(s.raw_nodes_total);
   r += "," + IntegerToString(s.nodes_total);
   r += "," + IntegerToString(s.confirmed_nodes_total);
   r += "," + IntegerToString(s.pending_nodes_total);
   r += "," + IntegerToString(s.hooks_total);
   r += "," + IntegerToString(s.visible_hooks_seen);
   r += "," + IntegerToString(s.events_total);
   r += "," + IntegerToString(s.visible_events_total);
   r += "," + IntegerToString(s.hidden_events_total);
   r += "," + IntegerToString(s.f1_total);
   r += "," + IntegerToString(s.f2_total);
   r += "," + IntegerToString(s.f3_total);
   r += "," + IntegerToString(s.nd_total);
   r += "," + FP_L19SafeCsv(FP_L19Bool(s.export_attempted));
   r += "," + FP_L19SafeCsv(FP_L19Bool(s.export_ok));
   r += "," + IntegerToString(s.export_files_written);
   r += "," + IntegerToString(s.export_file_errors);
   r += "," + FP_L19SafeCsv(FP_L19Bool(s.render_attempted));
   r += "," + FP_L19SafeCsv(FP_L19Bool(s.render_ok));
   r += "," + IntegerToString(s.render_objects_created);
   r += "," + IntegerToString(s.render_object_errors);
   r += "," + IntegerToString(s.render_objects_deleted);
   r += "," + FP_L19SafeCsv(s.render_reason);
   r += "," + FP_L19SafeCsv(FP_L19Bool(s.validation_attempted));
   r += "," + FP_L19SafeCsv(FP_L19Bool(s.validation_ok));
   r += "," + IntegerToString(s.validation_failed);
   r += "," + IntegerToString(s.validation_warned);
   r += "," + FP_L19SafeCsv(s.latest_visible_event_id);
   r += "," + IntegerToString(s.latest_visible_event_level);
   r += "," + IntegerToString(s.latest_visible_event_L);
   r += "," + IntegerToString(s.latest_visible_event_direction);
   r += "," + IntegerToString(s.latest_visible_event_status);
   r += "," + FP_L19SafeCsv(s.latest_visible_hook_id);
   r += "," + IntegerToString(s.latest_visible_hook_L);
   r += "," + IntegerToString(s.latest_visible_hook_direction);
   r += "," + IntegerToString(s.latest_visible_hook_status);
   r += "," + FP_L19SafeCsv(FP_L19Bool(s.latest_visible_hook_is_nd));
   r += "," + IntegerToString(s.latest_visible_hook_node_count);
   r += "," + FP_L19SafeCsv(s.state_status);
   r += "," + FP_L19SafeCsv(s.state_key);
   r += "," + FP_L19SafeCsv(s.no_touch_contract);
   return r;
}

bool FP_L19ExportSnapshot(const FP_Level19StateGateConfig &cfg,
                          const FP_Level19StateGateSnapshot &s,
                          FP_Level19StateGateReport &report)
{
   if(!cfg.export_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL19_STATE_GATE_DEFAULT_FOLDER;
   FolderCreate(folder);

   string path = FP_L19ExportPath(cfg);
   int handle = FileOpen(path, FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "level19_state_gate_export_open_failed";
      return false;
   }

   FileWriteString(handle, FP_L19Header() + "\r\n");
   FileWriteString(handle, FP_L19Row(s) + "\r\n");
   FileClose(handle);

   report.files_written++;
   return true;
}


bool FP_L19AppendClosedBarLedger(const FP_Level19StateGateConfig &cfg,
                                 const FP_Level19StateGateSnapshot &s,
                                 FP_Level19StateGateReport &report)
{
   if(!cfg.export_closed_bar_ledger_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL19_STATE_GATE_DEFAULT_FOLDER;
   FolderCreate(folder);

   string path = FP_L19ClosedBarLedgerPath(cfg);
   bool exists = FileIsExist(path);

   int handle = INVALID_HANDLE;
   if(!exists)
   {
      handle = FileOpen(path, FILE_WRITE|FILE_TXT|FILE_ANSI);
      if(handle == INVALID_HANDLE)
      {
         report.file_errors++;
         report.reason = "level19_closed_bar_ledger_create_failed";
         return false;
      }
      FileWriteString(handle, FP_L19Header() + "\r\n");
      FileWriteString(handle, FP_L19Row(s) + "\r\n");
      FileClose(handle);
      report.files_written++;
      report.ledger_written = true;
      return true;
   }

   handle = FileOpen(path, FILE_READ|FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "level19_closed_bar_ledger_open_failed";
      return false;
   }

   FileSeek(handle, 0, SEEK_END);
   FileWriteString(handle, FP_L19Row(s) + "\r\n");
   FileClose(handle);

   report.files_written++;
   report.ledger_written = true;
   return true;
}


string FP_L19StateDeltaHeader()
{
   string h = "";
   h += "generated_at,version,symbol,period,current_closed_bar_time,previous_closed_bar_time,has_previous,delta_status,delta_key";
   h += ",events_before,events_after,events_delta,events_delta_direction";
   h += ",hooks_before,hooks_after,hooks_delta,hooks_delta_direction";
   h += ",visible_events_before,visible_events_after,visible_events_delta,visible_events_delta_direction";
   h += ",f1_before,f1_after,f1_delta,f1_delta_direction";
   h += ",f2_before,f2_after,f2_delta,f2_delta_direction";
   h += ",f3_before,f3_after,f3_delta,f3_delta_direction";
   h += ",nd_before,nd_after,nd_delta,nd_delta_direction";
   h += ",latest_event_before,latest_event_after,latest_event_change";
   h += ",latest_hook_before,latest_hook_after,latest_hook_change";
   h += ",render_ok_before,render_ok_after,render_ok_change";
   h += ",validation_ok_before,validation_ok_after,validation_ok_change";
   h += ",state_status_before,state_status_after,state_key_before,state_key_after,no_touch_contract";
   return h;
}

string FP_L19StateDeltaRow(const bool has_previous,
                           const FP_Level19StateGateSnapshot &previous,
                           const FP_Level19StateGateSnapshot &current)
{
   int events_before = has_previous ? previous.events_total : 0;
   int hooks_before = has_previous ? previous.hooks_total : 0;
   int visible_before = has_previous ? previous.visible_events_total : 0;
   int f1_before = has_previous ? previous.f1_total : 0;
   int f2_before = has_previous ? previous.f2_total : 0;
   int f3_before = has_previous ? previous.f3_total : 0;
   int nd_before = has_previous ? previous.nd_total : 0;

   int events_delta = has_previous ? current.events_total - previous.events_total : 0;
   int hooks_delta = has_previous ? current.hooks_total - previous.hooks_total : 0;
   int visible_delta = has_previous ? current.visible_events_total - previous.visible_events_total : 0;
   int f1_delta = has_previous ? current.f1_total - previous.f1_total : 0;
   int f2_delta = has_previous ? current.f2_total - previous.f2_total : 0;
   int f3_delta = has_previous ? current.f3_total - previous.f3_total : 0;
   int nd_delta = has_previous ? current.nd_total - previous.nd_total : 0;

   string previous_event = has_previous ? previous.latest_visible_event_id : "NO_PREVIOUS";
   string previous_hook = has_previous ? previous.latest_visible_hook_id : "NO_PREVIOUS";
   string previous_status = has_previous ? previous.state_status : "NO_PREVIOUS";
   string previous_key = has_previous ? previous.state_key : "NO_PREVIOUS";

   string r = "";
   r += FP_L19SafeCsv(FP_L19Time(current.generated_at));
   r += "," + FP_L19SafeCsv(current.version);
   r += "," + FP_L19SafeCsv(current.symbol);
   r += "," + FP_L19SafeCsv(current.period_label);
   r += "," + FP_L19SafeCsv(FP_L19Time(current.last_bar_time));
   r += "," + FP_L19SafeCsv(has_previous ? FP_L19Time(previous.last_bar_time) : "");
   r += "," + FP_L19SafeCsv(FP_L19Bool(has_previous));
   r += "," + FP_L19SafeCsv(FP_L19DeltaStatus(has_previous, previous, current));
   r += "," + FP_L19SafeCsv(FP_L19DeltaKey(has_previous, previous, current));

   r += "," + IntegerToString(events_before);
   r += "," + IntegerToString(current.events_total);
   r += "," + IntegerToString(events_delta);
   r += "," + FP_L19SafeCsv(FP_L19DeltaDirection(events_delta));

   r += "," + IntegerToString(hooks_before);
   r += "," + IntegerToString(current.hooks_total);
   r += "," + IntegerToString(hooks_delta);
   r += "," + FP_L19SafeCsv(FP_L19DeltaDirection(hooks_delta));

   r += "," + IntegerToString(visible_before);
   r += "," + IntegerToString(current.visible_events_total);
   r += "," + IntegerToString(visible_delta);
   r += "," + FP_L19SafeCsv(FP_L19DeltaDirection(visible_delta));

   r += "," + IntegerToString(f1_before);
   r += "," + IntegerToString(current.f1_total);
   r += "," + IntegerToString(f1_delta);
   r += "," + FP_L19SafeCsv(FP_L19DeltaDirection(f1_delta));

   r += "," + IntegerToString(f2_before);
   r += "," + IntegerToString(current.f2_total);
   r += "," + IntegerToString(f2_delta);
   r += "," + FP_L19SafeCsv(FP_L19DeltaDirection(f2_delta));

   r += "," + IntegerToString(f3_before);
   r += "," + IntegerToString(current.f3_total);
   r += "," + IntegerToString(f3_delta);
   r += "," + FP_L19SafeCsv(FP_L19DeltaDirection(f3_delta));

   r += "," + IntegerToString(nd_before);
   r += "," + IntegerToString(current.nd_total);
   r += "," + IntegerToString(nd_delta);
   r += "," + FP_L19SafeCsv(FP_L19DeltaDirection(nd_delta));

   r += "," + FP_L19SafeCsv(previous_event);
   r += "," + FP_L19SafeCsv(current.latest_visible_event_id);
   r += "," + FP_L19SafeCsv(has_previous ? FP_L19StringChange(previous.latest_visible_event_id, current.latest_visible_event_id) : "BASELINE");

   r += "," + FP_L19SafeCsv(previous_hook);
   r += "," + FP_L19SafeCsv(current.latest_visible_hook_id);
   r += "," + FP_L19SafeCsv(has_previous ? FP_L19StringChange(previous.latest_visible_hook_id, current.latest_visible_hook_id) : "BASELINE");

   r += "," + FP_L19SafeCsv(has_previous ? FP_L19Bool(previous.render_ok) : "");
   r += "," + FP_L19SafeCsv(FP_L19Bool(current.render_ok));
   r += "," + FP_L19SafeCsv(has_previous ? FP_L19BoolChange(previous.render_ok, current.render_ok) : "BASELINE");

   r += "," + FP_L19SafeCsv(has_previous ? FP_L19Bool(previous.validation_ok) : "");
   r += "," + FP_L19SafeCsv(FP_L19Bool(current.validation_ok));
   r += "," + FP_L19SafeCsv(has_previous ? FP_L19BoolChange(previous.validation_ok, current.validation_ok) : "BASELINE");

   r += "," + FP_L19SafeCsv(previous_status);
   r += "," + FP_L19SafeCsv(current.state_status);
   r += "," + FP_L19SafeCsv(previous_key);
   r += "," + FP_L19SafeCsv(current.state_key);
   r += "," + FP_L19SafeCsv("READ_ONLY_DELTA_LEDGER_NO_RENDERER_MUTATION_NO_CHART_OBJECT_CHANGE");
   return r;
}

bool FP_L19AppendStateDeltaLedger(const FP_Level19StateGateConfig &cfg,
                                  const bool has_previous,
                                  const FP_Level19StateGateSnapshot &previous,
                                  const FP_Level19StateGateSnapshot &current,
                                  FP_Level19StateGateReport &report)
{
   if(!cfg.export_state_delta_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL19_STATE_GATE_DEFAULT_FOLDER;
   FolderCreate(folder);

   string path = FP_L19StateDeltaPath(cfg);
   bool exists = FileIsExist(path);

   int handle = INVALID_HANDLE;
   if(!exists)
   {
      handle = FileOpen(path, FILE_WRITE|FILE_TXT|FILE_ANSI);
      if(handle == INVALID_HANDLE)
      {
         report.file_errors++;
         report.reason = "level19_state_delta_create_failed";
         return false;
      }
      FileWriteString(handle, FP_L19StateDeltaHeader() + "\r\n");
      FileWriteString(handle, FP_L19StateDeltaRow(has_previous, previous, current) + "\r\n");
      FileClose(handle);
      report.files_written++;
      report.state_delta_written = true;
      return true;
   }

   handle = FileOpen(path, FILE_READ|FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "level19_state_delta_open_failed";
      return false;
   }

   FileSeek(handle, 0, SEEK_END);
   FileWriteString(handle, FP_L19StateDeltaRow(has_previous, previous, current) + "\r\n");
   FileClose(handle);

   report.files_written++;
   report.state_delta_written = true;
   return true;
}


string FP_L19TransitionEventHeader()
{
   string h = "";
   h += "generated_at,version,symbol,period,current_closed_bar_time,previous_closed_bar_time,has_previous";
   h += ",transition_family,transition_severity,bias_hint,action_hint,transition_key";
   h += ",events_delta,hooks_delta,visible_events_delta,f1_delta,f2_delta,f3_delta,nd_delta";
   h += ",latest_event_before,latest_event_after,latest_hook_before,latest_hook_after";
   h += ",render_ok_before,render_ok_after,validation_ok_before,validation_ok_after";
   h += ",state_status_before,state_status_after,no_touch_contract";
   return h;
}

string FP_L19TransitionEventRow(const bool has_previous,
                                const FP_Level19StateGateSnapshot &previous,
                                const FP_Level19StateGateSnapshot &current)
{
   string family = FP_L19TransitionFamily(has_previous, previous, current);
   string severity = FP_L19TransitionSeverity(has_previous, previous, current);
   string bias = FP_L19TransitionBiasHint(has_previous, previous, current);
   string action = FP_L19TransitionActionHint(family, severity);

   int events_delta = has_previous ? current.events_total - previous.events_total : 0;
   int hooks_delta = has_previous ? current.hooks_total - previous.hooks_total : 0;
   int visible_delta = has_previous ? current.visible_events_total - previous.visible_events_total : 0;
   int f1_delta = has_previous ? current.f1_total - previous.f1_total : 0;
   int f2_delta = has_previous ? current.f2_total - previous.f2_total : 0;
   int f3_delta = has_previous ? current.f3_total - previous.f3_total : 0;
   int nd_delta = has_previous ? current.nd_total - previous.nd_total : 0;

   string r = "";
   r += FP_L19SafeCsv(FP_L19Time(current.generated_at));
   r += "," + FP_L19SafeCsv(current.version);
   r += "," + FP_L19SafeCsv(current.symbol);
   r += "," + FP_L19SafeCsv(current.period_label);
   r += "," + FP_L19SafeCsv(FP_L19Time(current.last_bar_time));
   r += "," + FP_L19SafeCsv(has_previous ? FP_L19Time(previous.last_bar_time) : "");
   r += "," + FP_L19SafeCsv(FP_L19Bool(has_previous));
   r += "," + FP_L19SafeCsv(family);
   r += "," + FP_L19SafeCsv(severity);
   r += "," + FP_L19SafeCsv(bias);
   r += "," + FP_L19SafeCsv(action);
   r += "," + FP_L19SafeCsv(FP_L19TransitionKey(has_previous, previous, current));

   r += "," + IntegerToString(events_delta);
   r += "," + IntegerToString(hooks_delta);
   r += "," + IntegerToString(visible_delta);
   r += "," + IntegerToString(f1_delta);
   r += "," + IntegerToString(f2_delta);
   r += "," + IntegerToString(f3_delta);
   r += "," + IntegerToString(nd_delta);

   r += "," + FP_L19SafeCsv(has_previous ? previous.latest_visible_event_id : "NO_PREVIOUS");
   r += "," + FP_L19SafeCsv(current.latest_visible_event_id);
   r += "," + FP_L19SafeCsv(has_previous ? previous.latest_visible_hook_id : "NO_PREVIOUS");
   r += "," + FP_L19SafeCsv(current.latest_visible_hook_id);

   r += "," + FP_L19SafeCsv(has_previous ? FP_L19Bool(previous.render_ok) : "");
   r += "," + FP_L19SafeCsv(FP_L19Bool(current.render_ok));
   r += "," + FP_L19SafeCsv(has_previous ? FP_L19Bool(previous.validation_ok) : "");
   r += "," + FP_L19SafeCsv(FP_L19Bool(current.validation_ok));

   r += "," + FP_L19SafeCsv(has_previous ? previous.state_status : "NO_PREVIOUS");
   r += "," + FP_L19SafeCsv(current.state_status);
   r += "," + FP_L19SafeCsv("READ_ONLY_TRANSITION_EVENT_LEDGER_NO_RENDERER_MUTATION_NO_CHART_OBJECT_CHANGE");
   return r;
}

bool FP_L19AppendTransitionEventLedger(const FP_Level19StateGateConfig &cfg,
                                       const bool has_previous,
                                       const FP_Level19StateGateSnapshot &previous,
                                       const FP_Level19StateGateSnapshot &current,
                                       FP_Level19StateGateReport &report)
{
   if(!cfg.export_transition_event_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL19_STATE_GATE_DEFAULT_FOLDER;
   FolderCreate(folder);

   string path = FP_L19TransitionEventPath(cfg);
   bool exists = FileIsExist(path);

   int handle = INVALID_HANDLE;
   if(!exists)
   {
      handle = FileOpen(path, FILE_WRITE|FILE_TXT|FILE_ANSI);
      if(handle == INVALID_HANDLE)
      {
         report.file_errors++;
         report.reason = "level19_transition_event_create_failed";
         return false;
      }
      FileWriteString(handle, FP_L19TransitionEventHeader() + "\r\n");
      FileWriteString(handle, FP_L19TransitionEventRow(has_previous, previous, current) + "\r\n");
      FileClose(handle);
      report.files_written++;
      report.transition_event_written = true;
      return true;
   }

   handle = FileOpen(path, FILE_READ|FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "level19_transition_event_open_failed";
      return false;
   }

   FileSeek(handle, 0, SEEK_END);
   FileWriteString(handle, FP_L19TransitionEventRow(has_previous, previous, current) + "\r\n");
   FileClose(handle);

   report.files_written++;
   report.transition_event_written = true;
   return true;
}


string FP_L19TransitionSummaryHeader()
{
   string h = "";
   h += "generated_at,version,symbol,period,total_transition_rows,baseline_rows,no_change_rows";
   h += ",health_rows,major_rows,structural_rows,minor_rows";
   h += ",f1_expansion_rows,f2_expansion_rows,f3_expansion_rows,f_count_contraction_rows";
   h += ",nd_change_rows,hook_change_rows,visibility_change_rows,event_count_change_rows";
   h += ",latest_event_change_rows,latest_hook_change_rows,state_key_change_rows";
   h += ",dominant_transition_family,dominant_severity,no_touch_contract";
   return h;
}

string FP_L19TransitionSummaryRow(const FP_Level19StateGateSnapshot &current,
                                  const int total_rows,
                                  const int baseline_rows,
                                  const int no_change_rows,
                                  const int health_rows,
                                  const int major_rows,
                                  const int structural_rows,
                                  const int minor_rows,
                                  const int f1_rows,
                                  const int f2_rows,
                                  const int f3_rows,
                                  const int f_contraction_rows,
                                  const int nd_rows,
                                  const int hook_rows,
                                  const int visibility_rows,
                                  const int event_count_rows,
                                  const int latest_event_rows,
                                  const int latest_hook_rows,
                                  const int state_key_rows,
                                  const string dominant_family,
                                  const string dominant_severity)
{
   string r = "";
   r += FP_L19SafeCsv(FP_L19Time(current.generated_at));
   r += "," + FP_L19SafeCsv(current.version);
   r += "," + FP_L19SafeCsv(current.symbol);
   r += "," + FP_L19SafeCsv(current.period_label);
   r += "," + IntegerToString(total_rows);
   r += "," + IntegerToString(baseline_rows);
   r += "," + IntegerToString(no_change_rows);
   r += "," + IntegerToString(health_rows);
   r += "," + IntegerToString(major_rows);
   r += "," + IntegerToString(structural_rows);
   r += "," + IntegerToString(minor_rows);
   r += "," + IntegerToString(f1_rows);
   r += "," + IntegerToString(f2_rows);
   r += "," + IntegerToString(f3_rows);
   r += "," + IntegerToString(f_contraction_rows);
   r += "," + IntegerToString(nd_rows);
   r += "," + IntegerToString(hook_rows);
   r += "," + IntegerToString(visibility_rows);
   r += "," + IntegerToString(event_count_rows);
   r += "," + IntegerToString(latest_event_rows);
   r += "," + IntegerToString(latest_hook_rows);
   r += "," + IntegerToString(state_key_rows);
   r += "," + FP_L19SafeCsv(dominant_family);
   r += "," + FP_L19SafeCsv(dominant_severity);
   r += "," + FP_L19SafeCsv("READ_ONLY_TRANSITION_SUMMARY_NO_RENDERER_MUTATION_NO_EXECUTION");
   return r;
}

bool FP_L19WriteTransitionSummary(const FP_Level19StateGateConfig &cfg,
                                  const FP_Level19StateGateSnapshot &current,
                                  const int total_rows,
                                  const int baseline_rows,
                                  const int no_change_rows,
                                  const int health_rows,
                                  const int major_rows,
                                  const int structural_rows,
                                  const int minor_rows,
                                  const int f1_rows,
                                  const int f2_rows,
                                  const int f3_rows,
                                  const int f_contraction_rows,
                                  const int nd_rows,
                                  const int hook_rows,
                                  const int visibility_rows,
                                  const int event_count_rows,
                                  const int latest_event_rows,
                                  const int latest_hook_rows,
                                  const int state_key_rows,
                                  const string dominant_family,
                                  const string dominant_severity,
                                  FP_Level19StateGateReport &report)
{
   if(!cfg.export_transition_summary_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL19_STATE_GATE_DEFAULT_FOLDER;
   FolderCreate(folder);

   int handle = FileOpen(FP_L19TransitionSummaryPath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "level19_transition_summary_open_failed";
      return false;
   }

   FileWriteString(handle, FP_L19TransitionSummaryHeader() + "\r\n");
   FileWriteString(handle, FP_L19TransitionSummaryRow(current, total_rows, baseline_rows, no_change_rows,
                                                     health_rows, major_rows, structural_rows, minor_rows,
                                                     f1_rows, f2_rows, f3_rows, f_contraction_rows,
                                                     nd_rows, hook_rows, visibility_rows, event_count_rows,
                                                     latest_event_rows, latest_hook_rows, state_key_rows,
                                                     dominant_family, dominant_severity) + "\r\n");
   FileClose(handle);
   report.files_written++;
   report.transition_summary_written = true;
   return true;
}

string FP_L19TransitionStabilityHeader()
{
   string h = "";
   h += "generated_at,version,symbol,period,current_closed_bar_time,transition_family,transition_severity";
   h += ",previous_transition_family,current_streak,stability_status,stability_quality,bias_hint,action_hint,no_touch_contract";
   return h;
}

string FP_L19TransitionStabilityRow(const FP_Level19StateGateSnapshot &current,
                                    const string family,
                                    const string severity,
                                    const string previous_family,
                                    const int current_streak,
                                    const string bias_hint,
                                    const string action_hint)
{
   string stability_status = "STABILITY_SINGLE_OR_RESET";
   if(current_streak >= 5)
      stability_status = "STABILITY_PERSISTENT";
   else if(current_streak >= 3)
      stability_status = "STABILITY_STABLE";
   else if(current_streak == 2)
      stability_status = "STABILITY_REPEAT";

   string stability_quality = "STABILITY_QUALITY_OBSERVE_ONLY";
   if(severity == "TRANSITION_SEVERITY_HEALTH")
      stability_quality = "STABILITY_QUALITY_HEALTH_REVIEW";
   else if(current_streak >= 3 && severity == "TRANSITION_SEVERITY_MAJOR")
      stability_quality = "STABILITY_QUALITY_MAJOR_PERSISTENCE";
   else if(current_streak >= 3 && severity == "TRANSITION_SEVERITY_STRUCTURAL")
      stability_quality = "STABILITY_QUALITY_STRUCTURAL_PERSISTENCE";

   string r = "";
   r += FP_L19SafeCsv(FP_L19Time(current.generated_at));
   r += "," + FP_L19SafeCsv(current.version);
   r += "," + FP_L19SafeCsv(current.symbol);
   r += "," + FP_L19SafeCsv(current.period_label);
   r += "," + FP_L19SafeCsv(FP_L19Time(current.last_bar_time));
   r += "," + FP_L19SafeCsv(family);
   r += "," + FP_L19SafeCsv(severity);
   r += "," + FP_L19SafeCsv(previous_family);
   r += "," + IntegerToString(current_streak);
   r += "," + FP_L19SafeCsv(stability_status);
   r += "," + FP_L19SafeCsv(stability_quality);
   r += "," + FP_L19SafeCsv(bias_hint);
   r += "," + FP_L19SafeCsv(action_hint);
   r += "," + FP_L19SafeCsv("READ_ONLY_STABILITY_LEDGER_NO_RENDERER_MUTATION_NO_EXECUTION");
   return r;
}

bool FP_L19AppendTransitionStability(const FP_Level19StateGateConfig &cfg,
                                     const FP_Level19StateGateSnapshot &current,
                                     const string family,
                                     const string severity,
                                     const string previous_family,
                                     const int current_streak,
                                     const string bias_hint,
                                     const string action_hint,
                                     FP_Level19StateGateReport &report)
{
   if(!cfg.export_transition_stability_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL19_STATE_GATE_DEFAULT_FOLDER;
   FolderCreate(folder);

   string path = FP_L19TransitionStabilityPath(cfg);
   bool exists = FileIsExist(path);
   int handle = INVALID_HANDLE;

   if(!exists)
   {
      handle = FileOpen(path, FILE_WRITE|FILE_TXT|FILE_ANSI);
      if(handle == INVALID_HANDLE)
      {
         report.file_errors++;
         report.reason = "level19_transition_stability_create_failed";
         return false;
      }
      FileWriteString(handle, FP_L19TransitionStabilityHeader() + "\r\n");
   }
   else
   {
      handle = FileOpen(path, FILE_READ|FILE_WRITE|FILE_TXT|FILE_ANSI);
      if(handle == INVALID_HANDLE)
      {
         report.file_errors++;
         report.reason = "level19_transition_stability_open_failed";
         return false;
      }
      FileSeek(handle, 0, SEEK_END);
   }

   FileWriteString(handle, FP_L19TransitionStabilityRow(current, family, severity, previous_family,
                                                       current_streak, bias_hint, action_hint) + "\r\n");
   FileClose(handle);
   report.files_written++;
   report.transition_stability_written = true;
   return true;
}

string FP_L19RegimeLabelHeader()
{
   string h = "";
   h += "generated_at,version,symbol,period,current_closed_bar_time,regime_label,regime_quality";
   h += ",transition_family,transition_severity,stability_streak,bias_hint,action_hint,completion_status,next_step,no_touch_contract";
   return h;
}

string FP_L19RegimeLabelRow(const FP_Level19StateGateSnapshot &current,
                            const string regime_label,
                            const string regime_quality,
                            const string family,
                            const string severity,
                            const int stability_streak,
                            const string bias_hint,
                            const string action_hint,
                            const string completion_status,
                            const string next_step)
{
   string r = "";
   r += FP_L19SafeCsv(FP_L19Time(current.generated_at));
   r += "," + FP_L19SafeCsv(current.version);
   r += "," + FP_L19SafeCsv(current.symbol);
   r += "," + FP_L19SafeCsv(current.period_label);
   r += "," + FP_L19SafeCsv(FP_L19Time(current.last_bar_time));
   r += "," + FP_L19SafeCsv(regime_label);
   r += "," + FP_L19SafeCsv(regime_quality);
   r += "," + FP_L19SafeCsv(family);
   r += "," + FP_L19SafeCsv(severity);
   r += "," + IntegerToString(stability_streak);
   r += "," + FP_L19SafeCsv(bias_hint);
   r += "," + FP_L19SafeCsv(action_hint);
   r += "," + FP_L19SafeCsv(completion_status);
   r += "," + FP_L19SafeCsv(next_step);
   r += "," + FP_L19SafeCsv("READ_ONLY_REGIME_LABEL_NO_RENDERER_MUTATION_NO_EXECUTION");
   return r;
}

bool FP_L19AppendRegimeLabel(const FP_Level19StateGateConfig &cfg,
                             const FP_Level19StateGateSnapshot &current,
                             const string regime_label,
                             const string regime_quality,
                             const string family,
                             const string severity,
                             const int stability_streak,
                             const string bias_hint,
                             const string action_hint,
                             const string completion_status,
                             const string next_step,
                             FP_Level19StateGateReport &report)
{
   if(!cfg.export_regime_label_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL19_STATE_GATE_DEFAULT_FOLDER;
   FolderCreate(folder);

   string path = FP_L19RegimeLabelPath(cfg);
   bool exists = FileIsExist(path);
   int handle = INVALID_HANDLE;

   if(!exists)
   {
      handle = FileOpen(path, FILE_WRITE|FILE_TXT|FILE_ANSI);
      if(handle == INVALID_HANDLE)
      {
         report.file_errors++;
         report.reason = "level19_regime_label_create_failed";
         return false;
      }
      FileWriteString(handle, FP_L19RegimeLabelHeader() + "\r\n");
   }
   else
   {
      handle = FileOpen(path, FILE_READ|FILE_WRITE|FILE_TXT|FILE_ANSI);
      if(handle == INVALID_HANDLE)
      {
         report.file_errors++;
         report.reason = "level19_regime_label_open_failed";
         return false;
      }
      FileSeek(handle, 0, SEEK_END);
   }

   FileWriteString(handle, FP_L19RegimeLabelRow(current, regime_label, regime_quality,
                                                family, severity, stability_streak,
                                                bias_hint, action_hint, completion_status,
                                                next_step) + "\r\n");
   FileClose(handle);
   report.files_written++;
   report.regime_label_written = true;
   return true;
}

string FP_L19CompletionHeader()
{
   string h = "";
   h += "generated_at,version,symbol,period,current_closed_bar_time,completion_status,next_step";
   h += ",snapshot_enabled,closed_bar_ledger_enabled,state_delta_enabled,transition_event_enabled";
   h += ",transition_summary_enabled,transition_stability_enabled,regime_label_enabled,completion_enabled";
   h += ",panel_enabled,prints_default_off,renderer_no_touch,entry_ready_for_level20,no_touch_contract";
   return h;
}

string FP_L19CompletionRow(const FP_Level19StateGateConfig &cfg,
                           const FP_Level19StateGateSnapshot &current,
                           const string completion_status,
                           const string next_step)
{
   string r = "";
   r += FP_L19SafeCsv(FP_L19Time(current.generated_at));
   r += "," + FP_L19SafeCsv(current.version);
   r += "," + FP_L19SafeCsv(current.symbol);
   r += "," + FP_L19SafeCsv(current.period_label);
   r += "," + FP_L19SafeCsv(FP_L19Time(current.last_bar_time));
   r += "," + FP_L19SafeCsv(completion_status);
   r += "," + FP_L19SafeCsv(next_step);
   r += "," + FP_L19SafeCsv(FP_L19Bool(cfg.export_csv));
   r += "," + FP_L19SafeCsv(FP_L19Bool(cfg.export_closed_bar_ledger_csv));
   r += "," + FP_L19SafeCsv(FP_L19Bool(cfg.export_state_delta_csv));
   r += "," + FP_L19SafeCsv(FP_L19Bool(cfg.export_transition_event_csv));
   r += "," + FP_L19SafeCsv(FP_L19Bool(cfg.export_transition_summary_csv));
   r += "," + FP_L19SafeCsv(FP_L19Bool(cfg.export_transition_stability_csv));
   r += "," + FP_L19SafeCsv(FP_L19Bool(cfg.export_regime_label_csv));
   r += "," + FP_L19SafeCsv(FP_L19Bool(cfg.export_completion_csv));
   r += "," + FP_L19SafeCsv(FP_L19Bool(cfg.panel_enabled));
   r += "," + FP_L19SafeCsv("true");
   r += "," + FP_L19SafeCsv("true");
   r += "," + FP_L19SafeCsv(completion_status == "LEVEL19_COMPLETE_READY_FOR_LEVEL20_ENTRY_BRIDGE" ? "true" : "false");
   r += "," + FP_L19SafeCsv("LEVEL19_COMPLETE_OBSERVATION_ONLY_NO_RENDERER_MUTATION_NO_EXECUTION");
   return r;
}

bool FP_L19WriteCompletion(const FP_Level19StateGateConfig &cfg,
                           const FP_Level19StateGateSnapshot &current,
                           const string completion_status,
                           const string next_step,
                           FP_Level19StateGateReport &report)
{
   if(!cfg.export_completion_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL19_STATE_GATE_DEFAULT_FOLDER;
   FolderCreate(folder);

   int handle = FileOpen(FP_L19CompletionPath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "level19_completion_open_failed";
      return false;
   }

   FileWriteString(handle, FP_L19CompletionHeader() + "\r\n");
   FileWriteString(handle, FP_L19CompletionRow(cfg, current, completion_status, next_step) + "\r\n");
   FileClose(handle);
   report.files_written++;
   report.completion_written = true;
   return true;
}

#endif // __FP_STATE_GATE_EXPORT_MQH__
