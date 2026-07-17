#property strict
#include <StrategyFactory/SAED/V4_39/SAEDV439Authority.mqh>
#include <StrategyFactory/SAED/V4_39/SAEDV439QualificationGate.mqh>
#include <StrategyFactory/SAED/V4_39/SAEDV439KillSwitch.mqh>
int OnInit(){Print("SAED V4-39 micro-live qualification scaffold loaded; live order submission is disabled in reference build.");return(INIT_SUCCEEDED);}void OnTick(){/* external qualification only; no order API */}
