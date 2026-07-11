#ifndef __SF11_STATISTIC_SUMMARY_MQH__
#define __SF11_STATISTIC_SUMMARY_MQH__
#include "SF11_BoundedQuantiles.mqh"
struct SF11_StatisticSummary
{
   string schema;string group_key;long sample_count;long filled_count;long win_count;long loss_count;long flat_count;
   long unique_event_count;long unique_cluster_count;double fill_rate;double win_rate;double mean_net_r;double median_net_r;
   double standard_deviation_r;double standard_error_r;double profit_factor;double total_net_r;double maximum_drawdown_r;
   double average_mfe_r;double average_mae_r;double average_holding_seconds;double q05_net_r;double q25_net_r;double q75_net_r;
   double q95_net_r;double best_trade_r;double worst_trade_r;double best_trade_share;ENUM_SF11_REPORT_STATUS status;string summary_hash;
};
string SF11_StatisticSummaryCanonical(const SF11_StatisticSummary &s)
{
   return s.schema+"|"+s.group_key+"|"+IntegerToString(s.sample_count)+"|"+IntegerToString(s.filled_count)+"|"+
      IntegerToString(s.unique_event_count)+"|"+IntegerToString(s.unique_cluster_count)+"|"+SF01_CanonicalDouble(s.fill_rate)+"|"+
      SF01_CanonicalDouble(s.win_rate)+"|"+SF01_CanonicalDouble(s.mean_net_r)+"|"+SF01_CanonicalDouble(s.standard_deviation_r)+"|"+
      SF01_CanonicalDouble(s.profit_factor)+"|"+SF01_CanonicalDouble(s.total_net_r)+"|"+SF01_CanonicalDouble(s.maximum_drawdown_r)+"|"+
      SF01_CanonicalDouble(s.best_trade_share)+"|"+IntegerToString((int)s.status);
}
string SF11_DeriveStatisticSummaryHash(const SF11_StatisticSummary &s){return SF01_StableId("stat",SF11_StatisticSummaryCanonical(s));}
#endif
