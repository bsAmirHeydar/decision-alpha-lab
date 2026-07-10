#ifndef __EXP0018_DAYE_RELATIONSHIP_TYPES_MQH__
#define __EXP0018_DAYE_RELATIONSHIP_TYPES_MQH__

#include <DayeTrader/EXP0018/DAYE_PeriodEngine.mqh>

// EXP0018 Phase 04 — Declarative 22-Relationship Registry v2.
// This module defines topology and resolution types only.
// It has no hunt, direction, divergence, drawing, risk, or order authority.

#define DAYE_RELATIONSHIP_SCHEMA_VERSION 2

enum DAYE_RelationshipFamily
{
   DAYE_REL_FAMILY_UNKNOWN = 0,
   DAYE_REL_FAMILY_MAJOR = 1,
   DAYE_REL_FAMILY_MINOR_90M = 2
};

enum DAYE_RelationshipSelector
{
   DAYE_REL_SELECTOR_UNKNOWN = 0,
   DAYE_REL_SELECTOR_PREVIOUS_SAME_CODE = 1,
   DAYE_REL_SELECTOR_PREVIOUS_CHRONOLOGICAL = 2
};

enum DAYE_RelationshipDoctrineStatus
{
   DAYE_REL_DOCTRINE_UNKNOWN = 0,
   DAYE_REL_DOCTRINE_READY = 1,
   DAYE_REL_DOCTRINE_BLOCKED = 2
};

enum DAYE_RelationshipResolutionStatus
{
   DAYE_REL_RESOLUTION_UNKNOWN = 0,
   DAYE_REL_RESOLUTION_READY = 1,
   DAYE_REL_RESOLUTION_DISABLED_BY_CONFIG = 2,
   DAYE_REL_RESOLUTION_BLOCKED_BY_DOCTRINE = 3,
   DAYE_REL_RESOLUTION_CURRENT_NOT_ELIGIBLE = 4,
   DAYE_REL_RESOLUTION_REFERENCE_ID_MISSING = 5,
   DAYE_REL_RESOLUTION_REFERENCE_NOT_FOUND = 6,
   DAYE_REL_RESOLUTION_REFERENCE_CODE_MISMATCH = 7,
   DAYE_REL_RESOLUTION_REFERENCE_NOT_COMPLETE = 8,
   DAYE_REL_RESOLUTION_CURRENT_UNAVAILABLE = 9,
   DAYE_REL_RESOLUTION_DUPLICATE_OPPORTUNITY_ID = 10,
   DAYE_REL_RESOLUTION_INVALID_REGISTRY = 11,
   DAYE_REL_RESOLUTION_SOURCE_UNAVAILABLE = 12,
   DAYE_REL_RESOLUTION_IO_ERROR = 13
};

enum DAYE_RelationshipEventType
{
   DAYE_REL_EVENT_NONE = 0,
   DAYE_REL_EVENT_ENGINE_INITIALIZED = 1,
   DAYE_REL_EVENT_STATUS_CHANGED = 2,
   DAYE_REL_EVENT_STORE_READY = 3,
   DAYE_REL_EVENT_STORE_DEGRADED = 4,
   DAYE_REL_EVENT_SOURCE_UNAVAILABLE = 5,
   DAYE_REL_EVENT_LATEST_READY_OPPORTUNITY_ADVANCED = 6
};

struct DAYE_RelationshipConfig
{
   int schema_version;
   DAYE_PeriodAggregationConfig period_config;
   bool enable_major_relationships;
   bool enable_minor_relationships;
   bool allow_open_current_periods;
   bool allow_partial_current_periods;
   bool require_complete_reference_periods;
   bool publish_unavailable_resolutions;
   bool publish_blocked_registry_records;
   int minimum_ready_resolutions;
   int maximum_resolutions_to_publish;
};

struct DAYE_RelationshipDefinition
{
   int schema_version;
   string relationship_id;
   string source_alias;
   DAYE_RelationshipFamily family;
   DAYE_RelationshipSelector selector;
   DAYE_PeriodId current_period_id;
   string current_period_code;
   DAYE_PeriodId reference_period_id;
   string reference_period_code;
   bool is_major;
   string chart_label;
   bool enabled_by_default;
   bool implementation_ready;
   DAYE_RelationshipDoctrineStatus doctrine_status;
   string blocker_decision_id;
   string source_authority;
   string notes;
};

struct DAYE_RelationshipResolution
{
   int schema_version;
   DAYE_RelationshipResolutionStatus status;
   string reason_code;
   bool is_publishable;
   bool is_replay_safe;

   string opportunity_id;
   string relationship_id;
   string source_alias;
   DAYE_RelationshipFamily family;
   DAYE_RelationshipSelector selector;
   bool is_major;
   string chart_label;

   string current_paired_period_id;
   string current_period_instance_id;
   string current_period_code;
   string current_trading_day_key;

   string reference_paired_period_id;
   string reference_period_instance_id;
   string reference_period_code;
   string reference_trading_day_key;

   datetime event_time_utc;
   datetime availability_time_utc;
   datetime processing_time_utc;

   DAYE_PairedPeriodSnapshot current_period;
   DAYE_PairedPeriodSnapshot reference_period;
};

struct DAYE_RelationshipStoreSummary
{
   int schema_version;
   DAYE_RelationshipResolutionStatus status;
   string reason_code;
   bool is_ready;
   bool is_complete;
   bool is_replay_safe;
   string run_key;

   datetime event_time_utc;
   datetime availability_time_utc;
   datetime processing_time_utc;

   int registry_count;
   int major_registry_count;
   int minor_registry_count;
   int ready_registry_count;
   int blocked_registry_count;
   int enabled_registry_count;

   int source_period_count;
   int resolved_count;
   int ready_resolution_count;
   int unavailable_resolution_count;
   int blocked_resolution_count;
   int open_current_resolution_count;
   int complete_current_resolution_count;

   string latest_opportunity_id;
   string latest_ready_opportunity_id;
   string latest_relationship_id;
   string latest_current_period_instance_id;
};

struct DAYE_RelationshipEvent
{
   int schema_version;
   DAYE_RelationshipEventType event_type;
   string event_id;
   datetime event_time_utc;
   datetime availability_time_utc;
   datetime processing_time_utc;
   DAYE_RelationshipResolutionStatus from_status;
   DAYE_RelationshipResolutionStatus to_status;
   string opportunity_id;
   string relationship_id;
   string reason_code;
};

string DAYE_RelationshipFamilyToString(const DAYE_RelationshipFamily value)
{
   switch(value)
   {
      case DAYE_REL_FAMILY_MAJOR: return "MAJOR";
      case DAYE_REL_FAMILY_MINOR_90M: return "MINOR_90M";
      default: return "UNKNOWN";
   }
}

string DAYE_RelationshipSelectorToString(const DAYE_RelationshipSelector value)
{
   switch(value)
   {
      case DAYE_REL_SELECTOR_PREVIOUS_SAME_CODE: return "PREVIOUS_SAME_CODE";
      case DAYE_REL_SELECTOR_PREVIOUS_CHRONOLOGICAL: return "PREVIOUS_CHRONOLOGICAL";
      default: return "UNKNOWN";
   }
}

string DAYE_RelationshipDoctrineStatusToString(const DAYE_RelationshipDoctrineStatus value)
{
   switch(value)
   {
      case DAYE_REL_DOCTRINE_READY: return "READY";
      case DAYE_REL_DOCTRINE_BLOCKED: return "BLOCKED";
      default: return "UNKNOWN";
   }
}

string DAYE_RelationshipResolutionStatusToString(const DAYE_RelationshipResolutionStatus value)
{
   switch(value)
   {
      case DAYE_REL_RESOLUTION_READY: return "READY";
      case DAYE_REL_RESOLUTION_DISABLED_BY_CONFIG: return "DISABLED_BY_CONFIG";
      case DAYE_REL_RESOLUTION_BLOCKED_BY_DOCTRINE: return "BLOCKED_BY_DOCTRINE";
      case DAYE_REL_RESOLUTION_CURRENT_NOT_ELIGIBLE: return "CURRENT_NOT_ELIGIBLE";
      case DAYE_REL_RESOLUTION_REFERENCE_ID_MISSING: return "REFERENCE_ID_MISSING";
      case DAYE_REL_RESOLUTION_REFERENCE_NOT_FOUND: return "REFERENCE_NOT_FOUND";
      case DAYE_REL_RESOLUTION_REFERENCE_CODE_MISMATCH: return "REFERENCE_CODE_MISMATCH";
      case DAYE_REL_RESOLUTION_REFERENCE_NOT_COMPLETE: return "REFERENCE_NOT_COMPLETE";
      case DAYE_REL_RESOLUTION_CURRENT_UNAVAILABLE: return "CURRENT_UNAVAILABLE";
      case DAYE_REL_RESOLUTION_DUPLICATE_OPPORTUNITY_ID: return "DUPLICATE_OPPORTUNITY_ID";
      case DAYE_REL_RESOLUTION_INVALID_REGISTRY: return "INVALID_REGISTRY";
      case DAYE_REL_RESOLUTION_SOURCE_UNAVAILABLE: return "SOURCE_UNAVAILABLE";
      case DAYE_REL_RESOLUTION_IO_ERROR: return "IO_ERROR";
      default: return "UNKNOWN";
   }
}

string DAYE_RelationshipEventTypeToString(const DAYE_RelationshipEventType value)
{
   switch(value)
   {
      case DAYE_REL_EVENT_ENGINE_INITIALIZED: return "ENGINE_INITIALIZED";
      case DAYE_REL_EVENT_STATUS_CHANGED: return "STATUS_CHANGED";
      case DAYE_REL_EVENT_STORE_READY: return "STORE_READY";
      case DAYE_REL_EVENT_STORE_DEGRADED: return "STORE_DEGRADED";
      case DAYE_REL_EVENT_SOURCE_UNAVAILABLE: return "SOURCE_UNAVAILABLE";
      case DAYE_REL_EVENT_LATEST_READY_OPPORTUNITY_ADVANCED: return "LATEST_READY_OPPORTUNITY_ADVANCED";
      default: return "NONE";
   }
}

#endif
