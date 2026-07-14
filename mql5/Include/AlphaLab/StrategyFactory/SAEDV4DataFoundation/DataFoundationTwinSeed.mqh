#ifndef __AL_SAED_V4_DATA_FOUNDATION_TWIN_SEED_MQH__
#define __AL_SAED_V4_DATA_FOUNDATION_TWIN_SEED_MQH__
#include "DataFoundationContracts.mqh"
#include "DataFoundationIntegrity.mqh"
class ALTwinSeedGate {
public:
 static bool Validate(const ALTwinSeedIdentity &value,string &reason){
   if(value.package_id=="" || value.context_specification_artifact_id==""){reason="twin_seed_identity_missing";return false;}
   if(!ALDataIntegrityGate::HashLooksValid(value.package_hash) || !ALDataIntegrityGate::HashLooksValid(value.lineage_root) || !ALDataIntegrityGate::HashLooksValid(value.constitution_hash)){reason="twin_seed_hash_invalid";return false;}
   if(value.known_as_of<=0 || value.snapshot_count<1){reason="twin_seed_inputs_missing";return false;}
   reason="pass";return true;
 }
};
#endif
