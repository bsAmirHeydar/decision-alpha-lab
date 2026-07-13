#ifndef __FP_I05_CHECKPOINT_MQH__
#define __FP_I05_CHECKPOINT_MQH__
struct FP_I05_Checkpoint { string checkpoint_id,checkpoint_version,config_hash,source_revision_id,snapshot_semantic_hash,payload_hash; long created_utc_ms; bool Valid() const { return checkpoint_id!="" && checkpoint_version=="1.0.0" && config_hash!="" && source_revision_id!="" && payload_hash!=""; } };
#endif
