#ifndef __FP_NO_SEND_CONTEXT_ENGINE_MQH__
#define __FP_NO_SEND_CONTEXT_ENGINE_MQH__
#property strict

#include "FP_NoSendContextExport.mqh"

void FP_RunConsolidation01NoSendContext(const string symbol,
                                        const ENUM_TIMEFRAMES period,
                                        const FP_Consolidation01NoSendContextConfig &cfg,
                                        FP_Consolidation01NoSendContextReport &report)
{
   FP_ResetConsolidation01NoSendContextReport(report);
   report.attempted = cfg.enabled;

   if(!cfg.enabled)
   {
      report.ok = true;
      report.status = "CONSOLIDATION01_NO_SEND_CONTEXT_DISABLED";
      report.reason = "InpConsolidation01NoSendContextEnabled_false";
      return;
   }

   FP_Consolidation01NoSendContextRow row;
   FP_C01BuildNoSendContextRow(symbol, period, cfg, row);

   bool export_ok = FP_C01ExportNoSendContext(cfg, row, report);

   report.ok = (export_ok && report.file_errors == 0);
   report.status = row.context_status;
   report.reason = row.context_block_reason;
}

void FP_PrintConsolidation01NoSendContextReport(const string tag,
                                                const FP_Consolidation01NoSendContextReport &report)
{
   string line = tag;
   line += " attempted=" + FP_C01Bool(report.attempted);
   line += " ok=" + FP_C01Bool(report.ok);
   line += " status=" + report.status;
   line += " reason=" + report.reason;
   line += " files_written=" + IntegerToString(report.files_written);
   line += " file_errors=" + IntegerToString(report.file_errors);
   line += " latest_written=" + FP_C01Bool(report.latest_written);
   line += " execution=NO";
   Print(line);
}

#endif // __FP_NO_SEND_CONTEXT_ENGINE_MQH__
