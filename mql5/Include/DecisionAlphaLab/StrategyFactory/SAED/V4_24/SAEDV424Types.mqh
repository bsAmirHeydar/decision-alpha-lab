#ifndef DECISION_ALPHA_LAB_SAED_V424_TYPES_MQH
#define DECISION_ALPHA_LAB_SAED_V424_TYPES_MQH
enum ENUM_SAED_V424_ACTION { SAED_V424_SKIP=0, SAED_V424_LONG=1, SAED_V424_SHORT=2 };
struct SAEDV424Score { double value_lower; double coverage; double ood_score; double ood_p; double support; };
#endif
