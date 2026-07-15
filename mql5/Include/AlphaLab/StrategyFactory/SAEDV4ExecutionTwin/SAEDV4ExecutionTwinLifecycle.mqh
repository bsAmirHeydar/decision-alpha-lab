#ifndef __SAED_V4_EXECUTION_TWIN_LIFECYCLE_MQH__
#define __SAED_V4_EXECUTION_TWIN_LIFECYCLE_MQH__
bool SAEDV409LifecycleTransitionAllowed(const int from_state,const int to_state){return to_state>=from_state;}
#endif
