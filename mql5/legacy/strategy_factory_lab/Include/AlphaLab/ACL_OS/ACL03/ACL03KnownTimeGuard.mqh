#ifndef AL_ACL03_KNOWN_TIME_MQH
#define AL_ACL03_KNOWN_TIME_MQH
bool AL_ACL03_KnownTimeSafe(datetime event_time,datetime observation_time,datetime known_time,datetime decision_time){ return event_time<=observation_time && observation_time<=known_time && known_time<=decision_time; }
#endif
