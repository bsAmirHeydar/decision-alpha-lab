#ifndef SAED_V4_29_CUSTODY_MQH
#define SAED_V4_29_CUSTODY_MQH
bool SAEDV429CustodyThreshold(const int custodians,const int threshold){ return custodians>=2 && threshold>=2 && threshold<=custodians; }
bool SAEDV429ResearcherPlaintextAccess(){ return false; }
#endif
