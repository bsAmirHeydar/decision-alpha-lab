#ifndef __FP_FINAL_CSV_NORMALIZATION_EXPORT_MQH__
#define __FP_FINAL_CSV_NORMALIZATION_EXPORT_MQH__
#property strict

#include "FP_FinalCsvNormalizationRules.mqh"

string FP_C04FinalCsvNormalizationPath(const FP_Consolidation04FinalCsvNormalizationConfig &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_CONSOLIDATION04_FINAL_CSV_NORMALIZATION_DEFAULT_FOLDER;
   return folder + "\\final_no_send_decision_state_normalized.csv";
}

string FP_C04FinalCsvNormalizationHeader()
{
   string h = "";
   h += "generated_at,schema_version,version,symbol,period";
   h += ",attempted_i,decision_ready_i,context_ready_i,no_send_integrity_i";
   h += ",entry_bridge_ready_i,paper_intent_allowed_i,safety_gate_passed_i,dry_run_request_built_i,validator_passed_i,audit_passed_i,adapter_registered_i,lifecycle_tracked_i";
   h += ",decision_state,decision_block_reason,setup_state,chain_stage,next_action_hint,blocker_layer,blocker_reason";
   h += ",request_id,request_key,virtual_ticket,direction_label,direction_sign";
   h += ",entry_price,stop_price,target_price,request_volume,risk_distance,reward_distance,rr_like";
   h += ",lifecycle_status,paper_order_state,realized_r_like,normalized_quality_status,normalized_block_reason";
   h += ",no_send_contract,no_touch_contract,execution_status";
   return h;
}

string FP_C04FinalCsvNormalizationRowCsv(const FP_Consolidation04FinalCsvNormalizationRow &r)
{
   string s = "";
   s += FP_C04SafeCsv(FP_C04Time(r.generated_at));
   s += "," + FP_C04SafeCsv(r.schema_version);
   s += "," + FP_C04SafeCsv(r.version);
   s += "," + FP_C04SafeCsv(r.symbol);
   s += "," + FP_C04SafeCsv(r.period_label);

   s += "," + IntegerToString(r.attempted_i);
   s += "," + IntegerToString(r.decision_ready_i);
   s += "," + IntegerToString(r.context_ready_i);
   s += "," + IntegerToString(r.no_send_integrity_i);

   s += "," + IntegerToString(r.entry_bridge_ready_i);
   s += "," + IntegerToString(r.paper_intent_allowed_i);
   s += "," + IntegerToString(r.safety_gate_passed_i);
   s += "," + IntegerToString(r.dry_run_request_built_i);
   s += "," + IntegerToString(r.validator_passed_i);
   s += "," + IntegerToString(r.audit_passed_i);
   s += "," + IntegerToString(r.adapter_registered_i);
   s += "," + IntegerToString(r.lifecycle_tracked_i);

   s += "," + FP_C04SafeCsv(r.decision_state);
   s += "," + FP_C04SafeCsv(r.decision_block_reason);
   s += "," + FP_C04SafeCsv(r.setup_state);
   s += "," + FP_C04SafeCsv(r.chain_stage);
   s += "," + FP_C04SafeCsv(r.next_action_hint);
   s += "," + FP_C04SafeCsv(r.blocker_layer);
   s += "," + FP_C04SafeCsv(r.blocker_reason);

   s += "," + FP_C04SafeCsv(r.request_id);
   s += "," + FP_C04SafeCsv(r.request_key);
   s += "," + FP_C04SafeCsv(r.virtual_ticket);
   s += "," + FP_C04SafeCsv(r.direction_label);
   s += "," + IntegerToString(r.direction_sign);

   s += "," + DoubleToString(r.entry_price, _Digits);
   s += "," + DoubleToString(r.stop_price, _Digits);
   s += "," + DoubleToString(r.target_price, _Digits);
   s += "," + DoubleToString(r.request_volume, 2);
   s += "," + DoubleToString(r.risk_distance, _Digits);
   s += "," + DoubleToString(r.reward_distance, _Digits);
   s += "," + DoubleToString(r.rr_like, 4);

   s += "," + FP_C04SafeCsv(r.lifecycle_status);
   s += "," + FP_C04SafeCsv(r.paper_order_state);
   s += "," + DoubleToString(r.realized_r_like, 4);
   s += "," + FP_C04SafeCsv(r.normalized_quality_status);
   s += "," + FP_C04SafeCsv(r.normalized_block_reason);

   s += "," + FP_C04SafeCsv(r.no_send_contract);
   s += "," + FP_C04SafeCsv(r.no_touch_contract);
   s += "," + FP_C04SafeCsv(r.execution_status);
   return s;
}

bool FP_C04ExportFinalCsvNormalization(const FP_Consolidation04FinalCsvNormalizationConfig &cfg,
                                       const FP_Consolidation04FinalCsvNormalizationRow &row,
                                       FP_Consolidation04FinalCsvNormalizationReport &report)
{
   if(!cfg.export_csv || !cfg.write_latest_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_CONSOLIDATION04_FINAL_CSV_NORMALIZATION_DEFAULT_FOLDER;
   FolderCreate(folder);

   int handle = FileOpen(FP_C04FinalCsvNormalizationPath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "consolidation04_final_csv_normalization_export_open_failed";
      return false;
   }

   FileWriteString(handle, FP_C04FinalCsvNormalizationHeader() + "\r\n");
   FileWriteString(handle, FP_C04FinalCsvNormalizationRowCsv(row) + "\r\n");
   FileClose(handle);

   report.files_written++;
   report.latest_written = true;
   return true;
}

#endif // __FP_FINAL_CSV_NORMALIZATION_EXPORT_MQH__
