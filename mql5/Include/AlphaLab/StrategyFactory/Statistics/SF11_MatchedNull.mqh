#ifndef __SF11_MATCHED_NULL_MQH__
#define __SF11_MATCHED_NULL_MQH__
#include "SF11_ConfidenceInterval.mqh"
struct SF11_MatchedNullSpec
{
   string schema;string null_id;string null_version;ENUM_SF11_NULL_METHOD method;int seed;int minimum_pool_size;int maximum_reuse;bool require_different_cluster;string required_stratum_fields;string null_hash;
};
string SF11_MatchedNullSpecCanonical(const SF11_MatchedNullSpec &s)
{
   return s.schema+"|"+s.null_id+"|"+s.null_version+"|"+IntegerToString((int)s.method)+"|"+IntegerToString(s.seed)+"|"+IntegerToString(s.minimum_pool_size)+"|"+IntegerToString(s.maximum_reuse)+"|"+SF01_CanonicalBool(s.require_different_cluster)+"|"+s.required_stratum_fields;
}
string SF11_DeriveMatchedNullHash(const SF11_MatchedNullSpec &s){return SF01_StableId("null",SF11_MatchedNullSpecCanonical(s));}
struct SF11_NullAssignment
{
   string assignment_id;string null_hash;string observed_sample_id;string control_sample_id;string stratum_key;string observed_cluster_id;string control_cluster_id;int reuse_ordinal;
};
struct SF11_NullComparison
{
   string schema;string null_hash;string group_key;long matched_count;double observed_mean_r;double control_mean_r;double uplift_r;double paired_standard_error;double z_score;double match_rate;ENUM_SF11_REPORT_STATUS status;string comparison_hash;
};
#endif
