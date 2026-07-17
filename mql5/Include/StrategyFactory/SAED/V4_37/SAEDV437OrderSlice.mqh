#ifndef SAED_V4_37_ORDERSLICE_MQH
#define SAED_V4_37_ORDERSLICE_MQH
// SAED_V4_37 OrderSlice: research-only static contract mirror.
struct SAEDV437OrderSlice { string object_id; string object_hash; bool research_only; bool production_authorized; };
bool SAEDV437ValidateOrderSlice(const SAEDV437OrderSlice &x){ return x.object_id!="" && x.object_hash!="" && x.research_only && !x.production_authorized; }
#endif
