#ifndef __EXP0019_FP_I01_TYPES_MQH__
#define __EXP0019_FP_I01_TYPES_MQH__

#include "FP_I01_Enums.mqh"

#define FP_I01_SCHEMA_VERSION 1
#define FP_I01_ADAPTER_VERSION "1.0.0"

struct FP_I01_TimeSnapshot
  {
   int source_context;
   string source_type;
   string source_fingerprint;
   datetime broker_time;
   datetime utc_time;
   datetime new_york_time;
   datetime trading_day_start_ny;
   datetime trading_day_end_ny;
   bool inside_trading_day;
   int ny_utc_offset_hours;
   string trading_day_key;
   FP_I01_HealthState health;
   string reason_code;
  };

struct FP_I01_ReferencePair
  {
   int source_context;
   string source_type;
   string source_fingerprint;
   string reference_id;
   string window_code;
   datetime window_start;
   datetime window_end;
   bool complete;
   bool ready;
   string symbol_a;
   string symbol_b;
   double high_a;
   double low_a;
   double high_b;
   double low_b;
   datetime high_time_a;
   datetime low_time_a;
   datetime high_time_b;
   datetime low_time_b;
   bool data_ready_a;
   bool data_ready_b;
   FP_I01_HealthState health;
   string reason_code;
  };

struct FP_I01_HuntObservation
  {
   int source_context;
   string source_type;
   string source_fingerprint;
   string observation_id;
   string reference_id;
   string opportunity_id;
   FP_I01_HuntSide side;
   FP_I01_PairState pair_state;
   string hunter_symbol;
   string protected_symbol;
   double reference_price_a;
   double reference_price_b;
   double current_extreme_a;
   double current_extreme_b;
   datetime event_time_utc;
   datetime availability_time_utc;
   bool replay_safe;
   FP_I01_HealthState health;
   string reason_code;
  };

struct FP_I01_DivergenceCandidate
  {
   int source_context;
   string source_type;
   string source_fingerprint;
   string candidate_id;
   string reference_id;
   string opportunity_id;
   FP_I01_Direction direction;
   FP_I01_HuntSide side;
   string hunter_symbol;
   string protected_symbol;
   bool one_sided;
   bool symmetric;
   bool data_ready;
   double hunter_reference_price;
   double protected_reference_price;
   datetime event_time_utc;
   FP_I01_HealthState health;
   string reason_code;
  };

struct FP_I01_ConfirmationResult
  {
   int source_context;
   string source_type;
   string source_fingerprint;
   string result_id;
   string candidate_id;
   string observation_id;
   string opportunity_id;
   FP_I01_ConfirmationOutcome outcome;
   FP_I01_Direction direction;
   FP_I01_HuntSide side;
   string hunter_symbol;
   string protected_symbol;
   int host_timeframe_seconds;
   datetime host_bar_open_utc;
   datetime host_bar_close_utc;
   double confirmation_price;
   bool is_final;
   bool is_immutable;
   bool is_replay_safe;
   FP_I01_HealthState health;
   string reason_code;
  };

struct FP_I01_LifecycleRecord
  {
   int source_context;
   string source_type;
   string source_fingerprint;
   string reference_id;
   FP_I01_HuntSide side;
   string protected_symbol;
   string first_hunter_symbol;
   string state;
   bool retired;
   int accepted_use_count;
   int duplicate_use_count;
   int rejected_use_count;
   datetime activation_time_utc;
   datetime retirement_time_utc;
   bool immutable;
   bool replay_safe;
   FP_I01_HealthState health;
   string reason_code;
  };

struct FP_I01_AdapterDescriptor
  {
   string adapter_id;
   string adapter_version;
   string source_context;
   string source_type;
   string family;
   string dependency_id;
   string reuse_mode;
   bool read_only;
   bool broker_authority;
   bool order_authority;
   bool network_authority;
  };

struct FP_I01_SelfTestResult
  {
   int check_count;
   int pass_count;
   int fail_count;
   string latest_failed_check;
   string evidence_key;
  };

#endif
