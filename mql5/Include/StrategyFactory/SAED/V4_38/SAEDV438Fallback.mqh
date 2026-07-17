#ifndef SAED_V4_38_FALLBACK_MQH
#define SAED_V4_38_FALLBACK_MQH
#include "SAEDV438Types.mqh"
void SAEDV438Abstain(SAEDV438Decision &d){d.decision="ABSTAIN";d.treatment_id="BASELINE";d.confidence=0;d.net_edge_bps=0;d.size_fraction=0;}
#endif
