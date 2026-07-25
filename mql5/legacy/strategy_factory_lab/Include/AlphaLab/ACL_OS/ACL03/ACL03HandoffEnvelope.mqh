#ifndef AL_ACL03_HANDOFF_MQH
#define AL_ACL03_HANDOFF_MQH
struct AL_ACL03_Handoff { string context_id; string context_version; string source_snapshot_digest; string detector_ir_digest; bool search_authority_required; };
#endif
