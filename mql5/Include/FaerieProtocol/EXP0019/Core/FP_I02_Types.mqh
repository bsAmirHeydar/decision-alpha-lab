#ifndef __EXP0019_FP_I02_TYPES_MQH__
#define __EXP0019_FP_I02_TYPES_MQH__

#include "FP_I02_Enums.mqh"
#include "FP_I02_ReasonCodes.mqh"

#define FP_I02_SCHEMA_VERSION "1.0.0"
#define FP_I02_CONTEXT_ID "FP-CONTEXT-001"
#define FP_I02_CONTEXT_VERSION "1.0.0"
#define FP_I02_DECISION_SET_ID "FP-OWNER-DECISIONS-2026-07-13-V2"

struct FP_I02_SymbolPair
  {
   string primary_symbol;
   string secondary_symbol;
   string pair_version;
   string pair_id;
  };

struct FP_I02_WindowKey
  {
   string context_id;
   string pair_id;
   FP_I02_WindowKind kind;
   FP_I02_WindowScope scope;
   string trading_day_id;
   long start_utc_ms;
   long end_utc_ms;
   string timezone;
   int calendar_offset;
   string week_id;
   string data_revision;
   string window_id;
  };

struct FP_I02_ReferenceSideKey
  {
   string window_id;
   string symbol;
   FP_I02_PriceSide side;
   double price;
   string data_revision;
   string reference_side_id;
  };

struct FP_I02_HuntFact
  {
   string context_epoch_id;
   FP_I02_RelationCode relation;
   string reference_side_id;
   string check_window_id;
   string pair_id;
   string symbol;
   FP_I02_SymbolRole role;
   FP_I02_PriceSide side;
   long m1_open_utc_ms;
   double observed_price;
   double reference_price;
   string data_revision;
   string source_fingerprint;
   string reason_code;
   string hunt_id;
  };

struct FP_I02_DivergenceCandidate
  {
   string context_epoch_id;
   FP_I02_RelationCode relation;
   FP_I02_Direction direction;
   string pair_id;
   string hunter_symbol;
   string protected_symbol;
   string reference_window_id;
   string check_window_id;
   FP_I02_PriceSide reference_side;
   string hunter_hunt_id;
   long first_hunt_m1_utc_ms;
   long confirmation_deadline_utc_ms;
   int resolved_confirmation_timeframe_seconds;
   int calendar_offset;
   FP_I02_CandidateState state;
   string data_revision;
   string reason_code;
   string candidate_id;
  };

struct FP_I02_ConfirmedSignal
  {
   string candidate_id;
   string confirmation_event_id;
   FP_I02_RelationCode relation;
   FP_I02_Direction direction;
   string pair_id;
   string hunter_symbol;
   string protected_symbol;
   long first_hunt_m1_utc_ms;
   long confirmed_utc_ms;
   FP_I02_EligibilityState eligibility;
   string reason_code;
   string active_ww_id;
   string quota_key_id;
   string semantic_config_hash;
   string signal_id;
  };

struct FP_I02_QuotaKey
  {
   string context_epoch_id;
   string trading_day_id;
   string pair_id;
   FP_I02_WindowKind session;
   string quota_key_id;
  };

struct FP_I02_HealthStatus
  {
   FP_I02_HealthState state;
   string primary_reason_code;
   string reason_codes;
   long checked_utc_ms;
   string semantic_config_hash;
   string dependency_snapshot_hash;
   string health_id;
  };

struct FP_I02_ContextManifest
  {
   string schema_version;
   string context_id;
   string context_version;
   string decision_set_id;
   FP_I02_ContextProfile profile;
   FP_I02_SymbolPair pair;
   string semantic_config_hash;
   string projection_config_hash;
   string dependency_snapshot_hash;
   string relation_registry_hash;
   string reason_registry_hash;
   FP_I02_ExecutionAuthority execution_authority;
   string open_decision_ids;
   int resolved_confirmation_timeframe_seconds;
   long created_utc_ms;
   string context_epoch_id;
  };

struct FP_I02_SelfTestResult
  {
   int check_count;
   int pass_count;
   int fail_count;
   string latest_failed_check;
   string evidence_key;
  };

#endif
