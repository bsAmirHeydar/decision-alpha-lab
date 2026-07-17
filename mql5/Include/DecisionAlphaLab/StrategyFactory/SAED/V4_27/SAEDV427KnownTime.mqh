#ifndef SAED_V4_27_KNOWN_TIME_MQH
#define SAED_V4_27_KNOWN_TIME_MQH
bool SAEDV427KnownTimeValid(const long known_at,const long occurred_at){ return known_at<=occurred_at; }
#endif
