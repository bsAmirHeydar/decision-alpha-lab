#ifndef __ALPHALAB_LCM06_TRACE_EVENT_MQH__
#define __ALPHALAB_LCM06_TRACE_EVENT_MQH__
struct AL_LCM06_TRACE_EVENT { datetime event_time; datetime available_at; long bar_index; string event_type; string state_before; string state_after; string decision; string direction; bool no_trade; };
#endif
