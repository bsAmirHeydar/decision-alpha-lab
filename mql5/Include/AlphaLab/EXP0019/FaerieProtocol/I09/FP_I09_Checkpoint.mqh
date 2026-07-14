#ifndef __FP_I09_CHECKPOINT_MQH__
#define __FP_I09_CHECKPOINT_MQH__
struct FP_I09_CheckpointHeader { string checkpoint_id,version,config_hash,chain_head_hash,payload_hash; long event_count,created_utc; };
bool FP_I09_CheckpointCompatible(const FP_I09_CheckpointHeader &h,const string expected_config,const string expected_head){ return h.version=="1.0.0" && h.config_hash==expected_config && h.chain_head_hash==expected_head; }
#endif
