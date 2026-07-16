#ifndef __DECISION_ALPHA_LAB_SAEDV421TYPES_MQH__
#define __DECISION_ALPHA_LAB_SAEDV421TYPES_MQH__
enum ENUM_SAED_V421_OBJECTIVE { SAED_V421_MAXIMIN=0, SAED_V421_MINIMAX_REGRET=1, SAED_V421_DRO=2, SAED_V421_ROBUST_CVAR=3, SAED_V421_LEXICOGRAPHIC=4 }; struct SAEDV421Allocation { string allocation_id; double worst_case_utility; double maximum_regret; double robust_cvar; bool feasible; };
#endif
