#ifndef __FP_HOOK_PHASE01_EXPORT_MQH__
#define __FP_HOOK_PHASE01_EXPORT_MQH__
#property strict

#include "FP_HookPhase01Visual.mqh"

string FP_HookP01SafeCsv(string s)
{
   StringReplace(s, "\"", "\"\"");
   return "\"" + s + "\"";
}

string FP_HookP01NodePath(const FP_HookPhase01Config &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_HOOK_P01_DEFAULT_FOLDER;
   return folder + "\\hook_phase01_nodes.csv";
}

string FP_HookP01SummaryPath(const FP_HookPhase01Config &cfg)
{
   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_HOOK_P01_DEFAULT_FOLDER;
   return folder + "\\hook_phase01_summary.csv";
}

string FP_HookP01NodeHeader()
{
   return "schema_version,version,node_id,node_type,scale_l,bar_index,bar_time,price,high,low,confirmed,source";
}

string FP_HookP01NodeRow(const FP_HookPhase01Node &n)
{
   string s = "";
   s += FP_HookP01SafeCsv(FP_HOOK_P01_SCHEMA_VERSION);
   s += "," + FP_HookP01SafeCsv(FP_HOOK_P01_VERSION);
   s += "," + IntegerToString(n.node_id);
   s += "," + FP_HookP01SafeCsv(FP_HookP01NodeTypeName(n.node_type));
   s += "," + IntegerToString(n.scale_l);
   s += "," + IntegerToString(n.bar_index);
   s += "," + FP_HookP01SafeCsv(TimeToString(n.bar_time, TIME_DATE|TIME_SECONDS));
   s += "," + DoubleToString(n.price, _Digits);
   s += "," + DoubleToString(n.high, _Digits);
   s += "," + DoubleToString(n.low, _Digits);
   s += "," + FP_HookP01SafeCsv(FP_HookP01BoolName(n.confirmed));
   s += "," + FP_HookP01SafeCsv(n.source);
   return s;
}

string FP_HookP01SummaryHeader()
{
   return "schema_version,version,symbol,period,display_family,bars_seen,bars_scanned,scales_seen,scales_scanned,total_nodes,peak_nodes,valley_nodes,nodes_drawn,status,reason";
}

string FP_HookP01SummaryRow(const string symbol,
                            const ENUM_TIMEFRAMES period,
                            const FP_HookPhase01Config &cfg,
                            const FP_HookPhase01Report &r)
{
   string s = "";
   s += FP_HookP01SafeCsv(FP_HOOK_P01_SCHEMA_VERSION);
   s += "," + FP_HookP01SafeCsv(FP_HOOK_P01_VERSION);
   s += "," + FP_HookP01SafeCsv(symbol);
   s += "," + FP_HookP01SafeCsv(EnumToString(period));
   s += "," + FP_HookP01SafeCsv(FP_HookP01DisplayFamilyName(cfg.display_family));
   s += "," + IntegerToString(r.bars_seen);
   s += "," + IntegerToString(r.bars_scanned);
   s += "," + IntegerToString(r.scales_seen);
   s += "," + IntegerToString(r.scales_scanned);
   s += "," + IntegerToString(r.total_nodes);
   s += "," + IntegerToString(r.peak_nodes);
   s += "," + IntegerToString(r.valley_nodes);
   s += "," + IntegerToString(r.nodes_drawn);
   s += "," + FP_HookP01SafeCsv(r.status);
   s += "," + FP_HookP01SafeCsv(r.reason);
   return s;
}

bool FP_HookP01ExportNodes(const FP_HookPhase01Config &cfg,
                           const FP_HookPhase01Node &nodes[],
                           FP_HookPhase01Report &report)
{
   if(!cfg.export_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_HOOK_P01_DEFAULT_FOLDER;
   FolderCreate(folder);

   int handle = FileOpen(FP_HookP01NodePath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "HOOK_P01_NODE_EXPORT_OPEN_FAILED";
      return false;
   }

   FileWriteString(handle, FP_HookP01NodeHeader() + "\r\n");
   for(int i=0; i<ArraySize(nodes); i++)
      FileWriteString(handle, FP_HookP01NodeRow(nodes[i]) + "\r\n");
   FileClose(handle);
   report.files_written++;
   return true;
}

bool FP_HookP01ExportSummary(const string symbol,
                             const ENUM_TIMEFRAMES period,
                             const FP_HookPhase01Config &cfg,
                             FP_HookPhase01Report &report)
{
   if(!cfg.export_csv)
      return true;

   string folder = cfg.folder;
   if(StringLen(folder) <= 0)
      folder = FP_HOOK_P01_DEFAULT_FOLDER;
   FolderCreate(folder);

   int handle = FileOpen(FP_HookP01SummaryPath(cfg), FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = "HOOK_P01_SUMMARY_EXPORT_OPEN_FAILED";
      return false;
   }

   FileWriteString(handle, FP_HookP01SummaryHeader() + "\r\n");
   FileWriteString(handle, FP_HookP01SummaryRow(symbol, period, cfg, report) + "\r\n");
   FileClose(handle);
   report.files_written++;
   return true;
}

#endif // __FP_HOOK_PHASE01_EXPORT_MQH__
