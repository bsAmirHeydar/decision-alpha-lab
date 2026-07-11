#ifndef __SF09_SIMULATION_POLICY_MQH__
#define __SF09_SIMULATION_POLICY_MQH__
#include "SF09_OutcomeEnums.mqh"
#include "../Contracts/SF01_AllContracts.mqh"

struct SF09_SimulationPolicy
{
   string policy_id;
   string version;
   ENUM_SF09_AMBIGUITY_POLICY ambiguity_policy;
   ENUM_SF09_GAP_POLICY gap_policy;
   ENUM_SF09_MARKET_FILL_POLICY market_fill_policy;
   ENUM_SF09_DATA_FIDELITY minimum_fidelity;
   bool allow_limit_price_improvement;
   bool allow_stop_gap_slippage;
   bool strict_monotonic_observations;
   bool fail_on_stale_observation;
   long maximum_observation_age_milliseconds;
   int maximum_path_events;
   string policy_hash;
};

string SF09_SimulationPolicyCanonical(const SF09_SimulationPolicy &p)
{
   return p.policy_id+"|"+p.version+"|"+IntegerToString((int)p.ambiguity_policy)+"|"+
          IntegerToString((int)p.gap_policy)+"|"+IntegerToString((int)p.market_fill_policy)+"|"+
          IntegerToString((int)p.minimum_fidelity)+"|"+SF01_CanonicalBool(p.allow_limit_price_improvement)+"|"+
          SF01_CanonicalBool(p.allow_stop_gap_slippage)+"|"+SF01_CanonicalBool(p.strict_monotonic_observations)+"|"+
          SF01_CanonicalBool(p.fail_on_stale_observation)+"|"+IntegerToString(p.maximum_observation_age_milliseconds)+"|"+
          IntegerToString(p.maximum_path_events);
}
string SF09_DeriveSimulationPolicyHash(const SF09_SimulationPolicy &p)
{return SF01_StableId("spol",SF09_SimulationPolicyCanonical(p));}

bool SF09_ValidateSimulationPolicy(const SF09_SimulationPolicy &p,string &error)
{
   if(!SF01_IsSafeIdentifier(p.policy_id,128)||!SF01_IsSafeIdentifier(p.version,64))
   { error="invalid simulation policy identity"; return false; }
   if(p.ambiguity_policy<SF09_AMBIGUITY_STOP_FIRST||p.ambiguity_policy>SF09_AMBIGUITY_REQUIRE_LOWER_FIDELITY ||
      p.gap_policy<SF09_GAP_AT_TRIGGER||p.gap_policy>SF09_GAP_REJECT ||
      p.market_fill_policy<SF09_MARKET_FILL_AT_FIRST_OBSERVATION||p.market_fill_policy>SF09_MARKET_FILL_CONSERVATIVE_SIDE)
   { error="invalid simulation policy enum"; return false; }
   if(p.maximum_observation_age_milliseconds<0 || p.maximum_path_events<=0 || p.maximum_path_events>SF09_MAX_PATH_EVENTS)
   { error="invalid simulation policy bounds"; return false; }
   const string expected=SF09_DeriveSimulationPolicyHash(p);
   if(p.policy_hash!="" && p.policy_hash!=expected)
   { error="simulation policy hash mismatch"; return false; }
   error=""; return true;
}

SF09_SimulationPolicy SF09_ConservativeSimulationPolicy()
{
   SF09_SimulationPolicy p;
   p.policy_id="sf09.conservative"; p.version="1.0.0";
   p.ambiguity_policy=SF09_AMBIGUITY_STOP_FIRST;
   p.gap_policy=SF09_GAP_AT_OBSERVED_OPEN_CONSERVATIVE;
   p.market_fill_policy=SF09_MARKET_FILL_CONSERVATIVE_SIDE;
   p.minimum_fidelity=SF09_FIDELITY_BAR_APPROXIMATION;
   p.allow_limit_price_improvement=false;
   p.allow_stop_gap_slippage=true;
   p.strict_monotonic_observations=true;
   p.fail_on_stale_observation=true;
   p.maximum_observation_age_milliseconds=300000;
   p.maximum_path_events=64;
   p.policy_hash=SF09_DeriveSimulationPolicyHash(p);
   return p;
}

#endif
