#property strict
#property script_show_inputs
#include <StrategyFactory/LCM/V10C/LCM10CDryRunLifecycle.mqh>
void OnStart(){ CLCM10CDryRunLifecycle h; LCM10CReceipt r=h.Replay("LCM10C_REFERENCE",false,true,true,true); PrintFormat("LCM10C final=%d submissions=%d live=%d capital=%d",(int)r.final_state,r.submission_attempt_count,r.live_order_count,r.capital_activation_count); }
