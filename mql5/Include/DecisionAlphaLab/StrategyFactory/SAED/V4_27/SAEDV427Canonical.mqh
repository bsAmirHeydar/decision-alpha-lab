#ifndef SAED_V4_27_CANONICAL_MQH
#define SAED_V4_27_CANONICAL_MQH
string SAEDV427StableEnvelope(const string phase,const int sequence,const string previous_hash,const string payload_hash){ return phase+"|"+(string)sequence+"|"+previous_hash+"|"+payload_hash; }
#endif
