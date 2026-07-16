#ifndef SAEDV415_FUSION_CONTRACTS_MQH
#define SAEDV415_FUSION_CONTRACTS_MQH
// SAED_V4_15 closed static envelope mirror.
struct SAEDV415ViewEnvelope { string view_name; string source_plane; string envelope_hash; datetime known_as_of; int age_seconds; double quality; bool available; double embedding[16]; };
struct SAEDV415FusionEnvelope { string candidate_id; string fusion_hash; int directive; double uncertainty; double disagreement; double gate_concentration; bool production_eligible; double embedding[16]; };
#endif
