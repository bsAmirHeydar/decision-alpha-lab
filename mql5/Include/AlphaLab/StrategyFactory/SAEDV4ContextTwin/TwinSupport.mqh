#ifndef AL_SAED_V4_02_TWIN_SUPPORT_MQH
#define AL_SAED_V4_02_TWIN_SUPPORT_MQH
#include "TwinEnums.mqh"
int ALTwinSupportStatus(const double coverage,const double minimum_coverage,const double degraded_threshold,const bool required_missing,const bool required_failed){if(required_failed)return AL_SUPPORT_UNSUPPORTED;if(required_missing)return AL_SUPPORT_UNKNOWN;if(coverage>=minimum_coverage)return AL_SUPPORT_SUPPORTED;if(coverage>=degraded_threshold)return AL_SUPPORT_DEGRADED;return AL_SUPPORT_UNSUPPORTED;}
#endif
