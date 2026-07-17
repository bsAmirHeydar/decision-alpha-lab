#ifndef SAED_V4_37_IMPACTESTIMATE_MQH
#define SAED_V4_37_IMPACTESTIMATE_MQH
// SAED_V4_37 ImpactEstimate: research-only static contract mirror.
struct SAEDV437ImpactEstimate { string object_id; string object_hash; bool research_only; bool production_authorized; };
bool SAEDV437ValidateImpactEstimate(const SAEDV437ImpactEstimate &x){ return x.object_id!="" && x.object_hash!="" && x.research_only && !x.production_authorized; }
#endif
