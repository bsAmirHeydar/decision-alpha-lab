#property strict
#include <StrategyFactory/SAED/V4_39/SAEDV439Authority.mqh>
#include <StrategyFactory/SAED/V4_39/SAEDV439ShadowLedger.mqh>
int OnInit(){Print("SAED V4-39 shadow harness; order path disabled.");return(INIT_SUCCEEDED);}void OnTick(){/* shadow decisions only */}
