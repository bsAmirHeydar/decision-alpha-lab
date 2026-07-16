#ifndef SAEDV415_SUPPORT_GUARD_MQH
#define SAEDV415_SUPPORT_GUARD_MQH
// SAED_V4_15 required/critical support guard.
int SAEDV415SupportDirective(const bool required_ok,const bool critical_ok,const bool corrupt){ if(corrupt)return 5; if(!critical_ok || !required_ok)return 2; return 0; }
#endif
