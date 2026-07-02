#ifndef __FP_SAFETY_GATE_ENGINE_MQH__
#define __FP_SAFETY_GATE_ENGINE_MQH__
#property strict

#include "FP_SafetyGateExport.mqh"

void FP_RunLevel24SafetyGate(const string symbol,
                             const ENUM_TIMEFRAMES period,
                             const bool license_ok,
                             const FP_Level24SafetyGateConfig &cfg,
                             FP_Level24SafetyGateReport &report)
{
   FP_ResetLevel24SafetyGateReport(report);
   report.attempted = cfg.enabled;

   if(!cfg.enabled)
   {
      report.ok = true;
      report.status = "LEVEL24_SAFETY_GATE_DISABLED";
      report.reason = "InpLevel24SafetyGateEnabled_false";
      return;
   }

   FP_Level24SafetyGateRow row;
   FP_L24BuildSafetyGateRow(symbol, period, license_ok, cfg, row);

   bool export_ok = FP_L24ExportSafetyGate(cfg, row, report);

   report.ok = (export_ok && report.file_errors == 0);
   report.status = row.gate_status;
   report.reason = row.gate_block_reason;
}

void FP_PrintLevel24SafetyGateReport(const string tag,
                                     const FP_Level24SafetyGateReport &report)
{
   string line = tag;
   line += " attempted=" + FP_L24Bool(report.attempted);
   line += " ok=" + FP_L24Bool(report.ok);
   line += " status=" + report.status;
   line += " reason=" + report.reason;
   line += " files_written=" + IntegerToString(report.files_written);
   line += " file_errors=" + IntegerToString(report.file_errors);
   line += " safety_gate_written=" + FP_L24Bool(report.safety_gate_written);
   line += " execution=NO";
   Print(line);
}

#endif // __FP_SAFETY_GATE_ENGINE_MQH__
