#ifndef AL_ACL03_REPLAY_MQH
#define AL_ACL03_REPLAY_MQH
struct AL_ACL03_ReplayEvent { string event_name; datetime known_time; datetime decision_time; int guard_result; };
#endif
