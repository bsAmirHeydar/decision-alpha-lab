#ifndef UCEI05_CONFORMANCE_MQH
#define UCEI05_CONFORMANCE_MQH
#include "UCEI05_StressSuite.mqh"
class CUCEI05Conformance {
public:
 bool Run(string &reason) const {
   UCEI05_QuoteSnapshot q;q.symbol="EURUSD";q.bid=1.10000;q.ask=1.10010;q.source_time_ms=1700000000000;q.known_time_ms=q.source_time_ms;q.sequence=1;
   UCEI05_SymbolSpec s;s.symbol=q.symbol;s.digits=5;s.point=0.00001;s.tick_size=0.00001;s.tick_value_profit=1.0;s.tick_value_loss=1.0;s.contract_size=100000;s.volume_min=0.01;s.volume_max=100;s.volume_step=0.01;s.stops_level_points=20;s.leverage=100;s.margin_per_lot=0;s.known_time_ms=q.known_time_ms;
   UCEI05_AccountSnapshot a;a.account_id="acct";a.currency="USD";a.balance=100000;a.equity=100000;a.free_margin=50000;a.peak_equity=100000;a.known_time_ms=q.known_time_ms;
   UCEI05_CostProfile p;p.definition_id="cost.fx_standard@1.0.0";p.commission_per_lot_per_side=3.5;p.minimum_commission=0;p.entry_slippage_points_long=2;p.entry_slippage_points_short=2;p.exit_slippage_points_long=3;p.exit_slippage_points_short=3;p.gap_reserve_points=5;p.reserve_multiplier=1;p.max_quote_age_ms=2000;p.max_spec_age_ms=86400000;
   UCEI05_RiskGeometry g;g.treatment_id="ucet_fixture";g.side=UCEI05_SIDE_LONG;g.order_kind=UCEI05_ORDER_MARKET;g.logical_entry=1.10010;g.logical_stop=1.09810;g.logical_target=1.10410;g.has_target=true;g.entry_transactions=1;g.exit_transactions=1;
   CUCEI05CapitalPolicies cp; UCEI05_CapitalBudget b=cp.FixedCash(100); UCEI05_EconomicEnvelope e; CUCEI05MaximumLossSolver solver; if(!solver.Solve(g,q,s,a,p,b,e)){reason=e.reason_code;return false;} CUCEI05StressSuite stress;if(!stress.RiskWithinBudget(e)){reason="risk_budget";return false;}
   CUCEI05ReservationLedger ledger;if(!ledger.Reserve("res_fixture",a.account_id,g.treatment_id,e.maximum_loss_cash)){reason="reserve";return false;}if(ledger.Count()!=1){reason="ledger_count";return false;}reason="ok";return true;
 }
};
#endif
