#property strict
#property version "3.050"
#include <AlphaLab/StrategyFactory/Economics/UCEI05_All.mqh>
int OnInit(){string reason="";CUCEI05Conformance c;if(!c.Run(reason)){Print("UCE-I05 FAIL: ",reason);return INIT_FAILED;}Print("UCE-I05 PASS");return INIT_SUCCEEDED;}
void OnTick(){}
