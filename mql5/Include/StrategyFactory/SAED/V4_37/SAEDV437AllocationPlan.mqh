#ifndef SAED_V4_37_ALLOCATIONPLAN_MQH
#define SAED_V4_37_ALLOCATIONPLAN_MQH
// SAED_V4_37 AllocationPlan: research-only static contract mirror.
struct SAEDV437AllocationPlan { string object_id; string object_hash; bool research_only; bool production_authorized; };
bool SAEDV437ValidateAllocationPlan(const SAEDV437AllocationPlan &x){ return x.object_id!="" && x.object_hash!="" && x.research_only && !x.production_authorized; }
#endif
