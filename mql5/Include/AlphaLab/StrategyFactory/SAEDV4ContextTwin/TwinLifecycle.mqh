#ifndef AL_SAED_V4_02_TWIN_LIFECYCLE_MQH
#define AL_SAED_V4_02_TWIN_LIFECYCLE_MQH
#include "TwinEnums.mqh"
int ALTwinTransitionDisposition(const bool from_ok,const bool trigger_ok,const bool observables_ok,const bool support_ok,const bool contradiction_ok,const bool review_required){if(!from_ok||!trigger_ok||!observables_ok||!support_ok||!contradiction_ok)return AL_TRANSITION_REJECTED;if(review_required)return AL_TRANSITION_REVIEW;return AL_TRANSITION_APPLIED;}
#endif
