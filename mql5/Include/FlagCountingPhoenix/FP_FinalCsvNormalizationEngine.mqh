#ifndef __FP_FINAL_CSV_NORMALIZATION_ENGINE_MQH__
#define __FP_FINAL_CSV_NORMALIZATION_ENGINE_MQH__
#property strict

#include "FP_FinalCsvNormalizationExport.mqh"

void FP_RunConsolidation04FinalCsvNormalization(const string symbol,
                                                const ENUM_TIMEFRAMES period,
                                                const FP_Consolidation01NoSendContextConfig &context_cfg,
                                                const FP_Consolidation02FinalDecisionConfig &final_cfg,
                                                const FP_Consolidation04FinalCsvNormalizationConfig &cfg,
                                                FP_Consolidation04FinalCsvNormalizationReport &report)
{
   FP_ResetConsolidation04FinalCsvNormalizationReport(report);
   report.attempted = cfg.enabled;

   if(!cfg.enabled)
   {
      report.ok = true;
      report.status = "CONSOLIDATION04_FINAL_CSV_NORMALIZATION_DISABLED";
      report.reason = "InpConsolidation04FinalCsvNormalizationEnabled_false";
      return;
   }

   FP_Consolidation01NoSendContextRow ctx;
   FP_C01BuildNoSendContextRow(symbol, period, context_cfg, ctx);

   FP_Consolidation02FinalDecisionRow final_row;
   FP_C02BuildFinalDecisionRow(symbol, period, ctx, final_cfg, final_row);

   FP_Consolidation04FinalCsvNormalizationRow row;
   FP_C04BuildFinalCsvNormalizationRow(symbol, period, final_row, cfg, row);

   bool export_ok = FP_C04ExportFinalCsvNormalization(cfg, row, report);

   report.ok = (export_ok && report.file_errors == 0);
   report.status = row.normalized_quality_status;
   report.reason = row.normalized_block_reason;
}

void FP_PrintConsolidation04FinalCsvNormalizationReport(const string tag,
                                                        const FP_Consolidation04FinalCsvNormalizationReport &report)
{
   string line = tag;
   line += " attempted=" + FP_C02Bool(report.attempted);
   line += " ok=" + FP_C02Bool(report.ok);
   line += " status=" + report.status;
   line += " reason=" + report.reason;
   line += " files_written=" + IntegerToString(report.files_written);
   line += " file_errors=" + IntegerToString(report.file_errors);
   line += " latest_written=" + FP_C02Bool(report.latest_written);
   line += " execution=NO";
   Print(line);
}

#endif // __FP_FINAL_CSV_NORMALIZATION_ENGINE_MQH__
