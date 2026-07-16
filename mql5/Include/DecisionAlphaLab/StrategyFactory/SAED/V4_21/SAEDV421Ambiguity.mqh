#ifndef __DECISION_ALPHA_LAB_SAEDV421AMBIGUITY_MQH__
#define __DECISION_ALPHA_LAB_SAEDV421AMBIGUITY_MQH__
double SAEDV421L1Distance(const double &a[],const double &b[]){double s=0.0;int n=MathMin(ArraySize(a),ArraySize(b));for(int i=0;i<n;i++)s+=MathAbs(a[i]-b[i]);return s;}
#endif
