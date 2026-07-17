#ifndef SAED_V4_37_CERTIFICATE_MQH
#define SAED_V4_37_CERTIFICATE_MQH
// SAED_V4_37 Certificate: research-only static contract mirror.
struct SAEDV437Certificate { string object_id; string object_hash; bool research_only; bool production_authorized; };
bool SAEDV437ValidateCertificate(const SAEDV437Certificate &x){ return x.object_id!="" && x.object_hash!="" && x.research_only && !x.production_authorized; }
#endif
