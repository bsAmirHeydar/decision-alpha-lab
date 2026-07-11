#ifndef __ALPHA_LAB_SF2_CONTRACTS_MQH__
#define __ALPHA_LAB_SF2_CONTRACTS_MQH__

enum SF2_Direction
  {
   SF2_DIR_NEUTRAL=0,
   SF2_DIR_LONG=1,
   SF2_DIR_SHORT=-1
  };

enum SF2_DecisionAction
  {
   SF2_DECISION_SKIP=0,
   SF2_DECISION_TRADE=1,
   SF2_DECISION_ABSTAIN=2,
   SF2_DECISION_ERROR=3
  };

struct SF2_AnatomyEvent
  {
   string             event_id;
   string             strategy_id;
   string             strategy_version;
   string             symbol;
   string             reference_symbol;
   SF2_Direction      direction;
   datetime           event_time_utc;
   datetime           known_time_utc;
   datetime           confirmation_time_utc;
   double             reference_price;
   double             invalidation_price;
   string             timeframe_id;
   string             session_id;
   string             cluster_id;
   string             source_hash;
  };

struct SF2_FeatureValue
  {
   string             name;
   double             numeric_value;
   datetime           known_time_utc;
   string             source_id;
   string             version;
   bool               available;
  };

struct SF2_TradeCandidate
  {
   string             candidate_id;
   string             event_id;
   string             symbol;
   SF2_Direction      direction;
   string             template_id;
   string             entry_policy_id;
   string             stop_policy_id;
   string             exit_policy_id;
   ENUM_ORDER_TYPE    order_type;
   double             entry_price;
   double             stop_price;
   double             target_price;
   double             risk_distance;
   datetime           eligible_from_utc;
   datetime           expires_at_utc;
   int                max_holding_seconds;
   bool               eligible;
  };

struct SF2_CandidateScore
  {
   string             candidate_id;
   double             probability_positive;
   double             expected_net_r;
   double             expected_mfe_r;
   double             expected_mae_r;
   double             uncertainty;
   double             utility;
  };

struct SF2_DecisionEnvelope
  {
   string             decision_id;
   string             event_id;
   string             selected_candidate_id;
   SF2_DecisionAction action;
   string             reason_code;
   double             probability_positive;
   double             expected_net_r;
   double             utility;
   datetime           decision_time_utc;
   long               total_latency_microseconds;
   string             plan_hash;
   string             model_hash;
  };

#endif
