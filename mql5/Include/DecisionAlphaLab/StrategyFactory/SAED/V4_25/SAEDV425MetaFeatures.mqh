#ifndef __SAED_V4_25_META_FEATURES_MQH__
#define __SAED_V4_25_META_FEATURES_MQH__
struct SAEDV425MetaFeatureReceipt { string task_id; int dimension; bool uses_support_outcomes; bool uses_query_outcomes; bool future_suffix_accessed; bool protected_evidence_accessed; };
bool SAEDV425MetaFeatureSafe(const SAEDV425MetaFeatureReceipt &value){ return value.dimension>0 && value.uses_support_outcomes && !value.uses_query_outcomes && !value.future_suffix_accessed && !value.protected_evidence_accessed; }
#endif
