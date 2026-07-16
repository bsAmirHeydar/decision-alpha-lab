#property strict
#ifndef __DECISION_ALPHA_LAB_SAEDV420ACTIONMASK_MQH__
#define __DECISION_ALPHA_LAB_SAEDV420ACTIONMASK_MQH__
#define SAED_V4_20_PHASE "SAED_V4_20"
bool SAEDV420MaskAllowed(const bool proof_ok,const bool support_ok,const bool overlap_ok){ return proof_ok && support_ok && overlap_ok; }
#endif
