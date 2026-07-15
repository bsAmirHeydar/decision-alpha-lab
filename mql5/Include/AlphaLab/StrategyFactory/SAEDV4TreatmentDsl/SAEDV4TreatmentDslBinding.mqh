#ifndef ALPHALAB_SAED_V4_TREATMENT_DSL_BINDING_MQH
#define ALPHALAB_SAED_V4_TREATMENT_DSL_BINDING_MQH
#include "SAEDV4TreatmentDslTypes.mqh"
#include "SAEDV4TreatmentDslCanonical.mqh"

bool SAEDV4DslBindingHeaderValid(const SAEDV4DslBindingHeader &value)
  {
   if(!value.bound) return false;
   if(StringLen(value.descriptor_id)<2 || StringLen(value.graph_node_id)<8 || StringLen(value.program_id)<8) return false;
   return(SAEDV4DslLooksLikeSha256(value.binding_hash) && SAEDV4DslLooksLikeSha256(value.graph_node_hash) && SAEDV4DslLooksLikeSha256(value.program_hash));
  }
#endif
