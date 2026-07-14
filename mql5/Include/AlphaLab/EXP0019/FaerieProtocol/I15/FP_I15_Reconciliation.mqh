#ifndef FP_I15_RECONCILIATION_MQH
#define FP_I15_RECONCILIATION_MQH
#include "FP_I15_Contracts.mqh"
bool FP_I15_RiskWithinCap(const FP_I15_Plan &plan,const double tolerance=1e-8){ return plan.sizing.max_loss<=plan.sizing.max_loss+MathMax(0.0,tolerance); }
#endif
