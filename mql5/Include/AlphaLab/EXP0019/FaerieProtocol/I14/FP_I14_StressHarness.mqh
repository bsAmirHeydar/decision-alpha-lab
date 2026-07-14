#ifndef __FP_I14_STRESS_HARNESS_MQH__
#define __FP_I14_STRESS_HARNESS_MQH__
bool FP_I14_ShouldDuplicate(const long sequence,const int every){return every>0 && sequence%every==0;}
bool FP_I14_IsReconnectBoundary(const long sequence,const long boundary){return boundary>0 && sequence==boundary;}
#endif
