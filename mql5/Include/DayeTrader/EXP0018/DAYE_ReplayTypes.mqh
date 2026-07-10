#ifndef __EXP0018_DAYE_REPLAY_TYPES_MQH__
#define __EXP0018_DAYE_REPLAY_TYPES_MQH__

#include <DayeTrader/EXP0018/DAYE_LifecycleStateMachine.mqh>

// EXP0018 Phase 11 — Deterministic Historical Replay v2.
// Research and reconstruction only. No drawing, direction, risk, order,
// network, licensing, model, or execution authority.

#define DAYE_REPLAY_SCHEMA_VERSION 2

enum DAYE_ReplayStatus
{
   DAYE_REPLAY_STATUS_UNKNOWN = 0,
   DAYE_REPLAY_STATUS_LOADING = 1,
   DAYE_REPLAY_STATUS_READY = 2,
   DAYE_REPLAY_STATUS_RUNNING = 3,
   DAYE_REPLAY_STATUS_COMPLETE = 4,
   DAYE_REPLAY_STATUS_INVALID_CONFIG = 5,
   DAYE_REPLAY_STATUS_SOURCE_UNAVAILABLE = 6,
   DAYE_REPLAY_STATUS_SOURCE_ALIGNMENT_FAILED = 7,
   DAYE_REPLAY_STATUS_PIPELINE_FAILED = 8,
   DAYE_REPLAY_STATUS_IO_ERROR = 9,
   DAYE_REPLAY_STATUS_CANCELLED = 10
};

enum DAYE_ReplayEventType
{
   DAYE_REPLAY_EVENT_NONE = 0,
   DAYE_REPLAY_EVENT_RUN_INITIALIZED = 1,
   DAYE_REPLAY_EVENT_SOURCE_LOADED = 2,
   DAYE_REPLAY_EVENT_CURSOR_ADVANCED = 3,
   DAYE_REPLAY_EVENT_CANDIDATE_OPENED = 4,
   DAYE_REPLAY_EVENT_CANDIDATE_UPDATED = 5,
   DAYE_REPLAY_EVENT_CONFIRMATION_FINALIZED = 6,
   DAYE_REPLAY_EVENT_REFERENCE_ACTIVATED = 7,
   DAYE_REPLAY_EVENT_USE_ACCEPTED = 8,
   DAYE_REPLAY_EVENT_USE_REJECTED = 9,
   DAYE_REPLAY_EVENT_REFERENCE_RETIRED = 10,
   DAYE_REPLAY_EVENT_RUN_COMPLETED = 11,
   DAYE_REPLAY_EVENT_RUN_FAILED = 12
};

struct DAYE_ReplayConfig
{
   int schema_version;
   DAYE_LifecycleConfig lifecycle_config;
   datetime replay_start_new_york;
   datetime replay_end_new_york;
   bool require_manual_fixed_broker_offset;
   bool require_complete_source_alignment;
   bool fail_on_partial_period_source;
   bool fail_on_pipeline_error;
   int maximum_replay_bars;
   int cursor_steps_per_timer;
   int progress_log_every_steps;
   int frame_audit_stride;
   bool write_frame_rows;
   bool write_event_rows;
   bool write_confirmation_rows;
   bool write_reference_rows;
   bool write_use_rows;
   string output_prefix;
};

struct DAYE_ReplaySource
{
   bool is_ready;
   bool is_replay_safe;
   string reason_code;
   datetime start_utc;
   datetime end_utc;
   datetime start_broker;
   datetime end_broker;
   int copied_a;
   int copied_b;
   int aligned_count;
   int unmatched_a;
   int unmatched_b;
   DAYE_SynchronizedBarPair pairs[];
};

struct DAYE_ReplayFrame
{
   int schema_version;
   int cursor_index;
   datetime event_time_utc;
   datetime availability_time_utc;
   int period_count;
   int ready_resolution_count;
   int ready_observation_count;
   int one_sided_count;
   int pending_candidate_count;
   int result_count;
   int reference_count;
   int accepted_use_count;
   string frame_hash;
};

struct DAYE_ReplayEvent
{
   int schema_version;
   DAYE_ReplayEventType event_type;
   string event_id;
   string subject_id;
   string relationship_id;
   DAYE_HuntSide side;
   datetime event_time_utc;
   datetime availability_time_utc;
   datetime processing_time_utc;
   string reason_code;
   string state_hash;
};

struct DAYE_ReplaySummary
{
   int schema_version;
   DAYE_ReplayStatus status;
   string reason_code;
   bool is_ready;
   bool is_complete;
   bool is_replay_safe;
   bool is_deterministic;
   string run_id;
   datetime start_utc;
   datetime end_utc;
   datetime processing_started_utc;
   datetime processing_completed_utc;
   int source_pair_count;
   int cursor_count;
   int processed_cursor_count;
   int maximum_period_count;
   int resolution_evaluation_count;
   int observation_evaluation_count;
   int one_sided_transition_count;
   int candidate_opened_count;
   int candidate_updated_count;
   int confirmation_result_count;
   int confirmed_count;
   int double_hunt_invalidated_count;
   int no_signal_count;
   int unavailable_count;
   int role_changed_count;
   int reference_count;
   int surviving_reference_count;
   int retired_reference_count;
   int accepted_use_count;
   int duplicate_use_count;
   int rejected_use_count;
   int source_unmatched_a;
   int source_unmatched_b;
   string source_hash;
   string confirmation_hash;
   string lifecycle_hash;
   string final_state_hash;
};

string DAYE_ReplayStatusToString(const DAYE_ReplayStatus value)
{
   switch(value)
   {
      case DAYE_REPLAY_STATUS_LOADING: return "LOADING";
      case DAYE_REPLAY_STATUS_READY: return "READY";
      case DAYE_REPLAY_STATUS_RUNNING: return "RUNNING";
      case DAYE_REPLAY_STATUS_COMPLETE: return "COMPLETE";
      case DAYE_REPLAY_STATUS_INVALID_CONFIG: return "INVALID_CONFIG";
      case DAYE_REPLAY_STATUS_SOURCE_UNAVAILABLE: return "SOURCE_UNAVAILABLE";
      case DAYE_REPLAY_STATUS_SOURCE_ALIGNMENT_FAILED: return "SOURCE_ALIGNMENT_FAILED";
      case DAYE_REPLAY_STATUS_PIPELINE_FAILED: return "PIPELINE_FAILED";
      case DAYE_REPLAY_STATUS_IO_ERROR: return "IO_ERROR";
      case DAYE_REPLAY_STATUS_CANCELLED: return "CANCELLED";
      default: return "UNKNOWN";
   }
}

string DAYE_ReplayEventTypeToString(const DAYE_ReplayEventType value)
{
   switch(value)
   {
      case DAYE_REPLAY_EVENT_RUN_INITIALIZED: return "RUN_INITIALIZED";
      case DAYE_REPLAY_EVENT_SOURCE_LOADED: return "SOURCE_LOADED";
      case DAYE_REPLAY_EVENT_CURSOR_ADVANCED: return "CURSOR_ADVANCED";
      case DAYE_REPLAY_EVENT_CANDIDATE_OPENED: return "CANDIDATE_OPENED";
      case DAYE_REPLAY_EVENT_CANDIDATE_UPDATED: return "CANDIDATE_UPDATED";
      case DAYE_REPLAY_EVENT_CONFIRMATION_FINALIZED: return "CONFIRMATION_FINALIZED";
      case DAYE_REPLAY_EVENT_REFERENCE_ACTIVATED: return "REFERENCE_ACTIVATED";
      case DAYE_REPLAY_EVENT_USE_ACCEPTED: return "USE_ACCEPTED";
      case DAYE_REPLAY_EVENT_USE_REJECTED: return "USE_REJECTED";
      case DAYE_REPLAY_EVENT_REFERENCE_RETIRED: return "REFERENCE_RETIRED";
      case DAYE_REPLAY_EVENT_RUN_COMPLETED: return "RUN_COMPLETED";
      case DAYE_REPLAY_EVENT_RUN_FAILED: return "RUN_FAILED";
      default: return "NONE";
   }
}

#endif
