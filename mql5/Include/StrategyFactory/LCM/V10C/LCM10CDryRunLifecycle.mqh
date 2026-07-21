#ifndef __LCM10C_DRY_RUN_LIFECYCLE_MQH__
#define __LCM10C_DRY_RUN_LIFECYCLE_MQH__
#include "LCM10CTypes.mqh"
#include "LCM10CSafetyGuard.mqh"
#include "LCM10CAuthorityNegative.mqh"
class CLCM10CDryRunLifecycle { private: CLCM10CSafetyGuard m_guard; CLCM10CAuthorityNegative m_authority; public: LCM10CReceipt Replay(const string request_id,const bool kill_switch,const bool quote_present,const bool session_open,const bool reconciliation_ok) { LCM10CReceipt r; r.request_id=request_id; r.rejection_count=0; r.submission_attempt_count=0; r.live_order_count=0; r.capital_activation_count=0; if(!m_guard.Allow(kill_switch,quote_present,session_open,reconciliation_ok)){r.final_state=LCM10C_REJECTED;r.rejection_count=1;return r;} if(m_authority.SubmissionEnabled()){r.final_state=LCM10C_REJECTED;r.rejection_count=1;return r;} r.final_state=LCM10C_EXECUTION_BLOCKED; return r; } };
#endif
