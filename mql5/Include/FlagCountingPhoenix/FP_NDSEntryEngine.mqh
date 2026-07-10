#ifndef __FP_NDS_ENTRY_ENGINE_MQH__
#define __FP_NDS_ENTRY_ENGINE_MQH__
#property strict

#include "FP_NDSEntryExport.mqh"

void FP_RunNDSEntryPipeline(const string symbol,
                            const ENUM_TIMEFRAMES period,
                            const MqlRates &rates[],
                            const int bars,
                            const FP_NDSEntryConfig &cfg,
                            FP_NDSEntryReport &report)
{
   FP_ResetNDSEntryReport(report);
   report.attempted = cfg.enabled;

   if(!cfg.enabled)
   {
      report.ok = true;
      report.status = "NDS_ENTRY_PIPELINE_DISABLED";
      report.reason = "InpNDSEntryEnabled_false";
      return;
   }

   FP_NDSEntryPipelineRow row;
   FP_NDSBuildEntryPipelineRow(symbol, period, rates, bars, cfg, row);
   bool export_ok = FP_NDSExportEntryPipeline(cfg, row, report);

   report.ok = (export_ok && report.file_errors == 0);
   report.status = row.status;
   report.reason = row.block_reason;
}

void FP_PrintNDSEntryReport(const string tag,
                            const FP_NDSEntryReport &report)
{
   string line = tag;
   line += " attempted=" + FP_NDSEntryBool(report.attempted);
   line += " ok=" + FP_NDSEntryBool(report.ok);
   line += " status=" + report.status;
   line += " reason=" + report.reason;
   line += " files_written=" + IntegerToString(report.files_written);
   line += " file_errors=" + IntegerToString(report.file_errors);
   line += " command_written=" + FP_NDSEntryBool(report.command_written);
   line += " send_allowed=false";
   Print(line);
}

#endif // __FP_NDS_ENTRY_ENGINE_MQH__
