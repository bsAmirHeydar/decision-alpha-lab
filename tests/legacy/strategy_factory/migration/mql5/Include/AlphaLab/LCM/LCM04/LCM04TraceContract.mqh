#ifndef ALPHALAB_LCM04_TRACE_CONTRACT_MQH
#define ALPHALAB_LCM04_TRACE_CONTRACT_MQH
struct LCM04TraceEvent { string trace_id; string case_id; int sequence; datetime event_time; datetime available_at; string event_type; string reason_codes; bool broker_submission_performed; };
#endif
