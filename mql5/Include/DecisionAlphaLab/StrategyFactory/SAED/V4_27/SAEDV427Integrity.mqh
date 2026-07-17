#ifndef SAED_V4_27_INTEGRITY_MQH
#define SAED_V4_27_INTEGRITY_MQH
bool SAEDV427ChainLinkValid(const int sequence,const string previous_hash,const string expected_previous_hash){ return sequence>0 && previous_hash==expected_previous_hash; }
#endif
