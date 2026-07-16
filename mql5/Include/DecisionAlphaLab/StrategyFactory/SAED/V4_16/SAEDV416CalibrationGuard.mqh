#ifndef SAEDV416_CALIBRATION_MQH
#define SAEDV416_CALIBRATION_MQH
#define SAED_V4_16_PHASE "SAED_V4_16"
bool SAEDV416ProbabilityValid(const double value){return value>=0.0&&value<=1.0;} bool SAEDV416CalibrationErrorValid(const double value){return value>=0.0&&value<=1.0;}
#endif
