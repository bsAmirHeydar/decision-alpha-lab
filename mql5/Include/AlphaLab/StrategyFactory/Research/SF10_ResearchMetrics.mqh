#ifndef __SF10_RESEARCH_METRICS_MQH__
#define __SF10_RESEARCH_METRICS_MQH__
#include "SF10_FidelityPreset.mqh"

struct SF10_ResearchMetrics
{
   string schema;
   long outcome_count;
   long filled_count;
   long win_count;
   long loss_count;
   long flat_count;
   long ambiguous_count;
   long no_fill_count;
   long unique_event_count;
   long unique_cluster_count;
   double fill_rate;
   double win_rate;
   double average_win_r;
   double average_loss_r;
   double expectancy_r;
   double median_proxy_r;
   double standard_deviation_r;
   double profit_factor;
   double total_net_r;
   double maximum_drawdown_r;
   double maximum_runup_r;
   double average_mfe_r;
   double average_mae_r;
   double average_holding_seconds;
   double best_trade_r;
   double worst_trade_r;
   double best_trade_share;
   long maximum_consecutive_losses;
   double fold_survival_score;
   double cost_survival_score;
   double stability_score;
   string metrics_hash;
};

class CSF10ResearchAccumulator
{
private:
   long m_count,m_filled,m_wins,m_losses,m_flats,m_ambiguous,m_no_fill;
   double m_sum,m_sum_sq,m_sum_wins,m_sum_losses_abs,m_sum_mfe,m_sum_mae,m_sum_holding;
   double m_equity,m_peak,m_trough,m_max_dd,m_max_runup,m_best,m_worst;
   long m_consecutive_losses,m_max_consecutive_losses;
   string m_events[];
   string m_clusters[];
   int m_max_unique;

   bool AddUnique(string &items[],const string value)
   {
      if(value=="")return true;
      const int n=ArraySize(items);
      for(int i=0;i<n;i++)if(items[i]==value)return true;
      if(n>=m_max_unique)return false;
      ArrayResize(items,n+1);items[n]=value;return true;
   }
public:
   CSF10ResearchAccumulator(void){Reset(4096);}
   void Reset(const int max_unique)
   {
      m_count=0;m_filled=0;m_wins=0;m_losses=0;m_flats=0;m_ambiguous=0;m_no_fill=0;
      m_sum=0.0;m_sum_sq=0.0;m_sum_wins=0.0;m_sum_losses_abs=0.0;m_sum_mfe=0.0;m_sum_mae=0.0;m_sum_holding=0.0;
      m_equity=0.0;m_peak=0.0;m_trough=0.0;m_max_dd=0.0;m_max_runup=0.0;m_best=-1.0e100;m_worst=1.0e100;
      m_consecutive_losses=0;m_max_consecutive_losses=0;m_max_unique=MathMax(1,max_unique);
      ArrayResize(m_events,0);ArrayResize(m_clusters,0);
   }
   bool Observe(const SF09_OutcomeRecord &o,const string cluster_id,string &error)
   {
      if(!SF09_ValidateOutcomeRecord(o,error))return false;
      if(!AddUnique(m_events,o.event_id)||!AddUnique(m_clusters,cluster_id))
      {error="research unique-key capacity exceeded";return false;}
      m_count++;if(o.ambiguous)m_ambiguous++;
      if(!o.filled){m_no_fill++;error="";return true;}
      m_filled++;const double r=o.net_r;m_sum+=r;m_sum_sq+=r*r;m_sum_mfe+=o.mfe_r;m_sum_mae+=o.mae_r;
      m_sum_holding+=(double)o.holding_milliseconds/1000.0;m_equity+=r;
      if(m_equity>m_peak)m_peak=m_equity;const double dd=m_peak-m_equity;if(dd>m_max_dd)m_max_dd=dd;
      if(m_equity<m_trough)m_trough=m_equity;const double ru=m_equity-m_trough;if(ru>m_max_runup)m_max_runup=ru;
      if(r>m_best)m_best=r;if(r<m_worst)m_worst=r;
      if(r>0.0){m_wins++;m_sum_wins+=r;m_consecutive_losses=0;}
      else if(r<0.0){m_losses++;m_sum_losses_abs+=MathAbs(r);m_consecutive_losses++;if(m_consecutive_losses>m_max_consecutive_losses)m_max_consecutive_losses=m_consecutive_losses;}
      else {m_flats++;m_consecutive_losses=0;}
      error="";return true;
   }
   SF10_ResearchMetrics Snapshot(const double fold_survival=1.0,const double cost_survival=1.0,const double stability=1.0) const
   {
      SF10_ResearchMetrics m;m.schema="alpha_lab.strategy_factory/research_metrics@1.0.0";
      m.outcome_count=m_count;m.filled_count=m_filled;m.win_count=m_wins;m.loss_count=m_losses;m.flat_count=m_flats;
      m.ambiguous_count=m_ambiguous;m.no_fill_count=m_no_fill;m.unique_event_count=ArraySize(m_events);m.unique_cluster_count=ArraySize(m_clusters);
      m.fill_rate=(m_count>0)?(double)m_filled/(double)m_count:0.0;m.win_rate=(m_filled>0)?(double)m_wins/(double)m_filled:0.0;
      m.average_win_r=(m_wins>0)?m_sum_wins/(double)m_wins:0.0;m.average_loss_r=(m_losses>0)?-m_sum_losses_abs/(double)m_losses:0.0;
      m.expectancy_r=(m_filled>0)?m_sum/(double)m_filled:0.0;m.median_proxy_r=m.expectancy_r;
      double variance=(m_filled>1)?(m_sum_sq-(m_sum*m_sum/(double)m_filled))/(double)(m_filled-1):0.0;
      m.standard_deviation_r=MathSqrt(MathMax(0.0,variance));m.profit_factor=(m_sum_losses_abs>0.0)?m_sum_wins/m_sum_losses_abs:(m_sum_wins>0.0?1.0e9:0.0);
      m.total_net_r=m_sum;m.maximum_drawdown_r=m_max_dd;m.maximum_runup_r=m_max_runup;
      m.average_mfe_r=(m_filled>0)?m_sum_mfe/(double)m_filled:0.0;m.average_mae_r=(m_filled>0)?m_sum_mae/(double)m_filled:0.0;
      m.average_holding_seconds=(m_filled>0)?m_sum_holding/(double)m_filled:0.0;m.best_trade_r=(m_filled>0)?m_best:0.0;m.worst_trade_r=(m_filled>0)?m_worst:0.0;
      m.best_trade_share=(m_sum>0.0&&m_best>0.0)?m_best/m_sum:0.0;m.maximum_consecutive_losses=m_max_consecutive_losses;
      m.fold_survival_score=fold_survival;m.cost_survival_score=cost_survival;m.stability_score=stability;m.metrics_hash="";
      m.metrics_hash=SF10_DeriveMetricsHash(m);return m;
   }
};

string SF10_ResearchMetricsCanonical(const SF10_ResearchMetrics &m)
{
   return m.schema+"|"+IntegerToString(m.outcome_count)+"|"+IntegerToString(m.filled_count)+"|"+
          IntegerToString(m.unique_event_count)+"|"+IntegerToString(m.unique_cluster_count)+"|"+
          SF01_CanonicalDouble(m.fill_rate)+"|"+SF01_CanonicalDouble(m.win_rate)+"|"+
          SF01_CanonicalDouble(m.expectancy_r)+"|"+SF01_CanonicalDouble(m.standard_deviation_r)+"|"+
          SF01_CanonicalDouble(m.profit_factor)+"|"+SF01_CanonicalDouble(m.total_net_r)+"|"+
          SF01_CanonicalDouble(m.maximum_drawdown_r)+"|"+SF01_CanonicalDouble(m.best_trade_share)+"|"+
          SF01_CanonicalDouble(m.fold_survival_score)+"|"+SF01_CanonicalDouble(m.cost_survival_score)+"|"+
          SF01_CanonicalDouble(m.stability_score);
}
string SF10_DeriveMetricsHash(const SF10_ResearchMetrics &m)
{return SF01_StableId("rmet",SF10_ResearchMetricsCanonical(m));}
#endif
