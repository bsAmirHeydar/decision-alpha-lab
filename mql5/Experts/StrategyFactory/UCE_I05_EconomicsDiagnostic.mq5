#property strict
#property version "3.050"
#include <AlphaLab/StrategyFactory/Economics/UCEI05_All.mqh>
int OnInit(){ string reason=""; CUCEI05Conformance c; bool ok=c.Run(reason); Print("UCE-I05 economics diagnostic: ",ok?"PASS":"FAIL"," reason=",reason); return ok?INIT_SUCCEEDED:INIT_FAILED; }
void OnTick(){}
