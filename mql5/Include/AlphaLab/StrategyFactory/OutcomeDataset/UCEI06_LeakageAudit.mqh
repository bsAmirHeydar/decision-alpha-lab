#ifndef ALPHALAB_UCEI06_LEAKAGE_AUDIT_MQH
#define ALPHALAB_UCEI06_LEAKAGE_AUDIT_MQH
#include "UCEI06_Contracts.mqh"
#include "UCEI06_SplitPlanner.mqh"
class CUCEI06LeakageAudit{
public:
 bool AuditKnownTime(const UCEI06_OpportunityAnchor &a,string &reason)const{reason="";if(a.event_time_ms>a.decision_time_ms||a.decision_time_ms>a.known_time_ms){reason="anchor_time_order";return false;}return true;}
 bool AuditSplit(const UCEI06_SplitAssignment &items[],string &reason)const{reason="";CUCEI06SplitPlanner p;if(!p.ClusterRolesCompatible(items)){reason="cluster_crosses_train_test";return false;}return true;}
 bool AuditRebuild(const string hash_a,const string hash_b,string &reason)const{reason="";if(hash_a!=hash_b){reason="non_reproducible_dataset";return false;}return true;}
};
#endif
