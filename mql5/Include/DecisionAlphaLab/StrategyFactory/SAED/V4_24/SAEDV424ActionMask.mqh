#ifndef DECISION_ALPHA_LAB_SAED_V424_ACTIONMASK_MQH
#define DECISION_ALPHA_LAB_SAED_V424_ACTIONMASK_MQH
bool SAEDV424MaskAllows(const bool allow_skip,const bool allow_long,const bool allow_short,const int action){ if(action==0)return allow_skip; if(action==1)return allow_long; if(action==2)return allow_short; return false; }
#endif
