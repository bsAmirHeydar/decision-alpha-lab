#ifndef __SF19_DRIFT_MONITOR_MQH__
#define __SF19_DRIFT_MONITOR_MQH__
#include "SF19_TelemetryContracts.mqh"
struct SF19_DriftBaseline
{string baseline_id,feature_name,model_id;ENUM_SF19_DRIFT_KIND kind;int bin_count;double probabilities[SF19_MAX_DRIFT_BINS],mean,standard_deviation;long sample_count,window_start_utc_msc,window_end_utc_msc;};
struct SF19_DriftObservation
{string observation_id,baseline_id,feature_name,model_id;ENUM_SF19_DRIFT_KIND kind;int bin_count;long bin_counts[SF19_MAX_DRIFT_BINS],sample_count,missing_count,invalid_count,window_start_utc_msc,window_end_utc_msc;double mean,standard_deviation;};
struct SF19_DriftThresholdPolicy
{string policy_id;ENUM_SF19_DRIFT_KIND kind;double psi_warning,psi_critical,js_warning,js_critical,mean_z_warning,mean_z_critical,missing_rate_critical,invalid_rate_critical;long minimum_samples;};
struct SF19_DriftResult
{string result_id,baseline_id,observation_id,policy_id,reasons;ENUM_SF19_DRIFT_KIND kind;double psi,jensen_shannon,mean_z_shift,missing_rate,invalid_rate;ENUM_SF19_SEVERITY severity;bool sufficient_samples;};
class CSF19DriftMonitor
{
 private:
 double Safe(const double v)const{return MathMax(v,1.0e-12);}
 public:
 bool Evaluate(const SF19_DriftBaseline &b,const SF19_DriftObservation &o,const SF19_DriftThresholdPolicy &p,SF19_DriftResult &r,string &error)const
 {
  if(b.baseline_id==""||o.baseline_id!=b.baseline_id||b.kind!=o.kind||p.kind!=b.kind||b.bin_count<1||b.bin_count!=o.bin_count||b.bin_count>SF19_MAX_DRIFT_BINS){error="drift lineage or bins mismatch";return false;}
  long total=0;for(int i=0;i<o.bin_count;i++)total+=o.bin_counts[i];if(total!=o.sample_count||total<1){error="drift counts inconsistent";return false;}
  double psi=0.0,js=0.0;for(int i=0;i<b.bin_count;i++){double e=Safe(b.probabilities[i]);double a=Safe((double)o.bin_counts[i]/(double)total);double m=0.5*(e+a);psi+=(a-e)*MathLog(a/e);js+=0.5*(e*MathLog(e/m)+a*MathLog(a/m));}
  double z=MathAbs(o.mean-b.mean)/Safe(b.standard_deviation);double missing=(double)o.missing_count/(double)MathMax(1,o.sample_count+o.missing_count);double invalid=(double)o.invalid_count/(double)MathMax(1,o.sample_count+o.invalid_count);
  ENUM_SF19_SEVERITY sev=SF19_SEVERITY_INFO;string reasons="";bool enough=(o.sample_count>=p.minimum_samples);
  if(!enough)reasons="INSUFFICIENT_SAMPLES";
  if(enough&&(psi>=p.psi_warning||js>=p.js_warning||z>=p.mean_z_warning)){sev=SF19_SEVERITY_WARNING;reasons+=(reasons==""?"":"|")+"DRIFT_WARNING";}
  if(enough&&(psi>=p.psi_critical||js>=p.js_critical||z>=p.mean_z_critical||missing>=p.missing_rate_critical||invalid>=p.invalid_rate_critical)){sev=SF19_SEVERITY_CRITICAL;reasons+=(reasons==""?"":"|")+"DRIFT_CRITICAL";}
  r.baseline_id=b.baseline_id;r.observation_id=o.observation_id;r.policy_id=p.policy_id;r.kind=b.kind;r.psi=psi;r.jensen_shannon=js;r.mean_z_shift=z;r.missing_rate=missing;r.invalid_rate=invalid;r.severity=sev;r.sufficient_samples=enough;r.reasons=reasons;r.result_id=SF01_StableId("sf19-drift",b.baseline_id+"|"+o.observation_id+"|"+p.policy_id+"|"+SF01_CanonicalDouble(psi)+"|"+SF01_CanonicalDouble(js)+"|"+SF01_CanonicalDouble(z)+"|"+IntegerToString((int)sev));error="";return true;
 }
};
#endif
