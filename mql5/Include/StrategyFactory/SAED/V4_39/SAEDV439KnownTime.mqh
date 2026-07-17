#ifndef SAED_V4_39_KNOWN_TIME_MQH
#define SAED_V4_39_KNOWN_TIME_MQH
bool SAEDV439KnownTimeValid(const datetime known_time,const datetime cutoff){return known_time<=cutoff;}
#endif
