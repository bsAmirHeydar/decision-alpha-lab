#ifndef DECISION_ALPHA_LAB_SAED_V4_14_DOMAIN_SHIFT_GUARD_MQH
#define DECISION_ALPHA_LAB_SAED_V4_14_DOMAIN_SHIFT_GUARD_MQH
bool SAEDV414DomainSupported(const double mean_shift,const double scale_ratio,const double missing_rate,const double max_mean_shift,const double max_scale_ratio,const double max_missing_rate){return mean_shift<=max_mean_shift && scale_ratio<=max_scale_ratio && missing_rate<=max_missing_rate;}
#endif
