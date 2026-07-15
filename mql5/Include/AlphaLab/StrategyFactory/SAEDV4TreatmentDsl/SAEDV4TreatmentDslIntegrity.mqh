#ifndef ALPHALAB_SAED_V4_TREATMENT_DSL_INTEGRITY_MQH
#define ALPHALAB_SAED_V4_TREATMENT_DSL_INTEGRITY_MQH
#include "SAEDV4TreatmentDslCanonical.mqh"

bool SAEDV4DslIntegrityFieldsValid(const string package_hash,const string registry_hash,const string policy_hash,const string graph_hash)
  {
   return(SAEDV4DslLooksLikeSha256(package_hash) && SAEDV4DslLooksLikeSha256(registry_hash) && SAEDV4DslLooksLikeSha256(policy_hash) && SAEDV4DslLooksLikeSha256(graph_hash));
  }
#endif
