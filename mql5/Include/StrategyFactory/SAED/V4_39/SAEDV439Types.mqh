#ifndef SAED_V4_39_TYPES_MQH
#define SAED_V4_39_TYPES_MQH
struct SAEDV439Intent { string intent_id; string instrument; string side; double reference_price; double size_fraction; double risk_fraction; bool submission_allowed; };
struct SAEDV439RiskState { int orders_today; int concurrent_positions; double daily_loss_fraction; double drawdown_fraction; bool kill_switch_armed; };
struct SAEDV439Qualification { bool paper_reference_passed; bool shadow_reference_passed; bool external_runtime_passed; bool micro_live_authorized; };
#endif
