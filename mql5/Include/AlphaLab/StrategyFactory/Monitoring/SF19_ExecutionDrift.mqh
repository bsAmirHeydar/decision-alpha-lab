#ifndef __SF19_EXECUTION_DRIFT_MQH__
#define __SF19_EXECUTION_DRIFT_MQH__
#include "SF19_TelemetryContracts.mqh"
struct SF19_ExecutionDriftObservation
{string observation_id;long window_start_utc_msc,window_end_utc_msc;int order_count,fill_count,reject_count,mismatch_count,missing_transaction_count;double mean_slippage_points,p95_slippage_points,mean_fill_latency_us,p95_fill_latency_us;};
struct SF19_ExecutionDriftPolicy
{string policy_id;int minimum_orders;double reject_rate_warning,reject_rate_critical,mismatch_rate_critical,p95_slippage_warning,p95_slippage_critical,p95_fill_latency_warning_us,p95_fill_latency_critical_us;};
struct SF19_ExecutionDriftResult
{string result_id,observation_id,policy_id,reasons;double reject_rate,mismatch_rate;ENUM_SF19_SEVERITY severity;bool sufficient_samples;};
bool SF19_EvaluateExecutionDrift(const SF19_ExecutionDriftObservation &o,const SF19_ExecutionDriftPolicy &p,SF19_ExecutionDriftResult &r,string &error)
{
 if(o.observation_id==""||p.policy_id==""||o.order_count<0||p.minimum_orders<1){error="invalid execution drift input";return false;}double reject=(double)o.reject_count/(double)MathMax(1,o.order_count);double mismatch=(double)o.mismatch_count/(double)MathMax(1,o.order_count);bool enough=o.order_count>=p.minimum_orders;ENUM_SF19_SEVERITY sev=SF19_SEVERITY_INFO;string reasons=(enough?"":"INSUFFICIENT_ORDERS");
 if(enough&&(reject>=p.reject_rate_warning||o.p95_slippage_points>=p.p95_slippage_warning||o.p95_fill_latency_us>=p.p95_fill_latency_warning_us)){sev=SF19_SEVERITY_WARNING;reasons+=(reasons==""?"":"|")+"EXECUTION_WARNING";}
 if((enough&&(reject>=p.reject_rate_critical||mismatch>=p.mismatch_rate_critical||o.p95_slippage_points>=p.p95_slippage_critical||o.p95_fill_latency_us>=p.p95_fill_latency_critical_us))||o.missing_transaction_count>0){sev=SF19_SEVERITY_CRITICAL;reasons+=(reasons==""?"":"|")+"EXECUTION_CRITICAL";}
 r.observation_id=o.observation_id;r.policy_id=p.policy_id;r.reject_rate=reject;r.mismatch_rate=mismatch;r.severity=sev;r.sufficient_samples=enough;r.reasons=reasons;r.result_id=SF01_StableId("sf19-exec-drift",o.observation_id+"|"+p.policy_id+"|"+SF01_CanonicalDouble(reject)+"|"+SF01_CanonicalDouble(mismatch)+"|"+IntegerToString((int)sev));error="";return true;
}
#endif
