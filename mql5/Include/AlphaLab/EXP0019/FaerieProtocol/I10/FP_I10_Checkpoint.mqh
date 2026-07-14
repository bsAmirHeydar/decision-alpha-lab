#ifndef __FP_I10_CHECKPOINT_MQH__
#define __FP_I10_CHECKPOINT_MQH__
#include "FP_I10_Contracts.mqh"
bool FP_I10_CheckpointCompatible(const string stored_config_hash,const SFP_I10_Config &config){ return stored_config_hash==config.config_hash; }
#endif
