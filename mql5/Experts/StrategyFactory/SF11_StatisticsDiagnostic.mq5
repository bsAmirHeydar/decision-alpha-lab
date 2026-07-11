#property strict
#include <AlphaLab/StrategyFactory/Statistics/SF11_AllStatistics.mqh>
input int InpMinimumSamples=30;
CSF11StatisticsHarness g_statistics;
int OnInit(){Print("SF11 statistics diagnostic ready; minimum samples=",InpMinimumSamples);return INIT_SUCCEEDED;}
void OnTick(){}
void OnDeinit(const int reason){const SF11_StatisticSummary s=g_statistics.Finalize(InpMinimumSamples);Print("SF11 diagnostic finalized samples=",s.sample_count," mean_r=",DoubleToString(s.mean_net_r,6)," status=",(int)s.status);}
