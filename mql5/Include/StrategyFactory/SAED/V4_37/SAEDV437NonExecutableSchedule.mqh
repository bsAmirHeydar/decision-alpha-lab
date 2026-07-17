#ifndef SAED_V4_37_NONEXECUTABLESCHEDULE_MQH
#define SAED_V4_37_NONEXECUTABLESCHEDULE_MQH
// SAED_V4_37 NonExecutableSchedule: research-only static contract mirror.
struct SAEDV437NonExecutableSchedule { string object_id; string object_hash; bool research_only; bool production_authorized; };
bool SAEDV437ValidateNonExecutableSchedule(const SAEDV437NonExecutableSchedule &x){ return x.object_id!="" && x.object_hash!="" && x.research_only && !x.production_authorized; }
#endif
