#ifndef __AL_SAED_V4_DATA_FOUNDATION_SNAPSHOT_MQH__
#define __AL_SAED_V4_DATA_FOUNDATION_SNAPSHOT_MQH__
#include "DataFoundationContracts.mqh"
class ALSnapshotGate {
public:
 static bool Validate(const ALSnapshotIdentity &value,string &reason){
   if(value.snapshot_id=="" || value.snapshot_hash==""){reason="snapshot_identity_missing";return false;}
   if(value.lineage_root=="" || value.schema_set_hash==""){reason="snapshot_roots_missing";return false;}
   if(value.known_as_of<=0 || value.record_count<0){reason="snapshot_fields_invalid";return false;}
   reason="pass";return true;
 }
};
#endif
