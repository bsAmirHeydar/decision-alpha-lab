#ifndef __FP_RUNTIME_HEALTH_SUMMARY_EXPORT_MQH__
#define __FP_RUNTIME_HEALTH_SUMMARY_EXPORT_MQH__
#property strict

#include "FP_RuntimeHealthSummaryRules.mqh"

string FP_C05RuntimeHealthPath(const FP_Consolidation05RuntimeHealthConfig &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_CONSOLIDATION05_RUNTIME_HEALTH_DEFAULT_FOLDER;
   return folder + "\\runtime_no_send_health_summary.csv";
}

string FP_C05RuntimeHealthHeader()
{
   string h = "";
   h += "generated_at,schema_version,version,symbol,period,attempted,health_ok,health_status,health_block_reason,health_key";
   h += ",context_enabled,context_export_enabled,context_ready,context_status,context_block_reason";
   h += ",final_decision_enabled,final_decision_export_enabled,final_decision_ready,final_decision_state,final_decision_block_reason";
   h += ",normalized_enabled,normalized_export_enabled,normalized_ready,normalized_quality_status,normalized_block_reason";
   h += ",no_send_integrity_ok,expected_outputs_enabled,expected_outputs_enabled_count,expected_outputs_required_count";
   h += ",setup_state,chain_stage,blocker_layer,blocker_reason,request_id,virtual_ticket,request_direction";
   h += ",entry_price,stop_price,target_price,request_volume,realized_r_like";
   h += ",no_send_contract,no_touch_contract,execution_status";
   return h;
}

string FP_C05RuntimeHealthRowCsv(const FP_Consolidation05RuntimeHealthRow &r)
{
   string s = "";
   s += FP_C05SafeCsv(FP_C05Time(r.generated_at));
   s += "," + FP_C05SafeCsv(r.schema_version);
   s += "," + FP_C05SafeCsv(r.version);
   s += "," + FP_C05SafeCsv(r.symbol);
   s += "," + FP_C05SafeCsv(r.period_label);
   s += "," + FP_C05SafeCsv(FP_C05Bool(r.attempted));
   s += "," + FP_C05SafeCsv(FP_C05Bool(r.health_ok));
   s += "," + FP_C05SafeCsv(r.health_status);
   s += "," + FP_C05SafeCsv(r.health_block_reason);
   s += "," + FP_C05SafeCsv(r.health_key);

   s += "," + FP_C05SafeCsv(FP_C05Bool(r.context_enabled));
   s += "," + FP_C05SafeCsv(FP_C05Bool(r.context_export_enabled));
   s += "," + FP_C05SafeCsv(FP_C05Bool(r.context_ready));
   s += "," + FP_C05SafeCsv(r.context_status);
   s += "," + FP_C05SafeCsv(r.context_block_reason);

   s += "," + FP_C05SafeCsv(FP_C05Bool(r.final_decision_enabled));
   s += "," + FP_C05SafeCsv(FP_C05Bool(r.final_decision_export_enabled));
   s += "," + FP_C05SafeCsv(FP_C05Bool(r.final_decision_ready));
   s += "," + FP_C05SafeCsv(r.final_decision_state);
   s += "," + FP_C05SafeCsv(r.final_decision_block_reason);

   s += "," + FP_C05SafeCsv(FP_C05Bool(r.normalized_enabled));
   s += "," + FP_C05SafeCsv(FP_C05Bool(r.normalized_export_enabled));
   s += "," + FP_C05SafeCsv(FP_C05Bool(r.normalized_ready));
   s += "," + FP_C05SafeCsv(r.normalized_quality_status);
   s += "," + FP_C05SafeCsv(r.normalized_block_reason);

   s += "," + FP_C05SafeCsv(FP_C05Bool(r.no_send_integrity_ok));
   s += "," + FP_C05SafeCsv(FP_C05Bool(r.expected_outputs_enabled));
   s += "," + IntegerToString(r.expected_outputs_enabled_count);
   s += "," + IntegerToString(r.expected_outputs_required_count);

   s += "," + FP_C05SafeCsv(r.setup_state);
   s += "," + FP_C05SafeCsv(r.chain_stage);
   s += "," + FP_C05SafeCsv(r.blocker_layer);
   s += "," + FP_C05SafeCsv(r.blocker_reason);
   s += "," + FP_C05SafeCsv(r.request_id);
   s += "," + FP_C05SafeCsv(r.virtual_ticket);
   s += "," + FP_C05SafeCsv(r.request_direction);

   s += "," + DoubleToString(r.entry_price, _Digits);
   s += "," + DoubleToString(r.stop_price, _Digits);
   s += "," + DoubleToString(r.target_price, _Digits);
   s += "," + DoubleToString(r.request_volume, 2);
   s += "," + DoubleToString(r.realized_r_like, 4);

   s += "," + FP_C05SafeCsv(r.no_send_contract);
   s += "," + FP_C05SafeCsv(r.no_touch_contract);
   s += "," + FP_C05SafeCsv(r.execution_status);
   return s;
}

bool FP_C05ExportRuntimeHealth(const FP_Consolidation05RuntimeHealthConfig &cfg,
                               const FP_Consolidation05RuntimeHealthRow &row,
                               FP_Consolidation05RuntimeHealthReport &report)
{
   if(!cfg.export_csv || !cfg.write_latest_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_CONSOLIDATION05_RUNTIME_HEALTH_DEFAULT_FOLDER;
   FolderCreate(folder);

   int handle = FileOpen(FP_C05RuntimeHealthPath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "consolidation05_runtime_health_export_open_failed";
      return false;
   }

   FileWriteString(handle, FP_C05RuntimeHealthHeader() + "\r\n");
   FileWriteString(handle, FP_C05RuntimeHealthRowCsv(row) + "\r\n");
   FileClose(handle);

   report.files_written++;
   report.latest_written = true;
   return true;
}

#endif // __FP_RUNTIME_HEALTH_SUMMARY_EXPORT_MQH__
