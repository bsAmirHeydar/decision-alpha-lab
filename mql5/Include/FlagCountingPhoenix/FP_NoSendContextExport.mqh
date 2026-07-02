#ifndef __FP_NO_SEND_CONTEXT_EXPORT_MQH__
#define __FP_NO_SEND_CONTEXT_EXPORT_MQH__
#property strict

#include "FP_NoSendContextRules.mqh"

string FP_C01NoSendContextPath(const FP_Consolidation01NoSendContextConfig &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_CONSOLIDATION01_NO_SEND_CONTEXT_DEFAULT_FOLDER;
   return folder + "\\latest_consolidation_01_no_send_context.csv";
}

string FP_C01NoSendContextHeader()
{
   string h = "";
   h += "generated_at,version,symbol,period,attempted,context_ready,context_status,context_block_reason,context_key";
   h += ",has_entry_bridge,has_paper_intent,has_safety_gate,has_dry_run,has_validator,has_ledger,has_audit,has_adapter,has_lifecycle";
   h += ",entry_bridge_ready,entry_bridge_status";
   h += ",paper_intent_allowed,paper_intent_status";
   h += ",safety_gate_passed,safety_gate_status,safety_gate_block_reason";
   h += ",dry_run_request_built,dry_run_status,request_id,request_key";
   h += ",validator_passed,validator_status,validator_block_reason";
   h += ",audit_passed,audit_status,audit_block_reason";
   h += ",adapter_registered,adapter_status,adapter_block_reason,virtual_ticket";
   h += ",lifecycle_tracked,lifecycle_status,lifecycle_block_reason,paper_order_state,realized_r_like";
   h += ",request_direction,request_price,request_sl,request_tp,request_volume";
   h += ",no_send_contract,no_touch_contract,execution_status";
   return h;
}

string FP_C01NoSendContextRowCsv(const FP_Consolidation01NoSendContextRow &r)
{
   string s = "";
   s += FP_C01SafeCsv(FP_C01Time(r.generated_at));
   s += "," + FP_C01SafeCsv(r.version);
   s += "," + FP_C01SafeCsv(r.symbol);
   s += "," + FP_C01SafeCsv(r.period_label);
   s += "," + FP_C01SafeCsv(FP_C01Bool(r.attempted));
   s += "," + FP_C01SafeCsv(FP_C01Bool(r.context_ready));
   s += "," + FP_C01SafeCsv(r.context_status);
   s += "," + FP_C01SafeCsv(r.context_block_reason);
   s += "," + FP_C01SafeCsv(r.context_key);

   s += "," + FP_C01SafeCsv(FP_C01Bool(r.has_entry_bridge));
   s += "," + FP_C01SafeCsv(FP_C01Bool(r.has_paper_intent));
   s += "," + FP_C01SafeCsv(FP_C01Bool(r.has_safety_gate));
   s += "," + FP_C01SafeCsv(FP_C01Bool(r.has_dry_run));
   s += "," + FP_C01SafeCsv(FP_C01Bool(r.has_validator));
   s += "," + FP_C01SafeCsv(FP_C01Bool(r.has_ledger));
   s += "," + FP_C01SafeCsv(FP_C01Bool(r.has_audit));
   s += "," + FP_C01SafeCsv(FP_C01Bool(r.has_adapter));
   s += "," + FP_C01SafeCsv(FP_C01Bool(r.has_lifecycle));

   s += "," + FP_C01SafeCsv(FP_C01Bool(r.entry_bridge_ready));
   s += "," + FP_C01SafeCsv(r.entry_bridge_status);

   s += "," + FP_C01SafeCsv(FP_C01Bool(r.paper_intent_allowed));
   s += "," + FP_C01SafeCsv(r.paper_intent_status);

   s += "," + FP_C01SafeCsv(FP_C01Bool(r.safety_gate_passed));
   s += "," + FP_C01SafeCsv(r.safety_gate_status);
   s += "," + FP_C01SafeCsv(r.safety_gate_block_reason);

   s += "," + FP_C01SafeCsv(FP_C01Bool(r.dry_run_request_built));
   s += "," + FP_C01SafeCsv(r.dry_run_status);
   s += "," + FP_C01SafeCsv(r.request_id);
   s += "," + FP_C01SafeCsv(r.request_key);

   s += "," + FP_C01SafeCsv(FP_C01Bool(r.validator_passed));
   s += "," + FP_C01SafeCsv(r.validator_status);
   s += "," + FP_C01SafeCsv(r.validator_block_reason);

   s += "," + FP_C01SafeCsv(FP_C01Bool(r.audit_passed));
   s += "," + FP_C01SafeCsv(r.audit_status);
   s += "," + FP_C01SafeCsv(r.audit_block_reason);

   s += "," + FP_C01SafeCsv(FP_C01Bool(r.adapter_registered));
   s += "," + FP_C01SafeCsv(r.adapter_status);
   s += "," + FP_C01SafeCsv(r.adapter_block_reason);
   s += "," + FP_C01SafeCsv(r.virtual_ticket);

   s += "," + FP_C01SafeCsv(FP_C01Bool(r.lifecycle_tracked));
   s += "," + FP_C01SafeCsv(r.lifecycle_status);
   s += "," + FP_C01SafeCsv(r.lifecycle_block_reason);
   s += "," + FP_C01SafeCsv(r.paper_order_state);
   s += "," + DoubleToString(r.realized_r_like, 4);

   s += "," + FP_C01SafeCsv(r.request_direction);
   s += "," + DoubleToString(r.request_price, _Digits);
   s += "," + DoubleToString(r.request_sl, _Digits);
   s += "," + DoubleToString(r.request_tp, _Digits);
   s += "," + DoubleToString(r.request_volume, 2);

   s += "," + FP_C01SafeCsv(r.no_send_contract);
   s += "," + FP_C01SafeCsv(r.no_touch_contract);
   s += "," + FP_C01SafeCsv(r.execution_status);
   return s;
}

bool FP_C01ExportNoSendContext(const FP_Consolidation01NoSendContextConfig &cfg,
                               const FP_Consolidation01NoSendContextRow &row,
                               FP_Consolidation01NoSendContextReport &report)
{
   if(!cfg.export_csv || !cfg.write_latest_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_CONSOLIDATION01_NO_SEND_CONTEXT_DEFAULT_FOLDER;
   FolderCreate(folder);

   int handle = FileOpen(FP_C01NoSendContextPath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "consolidation01_no_send_context_export_open_failed";
      return false;
   }

   FileWriteString(handle, FP_C01NoSendContextHeader() + "\r\n");
   FileWriteString(handle, FP_C01NoSendContextRowCsv(row) + "\r\n");
   FileClose(handle);

   report.files_written++;
   report.latest_written = true;
   return true;
}

#endif // __FP_NO_SEND_CONTEXT_EXPORT_MQH__
