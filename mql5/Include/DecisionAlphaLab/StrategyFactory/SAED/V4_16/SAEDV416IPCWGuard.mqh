#ifndef SAEDV416_IPCW_MQH
#define SAEDV416_IPCW_MQH
#define SAED_V4_16_PHASE "SAED_V4_16"
bool SAEDV416IPCWValid(const double censor_survival,const double weight,const double floor_value,const double ceiling_value){return censor_survival>=floor_value&&censor_survival<=1.0&&weight>0.0&&weight<=ceiling_value;}
#endif
