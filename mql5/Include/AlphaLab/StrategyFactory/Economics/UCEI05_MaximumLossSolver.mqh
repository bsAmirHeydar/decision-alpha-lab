#ifndef UCEI05_MAXIMUM_LOSS_SOLVER_MQH
#define UCEI05_MAXIMUM_LOSS_SOLVER_MQH
#include "UCEI05_CapitalPolicies.mqh"
class CUCEI05MaximumLossSolver {
public:
 bool Solve(const UCEI05_RiskGeometry &g,const UCEI05_QuoteSnapshot &q,const UCEI05_SymbolSpec &s,const UCEI05_AccountSnapshot &a,const UCEI05_CostProfile &p,const UCEI05_CapitalBudget &b,UCEI05_EconomicEnvelope &e) const {
   ZeroMemory(e); e.treatment_id=g.treatment_id; e.side=g.side; e.risk_budget_cash=b.approved_cash; if(!b.accepted||b.approved_cash<=0.0){e.reason_code="zero_budget";return false;}
   CUCEI05ExecutablePriceKernel pk; string qs; double ep=(g.side==UCEI05_SIDE_LONG?p.entry_slippage_points_long:p.entry_slippage_points_short); double xp=(g.side==UCEI05_SIDE_LONG?p.exit_slippage_points_long:p.exit_slippage_points_short);
   pk.Compute(q,s,g.side,UCEI05_ROLE_ENTRY,g.order_kind,g.logical_entry,true,ep,e.entry_exec,qs); pk.Compute(q,s,g.side,UCEI05_ROLE_STOP_EXIT,UCEI05_ORDER_CLOSE,g.logical_stop,true,xp,e.stop_exec,qs); e.target_exec=g.logical_target; e.has_target=g.has_target;
   CUCEI05CostModel cm; UCEI05_CostBreakdown unit=cm.Estimate(p,s,q,g,1.0); double price_unit=MathAbs(e.entry_exec-e.stop_exec)*(s.tick_value_loss/s.tick_size); double per_lot=(price_unit+unit.total_cash)*MathMax(1.0,p.reserve_multiplier); if(per_lot<=0.0){e.reason_code="invalid_unit_risk";return false;}
   e.raw_volume=b.approved_cash/per_lot; CUCEI05BrokerConstraintSolver bc; string reason; if(!bc.Normalize(g,q,s,e.raw_volume,a.free_margin,e.entry_exec,e.stop_exec,e.target_exec,e.volume,e.margin_required,reason)){e.reason_code=reason;return false;}
   e.costs=cm.Estimate(p,s,q,g,e.volume); e.price_loss_cash=MathAbs(e.entry_exec-e.stop_exec)*(s.tick_value_loss/s.tick_size)*e.volume; e.maximum_loss_cash=(e.price_loss_cash+e.costs.total_cash)*MathMax(1.0,p.reserve_multiplier);
   while(e.volume>=s.volume_min && e.maximum_loss_cash>b.approved_cash+1e-8){e.volume=bc.FloorVolume(e.volume-s.volume_step,s); if(e.volume<s.volume_min)break; e.costs=cm.Estimate(p,s,q,g,e.volume); e.price_loss_cash=MathAbs(e.entry_exec-e.stop_exec)*(s.tick_value_loss/s.tick_size)*e.volume; e.maximum_loss_cash=(e.price_loss_cash+e.costs.total_cash)*MathMax(1.0,p.reserve_multiplier);}
   if(e.volume<s.volume_min){e.reason_code="risk_budget_below_minimum_volume";return false;} e.target_gross_cash=g.has_target?MathAbs(e.target_exec-e.entry_exec)*(s.tick_value_profit/s.tick_size)*e.volume:0.0; e.target_net_cash=e.target_gross_cash-e.costs.total_cash; e.accepted=true;e.reason_code="ok";return true;
 }
};
#endif
