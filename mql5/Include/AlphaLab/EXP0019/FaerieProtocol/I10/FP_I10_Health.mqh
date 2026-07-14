#ifndef __FP_I10_HEALTH_MQH__
#define __FP_I10_HEALTH_MQH__
#include "FP_I10_Contracts.mqh"
ENUM_FP_I10_HEALTH FP_I10_AggregateHealth(const ENUM_FP_I10_LIFECYCLE lifecycle,const ENUM_FP_I10_DATA_READINESS data,const bool history_ready,const int lag){
 if(lifecycle==FP_I10_BLOCKED||lifecycle==FP_I10_STOPPED||data==FP_I10_DATA_BLOCKED) return FP_I10_HEALTH_BLOCKED;
 if(lifecycle==FP_I10_INITIALIZING||lifecycle==FP_I10_DEGRADED||!history_ready||data==FP_I10_DATA_PARTIAL||lag>0) return FP_I10_HEALTH_DEGRADED;
 return FP_I10_HEALTH_READY;
}
#endif
