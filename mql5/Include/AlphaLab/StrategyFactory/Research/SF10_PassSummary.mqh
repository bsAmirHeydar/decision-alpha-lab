#ifndef __SF10_PASS_SUMMARY_MQH__
#define __SF10_PASS_SUMMARY_MQH__
#include "SF10_CustomObjective.mqh"
#define SF10_FRAME_DATA_SIZE 24

struct SF10_PassSummary
{
   string schema;
   long public_id;
   string run_id;
   string manifest_hash;
   string parameter_hash;
   double objective_score;
   ENUM_SF10_PASS_STATUS status;
   SF10_ResearchMetrics metrics;
   string summary_hash;
};

string SF10_PassSummaryCanonical(const SF10_PassSummary &s)
{
   return s.schema+"|"+IntegerToString(s.public_id)+"|"+s.run_id+"|"+s.manifest_hash+"|"+
          s.parameter_hash+"|"+SF01_CanonicalDouble(s.objective_score)+"|"+
          IntegerToString((int)s.status)+"|"+s.metrics.metrics_hash;
}
string SF10_DerivePassSummaryHash(const SF10_PassSummary &s)
{return SF01_StableId("psum",SF10_PassSummaryCanonical(s));}

void SF10_PassSummaryToFrame(const SF10_PassSummary &s,double &data[])
{
   ArrayResize(data,SF10_FRAME_DATA_SIZE);ArrayInitialize(data,0.0);
   data[0]=(double)s.status;data[1]=(double)s.metrics.outcome_count;data[2]=(double)s.metrics.filled_count;
   data[3]=(double)s.metrics.unique_event_count;data[4]=(double)s.metrics.unique_cluster_count;
   data[5]=s.metrics.fill_rate;data[6]=s.metrics.win_rate;data[7]=s.metrics.expectancy_r;
   data[8]=s.metrics.standard_deviation_r;data[9]=s.metrics.profit_factor;data[10]=s.metrics.total_net_r;
   data[11]=s.metrics.maximum_drawdown_r;data[12]=s.metrics.average_mfe_r;data[13]=s.metrics.average_mae_r;
   data[14]=s.metrics.average_holding_seconds;data[15]=s.metrics.best_trade_r;data[16]=s.metrics.worst_trade_r;
   data[17]=s.metrics.best_trade_share;data[18]=(double)s.metrics.maximum_consecutive_losses;
   data[19]=s.metrics.fold_survival_score;data[20]=s.metrics.cost_survival_score;data[21]=s.metrics.stability_score;
   data[22]=s.objective_score;data[23]=(double)s.public_id;
}

bool SF10_PassSummaryFromFrame(const string run_id,const string manifest_hash,const string parameter_hash,
                               const long public_id,const double objective_score,const double &data[],SF10_PassSummary &s,string &error)
{
   if(ArraySize(data)<SF10_FRAME_DATA_SIZE){error="research frame too short";return false;}
   s.schema="alpha_lab.strategy_factory/optimization_pass_summary@1.0.0";s.public_id=public_id;s.run_id=run_id;
   s.manifest_hash=manifest_hash;s.parameter_hash=parameter_hash;s.objective_score=objective_score;s.status=(ENUM_SF10_PASS_STATUS)(int)data[0];
   s.metrics.schema="alpha_lab.strategy_factory/research_metrics@1.0.0";s.metrics.outcome_count=(long)data[1];s.metrics.filled_count=(long)data[2];
   s.metrics.unique_event_count=(long)data[3];s.metrics.unique_cluster_count=(long)data[4];s.metrics.fill_rate=data[5];s.metrics.win_rate=data[6];
   s.metrics.expectancy_r=data[7];s.metrics.standard_deviation_r=data[8];s.metrics.profit_factor=data[9];s.metrics.total_net_r=data[10];
   s.metrics.maximum_drawdown_r=data[11];s.metrics.average_mfe_r=data[12];s.metrics.average_mae_r=data[13];s.metrics.average_holding_seconds=data[14];
   s.metrics.best_trade_r=data[15];s.metrics.worst_trade_r=data[16];s.metrics.best_trade_share=data[17];s.metrics.maximum_consecutive_losses=(long)data[18];
   s.metrics.fold_survival_score=data[19];s.metrics.cost_survival_score=data[20];s.metrics.stability_score=data[21];s.metrics.metrics_hash=SF10_DeriveMetricsHash(s.metrics);
   s.summary_hash="";s.summary_hash=SF10_DerivePassSummaryHash(s);error="";return true;
}
#endif
