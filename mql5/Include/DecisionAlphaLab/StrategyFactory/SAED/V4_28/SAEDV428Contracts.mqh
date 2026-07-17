#ifndef SAED_V4_28_CONTRACTS_MQH
#define SAED_V4_28_CONTRACTS_MQH
bool SAEDV428ValidProbability(const double value){ return MathIsValidNumber(value) && value>=0.0 && value<=1.0; }
bool SAEDV428ValidEValue(const double value){ return MathIsValidNumber(value) && value>=0.0; }
#endif
