#property strict
#include <StrategyFactory/SAED/V4_36/SAEDV436Version.mqh>
#include <StrategyFactory/SAED/V4_36/SAEDV436Authority.mqh>
#include <StrategyFactory/SAED/V4_36/SAEDV436StaticAssertions.mqh>
// Static-only contract harness. It never launches research jobs or submits, modifies or cancels orders.
int OnInit(){ return SAED_V4_36_StaticAuthoritySafe() ? INIT_SUCCEEDED : INIT_FAILED; }
void OnTick(){ }
