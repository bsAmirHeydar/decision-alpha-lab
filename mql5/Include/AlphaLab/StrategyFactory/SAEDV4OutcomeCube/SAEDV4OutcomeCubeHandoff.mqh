#ifndef ALPHALAB_SAED_V4_OUTCOME_CUBE_HANDOFF_MQH
#define ALPHALAB_SAED_V4_OUTCOME_CUBE_HANDOFF_MQH
// PRODUCTION_AUTHORIZATION false
struct SAEDV408Handoff{string phase;string next_phase;string cube_hash;string receipt_hash;bool complete_exposure;bool execution_authority;};
bool SAEDV408HandoffValid(const SAEDV408Handoff &x){return x.phase=="SAED_V4_08" && x.next_phase=="SAED_V4_09" && x.complete_exposure && !x.execution_authority;}
#endif
