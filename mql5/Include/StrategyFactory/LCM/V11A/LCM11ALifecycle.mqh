#ifndef ALPHA_LAB_LCM11A_LIFECYCLE_MQH
#define ALPHA_LAB_LCM11A_LIFECYCLE_MQH
#include "LCM11AVisualTypes.mqh"
bool LCM11A_CanTransition(const ENUM_LCM11A_LIFECYCLE_STATE from_state,const ENUM_LCM11A_LIFECYCLE_STATE to_state){if(to_state==LCM11A_VIS_CLEANED)return true;if(from_state==LCM11A_VIS_UNINITIALIZED&&to_state==LCM11A_VIS_INITIALIZED)return true;if(from_state==LCM11A_VIS_INITIALIZED&&to_state==LCM11A_VIS_BACKFILLED)return true;if((from_state==LCM11A_VIS_BACKFILLED||from_state==LCM11A_VIS_INCREMENTAL)&&to_state==LCM11A_VIS_INCREMENTAL)return true;if(to_state==LCM11A_VIS_RECONCILED)return true;return false;}
#endif
