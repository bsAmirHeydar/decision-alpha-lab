#ifndef __SAED_V4_25_CONTRACTS_MQH__
#define __SAED_V4_25_CONTRACTS_MQH__
#include "SAEDV425Types.mqh"
struct SAEDV425TransferContract { int maximum_sources; double minimum_source_support; double minimum_source_ood_pvalue; double maximum_meta_distance; bool same_cluster_forbidden; bool future_source_forbidden; bool source_query_outcomes_forbidden; bool fail_closed; };
struct SAEDV425AdaptationContract { double prior_strength; double ridge_penalty; double maximum_parameter_delta; int minimum_support_rows; bool query_outcomes_forbidden; bool baseline_preserved; };
struct SAEDV425CalibrationContract { int window_tasks; int minimum_residuals; double alpha; bool past_only; bool runtime_mutation_forbidden; };
#endif
