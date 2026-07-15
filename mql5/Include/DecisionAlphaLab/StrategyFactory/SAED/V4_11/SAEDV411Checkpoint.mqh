#ifndef __DECISION_ALPHA_LAB_SAED_V4_11_CHECKPOINT_MQH__
#define __DECISION_ALPHA_LAB_SAED_V4_11_CHECKPOINT_MQH__
#include "SAEDV411Contracts.mqh"
#include "SAEDV411Canonical.mqh"
bool SAEDV411ValidateCheckpoint(const SAEDV411CheckpointContract &checkpoint)
{
   if(checkpoint.checkpoint_id=="") return false;
   if(!SAEDV411IsSha256(checkpoint.checkpoint_hash)) return false;
   if(!SAEDV411IsSha256(checkpoint.tokenizer_hash)) return false;
   if(!SAEDV411IsSha256(checkpoint.corpus_manifest_hash)) return false;
   if(!SAEDV411IsSha256(checkpoint.split_manifest_hash)) return false;
   if(!SAEDV411IsSha256(checkpoint.training_receipt_hash)) return false;
   if(checkpoint.embedding_dimension<4 || checkpoint.embedding_dimension>256) return false;
   if(!checkpoint.synthetic_reference_only) return false;
   if(checkpoint.runtime_authority || checkpoint.execution_authority) return false;
   return true;
}
#endif
