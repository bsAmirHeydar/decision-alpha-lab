#property strict
#include <StrategyFactory/SAED/V4_34/SAEDV434Version.mqh>
#include <StrategyFactory/SAED/V4_34/SAEDV434Authority.mqh>
#include <StrategyFactory/SAED/V4_34/SAEDV434StaticAssertions.mqh>
// SAED_V4_34 static-only parity harness. It never submits orders.
int OnInit(){ return SAED_V4_34_StaticAuthoritySafe() ? INIT_SUCCEEDED : INIT_FAILED; }
void OnTick(){ }
