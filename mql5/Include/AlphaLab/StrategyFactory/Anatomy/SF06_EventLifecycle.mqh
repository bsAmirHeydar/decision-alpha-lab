#ifndef __SF06_EVENT_LIFECYCLE_MQH__
#define __SF06_EVENT_LIFECYCLE_MQH__
#include "SF06_AnatomyObservation.mqh"
struct SF06_LifecycleRecord
{
   string schema;
   string lifecycle_id;
   string aggregate_id;
   long sequence;
   ENUM_SF06_LIFECYCLE_STATE from_state;
   ENUM_SF06_LIFECYCLE_STATE to_state;
   SF01_MarketTimestamp transition_time;
   string reason_code;
   string source_hash;
   string previous_record_hash;
};
bool SF06_IsLifecycleTransitionAllowed(const ENUM_SF06_LIFECYCLE_STATE a,const ENUM_SF06_LIFECYCLE_STATE b){if(a==SF06_LIFE_UNKNOWN&&b==SF06_LIFE_OBSERVED)return true;if(a==SF06_LIFE_OBSERVED&&(b==SF06_LIFE_CONFIRMED||b==SF06_LIFE_REJECTED))return true;if(a==SF06_LIFE_CONFIRMED&&(b==SF06_LIFE_EMITTED||b==SF06_LIFE_REJECTED))return true;if(a==SF06_LIFE_EMITTED&&b==SF06_LIFE_RETIRED)return true;if(a==SF06_LIFE_REJECTED&&b==SF06_LIFE_RETIRED)return true;return false;}
string SF06_LifecycleCanonical(const SF06_LifecycleRecord &v){return v.schema+"|"+v.aggregate_id+"|"+IntegerToString(v.sequence)+"|"+IntegerToString((int)v.from_state)+"|"+IntegerToString((int)v.to_state)+"|"+IntegerToString(v.transition_time.utc_epoch_milliseconds)+"|"+v.reason_code+"|"+v.source_hash+"|"+v.previous_record_hash;}
string SF06_DeriveLifecycleId(const SF06_LifecycleRecord &v){return SF01_StableId("life",SF06_LifecycleCanonical(v));}
bool SF06_ValidateLifecycleRecord(const SF06_LifecycleRecord &v,string &e){if(v.schema!="alpha_lab.strategy_factory/anatomy_lifecycle@1.0.0"){e="unsupported lifecycle schema";return false;}if(!SF01_IsSafeIdentifier(v.aggregate_id,128)){e="invalid aggregate";return false;}if(v.sequence<1){e="sequence must be positive";return false;}if(!SF06_IsLifecycleTransitionAllowed(v.from_state,v.to_state)){e="illegal lifecycle transition";return false;}if(!SF01_ValidateTimestamp(v.transition_time,e))return false;if(!SF01_IsSafeIdentifier(v.reason_code,128)||!SF01_IsSafeIdentifier(v.source_hash,128)){e="invalid lifecycle lineage";return false;}if(v.sequence>1&&!SF01_IsSafeIdentifier(v.previous_record_hash,128)){e="previous hash required";return false;}string id=SF06_DeriveLifecycleId(v);if(v.lifecycle_id!=""&&v.lifecycle_id!=id){e="lifecycle id mismatch";return false;}e="";return true;}
class CSF06LifecycleTracker
{
private:string m_aggregate_id;long m_sequence;ENUM_SF06_LIFECYCLE_STATE m_state;string m_last_hash;
public:CSF06LifecycleTracker(void){Reset();}void Reset(void){m_aggregate_id="";m_sequence=0;m_state=SF06_LIFE_UNKNOWN;m_last_hash="none";}bool Begin(const string aggregate){if(!SF01_IsSafeIdentifier(aggregate,128))return false;Reset();m_aggregate_id=aggregate;return true;}ENUM_SF06_LIFECYCLE_STATE State(void)const{return m_state;}bool Transition(const ENUM_SF06_LIFECYCLE_STATE next,const SF01_MarketTimestamp &at,const string reason,const string source_hash,SF06_LifecycleRecord &out,string &e){if(!SF06_IsLifecycleTransitionAllowed(m_state,next)){e="illegal transition";return false;}out.schema="alpha_lab.strategy_factory/anatomy_lifecycle@1.0.0";out.lifecycle_id="";out.aggregate_id=m_aggregate_id;out.sequence=m_sequence+1;out.from_state=m_state;out.to_state=next;out.transition_time=at;out.reason_code=reason;out.source_hash=source_hash;out.previous_record_hash=(m_sequence==0)?"none":m_last_hash;out.lifecycle_id=SF06_DeriveLifecycleId(out);if(!SF06_ValidateLifecycleRecord(out,e))return false;m_sequence++;m_state=next;m_last_hash=out.lifecycle_id;e="";return true;}
};
#endif
