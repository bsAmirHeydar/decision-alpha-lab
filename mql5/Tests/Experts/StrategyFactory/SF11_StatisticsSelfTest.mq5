#property strict
#include <AlphaLab/StrategyFactory/Statistics/SF11_AllStatistics.mqh>
int OnInit()
{
   CSF11StatisticsHarness h;string error="";
   for(int i=0;i<6;i++)
   {
      SF11_StatisticalSample s;s.schema="alpha_lab.strategy_factory/statistical_sample@1.0.0";s.sample_id="sample_"+IntegerToString(i);s.outcome_id="outcome_"+IntegerToString(i);s.candidate_id="candidate_"+IntegerToString(i);s.event_id="event_"+IntegerToString(i);s.cluster_id="cluster_"+IntegerToString(i/2);s.strategy_id="fixture_strategy";s.symbol="EURUSD";s.direction=(i%2==0)?"long":"short";s.session_id="fixture";s.year=2026;s.month=7;s.weekday=4;s.stratum_key="session_fixture";s.filled=true;s.ambiguous=false;s.net_r=(i<4)?1.0:-1.0;s.mfe_r=1.5;s.mae_r=0.5;s.holding_seconds=60.0;s.weight=1.0;s.known_time_utc_msc=1000+i;
      if(!h.Observe(s,error)){Print("SF11 observe failed: ",error);return INIT_FAILED;}
   }
   const SF11_StatisticSummary summary=h.Finalize(1);if(summary.sample_count!=6||summary.filled_count!=6||summary.unique_cluster_count!=3||summary.mean_net_r<=0.0||summary.summary_hash==""){Print("SF11 summary assertion failed");return INIT_FAILED;}
   const SF11_ConfidenceInterval ci=SF11_WilsonInterval("win_rate","all=all",4,6);if(ci.lower<0.0||ci.upper>1.0||ci.interval_hash==""){Print("SF11 Wilson interval failed");return INIT_FAILED;}
   double observed[]={1.0,0.5,-0.5};double controls[]={0.0,0.0,0.0};const SF11_NullComparison cmp=SF11_CompareMatchedDifferences("null_fixture","all=all",observed,controls,3);if(cmp.matched_count!=3||cmp.uplift_r<=0.0||cmp.comparison_hash==""){Print("SF11 null comparison failed");return INIT_FAILED;}
   Print("SF11 Statistics Self-Test PASS");return INIT_SUCCEEDED;
}
void OnTick(){}
