#ifndef __SF08_PLANS_MQH__
#define __SF08_PLANS_MQH__
#include "SF08_CandidateEnums.mqh"
#include "../Contracts/SF01_AllContracts.mqh"

struct SF08_EntryPlan
{
   ENUM_SF08_ORDER_KIND order_kind;
   double requested_price;
   SF01_MarketTimestamp activation_time;
   SF01_MarketTimestamp expiration_time;
   long maximum_fill_delay_milliseconds;
   double maximum_slippage_points;
   string geometry_hash;
};

struct SF08_StopPlan
{
   bool has_price_stop;
   double stop_price;
   bool has_time_invalidation;
   SF01_MarketTimestamp invalidation_time;
   double initial_risk_points;
   string geometry_hash;
};

struct SF08_ExitPlan
{
   ENUM_SF08_EXIT_KIND exit_kind;
   bool has_price_target;
   double target_price;
   long maximum_holding_milliseconds;
   double planned_reward_points;
   double partial_fraction;
   string geometry_hash;
};

string SF08_EntryPlanCanonical(const SF08_EntryPlan &p)
{
   return IntegerToString((int)p.order_kind)+"|"+SF01_CanonicalDouble(p.requested_price)+"|"+
          IntegerToString(p.activation_time.utc_epoch_milliseconds)+"|"+
          IntegerToString(p.expiration_time.utc_epoch_milliseconds)+"|"+
          IntegerToString(p.maximum_fill_delay_milliseconds)+"|"+
          SF01_CanonicalDouble(p.maximum_slippage_points);
}
string SF08_StopPlanCanonical(const SF08_StopPlan &p)
{
   return SF01_CanonicalBool(p.has_price_stop)+"|"+SF01_CanonicalDouble(p.stop_price)+"|"+
          SF01_CanonicalBool(p.has_time_invalidation)+"|"+
          IntegerToString(p.invalidation_time.utc_epoch_milliseconds)+"|"+
          SF01_CanonicalDouble(p.initial_risk_points);
}
string SF08_ExitPlanCanonical(const SF08_ExitPlan &p)
{
   return IntegerToString((int)p.exit_kind)+"|"+SF01_CanonicalBool(p.has_price_target)+"|"+
          SF01_CanonicalDouble(p.target_price)+"|"+IntegerToString(p.maximum_holding_milliseconds)+"|"+
          SF01_CanonicalDouble(p.planned_reward_points)+"|"+SF01_CanonicalDouble(p.partial_fraction);
}

string SF08_DeriveEntryPlanHash(const SF08_EntryPlan &p){return SF01_StableId("epln",SF08_EntryPlanCanonical(p));}
string SF08_DeriveStopPlanHash(const SF08_StopPlan &p){return SF01_StableId("spln",SF08_StopPlanCanonical(p));}
string SF08_DeriveExitPlanHash(const SF08_ExitPlan &p){return SF01_StableId("xpln",SF08_ExitPlanCanonical(p));}

bool SF08_ValidateEntryPlan(const SF08_EntryPlan &p,string &error)
{
   if(p.order_kind<SF08_ORDER_MARKET || p.order_kind>SF08_ORDER_STOP)
   { error="invalid entry order kind"; return false; }
   if(!MathIsValidNumber(p.requested_price) || p.requested_price<=0.0)
   { error="invalid requested entry price"; return false; }
   if(!SF01_ValidateTimestamp(p.activation_time,error) || !SF01_ValidateTimestamp(p.expiration_time,error)) return false;
   if(p.expiration_time.utc_epoch_milliseconds<p.activation_time.utc_epoch_milliseconds)
   { error="entry expiration precedes activation"; return false; }
   if(p.maximum_fill_delay_milliseconds<0 || !MathIsValidNumber(p.maximum_slippage_points) || p.maximum_slippage_points<0.0)
   { error="invalid entry timing or slippage"; return false; }
   const string expected=SF08_DeriveEntryPlanHash(p);
   if(p.geometry_hash!="" && p.geometry_hash!=expected)
   { error="entry geometry hash mismatch"; return false; }
   error=""; return true;
}

bool SF08_ValidateStopPlan(const SF08_StopPlan &p,string &error)
{
   if(!p.has_price_stop && !p.has_time_invalidation)
   { error="stop plan has no invalidation mechanism"; return false; }
   if(p.has_price_stop && (!MathIsValidNumber(p.stop_price) || p.stop_price<=0.0))
   { error="invalid stop price"; return false; }
   if(p.has_time_invalidation && !SF01_ValidateTimestamp(p.invalidation_time,error)) return false;
   if(!MathIsValidNumber(p.initial_risk_points) || p.initial_risk_points<=0.0)
   { error="invalid initial risk points"; return false; }
   const string expected=SF08_DeriveStopPlanHash(p);
   if(p.geometry_hash!="" && p.geometry_hash!=expected)
   { error="stop geometry hash mismatch"; return false; }
   error=""; return true;
}

bool SF08_ValidateExitPlan(const SF08_ExitPlan &p,string &error)
{
   if(p.exit_kind<SF08_EXIT_PRICE_TARGET || p.exit_kind>SF08_EXIT_STRUCTURAL)
   { error="invalid exit kind"; return false; }
   if(p.has_price_target && (!MathIsValidNumber(p.target_price) || p.target_price<=0.0))
   { error="invalid target price"; return false; }
   if(p.maximum_holding_milliseconds<0 || !MathIsValidNumber(p.planned_reward_points) || p.planned_reward_points<0.0)
   { error="invalid exit horizon or reward"; return false; }
   if(!MathIsValidNumber(p.partial_fraction) || p.partial_fraction<0.0 || p.partial_fraction>1.0)
   { error="invalid partial fraction"; return false; }
   if(!p.has_price_target && p.maximum_holding_milliseconds<=0 && p.exit_kind!=SF08_EXIT_STRUCTURAL)
   { error="exit plan has no resolution mechanism"; return false; }
   const string expected=SF08_DeriveExitPlanHash(p);
   if(p.geometry_hash!="" && p.geometry_hash!=expected)
   { error="exit geometry hash mismatch"; return false; }
   error=""; return true;
}

#endif
