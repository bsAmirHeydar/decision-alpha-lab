#ifndef SAED_V4_37_INSTRUMENTMASTER_MQH
#define SAED_V4_37_INSTRUMENTMASTER_MQH
// SAED_V4_37 InstrumentMaster: research-only static contract mirror.
struct SAEDV437InstrumentMaster { string object_id; string object_hash; bool research_only; bool production_authorized; };
bool SAEDV437ValidateInstrumentMaster(const SAEDV437InstrumentMaster &x){ return x.object_id!="" && x.object_hash!="" && x.research_only && !x.production_authorized; }
#endif
