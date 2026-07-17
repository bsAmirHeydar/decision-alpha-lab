#ifndef SAED_V4_37_COSTSCHEDULE_MQH
#define SAED_V4_37_COSTSCHEDULE_MQH
// SAED_V4_37 CostSchedule: research-only static contract mirror.
struct SAEDV437CostSchedule { string object_id; string object_hash; bool research_only; bool production_authorized; };
bool SAEDV437ValidateCostSchedule(const SAEDV437CostSchedule &x){ return x.object_id!="" && x.object_hash!="" && x.research_only && !x.production_authorized; }
#endif
