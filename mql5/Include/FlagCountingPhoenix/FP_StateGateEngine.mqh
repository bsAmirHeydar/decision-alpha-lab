#ifndef __FP_STATE_GATE_ENGINE_MQH__
#define __FP_STATE_GATE_ENGINE_MQH__
#property strict

#include "FP_StateGateExport.mqh"

datetime g_fp_level19_last_ledger_bar_time = 0;

// ============================================================================
// FlagCounting Phoenix - Level 19 Clean Isolated State Gate Engine
// ----------------------------------------------------------------------------
// Read-only diagnostic layer. It does not call FP_Draw*, FP_DeleteObjectsByPrefix,
// order functions, or any structural mutation.
// ============================================================================

bool FP_L19ShouldWriteClosedBarLedger(const FP_Level19StateGateSnapshot &snapshot,
                                      FP_Level19StateGateReport &report)
{
   if(snapshot.last_bar_time <= 0)
      return false;

   if(g_fp_level19_last_ledger_bar_time == snapshot.last_bar_time)
   {
      report.ledger_skipped_duplicate_bar = true;
      return false;
   }

   g_fp_level19_last_ledger_bar_time = snapshot.last_bar_time;
   return true;
}


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
   bool ledger_ok = true;
   if(cfg.export_closed_bar_ledger_csv && FP_L19ShouldWriteClosedBarLedger(snapshot, report))
      ledger_ok = FP_L19AppendClosedBarLedger(cfg, snapshot, report);

   FP_L19PanelDraw(cfg, snapshot, report);

   report.ok = (export_ok && ledger_ok && report.file_errors == 0 && report.panel_object_errors == 0);
   report.status = snapshot.state_status;
   report.reason = snapshot.no_touch_contract;
}

void FP_PrintLevel19StateGateReport(const string tag,
                                    const FP_Level19StateGateReport &report)
{
   string line = tag;
   line += " attempted=" + FP_L19Bool(report.attempted);
   line += " ok=" + FP_L19Bool(report.ok);
   line += " status=" + report.status;
   line += " reason=" + report.reason;
   line += " files_written=" + IntegerToString(report.files_written);
   line += " file_errors=" + IntegerToString(report.file_errors);
   line += " ledger_written=" + FP_L19Bool(report.ledger_written);
   line += " ledger_duplicate_skip=" + FP_L19Bool(report.ledger_skipped_duplicate_bar);
   line += " panel_created=" + IntegerToString(report.panel_objects_created);
   line += " panel_errors=" + IntegerToString(report.panel_object_errors);
   line += " panel_deleted=" + IntegerToString(report.panel_objects_deleted);
   Print(line);
}

#endif // __FP_STATE_GATE_ENGINE_MQH__
