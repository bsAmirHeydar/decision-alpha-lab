#ifndef __SF18_CIRCUIT_BREAKER_MQH__
#define __SF18_CIRCUIT_BREAKER_MQH__
#include "SF18_KillSwitch.mqh"
class CSF18CircuitBreaker
{
private:int m_maximum,m_failures;long m_cooldown,m_opened_at;ENUM_SF18_CIRCUIT_STATE m_state;string m_reason;
public:
 CSF18CircuitBreaker(){m_maximum=1;m_failures=0;m_cooldown=0;m_opened_at=0;m_state=SF18_CIRCUIT_CLOSED;m_reason="";}
 void Configure(const int maximum,const long cooldown){m_maximum=MathMax(1,maximum);m_cooldown=MathMax((long)0,cooldown);Reset();}
 void Reset(void){m_failures=0;m_opened_at=0;m_state=SF18_CIRCUIT_CLOSED;m_reason="";}
 bool CanAttempt(const long now_utc_msc){if(m_state==SF18_CIRCUIT_CLOSED)return true;if(m_state==SF18_CIRCUIT_OPEN&&now_utc_msc-m_opened_at>=m_cooldown){m_state=SF18_CIRCUIT_HALF_OPEN;return true;}return m_state==SF18_CIRCUIT_HALF_OPEN;}
 bool RecordFailure(const string reason,const long now_utc_msc){m_failures++;m_reason=reason;if(m_failures>=m_maximum){m_state=SF18_CIRCUIT_OPEN;m_opened_at=now_utc_msc;return true;}return false;}
 void RecordSuccess(void){m_failures=0;if(m_state==SF18_CIRCUIT_HALF_OPEN)m_state=SF18_CIRCUIT_CLOSED;}
 ENUM_SF18_CIRCUIT_STATE State(void)const{return m_state;}int Failures(void)const{return m_failures;}
};
#endif
