#ifndef __FP_HOOK_PHASE10_EXPORT_MQH__
#define __FP_HOOK_PHASE10_EXPORT_MQH__
#property strict

#include "FP_HookPhase10Visual.mqh"

string FP_HookP10SafeCsv(string s)
{
   StringReplace(s, "\"", "\"\"");
   return "\"" + s + "\"";
}

string FP_HookP10Folder(const FP_HookPhase10Config &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_HOOK_P10_DEFAULT_FOLDER;
   return folder;
}

string FP_HookP10SummaryPath(const FP_HookPhase10Config &cfg)
{
   return FP_HookP10Folder(cfg) + "\\hook_phase10_freeze_summary.csv";
}

string FP_HookP10ContractsPath(const FP_HookPhase10Config &cfg)
{
   return FP_HookP10Folder(cfg) + "\\hook_phase10_contract_checks.csv";
}

string FP_HookP10SchemaPath(const FP_HookPhase10Config &cfg)
{
   return FP_HookP10Folder(cfg) + "\\hook_phase10_training_schema.csv";
}

string FP_HookP10ManifestPath(const FP_HookPhase10Config &cfg)
{
   return FP_HookP10Folder(cfg) + "\\hook_phase10_freeze_manifest.csv";
}

string FP_HookP10SummaryHeader()
{
   return "schema_version,version,contract_id,symbol,period,display_family,view_profile,freeze_mode,status,ok,freeze_ready,reason,contract_checks_total,contract_checks_required,contract_checks_passed,contract_checks_failed,contract_checks_skipped,info_count,warning_count,blocker_count,failed_required_count,phase08_ok,phase08_status,phase08_reason,phase09_ok,phase09_status,phase09_reason,p06_records_total,p06_xy_closed_count,p06_elite_count,p06_high_count,p06_medium_count,p06_low_count,p06_invalid_count,p06_high_or_elite_count,training_schema_columns,files_written,file_errors";
}

string FP_HookP10SummaryRow(const string symbol,
                            const ENUM_TIMEFRAMES period,
                            const FP_HookPhase10Report &r)
{
   string row = "";
   row += FP_HookP10SafeCsv(FP_HOOK_P10_SCHEMA_VERSION);
   row += "," + FP_HookP10SafeCsv(FP_HOOK_P10_VERSION);
   row += "," + FP_HookP10SafeCsv(r.contract_id);
   row += "," + FP_HookP10SafeCsv(symbol);
   row += "," + FP_HookP10SafeCsv(EnumToString(period));
   row += "," + FP_HookP10SafeCsv(FP_HookP01DisplayFamilyName(r.display_family));
   row += "," + FP_HookP10SafeCsv(FP_HookP07ViewProfileName(r.view_profile));
   row += "," + FP_HookP10SafeCsv(FP_HookP10FreezeModeName(r.freeze_mode));
   row += "," + FP_HookP10SafeCsv(r.status);
   row += "," + FP_HookP10SafeCsv(FP_HookP10BoolName(r.ok));
   row += "," + FP_HookP10SafeCsv(FP_HookP10BoolName(r.freeze_ready));
   row += "," + FP_HookP10SafeCsv(r.reason);
   row += "," + IntegerToString(r.contract_checks_total);
   row += "," + IntegerToString(r.contract_checks_required);
   row += "," + IntegerToString(r.contract_checks_passed);
   row += "," + IntegerToString(r.contract_checks_failed);
   row += "," + IntegerToString(r.contract_checks_skipped);
   row += "," + IntegerToString(r.info_count);
   row += "," + IntegerToString(r.warning_count);
   row += "," + IntegerToString(r.blocker_count);
   row += "," + IntegerToString(r.failed_required_count);
   row += "," + FP_HookP10SafeCsv(FP_HookP10BoolName(r.phase08_ok));
   row += "," + FP_HookP10SafeCsv(r.phase08_status);
   row += "," + FP_HookP10SafeCsv(r.phase08_reason);
   row += "," + FP_HookP10SafeCsv(FP_HookP10BoolName(r.phase09_ok));
   row += "," + FP_HookP10SafeCsv(r.phase09_status);
   row += "," + FP_HookP10SafeCsv(r.phase09_reason);
   row += "," + IntegerToString(r.p06_records_total);
   row += "," + IntegerToString(r.p06_xy_closed_count);
   row += "," + IntegerToString(r.p06_elite_count);
   row += "," + IntegerToString(r.p06_high_count);
   row += "," + IntegerToString(r.p06_medium_count);
   row += "," + IntegerToString(r.p06_low_count);
   row += "," + IntegerToString(r.p06_invalid_count);
   row += "," + IntegerToString(r.p06_high_or_elite_count);
   row += "," + IntegerToString(r.training_schema_columns);
   row += "," + IntegerToString(r.files_written);
   row += "," + IntegerToString(r.file_errors);
   return row;
}

string FP_HookP10ContractHeader()
{
   return "schema_version,version,contract_id,contract_code,severity,required,state,passed,evidence,recommendation";
}

string FP_HookP10ContractRowCsv(const string contract_id,
                                const FP_HookPhase10ContractRow &r)
{
   string row = "";
   row += FP_HookP10SafeCsv(FP_HOOK_P10_SCHEMA_VERSION);
   row += "," + FP_HookP10SafeCsv(FP_HOOK_P10_VERSION);
   row += "," + FP_HookP10SafeCsv(contract_id);
   row += "," + FP_HookP10SafeCsv(r.contract_code);
   row += "," + FP_HookP10SafeCsv(FP_HookP10SeverityName(r.severity));
   row += "," + FP_HookP10SafeCsv(FP_HookP10BoolName(r.required));
   row += "," + FP_HookP10SafeCsv(FP_HookP10ContractStateName(r.state));
   row += "," + FP_HookP10SafeCsv(FP_HookP10BoolName(r.passed));
   row += "," + FP_HookP10SafeCsv(r.evidence);
   row += "," + FP_HookP10SafeCsv(r.recommendation);
   return row;
}

string FP_HookP10SchemaHeader()
{
   return "schema_version,version,contract_id,column_name,source_phase,required,semantic_type,description";
}

string FP_HookP10SchemaRowCsv(const string contract_id,
                              const FP_HookPhase10TrainingSchemaRow &r)
{
   string row = "";
   row += FP_HookP10SafeCsv(FP_HOOK_P10_SCHEMA_VERSION);
   row += "," + FP_HookP10SafeCsv(FP_HOOK_P10_VERSION);
   row += "," + FP_HookP10SafeCsv(contract_id);
   row += "," + FP_HookP10SafeCsv(r.column_name);
   row += "," + FP_HookP10SafeCsv(r.source_phase);
   row += "," + FP_HookP10SafeCsv(FP_HookP10BoolName(r.required));
   row += "," + FP_HookP10SafeCsv(r.semantic_type);
   row += "," + FP_HookP10SafeCsv(r.description);
   return row;
}

string FP_HookP10ManifestHeader()
{
   return "schema_version,version,contract_id,key,value";
}

string FP_HookP10ManifestRowCsv(const string contract_id,
                                const string key,
                                const string value)
{
   string row = "";
   row += FP_HookP10SafeCsv(FP_HOOK_P10_SCHEMA_VERSION);
   row += "," + FP_HookP10SafeCsv(FP_HOOK_P10_VERSION);
   row += "," + FP_HookP10SafeCsv(contract_id);
   row += "," + FP_HookP10SafeCsv(key);
   row += "," + FP_HookP10SafeCsv(value);
   return row;
}

bool FP_HookP10ExportSummary(const string symbol,
                             const ENUM_TIMEFRAMES period,
                             const FP_HookPhase10Config &cfg,
                             FP_HookPhase10Report &report)
{
   if(!cfg.export_csv)
      return true;

   FolderCreate(FP_HookP10Folder(cfg));
   int handle = FileOpen(FP_HookP10SummaryPath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "HOOK_P10_SUMMARY_EXPORT_OPEN_FAILED";
      return false;
   }
   FileWriteString(handle, FP_HookP10SummaryHeader() + "\r\n");
   FileWriteString(handle, FP_HookP10SummaryRow(symbol, period, report) + "\r\n");
   FileClose(handle);
   report.files_written++;
   return true;
}

bool FP_HookP10ExportContracts(const FP_HookPhase10Config &cfg,
                               const FP_HookPhase10ContractRow &rows[],
                               FP_HookPhase10Report &report)
{
   if(!cfg.export_csv || !cfg.export_contract_checks_csv)
      return true;

   FolderCreate(FP_HookP10Folder(cfg));
   int handle = FileOpen(FP_HookP10ContractsPath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "HOOK_P10_CONTRACT_EXPORT_OPEN_FAILED";
      return false;
   }
   FileWriteString(handle, FP_HookP10ContractHeader() + "\r\n");
   for(int i=0; i<ArraySize(rows); i++)
      FileWriteString(handle, FP_HookP10ContractRowCsv(report.contract_id, rows[i]) + "\r\n");
   FileClose(handle);
   report.files_written++;
   return true;
}

bool FP_HookP10ExportSchema(const FP_HookPhase10Config &cfg,
                            const FP_HookPhase10TrainingSchemaRow &rows[],
                            FP_HookPhase10Report &report)
{
   if(!cfg.export_csv || !cfg.export_training_schema_csv)
      return true;

   FolderCreate(FP_HookP10Folder(cfg));
   int handle = FileOpen(FP_HookP10SchemaPath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "HOOK_P10_SCHEMA_EXPORT_OPEN_FAILED";
      return false;
   }
   FileWriteString(handle, FP_HookP10SchemaHeader() + "\r\n");
   for(int i=0; i<ArraySize(rows); i++)
      FileWriteString(handle, FP_HookP10SchemaRowCsv(report.contract_id, rows[i]) + "\r\n");
   FileClose(handle);
   report.files_written++;
   return true;
}

bool FP_HookP10ExportManifest(const string symbol,
                              const ENUM_TIMEFRAMES period,
                              const FP_HookPhase10Config &cfg,
                              FP_HookPhase10Report &report)
{
   if(!cfg.export_csv || !cfg.export_freeze_manifest_csv)
      return true;

   FolderCreate(FP_HookP10Folder(cfg));
   int handle = FileOpen(FP_HookP10ManifestPath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "HOOK_P10_MANIFEST_EXPORT_OPEN_FAILED";
      return false;
   }
   FileWriteString(handle, FP_HookP10ManifestHeader() + "\r\n");
   FileWriteString(handle, FP_HookP10ManifestRowCsv(report.contract_id, "symbol", symbol) + "\r\n");
   FileWriteString(handle, FP_HookP10ManifestRowCsv(report.contract_id, "period", EnumToString(period)) + "\r\n");
   FileWriteString(handle, FP_HookP10ManifestRowCsv(report.contract_id, "display_family", FP_HookP01DisplayFamilyName(report.display_family)) + "\r\n");
   FileWriteString(handle, FP_HookP10ManifestRowCsv(report.contract_id, "view_profile", FP_HookP07ViewProfileName(report.view_profile)) + "\r\n");
   FileWriteString(handle, FP_HookP10ManifestRowCsv(report.contract_id, "freeze_mode", FP_HookP10FreezeModeName(report.freeze_mode)) + "\r\n");
   FileWriteString(handle, FP_HookP10ManifestRowCsv(report.contract_id, "freeze_ready", FP_HookP10BoolName(report.freeze_ready)) + "\r\n");
   FileWriteString(handle, FP_HookP10ManifestRowCsv(report.contract_id, "status", report.status) + "\r\n");
   FileWriteString(handle, FP_HookP10ManifestRowCsv(report.contract_id, "reason", report.reason) + "\r\n");
   FileWriteString(handle, FP_HookP10ManifestRowCsv(report.contract_id, "p06_records_total", IntegerToString(report.p06_records_total)) + "\r\n");
   FileWriteString(handle, FP_HookP10ManifestRowCsv(report.contract_id, "p06_xy_closed_count", IntegerToString(report.p06_xy_closed_count)) + "\r\n");
   FileWriteString(handle, FP_HookP10ManifestRowCsv(report.contract_id, "training_schema_columns", IntegerToString(report.training_schema_columns)) + "\r\n");
   FileClose(handle);
   report.files_written++;
   return true;
}

#endif // __FP_HOOK_PHASE10_EXPORT_MQH__
