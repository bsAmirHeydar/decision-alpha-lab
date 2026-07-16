#ifndef SAEDV416_QUANTILE_MQH
#define SAEDV416_QUANTILE_MQH
#define SAED_V4_16_PHASE "SAED_V4_16"
bool SAEDV416QuantilesMonotone(const double &values[]){for(int i=1;i<ArraySize(values);i++)if(values[i]<values[i-1])return false;return true;}
#endif
