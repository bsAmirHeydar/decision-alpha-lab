#ifndef __FP_I14_CONTRACTS_MQH__
#define __FP_I14_CONTRACTS_MQH__
#include "FP_I14_Enums.mqh"
struct FP_I14_TraceEvent { long sequence; datetime event_time; ENUM_FP_I14_PRODUCT product; ENUM_FP_I14_EVENT event_type; string semantic_id; string payload_hash; string config_hash; string source_revision_id; string state; int buffer_index; double numeric_value; };
struct FP_I14_DifferentialSummary { ENUM_FP_I14_STATUS status; long compared_events; long mismatches; string first_reason_code; string report_hash; };
struct FP_I14_HealthSnapshot { ENUM_FP_I14_STATUS status; long indicator_events; long ea_events; long mismatches; long trace_lag; string reason_code; };
#endif
