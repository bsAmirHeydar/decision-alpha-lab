#property strict
#include <AlphaLab/StrategyFactory/ImmutableRuntime/UCEI14_All.mqh>
int OnInit(){UCEI14Input x;x.request_id="r";x.occurrence_id="o";x.symbol="EURUSD";x.score=0.8;x.direction="long";x.liquidity=0.8;x.blocked=false;string reason;return(UCEI14ParityVector(x,0.99116361,"enter_long",reason)?INIT_SUCCEEDED:INIT_FAILED);}
void OnTick(){}
