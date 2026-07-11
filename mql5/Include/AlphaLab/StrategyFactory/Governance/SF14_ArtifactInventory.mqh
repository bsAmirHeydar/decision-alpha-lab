#ifndef __SF14_ARTIFACT_INVENTORY_MQH__
#define __SF14_ARTIFACT_INVENTORY_MQH__
#include "SF14_ArtifactDigest.mqh"
struct SF14_ArtifactInventory{string inventory_id;string inventory_version;int digest_count;SF14_ArtifactDigest digests[SF14_MAX_ARTIFACTS];long generated_at_utc_msc;string inventory_hash;};
bool SF14_ValidateArtifactInventory(const SF14_ArtifactInventory &v,string &error){if(v.inventory_id==""||v.inventory_version==""||v.digest_count<1||v.digest_count>SF14_MAX_ARTIFACTS||v.generated_at_utc_msc<0||!SF14_IsLowerHex64(v.inventory_hash)){error="invalid artifact inventory header";return false;}for(int i=0;i<v.digest_count;i++){if(!SF14_ValidateArtifactDigest(v.digests[i],error))return false;for(int j=0;j<i;j++)if(v.digests[i].logical_name==v.digests[j].logical_name||v.digests[i].relative_path==v.digests[j].relative_path){error="duplicate artifact inventory identity";return false;}}error="";return true;}
#endif
