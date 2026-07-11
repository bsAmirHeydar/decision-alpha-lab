#ifndef __SF11_GROUP_ACCUMULATOR_MQH__
#define __SF11_GROUP_ACCUMULATOR_MQH__
#include "SF11_StatisticSummary.mqh"
class CSF11GroupAccumulator
{
private:
   string m_group_key;long m_sample_count;long m_filled;long m_wins;long m_losses;long m_flats;
   string m_events[];string m_clusters[];CSF11StreamingMoments m_net;CSF11StreamingMoments m_mfe;CSF11StreamingMoments m_mae;
   CSF11StreamingMoments m_holding;CSF11DrawdownTracker m_drawdown;CSF11BoundedQuantiles m_quantiles;
   double m_positive;double m_negative_abs;double m_total;double m_best;double m_worst;
   bool AddUnique(string &items[],const string value){for(int i=0;i<ArraySize(items);i++)if(items[i]==value)return true;int n=ArraySize(items);ArrayResize(items,n+1);items[n]=value;return true;}
public:
   CSF11GroupAccumulator(){Reset("all=all");}
   void Reset(const string group_key){m_group_key=group_key;m_sample_count=0;m_filled=0;m_wins=0;m_losses=0;m_flats=0;ArrayResize(m_events,0);ArrayResize(m_clusters,0);
      m_net.Reset();m_mfe.Reset();m_mae.Reset();m_holding.Reset();m_drawdown.Reset();m_quantiles.Configure(4096);m_positive=0.0;m_negative_abs=0.0;m_total=0.0;m_best=-DBL_MAX;m_worst=DBL_MAX;}
   bool Observe(const SF11_StatisticalSample &s,string &error)
   {
      if(!SF11_ValidateStatisticalSample(s,error))return false;m_sample_count++;AddUnique(m_events,s.event_id);AddUnique(m_clusters,s.cluster_id);
      if(!s.filled){error="";return true;}m_filled++;m_net.Add(s.net_r);m_mfe.Add(s.mfe_r);m_mae.Add(s.mae_r);m_holding.Add(s.holding_seconds);m_drawdown.Add(s.net_r);m_quantiles.Add(s.net_r);m_total+=s.net_r;
      if(s.net_r>m_best)m_best=s.net_r;if(s.net_r<m_worst)m_worst=s.net_r;if(s.net_r>0.0){m_wins++;m_positive+=s.net_r;}else if(s.net_r<0.0){m_losses++;m_negative_abs+=MathAbs(s.net_r);}else m_flats++;error="";return true;
   }
   SF11_StatisticSummary Snapshot(const long minimum_samples=1) const
   {
      SF11_StatisticSummary s;s.schema="alpha_lab.strategy_factory/statistic_summary@1.0.0";s.group_key=m_group_key;s.sample_count=m_sample_count;s.filled_count=m_filled;s.win_count=m_wins;s.loss_count=m_losses;s.flat_count=m_flats;
      s.unique_event_count=ArraySize(m_events);s.unique_cluster_count=ArraySize(m_clusters);s.fill_rate=(m_sample_count>0)?(double)m_filled/(double)m_sample_count:0.0;s.win_rate=(m_filled>0)?(double)m_wins/(double)m_filled:0.0;
      s.mean_net_r=m_net.Mean();s.median_net_r=m_quantiles.Quantile(0.5);s.standard_deviation_r=m_net.StandardDeviation();s.standard_error_r=m_net.StandardError();s.profit_factor=(m_negative_abs>0.0)?m_positive/m_negative_abs:(m_positive>0.0?1.0e9:0.0);s.total_net_r=m_total;s.maximum_drawdown_r=m_drawdown.MaximumDrawdown();
      s.average_mfe_r=m_mfe.Mean();s.average_mae_r=m_mae.Mean();s.average_holding_seconds=m_holding.Mean();s.q05_net_r=m_quantiles.Quantile(0.05);s.q25_net_r=m_quantiles.Quantile(0.25);s.q75_net_r=m_quantiles.Quantile(0.75);s.q95_net_r=m_quantiles.Quantile(0.95);
      s.best_trade_r=(m_filled>0)?m_best:0.0;s.worst_trade_r=(m_filled>0)?m_worst:0.0;s.best_trade_share=(m_total>0.0&&m_best>0.0)?m_best/m_total:0.0;s.status=(m_sample_count>=minimum_samples)?SF11_REPORT_VALID:SF11_REPORT_INSUFFICIENT_SAMPLE;s.summary_hash="";s.summary_hash=SF11_DeriveStatisticSummaryHash(s);return s;
   }
};
#endif
