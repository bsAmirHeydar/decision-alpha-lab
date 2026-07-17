#ifndef ALPHALAB_ACL05_TYPES_MQH
#define ALPHALAB_ACL05_TYPES_MQH
#define ACL05_SCHEMA_VERSION "1.0.0"
#define ACL05_CLAIM_CEILING "RESEARCH_BATCH_FREEZE_REFERENCE_ONLY"
enum ENUM_ACL05_BATCH_STATE { ACL05_BATCH_INVALID=0, ACL05_BATCH_FROZEN=1 };
struct ACL05ArtifactRef { string logical_id; string digest; string media_type; long size_bytes; bool immutable; };
struct ACL05CandidateRef { string setup_id; string candidate_id; string candidate_digest; string behavior_digest; string status; bool payload_mutable; };
#endif
