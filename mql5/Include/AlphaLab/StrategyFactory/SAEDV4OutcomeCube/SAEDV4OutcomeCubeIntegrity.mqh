#ifndef ALPHALAB_SAED_V4_OUTCOME_CUBE_INTEGRITY_MQH
#define ALPHALAB_SAED_V4_OUTCOME_CUBE_INTEGRITY_MQH
// PRODUCTION_AUTHORIZATION false
struct SAEDV408IntegrityReceipt{string cube_hash;string row_merkle_root;string lattice_hash;string context_hash;bool complete_exposure;};
bool SAEDV408IntegrityValid(const SAEDV408IntegrityReceipt &x){return StringLen(x.cube_hash)==64 && StringLen(x.row_merkle_root)==64 && x.complete_exposure;}
#endif
