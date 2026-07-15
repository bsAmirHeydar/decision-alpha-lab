#ifndef ALPHALAB_SAED_V4_TREATMENT_DSL_PROGRAM_MQH
#define ALPHALAB_SAED_V4_TREATMENT_DSL_PROGRAM_MQH
#include "SAEDV4TreatmentDslTypes.mqh"
#include "SAEDV4TreatmentDslCanonical.mqh"

bool SAEDV4DslProgramHeaderValid(const SAEDV4DslProgramHeader &value)
  {
   if(StringLen(value.program_id)<8 || !SAEDV4DslLooksLikeSha256(value.program_hash)) return false;
   if(StringLen(value.program_name)<2 || StringLen(value.exact_version)<5) return false;
   if(value.component_count<1 || value.constraint_count<0) return false;
   return(value.status==SAED_V4_DSL_PROGRAM_ACCEPTED);
  }
#endif
