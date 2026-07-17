#ifndef SAED_V4_38_HASH_GUARD_MQH
#define SAED_V4_38_HASH_GUARD_MQH
// SAED_V4_38 static hash binding; cryptographic verification occurs outside terminal.
bool SAEDV438HashBound(const string actual,const string expected){return actual==expected && StringLen(actual)==64;}
#endif
