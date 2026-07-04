#ifndef __FP_HOOK_PHASE08_ENGINE_MQH__
#define __FP_HOOK_PHASE08_ENGINE_MQH__
#property strict

#include "FP_HookPhase08Export.mqh"

void FP_RunHookPhase08(const string symbol,
                       const ENUM_TIMEFRAMES period,
                       const FP_HookPhase01Config &p01_cfg,
                       const FP_HookPhase02Config &p02_cfg,
                       const FP_HookPhase03Config &p03_cfg,
                       const FP_HookPhase04Config &p04_cfg,
                       const FP_HookPhase05Config &p05_cfg,
                       const FP_HookPhase06Config &p06_cfg,
                       const FP_HookPhase07Config &p07_cfg,
                       const FP_HookPhase08Config &p08_cfg,
                       const FP_HookPhase01Report &p01_report,
                       const FP_HookPhase02Report &p02_report,
                       const FP_HookPhase03Report &p03_report,
                       const FP_HookPhase04Report &p04_report,
                       const FP_HookPhase05Report &p05_report,
                       const FP_HookPhase06Report &p06_report,
                       const FP_HookPhase07Report &p07_report,
                       FP_HookPhase08Report &p08_report)
{
   FP_ResetHookPhase08Report(p08_report);
   p08_report.display_family = p08_cfg.display_family;
   p08_report.view_profile = p07_cfg.view_profile;

   if(!FP_HookP08ShouldRun(p08_cfg))
   {
      p08_report.ok = true;
      p08_report.status = "HOOK_P08_SKIPPED";
      if(!p08_cfg.enabled)
         p08_report.reason = "PHASE08_DISABLED";
      else
         p08_report.reason = "RALLY_ONLY_AUDIT_NOT_ALLOWED";
      return;
   }

   p08_report.attempted = true;

   FP_HookPhase08PhaseRow phase_rows[];
   FP_HookPhase08Finding findings[];

   FP_HookP08BuildPhaseMatrix(p01_cfg, p02_cfg, p03_cfg, p04_cfg, p05_cfg, p06_cfg, p07_cfg,
                              p01_report, p02_report, p03_report, p04_report, p05_report, p06_report, p07_report,
                              phase_rows, p08_report);

   FP_HookP08FillQualitySnapshot(p06_report, p08_report);

   FP_HookP08CheckRuntimeReports(p08_cfg, phase_rows, findings, p08_report);
   FP_HookP08CheckNonnegativeCounts(p08_cfg, phase_rows, findings, p08_report);
   FP_HookP08CheckNoFileErrors(p08_cfg, phase_rows, findings, p08_report);
   FP_HookP08CheckExportProfileAlignment(p08_cfg, p07_cfg, p07_report, findings, p08_report);
   FP_HookP08CheckChainAlignment(p08_cfg, p02_report, p03_report, p04_report, p05_report, p06_report, findings, p08_report);
   FP_HookP08CheckUniquePrefixes(p08_cfg, p01_cfg, p02_cfg, p03_cfg, p04_cfg, p05_cfg, p06_cfg, p07_cfg, findings, p08_report);
   FP_HookP08CheckP06QualityAudit(p08_cfg, p06_report, findings, p08_report);

   FP_HookP08FinalizeReport(p08_cfg, p08_report);

   bool exported_ok = true;
   if(p08_cfg.export_csv)
   {
      exported_ok = FP_HookP08ExportPhaseMatrix(p08_cfg, phase_rows, p08_report) && exported_ok;
      exported_ok = FP_HookP08ExportIntegrity(p08_cfg, findings, p08_report) && exported_ok;
      exported_ok = FP_HookP08ExportSummary(symbol, period, p08_cfg, p08_report) && exported_ok;

      if(!exported_ok)
      {
         p08_report.ok = false;
         p08_report.status = "HOOK_P08_FILE_ERROR";
         if(StringLen(p08_report.reason) <= 0 || p08_report.reason == "HOOK_AUDIT_RECONCILED")
            p08_report.reason = "PHASE08_EXPORT_FILE_ERROR";
      }
   }

   if(p08_cfg.print_summary)
      FP_PrintHookPhase08Report("FP_HOOK_P08", p08_report);

   if(p08_cfg.print_samples)
      FP_PrintHookPhase08Findings("FP_HOOK_P08", findings, p08_cfg.sample_limit);
}

#endif // __FP_HOOK_PHASE08_ENGINE_MQH__
