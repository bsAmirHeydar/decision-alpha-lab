#ifndef __SF11_CONFIDENCE_INTERVAL_MQH__
#define __SF11_CONFIDENCE_INTERVAL_MQH__
#include "SF11_GroupAccumulator.mqh"
struct SF11_ConfidenceInterval
{
   string schema;string metric_id;string group_key;ENUM_SF11_INTERVAL_KIND kind;double confidence_level;double estimate;double lower;double upper;double standard_error;long effective_sample_count;int seed;string interval_hash;
};
SF11_ConfidenceInterval SF11_NormalMeanInterval(const string metric_id,const string group_key,const double estimate,const double standard_deviation,const long sample_count)
{
   SF11_ConfidenceInterval r;r.schema="alpha_lab.strategy_factory/confidence_interval@1.0.0";r.metric_id=metric_id;r.group_key=group_key;r.kind=SF11_INTERVAL_NORMAL_MEAN;r.confidence_level=0.95;r.estimate=estimate;
   r.standard_error=(sample_count>1)?standard_deviation/MathSqrt((double)sample_count):0.0;const double z=1.959963984540054;r.lower=estimate-z*r.standard_error;r.upper=estimate+z*r.standard_error;r.effective_sample_count=sample_count;r.seed=0;
   r.interval_hash=SF01_StableId("cint",r.schema+"|"+r.metric_id+"|"+r.group_key+"|"+SF01_CanonicalDouble(r.estimate)+"|"+SF01_CanonicalDouble(r.lower)+"|"+SF01_CanonicalDouble(r.upper)+"|"+IntegerToString(sample_count));return r;
}
SF11_ConfidenceInterval SF11_WilsonInterval(const string metric_id,const string group_key,const long successes,const long trials)
{
   SF11_ConfidenceInterval r;r.schema="alpha_lab.strategy_factory/confidence_interval@1.0.0";r.metric_id=metric_id;r.group_key=group_key;r.kind=SF11_INTERVAL_WILSON_PROPORTION;r.confidence_level=0.95;const double z=1.959963984540054;const double z2=z*z;const double p=(trials>0)?(double)successes/(double)trials:0.0;
   const double den=1.0+z2/(double)MathMax(1,trials);const double center=(p+z2/(2.0*(double)MathMax(1,trials)))/den;const double half=z*MathSqrt((p*(1.0-p)+z2/(4.0*(double)MathMax(1,trials)))/(double)MathMax(1,trials))/den;
   r.estimate=p;r.lower=MathMax(0.0,center-half);r.upper=MathMin(1.0,center+half);r.standard_error=MathSqrt(p*(1.0-p)/(double)MathMax(1,trials));r.effective_sample_count=trials;r.seed=0;r.interval_hash=SF01_StableId("cint",r.schema+"|"+r.metric_id+"|"+r.group_key+"|"+IntegerToString(successes)+"|"+IntegerToString(trials));return r;
}
#endif
