#ifndef __DECISION_ALPHA_LAB_SAED_V4_11_CONTRACTS_MQH__
#define __DECISION_ALPHA_LAB_SAED_V4_11_CONTRACTS_MQH__
struct SAEDV411TokenStreamContract
{
   string record_id;
   string context_id;
   string root_context_id;
   string domain_id;
   datetime event_time;
   datetime known_time;
   string split_name;
   string token_hash;
};
struct SAEDV411CheckpointContract
{
   string checkpoint_id;
   string checkpoint_hash;
   string tokenizer_hash;
   string corpus_manifest_hash;
   string split_manifest_hash;
   string training_receipt_hash;
   int embedding_dimension;
   bool synthetic_reference_only;
   bool runtime_authority;
   bool execution_authority;
};
struct SAEDV411HandoffContract
{
   string handoff_id;
   string handoff_hash;
   string next_phase;
   string encoder_checkpoint_hash;
   bool outcome_supervision_absent;
   bool future_suffix_forbidden;
   bool send_order;
};
#endif
