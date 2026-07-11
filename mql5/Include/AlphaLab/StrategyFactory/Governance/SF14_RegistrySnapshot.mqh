#ifndef __SF14_REGISTRY_SNAPSHOT_MQH__
#define __SF14_REGISTRY_SNAPSHOT_MQH__
#include "SF14_ModelRegistry.mqh"
struct SF14_RegistrySnapshot{string snapshot_id;string registry_version;int decision_sequence;string decision_chain_hash;int entry_count;int champion_count;int challenger_count;long generated_at_utc_msc;bool no_execution_authority;string snapshot_hash;};
string SF14_RegistrySnapshotCanonical(const SF14_RegistrySnapshot &v){return "alpha_lab.strategy_factory/registry_snapshot@1.0.0|"+v.snapshot_id+"|"+v.registry_version+"|"+IntegerToString(v.decision_sequence)+"|"+v.decision_chain_hash+"|"+IntegerToString(v.entry_count)+"|"+IntegerToString(v.champion_count)+"|"+IntegerToString(v.challenger_count)+"|"+IntegerToString(v.generated_at_utc_msc)+"|"+SF01_CanonicalBool(v.no_execution_authority);}
string SF14_DeriveSnapshotHash(const SF14_RegistrySnapshot &v){return SF01_StableId("rsnap",SF14_RegistrySnapshotCanonical(v));}
#endif
