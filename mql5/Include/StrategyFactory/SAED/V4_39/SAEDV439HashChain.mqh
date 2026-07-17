#ifndef SAED_V4_39_HASH_CHAIN_MQH
#define SAED_V4_39_HASH_CHAIN_MQH
struct SAEDV439HashLink { long ordinal; string previous_hash; string event_hash; };
bool SAEDV439HashFormatValid(const string h){return StringLen(h)==64;}
#endif
