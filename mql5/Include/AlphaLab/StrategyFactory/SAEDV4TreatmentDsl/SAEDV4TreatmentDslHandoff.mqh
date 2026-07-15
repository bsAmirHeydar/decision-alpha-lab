#ifndef ALPHALAB_SAED_V4_TREATMENT_DSL_HANDOFF_MQH
#define ALPHALAB_SAED_V4_TREATMENT_DSL_HANDOFF_MQH

bool SAEDV4DslV407AuthorityBounded(const bool read_frozen_dsl,const bool solve_bounded_lattice,const bool mutate_dsl,const bool generate_unbounded,const bool select_treatment,const bool allocate_risk,const bool activate_runtime,const bool send_order)
  {
   return(read_frozen_dsl && solve_bounded_lattice && !mutate_dsl && !generate_unbounded && !select_treatment && !allocate_risk && !activate_runtime && !send_order);
  }
#endif
