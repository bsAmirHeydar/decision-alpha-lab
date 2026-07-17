#ifndef SAED_V4_38_STATE_MACHINE_MQH
#define SAED_V4_38_STATE_MACHINE_MQH
#include "SAEDV438Types.mqh"
void SAEDV438AdvanceState(SAEDV438State &s){s.sequence++;if(s.cooldown_bars>0)s.cooldown_bars--;}
#endif
