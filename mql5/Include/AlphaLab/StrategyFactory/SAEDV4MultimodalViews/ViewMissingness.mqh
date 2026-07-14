#ifndef ALPHA_LAB_SAED_V4_VIEW_MISSINGNESS_MQH
#define ALPHA_LAB_SAED_V4_VIEW_MISSINGNESS_MQH
#include "ViewEnums.mqh"
bool SAEDViewMissingAllowed(const ENUM_SAED_MISSING_POLICY policy){ return policy!=SAED_MISSING_PROHIBIT; }
int SAEDViewMask(const bool missing){ return missing ? 1 : 0; }
#endif
