#ifndef SAED_V4_37_CAPACITYSURFACE_MQH
#define SAED_V4_37_CAPACITYSURFACE_MQH
// SAED_V4_37 CapacitySurface: research-only static contract mirror.
struct SAEDV437CapacitySurface { string object_id; string object_hash; bool research_only; bool production_authorized; };
bool SAEDV437ValidateCapacitySurface(const SAEDV437CapacitySurface &x){ return x.object_id!="" && x.object_hash!="" && x.research_only && !x.production_authorized; }
#endif
