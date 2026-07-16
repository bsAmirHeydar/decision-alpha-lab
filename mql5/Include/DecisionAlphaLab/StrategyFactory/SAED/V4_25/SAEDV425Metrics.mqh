#ifndef __SAED_V4_25_METRICS_MQH__
#define __SAED_V4_25_METRICS_MQH__
double SAEDV425UtilityDelta(const double baseline_utility,const double transfer_utility){ return transfer_utility-baseline_utility; }
double SAEDV425Forgetting(const double frozen_baseline,const double after_value){ return MathMax(0.0,frozen_baseline-after_value); }
#endif
