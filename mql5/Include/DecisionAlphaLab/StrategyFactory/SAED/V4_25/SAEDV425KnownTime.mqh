#ifndef __SAED_V4_25_KNOWN_TIME_MQH__
#define __SAED_V4_25_KNOWN_TIME_MQH__
bool SAEDV425KnownTimeValid(const datetime window_start,const datetime feature_known_at,const datetime decision_time,const datetime window_end,const datetime outcome_observed_at){ return window_start<=feature_known_at && feature_known_at<=decision_time && decision_time<=window_end && window_end<=outcome_observed_at; }
bool SAEDV425FutureSourceAllowed(const datetime source_decision_time,const datetime target_decision_time){ return source_decision_time<target_decision_time; }
#endif
