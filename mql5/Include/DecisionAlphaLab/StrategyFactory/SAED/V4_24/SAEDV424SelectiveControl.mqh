#ifndef DECISION_ALPHA_LAB_SAED_V424_SELECTIVECONTROL_MQH
#define DECISION_ALPHA_LAB_SAED_V424_SELECTIVECONTROL_MQH
int SAEDV424Select(const int candidate,const bool conformal_ok,const bool ood_ok,const bool support_ok,const bool mask_ok){ if(!conformal_ok||!ood_ok||!support_ok||!mask_ok)return 0; return candidate; }
#endif
