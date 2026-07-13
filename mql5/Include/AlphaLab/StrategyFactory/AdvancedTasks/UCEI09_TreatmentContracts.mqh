#ifndef __UCEI09_TREATMENT_CONTRACTS_MQH__
#define __UCEI09_TREATMENT_CONTRACTS_MQH__
#include "UCEI09_Enums.mqh"
struct UCEI09_ActionMask{string mask_id;string opportunity_id;string allowed_action_keys[];long known_time_ms;string evidence_hash;bool Allows(const string key)const{for(int i=0;i<ArraySize(allowed_action_keys);i++)if(allowed_action_keys[i]==key)return true;return false;}bool Valid()const{return mask_id!="" && opportunity_id!="" && known_time_ms>=0 && evidence_hash!="";}};
struct UCEI09_TreatmentChoice{string prediction_id;string row_id;string chosen_action_key;UCEI09_POLICY_DECISION decision;string reason;string evidence_hash;bool Valid(const UCEI09_ActionMask &mask)const{return prediction_id!="" && row_id!="" && evidence_hash!="" && (decision!=UCEI09_ACTION || mask.Allows(chosen_action_key));}};
struct UCEI09_TreatmentSupportEntry{string action_key;int count;double effective_sample_size;double minimum_propensity;UCEI09_SUPPORT_STATE state;string reason;};
#endif
