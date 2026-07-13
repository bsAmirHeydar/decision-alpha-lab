#ifndef ALPHALAB_UCEI13_AUTHORITY
#define ALPHALAB_UCEI13_AUTHORITY
#include "UCEI13_Contracts.mqh"
UCEI13Authority UCEI13ResolveAuthority(const bool kill_switch,const bool risk_rejected,const bool manual_veto,const bool operator_veto){if(kill_switch)return UCEI13_KILL;if(risk_rejected)return UCEI13_RISK;if(operator_veto)return UCEI13_OPERATOR;if(manual_veto)return UCEI13_MANUAL;return UCEI13_SYSTEM;}
#endif
