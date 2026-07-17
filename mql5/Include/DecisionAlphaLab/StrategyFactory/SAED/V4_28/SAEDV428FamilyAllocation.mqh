#ifndef SAED_V4_28_FAMILY_ALLOCATION_MQH
#define SAED_V4_28_FAMILY_ALLOCATION_MQH
double SAEDV428FamilyTarget(const double global_q,const double weight){ if(weight<0.0 || weight>1.0) return 0.0; return global_q*weight; }
#endif
