#ifndef DECISION_ALPHA_LAB_SAED_V424_CALIBRATION_MQH
#define DECISION_ALPHA_LAB_SAED_V424_CALIBRATION_MQH
double SAEDV424DownsideResidual(const double predicted,const double realized){ return MathMax(0.0,predicted-realized); }
#endif
