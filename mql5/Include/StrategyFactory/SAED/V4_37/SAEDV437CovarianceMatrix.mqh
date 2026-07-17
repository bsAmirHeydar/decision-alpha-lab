#ifndef SAED_V4_37_COVARIANCEMATRIX_MQH
#define SAED_V4_37_COVARIANCEMATRIX_MQH
// SAED_V4_37 CovarianceMatrix: research-only static contract mirror.
struct SAEDV437CovarianceMatrix { string object_id; string object_hash; bool research_only; bool production_authorized; };
bool SAEDV437ValidateCovarianceMatrix(const SAEDV437CovarianceMatrix &x){ return x.object_id!="" && x.object_hash!="" && x.research_only && !x.production_authorized; }
#endif
