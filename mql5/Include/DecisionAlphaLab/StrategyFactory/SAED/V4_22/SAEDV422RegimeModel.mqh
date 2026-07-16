#ifndef SAEDV422_REGIME_MODEL_MQH
#define SAEDV422_REGIME_MODEL_MQH
double SAEDV422TransitionProbability(const double count,const double total,const int states){return (count+1.0)/(total+MathMax(states,1));}
#endif
