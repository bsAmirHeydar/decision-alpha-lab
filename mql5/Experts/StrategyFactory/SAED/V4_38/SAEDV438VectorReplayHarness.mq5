#property strict
#include <StrategyFactory/SAED/V4_38/SAEDV438CompiledRuntime.mqh>
// SAED_V4_38 research-only deterministic vector replay harness.
int OnInit(){Print("SAED V4-38 vector replay harness loaded; no order authority.");return(INIT_SUCCEEDED);}
void OnTick(){/* replay is invoked by explicit test script; no trading */}
