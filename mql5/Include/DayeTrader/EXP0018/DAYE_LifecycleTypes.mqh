#ifndef __EXP0018_DAYE_LIFECYCLE_TYPES_MQH__
#define __EXP0018_DAYE_LIFECYCLE_TYPES_MQH__

#include <DayeTrader/EXP0018/DAYE_ConfirmationEngine.mqh>

// EXP0018 Phase 07 — Reference Lifecycle and First-Sweep State Machine v2.
// This layer owns reference survival, exact-opportunity first-use deduplication,
// protected-symbol breach retirement, and immutable lifecycle evidence.
// It does not draw, map HIGH/LOW to BUY/SELL, size risk, or place orders.

#define DAYE_LIFECYCLE_SCHEMA_VERSION 2

enum DAYE_ReferenceLifecycleState
{
   DAYE_REF_STATE_UNKNOWN = 0,
   DAYE_REF_STATE_PROTECTED_SURVIVES = 1,
   DAYE_REF_STATE_RETIRED_PROTECTED_TOUCH = 2,
   DAYE_REF_STATE_RETIRED_DOUBLE_HUNT = 3,
   DAYE_REF_STATE_RETIRED_ROLE_SWITCH = 4,
   DAYE_REF_STATE_INVALID = 5,
   DAYE_REF_STATE_UNAVAILABLE = 6
};

enum DAYE_ReferenceUseStatus
{
   DAYE_USE_STATUS_UNKNOWN = 0,
   DAYE_USE_STATUS_ACCEPTED = 1,
   DAYE_USE_STATUS_DUPLICATE_EXACT_OPPORTUNITY = 2,
   DAYE_USE_STATUS_REJECTED_REFERENCE_RETIRED = 3,
   DAYE_USE_STATUS_REJECTED_ROLE_SWITCH = 4,
   DAYE_USE_STATUS_REJECTED_INVALID_RESULT = 5,
   DAYE_USE_STATUS_UNAVAILABLE = 6
};

enum DAYE_LifecycleStatus
{
   DAYE_LIFECYCLE_STATUS_UNKNOWN = 0,
   DAYE_LIFECYCLE_STATUS_READY = 1,
   DAYE_LIFECYCLE_STATUS_SOURCE_NOT_READY = 2,
   DAYE_LIFECYCLE_STATUS_INVALID_CONFIG = 3,
   DAYE_LIFECYCLE_STATUS_DUPLICATE_REFERENCE_ID = 4,
   DAYE_LIFECYCLE_STATUS_DUPLICATE_USE_ID = 5,
   DAYE_LIFECYCLE_STATUS_CHECKPOINT_ERROR = 6,
   DAYE_LIFECYCLE_STATUS_IO_ERROR = 7,
   DAYE_LIFECYCLE_STATUS_NO_CONFIRMED_RESULTS_YET = 8
};

enum DAYE_LifecycleEventType
{
   DAYE_LIFECYCLE_EVENT_NONE = 0,
   DAYE_LIFECYCLE_EVENT_ENGINE_INITIALIZED = 1,
   DAYE_LIFECYCLE_EVENT_STATUS_CHANGED = 2,
   DAYE_LIFECYCLE_EVENT_REFERENCE_ACTIVATED = 3,
   DAYE_LIFECYCLE_EVENT_CONFIRMED_USE_ACCEPTED = 4,
   DAYE_LIFECYCLE_EVENT_DUPLICATE_USE_SUPPRESSED = 5,
   DAYE_LIFECYCLE_EVENT_REFERENCE_SURVIVED = 6,
   DAYE_LIFECYCLE_EVENT_REFERENCE_RETIRED_PROTECTED_TOUCH = 7,
   DAYE_LIFECYCLE_EVENT_REFERENCE_RETIRED_DOUBLE_HUNT = 8,
   DAYE_LIFECYCLE_EVENT_REFERENCE_RETIRED_ROLE_SWITCH = 9,
   DAYE_LIFECYCLE_EVENT_RESULT_REJECTED_RETIRED = 10,
   DAYE_LIFECYCLE_EVENT_RESULT_REJECTED_ROLE_SWITCH = 11,
   DAYE_LIFECYCLE_EVENT_CHECKPOINT_RESTORED = 12,
   DAYE_LIFECYCLE_EVENT_CHECKPOINT_SAVED = 13,
   DAYE_LIFECYCLE_EVENT_SOURCE_BASELINED = 14
};

struct DAYE_LifecycleConfig
{
   int schema_version;
   DAYE_ConfirmationConfig confirmation_config;
   bool allow_repeat_across_new_opportunities_while_protected_survives;
   bool suppress_duplicate_exact_opportunity;
   bool retire_on_protected_touch;
   bool retire_on_double_hunt;
   bool retire_on_role_switch;
   bool preserve_accepted_uses_after_retirement;
   bool publish_rejected_uses;
   bool persist_checkpoint;
   string checkpoint_prefix;
   int maximum_reference_records;
   int maximum_use_records;
   int maximum_processed_result_ids;
};

struct DAYE_ReferenceLifecycleRecord
{
   int schema_version;
   DAYE_LifecycleStatus status;
   DAYE_ReferenceLifecycleState state;
   string reason_code;
   bool is_replay_safe;
   bool is_retired;
   bool is_immutable;

   string reference_id;
   string reference_period_instance_id;
   DAYE_HuntSide side;

   string broker_symbol_a;
   string canonical_symbol_a;
   string broker_symbol_b;
   string canonical_symbol_b;
   double reference_price_a;
   double reference_price_b;

   string first_hunter_canonical_symbol;
   string protected_canonical_symbol;
   string first_confirmation_result_id;
   string latest_confirmation_result_id;
   string latest_observation_id;
   DAYE_HuntPairState latest_pair_state;

   datetime activation_event_time_utc;
   datetime activation_availability_time_utc;
   datetime latest_use_event_time_utc;
   datetime latest_observation_availability_time_utc;
   datetime retirement_event_time_utc;
   datetime retirement_availability_time_utc;

   int accepted_use_count;
   int duplicate_use_count;
   int rejected_use_count;
   string retirement_evidence_id;
};

struct DAYE_ReferenceUseRecord
{
   int schema_version;
   DAYE_ReferenceUseStatus status;
   string reason_code;
   bool is_accepted;
   bool is_historical_immutable;
   bool is_replay_safe;

   string use_id;
   string exact_opportunity_use_key;
   string reference_id;
   string result_id;
   string candidate_id;
   string observation_id;
   string opportunity_id;
   string relationship_id;
   string source_alias;
   bool is_major;
   string chart_label;
   DAYE_HuntSide side;

   string hunter_broker_symbol;
   string hunter_canonical_symbol;
   string protected_broker_symbol;
   string protected_canonical_symbol;
   string current_period_instance_id;
   string reference_period_instance_id;

   double hunter_reference_price;
   double protected_reference_price;
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

struct DAYE_LifecycleStoreSummary
{
   int schema_version;
   DAYE_LifecycleStatus status;
   string reason_code;
   bool is_ready;
   bool is_replay_safe;
   bool checkpoint_restored;
   bool source_baselined;
   string run_key;

   datetime event_time_utc;
   datetime availability_time_utc;
   datetime processing_time_utc;

   int source_result_count;
   int source_observation_count;
   int reference_count;
   int surviving_reference_count;
   int retired_reference_count;
   int accepted_use_count;
   int duplicate_use_count;
   int rejected_use_count;
   int processed_result_id_count;
   int retired_protected_touch_count;
   int retired_double_hunt_count;
   int retired_role_switch_count;

   string latest_reference_id;
   string latest_use_id;
   string latest_retired_reference_id;
};

struct DAYE_LifecycleEvent
{
   int schema_version;
   DAYE_LifecycleEventType event_type;
   string event_id;
   string reference_id;
   string use_id;
   string result_id;
   string observation_id;
   string relationship_id;
   DAYE_HuntSide side;
   DAYE_ReferenceLifecycleState from_state;
   DAYE_ReferenceLifecycleState to_state;
   DAYE_ReferenceUseStatus use_status;
   datetime event_time_utc;
   datetime availability_time_utc;
   datetime processing_time_utc;
   string reason_code;
};

string DAYE_ReferenceLifecycleStateToString(const DAYE_ReferenceLifecycleState value)
{
   switch(value)
   {
      case DAYE_REF_STATE_PROTECTED_SURVIVES: return "PROTECTED_SURVIVES";
      case DAYE_REF_STATE_RETIRED_PROTECTED_TOUCH: return "RETIRED_PROTECTED_TOUCH";
      case DAYE_REF_STATE_RETIRED_DOUBLE_HUNT: return "RETIRED_DOUBLE_HUNT";
      case DAYE_REF_STATE_RETIRED_ROLE_SWITCH: return "RETIRED_ROLE_SWITCH";
      case DAYE_REF_STATE_INVALID: return "INVALID";
      case DAYE_REF_STATE_UNAVAILABLE: return "UNAVAILABLE";
      default: return "UNKNOWN";
   }
}

string DAYE_ReferenceUseStatusToString(const DAYE_ReferenceUseStatus value)
{
   switch(value)
   {
      case DAYE_USE_STATUS_ACCEPTED: return "ACCEPTED";
      case DAYE_USE_STATUS_DUPLICATE_EXACT_OPPORTUNITY: return "DUPLICATE_EXACT_OPPORTUNITY";
      case DAYE_USE_STATUS_REJECTED_REFERENCE_RETIRED: return "REJECTED_REFERENCE_RETIRED";
      case DAYE_USE_STATUS_REJECTED_ROLE_SWITCH: return "REJECTED_ROLE_SWITCH";
      case DAYE_USE_STATUS_REJECTED_INVALID_RESULT: return "REJECTED_INVALID_RESULT";
      case DAYE_USE_STATUS_UNAVAILABLE: return "UNAVAILABLE";
      default: return "UNKNOWN";
   }
}

string DAYE_LifecycleStatusToString(const DAYE_LifecycleStatus value)
{
   switch(value)
   {
      case DAYE_LIFECYCLE_STATUS_READY: return "READY";
      case DAYE_LIFECYCLE_STATUS_SOURCE_NOT_READY: return "SOURCE_NOT_READY";
      case DAYE_LIFECYCLE_STATUS_INVALID_CONFIG: return "INVALID_CONFIG";
      case DAYE_LIFECYCLE_STATUS_DUPLICATE_REFERENCE_ID: return "DUPLICATE_REFERENCE_ID";
      case DAYE_LIFECYCLE_STATUS_DUPLICATE_USE_ID: return "DUPLICATE_USE_ID";
      case DAYE_LIFECYCLE_STATUS_CHECKPOINT_ERROR: return "CHECKPOINT_ERROR";
      case DAYE_LIFECYCLE_STATUS_IO_ERROR: return "IO_ERROR";
      case DAYE_LIFECYCLE_STATUS_NO_CONFIRMED_RESULTS_YET: return "NO_CONFIRMED_RESULTS_YET";
      default: return "UNKNOWN";
   }
}

string DAYE_LifecycleEventTypeToString(const DAYE_LifecycleEventType value)
{
   switch(value)
   {
      case DAYE_LIFECYCLE_EVENT_ENGINE_INITIALIZED: return "ENGINE_INITIALIZED";
      case DAYE_LIFECYCLE_EVENT_STATUS_CHANGED: return "STATUS_CHANGED";
      case DAYE_LIFECYCLE_EVENT_REFERENCE_ACTIVATED: return "REFERENCE_ACTIVATED";
      case DAYE_LIFECYCLE_EVENT_CONFIRMED_USE_ACCEPTED: return "CONFIRMED_USE_ACCEPTED";
      case DAYE_LIFECYCLE_EVENT_DUPLICATE_USE_SUPPRESSED: return "DUPLICATE_USE_SUPPRESSED";
      case DAYE_LIFECYCLE_EVENT_REFERENCE_SURVIVED: return "REFERENCE_SURVIVED";
      case DAYE_LIFECYCLE_EVENT_REFERENCE_RETIRED_PROTECTED_TOUCH: return "REFERENCE_RETIRED_PROTECTED_TOUCH";
      case DAYE_LIFECYCLE_EVENT_REFERENCE_RETIRED_DOUBLE_HUNT: return "REFERENCE_RETIRED_DOUBLE_HUNT";
      case DAYE_LIFECYCLE_EVENT_REFERENCE_RETIRED_ROLE_SWITCH: return "REFERENCE_RETIRED_ROLE_SWITCH";
      case DAYE_LIFECYCLE_EVENT_RESULT_REJECTED_RETIRED: return "RESULT_REJECTED_RETIRED";
      case DAYE_LIFECYCLE_EVENT_RESULT_REJECTED_ROLE_SWITCH: return "RESULT_REJECTED_ROLE_SWITCH";
      case DAYE_LIFECYCLE_EVENT_CHECKPOINT_RESTORED: return "CHECKPOINT_RESTORED";
      case DAYE_LIFECYCLE_EVENT_CHECKPOINT_SAVED: return "CHECKPOINT_SAVED";
      case DAYE_LIFECYCLE_EVENT_SOURCE_BASELINED: return "SOURCE_BASELINED";
      default: return "NONE";
   }
}

#endif
