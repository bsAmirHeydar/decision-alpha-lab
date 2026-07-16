#property strict
#ifndef __DECISION_ALPHA_LAB_SAEDV420CALIBRATION_MQH__
#define __DECISION_ALPHA_LAB_SAEDV420CALIBRATION_MQH__
#define SAED_V4_20_PHASE "SAED_V4_20"
double SAEDV420ClampProbability(const double p){ return MathMax(0.0,MathMin(1.0,p)); }
#endif
