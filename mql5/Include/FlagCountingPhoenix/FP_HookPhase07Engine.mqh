#ifndef __FP_HOOK_PHASE07_ENGINE_MQH__
#define __FP_HOOK_PHASE07_ENGINE_MQH__
#property strict

#include "FP_HookPhase07Export.mqh"

void FP_ApplyHookPhase07Profile(const FP_HookPhase07Config &cfg,
                                FP_HookPhase01Config &p01,
                                FP_HookPhase02Config &p02,
                                FP_HookPhase03Config &p03,
                                FP_HookPhase04Config &p04,
                                FP_HookPhase05Config &p05,
                                FP_HookPhase06Config &p06,
                                FP_HookPhase07Report &report)
{
   FP_ResetHookPhase07Report(report);

   if(!FP_HookP07ShouldRun(cfg))
   {
      report.ok = true;
      report.status = "HOOK_P07_SKIPPED";
      report.reason = "PHASE07_DISABLED";
      FP_HookP07FillReportFromConfigs(cfg, p01, p02, p03, p04, p05, p06, report);
      return;
   }

   report.attempted = true;

   report.objects_deleted += FP_HookP07CleanObjects(cfg, p01, p02, p03, p04, p05, p06);

   FP_HookP07ApplyDisplayFamily(cfg, p01, p02, p03, p04, p05, p06);
   FP_HookP07ForceEnablePhases(cfg, p01, p02, p03, p04, p05, p06);
   FP_HookP07ApplyProfileDrawing(cfg, p01, p02, p03, p04, p05, p06);
   FP_HookP07ApplyGlobalLabels(cfg, p01, p02, p03, p04, p05, p06);
   FP_HookP07ApplyDrawBudgets(cfg, p01, p02, p03, p04, p05, p06);
   FP_HookP07ApplyGlobalAuditFlags(cfg, p01, p02, p03, p04, p05, p06);

   report.profiles_applied = 1;
   report.ok = true;
   report.status = "HOOK_P07_OK";
   report.reason = "HOOK_VIEW_PROFILE_APPLIED";

   FP_HookP07FillReportFromConfigs(cfg, p01, p02, p03, p04, p05, p06, report);

   if(cfg.export_profile_csv)
      FP_HookP07ExportProfile(cfg, report);

   if(cfg.print_summary)
      FP_PrintHookPhase07Report("FP_HOOK_P07", report);
}

#endif // __FP_HOOK_PHASE07_ENGINE_MQH__
