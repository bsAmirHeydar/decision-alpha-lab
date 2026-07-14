#ifndef __AL_SAED_V4_DATA_FOUNDATION_CONTRACTS_MQH__
#define __AL_SAED_V4_DATA_FOUNDATION_CONTRACTS_MQH__
#include "DataFoundationEnums.mqh"
struct ALBitemporalStamp { datetime event_time; datetime known_time; datetime valid_to; bool has_valid_to; };
struct ALArtifactIdentity { string artifact_id; string exact_version; string content_hash; string schema_name; string schema_version; AL_DATA_ROLE data_role; };
struct ALRevisionIdentity { string entity_id; string revision_id; int revision_number; string supersedes_revision_id; ALBitemporalStamp temporal; };
struct ALSnapshotIdentity { string snapshot_id; string snapshot_hash; string lineage_root; string schema_set_hash; datetime known_as_of; datetime event_as_of; bool has_event_as_of; AL_DATA_ROLE data_role; int record_count; };
struct ALTwinSeedIdentity { string package_id; string package_hash; string context_specification_artifact_id; string lineage_root; string constitution_hash; datetime known_as_of; int snapshot_count; };
#endif
