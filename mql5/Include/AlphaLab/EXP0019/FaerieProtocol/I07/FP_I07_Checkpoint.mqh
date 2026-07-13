#ifndef FP_I07_CHECKPOINT_MQH
#define FP_I07_CHECKPOINT_MQH
struct SFP_I07_Checkpoint { string version; string config_hash; datetime last_close; string revision_id; string payload_hash; };
bool FP_I07_CheckpointCompatible(const SFP_I07_Checkpoint &cp,const string expected_config) { return cp.version=="1.0.0" && cp.config_hash==expected_config && cp.payload_hash!=""; }
#endif
