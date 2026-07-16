#ifndef DECISION_ALPHA_LAB_SAED_V424_PVALUE_MQH
#define DECISION_ALPHA_LAB_SAED_V424_PVALUE_MQH
double SAEDV424EmpiricalPValue(const int greater_equal,const int count){ return count>=0?(1.0+greater_equal)/(1.0+count):0.0; }
#endif
