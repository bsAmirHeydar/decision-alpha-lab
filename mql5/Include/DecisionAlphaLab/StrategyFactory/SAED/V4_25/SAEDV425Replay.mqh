#ifndef __SAED_V4_25_REPLAY_MQH__
#define __SAED_V4_25_REPLAY_MQH__
struct SAEDV425ReplayEntry { string task_id; string context_id; ENUM_SAEDV425_DRIFT_CLASS drift_class; datetime decision_time; bool query_outcomes_stored; };
bool SAEDV425ReplayEntrySafe(const SAEDV425ReplayEntry &entry){ return StringLen(entry.task_id)>0 && StringLen(entry.context_id)>0 && !entry.query_outcomes_stored; }
#endif
