#ifndef __UCE03_RELEASE_MQH__
#define __UCE03_RELEASE_MQH__
#include "UCE03_KnownTime.mqh"
struct UCE03_ArtifactDigest{string path;string sha256;string media_type;long byte_count;};
struct UCE03_ContractReleaseManifest
{
   string release_id;
   string contract_version;
   UCE03_UtcInstant created_at;
   string semantic_owner;
   string registry_manifest_sha256;
   string artifact_inventory_sha256;
   string compatibility_policy_version;
   string migration_registry_version;
   string prior_release_id;
};
bool UCE03_ValidateReleaseManifest(const UCE03_ContractReleaseManifest &value,string &error)
{
   if(value.release_id==""||value.contract_version!="3.0.0"){error="invalid release identity";return false;}
   if(StringLen(value.registry_manifest_sha256)!=64||StringLen(value.artifact_inventory_sha256)!=64){error="invalid release digest";return false;}
   error="";return true;
}
#endif
