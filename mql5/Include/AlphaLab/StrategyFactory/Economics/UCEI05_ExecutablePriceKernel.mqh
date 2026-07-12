#ifndef UCEI05_EXECUTABLE_PRICE_KERNEL_MQH
#define UCEI05_EXECUTABLE_PRICE_KERNEL_MQH
#include "UCEI05_Contracts.mqh"
class CUCEI05ExecutablePriceKernel {
public:
 double RoundTick(const double price,const double tick,const bool round_up) const { if(tick<=0.0) return price; double units=price/tick; return (round_up?MathCeil(units-1e-12):MathFloor(units+1e-12))*tick; }
 bool Compute(const UCEI05_QuoteSnapshot &q,const UCEI05_SymbolSpec &s,const int side,const int role,const int order_kind,const double logical_price,const bool has_logical,const double slippage_points,double &out_price,string &quote_side) const {
   bool entry=(role==UCEI05_ROLE_ENTRY); bool adverse_up=((entry && side==UCEI05_SIDE_LONG)||(!entry && side==UCEI05_SIDE_SHORT));
   double base=has_logical?logical_price:(entry?(side==UCEI05_SIDE_LONG?q.ask:q.bid):(side==UCEI05_SIDE_LONG?q.bid:q.ask));
   out_price=RoundTick(base+(adverse_up?1.0:-1.0)*MathMax(0.0,slippage_points)*s.point,s.tick_size,adverse_up); quote_side=adverse_up?"ask":"bid"; return(out_price>0.0);
 }
};
#endif
