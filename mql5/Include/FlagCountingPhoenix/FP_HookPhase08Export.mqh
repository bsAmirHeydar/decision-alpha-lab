#ifndef __FP_HOOK_PHASE08_EXPORT_MQH__
#define __FP_HOOK_PHASE08_EXPORT_MQH__
#property strict

#include "FP_HookPhase08Visual.mqh"

string FP_HookP08SafeCsv(string s)
{
   StringReplace(s, "\"", "\"\"");
   return "\"" + s + "\"";
}

string FP_HookP08Folder(const FP_HookPhase08Config &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_HOOK_P08_DEFAULT_FOLDER;
   return folder;
}

string FP_HookP08SummaryPath(const FP_HookPhase08Config &cfg)
{
   return FP_HookP08Folder(cfg) + "\\hook_phase08_audit_summary.csv";
}

string FP_HookP08PhaseMatrixPath(const FP_HookPhase08Config &cfg)
{
   return FP_HookP08Folder(cfg) + "\\hook_phase08_phase_matrix.csv";
}

string FP_HookP08IntegrityPath(const FP_HookPhase08Config &cfg)
{
   return FP_HookP08Folder(cfg) + "\\hook_phase08_integrity_checks.csv";
}

string FP_HookP08SummaryHeader()
{
   return "schema_version,version,symbol,period,display_family,view_profile,status,ok,reason,phases_total,phases_enabled,phases_attempted,phases_ok,phases_failed,findings_total,passed_count,failed_count,info_count,warning_count,blocker_count,chain_checks,chain_passed,chain_failed,prefix_checks,prefix_failed,runtime_checks,runtime_failed,export_checks,export_failed,p06_records_total,p06_xy_closed,p06_elite,p06_high,p06_medium,p06_low,p06_invalid,files_written,file_errors";
}

string FP_HookP08SummaryRow(const string symbol,
                            const ENUM_TIMEFRAMES period,
                            const FP_HookPhase08Report &r)
{
   string row = "";
   row += FP_HookP08SafeCsv(FP_HOOK_P08_SCHEMA_VERSION);
   row += "," + FP_HookP08SafeCsv(FP_HOOK_P08_VERSION);
   row += "," + FP_HookP08SafeCsv(symbol);
   row += "," + FP_HookP08SafeCsv(EnumToString(period));
   row += "," + FP_HookP08SafeCsv(FP_HookP01DisplayFamilyName(r.display_family));
   row += "," + FP_HookP08SafeCsv(FP_HookP07ViewProfileName(r.view_profile));
   row += "," + FP_HookP08SafeCsv(r.status);
   row += "," + FP_HookP08SafeCsv(FP_HookP08BoolName(r.ok));
   row += "," + FP_HookP08SafeCsv(r.reason);
   row += "," + IntegerToString(r.phases_total);
   row += "," + IntegerToString(r.phases_enabled);
   row += "," + IntegerToString(r.phases_attempted);
   row += "," + IntegerToString(r.phases_ok);
   row += "," + IntegerToString(r.phases_failed);
   row += "," + IntegerToString(r.findings_total);
   row += "," + IntegerToString(r.passed_count);
   row += "," + IntegerToString(r.failed_count);
   row += "," + IntegerToString(r.info_count);
   row += "," + IntegerToString(r.warning_count);
   row += "," + IntegerToString(r.blocker_count);
   row += "," + IntegerToString(r.chain_checks);
   row += "," + IntegerToString(r.chain_passed);
   row += "," + IntegerToString(r.chain_failed);
   row += "," + IntegerToString(r.prefix_checks);
   row += "," + IntegerToString(r.prefix_failed);
   row += "," + IntegerToString(r.runtime_checks);
   row += "," + IntegerToString(r.runtime_failed);
   row += "," + IntegerToString(r.export_checks);
   row += "," + IntegerToString(r.export_failed);
   row += "," + IntegerToString(r.p06_records_total);
   row += "," + IntegerToString(r.p06_xy_closed_count);
   row += "," + IntegerToString(r.p06_elite_count);
   row += "," + IntegerToString(r.p06_high_count);
   row += "," + IntegerToString(r.p06_medium_count);
   row += "," + IntegerToString(r.p06_low_count);
   row += "," + IntegerToString(r.p06_invalid_count);
   row += "," + IntegerToString(r.files_written);
   row += "," + IntegerToString(r.file_errors);
   return row;
}

string FP_HookP08PhaseMatrixHeader()
{
   return "schema_version,version,phase,cfg_enabled,attempted,ok,status,reason,export_enabled,files_written,file_errors,records_seen,positive_seen,negative_seen,objects_created,objects_deleted,drawn_seen";
}

string FP_HookP08PhaseMatrixRow(const FP_HookPhase08PhaseRow &r)
{
   string row = "";
   row += FP_HookP08SafeCsv(FP_HOOK_P08_SCHEMA_VERSION);
   row += "," + FP_HookP08SafeCsv(FP_HOOK_P08_VERSION);
   row += "," + FP_HookP08SafeCsv(r.phase);
   row += "," + FP_HookP08SafeCsv(FP_HookP08BoolName(r.cfg_enabled));
   row += "," + FP_HookP08SafeCsv(FP_HookP08BoolName(r.attempted));
   row += "," + FP_HookP08SafeCsv(FP_HookP08BoolName(r.ok));
   row += "," + FP_HookP08SafeCsv(r.status);
   row += "," + FP_HookP08SafeCsv(r.reason);
   row += "," + FP_HookP08SafeCsv(FP_HookP08BoolName(r.export_enabled));
   row += "," + IntegerToString(r.files_written);
   row += "," + IntegerToString(r.file_errors);
   row += "," + IntegerToString(r.records_seen);
   row += "," + IntegerToString(r.positive_seen);
   row += "," + IntegerToString(r.negative_seen);
   row += "," + IntegerToString(r.objects_created);
   row += "," + IntegerToString(r.objects_deleted);
   row += "," + IntegerToString(r.drawn_seen);
   return row;
}

string FP_HookP08IntegrityHeader()
{
   return "schema_version,version,check_code,severity,passed,phase,evidence,recommendation";
}

string FP_HookP08IntegrityRow(const FP_HookPhase08Finding &f)
{
   string row = "";
   row += FP_HookP08SafeCsv(FP_HOOK_P08_SCHEMA_VERSION);
   row += "," + FP_HookP08SafeCsv(FP_HOOK_P08_VERSION);
   row += "," + FP_HookP08SafeCsv(f.check_code);
   row += "," + FP_HookP08SafeCsv(FP_HookP08SeverityName(f.severity));
   row += "," + FP_HookP08SafeCsv(FP_HookP08BoolName(f.passed));
   row += "," + FP_HookP08SafeCsv(f.phase);
   row += "," + FP_HookP08SafeCsv(f.evidence);
   row += "," + FP_HookP08SafeCsv(f.recommendation);
   return row;
}

bool FP_HookP08ExportSummary(const string symbol,
                             const ENUM_TIMEFRAMES period,
                             const FP_HookPhase08Config &cfg,
                             FP_HookPhase08Report &report)
{
   if(!cfg.export_csv)
      return true;

   FolderCreate(FP_HookP08Folder(cfg));

   int handle = FileOpen(FP_HookP08SummaryPath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "HOOK_P08_SUMMARY_EXPORT_OPEN_FAILED";
      return false;
   }

   FileWriteString(handle, FP_HookP08SummaryHeader() + "\r\n");
   FileWriteString(handle, FP_HookP08SummaryRow(symbol, period, report) + "\r\n");
   FileClose(handle);
   report.files_written++;
   return true;
}

bool FP_HookP08ExportPhaseMatrix(const FP_HookPhase08Config &cfg,
                                 const FP_HookPhase08PhaseRow &rows[],
                                 FP_HookPhase08Report &report)
{
   if(!cfg.export_csv || !cfg.export_phase_matrix_csv)
      return true;

   FolderCreate(FP_HookP08Folder(cfg));

   int handle = FileOpen(FP_HookP08PhaseMatrixPath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "HOOK_P08_PHASE_MATRIX_EXPORT_OPEN_FAILED";
      return false;
   }

   FileWriteString(handle, FP_HookP08PhaseMatrixHeader() + "\r\n");
   for(int i=0; i<ArraySize(rows); i++)
      FileWriteString(handle, FP_HookP08PhaseMatrixRow(rows[i]) + "\r\n");

   FileClose(handle);
   report.files_written++;
   return true;
}

bool FP_HookP08ExportIntegrity(const FP_HookPhase08Config &cfg,
                               const FP_HookPhase08Finding &findings[],
                               FP_HookPhase08Report &report)
{
   if(!cfg.export_csv || !cfg.export_integrity_csv)
      return true;

   FolderCreate(FP_HookP08Folder(cfg));

   int handle = FileOpen(FP_HookP08IntegrityPath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "HOOK_P08_INTEGRITY_EXPORT_OPEN_FAILED";
      return false;
   }

   FileWriteString(handle, FP_HookP08IntegrityHeader() + "\r\n");
   for(int i=0; i<ArraySize(findings); i++)
      FileWriteString(handle, FP_HookP08IntegrityRow(findings[i]) + "\r\n");

   FileClose(handle);
   report.files_written++;
   return true;
}

#endif // __FP_HOOK_PHASE08_EXPORT_MQH__
