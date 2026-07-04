#ifndef __FP_HOOK_PHASE10_ENGINE_MQH__
#define __FP_HOOK_PHASE10_ENGINE_MQH__
#property strict

#include "FP_HookPhase10Export.mqh"

void FP_RunHookPhase10(const string symbol,
                       const ENUM_TIMEFRAMES period,
                       const FP_HookPhase07Config &p07_cfg,
                       const FP_HookPhase10Config &p10_cfg,
                       const FP_HookPhase06Report &p06_report,
                       const FP_HookPhase08Report &p08_report,
                       const FP_HookPhase09Report &p09_report,
                       FP_HookPhase10Report &p10_report)
{
   FP_ResetHookPhase10Report(p10_report);
   p10_report.display_family = p10_cfg.display_family;
   p10_report.view_profile = p07_cfg.view_profile;
   p10_report.freeze_mode = p10_cfg.freeze_mode;
   p10_report.contract_id = FP_HookP10BuildContractId(symbol, period, p10_cfg, p07_cfg);

   if(!FP_HookP10ShouldRun(p10_cfg))
   {
      p10_report.ok = true;
      p10_report.freeze_ready = false;
      p10_report.status = "HOOK_P10_SKIPPED";
      if(!p10_cfg.enabled)
         p10_report.reason = "PHASE10_DISABLED";
      else
         p10_report.reason = "RALLY_ONLY_FREEZE_NOT_ALLOWED";
      return;
   }

   p10_report.attempted = true;

   FP_HookPhase10ContractRow contracts[];
   FP_HookPhase10TrainingSchemaRow schema[];

   FP_HookP10BuildTrainingSchema(schema, p10_report);
   FP_HookP10EvaluateContract(p10_cfg, p07_cfg, p08_report, p09_report, p06_report, contracts, p10_report);
   FP_HookP10FinalizeReport(p10_cfg, p10_report);

   bool exported_ok = true;
   if(p10_cfg.export_csv)
   {
      exported_ok = FP_HookP10ExportContracts(p10_cfg, contracts, p10_report) && exported_ok;
      exported_ok = FP_HookP10ExportSchema(p10_cfg, schema, p10_report) && exported_ok;
      exported_ok = FP_HookP10ExportManifest(symbol, period, p10_cfg, p10_report) && exported_ok;
      exported_ok = FP_HookP10ExportSummary(symbol, period, p10_cfg, p10_report) && exported_ok;

      if(!exported_ok)
      {
         p10_report.ok = false;
         p10_report.freeze_ready = false;
         p10_report.status = "HOOK_P10_FILE_ERROR";
         if(StringLen(p10_report.reason) <= 0 || p10_report.reason == "FREEZE_CONTRACT_RECONCILED")
            p10_report.reason = "PHASE10_EXPORT_FILE_ERROR";
      }
   }

   if(p10_cfg.print_summary)
      FP_PrintHookPhase10Report("FP_HOOK_P10", p10_report);

   if(p10_cfg.print_samples)
      FP_PrintHookPhase10Contracts("FP_HOOK_P10", contracts, p10_cfg.sample_limit);
}

#endif // __FP_HOOK_PHASE10_ENGINE_MQH__
