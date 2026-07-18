#ifndef ALPHALAB_ACL14_KNOWN_TIME_MQH
#define ALPHALAB_ACL14_KNOWN_TIME_MQH
bool ACL14KnownTimeSafe(const datetime event_time,const datetime available_at,const datetime cut_at){return event_time<=available_at && available_at<=cut_at;}
#endif
