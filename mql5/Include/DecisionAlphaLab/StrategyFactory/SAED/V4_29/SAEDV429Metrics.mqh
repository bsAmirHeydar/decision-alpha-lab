#ifndef SAED_V4_29_METRICS_MQH
#define SAED_V4_29_METRICS_MQH
double SAEDV429BalancedAccuracy(const double tpr,const double tnr){ return 0.5*(tpr+tnr); }
double SAEDV429Brier(const double prediction,const double label){ double d=prediction-label; return d*d; }
#endif
