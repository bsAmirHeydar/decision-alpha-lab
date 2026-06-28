#ifndef __FP_AMBIGUITY_AUDIT_MQH__
#define __FP_AMBIGUITY_AUDIT_MQH__
#property strict

#include "FP_AmbiguityRules.mqh"

// ============================================================================
// Phoenix Level 17 - Ambiguity / Decision-Lock Audit Output
// ============================================================================

void FP_PrintAmbiguityReport(const string prefix, const FP_AmbiguityReport &r)
{
   string msg = prefix;
   msg += " attempted=" + FP_AmbiguityBool(r.attempted);
   msg += " ok=" + FP_AmbiguityBool(r.ok);
   msg += " mode=" + r.mode_name;
   msg += " case=" + r.case_id;
   msg += " run_id=" + r.run_id;
   msg += " canon=" + r.canon_source;
   msg += " checks=" + FP_AmbiguityInt(r.checks_total);
   msg += " locked=" + FP_AmbiguityInt(r.checks_passed);
   msg += " unlocked=" + FP_AmbiguityInt(r.checks_failed);
   msg += " warn=" + FP_AmbiguityInt(r.checks_warned);
   msg += " skipped=" + FP_AmbiguityInt(r.checks_skipped);
   msg += " decisions=" + FP_AmbiguityInt(r.decisions_total);
   msg += " decisions_locked=" + FP_AmbiguityInt(r.decisions_locked);
   msg += " decisions_unlocked=" + FP_AmbiguityInt(r.decisions_unlocked);
   msg += " diagnostic=" + FP_AmbiguityInt(r.diagnostic_variants);
   msg += " release_blockers=" + FP_AmbiguityInt(r.release_blockers);
   msg += " source_conflicts=" + FP_AmbiguityInt(r.source_conflicts);
   msg += " profile_conflicts=" + FP_AmbiguityInt(r.profile_conflicts);
   msg += " default_conflicts=" + FP_AmbiguityInt(r.default_conflicts);
   msg += " runtime_conflicts=" + FP_AmbiguityInt(r.runtime_conflicts);
   msg += " legacy_conflicts=" + FP_AmbiguityInt(r.legacy_conflicts);
   msg += " files=" + FP_AmbiguityInt(r.files_written);
   msg += " file_errors=" + FP_AmbiguityInt(r.file_errors);
   msg += " file=" + r.report_file;
   msg += " reason=" + r.reason;
   Print(msg);
}

void FP_PrintAmbiguitySamples(const string prefix,
                              const FP_AmbiguityReport &r,
                              const string &rows[],
                              const int limit)
{
   int max_rows = MathMax(0, limit);
   for(int i=0; i<ArraySize(rows) && i<max_rows; i++)
      Print(prefix, "_SAMPLE ", rows[i]);
}

#endif // __FP_AMBIGUITY_AUDIT_MQH__
