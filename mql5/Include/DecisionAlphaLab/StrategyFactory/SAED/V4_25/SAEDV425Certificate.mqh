#ifndef __SAED_V4_25_CERTIFICATE_MQH__
#define __SAED_V4_25_CERTIFICATE_MQH__
struct SAEDV425CertificateMirror { string certificate_id; string certificate_hash; bool research_accepted; bool research_only; bool runtime_executable; bool promotion_authority; bool production_authority; };
bool SAEDV425CertificateSafe(const SAEDV425CertificateMirror &value){ return value.research_accepted && value.research_only && !value.runtime_executable && !value.promotion_authority && !value.production_authority; }
#endif
