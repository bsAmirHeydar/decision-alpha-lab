#ifndef __FP_I06_FIRST_SWEEP_CLASSIFIER_MQH__
#define __FP_I06_FIRST_SWEEP_CLASSIFIER_MQH__
#include "FP_I06_HuntAdapter.mqh"
class FP_I06_FirstSweepClassifier { public: static FP_I06_SWEEP_OUTCOME Outcome(FP_I06_CONTACT_STATE s){if(s==FP_I06_LEFT_ONLY)return FP_I06_LEFT_FIRST;if(s==FP_I06_RIGHT_ONLY)return FP_I06_RIGHT_FIRST;if(s==FP_I06_BOTH_SAME_M1)return FP_I06_SYMMETRIC_SAME_M1;if(s==FP_I06_DATA_BLOCKED)return FP_I06_SWEEP_DATA_BLOCKED;return FP_I06_NO_CONTACT;} static bool AssignRoles(FP_I06_CONTACT_STATE s,string left_symbol,string right_symbol,string &hunter,string &protected_symbol){hunter="";protected_symbol="";if(s==FP_I06_LEFT_ONLY){hunter=left_symbol;protected_symbol=right_symbol;return true;}if(s==FP_I06_RIGHT_ONLY){hunter=right_symbol;protected_symbol=left_symbol;return true;}return false;} };
#endif
