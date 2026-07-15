#ifndef __SAED_V4_EXECUTION_TWIN_TYPES_MQH__
#define __SAED_V4_EXECUTION_TWIN_TYPES_MQH__
enum ENUM_SAED_V4_09_TWIN_STATUS { SAED_TWIN_NON_ORDER=0, SAED_TWIN_REJECTED=1, SAED_TWIN_UNFILLED=2, SAED_TWIN_PARTIAL=3, SAED_TWIN_FILLED=4, SAED_TWIN_BROKER_INFEASIBLE=5 };
struct SAEDV409TwinProjection { string source_row_id; string scenario_id; ENUM_SAED_V4_09_TWIN_STATUS status; double fill_probability; double fill_fraction; double incremental_cost_r; bool synthetic_watermark; };
#endif
