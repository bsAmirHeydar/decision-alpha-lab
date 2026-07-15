#ifndef ALPHALAB_SAED_V4_TREATMENT_DSL_AUTHORITY_MQH
#define ALPHALAB_SAED_V4_TREATMENT_DSL_AUTHORITY_MQH
#include "SAEDV4TreatmentDslTypes.mqh"

SAEDV4DslAuthority SAEDV4DslInstitutionalAuthority()
  {
   SAEDV4DslAuthority value;
   value.read_hypergraph=true;
   value.define_finite_dsl=true;
   value.validate_program=true;
   value.bind_external_descriptor=true;
   value.solve_action_lattice=false;
   value.select_treatment=false;
   value.allocate_risk=false;
   value.activate_runtime=false;
   value.send_order=false;
   return value;
  }

bool SAEDV4DslAuthorityIsBounded(const SAEDV4DslAuthority &value)
  {
   return(value.read_hypergraph && value.define_finite_dsl && value.validate_program && value.bind_external_descriptor &&
          !value.solve_action_lattice && !value.select_treatment && !value.allocate_risk && !value.activate_runtime && !value.send_order);
  }
#endif
