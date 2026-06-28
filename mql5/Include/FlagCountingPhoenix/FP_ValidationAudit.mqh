#ifndef __FP_VALIDATION_AUDIT_MQH__
#define __FP_VALIDATION_AUDIT_MQH__
#property strict

#include "FP_ValidationRules.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 13 Validation Audit
// ============================================================================

string FP_ValidationHeader()
{
   string h = "";
   FP_ExportCsvAppend(h, "suite_tag");
   FP_ExportCsvAppend(h, "case_id");
   FP_ExportCsvAppend(h, "check_id");
   FP_ExportCsvAppend(h, "check_name");
   FP_ExportCsvAppend(h, "severity");
   FP_ExportCsvAppend(h, "actual");
   FP_ExportCsvAppend(h, "expected_min");
   FP_ExportCsvAppend(h, "expected_max");
   FP_ExportCsvAppend(h, "status");
   FP_ExportCsvAppend(h, "reason");
   return h;
}

string FP_ValidationRow(const FP_ValidationConfig &cfg,
                        const string check_id,
                        const string check_name,
                        const string severity,
                        const int actual,
                        const int expected_min,
                        const int expected_max,
                        const string status,
                        const string reason)
{
   string line = "";
   FP_ExportCsvAppend(line, cfg.suite_tag);
   FP_ExportCsvAppend(line, cfg.case_id);
   FP_ExportCsvAppend(line, check_id);
   FP_ExportCsvAppend(line, check_name);
   FP_ExportCsvAppend(line, severity);
   FP_ExportCsvAppend(line, IntegerToString(actual));
   FP_ExportCsvAppend(line, (expected_min < 0 ? "" : IntegerToString(expected_min)));
   FP_ExportCsvAppend(line, (expected_max < 0 ? "" : IntegerToString(expected_max)));
   FP_ExportCsvAppend(line, status);
   FP_ExportCsvAppend(line, reason);
   return line;
}

void FP_ValidationAppendRow(string &rows[], const string row)
{
   int n = ArraySize(rows);
   ArrayResize(rows, n + 1);
   rows[n] = row;
}

void FP_ValidationAddCheck(FP_ValidationReport &report,
                           const FP_ValidationConfig &cfg,
                           string &rows[],
                           const string check_id,
                           const string check_name,
                           const string severity,
                           const int actual,
                           const int expected_min,
                           const int expected_max,
                           const string pass_reason,
                           const string fail_reason)
{
   bool has_expected = (expected_min >= 0 || expected_max >= 0);
   if(!has_expected)
   {
      report.checks_skipped++;
      if(cfg.baseline_mode) report.checks_warned++;
      string status = (cfg.baseline_mode ? "WARN" : "SKIP");
      string reason = "baseline_required actual=" + IntegerToString(actual);
      FP_ValidationAppendRow(rows, FP_ValidationRow(cfg, check_id, check_name, severity, actual, expected_min, expected_max, status, reason));
      return;
   }

   report.checks_total++;
   bool pass = FP_ValidationRangePass(actual, expected_min, expected_max);
   if(pass)
   {
      report.checks_passed++;
      FP_ValidationAppendRow(rows, FP_ValidationRow(cfg, check_id, check_name, severity, actual, expected_min, expected_max, "PASS", pass_reason));
   }
   else
   {
      if(severity == "warning") report.checks_warned++;
      else report.checks_failed++;
      FP_ValidationAppendRow(rows, FP_ValidationRow(cfg, check_id, check_name, severity, actual, expected_min, expected_max, (severity == "warning" ? "WARN" : "FAIL"), fail_reason));
   }
}

void FP_ValidationAddBoolCheck(FP_ValidationReport &report,
                               const FP_ValidationConfig &cfg,
                               string &rows[],
                               const string check_id,
                               const string check_name,
                               const string severity,
                               const bool pass,
                               const string pass_reason,
                               const string fail_reason)
{
   report.checks_total++;
   if(pass)
   {
      report.checks_passed++;
      FP_ValidationAppendRow(rows, FP_ValidationRow(cfg, check_id, check_name, severity, 1, 1, 1, "PASS", pass_reason));
   }
   else
   {
      if(severity == "warning") report.checks_warned++;
      else report.checks_failed++;
      FP_ValidationAppendRow(rows, FP_ValidationRow(cfg, check_id, check_name, severity, 0, 1, 1, (severity == "warning" ? "WARN" : "FAIL"), fail_reason));
   }
}

void FP_PrintValidationReport(const string prefix, const FP_ValidationReport &r)
{
   string msg = prefix;
   msg += " attempted=" + FP_ValidationBool(r.attempted);
   msg += " ok=" + FP_ValidationBool(r.ok);
   msg += " case_id=" + r.case_id;
   msg += " suite=" + r.suite_tag;
   msg += " checks=" + IntegerToString(r.checks_total);
   msg += " pass=" + IntegerToString(r.checks_passed);
   msg += " fail=" + IntegerToString(r.checks_failed);
   msg += " warn=" + IntegerToString(r.checks_warned);
   msg += " skipped=" + IntegerToString(r.checks_skipped);
   msg += " files=" + IntegerToString(r.files_written);
   msg += " file_errors=" + IntegerToString(r.file_errors);
   msg += " bars=" + IntegerToString(r.actual_bars);
   msg += " scales=" + IntegerToString(r.actual_scales);
   msg += " raw_nodes=" + IntegerToString(r.actual_raw_nodes);
   msg += " canonical_nodes=" + IntegerToString(r.actual_canonical_nodes);
   msg += " hooks=" + IntegerToString(r.actual_hooks);
   msg += " nd=" + IntegerToString(r.actual_nd);
   msg += " events=" + IntegerToString(r.actual_events);
   msg += " visible=" + IntegerToString(r.actual_visible_events);
   msg += " hidden=" + IntegerToString(r.actual_hidden_events);
   msg += " f1=" + IntegerToString(r.actual_f1);
   msg += " f2=" + IntegerToString(r.actual_f2);
   msg += " f3=" + IntegerToString(r.actual_f3);
   msg += " locked_f3=" + IntegerToString(r.actual_locked_f3);
   msg += " hidden_without_reason=" + IntegerToString(r.hidden_without_reason);
   msg += " visible_with_hidden_reason=" + IntegerToString(r.visible_with_hidden_reason);
   msg += " visible_child_without_parent=" + IntegerToString(r.visible_child_without_visible_parent);
   msg += " visible_duplicate_canonical_id=" + IntegerToString(r.visible_duplicate_canonical_id);
   msg += " file=" + r.validation_file;
   msg += " reason=" + r.reason;
   Print(msg);
}

void FP_PrintValidationSamples(const string prefix, const FP_ValidationReport &r, const string &rows[], const int limit)
{
   int max_rows = MathMax(0, limit);
   for(int i=0; i<ArraySize(rows) && i<max_rows; i++)
      Print(prefix, "_CHECK_SAMPLE ", rows[i]);
}

#endif // __FP_VALIDATION_AUDIT_MQH__
