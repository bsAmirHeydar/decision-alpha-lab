#ifndef __FP_I12_CHECKPOINT_MQH__
#define __FP_I12_CHECKPOINT_MQH__
#include "FP_I12_Hash.mqh"
string FP_I12_CheckpointKey(const string instance_id){return "FP12::CKPT::"+FP_I12_Hash(instance_id);}
#endif
