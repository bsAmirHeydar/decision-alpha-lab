#ifndef ALPHA_LAB_SAED_V4_VIEW_SUPPORT_MQH
#define ALPHA_LAB_SAED_V4_VIEW_SUPPORT_MQH
#include "ViewEnums.mqh"
ENUM_SAED_VIEW_STATUS SAEDViewStatus(const int required_total,const int required_passed,const bool stale,const bool conflict){ if(conflict)return SAED_VIEW_CONFLICTED; if(required_passed<required_total)return SAED_VIEW_UNKNOWN; if(stale)return SAED_VIEW_DEGRADED; return SAED_VIEW_COMPLETE; }
#endif
