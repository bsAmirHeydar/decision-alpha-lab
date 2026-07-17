#ifndef DAL_SAED_V426_PATHWAYS_MQH
#define DAL_SAED_V426_PATHWAYS_MQH
double SAEDV426PathwayShare(const double delta,const double total_abs){ return total_abs>0.0?MathAbs(delta)/total_abs:0.0; }
#endif
