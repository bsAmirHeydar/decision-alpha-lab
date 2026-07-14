#ifndef __FP_I14_CHECKPOINT_MQH__
#define __FP_I14_CHECKPOINT_MQH__
struct FP_I14_Checkpoint { string version; string config_hash; long processed_sequence; string chain_hash; string payload_hash; };
bool FP_I14_ValidateCheckpoint(const FP_I14_Checkpoint &cp,const string expected_config,string &reason){if(cp.version!="FP-I14-CHECKPOINT-1"){reason="FP_DIAG_CHECKPOINT_VERSION_MISMATCH";return false;}if(cp.config_hash!=expected_config){reason="FP_DIAG_CHECKPOINT_CONFIG_MISMATCH";return false;}reason="FP_DIAG_CHECKPOINT_ACCEPTED";return true;}
#endif
