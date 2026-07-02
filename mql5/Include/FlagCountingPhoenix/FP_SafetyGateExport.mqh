#ifndef __FP_SAFETY_GATE_EXPORT_MQH__
#define __FP_SAFETY_GATE_EXPORT_MQH__
#property strict

#include "FP_SafetyGateRules.mqh"

string FP_L24SafetyGatePath(const FP_Level24SafetyGateConfig &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL24_SAFETY_GATE_DEFAULT_FOLDER;
   return folder + "\\state_gate_level24_safety_gate.csv";
}

string FP_L24SafetyGateHeader()
{
   string h = "";
   h += "generated_at,version,symbol,period,attempted,gate_passed,gate_status,gate_block_reason,gate_key";
   h += ",license_ok,symbol_allowed,timeframe_allowed,spread_ok,performance_ok,manual_arm_ok,real_execution_disabled_ok";
   h += ",current_spread_points,max_spread_points";
   h += ",performance_sample_total,performance_resolved_count,performance_target_count,performance_stop_count";
   h += ",performance_hit_rate_like,performance_avg_r_like,performance_best_r_like,performance_worst_r_like";
   h += ",min_resolved_samples,min_hit_rate_like,min_avg_r_like";
   h += ",allowed_symbols,allowed_timeframes,next_step,no_touch_contract,execution_status";
   return h;
}

string FP_L24SafetyGateRowCsv(const FP_Level24SafetyGateRow &r)
{
   string s = "";
   s += FP_L24SafeCsv(FP_L24Time(r.generated_at));
   s += "," + FP_L24SafeCsv(r.version);
   s += "," + FP_L24SafeCsv(r.symbol);
   s += "," + FP_L24SafeCsv(r.period_label);
   s += "," + FP_L24SafeCsv(FP_L24Bool(r.attempted));
   s += "," + FP_L24SafeCsv(FP_L24Bool(r.gate_passed));
   s += "," + FP_L24SafeCsv(r.gate_status);
   s += "," + FP_L24SafeCsv(r.gate_block_reason);
   s += "," + FP_L24SafeCsv(r.gate_key);

   s += "," + FP_L24SafeCsv(FP_L24Bool(r.license_ok));
   s += "," + FP_L24SafeCsv(FP_L24Bool(r.symbol_allowed));
   s += "," + FP_L24SafeCsv(FP_L24Bool(r.timeframe_allowed));
   s += "," + FP_L24SafeCsv(FP_L24Bool(r.spread_ok));
   s += "," + FP_L24SafeCsv(FP_L24Bool(r.performance_ok));
   s += "," + FP_L24SafeCsv(FP_L24Bool(r.manual_arm_ok));
   s += "," + FP_L24SafeCsv(FP_L24Bool(r.real_execution_disabled_ok));

   s += "," + IntegerToString(r.current_spread_points);
   s += "," + IntegerToString(r.max_spread_points);

   s += "," + IntegerToString(r.performance_sample_total);
   s += "," + IntegerToString(r.performance_resolved_count);
   s += "," + IntegerToString(r.performance_target_count);
   s += "," + IntegerToString(r.performance_stop_count);
   s += "," + DoubleToString(r.performance_hit_rate_like, 4);
   s += "," + DoubleToString(r.performance_avg_r_like, 4);
   s += "," + DoubleToString(r.performance_best_r_like, 4);
   s += "," + DoubleToString(r.performance_worst_r_like, 4);

   s += "," + IntegerToString(r.min_resolved_samples);
   s += "," + DoubleToString(r.min_hit_rate_like, 4);
   s += "," + DoubleToString(r.min_avg_r_like, 4);

   s += "," + FP_L24SafeCsv(r.allowed_symbols);
   s += "," + FP_L24SafeCsv(r.allowed_timeframes);
   s += "," + FP_L24SafeCsv(r.next_step);
   s += "," + FP_L24SafeCsv(r.no_touch_contract);
   s += "," + FP_L24SafeCsv(r.execution_status);
   return s;
}

bool FP_L24ExportSafetyGate(const FP_Level24SafetyGateConfig &cfg,
                            const FP_Level24SafetyGateRow &row,
                            FP_Level24SafetyGateReport &report)
{
   if(!cfg.export_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL24_SAFETY_GATE_DEFAULT_FOLDER;
   FolderCreate(folder);

   int handle = FileOpen(FP_L24SafetyGatePath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "level24_safety_gate_export_open_failed";
      return false;
   }

   FileWriteString(handle, FP_L24SafetyGateHeader() + "\r\n");
   FileWriteString(handle, FP_L24SafetyGateRowCsv(row) + "\r\n");
   FileClose(handle);

   report.files_written++;
   report.safety_gate_written = true;
   return true;
}

#endif // __FP_SAFETY_GATE_EXPORT_MQH__
