#ifndef __LCM10C_SAFETY_GUARD_MQH__
#define __LCM10C_SAFETY_GUARD_MQH__
class CLCM10CSafetyGuard { public: bool Allow(const bool kill_switch,const bool quote_present,const bool session_open,const bool reconciliation_ok) const { return (!kill_switch && quote_present && session_open && reconciliation_ok); } };
#endif
