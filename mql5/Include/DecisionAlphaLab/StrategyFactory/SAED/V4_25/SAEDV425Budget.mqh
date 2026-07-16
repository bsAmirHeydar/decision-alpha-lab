#ifndef __SAED_V4_25_BUDGET_MQH__
#define __SAED_V4_25_BUDGET_MQH__
struct SAEDV425ZeroExposureBudget { int hidden_evaluation_queries; int protected_evidence_exposures; int runtime_compilations; int order_submissions; int online_policy_mutations; };
bool SAEDV425ZeroExposureValid(const SAEDV425ZeroExposureBudget &value){ return value.hidden_evaluation_queries==0 && value.protected_evidence_exposures==0 && value.runtime_compilations==0 && value.order_submissions==0 && value.online_policy_mutations==0; }
#endif
