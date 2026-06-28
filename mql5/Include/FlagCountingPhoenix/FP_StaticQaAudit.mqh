#ifndef __FP_STATIC_QA_AUDIT_MQH__
#define __FP_STATIC_QA_AUDIT_MQH__
#property strict

#include "FP_StaticQaRules.mqh"

// ============================================================================
// Phoenix Level 18 - Static QA Audit Output
// ============================================================================

void FP_PrintStaticQaReport(const string prefix, const FP_StaticQaReport &r)
{
   string msg = prefix;
   msg += " attempted=" + FP_StaticQaBool(r.attempted);
   msg += " ok=" + FP_StaticQaBool(r.ok);
   msg += " mode=" + r.mode_name;
   msg += " case=" + r.case_id;
   msg += " run_id=" + r.run_id;
   msg += " checks=" + FP_StaticQaInt(r.checks_total);
   msg += " pass=" + FP_StaticQaInt(r.checks_passed);
   msg += " fail=" + FP_StaticQaInt(r.checks_failed);
   msg += " warn=" + FP_StaticQaInt(r.checks_warned);
   msg += " skipped=" + FP_StaticQaInt(r.checks_skipped);
   msg += " blockers=" + FP_StaticQaInt(r.blockers);
   msg += " compile_checks=" + FP_StaticQaInt(r.compile_contract_checks);
   msg += " compile_fail=" + FP_StaticQaInt(r.compile_contract_failures);
   msg += " runtime_checks=" + FP_StaticQaInt(r.runtime_contract_checks);
   msg += " runtime_fail=" + FP_StaticQaInt(r.runtime_contract_failures);
   msg += " print_checks=" + FP_StaticQaInt(r.print_safety_checks);
   msg += " print_fail=" + FP_StaticQaInt(r.print_safety_failures);
   msg += " input_checks=" + FP_StaticQaInt(r.input_contract_checks);
   msg += " input_fail=" + FP_StaticQaInt(r.input_contract_failures);
   msg += " dep_checks=" + FP_StaticQaInt(r.dependency_checks);
   msg += " dep_fail=" + FP_StaticQaInt(r.dependency_failures);
   msg += " io_checks=" + FP_StaticQaInt(r.io_contract_checks);
   msg += " io_fail=" + FP_StaticQaInt(r.io_contract_failures);
   msg += " report_checks=" + FP_StaticQaInt(r.report_alignment_checks);
   msg += " report_fail=" + FP_StaticQaInt(r.report_alignment_failures);
   msg += " toolchain_checks=" + FP_StaticQaInt(r.toolchain_checks);
   msg += " toolchain_fail=" + FP_StaticQaInt(r.toolchain_failures);
   msg += " files=" + FP_StaticQaInt(r.files_written);
   msg += " file_errors=" + FP_StaticQaInt(r.file_errors);
   msg += " file=" + r.report_file;
   msg += " reason=" + r.reason;
   Print(msg);
}

void FP_PrintStaticQaSamples(const string prefix,
                             const FP_StaticQaReport &r,
                             const string &rows[],
                             const int limit)
{
   int max_rows = MathMax(0, limit);
   for(int i=0; i<ArraySize(rows) && i<max_rows; i++)
      Print(prefix, "_SAMPLE ", rows[i]);
}

#endif // __FP_STATIC_QA_AUDIT_MQH__
