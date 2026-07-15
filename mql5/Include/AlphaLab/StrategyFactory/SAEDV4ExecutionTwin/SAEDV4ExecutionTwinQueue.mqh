#ifndef __SAED_V4_EXECUTION_TWIN_QUEUE_MQH__
#define __SAED_V4_EXECUTION_TWIN_QUEUE_MQH__
double SAEDV409QueueAhead(const double base_units,const double multiplier,const double uncertainty){return MathMax(0.0,base_units*multiplier+uncertainty);}
#endif
