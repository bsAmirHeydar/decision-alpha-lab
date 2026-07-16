#ifndef __DECISION_ALPHA_LAB_SAEDV421ROBUSTUTILITY_MQH__
#define __DECISION_ALPHA_LAB_SAEDV421ROBUSTUTILITY_MQH__
double SAEDV421WorstCase(const double &values[]){if(ArraySize(values)==0)return 0.0;double x=values[0];for(int i=1;i<ArraySize(values);i++)x=MathMin(x,values[i]);return x;}
#endif
