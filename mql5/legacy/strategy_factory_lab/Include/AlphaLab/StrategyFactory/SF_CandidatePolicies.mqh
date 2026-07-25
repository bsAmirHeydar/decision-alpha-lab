#ifndef __ALPHA_LAB_STRATEGY_FACTORY_CANDIDATE_POLICIES_MQH__
#define __ALPHA_LAB_STRATEGY_FACTORY_CANDIDATE_POLICIES_MQH__

#include "SF_Contracts.mqh"

struct SF_CandidatePolicyConfig
  {
   string entry_policy_id;
   string stop_policy_id;
   string exit_policy_id;
   double retracement_fraction;
   double entry_offset;
   double atr_buffer;
   double reward_r;
   long   expiration_seconds;
   long   max_holding_seconds;
   string cost_model_id;
  };

bool SF_BuildFixedRCandidate(const SF_AnatomyEvent &event,
                             const SF_CandidatePolicyConfig &config,
                             const double entry_price,
                             const double stop_price,
                             SF_TradeCandidate &candidate,
                             string &reason)
  {
   reason="";
   if(event.direction==SF_DIRECTION_NEUTRAL)
     { reason="neutral_event"; return(false); }
   const double risk=MathAbs(entry_price-stop_price);
   if(risk<=0.0)
     { reason="non_positive_risk"; return(false); }
   const double sign=(event.direction==SF_DIRECTION_LONG ? 1.0 : -1.0);
   candidate.event_id=event.event_id;
   candidate.symbol=event.symbol;
   candidate.direction=event.direction;
   candidate.entry_policy_id=config.entry_policy_id;
   candidate.stop_policy_id=config.stop_policy_id;
   candidate.exit_policy_id=config.exit_policy_id;
   candidate.created_time_utc=event.confirmation_time_utc;
   candidate.eligible_from_utc=event.confirmation_time_utc;
   candidate.expires_at_utc=event.confirmation_time_utc+config.expiration_seconds;
   candidate.entry_type=ORDER_TYPE_BUY;
   if(event.direction==SF_DIRECTION_SHORT)
      candidate.entry_type=ORDER_TYPE_SELL;
   candidate.entry_price=entry_price;
   candidate.stop_price=stop_price;
   candidate.target_price=entry_price+sign*risk*config.reward_r;
   candidate.has_target_price=true;
   candidate.risk_distance=risk;
   candidate.max_holding_seconds=config.max_holding_seconds;
   candidate.cost_model_id=config.cost_model_id;
   candidate.candidate_id=event.event_id+"|"+config.entry_policy_id+"|"+
                          config.stop_policy_id+"|"+config.exit_policy_id;
   return(SF_ValidateCandidate(candidate,reason));
  }

#endif
