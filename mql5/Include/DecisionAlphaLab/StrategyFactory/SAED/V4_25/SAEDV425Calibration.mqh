#ifndef __SAED_V4_25_CALIBRATION_MQH__
#define __SAED_V4_25_CALIBRATION_MQH__
bool SAEDV425CalibrationReady(const int residual_count,const int minimum_residuals){ return residual_count>=minimum_residuals; }
bool SAEDV425CalibrationMayUseCurrentOutcome(){ return false; }
bool SAEDV425CalibrationMayMutateRuntime(){ return false; }
#endif
