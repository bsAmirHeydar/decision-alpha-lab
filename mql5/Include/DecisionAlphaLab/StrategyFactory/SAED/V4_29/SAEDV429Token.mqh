#ifndef SAED_V4_29_TOKEN_MQH
#define SAED_V4_29_TOKEN_MQH
#include "SAEDV429Types.mqh"
bool SAEDV429CanConsume(const SAEDV429Token &t){ return !t.revoked && t.maximum_uses==1 && t.used_count==0; }
#endif
