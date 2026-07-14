#ifndef ALPHA_LAB_SAED_V4_EVENT_DIAGNOSTICS
#define ALPHA_LAB_SAED_V4_EVENT_DIAGNOSTICS
#include "EventAuthority.mqh"
#include "EventOrdering.mqh"
bool SAED_EventSelfTest(){return SAED_EventAuthoritySafe()&&SAED_EventTemporalValid(D'2026.01.01 00:00:00',D'2026.01.01 00:00:01')&&SAED_EventSequenceValid(1,1);}
#endif
