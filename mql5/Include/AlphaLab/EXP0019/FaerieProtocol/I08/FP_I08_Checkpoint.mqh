#ifndef FP_I08_CHECKPOINT_MQH
#define FP_I08_CHECKPOINT_MQH
struct FP_I08_Checkpoint{string version;string config_hash;string snapshot_hash;string stack_hash;datetime created_time;};
bool FP_I08_ValidateCheckpoint(const FP_I08_Checkpoint &cp,const string config_hash,const string snapshot_hash,const string stack_hash){return cp.version=="1.0.0"&&cp.config_hash==config_hash&&cp.snapshot_hash==snapshot_hash&&cp.stack_hash==stack_hash;}
#endif
