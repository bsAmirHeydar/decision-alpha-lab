#ifndef FP_SAEDV430PACKAGE_MQH
#define FP_SAEDV430PACKAGE_MQH
struct FP_SAEDV430Package { string package_id; string package_hash; string candidate_commitment_hash; string dataset_commitment_hash; bool blinded; bool raw_rows_included; };
bool FP_SAEDV430PackageValid(const FP_SAEDV430Package &value) { return(StringLen(value.package_id)>0 && StringLen(value.package_hash)==64 && value.blinded && !value.raw_rows_included); }
#endif
