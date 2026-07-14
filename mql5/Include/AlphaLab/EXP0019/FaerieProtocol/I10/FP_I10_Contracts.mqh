#ifndef __FP_I10_CONTRACTS_MQH__
#define __FP_I10_CONTRACTS_MQH__
#include "FP_I10_Enums.mqh"
struct SFP_I10_Config { string context_id; string context_epoch; string primary_symbol; string secondary_symbol; string pair_id; int host_timeframe_minutes; int timer_seconds; int history_days; int max_incremental_minutes; bool enable_state_buffers; bool enable_diagnostics; string config_hash; };
struct SFP_I10_Instance { string instance_id; long chart_id; string terminal_instance_id; string pair_id; string context_epoch; string config_hash; string object_namespace; string checkpoint_key; };
struct SFP_I10_ModuleHealth { string phase_id; string version; ENUM_FP_I10_HEALTH health; datetime last_processed_m1; string source_revision_id; long work_units; string reason_code; };
struct SFP_I10_Health { ENUM_FP_I10_HEALTH overall; ENUM_FP_I10_LIFECYCLE lifecycle; ENUM_FP_I10_DATA_READINESS data_readiness; bool history_ready; ENUM_FP_I10_CHECKPOINT checkpoint; int incremental_lag_minutes; long last_processing_us; string reason_code; };
struct SFP_I10_Output { double health_code; double lifecycle_code; double data_readiness_code; double active_ww_direction; double confirmed_signal_count; double allowed_signal_count; double suppressed_by_ww_count; double suppressed_by_quota_count; double quota_winner_present; double ledger_event_count; double source_revision_sequence; double heartbeat_utc_minute; string snapshot_hash; };
struct SFP_I10_EngineSnapshot { long sequence; SFP_I10_Instance instance; SFP_I10_Health health; SFP_I10_Output output; datetime last_processed_m1; string source_revision_id; string snapshot_hash; };
#endif
