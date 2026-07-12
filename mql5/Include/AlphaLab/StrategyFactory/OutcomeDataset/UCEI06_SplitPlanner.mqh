#ifndef ALPHALAB_UCEI06_SPLIT_PLANNER_MQH
#define ALPHALAB_UCEI06_SPLIT_PLANNER_MQH
#include "UCEI06_Contracts.mqh"
class CUCEI06SplitPlanner{
public:
 UCEI06_FOLD_ROLE Classify(const long decision_time_ms,const long test_start_ms,const long test_end_ms,const long purge_ms,const long embargo_ms)const{if(decision_time_ms>=test_start_ms&&decision_time_ms<=test_end_ms)return UCEI06_FOLD_TEST;if(decision_time_ms>=test_start_ms-purge_ms&&decision_time_ms<test_start_ms)return UCEI06_FOLD_PURGED;if(decision_time_ms>test_end_ms&&decision_time_ms<=test_end_ms+embargo_ms)return UCEI06_FOLD_EMBARGO;if(decision_time_ms<test_start_ms-purge_ms)return UCEI06_FOLD_TRAIN;return UCEI06_FOLD_UNUSED;}
 bool ClusterRolesCompatible(const UCEI06_SplitAssignment &items[])const{int n=ArraySize(items);for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)if(items[i].fold_id==items[j].fold_id&&items[i].dependence_cluster_id==items[j].dependence_cluster_id&&((items[i].role==UCEI06_FOLD_TRAIN&&items[j].role==UCEI06_FOLD_TEST)||(items[i].role==UCEI06_FOLD_TEST&&items[j].role==UCEI06_FOLD_TRAIN)))return false;return true;}
};
#endif
