#ifndef __FP_PAPER_PERFORMANCE_EXPORT_MQH__
#define __FP_PAPER_PERFORMANCE_EXPORT_MQH__
#property strict

#include "FP_PaperPerformanceRules.mqh"

string FP_L23PaperPerformancePath(const FP_Level23PaperPerformanceConfig &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL23_PAPER_PERFORMANCE_DEFAULT_FOLDER;
   return folder + "\\state_gate_level23_paper_performance.csv";
}

string FP_L23PaperPerformanceHeader()
{
   string h = "";
   h += "generated_at,version,symbol,period,attempted,updated,duplicate_skipped,performance_status,performance_key";
   h += ",current_lifecycle_id,current_lifecycle_status,current_outcome_class,current_r_like,current_bars_elapsed";
   h += ",sample_total,counted_total,duplicate_total,blocked_count,tracked_count,entered_count,target_count,stop_count,expired_count,open_count,ambiguous_count,resolved_count";
   h += ",win_like_count,loss_like_count,neutral_like_count,hit_rate_like,loss_rate_like,avg_r_like,best_r_like,worst_r_like,sum_r_like";
   h += ",no_touch_contract,execution_status";
   return h;
}

string FP_L23PaperPerformanceRowCsv(const FP_Level23PaperPerformanceRow &r)
{
   string s = "";
   s += FP_L23SafeCsv(FP_L23Time(r.generated_at));
   s += "," + FP_L23SafeCsv(r.version);
   s += "," + FP_L23SafeCsv(r.symbol);
   s += "," + FP_L23SafeCsv(r.period_label);
   s += "," + FP_L23SafeCsv(FP_L23Bool(r.attempted));
   s += "," + FP_L23SafeCsv(FP_L23Bool(r.updated));
   s += "," + FP_L23SafeCsv(FP_L23Bool(r.duplicate_skipped));
   s += "," + FP_L23SafeCsv(r.performance_status);
   s += "," + FP_L23SafeCsv(r.performance_key);

   s += "," + FP_L23SafeCsv(r.current_lifecycle_id);
   s += "," + FP_L23SafeCsv(r.current_lifecycle_status);
   s += "," + FP_L23SafeCsv(r.current_outcome_class);
   s += "," + DoubleToString(r.current_r_like, 4);
   s += "," + IntegerToString(r.current_bars_elapsed);

   s += "," + IntegerToString(r.sample_total);
   s += "," + IntegerToString(r.counted_total);
   s += "," + IntegerToString(r.duplicate_total);
   s += "," + IntegerToString(r.blocked_count);
   s += "," + IntegerToString(r.tracked_count);
   s += "," + IntegerToString(r.entered_count);
   s += "," + IntegerToString(r.target_count);
   s += "," + IntegerToString(r.stop_count);
   s += "," + IntegerToString(r.expired_count);
   s += "," + IntegerToString(r.open_count);
   s += "," + IntegerToString(r.ambiguous_count);
   s += "," + IntegerToString(r.resolved_count);

   s += "," + IntegerToString(r.win_like_count);
   s += "," + IntegerToString(r.loss_like_count);
   s += "," + IntegerToString(r.neutral_like_count);
   s += "," + DoubleToString(r.hit_rate_like, 4);
   s += "," + DoubleToString(r.loss_rate_like, 4);
   s += "," + DoubleToString(r.avg_r_like, 4);
   s += "," + DoubleToString(r.best_r_like, 4);
   s += "," + DoubleToString(r.worst_r_like, 4);
   s += "," + DoubleToString(r.sum_r_like, 4);

   s += "," + FP_L23SafeCsv(r.no_touch_contract);
   s += "," + FP_L23SafeCsv(r.execution_status);
   return s;
}

bool FP_L23ExportPaperPerformance(const FP_Level23PaperPerformanceConfig &cfg,
                                  const FP_Level23PaperPerformanceRow &row,
                                  FP_Level23PaperPerformanceReport &report)
{
   if(!cfg.export_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_LEVEL23_PAPER_PERFORMANCE_DEFAULT_FOLDER;
   FolderCreate(folder);

   int handle = FileOpen(FP_L23PaperPerformancePath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "level23_paper_performance_export_open_failed";
      return false;
   }

   FileWriteString(handle, FP_L23PaperPerformanceHeader() + "\r\n");
   FileWriteString(handle, FP_L23PaperPerformanceRowCsv(row) + "\r\n");
   FileClose(handle);

   report.files_written++;
   report.performance_written = true;
   return true;
}

#endif // __FP_PAPER_PERFORMANCE_EXPORT_MQH__
