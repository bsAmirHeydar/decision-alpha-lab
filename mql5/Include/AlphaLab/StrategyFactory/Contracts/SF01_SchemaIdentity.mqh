#ifndef __SF01_SCHEMA_IDENTITY_MQH__
#define __SF01_SCHEMA_IDENTITY_MQH__

#include "SF01_Enums.mqh"
#include "SF01_StringCodec.mqh"


struct SF01_SchemaIdentity
{
   string schema_namespace;
   string schema_name;
   int major;
   int minor;
   int patch;
};

SF01_SchemaIdentity SF01_MakeSchemaIdentity(const string schema_namespace,
                                             const string schema_name,
                                             const int major,
                                             const int minor,
                                             const int patch)
{
   SF01_SchemaIdentity value;
   value.schema_namespace = schema_namespace;
   value.schema_name = schema_name;
   value.major = major;
   value.minor = minor;
   value.patch = patch;
   return value;
}

string SF01_SchemaKey(const SF01_SchemaIdentity &value)
{
   return value.schema_namespace + "/" + value.schema_name;
}

string SF01_SchemaVersion(const SF01_SchemaIdentity &value)
{
   return IntegerToString(value.major) + "." + IntegerToString(value.minor) + "." + IntegerToString(value.patch);
}

string SF01_SchemaCanonical(const SF01_SchemaIdentity &value)
{
   return SF01_SchemaKey(value) + "@" + SF01_SchemaVersion(value);
}

bool SF01_ValidateSchemaIdentity(const SF01_SchemaIdentity &value, string &error)
{
   if(!SF01_IsSafeIdentifier(value.schema_namespace)) { error = "invalid schema_namespace"; return false; }
   if(!SF01_IsSafeIdentifier(value.schema_name)) { error = "invalid schema_name"; return false; }
   if(value.major < 0 || value.minor < 0 || value.patch < 0) { error = "negative schema version"; return false; }
   error = "";
   return true;
}

ENUM_SF01_COMPATIBILITY SF01_CheckSchemaCompatibility(const SF01_SchemaIdentity &producer,
                                                       const SF01_SchemaIdentity &consumer)
{
   if(SF01_SchemaKey(producer) != SF01_SchemaKey(consumer)) return SF01_INCOMPATIBLE;
   if(producer.major != consumer.major) return SF01_INCOMPATIBLE;
   if(producer.minor <= consumer.minor) return SF01_COMPATIBLE;
   return SF01_COMPATIBLE_WITH_MIGRATION;
}

#endif
