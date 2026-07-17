#ifndef SAED_V4_29_KNOWN_TIME_MQH
#define SAED_V4_29_KNOWN_TIME_MQH
bool SAEDV429CommitBeforeEvaluation(const datetime committed_at,const datetime evaluated_at){ return committed_at<=evaluated_at; }
#endif
