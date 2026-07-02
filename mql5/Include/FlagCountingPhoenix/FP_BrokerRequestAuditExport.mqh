#ifndef __FP_BROKER_REQUEST_AUDIT_EXPORT_MQH__
#define __FP_BROKER_REQUEST_AUDIT_EXPORT_MQH__
#property strict

#include "FP_BrokerRequestAuditRules.mqh"

string FP_L28BrokerRequestAuditPath(const FP_Level28BrokerRequestAuditConfig &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL28_BROKER_REQUEST_AUDIT_DEFAULT_FOLDER;
   return folder + "\\state_gate_level28_broker_request_audit.csv";
}

string FP_L28BrokerRequestAuditLatestPath(const FP_Level28BrokerRequestAuditConfig &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL28_BROKER_REQUEST_AUDIT_DEFAULT_FOLDER;
   return folder + "\\latest_state_gate_level28_broker_request_audit.csv";
}

string FP_L28BrokerRequestAuditHeader()
{
   string h = "";
   h += "generated_at,version,symbol,period,attempted,audit_passed,audit_written,latest_written,duplicate_skipped,audit_status,audit_block_reason,audit_id,audit_key";
   h += ",request_id,request_key,request_built,dry_run_only,dry_run_status,dry_run_block_reason";
   h += ",validator_passed,validator_status,validator_block_reason,validator_key";
   h += ",safety_gate_passed,safety_gate_status,safety_gate_block_reason";
   h += ",intent_allowed,intent_id,intent_status";
   h += ",request_order_type,request_direction,request_volume,request_price,request_sl,request_tp";
   h += ",dry_run_only_ok,zero_volume_ok,no_send_contract_ok,request_validator_coherence_ok,safety_intent_coherence_ok,ledger_runtime_seen";
   h += ",ledger_sequence_current,ledger_last_request_key,validator_readiness,request_chain_state,no_send_contract,no_touch_contract,execution_status";
   return h;
}

string FP_L28BrokerRequestAuditRowCsv(const FP_Level28BrokerRequestAuditRow &r)
{
   string s = "";
   s += FP_L28SafeCsv(FP_L28Time(r.generated_at));
   s += "," + FP_L28SafeCsv(r.version);
   s += "," + FP_L28SafeCsv(r.symbol);
   s += "," + FP_L28SafeCsv(r.period_label);
   s += "," + FP_L28SafeCsv(FP_L28Bool(r.attempted));
   s += "," + FP_L28SafeCsv(FP_L28Bool(r.audit_passed));
   s += "," + FP_L28SafeCsv(FP_L28Bool(r.audit_written));
   s += "," + FP_L28SafeCsv(FP_L28Bool(r.latest_written));
   s += "," + FP_L28SafeCsv(FP_L28Bool(r.duplicate_skipped));
   s += "," + FP_L28SafeCsv(r.audit_status);
   s += "," + FP_L28SafeCsv(r.audit_block_reason);
   s += "," + FP_L28SafeCsv(r.audit_id);
   s += "," + FP_L28SafeCsv(r.audit_key);

   s += "," + FP_L28SafeCsv(r.request_id);
   s += "," + FP_L28SafeCsv(r.request_key);
   s += "," + FP_L28SafeCsv(FP_L28Bool(r.request_built));
   s += "," + FP_L28SafeCsv(FP_L28Bool(r.dry_run_only));
   s += "," + FP_L28SafeCsv(r.dry_run_status);
   s += "," + FP_L28SafeCsv(r.dry_run_block_reason);

   s += "," + FP_L28SafeCsv(FP_L28Bool(r.validator_passed));
   s += "," + FP_L28SafeCsv(r.validator_status);
   s += "," + FP_L28SafeCsv(r.validator_block_reason);
   s += "," + FP_L28SafeCsv(r.validator_key);

   s += "," + FP_L28SafeCsv(FP_L28Bool(r.safety_gate_passed));
   s += "," + FP_L28SafeCsv(r.safety_gate_status);
   s += "," + FP_L28SafeCsv(r.safety_gate_block_reason);

   s += "," + FP_L28SafeCsv(FP_L28Bool(r.intent_allowed));
   s += "," + FP_L28SafeCsv(r.intent_id);
   s += "," + FP_L28SafeCsv(r.intent_status);

   s += "," + FP_L28SafeCsv(r.request_order_type);
   s += "," + FP_L28SafeCsv(r.request_direction);
   s += "," + DoubleToString(r.request_volume, 2);
   s += "," + DoubleToString(r.request_price, _Digits);
   s += "," + DoubleToString(r.request_sl, _Digits);
   s += "," + DoubleToString(r.request_tp, _Digits);

   s += "," + FP_L28SafeCsv(FP_L28Bool(r.dry_run_only_ok));
   s += "," + FP_L28SafeCsv(FP_L28Bool(r.zero_volume_ok));
   s += "," + FP_L28SafeCsv(FP_L28Bool(r.no_send_contract_ok));
   s += "," + FP_L28SafeCsv(FP_L28Bool(r.request_validator_coherence_ok));
   s += "," + FP_L28SafeCsv(FP_L28Bool(r.safety_intent_coherence_ok));
   s += "," + FP_L28SafeCsv(FP_L28Bool(r.ledger_runtime_seen));

   s += "," + IntegerToString(r.ledger_sequence_current);
   s += "," + FP_L28SafeCsv(r.ledger_last_request_key);
   s += "," + FP_L28SafeCsv(r.validator_readiness);
   s += "," + FP_L28SafeCsv(r.request_chain_state);
   s += "," + FP_L28SafeCsv(r.no_send_contract);
   s += "," + FP_L28SafeCsv(r.no_touch_contract);
   s += "," + FP_L28SafeCsv(r.execution_status);
   return s;
}

bool FP_L28WriteLatestBrokerRequestAudit(const FP_Level28BrokerRequestAuditConfig &cfg,
                                         const FP_Level28BrokerRequestAuditRow &row,
                                         FP_Level28BrokerRequestAuditReport &report)
{
   if(!cfg.export_csv)
      return true;

    if(!cfg.write_latest_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL28_BROKER_REQUEST_AUDIT_DEFAULT_FOLDER;
   FolderCreate(folder);

   int handle = FileOpen(FP_L28BrokerRequestAuditLatestPath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "level28_broker_request_audit_latest_open_failed";
      return false;
   }

   FileWriteString(handle, FP_L28BrokerRequestAuditHeader() + "\r\n");
   FileWriteString(handle, FP_L28BrokerRequestAuditRowCsv(row) + "\r\n");
   FileClose(handle);

   report.files_written++;
   report.latest_written = true;
   return true;
}

bool FP_L28AppendBrokerRequestAudit(const FP_Level28BrokerRequestAuditConfig &cfg,
                                    const FP_Level28BrokerRequestAuditRow &row,
                                    FP_Level28BrokerRequestAuditReport &report)
{
   if(!cfg.export_csv)
      return true;

    if(!cfg.append_audit_csv)
      return true;

   if(row.duplicate_skipped)
   {
      report.duplicate_skipped = true;
      return true;
   }

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL28_BROKER_REQUEST_AUDIT_DEFAULT_FOLDER;
   FolderCreate(folder);

   string path = FP_L28BrokerRequestAuditPath(cfg);
   bool exists = FileIsExist(path);
   int handle = INVALID_HANDLE;

   if(!exists)
   {
      handle = FileOpen(path, FILE_WRITE|FILE_TXT|FILE_ANSI);
      if(handle == INVALID_HANDLE)
      {
         report.file_errors++;
         report.reason = "level28_broker_request_audit_create_failed";
         return false;
      }
      FileWriteString(handle, FP_L28BrokerRequestAuditHeader() + "\r\n");
   }
   else
   {
      handle = FileOpen(path, FILE_READ|FILE_WRITE|FILE_TXT|FILE_ANSI);
      if(handle == INVALID_HANDLE)
      {
         report.file_errors++;
         report.reason = "level28_broker_request_audit_open_failed";
         return false;
      }
      FileSeek(handle, 0, SEEK_END);
   }

   FileWriteString(handle, FP_L28BrokerRequestAuditRowCsv(row) + "\r\n");
   FileClose(handle);

   report.files_written++;
   report.audit_written = true;
   return true;
}

#endif // __FP_BROKER_REQUEST_AUDIT_EXPORT_MQH__
