#ifndef __SF18_KILL_SWITCH_MQH__
#define __SF18_KILL_SWITCH_MQH__
#include "SF18_DryRunBrokerAdapter.mqh"
class CSF18KillSwitch
{
private:ENUM_SF18_KILL_SWITCH_STATE m_state;string m_reason;long m_changed_at;
public:
 CSF18KillSwitch(){m_state=SF18_KILL_ENGAGED;m_reason="startup-default";m_changed_at=0;}
 void Engage(const string reason,const long now_utc_msc){m_state=SF18_KILL_ENGAGED;m_reason=reason==""?"operator":reason;m_changed_at=now_utc_msc;}
 bool Disarm(const SF18_LiveAuthorization &a,const long now_utc_msc){string error;if(!SF18_ValidateAuthorization(a,error)||a.mode!=SF18_LIVE_MICRO||now_utc_msc>a.expires_at_utc_msc)return false;m_state=SF18_KILL_DISARMED;m_reason="authorized";m_changed_at=now_utc_msc;return true;}
 bool Engaged(void)const{return m_state==SF18_KILL_ENGAGED;}ENUM_SF18_KILL_SWITCH_STATE State(void)const{return m_state;}string Reason(void)const{return m_reason;}
};
#endif
