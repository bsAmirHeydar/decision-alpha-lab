#ifndef ALPHALAB_UCEI07_RESOURCE_GUARD_MQH
#define ALPHALAB_UCEI07_RESOURCE_GUARD_MQH
#include "UCEI07_Contracts.mqh"
class CUCEI07ResourceGuard{
private:long m_started_us;bool m_cancelled;
public:
 CUCEI07ResourceGuard(){m_started_us=0;m_cancelled=false;}
 bool Start(const UCEI07_ResourceBudget &b,const UCEI07_DatasetSchema &s,string &reason){reason="";if(b.max_rows<1||b.max_features<1||b.max_outputs<1||b.max_memory_mb<1||b.max_wall_ms<1){reason="invalid_budget";return false;}if(s.row_count>b.max_rows){reason="row_budget_exceeded";return false;}if(s.feature_count>b.max_features){reason="feature_budget_exceeded";return false;}if(s.output_count>b.max_outputs){reason="output_budget_exceeded";return false;}m_started_us=GetMicrosecondCount();m_cancelled=false;return true;}
 void Cancel(){m_cancelled=true;}
 bool Poll(const UCEI07_ResourceBudget &b,string &reason)const{reason="";if(m_cancelled){reason="cancelled";return false;}long elapsed_ms=(GetMicrosecondCount()-m_started_us)/1000;if(elapsed_ms>b.max_wall_ms){reason="wall_time_exceeded";return false;}return true;}
};
#endif
