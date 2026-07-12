#property strict
#property version "3.050"
#include <AlphaLab/StrategyFactory/Economics/UCEI05_All.mqh>
int OnInit(){
 UCEI05_QuoteSnapshot q;q.symbol="EURUSD";q.bid=1.10000;q.ask=1.10010;q.known_time_ms=1; UCEI05_SymbolSpec s;s.point=0.00001;s.tick_size=0.00001;CUCEI05ExecutablePriceKernel k;double lp,sp;string side;
 k.Compute(q,s,UCEI05_SIDE_LONG,UCEI05_ROLE_ENTRY,UCEI05_ORDER_MARKET,0,false,0,lp,side);k.Compute(q,s,UCEI05_SIDE_SHORT,UCEI05_ROLE_ENTRY,UCEI05_ORDER_MARKET,0,false,0,sp,side);
 if(MathAbs(lp-q.ask)>1e-10||MathAbs(sp-q.bid)>1e-10)return INIT_FAILED;Print("UCE-I05 long/short executable-side PASS");return INIT_SUCCEEDED;}
void OnTick(){}
