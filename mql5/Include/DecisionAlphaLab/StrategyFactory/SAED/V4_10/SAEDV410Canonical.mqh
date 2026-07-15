#ifndef DECISION_ALPHA_LAB_SAED_V410_CANONICAL_MQH
#define DECISION_ALPHA_LAB_SAED_V410_CANONICAL_MQH
string SAEDV410Bool(const bool value){return value?"true":"false";}
string SAEDV410Int(const int value){return IntegerToString(value);}
string SAEDV410Join(const string left,const string right){return left+"|"+right;}
#endif
