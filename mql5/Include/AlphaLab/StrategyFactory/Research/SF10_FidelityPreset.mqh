#ifndef __SF10_FIDELITY_PRESET_MQH__
#define __SF10_FIDELITY_PRESET_MQH__
#include "SF10_RunManifest.mqh"

struct SF10_FidelityPreset
{
   string schema;
   string preset_id;
   string preset_version;
   ENUM_SF10_FIDELITY_PRESET preset;
   ENUM_SF09_DATA_FIDELITY minimum_observation_fidelity;
   bool require_spread;
   bool require_bid_ask;
   bool reject_ambiguous_bars;
   bool require_differential_validation;
   int maximum_selected_passes;
   string preset_hash;
};

string SF10_FidelityPresetCanonical(const SF10_FidelityPreset &p)
{
   return p.schema+"|"+p.preset_id+"|"+p.preset_version+"|"+IntegerToString((int)p.preset)+"|"+
          IntegerToString((int)p.minimum_observation_fidelity)+"|"+SF01_CanonicalBool(p.require_spread)+"|"+
          SF01_CanonicalBool(p.require_bid_ask)+"|"+SF01_CanonicalBool(p.reject_ambiguous_bars)+"|"+
          SF01_CanonicalBool(p.require_differential_validation)+"|"+IntegerToString(p.maximum_selected_passes);
}
string SF10_DeriveFidelityPresetHash(const SF10_FidelityPreset &p)
{return SF01_StableId("fpst",SF10_FidelityPresetCanonical(p));}

bool SF10_ValidateFidelityPreset(const SF10_FidelityPreset &p,string &error)
{
   if(p.schema!="alpha_lab.strategy_factory/fidelity_preset@1.0.0")
   {error="unsupported fidelity preset schema";return false;}
   if(!SF01_IsSafeIdentifier(p.preset_id,128)||!SF01_IsSafeIdentifier(p.preset_version,64)||
      p.maximum_selected_passes<0)
   {error="invalid fidelity preset";return false;}
   const string expected=SF10_DeriveFidelityPresetHash(p);
   if(p.preset_hash!=""&&p.preset_hash!=expected){error="fidelity preset hash mismatch";return false;}
   error="";return true;
}
#endif
