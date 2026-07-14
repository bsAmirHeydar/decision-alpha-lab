#ifndef __FP_I13_PERFORMANCE_BUDGET_MQH__
#define __FP_I13_PERFORMANCE_BUDGET_MQH__
#include "FP_I13_Contracts.mqh"
class FP_I13_PerformanceBudget { public: static ENUM_FP_I13_BUDGET_STATUS Evaluate(const SFP_I13_Config &c,const ulong elapsed_us,const int object_count,const int object_ops,string &reason){if(object_count>c.max_objects*2||object_ops>c.max_object_ops_per_frame*5||elapsed_us>5000000){reason="FP_REL_BUDGET_BLOCKED";return FP_I13_BUDGET_BLOCKED;}if(object_count>c.max_objects||object_ops>c.max_object_ops_per_frame||elapsed_us>100000){reason="FP_REL_BUDGET_DEGRADED";return FP_I13_BUDGET_DEGRADED;}reason="FP_REL_BUDGET_PASS";return FP_I13_BUDGET_PASS;} };
#endif
