#ifndef __FP_RUNTIME_HEALTH_SUMMARY_ENGINE_MQH__
#define __FP_RUNTIME_HEALTH_SUMMARY_ENGINE_MQH__
#property strict

#include "FP_RuntimeHealthSummaryExport.mqh"

void FP_RunConsolidation05RuntimeHealth(const string symbol,
                                        const ENUM_TIMEFRAMES period,
                                        const FP_Consolidation01NoSendContextConfig &context_cfg,
                                        const FP_Consolidation02FinalDecisionConfig &final_cfg,
                                        const FP_Consolidation04FinalCsvNormalizationConfig &normalization_cfg,
                                        const FP_Consolidation05RuntimeHealthConfig &cfg,
                                        FP_Consolidation05RuntimeHealthReport &report)
{
   FP_ResetConsolidation05RuntimeHealthReport(report);
   report.attempted = cfg.enabled;

   if(!cfg.enabled)
   {
      report.ok = true;
      report.status = "CONSOLIDATION05_RUNTIME_HEALTH_DISABLED";
      report.reason = "InpConsolidation05RuntimeHealthEnabled_false";
      return;
   }

   FP_Consolidation01NoSendContextRow ctx;
   FP_C01BuildNoSendContextRow(symbol, period, context_cfg, ctx);

   FP_Consolidation02FinalDecisionRow final_row;
   FP_C02BuildFinalDecisionRow(symbol, period, ctx, final_cfg, final_row);

   FP_Consolidation04FinalCsvNormalizationRow normalized_row;
   FP_C04BuildFinalCsvNormalizationRow(symbol, period, final_row, normalization_cfg, normalized_row);

   FP_Consolidation05RuntimeHealthRow row;
   FP_C05BuildRuntimeHealthRow(symbol, period, context_cfg, final_cfg, normalization_cfg,
                               ctx, final_row, normalized_row, cfg, row);

   bool export_ok = FP_C05ExportRuntimeHealth(cfg, row, report);

   report.ok = (export_ok && report.file_errors == 0);
   report.status = row.health_status;
   report.reason = row.health_block_reason;
}

void FP_PrintConsolidation05RuntimeHealthReport(const string tag,
                                                const FP_Consolidation05RuntimeHealthReport &report)
{
   string line = tag;
   line += " attempted=" + FP_C05Bool(report.attempted);
   line += " ok=" + FP_C05Bool(report.ok);
   line += " status=" + report.status;
   line += " reason=" + report.reason;
   line += " files_written=" + IntegerToString(report.files_written);
   line += " file_errors=" + IntegerToString(report.file_errors);
   line += " latest_written=" + FP_C05Bool(report.latest_written);
   line += " execution=NO";
   Print(line);
}

#endif // __FP_RUNTIME_HEALTH_SUMMARY_ENGINE_MQH__
