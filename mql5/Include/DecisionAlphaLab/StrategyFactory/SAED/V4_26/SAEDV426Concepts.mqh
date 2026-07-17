#ifndef DAL_SAED_V426_CONCEPTS_MQH
#define DAL_SAED_V426_CONCEPTS_MQH
bool SAEDV426ConceptControlPass(const double signal,const double random_control,const double margin){ return MathAbs(signal)-MathAbs(random_control)>=margin; }
#endif
