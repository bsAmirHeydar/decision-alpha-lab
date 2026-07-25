#ifndef __ALPHA_LAB_STRATEGY_FACTORY_CONTRACTS_MQH__
#define __ALPHA_LAB_STRATEGY_FACTORY_CONTRACTS_MQH__

// Domain-neutral contracts shared by all anatomy adapters.
// No order-placement authority exists in this file.

enum ENUM_SF_DIRECTION
  {
   SF_DIRECTION_NEUTRAL = 0,
   SF_DIRECTION_LONG    = 1,
   SF_DIRECTION_SHORT   = -1
  };

enum ENUM_SF_DECISION_ACTION
  {
   SF_DECISION_SKIP   = 0,
   SF_DECISION_TRADE  = 1,
   SF_DECISION_REVIEW = 2
  };

struct SF_AnatomyEvent
  {
   string               event_id;
   string               strategy_id;
   string               strategy_version;
   string               symbol;
   string               reference_symbol;
   ENUM_SF_DIRECTION    direction;
   datetime             event_time_utc;
   datetime             known_time_utc;
   datetime             confirmation_time_utc;
   double               reference_price;
   double               invalidation_price;
   bool                 has_invalidation_price;
   string               timeframe;
   string               session;
   string               parent_event_id;
   string               market_event_cluster_id;
   string               anatomy_state;
   string               source_hash;
  };

struct SF_FeatureValue
  {
   string               name;
   double               numeric_value;
   string               text_value;
   bool                 is_numeric;
   bool                 is_missing;
   datetime             known_time_utc;
   string               source;
   string               version;
  };

struct SF_TradeCandidate
  {
   string               candidate_id;
   string               event_id;
   string               symbol;
   ENUM_SF_DIRECTION    direction;
   string               entry_policy_id;
   string               stop_policy_id;
   string               exit_policy_id;
   datetime             created_time_utc;
   datetime             eligible_from_utc;
   datetime             expires_at_utc;
   ENUM_ORDER_TYPE      entry_type;
   double               entry_price;
   double               stop_price;
   double               target_price;
   bool                 has_target_price;
   double               risk_distance;
   long                 max_holding_seconds;
   string               cost_model_id;
  };

struct SF_ModelDecision
  {
   string                  decision_id;
   string                  event_id;
   string                  candidate_id;
   string                  model_id;
   string                  model_version;
   datetime                decision_time_utc;
   ENUM_SF_DECISION_ACTION action;
   double                  predicted_probability;
   double                  expected_net_r;
   double                  expected_mfe_r;
   double                  expected_mae_r;
   string                  confidence_tier;
   string                  feature_schema_version;
   string                  model_artifact_hash;
  };

struct SF_ExecutionIntent
  {
   string               intent_id;
   string               event_id;
   string               candidate_id;
   string               strategy_id;
   string               strategy_version;
   string               model_decision_id;
   string               symbol;
   ENUM_SF_DIRECTION    direction;
   datetime             created_time_utc;
   ENUM_ORDER_TYPE      entry_type;
   double               entry_price;
   double               stop_price;
   double               target_price;
   bool                 has_target_price;
   double               volume;
   double               risk_dollars;
   datetime             expires_at_utc;
  };

bool SF_ValidateAnatomyEvent(const SF_AnatomyEvent &event,string &reason)
  {
   reason="";
   if(event.event_id=="" || event.strategy_id=="" || event.strategy_version=="")
     { reason="missing_event_identity"; return(false); }
   if(event.symbol=="")
     { reason="missing_symbol"; return(false); }
   if(event.known_time_utc<event.event_time_utc)
     { reason="known_time_before_event_time"; return(false); }
   if(event.confirmation_time_utc<event.known_time_utc)
     { reason="confirmation_before_known_time"; return(false); }
   if(!MathIsValidNumber(event.reference_price))
     { reason="invalid_reference_price"; return(false); }
   if(event.has_invalidation_price && !MathIsValidNumber(event.invalidation_price))
     { reason="invalid_invalidation_price"; return(false); }
   return(true);
  }

bool SF_ValidateCandidate(const SF_TradeCandidate &candidate,string &reason)
  {
   reason="";
   if(candidate.candidate_id=="" || candidate.event_id=="" || candidate.symbol=="")
     { reason="missing_candidate_identity"; return(false); }
   if(candidate.expires_at_utc<=candidate.eligible_from_utc)
     { reason="invalid_candidate_expiry"; return(false); }
   if(candidate.risk_distance<=0.0 || !MathIsValidNumber(candidate.risk_distance))
     { reason="invalid_risk_distance"; return(false); }
   if(MathAbs(MathAbs(candidate.entry_price-candidate.stop_price)-candidate.risk_distance)>1e-8)
     { reason="risk_distance_mismatch"; return(false); }
   if(candidate.direction==SF_DIRECTION_LONG && candidate.stop_price>=candidate.entry_price)
     { reason="long_stop_not_below_entry"; return(false); }
   if(candidate.direction==SF_DIRECTION_SHORT && candidate.stop_price<=candidate.entry_price)
     { reason="short_stop_not_above_entry"; return(false); }
   return(true);
  }

#endif
