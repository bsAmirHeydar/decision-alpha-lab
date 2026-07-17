#ifndef SAED_V4_37_DEPENDENCEMODEL_MQH
#define SAED_V4_37_DEPENDENCEMODEL_MQH
// SAED_V4_37 DependenceModel: research-only static contract mirror.
struct SAEDV437DependenceModel { string object_id; string object_hash; bool research_only; bool production_authorized; };
bool SAEDV437ValidateDependenceModel(const SAEDV437DependenceModel &x){ return x.object_id!="" && x.object_hash!="" && x.research_only && !x.production_authorized; }
#endif
