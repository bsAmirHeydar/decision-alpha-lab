#ifndef __UCE03_SCHEMA_MQH__
#define __UCE03_SCHEMA_MQH__
#include "UCE03_Identity.mqh"
struct UCE03_SemanticVersion{int major;int minor;int patch;};
struct UCE03_SchemaId{string schema_namespace;string name;UCE03_SemanticVersion version;};
struct UCE03_SchemaDescriptor
{
   UCE03_SchemaId schema_id;
   string semantic_owner;
   string semantic_hash_sha256;
   string required_fields_csv;
   string optional_fields_csv;
};
UCE03_SemanticVersion UCE03_MakeVersion(const int major,const int minor,const int patch){UCE03_SemanticVersion value;value.major=major;value.minor=minor;value.patch=patch;return value;}
UCE03_SchemaId UCE03_MakeSchemaId(const string ns,const string name,const int major,const int minor,const int patch){UCE03_SchemaId value;value.schema_namespace=ns;value.name=name;value.version=UCE03_MakeVersion(major,minor,patch);return value;}
string UCE03_SchemaFamily(const UCE03_SchemaId &value){return value.schema_namespace+"/"+value.name;}
string UCE03_SchemaExactKey(const UCE03_SchemaId &value){return UCE03_SchemaFamily(value)+"@"+IntegerToString(value.version.major)+"."+IntegerToString(value.version.minor)+"."+IntegerToString(value.version.patch);}
bool UCE03_ValidateSchemaId(const UCE03_SchemaId &value,string &error)
{
   if(!UCE03_IsSafeIdentifier(value.schema_namespace)){error="invalid schema namespace";return false;}
   if(!UCE03_IsSafeIdentifier(value.name)){error="invalid schema name";return false;}
   if(value.version.major<0||value.version.minor<0||value.version.patch<0){error="negative schema version";return false;}
   error="";return true;
}
int UCE03_CompareVersion(const UCE03_SemanticVersion &left,const UCE03_SemanticVersion &right)
{
   if(left.major<right.major)return -1;if(left.major>right.major)return 1;
   if(left.minor<right.minor)return -1;if(left.minor>right.minor)return 1;
   if(left.patch<right.patch)return -1;if(left.patch>right.patch)return 1;
   return 0;
}
bool UCE03_SchemaExactEqual(const UCE03_SchemaId &left,const UCE03_SchemaId &right){return UCE03_SchemaExactKey(left)==UCE03_SchemaExactKey(right);}
#endif
