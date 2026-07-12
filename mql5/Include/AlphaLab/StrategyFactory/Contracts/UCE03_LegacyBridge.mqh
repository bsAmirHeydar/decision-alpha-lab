#ifndef __UCE03_LEGACY_BRIDGE_MQH__
#define __UCE03_LEGACY_BRIDGE_MQH__
#include "UCE03_Identity.mqh"
#include "UCE03_Schema.mqh"
#include "UCE03_KnownTime.mqh"
struct UCE03_LegacyBridgeRecord
{
   string legacy_contract_id;
   string legacy_schema_id;
   string legacy_entity_id;
   string legacy_payload_sha256;
   string v3_entity_id;
   string v3_identity_sha256;
   UCE03_UtcInstant bridged_at;
   string bridge_version;
};
UCE03_IdentityKey UCE03_BuildLegacyIdentity(const ENUM_UCE03_IDENTITY_KIND kind,const string semantic_namespace,const string semantic_version,const string owner_id,const string legacy_contract_id,const UCE03_SchemaId &legacy_schema,const string legacy_entity_id,const string legacy_payload_sha256)
{
   CUCE03CanonicalObject dimensions;
   dimensions.AddString("legacy_contract_id",legacy_contract_id);
   dimensions.AddString("legacy_entity_id",legacy_entity_id);
   dimensions.AddString("legacy_payload_sha256",legacy_payload_sha256);
   dimensions.AddString("legacy_schema_id",UCE03_SchemaExactKey(legacy_schema));
   UCE03_IdentityKey result;result.kind=kind;result.semantic_namespace=semantic_namespace;result.semantic_version=semantic_version;result.owner_id=owner_id;result.dimensions_json=dimensions.Serialize();return result;
}
#endif
