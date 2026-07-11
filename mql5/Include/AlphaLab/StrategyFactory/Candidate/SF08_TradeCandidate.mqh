#ifndef __SF08_TRADE_CANDIDATE_MQH__
#define __SF08_TRADE_CANDIDATE_MQH__
#include "SF08_CandidateTemplate.mqh"
#include "SF08_Plans.mqh"
#include "../Context/SF07_ContextFrame.mqh"

struct SF08_TradeCandidate
{
   string schema;
   string candidate_id;
   string template_id;
   string template_hash;
   string event_id;
   string snapshot_id;
   string context_frame_id;
   string strategy_id;
   string strategy_version;
   string symbol;
   ENUM_SF01_DIRECTION direction;
   long runtime_generation_id;
   SF01_MarketTimestamp created_at;
   SF08_EntryPlan entry;
   SF08_StopPlan stop;
   SF08_ExitPlan exit_plan;
   double planned_r_multiple;
   string source_hash;
   ENUM_SF08_CANDIDATE_STATUS status;
};

string SF08_TradeCandidateCanonical(const SF08_TradeCandidate &c)
{
   return c.schema+"|"+c.template_id+"|"+c.template_hash+"|"+c.event_id+"|"+
          c.snapshot_id+"|"+c.context_frame_id+"|"+c.strategy_id+"|"+c.strategy_version+"|"+
          c.symbol+"|"+IntegerToString((int)c.direction)+"|"+IntegerToString(c.runtime_generation_id)+"|"+
          IntegerToString(c.created_at.utc_epoch_milliseconds)+"|"+SF08_DeriveEntryPlanHash(c.entry)+"|"+
          SF08_DeriveStopPlanHash(c.stop)+"|"+SF08_DeriveExitPlanHash(c.exit_plan)+"|"+
          SF01_CanonicalDouble(c.planned_r_multiple)+"|"+c.source_hash;
}
string SF08_DeriveTradeCandidateId(const SF08_TradeCandidate &c)
{return SF01_StableId("cand",SF08_TradeCandidateCanonical(c));}

bool SF08_ValidateTradeCandidate(const SF08_TradeCandidate &c,string &error)
{
   if(c.schema!="alpha_lab.strategy_factory/trade_candidate@1.0.0")
   { error="unsupported trade candidate schema"; return false; }
   if(!SF01_IsSafeIdentifier(c.template_id,128) || !SF01_IsSafeIdentifier(c.template_hash,128) ||
      !SF01_IsSafeIdentifier(c.event_id,128) || !SF01_IsSafeIdentifier(c.snapshot_id,128) ||
      !SF01_IsSafeIdentifier(c.context_frame_id,128) || !SF01_IsSafeIdentifier(c.strategy_id,128) ||
      !SF01_IsSafeIdentifier(c.strategy_version,64) || !SF01_IsTerminalSymbol(c.symbol) ||
      !SF01_IsSafeIdentifier(c.source_hash,128))
   { error="invalid trade candidate identity"; return false; }
   if(c.direction!=SF01_DIRECTION_LONG && c.direction!=SF01_DIRECTION_SHORT)
   { error="trade candidate direction must be long or short"; return false; }
   if(c.runtime_generation_id<0)
   { error="negative runtime generation"; return false; }
   if(!SF01_ValidateTimestamp(c.created_at,error) || !SF08_ValidateEntryPlan(c.entry,error) ||
      !SF08_ValidateStopPlan(c.stop,error) || !SF08_ValidateExitPlan(c.exit_plan,error)) return false;
   const double entry=c.entry.requested_price;
   if(c.direction==SF01_DIRECTION_LONG)
   {
      if(c.stop.has_price_stop && c.stop.stop_price>=entry)
      { error="long stop must be below entry"; return false; }
      if(c.exit_plan.has_price_target && c.exit_plan.target_price<=entry)
      { error="long target must be above entry"; return false; }
   }
   else
   {
      if(c.stop.has_price_stop && c.stop.stop_price<=entry)
      { error="short stop must be above entry"; return false; }
      if(c.exit_plan.has_price_target && c.exit_plan.target_price>=entry)
      { error="short target must be below entry"; return false; }
   }
   const double derived_r=(c.stop.initial_risk_points>0.0)?c.exit_plan.planned_reward_points/c.stop.initial_risk_points:0.0;
   if(!MathIsValidNumber(c.planned_r_multiple) || c.planned_r_multiple<0.0 || MathAbs(c.planned_r_multiple-derived_r)>0.0000001)
   { error="planned R multiple mismatch"; return false; }
   if(c.status!=SF08_CANDIDATE_VALID)
   { error="trade candidate is not valid"; return false; }
   const string expected=SF08_DeriveTradeCandidateId(c);
   if(c.candidate_id!="" && c.candidate_id!=expected)
   { error="candidate id mismatch"; return false; }
   error=""; return true;
}

#endif
