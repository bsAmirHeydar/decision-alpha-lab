#ifndef __FP_ACCEPTANCE_AUDIT_MQH__
#define __FP_ACCEPTANCE_AUDIT_MQH__
#property strict

#include "FP_AcceptanceRules.mqh"

// ============================================================================
// Phoenix Level 16 - Acceptance Audit Output
// ============================================================================

void FP_PrintAcceptanceReport(const string prefix, const FP_AcceptanceReport &r)
{
   string msg = prefix;
   msg += " attempted=" + FP_AcceptanceBool(r.attempted);
   msg += " ok=" + FP_AcceptanceBool(r.ok);
   msg += " mode=" + r.mode_name;
   msg += " case=" + r.case_id;
   msg += " run_id=" + r.run_id;
   msg += " checks=" + FP_AcceptanceInt(r.checks_total);
   msg += " pass=" + FP_AcceptanceInt(r.checks_passed);
   msg += " fail=" + FP_AcceptanceInt(r.checks_failed);
   msg += " warn=" + FP_AcceptanceInt(r.checks_warned);
   msg += " skipped=" + FP_AcceptanceInt(r.checks_skipped);
   msg += " hard=" + FP_AcceptanceInt(r.hard_gates_total);
   msg += " hard_pass=" + FP_AcceptanceInt(r.hard_gates_passed);
   msg += " hard_fail=" + FP_AcceptanceInt(r.hard_gates_failed);
   msg += " levels=" + FP_AcceptanceInt(r.levels_checked);
   msg += " levels_pass=" + FP_AcceptanceInt(r.levels_passed);
   msg += " levels_fail=" + FP_AcceptanceInt(r.levels_failed);
   msg += " levels_warn=" + FP_AcceptanceInt(r.levels_warned);
   msg += " baseline=" + FP_AcceptanceInt(r.baseline_items);
   msg += " regression=" + FP_AcceptanceInt(r.regression_items);
   msg += " release=" + FP_AcceptanceInt(r.release_items);
   msg += " order_errors=" + FP_AcceptanceInt(r.order_errors);
   msg += " dependency_errors=" + FP_AcceptanceInt(r.dependency_errors);
   msg += " matrix_errors=" + FP_AcceptanceInt(r.matrix_errors);
   msg += " invariant_errors=" + FP_AcceptanceInt(r.invariant_errors);
   msg += " files=" + FP_AcceptanceInt(r.files_written);
   msg += " file_errors=" + FP_AcceptanceInt(r.file_errors);
   msg += " file=" + r.report_file;
   msg += " reason=" + r.reason;
   Print(msg);
}

void FP_PrintAcceptanceSamples(const string prefix,
                               const FP_AcceptanceReport &r,
                               const string &rows[],
                               const int limit)
{
   int max_rows = MathMax(0, limit);
   for(int i=0; i<ArraySize(rows) && i<max_rows; i++)
      Print(prefix, "_SAMPLE ", rows[i]);
}

#endif // __FP_ACCEPTANCE_AUDIT_MQH__
