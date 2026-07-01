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

#endif // __FP_STATE_GATE_EXPORT_MQH__
