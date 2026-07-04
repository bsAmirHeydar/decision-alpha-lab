#ifndef __FP_HOOK_PHASE09_EXPORT_MQH__
#define __FP_HOOK_PHASE09_EXPORT_MQH__
#property strict

#include "FP_HookPhase09Visual.mqh"

string FP_HookP09SafeCsv(string s)
{
   StringReplace(s, "\"", "\"\"");
   return "\"" + s + "\"";
}

string FP_HookP09Folder(const FP_HookPhase09Config &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_HOOK_P09_DEFAULT_FOLDER;
   return folder;
}

string FP_HookP09SummaryPath(const FP_HookPhase09Config &cfg)
{
   return FP_HookP09Folder(cfg) + "\\hook_phase09_smoke_summary.csv";
}

string FP_HookP09ScenariosPath(const FP_HookPhase09Config &cfg)
{
   return FP_HookP09Folder(cfg) + "\\hook_phase09_smoke_scenarios.csv";
}

string FP_HookP09CensusPath(const FP_HookPhase09Config &cfg)
{
   return FP_HookP09Folder(cfg) + "\\hook_phase09_object_census.csv";
}

string FP_HookP09FindingsPath(const FP_HookPhase09Config &cfg)
{
   return FP_HookP09Folder(cfg) + "\\hook_phase09_smoke_findings.csv";
}

string FP_HookP09SummaryHeader()
{
   return "schema_version,version,symbol,period,display_family,view_profile,status,ok,reason,scenarios_total,scenarios_required,scenarios_passed,scenarios_failed,scenarios_skipped,object_prefixes_checked,object_prefixes_failed,chart_hook_objects_seen,p09_objects_deleted,p09_objects_created,findings_total,passed_count,failed_count,info_count,warning_count,blocker_count,draw_contract_checks,draw_contract_failed,audit_only_checks,audit_only_failed,phase_file_error_checks,phase_file_error_failed,phase08_attempted,phase08_ok,phase08_status,phase08_reason,files_written,file_errors";
}

string FP_HookP09SummaryRow(const string symbol,
                            const ENUM_TIMEFRAMES period,
                            const FP_HookPhase09Report &r)
{
   string row = "";
   row += FP_HookP09SafeCsv(FP_HOOK_P09_SCHEMA_VERSION);
   row += "," + FP_HookP09SafeCsv(FP_HOOK_P09_VERSION);
   row += "," + FP_HookP09SafeCsv(symbol);
   row += "," + FP_HookP09SafeCsv(EnumToString(period));
   row += "," + FP_HookP09SafeCsv(FP_HookP01DisplayFamilyName(r.display_family));
   row += "," + FP_HookP09SafeCsv(FP_HookP07ViewProfileName(r.view_profile));
   row += "," + FP_HookP09SafeCsv(r.status);
   row += "," + FP_HookP09SafeCsv(FP_HookP09BoolName(r.ok));
   row += "," + FP_HookP09SafeCsv(r.reason);
   row += "," + IntegerToString(r.scenarios_total);
   row += "," + IntegerToString(r.scenarios_required);
   row += "," + IntegerToString(r.scenarios_passed);
   row += "," + IntegerToString(r.scenarios_failed);
   row += "," + IntegerToString(r.scenarios_skipped);
   row += "," + IntegerToString(r.object_prefixes_checked);
   row += "," + IntegerToString(r.object_prefixes_failed);
   row += "," + IntegerToString(r.chart_hook_objects_seen);
   row += "," + IntegerToString(r.p09_objects_deleted);
   row += "," + IntegerToString(r.p09_objects_created);
   row += "," + IntegerToString(r.findings_total);
   row += "," + IntegerToString(r.passed_count);
   row += "," + IntegerToString(r.failed_count);
   row += "," + IntegerToString(r.info_count);
   row += "," + IntegerToString(r.warning_count);
   row += "," + IntegerToString(r.blocker_count);
   row += "," + IntegerToString(r.draw_contract_checks);
   row += "," + IntegerToString(r.draw_contract_failed);
   row += "," + IntegerToString(r.audit_only_checks);
   row += "," + IntegerToString(r.audit_only_failed);
   row += "," + IntegerToString(r.phase_file_error_checks);
   row += "," + IntegerToString(r.phase_file_error_failed);
   row += "," + IntegerToString(r.phase08_attempted);
   row += "," + FP_HookP09SafeCsv(FP_HookP09BoolName(r.phase08_ok));
   row += "," + FP_HookP09SafeCsv(r.phase08_status);
   row += "," + FP_HookP09SafeCsv(r.phase08_reason);
   row += "," + IntegerToString(r.files_written);
   row += "," + IntegerToString(r.file_errors);
   return row;
}

string FP_HookP09ScenarioHeader()
{
   return "schema_version,version,scenario_code,view_profile,required_for_current_profile,state,passed,expected_min_objects,actual_objects,records_seen,evidence,recommendation";
}

string FP_HookP09ScenarioRowCsv(const FP_HookPhase09ScenarioRow &r)
{
   string row = "";
   row += FP_HookP09SafeCsv(FP_HOOK_P09_SCHEMA_VERSION);
   row += "," + FP_HookP09SafeCsv(FP_HOOK_P09_VERSION);
   row += "," + FP_HookP09SafeCsv(r.scenario_code);
   row += "," + FP_HookP09SafeCsv(r.view_profile);
   row += "," + FP_HookP09SafeCsv(FP_HookP09BoolName(r.required_for_current_profile));
   row += "," + FP_HookP09SafeCsv(FP_HookP09ScenarioStateName(r.state));
   row += "," + FP_HookP09SafeCsv(FP_HookP09BoolName(r.passed));
   row += "," + IntegerToString(r.expected_min_objects);
   row += "," + IntegerToString(r.actual_objects);
   row += "," + IntegerToString(r.records_seen);
   row += "," + FP_HookP09SafeCsv(r.evidence);
   row += "," + FP_HookP09SafeCsv(r.recommendation);
   return row;
}

string FP_HookP09CensusHeader()
{
   return "schema_version,version,phase,prefix,cfg_enabled,draw_surface_enabled,expected_min_objects,actual_objects,passed,reason";
}

string FP_HookP09CensusRowCsv(const FP_HookPhase09ObjectCensusRow &r)
{
   string row = "";
   row += FP_HookP09SafeCsv(FP_HOOK_P09_SCHEMA_VERSION);
   row += "," + FP_HookP09SafeCsv(FP_HOOK_P09_VERSION);
   row += "," + FP_HookP09SafeCsv(r.phase);
   row += "," + FP_HookP09SafeCsv(r.prefix);
   row += "," + FP_HookP09SafeCsv(FP_HookP09BoolName(r.cfg_enabled));
   row += "," + FP_HookP09SafeCsv(FP_HookP09BoolName(r.draw_surface_enabled));
   row += "," + IntegerToString(r.expected_min_objects);
   row += "," + IntegerToString(r.actual_objects);
   row += "," + FP_HookP09SafeCsv(FP_HookP09BoolName(r.passed));
   row += "," + FP_HookP09SafeCsv(r.reason);
   return row;
}

string FP_HookP09FindingHeader()
{
   return "schema_version,version,check_code,severity,passed,scope,evidence,recommendation";
}

string FP_HookP09FindingRowCsv(const FP_HookPhase09Finding &r)
{
   string row = "";
   row += FP_HookP09SafeCsv(FP_HOOK_P09_SCHEMA_VERSION);
   row += "," + FP_HookP09SafeCsv(FP_HOOK_P09_VERSION);
   row += "," + FP_HookP09SafeCsv(r.check_code);
   row += "," + FP_HookP09SafeCsv(FP_HookP09SeverityName(r.severity));
   row += "," + FP_HookP09SafeCsv(FP_HookP09BoolName(r.passed));
   row += "," + FP_HookP09SafeCsv(r.scope);
   row += "," + FP_HookP09SafeCsv(r.evidence);
   row += "," + FP_HookP09SafeCsv(r.recommendation);
   return row;
}

bool FP_HookP09ExportSummary(const string symbol,
                             const ENUM_TIMEFRAMES period,
                             const FP_HookPhase09Config &cfg,
                             FP_HookPhase09Report &report)
{
   if(!cfg.export_csv)
      return true;

   FolderCreate(FP_HookP09Folder(cfg));
   int handle = FileOpen(FP_HookP09SummaryPath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "HOOK_P09_SUMMARY_EXPORT_OPEN_FAILED";
      return false;
   }
   FileWriteString(handle, FP_HookP09SummaryHeader() + "\r\n");
   FileWriteString(handle, FP_HookP09SummaryRow(symbol, period, report) + "\r\n");
   FileClose(handle);
   report.files_written++;
   return true;
}

bool FP_HookP09ExportScenarios(const FP_HookPhase09Config &cfg,
                               const FP_HookPhase09ScenarioRow &rows[],
                               FP_HookPhase09Report &report)
{
   if(!cfg.export_csv || !cfg.export_scenarios_csv)
      return true;

   FolderCreate(FP_HookP09Folder(cfg));
   int handle = FileOpen(FP_HookP09ScenariosPath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "HOOK_P09_SCENARIOS_EXPORT_OPEN_FAILED";
      return false;
   }
   FileWriteString(handle, FP_HookP09ScenarioHeader() + "\r\n");
   for(int i=0; i<ArraySize(rows); i++)
      FileWriteString(handle, FP_HookP09ScenarioRowCsv(rows[i]) + "\r\n");
   FileClose(handle);
   report.files_written++;
   return true;
}

bool FP_HookP09ExportCensus(const FP_HookPhase09Config &cfg,
                            const FP_HookPhase09ObjectCensusRow &rows[],
                            FP_HookPhase09Report &report)
{
   if(!cfg.export_csv || !cfg.export_object_census_csv)
      return true;

   FolderCreate(FP_HookP09Folder(cfg));
   int handle = FileOpen(FP_HookP09CensusPath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "HOOK_P09_CENSUS_EXPORT_OPEN_FAILED";
      return false;
   }
   FileWriteString(handle, FP_HookP09CensusHeader() + "\r\n");
   for(int i=0; i<ArraySize(rows); i++)
      FileWriteString(handle, FP_HookP09CensusRowCsv(rows[i]) + "\r\n");
   FileClose(handle);
   report.files_written++;
   return true;
}

bool FP_HookP09ExportFindings(const FP_HookPhase09Config &cfg,
                              const FP_HookPhase09Finding &rows[],
                              FP_HookPhase09Report &report)
{
   if(!cfg.export_csv || !cfg.export_findings_csv)
      return true;

   FolderCreate(FP_HookP09Folder(cfg));
   int handle = FileOpen(FP_HookP09FindingsPath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "HOOK_P09_FINDINGS_EXPORT_OPEN_FAILED";
      return false;
   }
   FileWriteString(handle, FP_HookP09FindingHeader() + "\r\n");
   for(int i=0; i<ArraySize(rows); i++)
      FileWriteString(handle, FP_HookP09FindingRowCsv(rows[i]) + "\r\n");
   FileClose(handle);
   report.files_written++;
   return true;
}

#endif // __FP_HOOK_PHASE09_EXPORT_MQH__
