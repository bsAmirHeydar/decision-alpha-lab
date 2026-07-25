#ifndef __ALPHA_LAB_STRATEGY_FACTORY_RISK_GATE_MQH__
#define __ALPHA_LAB_STRATEGY_FACTORY_RISK_GATE_MQH__

#include "SF_Contracts.mqh"

struct SF_RiskPolicy
  {
   string policy_id;
   double max_risk_dollars_per_intent;
   double max_daily_risk_dollars;
   double max_daily_loss_dollars;
   double max_open_risk_dollars;
   int    max_concurrent_positions;
  };

struct SF_RiskState
  {
   double reserved_daily_risk;
   double realized_daily_pnl;
   double open_risk;
   int    concurrent_positions;
   bool   kill_switch;
  };

bool SF_EvaluateRiskIntent(const SF_ExecutionIntent &intent,
                           const SF_RiskPolicy &policy,
                           const SF_RiskState &state,
                           string &reason)
  {
   reason="";
   if(state.kill_switch)
     { reason="kill_switch_active"; return(false); }
   if(intent.risk_dollars<=0.0 || intent.risk_dollars>policy.max_risk_dollars_per_intent)
     { reason="intent_risk_limit"; return(false); }
   if(state.reserved_daily_risk+intent.risk_dollars>policy.max_daily_risk_dollars)
     { reason="daily_risk_limit"; return(false); }
   if(state.realized_daily_pnl<=-MathAbs(policy.max_daily_loss_dollars))
     { reason="daily_loss_lock"; return(false); }
   if(state.open_risk+intent.risk_dollars>policy.max_open_risk_dollars)
     { reason="open_risk_limit"; return(false); }
   if(state.concurrent_positions>=policy.max_concurrent_positions)
     { reason="concurrent_position_limit"; return(false); }
   return(true);
  }

#endif
