#ifndef __FP_I06_HUNT_ADAPTER_MQH__
#define __FP_I06_HUNT_ADAPTER_MQH__
#include "FP_I06_Contracts.mqh"
class FP_I06_HuntAdapter { public: static bool Contact(FP_I06_PRICE_SIDE side,double bar_high,double bar_low,double reference_price){if(!MathIsValidNumber(bar_high)||!MathIsValidNumber(bar_low)||!MathIsValidNumber(reference_price))return false;return side==FP_I06_HIGH ? bar_high>=reference_price : bar_low<=reference_price;} static FP_I06_CONTACT_STATE ContactState(bool left,bool right,bool data_ok=true){if(!data_ok)return FP_I06_DATA_BLOCKED;if(left&&right)return FP_I06_BOTH_SAME_M1;if(left)return FP_I06_LEFT_ONLY;if(right)return FP_I06_RIGHT_ONLY;return FP_I06_NONE;} };
#endif
