#ifndef SAED_V4_29_EVALUATOR_MQH
#define SAED_V4_29_EVALUATOR_MQH
double SAEDV429Sigmoid(const double x){ if(x>=0.0){ double z=MathExp(-x); return 1.0/(1.0+z); } double z=MathExp(x); return z/(1.0+z); }
#endif
