#ifndef __FP_INTERFACE_AUDIT_MQH__
#define __FP_INTERFACE_AUDIT_MQH__
#property strict

#include "FP_InterfaceRules.mqh"

// ============================================================================
// Phoenix Level 15 - Interface Audit Output
// ============================================================================

void FP_PrintInterfaceReport(const string prefix, const FP_InterfaceReport &r)
{
   string msg = prefix;
   msg += " attempted=" + FP_InterfaceBool(r.attempted);
   msg += " ok=" + FP_InterfaceBool(r.ok);
   msg += " stage=" + r.stage;
   msg += " run_id=" + r.run_id;
   msg += " checks=" + FP_InterfaceInt(r.checks_total);
   msg += " pass=" + FP_InterfaceInt(r.checks_passed);
   msg += " fail=" + FP_InterfaceInt(r.checks_failed);
   msg += " warn=" + FP_InterfaceInt(r.checks_warned);
   msg += " skipped=" + FP_InterfaceInt(r.checks_skipped);
   msg += " facade=" + FP_InterfaceInt(r.facade_checks);
   msg += " config=" + FP_InterfaceInt(r.config_checks);
   msg += " enum=" + FP_InterfaceInt(r.enum_checks);
   msg += " dependency=" + FP_InterfaceInt(r.dependency_checks);
   msg += " result=" + FP_InterfaceInt(r.result_checks);
   msg += " parent=" + FP_InterfaceInt(r.parent_checks);
   msg += " identity=" + FP_InterfaceInt(r.id_checks);
   msg += " missing_ids=" + FP_InterfaceInt(r.missing_public_ids);
   msg += " parent_errors=" + FP_InterfaceInt(r.visible_child_parent_errors);
   msg += " negative_counters=" + FP_InterfaceInt(r.negative_counter_errors);
   msg += " partition_errors=" + FP_InterfaceInt(r.partition_errors);
   msg += " dep_errors=" + FP_InterfaceInt(r.dependency_errors);
   msg += " files=" + FP_InterfaceInt(r.files_written);
   msg += " file_errors=" + FP_InterfaceInt(r.file_errors);
   msg += " file=" + r.report_file;
   msg += " reason=" + r.reason;
   Print(msg);
}

void FP_PrintInterfaceSamples(const string prefix,
                              const FP_InterfaceReport &r,
                              const string &rows[],
                              const int limit)
{
   int max_rows = MathMax(0, limit);
   for(int i=0; i<ArraySize(rows) && i<max_rows; i++)
      Print(prefix, "_SAMPLE ", rows[i]);
}

#endif // __FP_INTERFACE_AUDIT_MQH__
