#ifndef ALPHALAB_ACL06_KNOWN_TIME_GUARD_MQH
#define ALPHALAB_ACL06_KNOWN_TIME_GUARD_MQH
bool ACL06KnownTimeValid(const datetime event_time,const datetime available_at,const datetime cut_at){ return event_time<=available_at && available_at<=cut_at; }
#endif
