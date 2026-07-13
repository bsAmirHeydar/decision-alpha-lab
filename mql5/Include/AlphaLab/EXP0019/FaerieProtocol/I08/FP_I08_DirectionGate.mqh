#ifndef FP_I08_GATE_MQH
#define FP_I08_GATE_MQH
#include "FP_I08_Contracts.mqh"
bool FP_I08_EvaluateDirectionGate(const int relation,const int direction,const FP_I08_ActiveStack &stack,FP_I08_GateDecision &out){if(relation==6){out.eligibility=FP_I08_GATE_NOT_APPLICABLE;out.reason_code="FP_WRC_WW_DIRECT_SETUP_NOT_SELF_GATED";return true;}if(stack.data_state!=FP_I08_DATA_COMPLETE){out.eligibility=FP_I08_GATE_BLOCKED;out.reason_code="FP_RC_WW_DATA_INCOMPLETE";return true;}if(stack.active_context_id==""){out.eligibility=FP_I08_GATE_ALLOWED;out.reason_code="FP_RC_WW_NONE_ALLOW_BOTH";return true;}if(direction==stack.active_direction){out.eligibility=FP_I08_GATE_ALLOWED;out.reason_code="FP_WRC_DIRECTION_ALIGNED_WITH_ACTIVE_WW";}else{out.eligibility=FP_I08_GATE_SUPPRESSED;out.reason_code="FP_RC_SUPPRESSED_BY_WW";}return true;}
#endif
