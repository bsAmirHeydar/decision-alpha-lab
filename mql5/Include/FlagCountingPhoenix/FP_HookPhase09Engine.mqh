#ifndef __FP_HOOK_PHASE09_ENGINE_MQH__
#define __FP_HOOK_PHASE09_ENGINE_MQH__
#property strict

#include "FP_HookPhase09Export.mqh"

void FP_RunHookPhase09(const string symbol,
                       const ENUM_TIMEFRAMES period,
                       const FP_HookPhase01Config &p01_cfg,
                       const FP_HookPhase02Config &p02_cfg,
                       const FP_HookPhase03Config &p03_cfg,
                       const FP_HookPhase04Config &p04_cfg,
                       const FP_HookPhase05Config &p05_cfg,
                       const FP_HookPhase06Config &p06_cfg,
                       const FP_HookPhase07Config &p07_cfg,
                       const FP_HookPhase08Config &p08_cfg,
                       const FP_HookPhase09Config &p09_cfg,
                       const FP_HookPhase01Report &p01_report,
                       const FP_HookPhase02Report &p02_report,
                       const FP_HookPhase03Report &p03_report,
                       const FP_HookPhase04Report &p04_report,
                       const FP_HookPhase05Report &p05_report,
                       const FP_HookPhase06Report &p06_report,
                       const FP_HookPhase07Report &p07_report,
                       const FP_HookPhase08Report &p08_report,
                       FP_HookPhase09Report &p09_report)
{
   FP_ResetHookPhase09Report(p09_report);
   p09_report.display_family = p09_cfg.display_family;
   p09_report.view_profile = p07_cfg.view_profile;

   if(!FP_HookP09ShouldRun(p09_cfg))
   {
      p09_report.ok = true;
      p09_report.status = "HOOK_P09_SKIPPED";
      if(!p09_cfg.enabled)
         p09_report.reason = "PHASE09_DISABLED";
      else
         p09_report.reason = "RALLY_ONLY_SMOKE_NOT_ALLOWED";
      return;
   }

   p09_report.attempted = true;

   FP_HookPhase09ObjectCensusRow census[];
   FP_HookPhase09ScenarioRow scenarios[];
   FP_HookPhase09Finding findings[];

   if(p09_cfg.clean_p09_objects_before_draw)
      p09_report.p09_objects_deleted += FP_HookP09DeleteObjectsByPrefix(p09_cfg.object_prefix);

   FP_HookP09BuildObjectCensus(p01_cfg, p02_cfg, p03_cfg, p04_cfg, p05_cfg, p06_cfg, p07_cfg, p08_cfg, p09_cfg,
                               p01_report, p02_report, p03_report, p04_report, p05_report, p06_report,
                               census, p09_report);

   FP_HookP09BuildCurrentProfileScenarios(p07_cfg, census,
                                          p01_report, p02_report, p03_report, p04_report, p05_report, p06_report,
                                          scenarios, p09_report);

   FP_HookP09CheckPhase08Ok(p09_cfg, p08_report, findings, p09_report);
   FP_HookP09CheckNoPhaseFileErrors(p09_cfg,
                                    p01_report, p02_report, p03_report, p04_report, p05_report, p06_report,
                                    p07_report, p08_report,
                                    findings, p09_report);
   FP_HookP09CheckObjectCensus(p09_cfg, census, findings, p09_report);
   FP_HookP09CheckCurrentProfileCoverage(p09_cfg, scenarios, findings, p09_report);
   FP_HookP09CheckAuditOnlyNoDraw(p09_cfg, p07_cfg, census, findings, p09_report);
   FP_HookP09CheckDrawContract(p09_cfg, census, findings, p09_report);

   FP_HookP09FinalizeReport(p09_cfg, p09_report);

   bool panel_ok = FP_HookP09DrawPanel(p09_cfg, p09_report);
   if(!panel_ok)
   {
      p09_report.ok = false;
      p09_report.status = "HOOK_P09_PANEL_ERROR";
      if(StringLen(p09_report.reason) <= 0 || p09_report.reason == "VISUAL_SMOKE_RECONCILED")
         p09_report.reason = "PHASE09_PANEL_ERROR";
   }

   // Rebuild the census after the optional panel draw so the P09 object row can
   // represent final chart state in exported smoke artifacts.
   FP_HookP09BuildObjectCensus(p01_cfg, p02_cfg, p03_cfg, p04_cfg, p05_cfg, p06_cfg, p07_cfg, p08_cfg, p09_cfg,
                               p01_report, p02_report, p03_report, p04_report, p05_report, p06_report,
                               census, p09_report);
   FP_HookP09CheckPanelContract(p09_cfg, census, findings, p09_report);
   FP_HookP09FinalizeReport(p09_cfg, p09_report);

   bool exported_ok = true;
   if(p09_cfg.export_csv)
   {
      exported_ok = FP_HookP09ExportScenarios(p09_cfg, scenarios, p09_report) && exported_ok;
      exported_ok = FP_HookP09ExportCensus(p09_cfg, census, p09_report) && exported_ok;
      exported_ok = FP_HookP09ExportFindings(p09_cfg, findings, p09_report) && exported_ok;
      exported_ok = FP_HookP09ExportSummary(symbol, period, p09_cfg, p09_report) && exported_ok;

      if(!exported_ok)
      {
         p09_report.ok = false;
         p09_report.status = "HOOK_P09_FILE_ERROR";
         if(StringLen(p09_report.reason) <= 0 || p09_report.reason == "VISUAL_SMOKE_RECONCILED")
            p09_report.reason = "PHASE09_EXPORT_FILE_ERROR";
      }
   }

   if(p09_cfg.print_summary)
      FP_PrintHookPhase09Report("FP_HOOK_P09", p09_report);

   if(p09_cfg.print_samples)
      FP_PrintHookPhase09Findings("FP_HOOK_P09", findings, p09_cfg.sample_limit);
}

#endif // __FP_HOOK_PHASE09_ENGINE_MQH__
