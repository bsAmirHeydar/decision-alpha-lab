#ifndef ALPHA_LAB_SAED_V4_EVENT_ORDERING
#define ALPHA_LAB_SAED_V4_EVENT_ORDERING
bool SAED_EventTemporalValid(const datetime event_time,const datetime known_time){return known_time>=event_time;}
bool SAED_EventSequenceValid(const long expected,const long observed){return expected==observed;}
#endif
