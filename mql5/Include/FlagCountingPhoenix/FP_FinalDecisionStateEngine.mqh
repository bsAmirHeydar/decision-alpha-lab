#ifndef __FP_FINAL_DECISION_STATE_ENGINE_MQH__
#define __FP_FINAL_DECISION_STATE_ENGINE_MQH__
#property strict

#include "FP_FinalDecisionStateExport.mqh"

void FP_RunConsolidation02FinalDecision(const string symbol,
                                        const ENUM_TIMEFRAMES period,
                                        const FP_Consolidation01NoSendContextConfig &context_cfg,
                                        const FP_Consolidation02FinalDecisionConfig &cfg,
                                        FP_Consolidation02FinalDecisionReport &report)
{
   FP_ResetConsolidation02FinalDecisionReport(report);
   report.attempted = cfg.enabled;

   if(!cfg.enabled)
   {
      report.ok = true;
      report.status = "CONSOLIDATION02_FINAL_DECISION_DISABLED";
      report.reason = "InpConsolidation02FinalDecisionEnabled_false";
      return;
   }

   FP_Consolidation01NoSendContextRow ctx;
   FP_C01BuildNoSendContextRow(symbol, period, context_cfg, ctx);

   FP_Consolidation02FinalDecisionRow row;
   FP_C02BuildFinalDecisionRow(symbol, period, ctx, cfg, row);

   bool export_ok = FP_C02ExportFinalDecision(cfg, row, report);

   report.ok = (export_ok && report.file_errors == 0);
   report.status = row.decision_state;
   report.reason = row.decision_block_reason;
}

void FP_PrintConsolidation02FinalDecisionReport(const string tag,
                                                const FP_Consolidation02FinalDecisionReport &report)
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

#endif // __FP_FINAL_DECISION_STATE_ENGINE_MQH__
