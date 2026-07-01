#ifndef __FP_ENTRY_BRIDGE_EXPORT_MQH__
#define __FP_ENTRY_BRIDGE_EXPORT_MQH__
#property strict

#include "FP_EntryBridgeRules.mqh"

string FP_L20EntryBridgePath(const FP_Level20EntryBridgeConfig &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL20_ENTRY_BRIDGE_DEFAULT_FOLDER;
   return folder + "\\state_gate_level20_entry_bridge.csv";
}

string FP_L20EntryBridgeHeader()
{
   string h = "";
   h += "generated_at,version,symbol,period,attempted,ready,readiness_status,block_reason,bridge_status,bridge_key";
   h += ",source_kind,source_id,source_level,source_L,direction,y_state_label,y_context_label";
   h += ",entry_anchor_kind,entry_anchor_time,entry_anchor_price,entry_anchor_node_id,entry_anchor_id";
   h += ",invalidation_anchor_kind,invalidation_anchor_time,invalidation_anchor_price,invalidation_anchor_node_id,invalidation_anchor_id";
   h += ",destination_anchor_kind,destination_anchor_time,destination_anchor_price,destination_anchor_node_id,destination_anchor_id";
   h += ",current_close,risk_distance,reward_distance,rr_like,min_rr_required";
   h += ",timebase_ok,render_health_ok,validation_health_ok,no_touch_contract,execution_status";
   return h;
}

string FP_L20EntryBridgeRowCsv(const FP_Level20EntryBridgeRow &r)
{
   string s = "";
   s += FP_L20SafeCsv(FP_L20Time(r.generated_at));
   s += "," + FP_L20SafeCsv(r.version);
   s += "," + FP_L20SafeCsv(r.symbol);
   s += "," + FP_L20SafeCsv(r.period_label);
   s += "," + FP_L20SafeCsv(FP_L20Bool(r.attempted));
   s += "," + FP_L20SafeCsv(FP_L20Bool(r.ready));
   s += "," + FP_L20SafeCsv(r.readiness_status);
   s += "," + FP_L20SafeCsv(r.block_reason);
   s += "," + FP_L20SafeCsv(r.bridge_status);
   s += "," + FP_L20SafeCsv(r.bridge_key);

   s += "," + FP_L20SafeCsv(r.source_kind);
   s += "," + FP_L20SafeCsv(r.source_id);
   s += "," + IntegerToString(r.source_level);
   s += "," + IntegerToString(r.source_L);
   s += "," + FP_L20SafeCsv(FP_L20DirectionLabel(r.direction));
   s += "," + FP_L20SafeCsv(r.y_state_label);
   s += "," + FP_L20SafeCsv(r.y_context_label);

   s += "," + FP_L20SafeCsv(r.entry_anchor_kind);
   s += "," + FP_L20SafeCsv(FP_L20Time(r.entry_anchor_time));
   s += "," + DoubleToString(r.entry_anchor_price, _Digits);
   s += "," + IntegerToString(r.entry_anchor_node_id);
   s += "," + FP_L20SafeCsv(r.entry_anchor_id);

   s += "," + FP_L20SafeCsv(r.invalidation_anchor_kind);
   s += "," + FP_L20SafeCsv(FP_L20Time(r.invalidation_anchor_time));
   s += "," + DoubleToString(r.invalidation_anchor_price, _Digits);
   s += "," + IntegerToString(r.invalidation_anchor_node_id);
   s += "," + FP_L20SafeCsv(r.invalidation_anchor_id);

   s += "," + FP_L20SafeCsv(r.destination_anchor_kind);
   s += "," + FP_L20SafeCsv(FP_L20Time(r.destination_anchor_time));
   s += "," + DoubleToString(r.destination_anchor_price, _Digits);
   s += "," + IntegerToString(r.destination_anchor_node_id);
   s += "," + FP_L20SafeCsv(r.destination_anchor_id);

   s += "," + DoubleToString(r.current_close, _Digits);
   s += "," + DoubleToString(r.risk_distance, _Digits);
   s += "," + DoubleToString(r.reward_distance, _Digits);
   s += "," + DoubleToString(r.rr_like, 4);
   s += "," + DoubleToString(r.min_rr_required, 4);

   s += "," + FP_L20SafeCsv(FP_L20Bool(r.timebase_ok));
   s += "," + FP_L20SafeCsv(FP_L20Bool(r.render_health_ok));
   s += "," + FP_L20SafeCsv(FP_L20Bool(r.validation_health_ok));
   s += "," + FP_L20SafeCsv(r.no_touch_contract);
   s += "," + FP_L20SafeCsv(r.execution_status);
   return s;
}

bool FP_L20ExportEntryBridge(const FP_Level20EntryBridgeConfig &cfg,
                             const FP_Level20EntryBridgeRow &row,
                             FP_Level20EntryBridgeReport &report)
{
   if(!cfg.export_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL20_ENTRY_BRIDGE_DEFAULT_FOLDER;
   FolderCreate(folder);

   int handle = FileOpen(FP_L20EntryBridgePath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "level20_entry_bridge_export_open_failed";
      return false;
   }

   FileWriteString(handle, FP_L20EntryBridgeHeader() + "\r\n");
   FileWriteString(handle, FP_L20EntryBridgeRowCsv(row) + "\r\n");
   FileClose(handle);

   report.files_written++;
   report.bridge_written = true;
   return true;
}

#endif // __FP_ENTRY_BRIDGE_EXPORT_MQH__
