#ifndef __SF11_STATISTICS_EXPORTER_MQH__
#define __SF11_STATISTICS_EXPORTER_MQH__
#include "SF11_ReportManifest.mqh"
class CSF11StatisticsExporter
{
public:
   bool WriteSummaryCsv(const string filename,const SF11_StatisticSummary &rows[],string &error) const
   {
      const int h=FileOpen(filename,FILE_WRITE|FILE_CSV|FILE_COMMON|FILE_ANSI,',');if(h==INVALID_HANDLE){error="cannot open statistics CSV: "+IntegerToString(GetLastError());return false;}
      FileWrite(h,"group_key","sample_count","filled_count","unique_events","unique_clusters","fill_rate","win_rate","mean_net_r","median_net_r","std_r","se_r","profit_factor","total_net_r","max_drawdown_r","avg_mfe_r","avg_mae_r","avg_holding_seconds","q05","q25","q75","q95","best_trade_r","worst_trade_r","best_trade_share","status","summary_hash");
      for(int i=0;i<ArraySize(rows);i++){const SF11_StatisticSummary s=rows[i];FileWrite(h,s.group_key,s.sample_count,s.filled_count,s.unique_event_count,s.unique_cluster_count,s.fill_rate,s.win_rate,s.mean_net_r,s.median_net_r,s.standard_deviation_r,s.standard_error_r,s.profit_factor,s.total_net_r,s.maximum_drawdown_r,s.average_mfe_r,s.average_mae_r,s.average_holding_seconds,s.q05_net_r,s.q25_net_r,s.q75_net_r,s.q95_net_r,s.best_trade_r,s.worst_trade_r,s.best_trade_share,(int)s.status,s.summary_hash);}FileClose(h);error="";return true;
   }
   bool WriteIntervalCsv(const string filename,const SF11_ConfidenceInterval &rows[],string &error) const
   {
      const int h=FileOpen(filename,FILE_WRITE|FILE_CSV|FILE_COMMON|FILE_ANSI,',');if(h==INVALID_HANDLE){error="cannot open interval CSV: "+IntegerToString(GetLastError());return false;}FileWrite(h,"metric_id","group_key","kind","confidence_level","estimate","lower","upper","standard_error","effective_sample_count","seed","interval_hash");
      for(int i=0;i<ArraySize(rows);i++){const SF11_ConfidenceInterval r=rows[i];FileWrite(h,r.metric_id,r.group_key,(int)r.kind,r.confidence_level,r.estimate,r.lower,r.upper,r.standard_error,r.effective_sample_count,r.seed,r.interval_hash);}FileClose(h);error="";return true;
   }
};
#endif
