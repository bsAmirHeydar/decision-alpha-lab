#ifndef __DECISION_ALPHA_LAB_SAEDV421ALLOCATIONS_MQH__
#define __DECISION_ALPHA_LAB_SAEDV421ALLOCATIONS_MQH__
bool SAEDV421WeightsValid(const double &weights[],const double tolerance=1e-9){double s=0.0;for(int i=0;i<ArraySize(weights);i++){if(weights[i]<0.0)return false;s+=weights[i];}return MathAbs(s-1.0)<=tolerance;}
#endif
