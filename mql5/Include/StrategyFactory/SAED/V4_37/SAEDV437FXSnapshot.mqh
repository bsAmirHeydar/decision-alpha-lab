#ifndef SAED_V4_37_FXSNAPSHOT_MQH
#define SAED_V4_37_FXSNAPSHOT_MQH
// SAED_V4_37 FXSnapshot: research-only static contract mirror.
struct SAEDV437FXSnapshot { string object_id; string object_hash; bool research_only; bool production_authorized; };
bool SAEDV437ValidateFXSnapshot(const SAEDV437FXSnapshot &x){ return x.object_id!="" && x.object_hash!="" && x.research_only && !x.production_authorized; }
#endif
