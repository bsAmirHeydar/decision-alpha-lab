#ifndef __SF19_LATENCY_HISTOGRAM_MQH__
#define __SF19_LATENCY_HISTOGRAM_MQH__
#include "SF19_TelemetryContracts.mqh"
struct SF19_LatencySloPolicy
{string policy_id,stage;int bucket_count;long bucket_edges_us[SF19_MAX_LATENCY_BUCKETS];long p50_limit_us,p95_limit_us,p99_limit_us;int minimum_samples;};
struct SF19_LatencySnapshot
{string snapshot_id,policy_id,stage;long sample_count,bucket_counts[SF19_MAX_LATENCY_BUCKETS],overflow_count,minimum_us,maximum_us,p50_us,p95_us,p99_us,snapshot_time_utc_msc;double mean_us;bool slo_breached;};
class CSF19LatencyHistogram
{
 private: SF19_LatencySloPolicy m_policy;long m_counts[SF19_MAX_LATENCY_BUCKETS],m_overflow,m_total,m_sum,m_minimum,m_maximum;
 long Percentile(const double q)const{if(m_total<=0)return 0;long target=(long)MathCeil((double)m_total*q);long c=0;for(int i=0;i<m_policy.bucket_count;i++){c+=m_counts[i];if(c>=target)return m_policy.bucket_edges_us[i];}return m_maximum;}
 public:
 CSF19LatencyHistogram(){Reset();}
 void Reset(){m_overflow=0;m_total=0;m_sum=0;m_minimum=0;m_maximum=0;for(int i=0;i<SF19_MAX_LATENCY_BUCKETS;i++)m_counts[i]=0;}
 bool Configure(const SF19_LatencySloPolicy &policy,string &error){if(policy.policy_id==""||policy.stage==""||policy.bucket_count<1||policy.bucket_count>SF19_MAX_LATENCY_BUCKETS||policy.minimum_samples<1){error="invalid latency policy";return false;}for(int i=0;i<policy.bucket_count;i++){if(policy.bucket_edges_us[i]<=0||(i>0&&policy.bucket_edges_us[i]<=policy.bucket_edges_us[i-1])){error="latency buckets must ascend";return false;}}m_policy=policy;Reset();error="";return true;}
 bool Observe(const long value_us,string &error){if(value_us<0){error="negative latency";return false;}m_total++;m_sum+=value_us;if(m_total==1)m_minimum=value_us;else m_minimum=MathMin(m_minimum,value_us);m_maximum=MathMax(m_maximum,value_us);for(int i=0;i<m_policy.bucket_count;i++){if(value_us<=m_policy.bucket_edges_us[i]){m_counts[i]++;error="";return true;}}m_overflow++;error="";return true;}
 void Snapshot(const long now,SF19_LatencySnapshot &s)const{s.policy_id=m_policy.policy_id;s.stage=m_policy.stage;s.sample_count=m_total;s.overflow_count=m_overflow;s.minimum_us=m_minimum;s.maximum_us=m_maximum;s.mean_us=(m_total>0?(double)m_sum/(double)m_total:0.0);s.p50_us=Percentile(0.50);s.p95_us=Percentile(0.95);s.p99_us=Percentile(0.99);s.snapshot_time_utc_msc=now;s.slo_breached=(m_total>=m_policy.minimum_samples&&(s.p50_us>m_policy.p50_limit_us||s.p95_us>m_policy.p95_limit_us||s.p99_us>m_policy.p99_limit_us));for(int i=0;i<SF19_MAX_LATENCY_BUCKETS;i++)s.bucket_counts[i]=m_counts[i];s.snapshot_id=SF01_StableId("sf19-latency",s.policy_id+"|"+IntegerToString(s.sample_count)+"|"+IntegerToString(s.p50_us)+"|"+IntegerToString(s.p95_us)+"|"+IntegerToString(s.p99_us)+"|"+IntegerToString(now));}
};
#endif
