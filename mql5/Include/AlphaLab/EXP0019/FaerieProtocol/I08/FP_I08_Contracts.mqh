#ifndef FP_I08_CONTRACTS_MQH
#define FP_I08_CONTRACTS_MQH
#include "FP_I08_Enums.mqh"
struct FP_I08_WWContext{string context_id;string signal_id;int direction;int side;string hunter_symbol;string protected_symbol;double protected_reference_price;datetime confirmed_time;datetime week_end;ENUM_FP_I08_WW_STATE state;datetime neutralized_time;string reason_code;};
struct FP_I08_ActiveStack{string stack_id;string active_context_id;string active_signal_id;int active_direction;ENUM_FP_I08_DATA_STATE data_state;string reason_code;};
struct FP_I08_GateDecision{string decision_id;string subject_signal_id;int subject_relation;int subject_direction;ENUM_FP_I08_GATE eligibility;string active_context_id;string reason_code;};
#endif
