#ifndef DECISION_ALPHA_LAB_SAED_V4_14_QUANTILE_GUARD_MQH
#define DECISION_ALPHA_LAB_SAED_V4_14_QUANTILE_GUARD_MQH
bool SAEDV414QuantilesMonotone(const double &values[]){for(int i=1;i<ArraySize(values);i++)if(values[i]<values[i-1])return false;return true;}
#endif
