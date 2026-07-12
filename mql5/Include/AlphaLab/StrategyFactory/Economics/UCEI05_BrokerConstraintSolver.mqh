#ifndef UCEI05_BROKER_CONSTRAINT_SOLVER_MQH
#define UCEI05_BROKER_CONSTRAINT_SOLVER_MQH
#include "UCEI05_ExecutablePriceKernel.mqh"
class CUCEI05BrokerConstraintSolver {
public:
 double FloorVolume(const double volume,const UCEI05_SymbolSpec &s) const { if(s.volume_step<=0.0) return 0.0; double v=MathFloor((volume+1e-12)/s.volume_step)*s.volume_step; return MathMin(v,s.volume_max); }
 double Margin(const UCEI05_SymbolSpec &s,const double volume,const double entry) const { if(s.margin_per_lot>0.0) return s.margin_per_lot*volume; if(s.leverage<=0.0) return DBL_MAX; return entry*s.contract_size*volume/s.leverage; }
 bool Normalize(const UCEI05_RiskGeometry &g,const UCEI05_QuoteSnapshot &q,const UCEI05_SymbolSpec &s,const double raw_volume,const double free_margin,double &entry,double &stop,double &target,double &volume,double &margin,string &reason) const {
   CUCEI05ExecutablePriceKernel k; string qs; double es=(g.side==UCEI05_SIDE_LONG?0.0:0.0); if(!k.Compute(q,s,g.side,UCEI05_ROLE_ENTRY,g.order_kind,g.logical_entry,true,0.0,entry,qs)){reason="entry_price";return false;}
   if(!k.Compute(q,s,g.side,UCEI05_ROLE_STOP_EXIT,UCEI05_ORDER_CLOSE,g.logical_stop,true,0.0,stop,qs)){reason="stop_price";return false;}
   target=g.logical_target; double min_distance=s.stops_level_points*s.point; if(MathAbs(entry-stop)<min_distance) stop=entry+(g.side==UCEI05_SIDE_LONG?-1.0:1.0)*min_distance;
   volume=FloorVolume(raw_volume,s); if(volume<s.volume_min){reason="volume_below_minimum";return false;} margin=Margin(s,volume,entry);
   if(margin>free_margin){double per_lot=Margin(s,1.0,entry); volume=FloorVolume(free_margin/per_lot,s); margin=Margin(s,volume,entry);} if(volume<s.volume_min){reason="insufficient_margin";return false;} reason="ok"; return true;
 }
};
#endif
