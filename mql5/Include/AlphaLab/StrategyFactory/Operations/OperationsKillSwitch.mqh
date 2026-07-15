#ifndef ALPHALAB_OPERATIONS_KILL_SWITCH_MQH
#define ALPHALAB_OPERATIONS_KILL_SWITCH_MQH
class ALOperationsKillSwitch { private: bool m_engaged; string m_reason; long m_engaged_at_ms; public: ALOperationsKillSwitch(void){m_engaged=true;m_reason="uninitialized";m_engaged_at_ms=0;} void Engage(const string reason,const long now_ms){m_engaged=true;m_reason=reason;m_engaged_at_ms=now_ms;} bool ReleaseAfterExternalApproval(const bool approval_valid,const bool reconciliation_exact){ if(!approval_valid||!reconciliation_exact) return false; m_engaged=false;m_reason="";return true;} bool Engaged(void) const{return m_engaged;} string Reason(void) const{return m_reason;} long EngagedAtMs(void) const{return m_engaged_at_ms;} };
#endif
