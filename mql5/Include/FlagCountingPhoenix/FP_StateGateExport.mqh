#ifndef __FP_STATE_GATE_EXPORT_MQH__
#define __FP_STATE_GATE_EXPORT_MQH__
#property strict

#include "FP_StateGateAudit.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 19 State Gate Export
// ----------------------------------------------------------------------------
// Phase 1 intentionally keeps export as a compile-safe stub.  CSV state-gate
// files start in later phases when real projection rows exist.
// ============================================================================

void FP_StateGateExportPhase1Stub(const FP_StateGateConfig &cfg,
                                  const FP_StateGateSnapshot &snapshot,
                                  FP_StateGateReport &report)
{
   if(!cfg.export_csv) return;
   report.files_written += 0;
   report.file_errors += 0;
   if(snapshot.initialized)
      report.reason = "phase1_export_stub";
}

#endif // __FP_STATE_GATE_EXPORT_MQH__
