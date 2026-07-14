#ifndef FP_I15_CHECKPOINT_MQH
#define FP_I15_CHECKPOINT_MQH
#define FP_I15_CHECKPOINT_VERSION "FP-I15-CHECKPOINT-1"
struct FP_I15_Checkpoint { string version; string config_hash; string policy_hash; int ledger_event_count; string chain_hash; string payload_hash; };
bool FP_I15_CheckpointCompatible(const FP_I15_Checkpoint &cp,const string config_hash,const string policy_hash){ return cp.version==FP_I15_CHECKPOINT_VERSION && cp.config_hash==config_hash && cp.policy_hash==policy_hash && StringLen(cp.payload_hash)>0; }
#endif
