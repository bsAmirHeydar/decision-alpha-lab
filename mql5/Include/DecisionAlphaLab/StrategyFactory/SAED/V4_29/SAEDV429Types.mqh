#ifndef SAED_V4_29_TYPES_MQH
#define SAED_V4_29_TYPES_MQH
struct SAEDV429Commitment { string candidate_id; string candidate_hash; string dataset_hash; string protocol_hash; datetime submitted_at; bool frozen; };
struct SAEDV429Token { string token_id; string candidate_hash; string dataset_hash; int maximum_uses; int used_count; bool revoked; };
struct SAEDV429AggregateResult { string evaluation_id; string candidate_id; double balanced_accuracy; double brier_score; double delta_vs_baseline; bool passed; };
#endif
