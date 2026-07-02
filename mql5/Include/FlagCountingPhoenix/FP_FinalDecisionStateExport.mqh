#ifndef __FP_FINAL_DECISION_STATE_EXPORT_MQH__
#define __FP_FINAL_DECISION_STATE_EXPORT_MQH__
#property strict

#include "FP_FinalDecisionStateRules.mqh"

string FP_C02FinalDecisionPath(const FP_Consolidation02FinalDecisionConfig &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_CONSOLIDATION02_FINAL_DECISION_DEFAULT_FOLDER;
   return folder + "\\final_no_send_decision_state.csv";
}

string FP_C02FinalDecisionHeader()
{
   string h = "";
   h += "generated_at,version,symbol,period,attempted,decision_ready,decision_state,decision_block_reason,decision_key";
   h += ",setup_state,chain_stage,next_action_hint";
   h += ",context_ready,context_status,context_block_reason";
   h += ",entry_bridge_ready,paper_intent_allowed,safety_gate_passed,dry_run_request_built,validator_passed,audit_passed,adapter_registered,lifecycle_tracked";
   h += ",request_id,request_key,virtual_ticket,request_direction,entry_price,stop_price,target_price,request_volume";
   h += ",lifecycle_status,lifecycle_block_reason,paper_order_state,realized_r_like";
   h += ",blocker_layer,blocker_status,blocker_reason,no_send_integrity_ok";
   h += ",no_send_contract,no_touch_contract,execution_status";
   return h;
}

string FP_C02FinalDecisionRowCsv(const FP_Consolidation02FinalDecisionRow &r)
{
   string s = "";
   s += FP_C02SafeCsv(FP_C02Time(r.generated_at));
   s += "," + FP_C02SafeCsv(r.version);
   s += "," + FP_C02SafeCsv(r.symbol);
   s += "," + FP_C02SafeCsv(r.period_label);
   s += "," + FP_C02SafeCsv(FP_C02Bool(r.attempted));
   s += "," + FP_C02SafeCsv(FP_C02Bool(r.decision_ready));
   s += "," + FP_C02SafeCsv(r.decision_state);
   s += "," + FP_C02SafeCsv(r.decision_block_reason);
   s += "," + FP_C02SafeCsv(r.decision_key);

   s += "," + FP_C02SafeCsv(r.setup_state);
   s += "," + FP_C02SafeCsv(r.chain_stage);
   s += "," + FP_C02SafeCsv(r.next_action_hint);

   s += "," + FP_C02SafeCsv(FP_C02Bool(r.context_ready));
   s += "," + FP_C02SafeCsv(r.context_status);
   s += "," + FP_C02SafeCsv(r.context_block_reason);

   s += "," + FP_C02SafeCsv(FP_C02Bool(r.entry_bridge_ready));
   s += "," + FP_C02SafeCsv(FP_C02Bool(r.paper_intent_allowed));
   s += "," + FP_C02SafeCsv(FP_C02Bool(r.safety_gate_passed));
   s += "," + FP_C02SafeCsv(FP_C02Bool(r.dry_run_request_built));
   s += "," + FP_C02SafeCsv(FP_C02Bool(r.validator_passed));
   s += "," + FP_C02SafeCsv(FP_C02Bool(r.audit_passed));
   s += "," + FP_C02SafeCsv(FP_C02Bool(r.adapter_registered));
   s += "," + FP_C02SafeCsv(FP_C02Bool(r.lifecycle_tracked));

   s += "," + FP_C02SafeCsv(r.request_id);
   s += "," + FP_C02SafeCsv(r.request_key);
   s += "," + FP_C02SafeCsv(r.virtual_ticket);
   s += "," + FP_C02SafeCsv(r.request_direction);
   s += "," + DoubleToString(r.entry_price, _Digits);
   s += "," + DoubleToString(r.stop_price, _Digits);
   s += "," + DoubleToString(r.target_price, _Digits);
   s += "," + DoubleToString(r.request_volume, 2);

   s += "," + FP_C02SafeCsv(r.lifecycle_status);
   s += "," + FP_C02SafeCsv(r.lifecycle_block_reason);
   s += "," + FP_C02SafeCsv(r.paper_order_state);
   s += "," + DoubleToString(r.realized_r_like, 4);

   s += "," + FP_C02SafeCsv(r.blocker_layer);
   s += "," + FP_C02SafeCsv(r.blocker_status);
   s += "," + FP_C02SafeCsv(r.blocker_reason);
   s += "," + FP_C02SafeCsv(FP_C02Bool(r.no_send_integrity_ok));

   s += "," + FP_C02SafeCsv(r.no_send_contract);
   s += "," + FP_C02SafeCsv(r.no_touch_contract);
   s += "," + FP_C02SafeCsv(r.execution_status);
   return s;
}

bool FP_C02ExportFinalDecision(const FP_Consolidation02FinalDecisionConfig &cfg,
                               const FP_Consolidation02FinalDecisionRow &row,
                               FP_Consolidation02FinalDecisionReport &report)
{
   if(!cfg.export_csv || !cfg.write_latest_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_CONSOLIDATION02_FINAL_DECISION_DEFAULT_FOLDER;
   FolderCreate(folder);

   int handle = FileOpen(FP_C02FinalDecisionPath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "consolidation02_final_decision_export_open_failed";
      return false;
   }

   FileWriteString(handle, FP_C02FinalDecisionHeader() + "\r\n");
   FileWriteString(handle, FP_C02FinalDecisionRowCsv(row) + "\r\n");
   FileClose(handle);

   report.files_written++;
   report.latest_written = true;
   return true;
}

#endif // __FP_FINAL_DECISION_STATE_EXPORT_MQH__
