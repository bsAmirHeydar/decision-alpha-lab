#ifndef FP_SAEDV430CERTIFICATE_MQH
#define FP_SAEDV430CERTIFICATE_MQH
struct FP_SAEDV430Certificate { string certificate_id; string certificate_hash; bool accepted_reference; bool synthetic_laboratory_fixture; bool external_replication_claim; bool production_authority; };
bool FP_SAEDV430CertificateValid(const FP_SAEDV430Certificate &value) { return(StringLen(value.certificate_id)>0 && StringLen(value.certificate_hash)==64 && value.accepted_reference && value.synthetic_laboratory_fixture && !value.external_replication_claim && !value.production_authority); }
#endif
