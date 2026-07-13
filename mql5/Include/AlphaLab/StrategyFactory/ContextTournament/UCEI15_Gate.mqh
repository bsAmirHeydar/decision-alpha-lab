#ifndef ALPHALAB_UCEI15_GATE_MQH
#define ALPHALAB_UCEI15_GATE_MQH
#include "UCEI15_Types.mqh"
bool UCEI15_AllCriticalGatesPass(const UCEI15_GateState &g){return(g.tournament_not_reference_only&&g.bounded_challenger_exists&&g.paper_mode_prospective&&g.paper_completed&&g.paper_untouched&&g.paper_no_critical_findings&&g.paper_zero_reconciliation_mismatch);}
int UCEI15_Decide(const UCEI15_GateState &g,const bool promotion_bundle_present){if(!UCEI15_AllCriticalGatesPass(g))return(UCEI15_REJECT);if(!promotion_bundle_present)return(UCEI15_PENDING);return(UCEI15_PROMOTE);}
#endif
