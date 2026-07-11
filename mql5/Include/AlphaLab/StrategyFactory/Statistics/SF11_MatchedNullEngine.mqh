#ifndef __SF11_MATCHED_NULL_ENGINE_MQH__
#define __SF11_MATCHED_NULL_ENGINE_MQH__
#include "SF11_MatchedNull.mqh"
class CSF11MatchedNullEngine
{
private:
   SF11_MatchedNullSpec m_spec;
public:
   void Configure(const SF11_MatchedNullSpec &spec){m_spec=spec;if(m_spec.null_hash=="")m_spec.null_hash=SF11_DeriveMatchedNullHash(m_spec);}
   bool SelectControl(const SF11_StatisticalSample &observed,const SF11_StatisticalSample &controls[],const int reuse_counts[],int &selected_index) const
   {
      selected_index=-1;const int n=ArraySize(controls);if(n<m_spec.minimum_pool_size)return false;
      const ulong h=SF01_Fnv1a64Utf16LE(observed.sample_id+"|"+IntegerToString(m_spec.seed));const int start=(int)(h%(ulong)n);
      for(int offset=0;offset<n;offset++)
      {
         const int i=(start+offset)%n;if(controls[i].stratum_key!=observed.stratum_key)continue;
         if(m_spec.require_different_cluster&&controls[i].cluster_id==observed.cluster_id)continue;
         if(reuse_counts[i]>=m_spec.maximum_reuse)continue;selected_index=i;return true;
      }
      return false;
   }
};
SF11_NullComparison SF11_CompareMatchedDifferences(const string null_hash,const string group_key,const double observed[],const double controls[],const long total_observed)
{
   SF11_NullComparison r;r.schema="alpha_lab.strategy_factory/null_comparison@1.0.0";r.null_hash=null_hash;r.group_key=group_key;r.matched_count=MathMin(ArraySize(observed),ArraySize(controls));double so=0.0,sc=0.0,sd=0.0,sd2=0.0;
   for(int i=0;i<r.matched_count;i++){const double d=observed[i]-controls[i];so+=observed[i];sc+=controls[i];sd+=d;sd2+=d*d;}
   r.observed_mean_r=(r.matched_count>0)?so/(double)r.matched_count:0.0;r.control_mean_r=(r.matched_count>0)?sc/(double)r.matched_count:0.0;r.uplift_r=r.observed_mean_r-r.control_mean_r;
   const double variance=(r.matched_count>1)?(sd2-(sd*sd/(double)r.matched_count))/(double)(r.matched_count-1):0.0;r.paired_standard_error=(r.matched_count>1)?MathSqrt(MathMax(0.0,variance))/MathSqrt((double)r.matched_count):0.0;
   r.z_score=(r.paired_standard_error>0.0)?r.uplift_r/r.paired_standard_error:(r.uplift_r>0.0?1.0e9:(r.uplift_r<0.0?-1.0e9:0.0));r.match_rate=(total_observed>0)?(double)r.matched_count/(double)total_observed:0.0;r.status=(r.matched_count==0)?SF11_REPORT_UNMATCHED:(r.match_rate>=0.8?SF11_REPORT_VALID:SF11_REPORT_PARTIAL_MATCH);
   r.comparison_hash=SF01_StableId("ncmp",r.schema+"|"+r.null_hash+"|"+r.group_key+"|"+IntegerToString(r.matched_count)+"|"+SF01_CanonicalDouble(r.uplift_r)+"|"+SF01_CanonicalDouble(r.match_rate));return r;
}
#endif
