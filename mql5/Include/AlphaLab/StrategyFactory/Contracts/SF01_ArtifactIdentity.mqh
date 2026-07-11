#ifndef __SF01_ARTIFACT_IDENTITY_MQH__
#define __SF01_ARTIFACT_IDENTITY_MQH__

#include "SF01_SchemaIdentity.mqh"
#include "SF01_MarketTimestamp.mqh"
#include "SF01_Hash.mqh"


struct SF01_ArtifactIdentity
{
   SF01_SchemaIdentity schema;
   string artifact_id;
   string artifact_type;
   string run_id;
   string producer_id;
   string producer_version;
   string git_commit;
   string strategy_id;
   string strategy_version;
   string manifest_hash;
   string source_hash;
   SF01_MarketTimestamp created_at;
};

string SF01_ArtifactCanonicalIdentity(const SF01_ArtifactIdentity &value)
{
   return value.artifact_type + "|" + value.run_id + "|" + value.producer_id + "|" +
          value.producer_version + "|" + value.git_commit + "|" + value.strategy_id + "|" +
          value.strategy_version + "|" + value.manifest_hash + "|" + value.source_hash + "|" +
          IntegerToString(value.created_at.utc_epoch_milliseconds);
}

string SF01_DeriveArtifactId(const SF01_ArtifactIdentity &value)
{
   return SF01_StableId("art", SF01_ArtifactCanonicalIdentity(value));
}

bool SF01_ValidateArtifactIdentity(const SF01_ArtifactIdentity &value, string &error)
{
   if(!SF01_ValidateSchemaIdentity(value.schema, error)) return false;
   if(!SF01_IsSafeIdentifier(value.artifact_type)) { error = "invalid artifact_type"; return false; }
   if(!SF01_IsSafeIdentifier(value.run_id)) { error = "invalid run_id"; return false; }
   if(!SF01_IsSafeIdentifier(value.producer_id)) { error = "invalid producer_id"; return false; }
   if(!SF01_IsSafeIdentifier(value.producer_version)) { error = "invalid producer_version"; return false; }
   if(!SF01_IsSafeIdentifier(value.git_commit)) { error = "invalid git_commit"; return false; }
   if(!SF01_IsSafeIdentifier(value.strategy_id)) { error = "invalid strategy_id"; return false; }
   if(!SF01_IsSafeIdentifier(value.strategy_version)) { error = "invalid strategy_version"; return false; }
   if(!SF01_IsSafeIdentifier(value.manifest_hash)) { error = "invalid manifest_hash"; return false; }
   if(!SF01_IsSafeIdentifier(value.source_hash)) { error = "invalid source_hash"; return false; }
   if(!SF01_ValidateTimestamp(value.created_at, error)) return false;
   const string expected = SF01_DeriveArtifactId(value);
   if(value.artifact_id != "" && value.artifact_id != expected) { error = "artifact_id mismatch"; return false; }
   error = "";
   return true;
}

#endif
