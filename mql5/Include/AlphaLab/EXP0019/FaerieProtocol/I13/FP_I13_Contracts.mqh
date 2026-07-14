#ifndef __FP_I13_CONTRACTS_MQH__
#define __FP_I13_CONTRACTS_MQH__
#include "FP_I13_Enums.mqh"
struct SFP_I13_Config { string instance_id;ENUM_FP_I13_RELEASE_PROFILE profile;int history_days;int max_objects;int max_object_ops_per_frame;int chunk_size;bool telemetry_enabled;int diagnostics_interval_seconds;string open_decision_state; };
struct SFP_I13_Telemetry { long frame_sequence;ulong elapsed_us;int object_count;int object_ops;long event_count;long full_scan_count;long incremental_count;double events_per_second;ENUM_FP_I13_BUDGET_STATUS budget_status;string reason_code; };
struct SFP_I13_Profile { ENUM_FP_I13_RELEASE_PROFILE profile;int history_days;int max_objects;int max_object_ops_per_frame;int chunk_size;bool alerts_enabled;bool audit_export_enabled;string visual_mode; };
struct SFP_I13_Acceptance { bool replay_parity;bool restart_parity;bool timeframe_invariance;bool multi_instance_isolation;bool performance_budget;bool static_mql5;bool metaeditor_compile;ENUM_FP_I13_ACCEPTANCE_STATUS status;string reason_code; };
#endif
