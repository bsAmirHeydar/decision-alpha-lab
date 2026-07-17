#property strict
#include <StrategyFactory/SAED/V4_38/SAEDV438CompiledRuntime.mqh>
// SAED_V4_38 parity harness only. No orders, no capital activation.
int OnInit(){Print("SAED V4-38 research-only parity harness: ",SAED_V4_38_BUNDLE_HASH);return(INIT_SUCCEEDED);}
void OnTick(){/* intentionally non-executable */}
