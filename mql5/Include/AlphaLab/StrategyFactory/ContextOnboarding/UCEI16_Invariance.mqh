#ifndef ALPHALAB_UCEI16_INVARIANCE_MQH
#define ALPHALAB_UCEI16_INVARIANCE_MQH
#include "UCEI16_Types.mqh"
struct UCEI16_InvarianceReport { string before_hash; string after_hash; UCEI16_InvarianceStatus status; int changed_core_count; string adr_id; };
bool UCEI16_InvarianceAccepted(const UCEI16_InvarianceReport &r){ if(r.changed_core_count==0) return r.status==UCEI16_INVARIANCE_PASS; return r.status==UCEI16_ADR_REQUIRED && StringLen(r.adr_id)>0; }
#endif
