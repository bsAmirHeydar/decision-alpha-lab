#ifndef __SF08_POLICY_DESCRIPTOR_MQH__
#define __SF08_POLICY_DESCRIPTOR_MQH__
#include "SF08_CandidateEnums.mqh"
#include "../Contracts/SF01_AllContracts.mqh"

struct SF08_PolicyDescriptor
{
   string policy_id;
   string version;
   ENUM_SF08_POLICY_KIND kind;
   bool deterministic;
   bool fast_path_safe;
   bool replay_safe;
   bool requires_reference_price;
   bool requires_invalidation_price;
   string required_feature_ids_csv;
   string descriptor_hash;
   string description;
};

string SF08_PolicyDescriptorCanonical(const SF08_PolicyDescriptor &d)
{
   return d.policy_id+"|"+d.version+"|"+IntegerToString((int)d.kind)+"|"+
          SF01_CanonicalBool(d.deterministic)+"|"+SF01_CanonicalBool(d.fast_path_safe)+"|"+
          SF01_CanonicalBool(d.replay_safe)+"|"+SF01_CanonicalBool(d.requires_reference_price)+"|"+
          SF01_CanonicalBool(d.requires_invalidation_price)+"|"+d.required_feature_ids_csv+"|"+d.description;
}

string SF08_DerivePolicyDescriptorHash(const SF08_PolicyDescriptor &d)
{
   return SF01_StableId("pdesc",SF08_PolicyDescriptorCanonical(d));
}

bool SF08_ValidatePolicyDescriptor(const SF08_PolicyDescriptor &d,string &error)
{
   if(!SF01_IsSafeIdentifier(d.policy_id,128) || !SF01_IsSafeIdentifier(d.version,64))
   { error="invalid policy identity"; return false; }
   if(d.kind<SF08_POLICY_ENTRY || d.kind>SF08_POLICY_GATE)
   { error="invalid policy kind"; return false; }
   if(!d.deterministic)
   { error="non-deterministic policy is not accepted in phase 08"; return false; }
   if(StringLen(d.required_feature_ids_csv)>1024 || StringLen(d.description)>512)
   { error="policy descriptor text too long"; return false; }
   const string expected=SF08_DerivePolicyDescriptorHash(d);
   if(d.descriptor_hash!="" && d.descriptor_hash!=expected)
   { error="policy descriptor hash mismatch"; return false; }
   error="";
   return true;
}

#endif
