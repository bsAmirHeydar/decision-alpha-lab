#ifndef SAEDV422_INVARIANTS_MQH
#define SAEDV422_INVARIANTS_MQH
#include "SAEDV422Types.mqh"
bool SAEDV422PointValid(const SAEDV422PathPoint &p){return p.low<=MathMin(p.open,p.close)&&MathMax(p.open,p.close)<=p.high&&p.bid<=p.ask&&p.close>0&&p.volume>=0&&p.liquidity>=0&&p.liquidity<=1;}
#endif
