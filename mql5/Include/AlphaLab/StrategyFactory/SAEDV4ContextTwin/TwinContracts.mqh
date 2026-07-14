#ifndef AL_SAED_V4_02_TWIN_CONTRACTS_MQH
#define AL_SAED_V4_02_TWIN_CONTRACTS_MQH
struct ALTwinIdentity { string twin_id; string exact_version; string manifest_hash; string context_id; string context_version; string seed_hash; string constitution_hash; };
struct ALTwinStateView { string twin_id; string lifecycle_state; int twin_state; int observation_count; int contradiction_count; int debt_count; string snapshot_hash; };
struct ALTwinSupportView { string geometry_id; int support_status; double coverage; int failed_count; int unknown_count; };
#endif
