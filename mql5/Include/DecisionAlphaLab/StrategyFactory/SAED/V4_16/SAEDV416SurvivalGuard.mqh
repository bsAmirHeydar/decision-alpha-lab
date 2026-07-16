#ifndef SAEDV416_SURVIVAL_MQH
#define SAEDV416_SURVIVAL_MQH
#define SAED_V4_16_PHASE "SAED_V4_16"
bool SAEDV416SurvivalCurveValid(const double &values[]){for(int i=0;i<ArraySize(values);i++){if(values[i]<0.0||values[i]>1.0)return false;if(i>0&&values[i]>values[i-1])return false;}return true;}
#endif
