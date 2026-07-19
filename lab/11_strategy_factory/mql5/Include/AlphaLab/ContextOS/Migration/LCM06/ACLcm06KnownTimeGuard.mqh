#ifndef __ALPHALAB_LCM06_KNOWN_TIME_GUARD_MQH__
#define __ALPHALAB_LCM06_KNOWN_TIME_GUARD_MQH__
inline bool AL_LCM06_KnownTimeSafe(const datetime event_time,const datetime available_at){ return event_time<=available_at; }
#endif
