#ifndef __UCE03_IDENTITY_MQH__
#define __UCE03_IDENTITY_MQH__
#include "UCE03_ContractVersion.mqh"
#include "UCE03_Enums.mqh"
#include "UCE03_CanonicalCodec.mqh"
#include "UCE03_Hash.mqh"
struct UCE03_IdentityKey
{
   ENUM_UCE03_IDENTITY_KIND kind;
   string semantic_namespace;
   string semantic_version;
   string owner_id;
   string dimensions_json;
};
bool UCE03_IsSafeIdentifier(const string value)
{
   const int size=StringLen(value);if(size<1 || size>128)return false;
   for(int i=0;i<size;i++)
   {
      const uint c=(uint)StringGetCharacter(value,i);
      const bool ok=(c>=65&&c<=90)||(c>=97&&c<=122)||(c>=48&&c<=57)||c=='.'||c=='_'||c==':'||c=='/'||c=='-';
      if(!ok)return false;
   }
   return true;
}
bool UCE03_ValidateIdentityKey(const UCE03_IdentityKey &value,string &error)
{
   if(!UCE03_IsSafeIdentifier(value.semantic_namespace)){error="invalid semantic_namespace";return false;}
   if(!UCE03_IsSafeIdentifier(value.semantic_version)){error="invalid semantic_version";return false;}
   if(!UCE03_IsSafeIdentifier(value.owner_id)){error="invalid owner_id";return false;}
   if(value.dimensions_json=="" || StringSubstr(value.dimensions_json,0,1)!="{"){error="dimensions_json must be a canonical object";return false;}
   error="";return true;
}
string UCE03_IdentityCanonicalMaterial(const UCE03_IdentityKey &value)
{
   CUCE03CanonicalObject object;
   object.AddString("contract_release",UCE03_CONTRACT_RELEASE);
   object.AddJson("dimensions",value.dimensions_json);
   object.AddString("kind",UCE03_IdentityKindName(value.kind));
   object.AddString("owner_id",value.owner_id);
   object.AddString("semantic_namespace",value.semantic_namespace);
   object.AddString("semantic_version",value.semantic_version);
   return object.Serialize();
}
string UCE03_StableIdentity(const UCE03_IdentityKey &value)
{
   return UCE03_ID_PREFIX+"_"+UCE03_IdentityKindName(value.kind)+"_"+UCE03_Fnv1a64HexUtf8(UCE03_IdentityCanonicalMaterial(value));
}
#endif
