#ifndef __FP_STATE_GATE_ENGINE_MQH__
#define __FP_STATE_GATE_ENGINE_MQH__
#property strict

#include "FP_StateGateExport.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 19 Clean Isolated State Gate Engine
// ----------------------------------------------------------------------------
// Read-only diagnostic layer. It does not call FP_Draw*, FP_DeleteObjectsByPrefix,
// order functions, or any structural mutation.
// ============================================================================

void FP_RunLevel19StateGate(const string symbol,
                            const ENUM_TIMEFRAMES period,
                            const MqlRates &rates[],
                            const int bars,
                            const int &scales[],
                            const int scale_count,
                            const FP_FlagEvent &events[],
                            const FP_HookBranch &hooks[],
                            const FP_DetectResult &result,
                            const FP_TimebaseReport &timebase_report,
                            const FP_ExportReport &export_report,
                            const FP_RenderReport &render_report,
                            const FP_ValidationReport &validation_report,
                            const FP_Level19StateGateConfig &cfg,
                            FP_Level19StateGateReport &report)
{
   FP_ResetLevel19StateGateReport(report);
   report.attempted = cfg.enabled;

   if(!cfg.enabled)
   {
      report.ok = true;
      report.status = "LEVEL19_DISABLED";
      report.reason = "InpLevel19StateGateEnabled_false";
      return;
   }

   FP_Level19StateGateSnapshot snapshot;
   FP_L19BuildSnapshot(symbol, period, rates, bars, scale_count, events, hooks, result,
                       timebase_report, export_report, render_report, validation_report, snapshot);

   bool export_ok = FP_L19ExportSnapshot(cfg, snapshot, report);
   FP_L19PanelDraw(cfg, snapshot, report);

   report.ok = (export_ok && report.file_errors == 0 && report.panel_object_errors == 0);
   report.status = snapshot.state_status;
   report.reason = snapshot.no_touch_contract;
}

void FP_PrintLevel19StateGateReport(const string tag,
                                    const FP_Level19StateGateReport &report)
{
   Print(tag,
         " attempted=", FP_L19Bool(report.attempted),
         " ok=", FP_L19Bool(report.ok),
         " status=", report.status,
         " reason=", report.reason,
         " files_written=", report.files_written,
         " file_errors=", report.file_errors,
         " panel_created=", report.panel_objects_created,
         " panel_errors=", report.panel_object_errors,
         " panel_deleted=", report.panel_objects_deleted);
}

#endif // __FP_STATE_GATE_ENGINE_MQH__
