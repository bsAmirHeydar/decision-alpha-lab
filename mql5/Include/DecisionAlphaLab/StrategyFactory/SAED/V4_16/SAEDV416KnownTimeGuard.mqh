#ifndef SAEDV416_KNOWN_TIME_MQH
#define SAEDV416_KNOWN_TIME_MQH
#define SAED_V4_16_PHASE "SAED_V4_16"
bool SAEDV416KnownTimeValid(const datetime context_time,const datetime feature_known_time,const datetime outcome_known_time){return feature_known_time<=context_time && outcome_known_time>=context_time;}
#endif
