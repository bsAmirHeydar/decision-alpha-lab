#ifndef UCEI05_COST_MODEL_MQH
#define UCEI05_COST_MODEL_MQH
#include "UCEI05_BrokerConstraintSolver.mqh"
class CUCEI05CostModel {
public:
 double Commission(const UCEI05_CostProfile &p,const double volume,const int entry_transactions,const int exit_transactions) const { return MathMax(p.minimum_commission,p.commission_per_lot_per_side*volume*(entry_transactions+exit_transactions)); }
 UCEI05_CostBreakdown Estimate(const UCEI05_CostProfile &p,const UCEI05_SymbolSpec &s,const UCEI05_QuoteSnapshot &q,const UCEI05_RiskGeometry &g,const double volume) const {
   UCEI05_CostBreakdown c; ZeroMemory(c); double value_per_price=s.tick_value_loss/s.tick_size*volume; c.spread_cash=(q.ask-q.bid)*value_per_price;
   double ep=(g.side==UCEI05_SIDE_LONG?p.entry_slippage_points_long:p.entry_slippage_points_short); double xp=(g.side==UCEI05_SIDE_LONG?p.exit_slippage_points_long:p.exit_slippage_points_short);
   c.entry_slippage_cash=ep*s.point*value_per_price; c.exit_slippage_cash=xp*s.point*value_per_price; c.commission_cash=Commission(p,volume,g.entry_transactions,g.exit_transactions); c.gap_reserve_cash=p.gap_reserve_points*s.point*value_per_price;
   c.total_cash=c.spread_cash+c.entry_slippage_cash+c.exit_slippage_cash+c.commission_cash+c.financing_cash+c.tax_cash+c.conversion_cash+c.gap_reserve_cash; return c;
 }
};
#endif
