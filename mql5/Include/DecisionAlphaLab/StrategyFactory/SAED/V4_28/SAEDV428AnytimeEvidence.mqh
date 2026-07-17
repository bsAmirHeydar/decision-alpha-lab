#ifndef SAED_V4_28_ANYTIME_EVIDENCE_MQH
#define SAED_V4_28_ANYTIME_EVIDENCE_MQH
#include "SAEDV428Types.mqh"
bool SAEDV428KnownAtDecision(const SAEDV428Evidence &e){ return e.known_at<=e.decision_time; }
bool SAEDV428CrossesP(const SAEDV428Evidence &e,const double alpha){ return SAEDV428KnownAtDecision(e) && e.anytime_p<=alpha; }
#endif
