#ifndef SAED_V4_12_TYPES_MQH
#define SAED_V4_12_TYPES_MQH
#define SAED_V4_12_PHASE "SAED_V4_12"
struct SAEDV412State { double hidden[10]; long step_count; string state_hash; };
struct SAEDV412ResetPolicy { bool reset_on_root_change; bool reset_on_domain_change; int gap_reset_seconds; bool fail_closed; };
#endif
