#ifndef __EXP0018_DAYE_HUNT_TYPES_MQH__
#define __EXP0018_DAYE_HUNT_TYPES_MQH__

#include <DayeTrader/EXP0018/DAYE_RelationshipEngine.mqh>

// EXP0018 Phase 05 — Touch-Only Hunt Observation v2.
// This layer classifies symbol-local touches against resolved P04 references.
// It does not map HIGH/LOW to BUY/SELL, confirm at host candle close, retire references,
// draw chart objects, size risk, or place orders.

#define DAYE_HUNT_SCHEMA_VERSION 2

enum DAYE_HuntSide
{
   DAYE_HUNT_SIDE_UNKNOWN = 0,
   DAYE_HUNT_SIDE_HIGH = 1,
   DAYE_HUNT_SIDE_LOW = 2
};

enum DAYE_SymbolHuntState
{
   DAYE_SYMBOL_HUNT_UNKNOWN = 0,
   DAYE_SYMBOL_HUNT_NOT_HUNTED = 1,
   DAYE_SYMBOL_HUNT_HUNTED = 2,
   DAYE_SYMBOL_HUNT_UNAVAILABLE = 3
};

enum DAYE_HuntPairState
{
   DAYE_HUNT_PAIR_UNKNOWN = 0,
   DAYE_HUNT_PAIR_NONE = 1,
   DAYE_HUNT_PAIR_A_ONLY = 2,
   DAYE_HUNT_PAIR_B_ONLY = 3,
   DAYE_HUNT_PAIR_BOTH = 4,
   DAYE_HUNT_PAIR_UNAVAILABLE = 5
};

enum DAYE_HuntObservationStatus
{
   DAYE_HUNT_STATUS_UNKNOWN = 0,
   DAYE_HUNT_STATUS_READY = 1,
   DAYE_HUNT_STATUS_RELATIONSHIP_NOT_READY = 2,
   DAYE_HUNT_STATUS_SOURCE_UNAVAILABLE = 3,
   DAYE_HUNT_STATUS_INVALID_REFERENCE_PRICE = 4,
   DAYE_HUNT_STATUS_INVALID_CURRENT_EXTREME = 5,
   DAYE_HUNT_STATUS_DUPLICATE_OBSERVATION_ID = 6,
   DAYE_HUNT_STATUS_INSUFFICIENT_READY_OBSERVATIONS = 7,
   DAYE_HUNT_STATUS_INVALID_CONFIG = 8,
   DAYE_HUNT_STATUS_IO_ERROR = 9
};

enum DAYE_HuntEventType
{
   DAYE_HUNT_EVENT_NONE = 0,
   DAYE_HUNT_EVENT_ENGINE_INITIALIZED = 1,
   DAYE_HUNT_EVENT_STATUS_CHANGED = 2,
   DAYE_HUNT_EVENT_STORE_READY = 3,
   DAYE_HUNT_EVENT_STORE_DEGRADED = 4,
   DAYE_HUNT_EVENT_SOURCE_UNAVAILABLE = 5,
   DAYE_HUNT_EVENT_LATEST_OBSERVATION_ADVANCED = 6,
   DAYE_HUNT_EVENT_OBSERVATION_STATE_CHANGED = 7,
   DAYE_HUNT_EVENT_ONE_SIDED_HUNT_APPEARED = 8,
   DAYE_HUNT_EVENT_DOUBLE_HUNT_APPEARED = 9
};

struct DAYE_HuntConfig
{
   int schema_version;
   DAYE_RelationshipConfig relationship_config;
   bool enable_high_side;
   bool enable_low_side;
   bool equality_counts_as_hunt;
   bool publish_unavailable_observations;
   bool require_positive_prices;
   int minimum_ready_observations;
   int maximum_observations_to_publish;
};

struct DAYE_SymbolHuntFact
{
   int schema_version;
   DAYE_HuntObservationStatus status;
   string reason_code;
   DAYE_SymbolHuntState state;
   bool is_available;
   bool is_hunted;
   bool touched_by_equality;
   bool touched_beyond;

   string broker_symbol;
   string canonical_symbol;
   DAYE_HuntSide side;
   double reference_price;
   double current_extreme;
   double signed_penetration;

   string reference_snapshot_id;
   string current_snapshot_id;
   DAYE_PeriodCompleteness reference_completeness;
   DAYE_PeriodCompleteness current_completeness;

   datetime event_time_utc;
   datetime availability_time_utc;
};

struct DAYE_HuntObservation
{
   int schema_version;
   DAYE_HuntObservationStatus status;
   string reason_code;
   bool is_publishable;
   bool is_replay_safe;

   string observation_id;
   string opportunity_id;
   string relationship_id;
   string source_alias;
   DAYE_RelationshipFamily relationship_family;
   bool is_major;
   string chart_label;

   DAYE_HuntSide side;
   DAYE_HuntPairState pair_state;
   bool is_no_hunt;
   bool is_one_sided;
   bool is_double_hunt;
   bool current_period_is_open;

   string hunter_broker_symbol;
   string hunter_canonical_symbol;
   string protected_broker_symbol;
   string protected_canonical_symbol;

   string current_period_instance_id;
   string current_period_code;
   string current_trading_day_key;
   string reference_period_instance_id;
   string reference_period_code;
   string reference_trading_day_key;

   datetime event_time_utc;
   datetime availability_time_utc;
   datetime processing_time_utc;

   DAYE_SymbolHuntFact symbol_a;
   DAYE_SymbolHuntFact symbol_b;
};

struct DAYE_HuntStoreSummary
{
   int schema_version;
   DAYE_HuntObservationStatus status;
   string reason_code;
   bool is_ready;
   bool is_complete;
   bool is_replay_safe;
   string run_key;

   datetime event_time_utc;
   datetime availability_time_utc;
   datetime processing_time_utc;

   int source_resolution_count;
   int observation_count;
   int ready_observation_count;
   int unavailable_observation_count;
   int high_side_count;
   int low_side_count;
   int no_hunt_count;
   int a_only_count;
   int b_only_count;
   int one_sided_count;
   int double_hunt_count;
   int open_current_count;
   int complete_current_count;
   int equality_hunt_count;

   string latest_observation_id;
   string latest_one_sided_observation_id;
   string latest_relationship_id;
   string latest_current_period_instance_id;
};

struct DAYE_HuntEvent
{
   int schema_version;
   DAYE_HuntEventType event_type;
   string event_id;
   datetime event_time_utc;
   datetime availability_time_utc;
   datetime processing_time_utc;
   DAYE_HuntObservationStatus from_status;
   DAYE_HuntObservationStatus to_status;
   DAYE_HuntPairState from_pair_state;
   DAYE_HuntPairState to_pair_state;
   string observation_id;
   string opportunity_id;
   string relationship_id;
   DAYE_HuntSide side;
   string reason_code;
};

string DAYE_HuntSideToString(const DAYE_HuntSide value)
{
   switch(value)
   {
      case DAYE_HUNT_SIDE_HIGH: return "HIGH";
      case DAYE_HUNT_SIDE_LOW: return "LOW";
      default: return "UNKNOWN";
   }
}

string DAYE_SymbolHuntStateToString(const DAYE_SymbolHuntState value)
{
   switch(value)
   {
      case DAYE_SYMBOL_HUNT_NOT_HUNTED: return "NOT_HUNTED";
      case DAYE_SYMBOL_HUNT_HUNTED: return "HUNTED";
      case DAYE_SYMBOL_HUNT_UNAVAILABLE: return "UNAVAILABLE";
      default: return "UNKNOWN";
   }
}

string DAYE_HuntPairStateToString(const DAYE_HuntPairState value)
{
   switch(value)
   {
      case DAYE_HUNT_PAIR_NONE: return "NONE";
      case DAYE_HUNT_PAIR_A_ONLY: return "A_ONLY";
      case DAYE_HUNT_PAIR_B_ONLY: return "B_ONLY";
      case DAYE_HUNT_PAIR_BOTH: return "BOTH";
      case DAYE_HUNT_PAIR_UNAVAILABLE: return "UNAVAILABLE";
      default: return "UNKNOWN";
   }
}

string DAYE_HuntObservationStatusToString(const DAYE_HuntObservationStatus value)
{
   switch(value)
   {
      case DAYE_HUNT_STATUS_READY: return "READY";
      case DAYE_HUNT_STATUS_RELATIONSHIP_NOT_READY: return "RELATIONSHIP_NOT_READY";
      case DAYE_HUNT_STATUS_SOURCE_UNAVAILABLE: return "SOURCE_UNAVAILABLE";
      case DAYE_HUNT_STATUS_INVALID_REFERENCE_PRICE: return "INVALID_REFERENCE_PRICE";
      case DAYE_HUNT_STATUS_INVALID_CURRENT_EXTREME: return "INVALID_CURRENT_EXTREME";
      case DAYE_HUNT_STATUS_DUPLICATE_OBSERVATION_ID: return "DUPLICATE_OBSERVATION_ID";
      case DAYE_HUNT_STATUS_INSUFFICIENT_READY_OBSERVATIONS: return "INSUFFICIENT_READY_OBSERVATIONS";
      case DAYE_HUNT_STATUS_INVALID_CONFIG: return "INVALID_CONFIG";
      case DAYE_HUNT_STATUS_IO_ERROR: return "IO_ERROR";
      default: return "UNKNOWN";
   }
}

string DAYE_HuntEventTypeToString(const DAYE_HuntEventType value)
{
   switch(value)
   {
      case DAYE_HUNT_EVENT_ENGINE_INITIALIZED: return "ENGINE_INITIALIZED";
      case DAYE_HUNT_EVENT_STATUS_CHANGED: return "STATUS_CHANGED";
      case DAYE_HUNT_EVENT_STORE_READY: return "STORE_READY";
      case DAYE_HUNT_EVENT_STORE_DEGRADED: return "STORE_DEGRADED";
      case DAYE_HUNT_EVENT_SOURCE_UNAVAILABLE: return "SOURCE_UNAVAILABLE";
      case DAYE_HUNT_EVENT_LATEST_OBSERVATION_ADVANCED: return "LATEST_OBSERVATION_ADVANCED";
      case DAYE_HUNT_EVENT_OBSERVATION_STATE_CHANGED: return "OBSERVATION_STATE_CHANGED";
      case DAYE_HUNT_EVENT_ONE_SIDED_HUNT_APPEARED: return "ONE_SIDED_HUNT_APPEARED";
      case DAYE_HUNT_EVENT_DOUBLE_HUNT_APPEARED: return "DOUBLE_HUNT_APPEARED";
      default: return "NONE";
   }
}

#endif
