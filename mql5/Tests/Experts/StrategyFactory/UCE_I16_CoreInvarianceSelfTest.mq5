#property strict
#include <AlphaLab/StrategyFactory/ContextOnboarding/UCEI16_All.mqh>
int OnInit(){ UCEI16_InvarianceReport r;r.before_hash=StringInit(64,'a');r.after_hash=StringInit(64,'a');r.status=UCEI16_INVARIANCE_PASS;r.changed_core_count=0;r.adr_id=""; bool boundary=!UCEI16_HasTradingAuthority() && !UCEI16_HasNetworkAuthority(); return (UCEI16_InvarianceAccepted(r) && boundary)?INIT_SUCCEEDED:INIT_FAILED; }
void OnTick(){}
