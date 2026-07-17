#ifndef SAED_V4_39_KILL_SWITCH_MQH
#define SAED_V4_39_KILL_SWITCH_MQH
struct SAEDV439KillSwitch { bool armed; bool tripped; string reason; datetime tripped_at; };
void SAEDV439Trip(SAEDV439KillSwitch &k,const string reason){k.armed=true;k.tripped=true;k.reason=reason;k.tripped_at=TimeCurrent();}
bool SAEDV439OrderPathDisabled(const SAEDV439KillSwitch &k){return true;}
#endif
