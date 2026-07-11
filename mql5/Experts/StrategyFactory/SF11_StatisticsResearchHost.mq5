#property strict
#include <AlphaLab/StrategyFactory/Statistics/SF11_AllStatistics.mqh>
input string InpReportId="sf11_reference_report";
input int InpMinimumSamples=30;
CSF11StatisticsHarness g_statistics;
int OnInit(){Print("SF11 statistics research host initialized: ",InpReportId);return INIT_SUCCEEDED;}
void OnTick(){}
double OnTester(){const SF11_StatisticSummary s=g_statistics.Finalize(InpMinimumSamples);if(s.status!=SF11_REPORT_VALID)return -1.0e100;return s.mean_net_r*MathSqrt((double)MathMax(1,s.unique_cluster_count))/(1.0+s.maximum_drawdown_r+s.standard_deviation_r);}
