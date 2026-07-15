#ifndef DECISION_ALPHA_LAB_SAED_V410_PROGRAM_MQH
#define DECISION_ALPHA_LAB_SAED_V410_PROGRAM_MQH
#include "SAEDV410Types.mqh"
bool SAEDV410ValidFeatureRef(const string feature_ref){
 if(StringLen(feature_ref)==0)return false;
 string x=feature_ref;StringToLower(x);
 if(StringFind(x,"outcome")>=0 || StringFind(x,"net_r")>=0 || StringFind(x,"future")>=0 || StringFind(x,"live")>=0)return false;
 return StringFind(feature_ref,":")>0;
}
#endif
