#ifndef __SAED_V4_25_SOURCE_ELIGIBILITY_MQH__
#define __SAED_V4_25_SOURCE_ELIGIBILITY_MQH__
bool SAEDV425SourceEligible(const string source_cluster,const string target_cluster,const datetime source_time,const datetime target_time,const double support,const double ood_pvalue,const double distance,const double minimum_support,const double minimum_ood,const double maximum_distance){ if(source_cluster==target_cluster) return false; if(source_time>=target_time) return false; if(support<minimum_support) return false; if(ood_pvalue<minimum_ood) return false; if(distance>maximum_distance) return false; return true; }
#endif
