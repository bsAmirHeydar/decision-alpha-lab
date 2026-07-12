#ifndef ALPHALAB_UCEI06_ANCHOR_MQH
#define ALPHALAB_UCEI06_ANCHOR_MQH
#include "UCEI06_Contracts.mqh"
#include "UCEI06_Identity.mqh"
class CUCEI06OpportunityAnchorBuilder{
public:
 bool Validate(const UCEI06_OpportunityAnchor &a,string &reason)const{reason="";if(a.context_occurrence_id==""||a.dependence_cluster_id==""||a.feature_frame_hash==""){reason="missing_identity_field";return false;}if(a.event_time_ms>a.decision_time_ms||a.decision_time_ms>a.known_time_ms){reason="invalid_known_time_order";return false;}return true;}
 string BuildIdentity(const UCEI06_OpportunityAnchor &a)const{string m=a.context_package_key+"|"+a.context_occurrence_id+"|"+a.dependence_cluster_id+"|"+a.symbol+"|"+IntegerToString((long)a.timeframe)+"|"+IntegerToString((long)a.side)+"|"+IntegerToString(a.decision_time_ms)+"|"+a.feature_frame_hash;return UCEI06_StableId("uceopp",m);}
};
#endif
