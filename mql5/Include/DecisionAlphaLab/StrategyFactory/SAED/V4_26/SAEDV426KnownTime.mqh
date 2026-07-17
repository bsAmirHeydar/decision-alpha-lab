#ifndef DAL_SAED_V426_KNOWN_TIME_MQH
#define DAL_SAED_V426_KNOWN_TIME_MQH
bool SAEDV426KnownAtDecision(const datetime known_at,const datetime decision_at){ return known_at<=decision_at; }
#endif
