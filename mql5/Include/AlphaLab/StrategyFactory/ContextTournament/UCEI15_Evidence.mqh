#ifndef ALPHALAB_UCEI15_EVIDENCE_MQH
#define ALPHALAB_UCEI15_EVIDENCE_MQH
bool UCEI15_EvidencePass(const bool hash_valid,const bool ledger_valid,const bool rejected_work_retained){return(hash_valid&&ledger_valid&&rejected_work_retained);}
#endif
