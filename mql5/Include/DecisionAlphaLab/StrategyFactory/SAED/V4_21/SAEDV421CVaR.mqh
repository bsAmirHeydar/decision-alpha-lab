#ifndef __DECISION_ALPHA_LAB_SAEDV421CVAR_MQH__
#define __DECISION_ALPHA_LAB_SAEDV421CVAR_MQH__
double SAEDV421LowerTailMean(const double &sorted_values[],const int count){if(count<=0)return 0.0;double s=0.0;for(int i=0;i<count && i<ArraySize(sorted_values);i++)s+=sorted_values[i];return s/count;}
#endif
