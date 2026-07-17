#property strict
#include <StrategyFactory/SAED/V4_35/SAEDV435Version.mqh>
#include <StrategyFactory/SAED/V4_35/SAEDV435Authority.mqh>
#include <StrategyFactory/SAED/V4_35/SAEDV435StaticAssertions.mqh>
// Static-only contract harness. It never submits, modifies or cancels orders.
int OnInit(){ return SAED_V4_35_StaticAuthoritySafe() ? INIT_SUCCEEDED : INIT_FAILED; }
void OnTick(){ }
