#property strict
#include <AlphaLab/StrategyFactory/HybridPolicy/UCEI13_All.mqh>
int OnInit(){UCEI13ManualDecision m;m.eligible=true;m.vetoed=false;m.action="enter_long";m.treatment="market";m.risk_tier="standard";UCEI13ModelOutput x;x.valid=false;x.stale=true;x.ood=false;x.low_confidence=false;x.missing_view=false;UCEI13Decision d=UCEI13Resolve(m,x,false,false,false,false);return(d.status==UCEI13_APPROVED&&d.authority==UCEI13_MANUAL&&d.treatment=="market")?INIT_SUCCEEDED:INIT_FAILED;}
void OnTick(){}
