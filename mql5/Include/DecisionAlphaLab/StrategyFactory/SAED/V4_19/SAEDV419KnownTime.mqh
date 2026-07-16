#ifndef SAED_V4_19_KNOWN_TIME_MQH
#define SAED_V4_19_KNOWN_TIME_MQH
bool SAEDV419KnownTimeValid(const long known_time,const long decision_time){ return known_time<=decision_time; }
#endif
