#property strict
#ifndef __DECISION_ALPHA_LAB_SAEDV420ABSTENTION_MQH__
#define __DECISION_ALPHA_LAB_SAEDV420ABSTENTION_MQH__
#define SAED_V4_20_PHASE "SAED_V4_20"
bool SAEDV420MustAbstain(const bool proof_fail,const bool support_fail,const bool margin_fail){ return proof_fail || support_fail || margin_fail; }
#endif
