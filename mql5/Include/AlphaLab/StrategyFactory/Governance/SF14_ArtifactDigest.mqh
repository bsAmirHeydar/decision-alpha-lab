#ifndef __SF14_ARTIFACT_DIGEST_MQH__
#define __SF14_ARTIFACT_DIGEST_MQH__
#include "SF14_GovernanceEnums.mqh"
#include "../Contracts/SF01_AllContracts.mqh"
struct SF14_ArtifactDigest{string logical_name;string relative_path;ENUM_SF14_ARTIFACT_ROLE role;string media_type;long byte_size;string sha256;string schema_id;bool required;string digest_id;};
string SF14_ArtifactDigestCanonical(const SF14_ArtifactDigest &v){return "alpha_lab.strategy_factory/artifact_digest@1.0.0|"+v.logical_name+"|"+v.relative_path+"|"+IntegerToString((int)v.role)+"|"+v.media_type+"|"+IntegerToString(v.byte_size)+"|"+v.sha256+"|"+v.schema_id+"|"+SF01_CanonicalBool(v.required);}
string SF14_DeriveArtifactDigestId(const SF14_ArtifactDigest &v){return SF01_StableId("adig",SF14_ArtifactDigestCanonical(v));}
bool SF14_IsLowerHex64(const string value){if(StringLen(value)!=64)return false;for(int i=0;i<64;i++){int c=(int)StringGetCharacter(value,i);bool digit=(c>=48&&c<=57);bool hex=(c>=97&&c<=102);if(!digit&&!hex)return false;}return true;}
bool SF14_ValidateArtifactDigest(const SF14_ArtifactDigest &v,string &error){if(v.logical_name==""||v.relative_path==""||v.media_type==""||v.byte_size<0||!SF14_IsLowerHex64(v.sha256)){error="invalid artifact digest";return false;}if(StringFind(v.relative_path,"..")>=0||StringSubstr(v.relative_path,0,1)=="/"||StringSubstr(v.relative_path,0,1)=="\\"){error="unsafe artifact path";return false;}if(v.digest_id!=""&&v.digest_id!=SF14_DeriveArtifactDigestId(v)){error="artifact digest id mismatch";return false;}error="";return true;}
#endif
