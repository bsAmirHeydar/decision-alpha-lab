#ifndef __SAED_V4_25_CANONICAL_MQH__
#define __SAED_V4_25_CANONICAL_MQH__
bool SAEDV425IsFinite(const double value){ return MathIsValidNumber(value); }
bool SAEDV425NonEmpty(const string value){ return StringLen(value)>0; }
double SAEDV425Clamp(const double value,const double lower,const double upper){ if(value<lower) return lower; if(value>upper) return upper; return value; }
#endif
