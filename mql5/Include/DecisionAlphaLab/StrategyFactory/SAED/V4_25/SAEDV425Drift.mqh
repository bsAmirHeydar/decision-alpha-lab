#ifndef __SAED_V4_25_DRIFT_MQH__
#define __SAED_V4_25_DRIFT_MQH__
#include "SAEDV425Types.mqh"
ENUM_SAEDV425_DRIFT_CLASS SAEDV425ClassifyDrift(const double distance,const double recurrence_similarity,const double stationary_threshold,const double gradual_threshold,const double sudden_threshold,const double recurrence_threshold){ if(recurrence_similarity>=recurrence_threshold && distance>stationary_threshold) return SAEDV425_RECURRING; if(distance<=stationary_threshold) return SAEDV425_STATIONARY; if(distance<=gradual_threshold) return SAEDV425_GRADUAL; if(distance<=sudden_threshold) return SAEDV425_SUDDEN; return SAEDV425_NOVEL; }
#endif
