#ifndef __SF12_FOLD_OBSERVATION_MQH__
#define __SF12_FOLD_OBSERVATION_MQH__
#include "SF12_FoldCompiler.mqh"
struct SF12_FoldObservation
{
   string schema;string observation_id;string trial_id;string parameter_hash;string fold_id;ENUM_SF12_FOLD_ROLE role;
   string event_id;string cluster_id;string outcome_id;long known_time_utc_msc;long resolved_time_utc_msc;
   double net_r;double gross_r;double cost_r;bool ambiguous;string observation_hash;
};
string SF12_FoldObservationCanonical(const SF12_FoldObservation &o)
{
   return o.schema+"|"+o.observation_id+"|"+o.trial_id+"|"+o.parameter_hash+"|"+o.fold_id+"|"+IntegerToString((int)o.role)+"|"+
      o.event_id+"|"+o.cluster_id+"|"+o.outcome_id+"|"+IntegerToString(o.known_time_utc_msc)+"|"+IntegerToString(o.resolved_time_utc_msc)+"|"+
      SF01_CanonicalDouble(o.net_r)+"|"+SF01_CanonicalDouble(o.gross_r)+"|"+SF01_CanonicalDouble(o.cost_r)+"|"+SF01_CanonicalBool(o.ambiguous);
}
string SF12_DeriveFoldObservationHash(const SF12_FoldObservation &o){return SF01_StableId("fobs",SF12_FoldObservationCanonical(o));}
bool SF12_ValidateFoldObservation(const SF12_FoldObservation &o,string &error)
{
   if(o.schema!="alpha_lab.strategy_factory/fold_observation@1.0.0"){error="unsupported fold observation schema";return false;}
   if(!SF01_IsSafeIdentifier(o.observation_id,128)||!SF01_IsSafeIdentifier(o.trial_id,128)||o.parameter_hash==""||
      !SF01_IsSafeIdentifier(o.fold_id,128)||!SF01_IsSafeIdentifier(o.event_id,128)||!SF01_IsSafeIdentifier(o.cluster_id,128)||
      !SF01_IsSafeIdentifier(o.outcome_id,128)){error="invalid fold observation identity";return false;}
   if(o.known_time_utc_msc<0||o.resolved_time_utc_msc<o.known_time_utc_msc||!MathIsValidNumber(o.net_r)||!MathIsValidNumber(o.gross_r)||!MathIsValidNumber(o.cost_r))
   {error="invalid fold observation values";return false;}
   if(o.observation_hash!=""&&o.observation_hash!=SF12_DeriveFoldObservationHash(o)){error="fold observation hash mismatch";return false;}error="";return true;
}
#endif
