#ifndef ALPHA_LAB_LCM11A_ANCHOR_SEMANTICS_MQH
#define ALPHA_LAB_LCM11A_ANCHOR_SEMANTICS_MQH
#include "LCM11AVisualTypes.mqh"
bool LCM11A_AnchorReady(const SLCM11A_AnchorContract &anchor){if(!anchor.availability_confirmed)return false;if(anchor.kind==LCM11A_ANCHOR_UNKNOWN)return false;return true;}
#endif
