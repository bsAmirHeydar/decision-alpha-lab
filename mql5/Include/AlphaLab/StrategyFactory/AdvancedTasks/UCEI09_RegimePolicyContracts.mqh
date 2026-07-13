#ifndef __UCEI09_REGIME_POLICY_CONTRACTS_MQH__
#define __UCEI09_REGIME_POLICY_CONTRACTS_MQH__
#include "UCEI09_Enums.mqh"
struct UCEI09_ExpertGateResult{string result_id;string row_id;string selected_expert_key;bool global_model_used;string regime_id;int support_count;UCEI09_GATE_DECISION decision;string reason;string evidence_hash;};
struct UCEI09_PolicyActionScore{string action_key;double mean_utility;double uncertainty;double conservative_value;int support_count;UCEI09_SUPPORT_STATE support_state;};
struct UCEI09_ConservativePolicyDecision{string decision_id;string row_id;UCEI09_PolicyActionScore scores[];string selected_action_key;string baseline_action_key;UCEI09_POLICY_DECISION decision;double improvement_lower_bound;string reason;string evidence_hash;bool UsesDeclaredAction(const string declared[])const{for(int i=0;i<ArraySize(declared);i++)if(declared[i]==selected_action_key)return true;return decision==UCEI09_ABSTAIN;} };
#endif
