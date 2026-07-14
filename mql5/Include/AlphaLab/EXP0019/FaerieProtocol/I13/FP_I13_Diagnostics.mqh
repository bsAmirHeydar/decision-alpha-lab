#ifndef __FP_I13_DIAGNOSTICS_MQH__
#define __FP_I13_DIAGNOSTICS_MQH__
#include "FP_I13_Contracts.mqh"
string FP_I13_StatusText(ENUM_FP_I13_BUDGET_STATUS s){if(s==FP_I13_BUDGET_BLOCKED)return "BLOCKED";if(s==FP_I13_BUDGET_DEGRADED)return "DEGRADED";return "READY";}
#endif
