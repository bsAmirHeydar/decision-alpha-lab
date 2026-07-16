#ifndef __DECISION_ALPHA_LAB_SAEDV421OPTIMIZER_MQH__
#define __DECISION_ALPHA_LAB_SAEDV421OPTIMIZER_MQH__
bool SAEDV421Prefer(const SAEDV421Allocation &a,const SAEDV421Allocation &b){if(a.feasible!=b.feasible)return a.feasible;if(a.maximum_regret!=b.maximum_regret)return a.maximum_regret<b.maximum_regret;if(a.worst_case_utility!=b.worst_case_utility)return a.worst_case_utility>b.worst_case_utility;return a.allocation_id<b.allocation_id;}
#endif
