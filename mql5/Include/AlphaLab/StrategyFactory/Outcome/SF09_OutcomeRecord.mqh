#ifndef __SF09_OUTCOME_RECORD_MQH__
#define __SF09_OUTCOME_RECORD_MQH__
#include "SF09_CostModel.mqh"
#include "SF09_PathTracker.mqh"

struct SF09_OutcomeRecord
{
   string schema;
   string outcome_id;
   string candidate_id;
   string event_id;
   string strategy_id;
   string symbol;
   ENUM_SF01_DIRECTION direction;
   ENUM_SF09_RUNTIME_STATE terminal_state;
   ENUM_SF09_EXIT_REASON exit_reason;
   ENUM_SF09_DATA_FIDELITY fidelity;
   bool filled;
   bool ambiguous;
   bool partial_exit_used;
   SF01_MarketTimestamp registered_at;
   SF01_MarketTimestamp fill_time;
   double fill_price;
   SF01_MarketTimestamp exit_time;
   double exit_price;
   double remaining_fraction;
   double gross_points;
   double gross_r;
   double net_r;
   double mfe_points;
   double mae_points;
   double mfe_r;
   double mae_r;
   long holding_milliseconds;
   long time_to_fill_milliseconds;
   SF09_CostBreakdown costs;
   string simulation_policy_hash;
   string cost_registry_hash;
   string path_hash;
   string source_hash;
};

string SF09_OutcomeRecordCanonical(const SF09_OutcomeRecord &o)
{
   return o.schema+"|"+o.candidate_id+"|"+o.event_id+"|"+o.strategy_id+"|"+o.symbol+"|"+
          IntegerToString((int)o.direction)+"|"+IntegerToString((int)o.terminal_state)+"|"+
          IntegerToString((int)o.exit_reason)+"|"+IntegerToString((int)o.fidelity)+"|"+
          SF01_CanonicalBool(o.filled)+"|"+SF01_CanonicalBool(o.ambiguous)+"|"+
          SF01_CanonicalBool(o.partial_exit_used)+"|"+IntegerToString(o.registered_at.utc_epoch_milliseconds)+"|"+
          IntegerToString(o.fill_time.utc_epoch_milliseconds)+"|"+SF01_CanonicalDouble(o.fill_price)+"|"+
          IntegerToString(o.exit_time.utc_epoch_milliseconds)+"|"+SF01_CanonicalDouble(o.exit_price)+"|"+
          SF01_CanonicalDouble(o.remaining_fraction)+"|"+SF01_CanonicalDouble(o.gross_points)+"|"+
          SF01_CanonicalDouble(o.gross_r)+"|"+SF01_CanonicalDouble(o.net_r)+"|"+
          SF01_CanonicalDouble(o.mfe_points)+"|"+SF01_CanonicalDouble(o.mae_points)+"|"+
          SF01_CanonicalDouble(o.mfe_r)+"|"+SF01_CanonicalDouble(o.mae_r)+"|"+
          IntegerToString(o.holding_milliseconds)+"|"+IntegerToString(o.time_to_fill_milliseconds)+"|"+
          o.costs.cost_hash+"|"+o.simulation_policy_hash+"|"+o.cost_registry_hash+"|"+o.path_hash+"|"+o.source_hash;
}
string SF09_DeriveOutcomeId(const SF09_OutcomeRecord &o)
{return SF01_StableId("outc",SF09_OutcomeRecordCanonical(o));}

bool SF09_IsTerminalState(const ENUM_SF09_RUNTIME_STATE state)
{return state==SF09_STATE_CLOSED||state==SF09_STATE_EXPIRED||state==SF09_STATE_INVALIDATED||state==SF09_STATE_AMBIGUOUS||state==SF09_STATE_REJECTED;}

bool SF09_ValidateOutcomeRecord(const SF09_OutcomeRecord &o,string &error)
{
   if(o.schema!="alpha_lab.strategy_factory/outcome_record@1.0.0")
   {error="unsupported outcome schema";return false;}
   if(!SF01_IsSafeIdentifier(o.candidate_id,128)||!SF01_IsSafeIdentifier(o.event_id,128)||
      !SF01_IsSafeIdentifier(o.strategy_id,128)||!SF01_IsTerminalSymbol(o.symbol)||
      !SF01_IsSafeIdentifier(o.source_hash,128))
   {error="invalid outcome identity";return false;}
   if(!SF09_IsTerminalState(o.terminal_state)){error="outcome is not terminal";return false;}
   if(o.filled && (o.fill_price<=0.0||o.exit_price<=0.0||o.exit_time.utc_epoch_milliseconds<o.fill_time.utc_epoch_milliseconds))
   {error="invalid filled outcome geometry";return false;}
   if(!MathIsValidNumber(o.gross_r)||!MathIsValidNumber(o.net_r)||!MathIsValidNumber(o.mfe_r)||!MathIsValidNumber(o.mae_r))
   {error="non-finite outcome metric";return false;}
   if(o.mfe_r<0.0||o.mae_r<0.0||o.remaining_fraction<0.0||o.remaining_fraction>1.0)
   {error="invalid outcome bounds";return false;}
   if(MathAbs(o.net_r-(o.gross_r-o.costs.total_cost_r))>0.0000001)
   {error="net R does not reconcile";return false;}
   const string expected=SF09_DeriveOutcomeId(o);
   if(o.outcome_id!=""&&o.outcome_id!=expected){error="outcome id mismatch";return false;}
   error="";return true;
}

#endif
