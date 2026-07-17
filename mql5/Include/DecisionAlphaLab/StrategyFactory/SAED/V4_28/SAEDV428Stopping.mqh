#ifndef SAED_V4_28_STOPPING_MQH
#define SAED_V4_28_STOPPING_MQH
bool SAEDV428LookBudgetValid(const int known_looks,const int maximum_looks){ return known_looks>=1 && known_looks<=maximum_looks; }
#endif
