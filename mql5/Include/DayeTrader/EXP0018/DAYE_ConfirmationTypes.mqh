#ifndef __EXP0018_DAYE_CONFIRMATION_TYPES_MQH__
#define __EXP0018_DAYE_CONFIRMATION_TYPES_MQH__

#include <DayeTrader/EXP0018/DAYE_HuntEngine.mqh>

// EXP0018 Phase 06 — Host-Timeframe Close Confirmation v2.
// This layer converts live P05 one-sided transitions into immutable close outcomes.
// It does not retire references, draw objects, map HIGH/LOW to BUY/SELL, size risk, or place orders.

#define DAYE_CONFIRMATION_SCHEMA_VERSION 2

enum DAYE_HostClockStatus
{
   DAYE_HOST_CLOCK_UNKNOWN = 0,
   DAYE_HOST_CLOCK_READY = 1,
   DAYE_HOST_CLOCK_SYMBOL_A_UNAVAILABLE = 2,
   DAYE_HOST_CLOCK_SYMBOL_B_UNAVAILABLE = 3,
   DAYE_HOST_CLOCK_TIMESTAMP_MISMATCH = 4,
   DAYE_HOST_CLOCK_INVALID_TIMEFRAME = 5,
   DAYE_HOST_CLOCK_TIME_CONVERSION_FAILED = 6,
   DAYE_HOST_CLOCK_DATA_REGRESSION = 7
};

enum DAYE_ConfirmationCandidateState
{
   DAYE_CONFIRM_CANDIDATE_UNKNOWN = 0,
   DAYE_CONFIRM_CANDIDATE_PENDING = 1,
   DAYE_CONFIRM_CANDIDATE_FINALIZED = 2,
   DAYE_CONFIRM_CANDIDATE_UNAVAILABLE = 3
};

enum DAYE_ConfirmationOutcome
{
   DAYE_CONFIRM_OUTCOME_UNKNOWN = 0,
   DAYE_CONFIRM_OUTCOME_CONFIRMED = 1,
   DAYE_CONFIRM_OUTCOME_INVALIDATED_DOUBLE_HUNT = 2,
   DAYE_CONFIRM_OUTCOME_NO_SIGNAL_AT_CLOSE = 3,
   DAYE_CONFIRM_OUTCOME_UNAVAILABLE_AT_CLOSE = 4,
   DAYE_CONFIRM_OUTCOME_INVALIDATED_ROLE_CHANGED = 5,
   DAYE_CONFIRM_OUTCOME_MISSED_CLOSE_REPLAY_REQUIRED = 6
};

enum DAYE_ConfirmationStatus
{
   DAYE_CONFIRM_STATUS_UNKNOWN = 0,
   DAYE_CONFIRM_STATUS_READY = 1,
   DAYE_CONFIRM_STATUS_SOURCE_NOT_READY = 2,
   DAYE_CONFIRM_STATUS_HOST_CLOCK_NOT_READY = 3,
   DAYE_CONFIRM_STATUS_INVALID_CONFIG = 4,
   DAYE_CONFIRM_STATUS_DUPLICATE_CANDIDATE_ID = 5,
   DAYE_CONFIRM_STATUS_DUPLICATE_RESULT_ID = 6,
   DAYE_CONFIRM_STATUS_CHECKPOINT_ERROR = 7,
   DAYE_CONFIRM_STATUS_IO_ERROR = 8,
   DAYE_CONFIRM_STATUS_NO_LIVE_TRANSITIONS_YET = 9
};

enum DAYE_ConfirmationEventType
{
   DAYE_CONFIRM_EVENT_NONE = 0,
   DAYE_CONFIRM_EVENT_ENGINE_INITIALIZED = 1,
   DAYE_CONFIRM_EVENT_STATUS_CHANGED = 2,
   DAYE_CONFIRM_EVENT_HOST_BAR_CLOSED = 3,
   DAYE_CONFIRM_EVENT_HOST_CLOSE_MISSED = 4,
   DAYE_CONFIRM_EVENT_CANDIDATE_OPENED = 5,
   DAYE_CONFIRM_EVENT_CANDIDATE_UPDATED = 6,
   DAYE_CONFIRM_EVENT_CONFIRMED = 7,
   DAYE_CONFIRM_EVENT_INVALIDATED_DOUBLE_HUNT = 8,
   DAYE_CONFIRM_EVENT_NO_SIGNAL_AT_CLOSE = 9,
   DAYE_CONFIRM_EVENT_UNAVAILABLE_AT_CLOSE = 10,
   DAYE_CONFIRM_EVENT_ROLE_CHANGED = 11,
   DAYE_CONFIRM_EVENT_CHECKPOINT_RESTORED = 12,
   DAYE_CONFIRM_EVENT_CHECKPOINT_SAVED = 13,
   DAYE_CONFIRM_EVENT_SOURCE_BASELINED = 14
};

struct DAYE_ConfirmationConfig
{
   int schema_version;
   DAYE_HuntConfig hunt_config;
   ENUM_TIMEFRAMES host_timeframe;
   bool require_exact_host_symbol_alignment;
   bool require_closed_host_bars;
   bool persist_checkpoint;
   string checkpoint_prefix;
   bool publish_nonconfirmed_results;
   bool fail_closed_on_missed_host_close;
   int maximum_pending_candidates;
   int maximum_results_to_publish;
   int maximum_finalized_ids_to_remember;
};

struct DAYE_HostBarSnapshot
{
   int schema_version;
   DAYE_HostClockStatus status;
   string reason_code;
   bool is_available;
   bool is_replay_safe;
   string broker_symbol;
   string canonical_symbol;
   ENUM_TIMEFRAMES timeframe;
   int timeframe_seconds;
   datetime broker_open_time;
   datetime open_time_utc;
   datetime close_time_utc;
   double open;
   double high;
   double low;
   double close;
   long tick_volume;
   int spread;
   long real_volume;
};

struct DAYE_HostBarPair
{
   int schema_version;
   DAYE_HostClockStatus status;
   string reason_code;
   bool is_ready;
   bool is_replay_safe;
   string host_bar_id;
   ENUM_TIMEFRAMES timeframe;
   int timeframe_seconds;
   datetime open_time_utc;
   datetime close_time_utc;
   DAYE_HostBarSnapshot symbol_a;
   DAYE_HostBarSnapshot symbol_b;
};

struct DAYE_HostClockSnapshot
{
   int schema_version;
   DAYE_HostClockStatus status;
   string reason_code;
   bool is_ready;
   bool is_replay_safe;
   ENUM_TIMEFRAMES timeframe;
   int timeframe_seconds;
   datetime processing_time_utc;
   DAYE_HostBarPair current_open_bar;
   DAYE_HostBarPair latest_closed_bar;
};

struct DAYE_ConfirmationCandidate
{
   int schema_version;
   DAYE_ConfirmationCandidateState state;
   DAYE_ConfirmationStatus status;
   string reason_code;
   bool is_replay_safe;
   string candidate_id;
   string observation_id;
   string opportunity_id;
   string relationship_id;
   string source_alias;
   bool is_major;
   string chart_label;
   DAYE_HuntSide side;
   DAYE_HuntPairState initial_pair_state;
   DAYE_HuntPairState last_pair_state;
   string hunter_broker_symbol;
   string hunter_canonical_symbol;
   string protected_broker_symbol;
   string protected_canonical_symbol;
   string current_period_instance_id;
   string reference_period_instance_id;
   double hunter_reference_price;
   double protected_reference_price;
   datetime first_seen_event_time_utc;
   datetime first_seen_availability_time_utc;
   datetime last_seen_availability_time_utc;
   datetime target_host_open_utc;
   datetime target_host_close_utc;
   string target_host_bar_id;
   int update_count;
};

struct DAYE_ConfirmationResult
{
   int schema_version;
   DAYE_ConfirmationStatus status;
   DAYE_ConfirmationOutcome outcome;
   string reason_code;
   bool is_final;
   bool is_confirmed;
   bool is_immutable;
   bool is_replay_safe;
   string result_id;
   string candidate_id;
   string observation_id;
   string opportunity_id;
   string relationship_id;
   string source_alias;
   bool is_major;
   string chart_label;
   DAYE_HuntSide side;
   DAYE_HuntPairState initial_pair_state;
   DAYE_HuntPairState close_pair_state;
   string hunter_broker_symbol;
   string hunter_canonical_symbol;
   string protected_broker_symbol;
   string protected_canonical_symbol;
   string current_period_instance_id;
   string reference_period_instance_id;
   double hunter_reference_price;
   double protected_reference_price;
   datetime candidate_first_seen_utc;
   datetime host_bar_open_utc;
   datetime host_bar_close_utc;
   string host_bar_id;
   double hunter_host_open;
   double hunter_host_high;
   double hunter_host_low;
   double hunter_host_close;
   double confirmation_endpoint_price;
   datetime event_time_utc;
   datetime availability_time_utc;
   datetime processing_time_utc;
};

struct DAYE_ConfirmationSourceMemory
{
   string observation_id;
   DAYE_HuntObservationStatus status;
   DAYE_HuntPairState pair_state;
   datetime availability_time_utc;
   bool is_one_sided;
};

struct DAYE_ConfirmationStoreSummary
{
   int schema_version;
   DAYE_ConfirmationStatus status;
   string reason_code;
   bool is_ready;
   bool is_replay_safe;
   bool source_baselined;
   bool checkpoint_restored;
   string run_key;
   ENUM_TIMEFRAMES host_timeframe;
   int host_timeframe_seconds;
   datetime event_time_utc;
   datetime availability_time_utc;
   datetime processing_time_utc;
   datetime latest_closed_host_open_utc;
   datetime latest_closed_host_close_utc;
   int source_observation_count;
   int pending_candidate_count;
   int result_count;
   int confirmed_count;
   int invalidated_double_hunt_count;
   int no_signal_count;
   int unavailable_count;
   int role_changed_count;
   int missed_close_count;
   int restored_candidate_count;
   int remembered_finalized_count;
   string latest_candidate_id;
   string latest_result_id;
   string latest_confirmed_result_id;
};

struct DAYE_ConfirmationEvent
{
   int schema_version;
   DAYE_ConfirmationEventType event_type;
   string event_id;
   string candidate_id;
   string result_id;
   string observation_id;
   string relationship_id;
   DAYE_HuntSide side;
   DAYE_HuntPairState from_pair_state;
   DAYE_HuntPairState to_pair_state;
   DAYE_ConfirmationOutcome outcome;
   datetime event_time_utc;
   datetime availability_time_utc;
   datetime processing_time_utc;
   string reason_code;
};

string DAYE_HostClockStatusToString(const DAYE_HostClockStatus value)
{
   switch(value)
   {
      case DAYE_HOST_CLOCK_READY: return "READY";
      case DAYE_HOST_CLOCK_SYMBOL_A_UNAVAILABLE: return "SYMBOL_A_UNAVAILABLE";
      case DAYE_HOST_CLOCK_SYMBOL_B_UNAVAILABLE: return "SYMBOL_B_UNAVAILABLE";
      case DAYE_HOST_CLOCK_TIMESTAMP_MISMATCH: return "TIMESTAMP_MISMATCH";
      case DAYE_HOST_CLOCK_INVALID_TIMEFRAME: return "INVALID_TIMEFRAME";
      case DAYE_HOST_CLOCK_TIME_CONVERSION_FAILED: return "TIME_CONVERSION_FAILED";
      case DAYE_HOST_CLOCK_DATA_REGRESSION: return "DATA_REGRESSION";
      default: return "UNKNOWN";
   }
}

string DAYE_ConfirmationCandidateStateToString(const DAYE_ConfirmationCandidateState value)
{
   switch(value)
   {
      case DAYE_CONFIRM_CANDIDATE_PENDING: return "PENDING";
      case DAYE_CONFIRM_CANDIDATE_FINALIZED: return "FINALIZED";
      case DAYE_CONFIRM_CANDIDATE_UNAVAILABLE: return "UNAVAILABLE";
      default: return "UNKNOWN";
   }
}

string DAYE_ConfirmationOutcomeToString(const DAYE_ConfirmationOutcome value)
{
   switch(value)
   {
      case DAYE_CONFIRM_OUTCOME_CONFIRMED: return "CONFIRMED";
      case DAYE_CONFIRM_OUTCOME_INVALIDATED_DOUBLE_HUNT: return "INVALIDATED_DOUBLE_HUNT";
      case DAYE_CONFIRM_OUTCOME_NO_SIGNAL_AT_CLOSE: return "NO_SIGNAL_AT_CLOSE";
      case DAYE_CONFIRM_OUTCOME_UNAVAILABLE_AT_CLOSE: return "UNAVAILABLE_AT_CLOSE";
      case DAYE_CONFIRM_OUTCOME_INVALIDATED_ROLE_CHANGED: return "INVALIDATED_ROLE_CHANGED";
      case DAYE_CONFIRM_OUTCOME_MISSED_CLOSE_REPLAY_REQUIRED: return "MISSED_CLOSE_REPLAY_REQUIRED";
      default: return "UNKNOWN";
   }
}

string DAYE_ConfirmationStatusToString(const DAYE_ConfirmationStatus value)
{
   switch(value)
   {
      case DAYE_CONFIRM_STATUS_READY: return "READY";
      case DAYE_CONFIRM_STATUS_SOURCE_NOT_READY: return "SOURCE_NOT_READY";
      case DAYE_CONFIRM_STATUS_HOST_CLOCK_NOT_READY: return "HOST_CLOCK_NOT_READY";
      case DAYE_CONFIRM_STATUS_INVALID_CONFIG: return "INVALID_CONFIG";
      case DAYE_CONFIRM_STATUS_DUPLICATE_CANDIDATE_ID: return "DUPLICATE_CANDIDATE_ID";
      case DAYE_CONFIRM_STATUS_DUPLICATE_RESULT_ID: return "DUPLICATE_RESULT_ID";
      case DAYE_CONFIRM_STATUS_CHECKPOINT_ERROR: return "CHECKPOINT_ERROR";
      case DAYE_CONFIRM_STATUS_IO_ERROR: return "IO_ERROR";
      case DAYE_CONFIRM_STATUS_NO_LIVE_TRANSITIONS_YET: return "NO_LIVE_TRANSITIONS_YET";
      default: return "UNKNOWN";
   }
}

string DAYE_ConfirmationEventTypeToString(const DAYE_ConfirmationEventType value)
{
   switch(value)
   {
      case DAYE_CONFIRM_EVENT_ENGINE_INITIALIZED: return "ENGINE_INITIALIZED";
      case DAYE_CONFIRM_EVENT_STATUS_CHANGED: return "STATUS_CHANGED";
      case DAYE_CONFIRM_EVENT_HOST_BAR_CLOSED: return "HOST_BAR_CLOSED";
      case DAYE_CONFIRM_EVENT_HOST_CLOSE_MISSED: return "HOST_CLOSE_MISSED";
      case DAYE_CONFIRM_EVENT_CANDIDATE_OPENED: return "CANDIDATE_OPENED";
      case DAYE_CONFIRM_EVENT_CANDIDATE_UPDATED: return "CANDIDATE_UPDATED";
      case DAYE_CONFIRM_EVENT_CONFIRMED: return "CONFIRMED";
      case DAYE_CONFIRM_EVENT_INVALIDATED_DOUBLE_HUNT: return "INVALIDATED_DOUBLE_HUNT";
      case DAYE_CONFIRM_EVENT_NO_SIGNAL_AT_CLOSE: return "NO_SIGNAL_AT_CLOSE";
      case DAYE_CONFIRM_EVENT_UNAVAILABLE_AT_CLOSE: return "UNAVAILABLE_AT_CLOSE";
      case DAYE_CONFIRM_EVENT_ROLE_CHANGED: return "ROLE_CHANGED";
      case DAYE_CONFIRM_EVENT_CHECKPOINT_RESTORED: return "CHECKPOINT_RESTORED";
      case DAYE_CONFIRM_EVENT_CHECKPOINT_SAVED: return "CHECKPOINT_SAVED";
      case DAYE_CONFIRM_EVENT_SOURCE_BASELINED: return "SOURCE_BASELINED";
      default: return "NONE";
   }
}

#endif
