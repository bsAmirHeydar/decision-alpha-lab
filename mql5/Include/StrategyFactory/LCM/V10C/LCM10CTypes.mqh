#ifndef __LCM10C_TYPES_MQH__
#define __LCM10C_TYPES_MQH__
enum ENUM_LCM10C_STATE { LCM10C_CREATED=0, LCM10C_VALIDATING=1, LCM10C_REJECTED=2, LCM10C_DRY_RUN_ACCEPTED=3, LCM10C_EXECUTION_BLOCKED=4 };
struct LCM10CReceipt { string request_id; ENUM_LCM10C_STATE final_state; int rejection_count; int submission_attempt_count; int live_order_count; int capital_activation_count; };
#endif
