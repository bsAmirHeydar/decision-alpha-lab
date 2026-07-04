#ifndef __FP_HOOK_PHASE01_RULES_MQH__
#define __FP_HOOK_PHASE01_RULES_MQH__
#property strict

#include "FP_HookPhase01Types.mqh"

bool FP_HookP01ShouldRun(const FP_HookPhase01Config &cfg)
{
   if(!cfg.enabled)
      return false;
   if(cfg.display_family == FP_NDS_HOOK_DISPLAY_RALLY_ONLY)
      return false;
   return true;
}

int FP_HookP01BarsToScan(const int copied, const FP_HookPhase01Config &cfg)
{
   if(copied <= 0)
      return 0;
   if(cfg.max_bars_to_scan <= 0 || cfg.max_bars_to_scan >= copied)
      return copied;
   return cfg.max_bars_to_scan;
}

bool FP_HookP01IsStrictPeak(const MqlRates &rates[], const int copied, const int index, const int L)
{
   if(L < 1) return false;
   if(index - L < 0) return false;
   if(index + L >= copied) return false;

   double v = rates[index].high;
   for(int i=index-L; i<=index+L; i++)
   {
      if(i == index) continue;
      if(rates[i].high >= v)
         return false;
   }
   return true;
}

bool FP_HookP01IsStrictValley(const MqlRates &rates[], const int copied, const int index, const int L)
{
   if(L < 1) return false;
   if(index - L < 0) return false;
   if(index + L >= copied) return false;

   double v = rates[index].low;
   for(int i=index-L; i<=index+L; i++)
   {
      if(i == index) continue;
      if(rates[i].low <= v)
         return false;
   }
   return true;
}

bool FP_HookP01AppendNode(FP_HookPhase01Node &nodes[],
                         const FP_HookPhase01Node &node,
                         const int max_nodes)
{
   int n = ArraySize(nodes);
   if(max_nodes > 0 && n >= max_nodes)
      return false;

   ArrayResize(nodes, n + 1);
   nodes[n] = node;
   return true;
}

void FP_HookP01BuildNode(FP_HookPhase01NodeType node_type,
                         const int node_id,
                         const int scale_l,
                         const int bar_index,
                         const MqlRates &rate,
                         FP_HookPhase01Node &out)
{
   FP_ResetHookPhase01Node(out);
   out.node_id = node_id;
   out.scale_l = scale_l;
   out.bar_index = bar_index;
   out.bar_time = rate.time;
   out.high = rate.high;
   out.low = rate.low;
   out.node_type = node_type;
   out.confirmed = true;
   out.source = "HOOK_P01_STRICT_SWING_ADAPTER";

   if(node_type == FP_HOOK_P01_NODE_PEAK)
      out.price = rate.high;
   else
      out.price = rate.low;
}

void FP_HookP01UpdateSummary(const FP_HookPhase01Node &node,
                             FP_HookPhase01ScaleSummary &summary,
                             FP_HookPhase01Report &report)
{
   summary.total++;
   report.total_nodes++;

   if(node.node_type == FP_HOOK_P01_NODE_PEAK)
   {
      summary.peaks++;
      report.peak_nodes++;
   }
   else if(node.node_type == FP_HOOK_P01_NODE_VALLEY)
   {
      summary.valleys++;
      report.valley_nodes++;
   }
}

int FP_HookP01ScanScale(const MqlRates &rates[],
                        const int copied,
                        const int scale_l,
                        const int scan_start,
                        const FP_HookPhase01Config &cfg,
                        FP_HookPhase01Node &nodes[],
                        FP_HookPhase01ScaleSummary &summary,
                        FP_HookPhase01Report &report)
{
   FP_ResetHookPhase01ScaleSummary(summary);
   summary.scale_l = scale_l;

   if(scale_l < 1)
      return 0;
   if(copied <= (scale_l * 2 + 1))
      return 0;

   int added = 0;
   int first = scan_start;
   if(first < scale_l)
      first = scale_l;

   int last = copied - scale_l - 1;
   if(last < first)
      return 0;

   for(int i=first; i<=last; i++)
   {
      if(cfg.show_peaks && FP_HookP01IsStrictPeak(rates, copied, i, scale_l))
      {
         FP_HookPhase01Node node;
         FP_HookP01BuildNode(FP_HOOK_P01_NODE_PEAK, ArraySize(nodes), scale_l, i, rates[i], node);
         if(FP_HookP01AppendNode(nodes, node, cfg.max_nodes))
         {
            FP_HookP01UpdateSummary(node, summary, report);
            added++;
         }
      }

      if(cfg.show_valleys && FP_HookP01IsStrictValley(rates, copied, i, scale_l))
      {
         FP_HookPhase01Node node;
         FP_HookP01BuildNode(FP_HOOK_P01_NODE_VALLEY, ArraySize(nodes), scale_l, i, rates[i], node);
         if(FP_HookP01AppendNode(nodes, node, cfg.max_nodes))
         {
            FP_HookP01UpdateSummary(node, summary, report);
            added++;
         }
      }
   }

   return added;
}

int FP_HookP01BuildNodes(const MqlRates &rates[],
                         const int copied,
                         const int &scales[],
                         const int scale_count,
                         const FP_HookPhase01Config &cfg,
                         FP_HookPhase01Node &nodes[],
                         FP_HookPhase01ScaleSummary &summaries[],
                         FP_HookPhase01Report &report)
{
   ArrayResize(nodes, 0);
   ArrayResize(summaries, 0);

   report.bars_seen = copied;
   report.scales_seen = scale_count;

   int bars_to_scan = FP_HookP01BarsToScan(copied, cfg);
   report.bars_scanned = bars_to_scan;
   if(bars_to_scan <= 0)
      return 0;

   int scan_start = copied - bars_to_scan;
   if(scan_start < 0)
      scan_start = 0;

   int total_added = 0;
   for(int s=0; s<scale_count; s++)
   {
      int L = scales[s];
      if(L < 2)
         L = 2;

      FP_HookPhase01ScaleSummary summary;
      int added = FP_HookP01ScanScale(rates, copied, L, scan_start, cfg, nodes, summary, report);
      if(added > 0 || L >= 2)
      {
         int n = ArraySize(summaries);
         ArrayResize(summaries, n + 1);
         summaries[n] = summary;
         report.scales_scanned++;
      }
      total_added += added;
   }

   return total_added;
}

void FP_HookP01FinalizeReport(FP_HookPhase01Report &report)
{
   report.ok = true;
   report.status = "HOOK_P01_OK";
   report.reason = "NODE_SOURCE_ADAPTER_BUILT";

   if(report.total_nodes <= 0)
   {
      report.status = "HOOK_P01_NO_NODES";
      report.reason = "NO_STRICT_PEAKS_OR_VALLEYS_FOUND_FOR_SELECTED_SCALES";
   }
}

void FP_PrintHookPhase01Report(const string tag, const FP_HookPhase01Report &r)
{
   Print(tag,
         " status=", r.status,
         " reason=", r.reason,
         " attempted=", FP_HookP01BoolName(r.attempted),
         " ok=", FP_HookP01BoolName(r.ok),
         " bars_seen=", r.bars_seen,
         " bars_scanned=", r.bars_scanned,
         " scales_seen=", r.scales_seen,
         " scales_scanned=", r.scales_scanned,
         " total_nodes=", r.total_nodes,
         " peaks=", r.peak_nodes,
         " valleys=", r.valley_nodes,
         " drawn=", r.nodes_drawn,
         " files=", r.files_written,
         " file_errors=", r.file_errors);
}

void FP_PrintHookPhase01Samples(const string tag,
                                const FP_HookPhase01Node &nodes[],
                                const int sample_limit)
{
   int n = ArraySize(nodes);
   int limit = sample_limit;
   if(limit <= 0 || limit > n)
      limit = n;

   for(int i=0; i<limit; i++)
   {
      FP_HookPhase01Node node = nodes[i];
      Print(tag,
            " sample=", i,
            " node_id=", node.node_id,
            " type=", FP_HookP01NodeTypeName(node.node_type),
            " L=", node.scale_l,
            " bar=", node.bar_index,
            " time=", TimeToString(node.bar_time, TIME_DATE|TIME_SECONDS),
            " price=", DoubleToString(node.price, _Digits));
   }
}

#endif // __FP_HOOK_PHASE01_RULES_MQH__
