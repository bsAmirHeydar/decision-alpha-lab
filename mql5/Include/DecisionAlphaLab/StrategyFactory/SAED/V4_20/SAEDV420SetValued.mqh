#property strict
#ifndef __DECISION_ALPHA_LAB_SAEDV420SETVALUED_MQH__
#define __DECISION_ALPHA_LAB_SAEDV420SETVALUED_MQH__
#define SAED_V4_20_PHASE "SAED_V4_20"
bool SAEDV420WithinMargin(const double best,const double score,const double margin){ return best-score<=margin; }
#endif
